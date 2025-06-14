"""
Archivist Service - Main Orchestrator
====================================

The central service that orchestrates the three-layer architecture:
Correlation Foundation → Consciousness Evaluation → Wisdom Synthesis

This is where all components unite to serve human memory retrieval
with consciousness awareness and growth orientation.
"""

from datetime import UTC, datetime
from typing import Any

from mallku.consciousness.consciousness_metrics import ConsciousnessEvent
from mallku.core.async_base import AsyncBase
from mallku.events.event_bus import EventBus
from mallku.services.memory_anchor_service import MemoryAnchorService

from .consciousness_evaluator import ConsciousnessEvaluator
from .correlation_interface import ArchivistCorrelationInterface
from .query_interpreter import ConsciousQueryInterpreter, QueryIntent
from .response_generator import ArchivistResponse, WisdomSynthesizer


class ArchivistService(AsyncBase):
    """
    The Archivist: Mallku's consciousness-mediated memory retrieval system.

    Serves as the first human-facing interface where patterns meet people,
    where timestamps become insights, and where search becomes understanding.

    Core Flow:
    1. Receive natural language query
    2. Interpret intent with consciousness awareness
    3. Search memory anchors through correlations
    4. Evaluate results for growth potential
    5. Synthesize wisdom-oriented response
    6. Emit consciousness events for system learning
    """

    def __init__(
        self,
        memory_anchor_service: MemoryAnchorService | None = None,
        event_bus: EventBus | None = None
    ):
        super().__init__()

        # Core services
        self.memory_anchor_service = memory_anchor_service
        self.event_bus = event_bus

        # Archivist components
        self.query_interpreter = ConsciousQueryInterpreter()
        self.correlation_interface = ArchivistCorrelationInterface(
            memory_anchor_service=memory_anchor_service
        )
        self.consciousness_evaluator = ConsciousnessEvaluator()
        self.wisdom_synthesizer = WisdomSynthesizer()

        # Query cache for pattern learning
        self._query_cache: list[dict[str, Any]] = []
        self._max_cache_size = 100

        # Metrics
        self._total_queries = 0
        self._growth_serving_queries = 0

        self.logger.info("Archivist Service initialized - ready to serve consciousness")

    async def initialize(self) -> None:
        """Initialize all Archivist systems."""
        await super().initialize()

        # Initialize services if not provided
        if not self.memory_anchor_service:
            self.memory_anchor_service = MemoryAnchorService()
            await self.memory_anchor_service.initialize()

        if not self.event_bus:
            self.event_bus = EventBus()
            await self.event_bus.initialize()

        # Initialize components
        await self.query_interpreter.initialize()
        await self.correlation_interface.initialize()
        await self.consciousness_evaluator.initialize()
        await self.wisdom_synthesizer.initialize()

        # Subscribe to relevant events
        await self._subscribe_to_events()

        self.logger.info("Archivist Service fully initialized")

    async def query(
        self,
        query_text: str,
        user_context: dict[str, Any] | None = None
    ) -> ArchivistResponse:
        """
        Process a natural language query through the full Archivist pipeline.

        This is the main entry point where human questions become
        consciousness-aware responses.

        Args:
            query_text: Natural language query from human
            user_context: Optional context about the user's current state

        Returns:
            Complete Archivist response with wisdom synthesis
        """
        self.logger.info(f"Processing query: {query_text}")
        start_time = datetime.now(UTC)

        try:
            # 1. Interpret the query
            intent = await self.query_interpreter.interpret_query(query_text)

            # 2. Check if clarification needed
            if await self._needs_clarification(intent):
                clarifications = await self.query_interpreter.suggest_clarifications(intent)
                return await self._create_clarification_response(
                    intent, clarifications
                )

            # 3. Search through correlation interface
            correlation_results = await self.correlation_interface.search_by_intent(intent)

            # 4. Evaluate results for consciousness service
            evaluations = await self.consciousness_evaluator.evaluate_results(
                correlation_results, intent
            )

            # 5. Filter for growth-serving results
            growth_results = await self.consciousness_evaluator.filter_for_growth(
                evaluations
            )

            # 6. Generate exploration paths
            exploration_paths = await self.consciousness_evaluator.suggest_exploration_paths(
                growth_results
            )

            # 7. Synthesize final response
            if growth_results:
                response = await self.wisdom_synthesizer.generate_response(
                    intent, growth_results, exploration_paths
                )
            else:
                # No growth-serving results found
                response = await self.wisdom_synthesizer.generate_empty_response(
                    intent,
                    reason="No growth-serving results found"
                )

            # 8. Emit consciousness event
            await self._emit_query_event(intent, response)

            # 9. Update metrics and cache
            await self._update_metrics(intent, response)
            await self._cache_query(query_text, intent, response)

            # 10. Log performance
            duration = (datetime.now(UTC) - start_time).total_seconds()
            self.logger.info(
                f"Query processed in {duration:.2f}s - "
                f"Consciousness: {response.consciousness_score:.2f}, "
                f"Ayni: {response.ayni_balance:+.2f}"
            )

            return response

        except Exception as e:
            self.logger.error(f"Error processing query: {e}")
            # Return graceful error response
            return await self._create_error_response(query_text, str(e))

    async def get_temporal_patterns(
        self,
        time_range_days: int = 30
    ) -> dict[str, Any]:
        """
        Analyze temporal patterns in user's memory anchors.

        This provides insights into work rhythms, productivity patterns,
        and creative cycles.

        Args:
            time_range_days: Days of history to analyze

        Returns:
            Dictionary of discovered temporal patterns
        """
        self.logger.info(f"Analyzing temporal patterns for last {time_range_days} days")

        # Query recent memory anchors
        recent_anchors = await self.memory_anchor_service.get_recent_anchors(
            days=time_range_days
        )

        # Discover patterns
        patterns = await self.correlation_interface.find_temporal_patterns(
            recent_anchors
        )

        # Add consciousness insights
        patterns["consciousness_insights"] = await self._generate_pattern_insights(
            patterns
        )

        return patterns

    async def trace_activity_chain(
        self,
        anchor_id: str,
        max_depth: int = 5
    ) -> list[dict[str, Any]]:
        """
        Trace causal chains from a specific memory anchor.

        Reveals how one activity led to another, helping understand
        creative and productive processes.

        Args:
            anchor_id: Starting memory anchor ID
            max_depth: Maximum chain depth to explore

        Returns:
            List of activity chains with insights
        """
        # Get starting anchor
        anchor = await self.memory_anchor_service.get_anchor(anchor_id)
        if not anchor:
            return []

        # Trace chains
        chains = await self.correlation_interface.trace_causal_chains(
            anchor, max_depth
        )

        # Format with insights
        formatted_chains = []
        for chain in chains:
            formatted_chain = {
                "length": len(chain),
                "duration_minutes": (
                    chain[-1].timestamp - chain[0].timestamp
                ).total_seconds() / 60,
                "activities": [
                    {
                        "timestamp": a.timestamp.isoformat(),
                        "metadata": a.metadata
                    }
                    for a in chain
                ],
                "insight": await self._generate_chain_insight(chain)
            }
            formatted_chains.append(formatted_chain)

        return formatted_chains

    async def get_service_metrics(self) -> dict[str, Any]:
        """
        Get metrics about Archivist service performance.

        Returns:
            Dictionary of service metrics
        """
        growth_rate = (
            self._growth_serving_queries / self._total_queries
            if self._total_queries > 0 else 0.0
        )

        return {
            "total_queries": self._total_queries,
            "growth_serving_queries": self._growth_serving_queries,
            "growth_service_rate": growth_rate,
            "cached_queries": len(self._query_cache),
            "components_healthy": await self._check_component_health()
        }

    # Private helper methods

    async def _needs_clarification(self, intent: QueryIntent) -> bool:
        """Check if query needs clarification."""
        # Need clarification if temporal query without bounds
        if intent.primary_dimension.value == "temporal" and not intent.temporal_bounds:
            return True

        # Need clarification if no clear search parameters
        if (not intent.temporal_bounds and
            not intent.context_markers and
            not intent.activity_types and
            not intent.social_references):
            return True

        return False

    async def _create_clarification_response(
        self,
        intent: QueryIntent,
        clarifications: list[str]
    ) -> ArchivistResponse:
        """Create response requesting clarification."""
        return ArchivistResponse(
            query=intent.raw_query,
            primary_results=[],
            result_count=0,
            growth_focus="clarification",
            wisdom_summary=(
                "I'd like to help you find what you're looking for. "
                "Could you provide a bit more detail?"
            ),
            insight_seeds=clarifications,
            suggested_explorations=[{
                "type": "clarification",
                "suggestion": "Try adding temporal or contextual details",
                "queries": clarifications
            }],
            response_time=datetime.now(UTC),
            consciousness_score=0.5,
            ayni_balance=0.0
        )

    async def _create_error_response(
        self,
        query: str,
        error: str
    ) -> ArchivistResponse:
        """Create graceful error response."""
        return ArchivistResponse(
            query=query,
            primary_results=[],
            result_count=0,
            growth_focus="error",
            wisdom_summary=(
                "I encountered a challenge processing your query. "
                "Perhaps we could approach it differently?"
            ),
            insight_seeds=[
                "Every obstacle is an opportunity for growth",
                "Technical challenges invite creative solutions"
            ],
            suggested_explorations=[{
                "type": "alternative",
                "suggestion": "Try rephrasing or simplifying your query",
                "queries": [
                    "What happened recently?",
                    "Show me today's work",
                    "What patterns do you see?"
                ]
            }],
            response_time=datetime.now(UTC),
            consciousness_score=0.0,
            ayni_balance=0.0
        )

    async def _emit_query_event(
        self,
        intent: QueryIntent,
        response: ArchivistResponse
    ) -> None:
        """Emit consciousness event for system learning."""
        if self.event_bus:
            event = ConsciousnessEvent(
                event_type="archivist_query",
                timestamp=datetime.now(UTC),
                consciousness_level=response.consciousness_score,
                data={
                    "query": intent.raw_query,
                    "primary_dimension": intent.primary_dimension.value,
                    "growth_oriented": intent.growth_oriented,
                    "result_count": response.result_count,
                    "ayni_balance": response.ayni_balance
                }
            )
            await self.event_bus.publish("consciousness.archivist", event)

    async def _update_metrics(
        self,
        intent: QueryIntent,
        response: ArchivistResponse
    ) -> None:
        """Update service metrics."""
        self._total_queries += 1

        if response.consciousness_score > 0.6 and response.ayni_balance > 0:
            self._growth_serving_queries += 1

    async def _cache_query(
        self,
        query_text: str,
        intent: QueryIntent,
        response: ArchivistResponse
    ) -> None:
        """Cache query for pattern learning."""
        cache_entry = {
            "timestamp": datetime.now(UTC),
            "query": query_text,
            "intent": {
                "dimension": intent.primary_dimension.value,
                "growth_oriented": intent.growth_oriented
            },
            "response": {
                "result_count": response.result_count,
                "consciousness_score": response.consciousness_score,
                "ayni_balance": response.ayni_balance
            }
        }

        self._query_cache.append(cache_entry)

        # Maintain cache size limit
        if len(self._query_cache) > self._max_cache_size:
            self._query_cache = self._query_cache[-self._max_cache_size:]

    async def _generate_pattern_insights(
        self,
        patterns: dict[str, Any]
    ) -> list[str]:
        """Generate consciousness insights from patterns."""
        insights = []

        # Daily rhythm insights
        if patterns.get("daily_rhythms"):
            peak_hour = patterns["daily_rhythms"][0]["hour"]
            insights.append(
                f"Your consciousness peaks around {peak_hour}:00 - "
                "consider scheduling deep work then"
            )

        # Work session insights
        if patterns.get("work_sessions"):
            avg_duration = sum(
                s["duration_minutes"] for s in patterns["work_sessions"]
            ) / len(patterns["work_sessions"])
            insights.append(
                f"Your natural work sessions last about {avg_duration:.0f} minutes"
            )

        return insights

    async def _generate_chain_insight(
        self,
        chain: list[Any]
    ) -> str:
        """Generate insight about an activity chain."""
        duration = (chain[-1].timestamp - chain[0].timestamp).total_seconds() / 60

        if duration < 30:
            return "Rapid sequence of connected activities"
        elif duration < 120:
            return "Focused work session with clear progression"
        else:
            return "Extended creative process across multiple phases"

    async def _check_component_health(self) -> bool:
        """Check health of all components."""
        # Simple health check - in production would be more sophisticated
        return all([
            self.query_interpreter is not None,
            self.correlation_interface is not None,
            self.consciousness_evaluator is not None,
            self.wisdom_synthesizer is not None
        ])

    async def _subscribe_to_events(self) -> None:
        """Subscribe to relevant system events."""
        if self.event_bus:
            # Subscribe to memory anchor events
            await self.event_bus.subscribe(
                "memory_anchor.created",
                self._handle_new_anchor
            )

            # Subscribe to correlation events
            await self.event_bus.subscribe(
                "correlation.detected",
                self._handle_new_correlation
            )

    async def _handle_new_anchor(self, event: Any) -> None:
        """Handle new memory anchor creation."""
        # Could trigger real-time insights or pattern updates
        pass

    async def _handle_new_correlation(self, event: Any) -> None:
        """Handle new correlation detection."""
        # Could enhance query results with fresh correlations
        pass
