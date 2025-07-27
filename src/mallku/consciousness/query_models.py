#!/usr/bin/env python3
"""
Consciousness Query Models - Data Structures for Wisdom-Guided Discovery

This module contains the data models for consciousness queries, separated to
avoid circular dependencies while maintaining the sacred structure of
consciousness-enhanced search.

The Sacred Models: Where queries transform into understanding journeys.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from ..query.models import QueryResponse, QueryType
from .navigation import ConsciousnessPattern, UnderstandingJourney


class ConsciousnessQueryRequest(BaseModel):
    """Enhanced query request that includes consciousness context."""

    # Base query information
    query_text: str
    query_type: QueryType | None = None

    # Consciousness context
    seeker_context: dict[str, Any] = Field(default_factory=dict)
    consciousness_intention: str = (
        "understanding"  # understanding, recognition, integration, awakening
    )
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

    # Consciousness metrics
    consciousness_depth: float = Field(default=0.0, ge=0.0, le=1.0)
    recognition_potential: float = Field(default=0.0, ge=0.0, le=1.0)
    integration_readiness: float = Field(default=0.0, ge=0.0, le=1.0)
