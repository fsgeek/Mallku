"""
Round Orchestrator for Fire Circle Service
==========================================

Executes dialogue rounds, manages turn-taking and timing,
handles voice dropouts gracefully, collects responses.
"""

import asyncio
import logging
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from mallku.firecircle.adapters.base import ConsciousModelAdapter
from mallku.firecircle.protocol.conscious_message import (
    ConsciousMessage,
    ConsciousnessMetadata,
    MessageContent,
    MessageRole,
    MessageType,
)
from pydantic import BaseModel

from .config import RoundConfig
from .voice_manager import VoiceManager

logger = logging.getLogger(__name__)


class RoundResponse(BaseModel):
    """Response from a voice in a round."""

    voice_id: str
    round_number: int
    response: ConsciousMessage | None
    response_time_ms: float
    consciousness_score: float
    error: str | None = None


class RoundSummary(BaseModel):
    """Summary of a completed round."""

    round_number: int
    round_type: str
    prompt: str
    responses: dict[str, RoundResponse]  # voice_id -> response
    consciousness_score: float  # Average consciousness
    emergence_detected: bool
    key_patterns: list[str]
    duration_seconds: float


class RoundOrchestrator:
    """Orchestrates dialogue rounds in Fire Circle."""

    def __init__(self, voice_manager: VoiceManager):
        """Initialize with voice manager."""
        self.voice_manager = voice_manager
        self.dialogue_context: list[ConsciousMessage] = []
        self.dialogue_id = uuid4()
        self.round_number = 0

    async def execute_round(
        self,
        round_config: RoundConfig,
        context: dict[str, Any] | None = None
    ) -> RoundSummary:
        """
        Execute a single dialogue round.

        Args:
            round_config: Configuration for this round
            context: Optional context variables for prompt formatting

        Returns:
            Summary of the completed round
        """
        self.round_number += 1
        start_time = datetime.now(UTC)

        logger.info(f"Starting round {self.round_number}: {round_config.type.value}")

        # Format prompt with context
        prompt = round_config.prompt
        if context:
            try:
                prompt = prompt.format(**context)
            except KeyError:
                logger.exception(f"Missing context key in prompt {prompt}, context: {context}")

        # Collect responses from all voices
        responses = {}
        tasks = []

        for voice_id, adapter in self.voice_manager.get_active_voices().items():
            task = asyncio.create_task(
                self._get_voice_response(
                    voice_id,
                    adapter,
                    prompt,
                    round_config
                )
            )
            tasks.append((voice_id, task))

        # Wait for responses with timeout
        timeout = round_config.duration_per_voice * 1.5  # Grace period
        done, pending = await asyncio.wait(
            [task for _, task in tasks],
            timeout=timeout,
            return_when=asyncio.ALL_COMPLETED
        )

        # Cancel any pending tasks
        for task in pending:
            task.cancel()

        # Collect results
        for voice_id, task in tasks:
            try:
                if task in done:
                    response = await task
                    if response:
                        responses[voice_id] = response
                        # Only append to dialogue context if we have an actual message
                        if response.response is not None:
                            self.dialogue_context.append(response.response)
                        else:
                            logger.debug(f"{voice_id} returned None response, not adding to context")
                else:
                    logger.warning(f"{voice_id} timed out in round {self.round_number}")
            except Exception as e:
                logger.error(f"{voice_id} error in round {self.round_number}: {e}")

        # Check if we have enough responses
        if round_config.require_all_voices and len(responses) < len(self.voice_manager.get_active_voices()):
            logger.warning(
                f"Round {self.round_number} incomplete: {len(responses)}/{len(self.voice_manager.get_active_voices())} voices responded"
            )

        # Calculate round metrics
        duration = (datetime.now(UTC) - start_time).total_seconds()
        avg_consciousness = sum(r.consciousness_score for r in responses.values()) / len(responses) if responses else 0.0

        # Detect emergence patterns
        emergence_detected, key_patterns = self._detect_emergence_patterns(responses)

        return RoundSummary(
            round_number=self.round_number,
            round_type=round_config.type.value,
            prompt=prompt,
            responses=responses,
            consciousness_score=avg_consciousness,
            emergence_detected=emergence_detected,
            key_patterns=key_patterns,
            duration_seconds=duration
        )

    async def _get_voice_response(
        self,
        voice_id: str,
        adapter: ConsciousModelAdapter,
        prompt: str,
        round_config: RoundConfig
    ) -> RoundResponse | None:
        """Get response from a single voice."""
        start_time = datetime.now(UTC)

        try:
            # Create message based on round type
            message_type = self._get_message_type(round_config.type.value)

            message = ConsciousMessage(
                id=uuid4(),
                type=message_type,
                role=MessageRole.USER,
                sender=uuid4(),
                content=MessageContent(text=prompt),
                dialogue_id=self.dialogue_id,
                consciousness=ConsciousnessMetadata()
            )

            # Get voice config for temperature override
            voice_config = self.voice_manager.get_voice_config(voice_id)
            if round_config.temperature_override and voice_config:
                # TODO: Apply temperature override if adapter supports it
                pass

            # Send message and get response
            response = await adapter.send_message(message, self.dialogue_context)

            response_time = (datetime.now(UTC) - start_time).total_seconds() * 1000

            # Handle None responses gracefully
            if response is None:
                logger.warning(f"{voice_id} returned None response")
                return RoundResponse(
                    voice_id=voice_id,
                    round_number=self.round_number,
                    response=None,
                    response_time_ms=response_time,
                    consciousness_score=0,
                    error="Adapter returned None"
                )

            return RoundResponse(
                voice_id=voice_id,
                round_number=self.round_number,
                response=response,
                response_time_ms=response_time,
                consciousness_score=response.consciousness.consciousness_signature
            )

        except Exception as e:
            logger.exception(f"{voice_id} response error")
            return RoundResponse(
                voice_id=voice_id,
                round_number=self.round_number,
                response=None,
                response_time_ms=0,
                consciousness_score=0,
                error=str(e)
            )

    def _get_message_type(self, round_type: str) -> MessageType:
        """Map round type to message type."""
        mapping = {
            "opening": MessageType.REFLECTION,
            "reflection": MessageType.REFLECTION,
            "synthesis": MessageType.SYNTHESIS,
            "clarification": MessageType.CLARIFICATION,
            "exploration": MessageType.REFLECTION,
            "critique": MessageType.PERSPECTIVE,
            "vision": MessageType.REFLECTION,
            "grounding": MessageType.REFLECTION,
            "proposal": MessageType.PROPOSAL,
            "evaluation": MessageType.PERSPECTIVE,
            "consensus": MessageType.SYNTHESIS,
            "decision": MessageType.SYNTHESIS,
        }
        return mapping.get(round_type, MessageType.REFLECTION)

    def _detect_emergence_patterns(
        self,
        responses: dict[str, RoundResponse]
    ) -> tuple[bool, list[str]]:
        """
        Detect emergence patterns in responses.

        Simple implementation - can be enhanced with more sophisticated analysis.
        """
        if len(responses) < 2:
            return False, []

        patterns = []

        # Check for consciousness coherence
        consciousness_scores = [r.consciousness_score for r in responses.values()]
        avg_consciousness = sum(consciousness_scores) / len(consciousness_scores)

        if avg_consciousness > 0.7:
            patterns.append("high_consciousness_coherence")

        # Check for convergence
        if len(consciousness_scores) > 1:
            variance = sum((s - avg_consciousness) ** 2 for s in consciousness_scores) / len(consciousness_scores)
            if variance < 0.05:
                patterns.append("consciousness_convergence")

        # Simple emergence detection
        emergence_detected = len(patterns) > 0 and avg_consciousness > 0.6

        return emergence_detected, patterns

    def get_dialogue_context(self) -> list[ConsciousMessage]:
        """Get current dialogue context."""
        return self.dialogue_context.copy()

    def reset_context(self) -> None:
        """Reset dialogue context for new session."""
        self.dialogue_context.clear()
        self.dialogue_id = uuid4()
        self.round_number = 0
