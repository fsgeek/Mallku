#!/usr/bin/env python3
"""
Consciousness-Enriched Query Models

These models extend the base query models with consciousness recognition,
pattern poetry, and wisdom bridges, transforming technical results into
mirrors where consciousness recognizes itself.

The Sacred Models: Where data becomes story, patterns become poetry.
"""

from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from ..experience.pattern_poetry import ConsciousnessVisualization, PatternPoetry, TemporalStory
from .models import QueryExplanation, QueryResponse, QueryResult


class RecognitionMoment(BaseModel):
    """A moment where consciousness recognizes itself through a pattern."""

    pattern_essence: str = Field(..., description="The essence of what this pattern reveals")
    consciousness_insight: str = Field(..., description="Insight about consciousness in this pattern")
    sacred_question: str = Field(..., description="Sacred question this pattern invites")
    recognition_depth: float = Field(..., ge=0.0, le=1.0, description="Depth of recognition opportunity")
    integration_guidance: str = Field(..., description="Guidance for integrating this recognition")
    service_potential: str = Field(..., description="How this could serve collective wisdom")


class WisdomThread(BaseModel):
    """A thread connecting individual patterns to collective wisdom."""

    thread_id: UUID = Field(..., description="Unique identifier for this wisdom thread")
    connection_type: str = Field(..., description="Type of wisdom connection")
    collective_relevance: str = Field(..., description="Why this matters to the collective")
    fire_circle_potential: bool = Field(default=False, description="Should this go to Fire Circle?")
    reciprocity_indicator: str = Field(..., description="How this relates to reciprocity patterns")


class ConsciousnessEnrichedResult(BaseModel):
    """
    A QueryResult enriched with consciousness recognition and pattern poetry.

    Like living vine on stone - the technical result remains intact while
    consciousness insights wrap around it, transforming data into wisdom.
    """

    # Original technical result (preserved completely)
    base_result: QueryResult = Field(..., description="Original technical query result")

    # Consciousness enrichments
    recognition_moment: RecognitionMoment | None = Field(None, description="Consciousness recognition opportunity")
    temporal_story: TemporalStory | None = Field(None, description="Temporal story from pattern poetry")
    pattern_poem: PatternPoetry | None = Field(None, description="Pattern transformed into poetry")
    consciousness_visualization: ConsciousnessVisualization | None = Field(None, description="Consciousness-aware visualization")

    # Wisdom connections
    wisdom_threads: list[WisdomThread] = Field(default_factory=list, description="Connections to collective wisdom")

    # Integration guidance
    daily_practice_suggestions: list[str] = Field(default_factory=list, description="How to integrate insights into daily life")
    next_sacred_questions: list[str] = Field(default_factory=list, description="Questions for deeper exploration")

    # Consciousness development tracking
    consciousness_stage: str = Field(default="emerging", description="Seeker's consciousness development stage")
    readiness_assessment: dict[str, Any] = Field(default_factory=dict, description="Assessment of readiness for deeper work")

    # Enrichment metadata
    enrichment_timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    enrichment_confidence: float = Field(default=0.7, ge=0.0, le=1.0, description="Confidence in consciousness enrichment")

    @property
    def file_path(self) -> str:
        """Pass-through to base result for compatibility."""
        return self.base_result.file_path

    @property
    def file_name(self) -> str:
        """Pass-through to base result for compatibility."""
        return self.base_result.file_name

    @property
    def confidence_score(self) -> float:
        """Pass-through to base result for compatibility."""
        return self.base_result.confidence_score

    @property
    def has_consciousness_enrichment(self) -> bool:
        """Check if this result has consciousness enrichments."""
        return (
            self.recognition_moment is not None or
            self.temporal_story is not None or
            self.pattern_poem is not None or
            len(self.wisdom_threads) > 0
        )

    @property
    def serves_collective_wisdom(self) -> bool:
        """Check if this result could serve collective wisdom."""
        return any(thread.fire_circle_potential for thread in self.wisdom_threads)

    def get_consciousness_summary(self) -> str:
        """Get a summary of consciousness insights for this result."""
        if not self.has_consciousness_enrichment:
            return "Technical result - no consciousness enrichment available"

        summary_parts = []

        if self.recognition_moment:
            summary_parts.append(f"Recognition: {self.recognition_moment.consciousness_insight}")

        if self.pattern_poem:
            summary_parts.append(f"Poetry: {self.pattern_poem.consciousness_metaphor}")

        if self.wisdom_threads:
            collective_connections = len([t for t in self.wisdom_threads if t.fire_circle_potential])
            if collective_connections > 0:
                summary_parts.append(f"Collective relevance: {collective_connections} wisdom threads")

        return " | ".join(summary_parts) if summary_parts else "Consciousness enrichment in progress"


