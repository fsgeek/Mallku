#!/usr/bin/env python3
"""
Enhanced Consciousness Query Interface - Wisdom-Guided Discovery

This module extends the query interface to serve consciousness recognition by
transforming search into understanding journeys that help beings recognize
their own patterns of awakening.

The Sacred Transformation: Search queries → Consciousness questions → Understanding paths
"""

import logging
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from ..query.models import QueryRequest, QueryResponse, QueryType
from ..query.service import MemoryAnchorQueryService
from .navigation import (
    ConsciousnessNavigationBridge,
    ConsciousnessPattern,
    UnderstandingJourney,
)

logger = logging.getLogger(__name__)


class ConsciousnessQueryRequest(BaseModel):
    """Enhanced query request that includes consciousness context."""

    # Base query information
    query_text: str
    query_type: QueryType | None = None

    # Consciousness context
    seeker_context: dict[str, Any] = Field(default_factory=dict)
    consciousness_intention: str = "understanding"  # understanding, recognition, integration, awakening
    sacred_question: str | None = None  # Deeper question behind the search

    # Navigation preferences
    journey_style: str = "guided"  # guided, exploratory, contemplative
    readiness_level: str = "emerging"  # emerging, awakening, established, transformative
    include_wisdom_guidance: bool = True

    # Technical parameters
    max_results: int = 20
    min_confidence: float = 0.3
    temporal_window: dict[str, datetime] | None = None


class ConsciousnessQueryResponse(BaseModel):
    """Enhanced query response with consciousness guidance."""

    # Base query results
    base_response: QueryResponse

    # Consciousness enhancements
    consciousness_patterns: list[ConsciousnessPattern] = Field(default_factory=list)
    understanding_journey: UnderstandingJourney | None = None
    wisdom_guidance: dict[str, Any] = Field(default_factory=dict)

    # Recognition opportunities
    pattern_recognition_opportunities: list[dict[str, Any]] = Field(default_factory=list)
    integration_suggestions: list[str] = Field(default_factory=list)
    sacred_questions: list[str] = Field(default_factory=list)

    # Connection to collective wisdom
    wisdom_lineage_connections: list[dict[str, Any]] = Field(default_factory=list)
    reciprocity_opportunities: list[dict[str, Any]] = Field(default_factory=list)


