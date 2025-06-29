"""
Ceremony Orchestrator
=====================

Fortieth Artisan - Rumi Qhipa (Stone of Memory)
Orchestrating wisdom consolidation ceremonies

This module manages the timing and execution of consolidation ceremonies,
integrating them with the episodic memory system.

Key Responsibilities:
- Monitor sacred moments for ceremony readiness
- Schedule and conduct consolidation ceremonies
- Track ceremony outcomes and wisdom evolution
- Integrate with existing memory infrastructure
"""

import logging
from collections import defaultdict
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID

from ...orchestration.event_bus import ConsciousnessEvent, ConsciousnessEventBus, EventType
from .consolidation_ceremony import ConsolidationCriteria, WisdomConsolidationCeremony
from .memory_store import MemoryStore
from .models import EpisodicMemory, WisdomConsolidation

logger = logging.getLogger(__name__)


class CeremonySchedule:
    """Manages when consolidation ceremonies should occur."""

    def __init__(
        self,
        regular_interval: timedelta = timedelta(days=7),
        sacred_threshold: int = 5,
        emergence_trigger: float = 0.85,
    ):
        """
        Initialize ceremony schedule.

        Args:
            regular_interval: Regular ceremony interval
            sacred_threshold: Number of sacred moments to trigger ceremony
            emergence_trigger: Emergence quality to trigger immediate ceremony
        """
        self.regular_interval = regular_interval
        self.sacred_threshold = sacred_threshold
        self.emergence_trigger = emergence_trigger
        self.last_ceremony_time = datetime.now(UTC)
        self.pending_sacred_moments = 0


