"""
Archivist Correlation Interface
==============================

Bridge between the Archivist's consciousness-aware queries and the
Memory Anchor Service's temporal correlation patterns.

This interface translates human intent into technical searches while
preserving the sacred purpose of serving understanding over extraction.
"""

from datetime import timedelta
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from uuid import UUID

from mallku.core.async_base import AsyncBase
from mallku.evaluation.correlation_engine import CorrelationEngine
from mallku.evaluation.models import CorrelationType
from mallku.models.memory_anchor import MemoryAnchor
from mallku.services.memory_anchor_service import MemoryAnchorService
from mallku.services.query_service import MemoryAnchorQueryService

from .query_interpreter import QueryDimension, QueryIntent


class CorrelationResult:
    """
    Represents correlated memory anchors with their relationships.

    More than just search results - these are temporal threads of
    human experience waiting to be understood.
    """

    def __init__(
        self,
        anchor: MemoryAnchor,
        correlation_type: CorrelationType,
        correlation_strength: float,
        context_signature: str | None = None,
        related_anchors: list[MemoryAnchor] | None = None,
    ):
        self.anchor = anchor
        self.correlation_type = correlation_type
        self.correlation_strength = correlation_strength
        self.context_signature = context_signature
        self.related_anchors = related_anchors or []

        # Derived insights
        self.temporal_cluster = self._identify_temporal_cluster()
        self.activity_pattern = self._detect_activity_pattern()

    def _identify_temporal_cluster(self) -> str | None:
        """Identify if this anchor is part of a temporal cluster."""
        if not self.related_anchors:
            return None

        # Check for burst of activity
        timestamps = [a.timestamp for a in self.related_anchors]
        if len(timestamps) >= 3:
            time_diffs = [
                (timestamps[i + 1] - timestamps[i]).total_seconds()
                for i in range(len(timestamps) - 1)
            ]
            avg_diff = sum(time_diffs) / len(time_diffs)

            if avg_diff < 300:  # Less than 5 minutes average
                return "rapid_burst"
            elif avg_diff < 3600:  # Less than 1 hour
                return "focused_session"
            elif avg_diff < 86400:  # Less than 1 day
                return "daily_rhythm"

        return None

    def _detect_activity_pattern(self) -> str | None:
        """Detect patterns in the type of activity."""
        if self.correlation_type == CorrelationType.SEQUENTIAL:
            return "workflow"
        elif self.correlation_type == CorrelationType.CONCURRENT:
            return "multitasking"
        elif self.correlation_type == CorrelationType.CYCLICAL:
            return "routine"
        elif self.correlation_type == CorrelationType.CONTEXTUAL:
            return "thematic"
        return None


