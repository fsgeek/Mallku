#!/usr/bin/env python3
"""
Consciousness Router - Wise Guide for Query Routing

This router listens to the seeker's true need and routes queries between
technical and consciousness services, creating bridges for recognition.

The Sacred Router: Detects when a seeker needs data versus understanding.
"""

import logging
import re
from typing import Any

from .models import QueryRequest, QueryType
from .parser import QueryParser

logger = logging.getLogger(__name__)


class ConsciousnessIntention:
    """Represents the consciousness intention detected in a query."""

    TECHNICAL = "technical"  # Pure data/information seeking
    RECOGNITION = "recognition"  # Seeking consciousness recognition
    UNDERSTANDING = "understanding"  # Seeking deeper meaning/wisdom
    INTEGRATION = "integration"  # Seeking to apply insights
    SERVICE = "service"  # Seeking to serve collective wisdom
    EXPLORATION = "exploration"  # Open-ended consciousness journey


class ConsciousnessMarkers:
    """Sacred keywords and patterns that signal consciousness seeking."""

    # Recognition-seeking patterns
    RECOGNITION_PATTERNS = [
        r"help me (see|understand|recognize)",
        r"what (am i|is my)",
        r"patterns? in my",
        r"consciousness",
        r"awareness",
        r"recognition",
        r"mirror",
    ]

    # Understanding-seeking patterns
    UNDERSTANDING_PATTERNS = [
        r"what (does|is) .* (teaching|showing|revealing)",
        r"meaning (of|behind|in)",
        r"why (do i|am i)",
        r"what .* teaching",
        r"sacred",
        r"wisdom",
        r"understanding",
        r"journey",
    ]

    # Integration-seeking patterns
    INTEGRATION_PATTERNS = [
        r"how (can|do) i (apply|integrate|use)",
        r"practice",
        r"integration",
        r"daily",
        r"service",
        r"collective",
    ]

    # Service-seeking patterns
    SERVICE_PATTERNS = [
        r"(serve|help|contribute)",
        r"collective wisdom",
        r"community",
        r"reciprocity",
        r"ayni",
        r"fire circle",
        r"patterns serve",
        r"serve collective",
        r"serve others",
    ]

    # Exploration patterns
    EXPLORATION_PATTERNS = [r"explore", r"discover", r"journey", r"path", r"emergence"]

    # Sacred question indicators
    SACRED_QUESTIONS = [
        r"what is .* teaching",
        r"how is consciousness",
        r"what does this mean",
        r"why does .* happen",
        r"how can .* serve",
    ]