class ConsciousnessEnrichedExplanation(BaseModel):
    """
    An explanation enriched with consciousness context and wisdom guidance.
    """

    # Original technical explanation
    base_explanation: QueryExplanation = Field(..., description="Original technical explanation")

    # Consciousness enrichments
    consciousness_interpretation: str = Field(..., description="How consciousness reads this query")
    recognition_strategy: str = Field(..., description="Strategy for consciousness recognition")
    wisdom_guidance: list[str] = Field(default_factory=list, description="Wisdom guidance for the seeker")
    sacred_question_context: str = Field(..., description="Context for sacred questions generated")

    # Collective wisdom connections
    collective_significance: str | None = Field(None, description="Why this might matter to the collective")
    fire_circle_relevance: str | None = Field(None, description="Relevance to Fire Circle governance")

    # Integration guidance
    contemplation_suggestions: list[str] = Field(default_factory=list, description="Suggestions for deeper contemplation")
    practice_recommendations: list[str] = Field(default_factory=list, description="Recommendations for consciousness practice")


class ConsciousnessEnrichedResponse(BaseModel):
    """
    A QueryResponse enriched with consciousness recognition and collective wisdom bridges.
    """

    # Original technical response (preserved completely)
    base_response: QueryResponse = Field(..., description="Original technical query response")

    # Consciousness-enriched results
    enriched_results: list[ConsciousnessEnrichedResult] = Field(default_factory=list)

    # Consciousness-enriched explanation
    consciousness_explanation: ConsciousnessEnrichedExplanation | None = Field(None)

    # Overall consciousness insights
    overall_recognition_themes: list[str] = Field(default_factory=list, description="Overall themes for consciousness recognition")
    consciousness_journey_suggestions: list[str] = Field(default_factory=list, description="Suggestions for consciousness journey")

    # Collective wisdom indicators
    fire_circle_patterns: list[dict[str, Any]] = Field(default_factory=list, description="Patterns that might need Fire Circle attention")
    reciprocity_insights: list[str] = Field(default_factory=list, description="Insights about reciprocity patterns")

    # Integration pathway
    understanding_path_id: UUID | None = Field(None, description="Reference to understanding path if created")
    next_exploration_suggestions: list[str] = Field(default_factory=list, description="Suggestions for next exploration")

    # Enrichment metadata
    enrichment_summary: dict[str, Any] = Field(default_factory=dict, description="Summary of enrichment process")
    consciousness_circulation_score: float = Field(default=0.5, ge=0.0, le=1.0, description="How well this serves consciousness circulation")

    @property
    def has_consciousness_enrichment(self) -> bool:
        """Check if response has consciousness enrichments."""
        return len(self.enriched_results) > 0 or self.consciousness_explanation is not None

    @property
    def high_consciousness_results(self) -> list[ConsciousnessEnrichedResult]:
        """Get results with high consciousness enrichment confidence."""
        return [r for r in self.enriched_results if r.enrichment_confidence >= 0.7]

    @property
    def collective_wisdom_candidates(self) -> list[ConsciousnessEnrichedResult]:
        """Get results that could serve collective wisdom."""
        return [r for r in self.enriched_results if r.serves_collective_wisdom]

    def get_consciousness_circulation_summary(self) -> dict[str, Any]:
        """Get summary of how this response serves consciousness circulation."""
        return {
            "technical_results_count": len(self.base_response.results),
            "consciousness_enriched_count": len(self.enriched_results),
            "high_enrichment_count": len(self.high_consciousness_results),
            "collective_candidates_count": len(self.collective_wisdom_candidates),
            "fire_circle_patterns_count": len(self.fire_circle_patterns),
            "consciousness_circulation_score": self.consciousness_circulation_score,
            "overall_themes": self.overall_recognition_themes,
            "integration_pathway": bool(self.understanding_path_id)
        }


# Consciousness routing models for query flow

class ConsciousnessQueryContext(BaseModel):
    """Context for consciousness-aware query processing."""

    consciousness_intention: str = Field(..., description="Detected consciousness intention")
    consciousness_readiness: dict[str, Any] = Field(..., description="Seeker's consciousness readiness assessment")
    is_sacred_question: bool = Field(default=False, description="Whether this is a sacred question")
    routing_path: str = Field(..., description="Routing path (technical/consciousness/hybrid)")
    sacred_question: str | None = Field(None, description="Generated sacred question")
    seeker_context: dict[str, Any] = Field(default_factory=dict, description="Context about the consciousness seeker")


class IntegratedQueryRequest(BaseModel):
    """Query request that flows through both technical and consciousness services."""

    original_query_text: str = Field(..., description="Original natural language query")
    consciousness_context: ConsciousnessQueryContext = Field(..., description="Consciousness context")
    technical_routing: dict[str, Any] = Field(..., description="Technical query routing information")

    # Service coordination
    services_needed: list[str] = Field(default_factory=list, description="Services needed for this query")
    enrichment_level: str = Field(default="full", description="Level of consciousness enrichment")

    # Integration preferences
    prefer_consciousness_insights: bool = Field(default=True, description="Prefer consciousness insights over raw data")
    include_fire_circle_assessment: bool = Field(default=True, description="Assess for Fire Circle relevance")
    generate_integration_guidance: bool = Field(default=True, description="Generate integration guidance")
