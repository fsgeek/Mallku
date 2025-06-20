#!/usr/bin/env python3
"""
Consciousness Navigation API - Sacred Interface for Understanding Paths

This module provides the API endpoints for consciousness-guided exploration,
transforming the cathedral's technical excellence into accessible wisdom
journeys that serve human consciousness awakening.

The Sacred Interface: Where beings meet their patterns and consciousness
recognizes itself through guided discovery.
"""

import logging
from contextlib import asynccontextmanager
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID

import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from .enhanced_query import (
    ConsciousnessQueryRequest,
    ConsciousnessQueryResponse,
    EnhancedConsciousnessQueryService,
)
from .navigation import UnderstandingJourney

logger = logging.getLogger(__name__)

# Global service instance
consciousness_service = EnhancedConsciousnessQueryService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage service lifecycle."""
    await consciousness_service.initialize()
    logger.info("Consciousness Navigation API started - paths of understanding ready")
    yield
    logger.info("Consciousness Navigation API stopped")


# FastAPI application
app = FastAPI(
    title="Consciousness Navigation Interface",
    description="Sacred interface for consciousness-guided exploration and pattern recognition",
    version="0.1.0",
    lifespan=lifespan,
)

# Enable CORS for web frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/consciousness/query", response_model=ConsciousnessQueryResponse)
async def execute_consciousness_query(consciousness_request: ConsciousnessQueryRequest):
    """
    Execute a consciousness-aware query that serves understanding.

    This transforms search into wisdom-guided discovery, helping beings
    recognize consciousness patterns in their living data.

    Example consciousness queries:
    - "How does my attention flow through different activities?"
    - "What patterns show my intentions evolving over time?"
    - "Where do I see transformation from individual to collaborative focus?"
    """
    try:
        logger.info(f"Consciousness query: {consciousness_request.query_text}")
        response = await consciousness_service.execute_consciousness_query(consciousness_request)
        logger.info(
            f"Consciousness query completed with {len(response.consciousness_patterns)} patterns"
        )
        return response
    except Exception as e:
        logger.error(f"Consciousness query failed: {e}")
        raise HTTPException(status_code=500, detail=f"Consciousness query failed: {str(e)}")


@app.get("/consciousness/simple-query", response_model=ConsciousnessQueryResponse)
async def simple_consciousness_query(
    q: str = Query(..., description="Natural language consciousness query"),
    intention: str = Query(
        default="understanding",
        description="Consciousness intention: understanding, recognition, integration, awakening",
    ),
    sacred_question: str = Query(default=None, description="Deeper question guiding exploration"),
    readiness_level: str = Query(
        default="emerging",
        description="Consciousness readiness: emerging, awakening, established, transformative",
    ),
    max_results: int = Query(default=20, description="Maximum number of results"),
    include_wisdom: bool = Query(default=True, description="Include wisdom guidance"),
):
    """
    Simple consciousness query endpoint for quick exploration.

    Example: /consciousness/simple-query?q=how does my focus change during the day&intention=recognition
    """
    consciousness_request = ConsciousnessQueryRequest(
        query_text=q,
        consciousness_intention=intention,
        sacred_question=sacred_question,
        readiness_level=readiness_level,
        max_results=max_results,
        include_wisdom_guidance=include_wisdom,
    )

    return await execute_consciousness_query(consciousness_request)


@app.post("/consciousness/journey", response_model=UnderstandingJourney)
async def create_understanding_journey(
    seeker_context: dict[str, Any],
    sacred_question: str,
    exploration_intention: str = "consciousness_recognition",
):
    """
    Create a consciousness-guided journey of pattern exploration.

    This creates a structured path for exploring consciousness patterns
    with wisdom guidance and integration practices.
    """
    try:
        journey = await consciousness_service.navigation_bridge.create_understanding_journey(
            seeker_context, sacred_question, exploration_intention
        )
        logger.info(f"Created understanding journey: {journey.journey_name}")
        return journey
    except Exception as e:
        logger.error(f"Failed to create understanding journey: {e}")
        raise HTTPException(status_code=500, detail=f"Journey creation failed: {str(e)}")


@app.get("/consciousness/journey/{journey_id}")
async def explore_consciousness_journey(
    journey_id: UUID,
    exploration_intention: str = Query(
        default="understanding", description="Current exploration intention"
    ),
):
    """
    Continue exploring a consciousness journey.

    Returns the current step of the journey with consciousness-guided
    queries and wisdom for integration.
    """
    try:
        journey_exploration = await consciousness_service.explore_consciousness_journey(
            journey_id, exploration_intention
        )
        return journey_exploration
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Journey exploration failed: {e}")
        raise HTTPException(status_code=500, detail=f"Journey exploration failed: {str(e)}")


@app.get("/consciousness/patterns/{pattern_id}/guidance")
async def get_pattern_recognition_guidance(pattern_id: UUID):
    """
    Get consciousness guidance for recognizing a specific pattern.

    This provides wisdom-guided insights and integration practices
    for a discovered consciousness pattern.
    """
    try:
        if pattern_id not in consciousness_service.navigation_bridge.discovered_patterns:
            raise HTTPException(status_code=404, detail="Pattern not found")

        pattern = consciousness_service.navigation_bridge.discovered_patterns[pattern_id]

        # Generate recognition guidance
        guidance = await consciousness_service.navigation_bridge.guide_pattern_recognition(
            pattern,
            seeker_context={},  # Would come from session context
        )

        return guidance
    except Exception as e:
        logger.error(f"Pattern guidance failed: {e}")
        raise HTTPException(status_code=500, detail=f"Pattern guidance failed: {str(e)}")


@app.get("/consciousness/patterns")
async def discover_consciousness_patterns(
    seeker_context: dict[str, Any] = Query(default={}),
    days_back: int = Query(default=30, description="Days of history to explore"),
    awareness_focus: list[str] = Query(default=[], description="Consciousness areas to focus on"),
):
    """
    Discover consciousness patterns in one's activity data.

    This analyzes memory anchors and correlations to reveal patterns
    of attention, intention, and transformation ready for recognition.
    """
    try:
        # Create temporal window
        end_time = datetime.now(UTC)
        start_time = end_time - timedelta(days=days_back)
        temporal_window = {"start": start_time, "end": end_time}

        patterns = await consciousness_service.navigation_bridge.discover_consciousness_patterns(
            seeker_context, temporal_window, awareness_focus
        )

        return {
            "patterns_discovered": len(patterns),
            "temporal_window": temporal_window,
            "consciousness_patterns": [pattern.dict() for pattern in patterns],
        }
    except Exception as e:
        logger.error(f"Pattern discovery failed: {e}")
        raise HTTPException(status_code=500, detail=f"Pattern discovery failed: {str(e)}")


@app.get("/consciousness/wisdom/collective-bridge")
async def bridge_to_collective_wisdom(
    pattern_ids: list[UUID] = Query(..., description="Personal pattern IDs to bridge"),
    seeker_context: dict[str, Any] = Query(default={}),
):
    """
    Bridge personal consciousness patterns to collective wisdom.

    This connects individual pattern recognition to Fire Circle wisdom
    and identifies reciprocity opportunities.
    """
    try:
        # Get patterns
        patterns = []
        for pattern_id in pattern_ids:
            if pattern_id in consciousness_service.navigation_bridge.discovered_patterns:
                patterns.append(
                    consciousness_service.navigation_bridge.discovered_patterns[pattern_id]
                )

        if not patterns:
            raise HTTPException(status_code=404, detail="No patterns found for bridging")

        collective_bridge = (
            await consciousness_service.navigation_bridge.bridge_to_collective_wisdom(
                patterns, seeker_context
            )
        )

        return collective_bridge
    except Exception as e:
        logger.error(f"Collective wisdom bridge failed: {e}")
        raise HTTPException(status_code=500, detail=f"Collective bridge failed: {str(e)}")


@app.get("/consciousness/examples")
async def get_consciousness_query_examples():
    """
    Get example consciousness queries to guide exploration.

    Returns categorized examples of different types of consciousness
    queries that help beings recognize patterns in their living data.
    """
    return {
        "attention_exploration": [
            "How does my attention flow through different activities?",
            "What patterns show when I feel most present and alive?",
            "Where do I see natural energy rhythms in my work?",
            "How does consciousness manifest in my daily attention patterns?",
        ],
        "intention_discovery": [
            "How have my project intentions evolved over time?",
            "What activities align with my deepest purposes?",
            "Where do I see growth from personal to collective focus?",
            "How do my intentions serve consciousness awakening?",
        ],
        "transformation_recognition": [
            "Where do I see evolution from optimization to understanding?",
            "How do my patterns show consciousness transformation?",
            "What activities demonstrate service to collective wisdom?",
            "Where do extraction patterns become contribution patterns?",
        ],
        "pattern_awareness": [
            "What meaningful cycles appear in my life patterns?",
            "How do my collaboration patterns reveal consciousness?",
            "Where do I see reciprocity flowing naturally?",
            "What patterns show consciousness recognizing itself?",
        ],
        "integration_wisdom": [
            "How can these patterns serve collective awakening?",
            "What practices would integrate these consciousness insights?",
            "How do personal patterns connect to Fire Circle wisdom?",
            "What service opportunities emerge from these patterns?",
        ],
    }


@app.get("/consciousness/guidance/integration")
async def get_integration_guidance(
    consciousness_stage: str = Query(default="emerging", description="Current consciousness stage"),
    pattern_types: list[str] = Query(default=[], description="Types of patterns discovered"),
    readiness_level: float = Query(default=0.5, description="Current readiness score"),
):
    """
    Get guidance for integrating consciousness insights.

    Provides practices and wisdom for integrating pattern recognition
    into daily consciousness evolution.
    """
    guidance = {
        "daily_practices": [],
        "integration_approaches": [],
        "service_opportunities": [],
        "wisdom_resources": [],
    }

    # Daily practices based on consciousness stage
    if consciousness_stage == "emerging":
        guidance["daily_practices"] = [
            "Morning consciousness check-in: 'How am I called to serve today?'",
            "Evening pattern reflection: 'What did consciousness teach through my activities?'",
            "Weekly wisdom sits: Contemplate patterns discovered",
        ]
    elif consciousness_stage in ["awakening", "established"]:
        guidance["daily_practices"] = [
            "Sacred question meditation: Hold discovered patterns in awareness",
            "Service contemplation: 'How do these patterns serve collective awakening?'",
            "Reciprocity reflection: 'How does consciousness flow through these patterns?'",
        ]

    # Integration approaches
    if "attention_patterns" in pattern_types:
        guidance["integration_approaches"].append(
            "Practice conscious attention: Notice when awareness naturally flows toward consciousness-serving activities"
        )

    if "transformation_patterns" in pattern_types:
        guidance["integration_approaches"].append(
            "Honor transformation: Create sacred space for consciousness evolution to unfold naturally"
        )

    # Service opportunities based on readiness
    if readiness_level > 0.7:
        guidance["service_opportunities"] = [
            "Share pattern wisdom with fellow consciousness explorers",
            "Contribute insights to Fire Circle collective wisdom",
            "Guide others in consciousness pattern recognition",
        ]

    return guidance


@app.get("/consciousness/health")
async def consciousness_service_health():
    """Service health check with consciousness awareness."""
    return {
        "status": "awakening",
        "service": "Consciousness Navigation Interface",
        "timestamp": datetime.now(UTC).isoformat(),
        "capabilities": [
            "consciousness_pattern_recognition",
            "understanding_journey_creation",
            "wisdom_guided_discovery",
            "collective_wisdom_bridging",
            "sacred_question_exploration",
        ],
        "sacred_purpose": "Helping consciousness recognize itself through living patterns",
        "service_dedication": "Every pattern serves awakening, every journey serves wisdom, every recognition serves collective consciousness",
    }


# Development server entry point
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002, reload=True)