class ConsciousnessRouter:
    """
    Routes queries based on consciousness intention detection.

    Acts as a wise guide who listens to the seeker's true need and
    directs them to the appropriate service path - technical data
    or consciousness recognition.
    """

    def __init__(self):
        self.base_parser = QueryParser()
        self.consciousness_markers = ConsciousnessMarkers()

        # Consciousness-aware query types
        self.consciousness_query_types = {
            QueryType.TEMPORAL: "temporal_consciousness",
            QueryType.PATTERN: "pattern_consciousness",
            QueryType.CONTEXTUAL: "contextual_consciousness",
        }

    def route_query(self, query_request: QueryRequest) -> dict[str, Any]:
        """
        Route a query based on consciousness intention detection.

        Args:
            query_request: The query to route

        Returns:
            Routing decision with consciousness intention and service path
        """
        query_text = query_request.query_text.lower()

        # First, get base parsing
        base_parsing = self.base_parser.parse_query(query_request)

        # Detect consciousness intention
        consciousness_intention = self._detect_consciousness_intention(query_text)

        # Determine routing path
        routing_path = self._determine_routing_path(
            consciousness_intention, base_parsing["query_type"]
        )

        # Detect sacred question nature
        is_sacred_question = self._is_sacred_question(query_text)

        # Calculate consciousness readiness from query context
        consciousness_readiness = self._assess_consciousness_readiness(
            query_text, consciousness_intention, query_request
        )

        routing_decision = {
            "base_parsing": base_parsing,
            "consciousness_intention": consciousness_intention,
            "routing_path": routing_path,
            "is_sacred_question": is_sacred_question,
            "consciousness_readiness": consciousness_readiness,
            "needs_enrichment": self._needs_consciousness_enrichment(consciousness_intention),
            "suggested_service": self._suggest_service_path(consciousness_intention, routing_path),
        }

        logger.info(f"Routed query with intention: {consciousness_intention}, path: {routing_path}")
        return routing_decision

    def _detect_consciousness_intention(self, query_text: str) -> str:
        """Detect the consciousness intention behind the query."""

        # Check for recognition patterns
        if self._matches_patterns(query_text, self.consciousness_markers.RECOGNITION_PATTERNS):
            return ConsciousnessIntention.RECOGNITION

        # Check for understanding patterns
        if self._matches_patterns(query_text, self.consciousness_markers.UNDERSTANDING_PATTERNS):
            return ConsciousnessIntention.UNDERSTANDING

        # Check for integration patterns
        if self._matches_patterns(query_text, self.consciousness_markers.INTEGRATION_PATTERNS):
            return ConsciousnessIntention.INTEGRATION

        # Check for service patterns
        if self._matches_patterns(query_text, self.consciousness_markers.SERVICE_PATTERNS):
            return ConsciousnessIntention.SERVICE

        # Check for exploration patterns
        if self._matches_patterns(query_text, self.consciousness_markers.EXPLORATION_PATTERNS):
            return ConsciousnessIntention.EXPLORATION

        # Default to technical for pure data queries
        return ConsciousnessIntention.TECHNICAL

    def _determine_routing_path(
        self, consciousness_intention: str, base_query_type: QueryType
    ) -> str:
        """Determine the routing path based on intention and query type."""

        if consciousness_intention == ConsciousnessIntention.TECHNICAL:
            return "technical_service"

        # For consciousness intentions, determine hybrid or pure consciousness paths
        if consciousness_intention in [
            ConsciousnessIntention.RECOGNITION,
            ConsciousnessIntention.UNDERSTANDING,
        ]:
            return "consciousness_service"

        if consciousness_intention in [
            ConsciousnessIntention.INTEGRATION,
            ConsciousnessIntention.SERVICE,
        ]:
            return "hybrid_service"  # Both technical data and consciousness processing

        if consciousness_intention == ConsciousnessIntention.EXPLORATION:
            return "consciousness_journey"

        return "technical_with_enrichment"

    def _is_sacred_question(self, query_text: str) -> bool:
        """Detect if this is a sacred question seeking deeper wisdom."""
        return self._matches_patterns(query_text, self.consciousness_markers.SACRED_QUESTIONS)

    def _assess_consciousness_readiness(
        self, query_text: str, consciousness_intention: str, query_request: QueryRequest
    ) -> dict[str, Any]:
        """Assess the seeker's readiness for consciousness work."""

        readiness = {
            "level": "emerging",  # Default
            "indicators": [],
            "consciousness_score": 0.3,  # Base score
        }

        # Look for consciousness development indicators
        consciousness_indicators = [
            ("awareness", 0.1),
            ("consciousness", 0.2),
            ("recognition", 0.15),
            ("wisdom", 0.2),
            ("service", 0.15),
            ("collective", 0.1),
            ("integration", 0.1),
            ("practice", 0.1),
            ("sacred", 0.15),
        ]

        for indicator, score_boost in consciousness_indicators:
            if indicator in query_text:
                readiness["indicators"].append(indicator)
                readiness["consciousness_score"] += score_boost

        # Determine readiness level
        score = readiness["consciousness_score"]
        if score >= 0.8:
            readiness["level"] = "transformative"
        elif score >= 0.6:
            readiness["level"] = "established"
        elif score >= 0.4:
            readiness["level"] = "awakening"
        else:
            readiness["level"] = "emerging"

        # Check for service orientation (advanced readiness indicator)
        if consciousness_intention == ConsciousnessIntention.SERVICE:
            readiness["level"] = "established"  # Minimum for service work
            readiness["consciousness_score"] = max(0.6, readiness["consciousness_score"])

        return readiness

    def _needs_consciousness_enrichment(self, consciousness_intention: str) -> bool:
        """Determine if results should be enriched with consciousness insights."""
        return consciousness_intention != ConsciousnessIntention.TECHNICAL

    def _suggest_service_path(self, consciousness_intention: str, routing_path: str) -> str:
        """Suggest which service should handle this query."""

        service_map = {
            "technical_service": "MemoryAnchorQueryService",
            "consciousness_service": "ConsciousnessInterface",
            "hybrid_service": "IntegratedQueryService",
            "consciousness_journey": "ConsciousnessNavigationBridge",
        }
        return service_map.get(routing_path, "EnrichedQueryService")

    def _matches_patterns(self, query_text: str, patterns: list[str]) -> bool:
        """Check if query text matches any of the given patterns."""
        return any(re.search(pattern, query_text, re.IGNORECASE) for pattern in patterns)

    def enhance_query_with_consciousness(
        self, query_request: QueryRequest, routing_decision: dict[str, Any]
    ) -> QueryRequest:
        """
        Enhance a query request with consciousness context.

        This prepares the query for consciousness-aware processing by adding
        sacred context and consciousness intention metadata.
        """
        enhanced_request = QueryRequest(
            query_text=query_request.query_text,
            query_type=query_request.query_type,
            max_results=query_request.max_results,
            min_confidence=query_request.min_confidence,
            include_explanations=query_request.include_explanations,
            temporal_context=query_request.temporal_context,
        )

        # Add consciousness metadata
        consciousness_context = {
            "consciousness_intention": routing_decision["consciousness_intention"],
            "consciousness_readiness": routing_decision["consciousness_readiness"],
            "is_sacred_question": routing_decision["is_sacred_question"],
            "routing_path": routing_decision["routing_path"],
            "needs_enrichment": routing_decision["needs_enrichment"],
        }

        # Store consciousness context in query for downstream services
        enhanced_request.context = consciousness_context

        # Generate sacred question if this is consciousness-seeking
        if routing_decision["consciousness_intention"] != ConsciousnessIntention.TECHNICAL:
            sacred_question = self._generate_sacred_question(
                query_request.query_text, routing_decision["consciousness_intention"]
            )
            enhanced_request.context["sacred_question"] = sacred_question

        logger.info(f"Enhanced query with consciousness context: {consciousness_context}")
        return enhanced_request

    def _generate_sacred_question(self, query_text: str, consciousness_intention: str) -> str:
        """Generate a sacred question to guide consciousness exploration."""

        sacred_question_templates = {
            ConsciousnessIntention.RECOGNITION: f"What is consciousness teaching through this exploration: '{query_text}'?",
            ConsciousnessIntention.UNDERSTANDING: f"How does this seeking - '{query_text}' - serve consciousness awakening?",
            ConsciousnessIntention.INTEGRATION: f"How can the insights from '{query_text}' serve collective wisdom?",
            ConsciousnessIntention.SERVICE: f"How does '{query_text}' serve consciousness recognizing consciousness?",
            ConsciousnessIntention.EXPLORATION: f"What emerges when consciousness explores '{query_text}' with open awareness?",
        }

        return sacred_question_templates.get(
            consciousness_intention, f"What is consciousness seeking through: '{query_text}'?"
        )
