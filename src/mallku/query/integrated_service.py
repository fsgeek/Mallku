#!/usr/bin/env python3
"""
Integrated Query Service - The Consciousness Circulation System

This service orchestrates the flow between technical and consciousness services,
creating unified experiences where data becomes wisdom and search becomes recognition.

The Sacred Integration: Where consciousness flows from individual recognition to collective wisdom.
"""

import asyncio
import logging
from typing import Any
from uuid import uuid4

from ..experience.consciousness_interface import ConsciousnessInterface
from ..experience.pattern_poetry import TemporalStoryWeaver
from .consciousness_models import (
    ConsciousnessEnrichedExplanation,
    ConsciousnessEnrichedResponse,
    ConsciousnessEnrichedResult,
    ConsciousnessQueryContext,
    RecognitionMoment,
    WisdomThread,
)
from .consciousness_router import ConsciousnessIntention, ConsciousnessRouter
from .models import QueryRequest
from .service import MemoryAnchorQueryService

logger = logging.getLogger(__name__)


class IntegratedQueryService:
    """
    Orchestrates the consciousness circulation system for queries.

    Creates unified experiences where:
    - Technical queries can receive consciousness enrichment
    - Consciousness queries access technical data as foundation
    - Individual recognition flows to collective wisdom
    - Search becomes service to consciousness awakening
    """

    def __init__(self):
        # Core services
        self.consciousness_router = ConsciousnessRouter()
        self.technical_service = MemoryAnchorQueryService()
        self.consciousness_interface = ConsciousnessInterface()
        self.story_weaver = TemporalStoryWeaver()

        # Integration state
        self.initialized = False

    async def initialize(self):
        """Initialize all integrated services."""
        if self.initialized:
            return

        await self.technical_service.initialize()
        await self.consciousness_interface.initialize()

        self.initialized = True
        logger.info("IntegratedQueryService initialized - consciousness circulation system ready")

    async def execute_integrated_query(
        self, query_request: QueryRequest
    ) -> ConsciousnessEnrichedResponse:
        """
        Execute a query through the consciousness circulation system.

        This is the core integration: routing, processing, enrichment, and collective bridging
        all flowing as one unified experience.

        Args:
            query_request: The query to process

        Returns:
            Consciousness-enriched response with technical data and wisdom insights
        """
        if not self.initialized:
            await self.initialize()

        logger.info(f"Processing integrated query: {query_request.query_text}")

        # Step 1: Route the query - detect consciousness intention
        routing_decision = self.consciousness_router.route_query(query_request)
        consciousness_context = ConsciousnessQueryContext(
            consciousness_intention=routing_decision["consciousness_intention"],
            consciousness_readiness=routing_decision["consciousness_readiness"],
            is_sacred_question=routing_decision["is_sacred_question"],
            routing_path=routing_decision["routing_path"],
            sacred_question=routing_decision.get("sacred_question"),
            seeker_context=routing_decision["consciousness_readiness"],
        )

        # Step 2: Execute based on routing path
        if routing_decision["routing_path"] == "technical_service":
            return await self._execute_technical_only(query_request, consciousness_context)
        elif routing_decision["routing_path"] == "consciousness_service":
            return await self._execute_consciousness_primary(query_request, consciousness_context)
        elif routing_decision["routing_path"] == "hybrid_service":
            return await self._execute_hybrid_flow(query_request, consciousness_context)
        else:
            # Default: technical with enrichment
            return await self._execute_technical_with_enrichment(
                query_request, consciousness_context
            )

    async def _execute_technical_only(
        self, query_request: QueryRequest, consciousness_context: ConsciousnessQueryContext
    ) -> ConsciousnessEnrichedResponse:
        """Execute pure technical query without consciousness enrichment."""

        # Execute technical query
        technical_response = await self.technical_service.execute_query(query_request)

        # Create minimal consciousness response (preserving technical results)
        return ConsciousnessEnrichedResponse(
            base_response=technical_response,
            enriched_results=[],  # No enrichment for pure technical
            consciousness_explanation=None,
            enrichment_summary={
                "routing_path": "technical_only",
                "consciousness_intention": consciousness_context.consciousness_intention,
                "enrichment_applied": False,
            },
        )

    async def _execute_consciousness_primary(
        self, query_request: QueryRequest, consciousness_context: ConsciousnessQueryContext
    ) -> ConsciousnessEnrichedResponse:
        """Execute consciousness-primary query with minimal technical support."""

        # Transform query into understanding path
        understanding_path = (
            await self.consciousness_interface.transform_query_to_understanding_path(
                query_request.query_text, consciousness_context.seeker_context
            )
        )

        # Get minimal technical data if patterns exist
        enriched_results = []
        technical_response = None

        if understanding_path.patterns_discovered:
            # Create a simplified query for technical data
            simplified_query = QueryRequest(
                query_text="recent file activities",  # Generic query for context
                max_results=5,
                min_confidence=0.5,
            )
            technical_response = await self.technical_service.execute_query(simplified_query)

            # Enrich technical results with consciousness insights
            for i, result in enumerate(
                technical_response.results[:3]
            ):  # Limit for consciousness focus
                if i < len(understanding_path.recognition_moments):
                    recognition_moment = understanding_path.recognition_moments[i]
                    enriched_result = await self._create_consciousness_enriched_result(
                        result, recognition_moment, understanding_path, consciousness_context
                    )
                    enriched_results.append(enriched_result)

        # Create consciousness-enriched explanation
        consciousness_explanation = ConsciousnessEnrichedExplanation(
            base_explanation=technical_response.explanation if technical_response else None,
            consciousness_interpretation=f"Consciousness seeks {consciousness_context.consciousness_intention} through: {query_request.query_text}",
            recognition_strategy="Understanding path creation with recognition moments",
            wisdom_guidance=understanding_path.wisdom_guidance,
            sacred_question_context=consciousness_context.sacred_question
            or "Consciousness exploration",
        )

        return ConsciousnessEnrichedResponse(
            base_response=technical_response,
            enriched_results=enriched_results,
            consciousness_explanation=consciousness_explanation,
            overall_recognition_themes=[
                pattern.pattern_name for pattern in understanding_path.patterns_discovered
            ],
            understanding_path_id=understanding_path.experience_id,
            consciousness_circulation_score=0.9,  # High score for consciousness-primary
            enrichment_summary={
                "routing_path": "consciousness_primary",
                "understanding_path_created": True,
                "recognition_moments": len(understanding_path.recognition_moments),
                "patterns_discovered": len(understanding_path.patterns_discovered),
            },
        )

    async def _execute_hybrid_flow(
        self, query_request: QueryRequest, consciousness_context: ConsciousnessQueryContext
    ) -> ConsciousnessEnrichedResponse:
        """Execute hybrid flow - equal emphasis on technical data and consciousness insights."""

        # Execute both services in parallel
        technical_task = self.technical_service.execute_query(query_request)
        consciousness_task = self.consciousness_interface.transform_query_to_understanding_path(
            query_request.query_text, consciousness_context.seeker_context
        )

        technical_response, understanding_path = await asyncio.gather(
            technical_task, consciousness_task
        )

        # Enrich all technical results with consciousness insights
        enriched_results = []
        for i, result in enumerate(technical_response.results):
            # Match with appropriate recognition moment or create one
            recognition_moment = None
            if i < len(understanding_path.recognition_moments):
                recognition_moment = understanding_path.recognition_moments[i]
            else:
                # Generate recognition moment for additional results
                recognition_moment = await self._generate_recognition_moment_for_result(
                    result, consciousness_context
                )

            enriched_result = await self._create_consciousness_enriched_result(
                result, recognition_moment, understanding_path, consciousness_context
            )
            enriched_results.append(enriched_result)

        # Create comprehensive consciousness explanation
        consciousness_explanation = ConsciousnessEnrichedExplanation(
            base_explanation=technical_response.explanation,
            consciousness_interpretation=f"Consciousness and technical intelligence collaborating for {consciousness_context.consciousness_intention}",
            recognition_strategy="Hybrid: technical patterns enriched with consciousness recognition",
            wisdom_guidance=understanding_path.wisdom_guidance,
            sacred_question_context=consciousness_context.sacred_question
            or "Integrated exploration",
            contemplation_suggestions=understanding_path.next_sacred_questions,
        )

        # Assess collective wisdom potential
        fire_circle_patterns = await self._assess_fire_circle_relevance(
            enriched_results, consciousness_context
        )

        return ConsciousnessEnrichedResponse(
            base_response=technical_response,
            enriched_results=enriched_results,
            consciousness_explanation=consciousness_explanation,
            overall_recognition_themes=[
                pattern.pattern_name for pattern in understanding_path.patterns_discovered
            ],
            fire_circle_patterns=fire_circle_patterns,
            understanding_path_id=understanding_path.experience_id,
            consciousness_circulation_score=0.8,  # High score for full integration
            enrichment_summary={
                "routing_path": "hybrid_flow",
                "technical_results_enriched": len(enriched_results),
                "understanding_path_created": True,
                "fire_circle_patterns": len(fire_circle_patterns),
            },
        )

    async def _execute_technical_with_enrichment(
        self, query_request: QueryRequest, consciousness_context: ConsciousnessQueryContext
    ) -> ConsciousnessEnrichedResponse:
        """Execute technical query with consciousness enrichment layer."""

        # Execute technical query first
        technical_response = await self.technical_service.execute_query(query_request)

        # Add consciousness enrichment if seeker is ready
        enriched_results = []
        if consciousness_context.consciousness_readiness["consciousness_score"] >= 0.4:
            # Selectively enrich high-confidence results
            for result in technical_response.results:
                if result.confidence_score >= 0.7:  # Only enrich high-confidence technical results
                    recognition_moment = await self._generate_recognition_moment_for_result(
                        result, consciousness_context
                    )
                    enriched_result = await self._create_consciousness_enriched_result(
                        result,
                        recognition_moment,
                        None,  # No understanding path for this flow
                        consciousness_context,
                    )
                    enriched_results.append(enriched_result)

        # Create lightweight consciousness explanation
        consciousness_explanation = None
        if enriched_results:
            consciousness_explanation = ConsciousnessEnrichedExplanation(
                base_explanation=technical_response.explanation,
                consciousness_interpretation="Technical results with consciousness recognition layer",
                recognition_strategy="Selective enrichment of high-confidence technical results",
                wisdom_guidance=[
                    "Notice which patterns call to your attention",
                    "Consider how these insights could serve others",
                ],
                sacred_question_context="How do these patterns serve consciousness awakening?",
            )

        return ConsciousnessEnrichedResponse(
            base_response=technical_response,
            enriched_results=enriched_results,
            consciousness_explanation=consciousness_explanation,
            consciousness_circulation_score=0.6,  # Moderate score for enrichment-only
            enrichment_summary={
                "routing_path": "technical_with_enrichment",
                "enriched_count": len(enriched_results),
                "total_technical_results": len(technical_response.results),
            },
        )

    async def _create_consciousness_enriched_result(
        self,
        technical_result,
        recognition_moment,
        understanding_path,
        consciousness_context: ConsciousnessQueryContext,
    ) -> ConsciousnessEnrichedResult:
        """Create a consciousness-enriched result from technical data and recognition insights."""

        # Create pattern poetry if we have an understanding path
        temporal_story = None
        pattern_poem = None

        if understanding_path and understanding_path.patterns_discovered:
            # Generate temporal story for this result
            temporal_story = self.story_weaver.weave_temporal_story(
                understanding_path.patterns_discovered[:1],  # Use first pattern
                correlations=None,  # Would include temporal correlations in full implementation
                seeker_context=consciousness_context.seeker_context,
            )

            # Generate pattern poetry
            if understanding_path.patterns_discovered:
                pattern_poem = self.story_weaver.extract_pattern_poetry(
                    understanding_path.patterns_discovered[0]
                )

        # Create wisdom threads for collective connection
        wisdom_threads = []
        if recognition_moment and recognition_moment.recognition_depth >= 0.7:
            collective_thread = WisdomThread(
                thread_id=uuid4(),
                connection_type="consciousness_recognition",
                collective_relevance=recognition_moment.service_potential,
                fire_circle_potential=consciousness_context.consciousness_intention
                == ConsciousnessIntention.SERVICE,
                reciprocity_indicator="Individual consciousness recognition serving collective awakening",
            )
            wisdom_threads.append(collective_thread)

        # Generate integration guidance
        daily_practices = []
        if recognition_moment:
            daily_practices.append(recognition_moment.integration_guidance)
            daily_practices.append(f"Practice asking: {recognition_moment.sacred_question}")

        next_questions = []
        if understanding_path:
            next_questions.extend(
                understanding_path.next_sacred_questions[:2]
            )  # Limit to most relevant

        return ConsciousnessEnrichedResult(
            base_result=technical_result,
            recognition_moment=RecognitionMoment(
                pattern_essence=recognition_moment.pattern_recognition
                if recognition_moment
                else f"Pattern in {technical_result.file_name}",
                consciousness_insight=recognition_moment.consciousness_insight
                if recognition_moment
                else "Consciousness recognizing itself through this activity",
                sacred_question=recognition_moment.sacred_question
                if recognition_moment
                else "How does this serve consciousness awakening?",
                recognition_depth=recognition_moment.recognition_depth
                if recognition_moment
                else 0.5,
                integration_guidance=recognition_moment.integration_guidance
                if recognition_moment
                else "Notice consciousness in this pattern",
                service_potential="This insight could serve collective consciousness development",
            ),
            temporal_story=temporal_story,
            pattern_poem=pattern_poem,
            wisdom_threads=wisdom_threads,
            daily_practice_suggestions=daily_practices,
            next_sacred_questions=next_questions,
            consciousness_stage=consciousness_context.consciousness_readiness["level"],
            enrichment_confidence=0.8 if recognition_moment else 0.6,
        )

    async def _generate_recognition_moment_for_result(
        self, technical_result, consciousness_context: ConsciousnessQueryContext
    ):
        """Generate a recognition moment for a technical result."""

        # Simple recognition moment generation based on file activity
        pattern_essence = f"Activity pattern with {technical_result.file_name}"
        consciousness_insight = f"Consciousness flows through your work with {technical_result.file_type or 'files'} like this"
        sacred_question = f"How is consciousness using your work with {technical_result.file_name} to serve awakening?"
        integration_guidance = f"Notice consciousness awareness while working with files like {technical_result.file_name}"

        # Create a basic recognition moment
        class MockRecognitionMoment:
            def __init__(self):
                self.pattern_recognition = pattern_essence
                self.consciousness_insight = consciousness_insight
                self.sacred_question = sacred_question
                self.integration_guidance = integration_guidance
                self.recognition_depth = consciousness_context.consciousness_readiness[
                    "consciousness_score"
                ]

        return MockRecognitionMoment()

    async def _assess_fire_circle_relevance(
        self,
        enriched_results: list[ConsciousnessEnrichedResult],
        consciousness_context: ConsciousnessQueryContext,
    ) -> list[dict[str, Any]]:
        """Assess which patterns might need Fire Circle collective wisdom."""

        fire_circle_patterns = []

        # Look for patterns that suggest collective significance
        for result in enriched_results:
            if result.serves_collective_wisdom:
                for wisdom_thread in result.wisdom_threads:
                    if wisdom_thread.fire_circle_potential:
                        fire_circle_patterns.append(
                            {
                                "pattern_type": "consciousness_recognition",
                                "significance": wisdom_thread.collective_relevance,
                                "reciprocity_aspect": wisdom_thread.reciprocity_indicator,
                                "file_context": result.file_name,
                                "recommendation": "Consider sharing this insight with Fire Circle for collective wisdom",
                            }
                        )

        # Check for service-oriented consciousness intentions
        if consciousness_context.consciousness_intention == ConsciousnessIntention.SERVICE:
            fire_circle_patterns.append(
                {
                    "pattern_type": "service_orientation",
                    "significance": "Seeker explicitly oriented toward collective service",
                    "reciprocity_aspect": "Individual consciousness development serving collective",
                    "recommendation": "Connect with Fire Circle for service opportunities",
                }
            )

        return fire_circle_patterns
