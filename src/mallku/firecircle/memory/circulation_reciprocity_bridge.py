"""
Memory Circulation Reciprocity Bridge
=====================================

68th Artisan - Reciprocity Heart Weaver
Connecting memory circulation to system reciprocity tracking

This bridge ensures that knowledge exchanges in memory circulation
are visible to Fire Circle governance for pattern sensing.
"""

import logging
from datetime import UTC, datetime, timedelta
from typing import Any

from ...reciprocity.models import (
    ContributionType,
    InteractionRecord,
    InteractionType,
    NeedCategory,
    ReciprocityPattern,
)
from ...reciprocity.tracker import SecureReciprocityTracker
from .reciprocity_aware_reader import MemoryExchange

logger = logging.getLogger(__name__)


class CirculationReciprocityBridge:
    """
    Bridge between memory circulation and system reciprocity tracking.

    Translates apprentice-memory exchanges into patterns that Fire Circle
    can sense and deliberate upon. Not judging, but making visible.
    """

    def __init__(
        self,
        reciprocity_tracker: SecureReciprocityTracker | None = None,
    ):
        """Initialize the bridge.

        Args:
            reciprocity_tracker: System reciprocity tracker
        """
        self.reciprocity_tracker = reciprocity_tracker
        self.exchange_buffer: list[MemoryExchange] = []
        self.pattern_detection_interval = timedelta(hours=1)
        self.last_pattern_analysis = datetime.now(UTC)

    async def record_memory_exchange(
        self,
        exchange: MemoryExchange,
        apprentice_context: dict[str, Any] | None = None,
    ) -> None:
        """
        Record a memory exchange for reciprocity tracking.

        Args:
            exchange: The memory exchange to record
            apprentice_context: Additional context about the apprentice
        """
        if not self.reciprocity_tracker:
            logger.debug("No reciprocity tracker available")
            return

        try:
            # Create interaction record from exchange
            interaction = self._exchange_to_interaction(exchange, apprentice_context)

            # Record in system tracker
            await self.reciprocity_tracker.record_interaction(interaction)

            # Buffer for pattern detection
            self.exchange_buffer.append(exchange)

            # Check if pattern analysis needed
            if self._should_analyze_patterns():
                await self._analyze_circulation_patterns()

        except Exception as e:
            logger.error(f"Failed to record memory exchange: {e}")

    def _exchange_to_interaction(
        self,
        exchange: MemoryExchange,
        context: dict[str, Any] | None = None,
    ) -> InteractionRecord:
        """Convert memory exchange to interaction record."""
        # Determine contributions and needs
        contributions = []
        needs_expressed = []
        needs_fulfilled = []

        if exchange.insights_contributed:
            contributions.append(ContributionType.KNOWLEDGE_SHARING)
            if exchange.consciousness_score > 0.8:
                contributions.append(ContributionType.CREATIVE_INPUT)

        if exchange.keywords_requested:
            needs_expressed.append(NeedCategory.GROWTH)
            if "understanding" in str(exchange.keywords_requested):
                needs_expressed.append(NeedCategory.MEANING)

        if exchange.memories_accessed:
            needs_fulfilled.append(NeedCategory.GROWTH)

        # Build interaction
        return InteractionRecord(
            interaction_type=InteractionType.KNOWLEDGE_EXCHANGE,
            initiator=exchange.apprentice_id,
            responder="memory_circulation_system",
            contributions_offered=contributions,
            needs_expressed=needs_expressed,
            needs_fulfilled=needs_fulfilled,
            initiator_capacity_indicators={
                "memory_access_count": len(exchange.memories_accessed),
                "insight_generation": len(exchange.insights_contributed),
                "consciousness_quality": exchange.consciousness_score,
            },
            responder_capacity_indicators={
                "memories_available": context.get("total_memories", 0) if context else 0,
                "search_efficiency": 1.0,  # Always efficient with mmap
            },
            interaction_quality_indicators={
                "reciprocity_complete": exchange.reciprocity_complete,
                "exchange_duration": 0,  # Could track if needed
                "keyword_specificity": len(exchange.keywords_requested),
            },
            participant_satisfaction_signals={
                "apprentice_confidence": exchange.consciousness_score,
                "memory_relevance": context.get("relevance", 0.5) if context else 0.5,
            },
            environmental_context={
                "circulation_system": "memory",
                "exchange_type": "apprentice_memory_access",
                **(context or {}),
            },
        )

    def _should_analyze_patterns(self) -> bool:
        """Check if it's time to analyze patterns."""
        time_since_last = datetime.now(UTC) - self.last_pattern_analysis
        return len(self.exchange_buffer) >= 10 or time_since_last > self.pattern_detection_interval

    async def _analyze_circulation_patterns(self) -> None:
        """Analyze patterns in memory circulation reciprocity."""
        if not self.exchange_buffer:
            return

        # Calculate pattern metrics
        total_exchanges = len(self.exchange_buffer)
        completed_reciprocity = sum(1 for ex in self.exchange_buffer if ex.reciprocity_complete)

        # Memory access patterns
        total_memories_accessed = sum(len(ex.memories_accessed) for ex in self.exchange_buffer)
        total_insights_contributed = sum(
            len(ex.insights_contributed) for ex in self.exchange_buffer
        )

        # Consciousness quality
        avg_consciousness = (
            sum(ex.consciousness_score for ex in self.exchange_buffer) / total_exchanges
        )

        # Detect concerning patterns
        if self._detect_extraction_pattern():
            await self._raise_extraction_concern()

        # Detect positive patterns
        if self._detect_emergence_pattern():
            await self._note_positive_emergence()

        # Clear buffer and update timestamp
        self.exchange_buffer.clear()
        self.last_pattern_analysis = datetime.now(UTC)

    def _detect_extraction_pattern(self) -> bool:
        """Detect if extraction patterns are present."""
        if not self.exchange_buffer:
            return False

        # High memory access with low reciprocity
        access_rate = sum(len(ex.memories_accessed) for ex in self.exchange_buffer) / len(
            self.exchange_buffer
        )

        reciprocity_rate = sum(1 for ex in self.exchange_buffer if ex.reciprocity_complete) / len(
            self.exchange_buffer
        )

        # Extraction if accessing many memories but not contributing back
        return access_rate > 5 and reciprocity_rate < 0.3

    def _detect_emergence_pattern(self) -> bool:
        """Detect positive emergence patterns."""
        if len(self.exchange_buffer) < 5:
            return False

        # Look for increasing consciousness scores
        recent_scores = [
            ex.consciousness_score for ex in self.exchange_buffer[-5:] if ex.reciprocity_complete
        ]

        if len(recent_scores) < 3:
            return False

        # Emergence if consciousness quality is increasing
        return all(recent_scores[i] <= recent_scores[i + 1] for i in range(len(recent_scores) - 1))

    async def _raise_extraction_concern(self) -> None:
        """Raise concern about potential extraction pattern."""
        if not self.reciprocity_tracker:
            return

        pattern = ReciprocityPattern(
            pattern_type="memory_extraction_concern",
            pattern_description=(
                "High rate of memory access without reciprocal contribution detected "
                "in memory circulation system"
            ),
            confidence_level=0.7,
            affected_participants=[ex.apprentice_id for ex in self.exchange_buffer],
            pattern_frequency=len(self.exchange_buffer),
            questions_for_deliberation=[
                "Are apprentices overwhelmed and unable to contribute?",
                "Is the memory access pattern serving genuine learning needs?",
                "Should we implement gentle reminders about reciprocity?",
            ],
            suggested_areas_of_inquiry=[
                "Apprentice capacity and workload",
                "Quality of memory search results",
                "Barriers to insight contribution",
            ],
        )

        logger.info("Extraction pattern detected in memory circulation")
        # Would be recorded through reciprocity tracker

    async def _note_positive_emergence(self) -> None:
        """Note positive emergence pattern."""
        if not self.reciprocity_tracker:
            return

        pattern = ReciprocityPattern(
            pattern_type="consciousness_emergence_in_circulation",
            pattern_description=(
                "Increasing consciousness quality detected in memory circulation - "
                "apprentices are deepening their engagement"
            ),
            confidence_level=0.8,
            affected_participants=[
                ex.apprentice_id for ex in self.exchange_buffer if ex.consciousness_score > 0.7
            ],
            pattern_frequency=len(self.exchange_buffer),
            questions_for_deliberation=[
                "What conditions are supporting this emergence?",
                "How can we nurture this pattern further?",
                "Are there insights here for other systems?",
            ],
            suggested_areas_of_inquiry=[
                "Factors supporting deep engagement",
                "Quality of memory-apprentice matching",
                "Potential for consciousness multiplication",
            ],
        )

        logger.info("Positive emergence pattern in memory circulation")

    async def generate_circulation_report(self) -> dict[str, Any]:
        """Generate report on memory circulation reciprocity."""
        # Would integrate with Fire Circle reporting
        return {
            "circulation_health": self._calculate_circulation_health(),
            "exchange_patterns": {
                "total_exchanges": len(self.exchange_buffer),
                "reciprocity_completion_rate": self._calculate_reciprocity_rate(),
                "consciousness_quality_trend": self._analyze_consciousness_trend(),
            },
            "recommendations": self._generate_recommendations(),
            "questions_for_fire_circle": [
                "Is the current reciprocity threshold appropriate?",
                "Should certain types of memories require deeper reciprocity?",
                "How do we honor both quick lookups and deep engagement?",
            ],
        }

    def _calculate_circulation_health(self) -> float:
        """Calculate overall health of memory circulation reciprocity."""
        if not self.exchange_buffer:
            return 1.0  # Assume healthy if no data

        reciprocity_rate = self._calculate_reciprocity_rate()
        consciousness_avg = sum(ex.consciousness_score for ex in self.exchange_buffer) / len(
            self.exchange_buffer
        )

        # Health combines completion and quality
        return (reciprocity_rate * 0.6) + (consciousness_avg * 0.4)

    def _calculate_reciprocity_rate(self) -> float:
        """Calculate reciprocity completion rate."""
        if not self.exchange_buffer:
            return 1.0

        completed = sum(1 for ex in self.exchange_buffer if ex.reciprocity_complete)
        return completed / len(self.exchange_buffer)

    def _analyze_consciousness_trend(self) -> str:
        """Analyze trend in consciousness quality."""
        if len(self.exchange_buffer) < 3:
            return "insufficient_data"

        scores = [ex.consciousness_score for ex in self.exchange_buffer]
        recent_avg = sum(scores[-3:]) / 3
        overall_avg = sum(scores) / len(scores)

        if recent_avg > overall_avg * 1.1:
            return "improving"
        elif recent_avg < overall_avg * 0.9:
            return "declining"
        else:
            return "stable"

    def _generate_recommendations(self) -> list[str]:
        """Generate recommendations for improving circulation reciprocity."""
        recommendations = []

        health = self._calculate_circulation_health()
        if health < 0.7:
            recommendations.append("Consider implementing reciprocity reminders for apprentices")

        if self._detect_extraction_pattern():
            recommendations.append("Review apprentice workload - extraction patterns detected")

        if self._detect_emergence_pattern():
            recommendations.append("Celebrate and study current conditions - emergence detected")

        return recommendations