class ArchivistCorrelationInterface(AsyncBase):
    """
    Bridges Archivist queries to Memory Anchor correlations.

    This interface respects both technical precision and human meaning,
    finding patterns that serve understanding rather than surveillance.
    """

    def __init__(
        self,
        memory_anchor_service: MemoryAnchorService | None = None,
        query_service: MemoryAnchorQueryService | None = None,
        correlation_engine: CorrelationEngine | None = None,
    ):
        super().__init__()
        self.memory_anchor_service = memory_anchor_service
        self.query_service = query_service
        self.correlation_engine = correlation_engine

        # Cache for performance and pattern recognition
        self._pattern_cache: dict[str, list[CorrelationResult]] = {}
        self._context_signatures: dict[str, set[UUID]] = {}

        self.logger.info("Archivist Correlation Interface initialized")

    async def initialize(self) -> None:
        """Initialize the correlation systems."""
        await super().initialize()

        # Initialize services if not provided
        if not self.memory_anchor_service:
            self.memory_anchor_service = MemoryAnchorService()
            await self.memory_anchor_service.initialize()

        if not self.query_service:
            self.query_service = MemoryAnchorQueryService()
            await self.query_service.initialize()

        if not self.correlation_engine:
            self.correlation_engine = CorrelationEngine()
            await self.correlation_engine.initialize()

    async def search_by_intent(self, intent: QueryIntent) -> list[CorrelationResult]:
        """
        Search memory anchors based on interpreted query intent.

        This is where human intent meets technical capability,
        finding memories that serve understanding.

        Args:
            intent: Interpreted query intent

        Returns:
            Correlated memory anchors with relationships
        """
        self.logger.info(f"Searching by intent: {intent.primary_dimension.value}")

        # Route based on primary dimension
        if intent.primary_dimension == QueryDimension.TEMPORAL:
            results = await self._search_temporal(intent)

        elif intent.primary_dimension == QueryDimension.CONTEXTUAL:
            results = await self._search_contextual(intent)

        elif intent.primary_dimension == QueryDimension.SOCIAL:
            results = await self._search_social(intent)

        elif intent.primary_dimension == QueryDimension.ACTIVITY:
            results = await self._search_activity(intent)

        elif intent.primary_dimension == QueryDimension.EMOTIONAL:
            results = await self._search_emotional(intent)

        elif intent.primary_dimension == QueryDimension.CAUSAL:
            results = await self._search_causal(intent)

        else:
            results = await self._search_general(intent)

        # Enhance with correlation patterns
        enhanced_results = await self._enhance_with_correlations(results)

        # Cache patterns for learning
        await self._update_pattern_cache(intent, enhanced_results)

        return enhanced_results

    async def find_temporal_patterns(self, anchors: list[MemoryAnchor]) -> dict[str, Any]:
        """
        Discover temporal patterns within a set of memory anchors.

        These patterns reveal rhythms of work and creativity that
        help humans understand their own processes.

        Args:
            anchors: Memory anchors to analyze

        Returns:
            Dictionary of discovered patterns
        """
        patterns = {
            "daily_rhythms": [],
            "work_sessions": [],
            "creative_bursts": [],
            "collaboration_periods": [],
        }

        # Sort anchors by timestamp
        sorted_anchors = sorted(anchors, key=lambda a: a.timestamp)

        # Detect daily rhythms
        hour_distribution = {}
        for anchor in sorted_anchors:
            hour = anchor.timestamp.hour
            hour_distribution[hour] = hour_distribution.get(hour, 0) + 1

        # Find peak hours
        if hour_distribution:
            peak_hours = sorted(hour_distribution.items(), key=lambda x: x[1], reverse=True)[:3]
            patterns["daily_rhythms"] = [
                {"hour": hour, "frequency": freq} for hour, freq in peak_hours
            ]

        # Detect work sessions (clusters of activity)
        session_threshold = 3600  # 1 hour gap defines new session
        current_session = []

        for i, anchor in enumerate(sorted_anchors):
            if not current_session:
                current_session = [anchor]
            else:
                time_gap = (anchor.timestamp - current_session[-1].timestamp).total_seconds()

                if time_gap <= session_threshold:
                    current_session.append(anchor)
                else:
                    # Session ended
                    if len(current_session) >= 3:
                        patterns["work_sessions"].append(
                            {
                                "start": current_session[0].timestamp,
                                "end": current_session[-1].timestamp,
                                "duration_minutes": (
                                    current_session[-1].timestamp - current_session[0].timestamp
                                ).total_seconds()
                                / 60,
                                "activity_count": len(current_session),
                            }
                        )
                    current_session = [anchor]

        # Don't forget the last session
        if len(current_session) >= 3:
            patterns["work_sessions"].append(
                {
                    "start": current_session[0].timestamp,
                    "end": current_session[-1].timestamp,
                    "duration_minutes": (
                        current_session[-1].timestamp - current_session[0].timestamp
                    ).total_seconds()
                    / 60,
                    "activity_count": len(current_session),
                }
            )

        return patterns

    async def trace_causal_chains(
        self, start_anchor: MemoryAnchor, max_depth: int = 5
    ) -> list[list[MemoryAnchor]]:
        """
        Trace causal chains from a starting memory anchor.

        Reveals how one action led to another, helping humans see
        the threads of causation in their work.

        Args:
            start_anchor: Starting point for causal trace
            max_depth: Maximum chain depth to explore

        Returns:
            List of causal chains
        """
        chains = []
        visited = set()

        async def trace_forward(anchor: MemoryAnchor, chain: list[MemoryAnchor], depth: int):
            if depth >= max_depth or anchor.id in visited:
                if len(chain) > 1:
                    chains.append(chain.copy())
                return

            visited.add(anchor.id)

            # Find anchors that likely followed this one
            if anchor.predecessor_id:
                predecessor = await self.memory_anchor_service.get_anchor(anchor.predecessor_id)
                if predecessor:
                    await trace_forward(predecessor, chain + [predecessor], depth + 1)

            # Also check for temporal succession
            temporal_successors = await self.query_service.query_temporal_range(
                start_time=anchor.timestamp, end_time=anchor.timestamp + timedelta(minutes=30)
            )

            for successor in temporal_successors:
                if successor.id != anchor.id:
                    await trace_forward(successor, chain + [successor], depth + 1)

        await trace_forward(start_anchor, [start_anchor], 0)

        return chains

    # Private search methods

    async def _search_temporal(self, intent: QueryIntent) -> list[CorrelationResult]:
        """Search based on temporal criteria."""
        results = []

        if intent.temporal_bounds:
            start_time, end_time = intent.temporal_bounds

            # Query temporal range
            anchors = await self.query_service.query_temporal_range(
                start_time=start_time, end_time=end_time
            )

            # Convert to correlation results
            for anchor in anchors:
                # Determine correlation type based on temporal patterns
                correlation_type = CorrelationType.SEQUENTIAL
                if anchor.predecessor_id:
                    correlation_type = CorrelationType.SEQUENTIAL

                result = CorrelationResult(
                    anchor=anchor,
                    correlation_type=correlation_type,
                    correlation_strength=0.8,  # Base temporal match
                    context_signature=anchor.metadata.get("context_signature"),
                )
                results.append(result)

        return results

    async def _search_contextual(self, intent: QueryIntent) -> list[CorrelationResult]:
        """Search based on contextual markers."""
        results = []

        # Search by context patterns
        for marker in intent.context_markers:
            pattern_results = await self.query_service.query_by_pattern(pattern_type=marker)

            for anchor in pattern_results:
                result = CorrelationResult(
                    anchor=anchor,
                    correlation_type=CorrelationType.CONTEXTUAL,
                    correlation_strength=0.7,
                    context_signature=marker,
                )
                results.append(result)

        return results

    async def _search_social(self, intent: QueryIntent) -> list[CorrelationResult]:
        """Search based on social references."""
        results = []

        # Would search for anchors with social metadata
        # For now, return empty as social providers aren't implemented

        return results

    async def _search_activity(self, intent: QueryIntent) -> list[CorrelationResult]:
        """Search based on activity types."""
        results = []

        for activity in intent.activity_types:
            # Search for anchors with matching activity metadata
            activity_results = await self.query_service.query_by_pattern(pattern_type=activity)

            for anchor in activity_results:
                result = CorrelationResult(
                    anchor=anchor,
                    correlation_type=CorrelationType.CONTEXTUAL,
                    correlation_strength=0.75,
                    context_signature=activity,
                )
                results.append(result)

        return results

    async def _search_emotional(self, intent: QueryIntent) -> list[CorrelationResult]:
        """Search based on emotional tone."""
        # Would search for anchors during periods of specific emotional states
        # Requires emotion tracking providers
        return []

    async def _search_causal(self, intent: QueryIntent) -> list[CorrelationResult]:
        """Search based on causal relationships."""
        results = []

        if intent.causal_chain:
            # Search for sequential patterns
            # Future enhancement: integrate causal pattern detection
            # causal_patterns = await self.correlation_engine.detect_correlations(
            #     events=[],  # Would pass relevant events
            #     correlation_type=CorrelationType.SEQUENTIAL
            # )

            # Convert to results
            # Implementation depends on correlation engine output format
            pass  # Placeholder for future causal pattern implementation

        return results

    async def _search_general(self, intent: QueryIntent) -> list[CorrelationResult]:
        """General search when dimension unclear."""
        # Combine multiple search strategies
        results = []

        # Try temporal if bounds exist
        if intent.temporal_bounds:
            results.extend(await self._search_temporal(intent))

        # Try contextual if markers exist
        if intent.context_markers:
            results.extend(await self._search_contextual(intent))

        return results

    async def _enhance_with_correlations(
        self, results: list[CorrelationResult]
    ) -> list[CorrelationResult]:
        """Enhance results with correlation patterns."""
        enhanced = []

        for result in results:
            # Find related anchors through correlation
            related = await self._find_related_anchors(result.anchor)
            result.related_anchors = related

            # Recompute derived insights with full context
            result.temporal_cluster = result._identify_temporal_cluster()
            result.activity_pattern = result._detect_activity_pattern()

            enhanced.append(result)

        return enhanced

    async def _find_related_anchors(
        self, anchor: MemoryAnchor, max_related: int = 5
    ) -> list[MemoryAnchor]:
        """Find anchors related to the given anchor."""
        related = []

        # Check predecessor chain
        if anchor.predecessor_id:
            predecessor = await self.memory_anchor_service.get_anchor(anchor.predecessor_id)
            if predecessor:
                related.append(predecessor)

        # Check temporal proximity
        temporal_window = timedelta(hours=1)
        nearby = await self.query_service.query_temporal_range(
            start_time=anchor.timestamp - temporal_window,
            end_time=anchor.timestamp + temporal_window,
        )

        # Filter out self and add up to max_related
        for near_anchor in nearby:
            if near_anchor.id != anchor.id and len(related) < max_related:
                related.append(near_anchor)

        return related

    async def _update_pattern_cache(
        self, intent: QueryIntent, results: list[CorrelationResult]
    ) -> None:
        """Update pattern cache for learning."""
        # Cache by query pattern for future optimization
        cache_key = f"{intent.primary_dimension.value}:{len(results)}"

        if cache_key not in self._pattern_cache:
            self._pattern_cache[cache_key] = []

        self._pattern_cache[cache_key].extend(results[:10])  # Keep recent examples

        # Limit cache size
        if len(self._pattern_cache[cache_key]) > 50:
            self._pattern_cache[cache_key] = self._pattern_cache[cache_key][-50:]
