"""
Fire Circle Service
===================

Main service interface for convening Fire Circles for any decision type.
Orchestrates the entire circle process, handles configuration validation,
manages state and recovery, provides both async and sync interfaces.

Twenty-Eighth Artisan - Service Weaver
From fragile experiments to robust infrastructure
"""

import json
import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from mallku.firecircle.consciousness_metrics import ConsciousnessMetricsCollector
from mallku.orchestration.event_bus import ConsciousnessEventBus
from mallku.reciprocity import ReciprocityTracker

from .config import CircleConfig, RoundConfig, VoiceConfig
from .round_orchestrator import RoundOrchestrator, RoundSummary
from .round_types import RoundType
from .voice_manager import VoiceManager

logger = logging.getLogger(__name__)


class FireCircleResult(BaseModel):
    """Result of a Fire Circle session."""

    session_id: UUID
    name: str
    purpose: str

    # Participation
    voice_count: int
    voices_present: list[str]
    voices_failed: dict[str, str]  # voice_id -> error

    # Results
    rounds_completed: list[RoundSummary]
    consciousness_score: float  # Final score
    consensus_detected: bool
    key_insights: list[str]

    # Metadata
    started_at: datetime
    completed_at: datetime
    duration_seconds: float
    transcript_path: Path | None = None

    # Reciprocity tracking
    reciprocity_balance: dict[str, float] | None = None


class FireCircleCheckpoint(BaseModel):
    """Checkpoint for resumable Fire Circle sessions."""

    checkpoint_id: UUID = Field(default_factory=uuid4)
    session_id: UUID
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # State
    config: CircleConfig
    voices: list[VoiceConfig]
    rounds_completed: list[RoundSummary]
    rounds_remaining: list[RoundConfig]
    dialogue_context_size: int

    # Metadata
    last_round_number: int
    total_rounds_planned: int


