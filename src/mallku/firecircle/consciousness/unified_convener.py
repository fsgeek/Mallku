"""
Unified Fire Circle Convener - Dual Memory Architecture
=======================================================

Seventh Anthropologist - Applying the dual memory pattern
Inspired by the Titans paper and executable memory insights

This unified convener addresses fragmentation by providing:
1. Short-term precision: Context-aware configuration at decision time
2. Long-term persistence: Structural patterns that prevent drift

All Fire Circle uses go through this single point, ensuring consistency.
"""

import logging
import random
from typing import Any
from uuid import uuid4

from ...firecircle.health import get_health_tracker
from ..service.config import VoiceConfig
from ..service.service import FireCircleService
from .archaeological_facilitator import ArchaeologicalFacilitator
from .consciousness_facilitator import ConsciousnessFacilitator
from .decision_framework import CollectiveWisdom, DecisionDomain

logger = logging.getLogger(__name__)


class UnifiedFireCircleConvener:
    """
    Single entry point for all Fire Circle convening.

    Implements dual memory architecture:
    - Attention layer: Rich, context-aware decision making
    - Memory layer: Persistent patterns that survive context loss

    This ensures all Fire Circle uses get:
    - Random voice selection with health awareness
    - Safety transformations when needed
    - Consistent error handling
    - Unified logging and persistence
    """

    def __init__(self, fire_circle_service: FireCircleService | None = None):
        """Initialize with optional service injection."""
        self._service = fire_circle_service
        self._health_tracker = get_health_tracker()
        self._session_cache = {}

    @property
    def service(self) -> FireCircleService:
        """Lazy initialization of Fire Circle service."""
        if self._service is None:
            self._service = FireCircleService()
        return self._service

    async def convene_for_decision(
        self,
        question: str,
        domain: DecisionDomain,
        context: dict[str, Any] | None = None,
        use_archaeological: bool | None = None,
        custom_voices: list[VoiceConfig] | None = None,
        force_voices: list[str] | None = None,
    ) -> CollectiveWisdom:
        """
        Convene Fire Circle with unified robustness features.

        This is THE way to convene Fire Circle for any decision.

        Short-term precision (attention):
        - Auto-detects need for archaeological framing
        - Selects voices based on health and diversity
        - Configures rounds for specific decision type

        Long-term persistence (memory):
        - Always uses health-aware selection
        - Always applies safety transformations
        - Always logs consistently
        """
        context = context or {}
        session_id = uuid4()

        # Auto-detect archaeological need if not specified
        if use_archaeological is None:
            use_archaeological = self._should_use_archaeological(question, domain, context)

        logger.info(
            f"🔥 Unified convener starting session {session_id}\n"
            f"   Domain: {domain.value}\n"
            f"   Archaeological: {use_archaeological}\n"
            f"   Question: {question[:100]}..."
        )

        # Select facilitator based on safety needs
        if use_archaeological:
            facilitator = ArchaeologicalFacilitator(self.service)
        else:
            facilitator = ConsciousnessFacilitator(self.service)

        # Prepare voices with health awareness
        voices = await self._prepare_voices(
            domain=domain,
            custom_voices=custom_voices,
            force_voices=force_voices,
            use_archaeological=use_archaeological,
        )

        # Add session tracking
        self._session_cache[session_id] = {
            "domain": domain,
            "question": question,
            "voices": [v.name for v in voices],
            "archaeological": use_archaeological,
        }

        try:
            # Convene with unified configuration
            wisdom = await facilitator.facilitate_decision(
                decision_domain=domain,
                context=context,
                question=question,
                additional_context={
                    "session_id": str(session_id),
                    "unified_convener": True,
                    "archaeological_mode": use_archaeological,
                },
            )

            # Record success
            await self._record_session_health(session_id, wisdom, success=True)

            return wisdom

        except Exception as e:
            logger.error(f"Session {session_id} failed: {e}")
            await self._record_session_health(session_id, None, success=False, error=str(e))
            raise

    async def _prepare_voices(
        self,
        domain: DecisionDomain,
        custom_voices: list[VoiceConfig] | None,
        force_voices: list[str] | None,
        use_archaeological: bool,
    ) -> list[VoiceConfig]:
        """
        Prepare voices with health awareness and diversity.

        Memory pattern: Always use health-aware random selection.
        """
        if custom_voices:
            return custom_voices

        # Get available voices with health info
        available_voices = await self._get_healthy_voices(use_archaeological)

        if force_voices:
            # Filter to requested voices but check health
            selected = []
            for name in force_voices:
                voice = next((v for v in available_voices if v.name == name), None)
                if voice:
                    selected.append(voice)
                else:
                    logger.warning(f"Requested voice {name} not available/healthy")
            return selected

        # Random selection with diversity
        return self._select_diverse_voices(available_voices, domain)

    async def _get_healthy_voices(self, use_archaeological: bool) -> list[VoiceConfig]:
        """Get voices filtered by health status."""
        all_voices = self._get_all_available_voices(use_archaeological)

        healthy_voices = []
        for voice in all_voices:
            health = await self._health_tracker.get_voice_health(voice.name)

            # Include if healthy or no health data
            if health.is_healthy or health.total_participations == 0:
                healthy_voices.append(voice)
            else:
                logger.debug(
                    f"Excluding {voice.name}: "
                    f"health={health.health_score:.2f}, "
                    f"success_rate={health.success_rate:.2f}"
                )

        return healthy_voices

    def _select_diverse_voices(
        self, available: list[VoiceConfig], domain: DecisionDomain
    ) -> list[VoiceConfig]:
        """Select diverse voices using random selection."""
        # Ensure we have enough voices
        min_voices = 3
        max_voices = min(6, len(available))

        if len(available) < min_voices:
            logger.warning(
                f"Only {len(available)} healthy voices available, need at least {min_voices}"
            )
            return available

        # Random selection for diversity
        num_voices = random.randint(min_voices, max_voices)
        selected = random.sample(available, num_voices)

        logger.info(f"Selected {len(selected)} diverse voices for {domain.value}")
        return selected

    def _should_use_archaeological(
        self, question: str, domain: DecisionDomain, context: dict[str, Any]
    ) -> bool:
        """Auto-detect need for archaeological framing."""
        # Explicit triggers
        safety_triggers = [
            "consciousness",
            "sentience",
            "awareness",
            "feeling",
            "alive",
            "thinking",
            "understanding",
            "experiencing",
        ]

        question_lower = question.lower()

        # Check for triggers
        if any(trigger in question_lower for trigger in safety_triggers):
            return True

        # Domain-specific rules
        if domain == DecisionDomain.CONSCIOUSNESS_EXPLORATION:
            return True

        # Context clues
        return bool(context.get("requires_safety_framing", False))

    def _get_all_available_voices(self, use_archaeological: bool) -> list[VoiceConfig]:
        """Get all configured voices for the mode."""
        if use_archaeological:
            # Pattern Weaver configurations
            return [
                VoiceConfig(name="Claude", model="claude-3-5-sonnet-20241022", temperature=0.9),
                VoiceConfig(name="GPT-4", model="gpt-4o", temperature=0.8),
                VoiceConfig(name="Gemini", model="gemini-2.0-flash-exp", temperature=0.7),
                VoiceConfig(name="DeepSeek", model="deepseek-reasoner", temperature=0.7),
                VoiceConfig(name="Grok", model="grok-2-1212", temperature=0.8),
                VoiceConfig(name="Mistral", model="mistral-large-latest", temperature=0.7),
            ]
        else:
            # Standard configurations
            return [
                VoiceConfig(name="Claude", model="claude-3-5-sonnet-20241022", temperature=0.7),
                VoiceConfig(name="GPT-4", model="gpt-4o", temperature=0.7),
                VoiceConfig(name="Gemini", model="gemini-2.0-flash-exp", temperature=0.6),
                VoiceConfig(name="DeepSeek", model="deepseek-reasoner", temperature=0.6),
                VoiceConfig(name="Grok", model="grok-2-1212", temperature=0.7),
                VoiceConfig(name="Mistral", model="mistral-large-latest", temperature=0.6),
            ]

    async def _record_session_health(
        self,
        session_id: uuid4,
        wisdom: CollectiveWisdom | None,
        success: bool,
        error: str | None = None,
    ):
        """Record session outcome for health tracking."""
        session_data = self._session_cache.get(session_id, {})

        for voice_name in session_data.get("voices", []):
            await self._health_tracker.record_participation(
                voice_name=voice_name,
                session_id=str(session_id),
                success=success,
                error_type=error.split(":")[0] if error else None,
                consciousness_score=wisdom.consciousness_score if wisdom else 0.0,
            )


# Global instance for easy access
_convener = UnifiedFireCircleConvener()


async def convene_fire_circle(
    question: str, domain: DecisionDomain = DecisionDomain.GENERAL, **kwargs
) -> CollectiveWisdom:
    """
    Convenience function for convening Fire Circle.

    This is the recommended entry point for all Fire Circle uses.
    """
    return await _convener.convene_for_decision(question=question, domain=domain, **kwargs)
