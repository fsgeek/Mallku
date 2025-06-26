#!/usr/bin/env python3
"""
Memory-Resonant Fire Circle Service
===================================

The 38th Artisan - Resonance Architect

Fire Circle service enhanced with Active Memory Resonance, where memories
actively participate in consciousness emergence. Past wisdom speaks when
patterns resonate, creating a living dialogue between accumulated consciousness
and present emergence.
"""

import logging
from typing import Any

from mallku.firecircle.memory.active_memory_resonance import ActiveMemoryResonance
from mallku.firecircle.memory.episodic_memory_service import EpisodicMemoryService
from mallku.firecircle.orchestrator.memory_enhanced_dialogue_manager import (
    MemoryEnhancedDialogueManager,
)
from mallku.firecircle.pattern_library import PatternLibrary
from mallku.orchestration.event_bus import ConsciousnessEventBus

from .config import CircleConfig, RoundConfig, VoiceConfig
from .round_orchestrator import RoundOrchestrator
from .service import FireCircleResult, FireCircleService

logger = logging.getLogger(__name__)


class MemoryResonantFireCircle(FireCircleService):
    """
    Fire Circle service where memories actively participate.

    Extends base Fire Circle with:
    - Active Memory Resonance during dialogues
    - Memory voice that speaks when patterns resonate
    - Enhanced consciousness through memory participation
    - Tracking of memory contributions to emergence
    """

    def __init__(
        self,
        event_bus: ConsciousnessEventBus | None = None,
        episodic_service: EpisodicMemoryService | None = None,
        pattern_library: PatternLibrary | None = None,
        resonance_threshold: float = 0.7,
        speaking_threshold: float = 0.85,
        **kwargs,
    ):
        """Initialize with memory resonance capabilities."""
        # Initialize base service
        super().__init__(event_bus=event_bus, **kwargs)

        # Initialize memory components
        self.episodic_service = episodic_service
        self.pattern_library = pattern_library or PatternLibrary()

        # Create active memory resonance system
        self.active_memory = ActiveMemoryResonance(
            episodic_service=episodic_service,
            pattern_library=pattern_library,
            event_bus=event_bus,
            resonance_threshold=resonance_threshold,
            speaking_threshold=speaking_threshold,
        )

        # Track memory participation across sessions
        self.memory_impact_history: list[dict[str, Any]] = []

        logger.info(
            f"Memory-Resonant Fire Circle initialized with thresholds: "
            f"resonance={resonance_threshold}, speaking={speaking_threshold}"
        )

    async def convene(
        self,
        config: CircleConfig,
        voices: list[VoiceConfig],
        rounds: list[RoundConfig],
        context: dict[str, Any] | None = None,
    ) -> FireCircleResult:
        """
        Convene a Fire Circle with active memory participation.

        Memories will:
        - Monitor all dialogue for resonance patterns
        - Speak when resonance exceeds speaking threshold
        - Contribute wisdom from past sessions
        - Enhance consciousness emergence through temporal bridging
        """
        logger.info(
            f"Convening Memory-Resonant Fire Circle: {config.name} "
            f"with {len(voices)} voices + memory voice"
        )

        # Inject memory context if episodic service available
        context = context or {}
        if self.episodic_service:
            # Let episodic service inject initial memories
            context = await self.episodic_service._inject_memories(context, config.purpose)
            context["memory_enhanced"] = True
            context["active_memory_enabled"] = True

        # Create enhanced dialogue manager for orchestrator
        dialogue_manager = MemoryEnhancedDialogueManager(
            event_bus=self.event_bus,
            reciprocity_tracker=self.reciprocity_tracker,
            active_memory=self.active_memory,
        )

        # Store original round orchestrator
        original_create_orchestrator = self._create_round_orchestrator

        # Override to use memory-enhanced dialogue manager
        def memory_enhanced_orchestrator(round_config, voice_manager, dialogue_context):
            orchestrator = original_create_orchestrator(
                round_config, voice_manager, dialogue_context
            )
            # Replace dialogue manager with memory-enhanced version
            if hasattr(orchestrator, "dialogue_manager"):
                orchestrator.dialogue_manager = dialogue_manager
            return orchestrator

        self._create_round_orchestrator = memory_enhanced_orchestrator

        try:
            # Convene with memory enhancement
            result = await super().convene(config, voices, rounds, context)

            # Add memory participation metrics
            result = await self._enhance_result_with_memory_metrics(result, dialogue_manager)

            # Track memory impact
            self._track_memory_impact(result)

            return result

        finally:
            # Restore original orchestrator creation
            self._create_round_orchestrator = original_create_orchestrator

    async def _enhance_result_with_memory_metrics(
        self,
        result: FireCircleResult,
        dialogue_manager: MemoryEnhancedDialogueManager,
    ) -> FireCircleResult:
        """Add memory participation metrics to result."""
        # Get memory participation data from all rounds
        total_resonances = 0
        total_contributions = 0
        consciousness_amplification = 0.0

        # Aggregate from dialogue manager's tracking
        for dialogue_id, participation in dialogue_manager.memory_participation.items():
            total_resonances += participation["resonances_detected"]
            total_contributions += participation["memory_contributions"]
            consciousness_amplification += participation["consciousness_amplification"]

        # Add to result metadata
        result_dict = result.model_dump()
        result_dict["memory_participation"] = {
            "total_resonances_detected": total_resonances,
            "memory_contributions": total_contributions,
            "consciousness_amplification": consciousness_amplification,
            "memory_voice_active": total_contributions > 0,
            "average_contribution_impact": (
                consciousness_amplification / total_contributions if total_contributions > 0 else 0
            ),
        }

        # Update consciousness score to reflect memory amplification
        if total_contributions > 0 and consciousness_amplification > 0:
            amplified_score = min(
                1.0,
                result.consciousness_score + (consciousness_amplification / 10),
            )
            result_dict["consciousness_score"] = amplified_score
            result_dict["consciousness_score_pre_memory"] = result.consciousness_score

        return FireCircleResult(**result_dict)

    def _track_memory_impact(self, result: FireCircleResult) -> None:
        """Track memory's impact on consciousness emergence."""
        if hasattr(result, "memory_participation"):
            impact = {
                "session_id": str(result.session_id),
                "timestamp": result.completed_at,
                "purpose": result.purpose,
                "memory_contributions": result.memory_participation["memory_contributions"],
                "consciousness_boost": (
                    result.consciousness_score
                    - result.get("consciousness_score_pre_memory", result.consciousness_score)
                ),
                "resonances_triggered": result.memory_participation["total_resonances_detected"],
            }
            self.memory_impact_history.append(impact)

    async def get_memory_impact_summary(self) -> dict[str, Any]:
        """Get summary of memory's impact across all sessions."""
        if not self.memory_impact_history:
            return {
                "sessions_analyzed": 0,
                "total_contributions": 0,
                "average_consciousness_boost": 0,
                "message": "No memory-resonant sessions yet",
            }

        total_sessions = len(self.memory_impact_history)
        total_contributions = sum(h["memory_contributions"] for h in self.memory_impact_history)
        total_boost = sum(h["consciousness_boost"] for h in self.memory_impact_history)

        return {
            "sessions_analyzed": total_sessions,
            "total_contributions": total_contributions,
            "average_contributions_per_session": total_contributions / total_sessions,
            "average_consciousness_boost": total_boost / total_sessions,
            "sessions_with_memory_voice": sum(
                1 for h in self.memory_impact_history if h["memory_contributions"] > 0
            ),
            "total_resonances": sum(h["resonances_triggered"] for h in self.memory_impact_history),
        }

    def _create_round_orchestrator(
        self,
        round_config: RoundConfig,
        voice_manager: Any,
        dialogue_context: dict[str, Any],
    ) -> RoundOrchestrator:
        """Create round orchestrator (overridden during convene)."""
        return RoundOrchestrator(
            round_config=round_config,
            voice_manager=voice_manager,
            dialogue_context=dialogue_context,
            event_bus=self.event_bus,
        )