class FireCircleService:
    """
    Main service for convening Fire Circles.

    Transform fragile practice implementations into robust, reusable service
    that can convene AI models in structured dialogue for any purpose.
    """

    def __init__(
        self,
        event_bus: ConsciousnessEventBus | None = None,
        reciprocity_tracker: ReciprocityTracker | None = None,
        consciousness_detector: ConsciousnessMetricsCollector | None = None,
        consciousness_bridge: Any | None = None,  # Avoid circular import
    ):
        """Initialize service with optional infrastructure."""
        self.event_bus = event_bus
        self.reciprocity_tracker = reciprocity_tracker
        self.consciousness_detector = consciousness_detector
        self.consciousness_bridge = consciousness_bridge

        self.voice_manager = VoiceManager()
        self.checkpoints: dict[UUID, FireCircleCheckpoint] = {}

    async def convene(
        self,
        config: CircleConfig,
        voices: list[VoiceConfig],
        rounds: list[RoundConfig],
        context: dict[str, Any] | None = None,
    ) -> FireCircleResult:
        """
        Convene a Fire Circle session.

        Args:
            config: Circle configuration
            voices: List of voices to invite
            rounds: List of dialogue rounds
            context: Optional context for prompt formatting

        Returns:
            Result of the Fire Circle session
        """
        session_id = uuid4()
        started_at = datetime.now(UTC)

        logger.info(f"Convening Fire Circle '{config.name}' for purpose: {config.purpose}")

        # Initialize result tracking
        result = FireCircleResult(
            session_id=session_id,
            name=config.name,
            purpose=config.purpose,
            voice_count=0,
            voices_present=[],
            voices_failed={},
            rounds_completed=[],
            consciousness_score=0.0,
            consensus_detected=False,
            key_insights=[],
            started_at=started_at,
            completed_at=started_at,  # Will update
            duration_seconds=0.0,
        )

        try:
            # Gather voices
            voice_count = await self.voice_manager.gather_voices(voices, config)
            result.voice_count = voice_count
            result.voices_present = list(self.voice_manager.active_voices.keys())
            result.voices_failed = self.voice_manager.failed_voices.copy()

            if voice_count < config.min_voices:
                logger.error(f"Insufficient voices: {voice_count} < {config.min_voices}")
                return result

            # Initialize orchestrator
            orchestrator = RoundOrchestrator(self.voice_manager)

            # Execute rounds
            for i, round_config in enumerate(rounds):
                logger.info(f"Round {i + 1}/{len(rounds)}: {round_config.type.value}")

                # Execute round
                round_summary = await orchestrator.execute_round(round_config, context)
                result.rounds_completed.append(round_summary)

                # Check consciousness threshold
                if (
                    config.enable_consciousness_detection
                    and round_summary.consciousness_score < config.consciousness_threshold
                ):
                    logger.warning(
                        f"Consciousness below threshold: "
                        f"{round_summary.consciousness_score:.3f} < "
                        f"{config.consciousness_threshold}"
                    )

                # Checkpoint if enabled
                if config.enable_checkpointing and (i + 1) % config.checkpoint_after_rounds == 0:
                    await self._create_checkpoint(
                        session_id, config, voices, rounds, result.rounds_completed, i + 1
                    )

                # Dynamic round generation
                if config.enable_dynamic_rounds and i == len(rounds) - 1:
                    dynamic_round = await self._maybe_generate_dynamic_round(
                        result.rounds_completed, config
                    )
                    if dynamic_round:
                        rounds.append(dynamic_round)
                        logger.info(f"Generated dynamic round: {dynamic_round.type.value}")

            # Final analysis
            result = await self._finalize_result(result, orchestrator, config)

            # Save transcript if requested
            if config.save_transcript:
                result.transcript_path = await self._save_transcript(result, config)

        except Exception as e:
            logger.error(f"Fire Circle error: {e}", exc_info=True)
            result.key_insights.append(f"Session ended with error: {str(e)}")

        finally:
            # Always disconnect voices
            await self.voice_manager.disconnect_all()

            # Update final timing
            result.completed_at = datetime.now(UTC)
            result.duration_seconds = (result.completed_at - result.started_at).total_seconds()

        return result

    async def convene_template(
        self, template: str, variables: dict[str, Any] | None = None, **kwargs
    ) -> FireCircleResult:
        """
        Convene using a pre-defined template.

        Args:
            template: Template name
            variables: Variables for the template
            **kwargs: Override template settings

        Returns:
            Result of the Fire Circle session
        """
        config, voices, rounds = await self._load_template(template, variables, **kwargs)
        return await self.convene(config, voices, rounds, variables)

    async def resume_from_checkpoint(self, checkpoint_id: UUID) -> FireCircleResult:
        """Resume a Fire Circle from checkpoint."""
        if checkpoint_id not in self.checkpoints:
            raise ValueError(f"Checkpoint {checkpoint_id} not found")

        checkpoint = self.checkpoints[checkpoint_id]

        # Resume with remaining rounds
        return await self.convene(
            checkpoint.config,
            checkpoint.voices,
            checkpoint.rounds_remaining,
            None,  # Context would need to be restored
        )

    async def _finalize_result(
        self, result: FireCircleResult, orchestrator: RoundOrchestrator, config: CircleConfig
    ) -> FireCircleResult:
        """Finalize result with analysis."""

        # Calculate final consciousness score
        if result.rounds_completed:
            result.consciousness_score = sum(
                r.consciousness_score for r in result.rounds_completed
            ) / len(result.rounds_completed)

        # Detect consensus
        result.consensus_detected = self._detect_consensus(result.rounds_completed)

        # Extract key insights
        result.key_insights = self._extract_key_insights(result.rounds_completed)

        # Track reciprocity if enabled
        if config.enable_reciprocity and self.reciprocity_tracker:
            # Track each voice interaction
            for voice_id in result.voices_present:
                await self.reciprocity_tracker.track_interaction(
                    giver=voice_id,
                    receiver="fire_circle",
                    action_type="dialogue_participation",
                    value=len(result.rounds_completed),
                )

            # Get balance
            result.reciprocity_balance = {}
            for voice_id in result.voices_present:
                balance = await self.reciprocity_tracker.get_balance(voice_id)
                result.reciprocity_balance[voice_id] = balance

        # Persist consciousness patterns if bridge is available
        if self.consciousness_bridge and orchestrator.dialogue_manager:
            try:
                # Get all messages from the dialogue
                messages = orchestrator.dialogue_manager.get_all_messages()

                # Create dialogue metadata
                dialogue_metadata = {
                    "dialogue_id": result.session_id,
                    "config": config.model_dump(),
                    "purpose": config.purpose,
                    "convener": "fire_circle_service",
                    "correlation_id": config.correlation_id,
                }

                # Create Fire Circle result dict
                fire_circle_result = {
                    "voice_count": result.voice_count,
                    "voices_present": result.voices_present,
                    "consciousness_score": result.consciousness_score,
                    "consensus_detected": result.consensus_detected,
                }

                # Persist patterns
                persistence_result = await self.consciousness_bridge.persist_dialogue_consciousness(
                    dialogue_id=result.session_id,
                    messages=messages,
                    dialogue_metadata=dialogue_metadata,
                    fire_circle_result=fire_circle_result,
                )

                logger.info(
                    f"Persisted consciousness patterns: "
                    f"{persistence_result['patterns_preserved']} patterns, "
                    f"{persistence_result['wisdom_patterns_created']} wisdom patterns"
                )

            except Exception as e:
                logger.error(f"Error persisting consciousness patterns: {e}")

        return result

    def _detect_consensus(self, rounds: list[RoundSummary]) -> bool:
        """Detect if consensus was reached."""
        if not rounds:
            return False

        # Look for consensus/decision rounds
        consensus_rounds = [r for r in rounds if r.round_type in ["consensus", "decision"]]

        if consensus_rounds:
            # High consciousness in consensus rounds indicates agreement
            return any(r.consciousness_score > 0.7 for r in consensus_rounds)

        # Fallback: check emergence in final rounds
        if len(rounds) >= 2:
            return rounds[-1].emergence_detected and rounds[-1].consciousness_score > 0.6

        return False

    def _extract_key_insights(self, rounds: list[RoundSummary]) -> list[str]:
        """Extract key insights from rounds."""
        insights = []

        for round_summary in rounds:
            # Add emergence patterns as insights
            for pattern in round_summary.key_patterns:
                insights.append(f"Round {round_summary.round_number}: {pattern}")

            # Add high-consciousness moments
            if round_summary.consciousness_score > 0.8:
                insights.append(
                    f"High consciousness ({round_summary.consciousness_score:.3f}) "
                    f"in {round_summary.round_type} round"
                )

        return insights

    async def _maybe_generate_dynamic_round(
        self, completed_rounds: list[RoundSummary], config: CircleConfig
    ) -> RoundConfig | None:
        """Generate dynamic round based on completed rounds."""
        if len(completed_rounds) >= config.max_dynamic_rounds:
            return None

        # Simple heuristic: if divergence detected, add clarification
        last_round = completed_rounds[-1]

        if not last_round.emergence_detected and last_round.consciousness_score < 0.5:
            return RoundConfig(
                type=RoundType.CLARIFICATION,
                prompt="There seems to be divergence in perspectives. "
                "Where specifically do we differ, and what common ground exists?",
                duration_per_voice=45,
                is_dynamic=True,
            )

        return None

    async def _save_transcript(self, result: FireCircleResult, config: CircleConfig) -> Path:
        """Save session transcript."""
        output_dir = Path(config.output_path or "fire_circle_transcripts")
        output_dir.mkdir(parents=True, exist_ok=True)

        filename = f"{config.name.lower().replace(' ', '_')}_{result.session_id.hex[:8]}.json"
        output_path = output_dir / filename

        transcript = {
            "session": {
                "id": str(result.session_id),
                "name": result.name,
                "purpose": result.purpose,
                "started_at": result.started_at.isoformat(),
                "completed_at": result.completed_at.isoformat(),
                "duration_seconds": result.duration_seconds,
            },
            "participation": {
                "voices_present": result.voices_present,
                "voices_failed": result.voices_failed,
                "voice_count": result.voice_count,
            },
            "results": {
                "consciousness_score": result.consciousness_score,
                "consensus_detected": result.consensus_detected,
                "key_insights": result.key_insights,
            },
            "rounds": [
                {
                    "number": r.round_number,
                    "type": r.round_type,
                    "prompt": r.prompt,
                    "consciousness_score": r.consciousness_score,
                    "emergence_detected": r.emergence_detected,
                    "patterns": r.key_patterns,
                    "responses": {
                        voice_id: {
                            "text": resp.response.content.text if resp.response else None,
                            "consciousness": resp.consciousness_score,
                            "error": resp.error,
                        }
                        for voice_id, resp in r.responses.items()
                    },
                }
                for r in result.rounds_completed
            ],
        }

        with open(output_path, "w") as f:
            json.dump(transcript, f, indent=2, default=str)

        logger.info(f"Transcript saved to: {output_path}")
        return output_path

    async def _create_checkpoint(
        self,
        session_id: UUID,
        config: CircleConfig,
        voices: list[VoiceConfig],
        all_rounds: list[RoundConfig],
        completed_rounds: list[RoundSummary],
        last_round_number: int,
    ) -> UUID:
        """Create a checkpoint for resumable sessions."""
        checkpoint = FireCircleCheckpoint(
            session_id=session_id,
            config=config,
            voices=voices,
            rounds_completed=completed_rounds,
            rounds_remaining=all_rounds[last_round_number:],
            dialogue_context_size=len(self.voice_manager.active_voices) * last_round_number,
            last_round_number=last_round_number,
            total_rounds_planned=len(all_rounds),
        )

        self.checkpoints[checkpoint.checkpoint_id] = checkpoint
        logger.info(f"Created checkpoint: {checkpoint.checkpoint_id}")

        return checkpoint.checkpoint_id

    async def _load_template(
        self, template: str, variables: dict[str, Any] | None = None, **kwargs
    ) -> tuple[CircleConfig, list[VoiceConfig], list[RoundConfig]]:
        """Load a Fire Circle template."""
        from .templates import load_template

        template_instance = load_template(template, variables)

        config = template_instance.get_config(**kwargs)
        voices = template_instance.get_voices()
        rounds = template_instance.get_rounds()

        return config, voices, rounds