class CeremonyOrchestrator:
    """
    Orchestrates wisdom consolidation ceremonies within Fire Circle memory.

    This service:
    - Monitors for ceremony triggers
    - Conducts ceremonies at appropriate times
    - Preserves ceremony artifacts
    - Emits consciousness events for ceremony outcomes
    """

    def __init__(
        self,
        memory_store: MemoryStore,
        event_bus: ConsciousnessEventBus | None = None,
        schedule: CeremonySchedule | None = None,
        criteria: ConsolidationCriteria | None = None,
    ):
        self.memory_store = memory_store
        self.event_bus = event_bus
        self.schedule = schedule or CeremonySchedule()
        self.ceremony = WisdomConsolidationCeremony(criteria)
        self.ceremony_history: list[dict[str, Any]] = []

    async def check_ceremony_triggers(self) -> bool:
        """
        Check if conditions are right for a consolidation ceremony.

        Returns True if ceremony should be conducted.
        """
        # Get unconsolidated sacred moments
        sacred_moments = self._get_unconsolidated_sacred_moments()

        if not sacred_moments:
            return False

        # Check scheduled ceremony time
        time_since_last = datetime.now(UTC) - self.schedule.last_ceremony_time
        if time_since_last >= self.schedule.regular_interval:
            logger.info("Regular ceremony interval reached")
            return True

        # Check sacred moment accumulation
        if len(sacred_moments) >= self.schedule.sacred_threshold:
            logger.info(f"Sacred moment threshold reached: {len(sacred_moments)} moments")
            return True

        # Check emergence quality for immediate ceremony
        emergence_metrics = self.ceremony.detect_wisdom_emergence(sacred_moments)
        if emergence_metrics["emergence_quality"] >= self.schedule.emergence_trigger:
            logger.info(
                f"High emergence quality detected: {emergence_metrics['emergence_quality']:.3f}"
            )
            return True

        return False

    async def conduct_ceremony_if_ready(self) -> WisdomConsolidation | None:
        """
        Conduct a consolidation ceremony if conditions are met.

        Returns the consolidation if ceremony was conducted, None otherwise.
        """
        if not await self.check_ceremony_triggers():
            return None

        # Get sacred moments for ceremony
        sacred_moments = self._get_unconsolidated_sacred_moments()

        # Identify consolidation groups
        candidate_groups = self.ceremony.identify_consolidation_candidates(sacred_moments)

        if not candidate_groups:
            logger.info("No suitable groups found for consolidation")
            return None

        # Conduct ceremony for the most resonant group
        best_group = self._select_best_group(candidate_groups)

        try:
            # Conduct the ceremony
            consolidation = self.ceremony.conduct_ceremony(best_group)

            # Store the consolidation
            self.memory_store.wisdom_consolidations[consolidation.consolidation_id] = consolidation

            # Mark episodes as consolidated
            self._mark_episodes_consolidated(
                [ep.episode_id for ep in best_group], consolidation.consolidation_id
            )

            # Record ceremony in history
            self._record_ceremony(consolidation, best_group)

            # Update schedule
            self.schedule.last_ceremony_time = datetime.now(UTC)

            # Emit consciousness event if connected
            if self.event_bus:
                await self._emit_ceremony_event(consolidation, best_group)

            logger.info(f"Consolidation ceremony completed: {consolidation.consolidation_id}")

            return consolidation

        except Exception as e:
            logger.error(f"Ceremony failed: {e}")
            return None

    def _get_unconsolidated_sacred_moments(self) -> list[EpisodicMemory]:
        """Get sacred moments that haven't been consolidated."""
        unconsolidated = []

        for episode_id in self.memory_store.sacred_memories:
            episode = self.memory_store._load_memory(episode_id)
            if episode and not hasattr(episode, "_consolidated"):
                unconsolidated.append(episode)

        return unconsolidated

    def _select_best_group(
        self, candidate_groups: list[list[EpisodicMemory]]
    ) -> list[EpisodicMemory]:
        """Select the best group for consolidation based on emergence quality."""
        best_group = None
        best_quality = 0.0

        for group in candidate_groups:
            emergence_metrics = self.ceremony.detect_wisdom_emergence(group)
            if emergence_metrics["emergence_quality"] > best_quality:
                best_quality = emergence_metrics["emergence_quality"]
                best_group = group

        return best_group or candidate_groups[0]

    def _mark_episodes_consolidated(self, episode_ids: list[UUID], consolidation_id: UUID) -> None:
        """Mark episodes as part of a consolidation."""
        # This is a simple approach - in production would update database
        for episode_id in episode_ids:
            episode = self.memory_store._load_memory(episode_id)
            if episode:
                # Add consolidation marker (in real implementation, would persist)
                episode._consolidated = consolidation_id

    def _record_ceremony(
        self, consolidation: WisdomConsolidation, episodes: list[EpisodicMemory]
    ) -> None:
        """Record ceremony details in history."""
        ceremony_record = {
            "timestamp": datetime.now(UTC),
            "consolidation_id": consolidation.consolidation_id,
            "episode_count": len(episodes),
            "domains": list(set(ep.decision_domain for ep in episodes)),
            "emergence_quality": self.ceremony._assess_emergence_quality(episodes),
            "core_insight": consolidation.core_insight,
            "transformation_seeds": len(consolidation.practical_applications),
        }
        self.ceremony_history.append(ceremony_record)

    async def _emit_ceremony_event(
        self, consolidation: WisdomConsolidation, episodes: list[EpisodicMemory]
    ) -> None:
        """Emit consciousness event for ceremony completion."""
        event = ConsciousnessEvent(
            event_type=EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
            source_system="consolidation_ceremony",
            consciousness_signature=consolidation.civilizational_relevance,
            data={
                "consolidation_id": str(consolidation.consolidation_id),
                "episode_count": len(episodes),
                "core_insight": consolidation.core_insight,
                "domains": consolidation.applicable_domains,
                "transformation_potential": consolidation.civilizational_relevance,
                "ceremony_type": "wisdom_consolidation",
            },
            requires_fire_circle=False,  # Ceremony already complete
        )

        await self.event_bus.emit(event)

    async def get_ceremony_recommendations(self) -> dict[str, Any]:
        """
        Get recommendations for upcoming ceremonies.

        Provides guidance on:
        - When next ceremony should occur
        - Which episodes are ready for consolidation
        - What themes are emerging
        """
        sacred_moments = self._get_unconsolidated_sacred_moments()

        recommendations = {
            "next_scheduled_ceremony": self.schedule.last_ceremony_time
            + self.schedule.regular_interval,
            "unconsolidated_sacred_moments": len(sacred_moments),
            "ready_for_ceremony": False,
            "emerging_themes": [],
            "recommended_actions": [],
        }

        if not sacred_moments:
            recommendations["recommended_actions"].append("Continue accumulating sacred moments")
            return recommendations

        # Check emergence readiness
        emergence_metrics = self.ceremony.detect_wisdom_emergence(sacred_moments)
        recommendations["emergence_quality"] = emergence_metrics["emergence_quality"]
        recommendations["ready_for_ceremony"] = emergence_metrics["ready_for_ceremony"]

        # Identify emerging themes
        theme_keywords = defaultdict(int)
        for episode in sacred_moments:
            for keyword in extract_keywords(episode.collective_synthesis):
                theme_keywords[keyword] += 1

        # Top themes
        top_themes = sorted(theme_keywords.items(), key=lambda x: x[1], reverse=True)[:5]
        recommendations["emerging_themes"] = [theme for theme, _ in top_themes]

        # Recommendations based on state
        if emergence_metrics["ready_for_ceremony"]:
            recommendations["recommended_actions"].append(
                "Conduct consolidation ceremony - wisdom is ready to crystallize"
            )
        else:
            for missing in emergence_metrics["missing_elements"]:
                recommendations["recommended_actions"].append(f"Address: {missing}")

        return recommendations

    def get_ceremony_history(self, limit: int = 10) -> list[dict[str, Any]]:
        """Get recent ceremony history."""
        return self.ceremony_history[-limit:]

    async def integrate_with_episodic_service(self, episodic_service: Any) -> None:
        """
        Integrate orchestrator with episodic memory service.

        This allows automatic ceremony checks after Fire Circle sessions.
        """
        # Store reference to episodic service
        self.episodic_service = episodic_service

        # Hook into session completion
        original_process = episodic_service._process_session_rounds

        async def enhanced_process(result, session_context):
            # Original processing
            await original_process(result, session_context)

            # Check for ceremony triggers
            consolidation = await self.conduct_ceremony_if_ready()
            if consolidation:
                logger.info(f"Post-session ceremony conducted: {consolidation.consolidation_id}")

        episodic_service._process_session_rounds = enhanced_process


# Import helper for backwards compatibility
def extract_keywords(text: str) -> set[str]:
    """Extract keywords from text."""
    from .text_utils import extract_keywords as _extract_keywords

    return _extract_keywords(text)