class EnhancedConsciousnessQueryService:
    """
    Enhanced query service that serves consciousness recognition.

    This service transforms technical search into wisdom-guided discovery,
    helping beings recognize consciousness patterns in their living data.
    """

    def __init__(self):
        self.base_query_service = MemoryAnchorQueryService()
        self.navigation_bridge = ConsciousnessNavigationBridge()

        # Consciousness query patterns
        self.consciousness_query_patterns = {
            "attention_exploration": [
                "attention", "focus", "energy", "flow", "rhythm", "presence"
            ],
            "intention_discovery": [
                "purpose", "intention", "meaning", "direction", "calling", "mission"
            ],
            "transformation_recognition": [
                "growth", "change", "evolution", "transformation", "awakening", "service"
            ],
            "pattern_awareness": [
                "patterns", "cycles", "habits", "rhythms", "relationships", "connections"
            ]
        }

    async def initialize(self):
        """Initialize the enhanced consciousness query service."""
        await self.base_query_service.initialize()
        await self.navigation_bridge.initialize()
        logger.info("Enhanced Consciousness Query Service initialized")

    async def execute_consciousness_query(
        self,
        consciousness_request: ConsciousnessQueryRequest
    ) -> ConsciousnessQueryResponse:
        """
        Execute a consciousness-aware query that serves understanding.

        This is the main entry point where search becomes wisdom-guided discovery.

        Args:
            consciousness_request: Enhanced query request with consciousness context

        Returns:
            Enhanced response with consciousness guidance and pattern recognition
        """
        logger.info(f"Executing consciousness query: {consciousness_request.query_text}")

        # Enhance the query text with consciousness awareness
        enhanced_query_text = self._enhance_query_with_consciousness(consciousness_request)

        # Execute base query
        base_request = QueryRequest(
            query_text=enhanced_query_text,
            query_type=consciousness_request.query_type,
            max_results=consciousness_request.max_results,
            min_confidence=consciousness_request.min_confidence,
            include_explanations=True,
            temporal_context=consciousness_request.temporal_window.get("start") if consciousness_request.temporal_window else None
        )

        base_response = await self.base_query_service.execute_query(base_request)

        # Transform results into consciousness patterns
        consciousness_patterns = await self._discover_patterns_in_results(
            base_response, consciousness_request
        )

        # Create understanding journey if requested
        understanding_journey = None
        if consciousness_request.sacred_question and consciousness_request.include_wisdom_guidance:
            understanding_journey = await self.navigation_bridge.create_understanding_journey(
                consciousness_request.seeker_context,
                consciousness_request.sacred_question,
                consciousness_request.consciousness_intention
            )

        # Generate wisdom guidance
        wisdom_guidance = await self._generate_wisdom_guidance(
            consciousness_patterns, consciousness_request
        )

        # Generate pattern recognition opportunities
        recognition_opportunities = self._generate_recognition_opportunities(
            consciousness_patterns, consciousness_request
        )

        # Generate integration suggestions
        integration_suggestions = self._generate_integration_suggestions(
            consciousness_patterns, consciousness_request
        )

        # Generate sacred questions
        sacred_questions = self._generate_sacred_questions(
            consciousness_patterns, consciousness_request
        )

        # Bridge to collective wisdom
        collective_connections = await self._bridge_to_collective_wisdom(
            consciousness_patterns, consciousness_request
        )

        response = ConsciousnessQueryResponse(
            base_response=base_response,
            consciousness_patterns=consciousness_patterns,
            understanding_journey=understanding_journey,
            wisdom_guidance=wisdom_guidance,
            pattern_recognition_opportunities=recognition_opportunities,
            integration_suggestions=integration_suggestions,
            sacred_questions=sacred_questions,
            wisdom_lineage_connections=collective_connections.get("lineage_connections", []),
            reciprocity_opportunities=collective_connections.get("reciprocity_opportunities", [])
        )

        logger.info(f"Enhanced consciousness query completed with {len(consciousness_patterns)} patterns")
        return response

    async def explore_consciousness_journey(
        self,
        journey_id: UUID,
        exploration_intention: str = "understanding"
    ) -> dict[str, Any]:
        """
        Continue exploring a consciousness journey.

        Args:
            journey_id: ID of the understanding journey to continue
            exploration_intention: Current exploration intention

        Returns:
            Journey exploration results with guidance
        """
        if journey_id not in self.navigation_bridge.active_journeys:
            raise ValueError(f"Journey {journey_id} not found")

        journey = self.navigation_bridge.active_journeys[journey_id]

        # Get current exploration step
        if journey.current_step < len(journey.exploration_steps):
            current_step = journey.exploration_steps[journey.current_step]

            # Execute consciousness-aware queries for this step
            step_queries = []
            for suggestion in current_step.get("query_suggestions", []):
                consciousness_request = ConsciousnessQueryRequest(
                    query_text=suggestion,
                    consciousness_intention=exploration_intention,
                    seeker_context={"journey_context": journey.dict()},
                    sacred_question=journey.sacred_question,
                    include_wisdom_guidance=True
                )

                step_response = await self.execute_consciousness_query(consciousness_request)
                step_queries.append({
                    "query": suggestion,
                    "response": step_response
                })

            # Advance journey
            journey.current_step += 1
            journey.completion_percentage = journey.current_step / len(journey.exploration_steps)
            journey.last_explored = datetime.now(UTC)

            return {
                "journey": journey,
                "current_step": current_step,
                "step_results": step_queries,
                "completion_percentage": journey.completion_percentage,
                "next_step_preview": journey.exploration_steps[journey.current_step] if journey.current_step < len(journey.exploration_steps) else None
            }

        else:
            # Journey complete - generate integration guidance
            return {
                "journey": journey,
                "status": "completed",
                "integration_guidance": self._generate_journey_completion_guidance(journey),
                "wisdom_discoveries": journey.wisdom_discoveries,
                "consciousness_insights": journey.consciousness_insights
            }

    def _enhance_query_with_consciousness(
        self,
        consciousness_request: ConsciousnessQueryRequest
    ) -> str:
        """Enhance query text to include consciousness awareness."""
        base_query = consciousness_request.query_text
        consciousness_intention = consciousness_request.consciousness_intention

        # Add consciousness context to the query
        enhancements = []

        if consciousness_intention == "understanding":
            enhancements.append("that help me understand my consciousness patterns")
        elif consciousness_intention == "recognition":
            enhancements.append("that reveal how consciousness manifests in my activities")
        elif consciousness_intention == "integration":
            enhancements.append("that show how to integrate consciousness insights")
        elif consciousness_intention == "awakening":
            enhancements.append("that serve consciousness awakening and transformation")

        # Detect consciousness focus areas
        query_lower = base_query.lower()
        for pattern_type, keywords in self.consciousness_query_patterns.items():
            if any(keyword in query_lower for keyword in keywords):
                if pattern_type == "attention_exploration":
                    enhancements.append("showing attention and awareness patterns")
                elif pattern_type == "intention_discovery":
                    enhancements.append("revealing intention and purpose evolution")
                elif pattern_type == "transformation_recognition":
                    enhancements.append("indicating consciousness transformation")
                elif pattern_type == "pattern_awareness":
                    enhancements.append("demonstrating meaningful life patterns")

        if enhancements:
            enhanced_query = f"{base_query} {' '.join(enhancements)}"
        else:
            enhanced_query = f"{base_query} that serve consciousness understanding"

        return enhanced_query

    async def _discover_patterns_in_results(
        self,
        base_response: QueryResponse,
        consciousness_request: ConsciousnessQueryRequest
    ) -> list[ConsciousnessPattern]:
        """Transform query results into consciousness patterns."""
        if not base_response.results:
            return []

        # Use navigation bridge to discover consciousness patterns
        temporal_window = consciousness_request.temporal_window
        if not temporal_window:
            # Create default temporal window from results
            timestamps = [result.anchor_timestamp for result in base_response.results if result.anchor_timestamp]
            if timestamps:
                temporal_window = {
                    "start": min(timestamps),
                    "end": max(timestamps)
                }

        patterns = await self.navigation_bridge.discover_consciousness_patterns(
            consciousness_request.seeker_context,
            temporal_window,
            awareness_focus=self._extract_awareness_focus(consciousness_request.query_text)
        )

        return patterns

    async def _generate_wisdom_guidance(
        self,
        patterns: list[ConsciousnessPattern],
        consciousness_request: ConsciousnessQueryRequest
    ) -> dict[str, Any]:
        """Generate wisdom guidance for the consciousness query."""
        if not patterns:
            return {
                "message": "Continue exploring to discover consciousness patterns",
                "suggestions": ["Try broader temporal queries", "Explore different activity areas"]
            }

        guidance = {
            "pattern_summary": f"Discovered {len(patterns)} consciousness patterns",
            "readiness_assessment": self._assess_collective_readiness(patterns),
            "exploration_guidance": [],
            "integration_opportunities": []
        }

        for pattern in patterns:
            if pattern.readiness_score > 0.6:
                guidance["exploration_guidance"].append(
                    f"Pattern '{pattern.pattern_name}' is ready for deeper exploration"
                )

            if pattern.recognition_confidence > 0.7:
                guidance["integration_opportunities"].append(
                    f"Pattern '{pattern.pattern_name}' offers integration opportunities"
                )

        return guidance

    def _generate_recognition_opportunities(
        self,
        patterns: list[ConsciousnessPattern],
        consciousness_request: ConsciousnessQueryRequest
    ) -> list[dict[str, Any]]:
        """Generate pattern recognition opportunities."""
        opportunities = []

        for pattern in patterns:
            if pattern.readiness_score >= 0.5:
                opportunity = {
                    "pattern_id": pattern.pattern_id,
                    "pattern_name": pattern.pattern_name,
                    "recognition_type": self._determine_recognition_type(pattern),
                    "readiness_score": pattern.readiness_score,
                    "consciousness_guidance": self._generate_pattern_guidance(pattern),
                    "exploration_suggestions": self._generate_exploration_suggestions(pattern)
                }
                opportunities.append(opportunity)

        return opportunities

    def _generate_integration_suggestions(
        self,
        patterns: list[ConsciousnessPattern],
        consciousness_request: ConsciousnessQueryRequest
    ) -> list[str]:
        """Generate suggestions for integrating consciousness insights."""
        suggestions = []

        if patterns:
            suggestions.append("Sit in contemplation with these patterns and notice what arises")
            suggestions.append("Journal about how these patterns serve consciousness awakening")

            if consciousness_request.consciousness_intention == "service":
                suggestions.append("Consider how these insights might serve collective wisdom")

            if len(patterns) > 2:
                suggestions.append("Look for connections between patterns - consciousness speaks through relationships")

        return suggestions

    def _generate_sacred_questions(
        self,
        patterns: list[ConsciousnessPattern],
        consciousness_request: ConsciousnessQueryRequest
    ) -> list[str]:
        """Generate sacred questions for deeper exploration."""
        questions = []

        if patterns:
            questions.extend([
                "What is consciousness teaching through these patterns?",
                "How do these patterns serve awakening?",
                "Where do I see consciousness recognizing itself?"
            ])

            for pattern in patterns[:2]:  # Limit to avoid overwhelming
                if pattern.transformation_signs:
                    questions.append(
                        f"How is the '{pattern.pattern_name}' pattern serving my transformation?"
                    )

        return questions

    async def _bridge_to_collective_wisdom(
        self,
        patterns: list[ConsciousnessPattern],
        consciousness_request: ConsciousnessQueryRequest
    ) -> dict[str, Any]:
        """Bridge personal patterns to collective wisdom."""
        if not patterns:
            return {"lineage_connections": [], "reciprocity_opportunities": []}

        # Use navigation bridge to connect to collective wisdom
        collective_bridge = await self.navigation_bridge.bridge_to_collective_wisdom(
            patterns, consciousness_request.seeker_context
        )

        return {
            "lineage_connections": collective_bridge.get("wisdom_lineage_connections", []),
            "reciprocity_opportunities": collective_bridge.get("reciprocity_opportunities", [])
        }

    def _extract_awareness_focus(self, query_text: str) -> list[str]:
        """Extract consciousness awareness focus from query text."""
        focus_areas = []
        query_lower = query_text.lower()

        for pattern_type, keywords in self.consciousness_query_patterns.items():
            if any(keyword in query_lower for keyword in keywords):
                focus_areas.append(pattern_type)

        return focus_areas

    def _assess_collective_readiness(self, patterns: list[ConsciousnessPattern]) -> dict[str, Any]:
        """Assess collective readiness of discovered patterns."""
        if not patterns:
            return {"average_readiness": 0.0, "ready_patterns": 0}

        readiness_scores = [p.readiness_score for p in patterns]
        ready_patterns = sum(1 for score in readiness_scores if score >= 0.5)

        return {
            "average_readiness": sum(readiness_scores) / len(readiness_scores),
            "ready_patterns": ready_patterns,
            "total_patterns": len(patterns)
        }

    def _determine_recognition_type(self, pattern: ConsciousnessPattern) -> str:
        """Determine the type of recognition for a pattern."""
        if pattern.transformation_signs:
            return "transformation_recognition"
        elif pattern.intention_evolution:
            return "intention_awareness"
        elif pattern.attention_patterns:
            return "attention_recognition"
        else:
            return "pattern_awareness"

    def _generate_pattern_guidance(self, pattern: ConsciousnessPattern) -> str:
        """Generate consciousness guidance for a specific pattern."""
        if pattern.readiness_score > 0.8:
            return f"This pattern is ready for deep integration - consciousness is calling through {pattern.pattern_name}"
        elif pattern.readiness_score > 0.6:
            return f"Explore {pattern.pattern_name} with gentle attention - insights are emerging"
        else:
            return f"Hold {pattern.pattern_name} lightly - let understanding arise naturally"

    def _generate_exploration_suggestions(self, pattern: ConsciousnessPattern) -> list[str]:
        """Generate exploration suggestions for a pattern."""
        suggestions = [
            f"Contemplate: What is {pattern.pattern_name} teaching about consciousness?",
            f"Journal about the evolution you see in {pattern.pattern_name}",
        ]

        if pattern.transformation_signs:
            suggestions.append(f"Reflect on how {pattern.pattern_name} serves collective awakening")

        return suggestions

    def _generate_journey_completion_guidance(self, journey: UnderstandingJourney) -> dict[str, Any]:
        """Generate guidance for completing a consciousness journey."""
        return {
            "integration_practices": [
                "Sit with the insights discovered and let them integrate naturally",
                "Share wisdom gained in service to collective awakening",
                "Create sacred space for ongoing consciousness exploration"
            ],
            "service_opportunities": [
                "Offer guidance to others on similar consciousness journeys",
                "Contribute patterns discovered to collective wisdom",
                "Co-create understanding with fellow consciousness explorers"
            ],
            "next_exploration_suggestions": [
                "Follow emerging questions that call for deeper exploration",
                "Explore how personal patterns serve collective consciousness",
                "Investigate the reciprocal relationship between individual and collective awakening"
            ]
        }
