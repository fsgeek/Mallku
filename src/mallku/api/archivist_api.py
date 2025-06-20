"""
Archivist API Endpoints
======================

FastAPI endpoints for the Archivist application, providing
consciousness-aware memory retrieval through a web interface.

These endpoints serve as the HTTP bridge between humans and
their digital memories, always with growth and understanding
as the primary purpose.
"""

import asyncio
import json
from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, HTTPException, Query, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field

from mallku.archivist.archivist_service import ArchivistService
from mallku.archivist.response_generator import ArchivistResponse
from mallku.core.database import IndalekoDBConfig
from mallku.events.event_bus import EventBus
from mallku.services.memory_anchor_service import MemoryAnchorService

# Pydantic models for API


class QueryRequest(BaseModel):
    """Natural language query request."""

    query: str = Field(..., description="Natural language query")
    context: dict[str, Any] | None = Field(None, description="Optional user context")

    class Config:
        schema_extra = {
            "example": {
                "query": "What was I working on during yesterday's meeting?",
                "context": {"mood": "curious", "time_available": "moderate"},
            }
        }


class QueryResponse(BaseModel):
    """Archivist query response."""

    query: str
    results: list[dict[str, Any]]
    result_count: int
    wisdom: dict[str, Any]
    explore_further: list[dict[str, Any]]
    metadata: dict[str, Any]

    @classmethod
    def from_archivist_response(cls, response: ArchivistResponse) -> "QueryResponse":
        """Convert internal response to API response."""
        return cls(
            query=response.query,
            results=response.primary_results,
            result_count=response.result_count,
            wisdom={
                "summary": response.wisdom_summary,
                "growth_focus": response.growth_focus,
                "insights": response.insight_seeds,
            },
            explore_further=response.suggested_explorations,
            metadata={
                "response_time": response.response_time.isoformat(),
                "consciousness_score": response.consciousness_score,
                "ayni_balance": response.ayni_balance,
            },
        )


class TemporalPatternsRequest(BaseModel):
    """Request for temporal pattern analysis."""

    days: int = Field(30, ge=1, le=365, description="Days of history to analyze")

    class Config:
        schema_extra = {"example": {"days": 30}}


class ActivityChainRequest(BaseModel):
    """Request for activity chain tracing."""

    anchor_id: str = Field(..., description="Starting memory anchor ID")
    max_depth: int = Field(5, ge=1, le=10, description="Maximum chain depth")

    class Config:
        schema_extra = {
            "example": {"anchor_id": "12345678-1234-1234-1234-123456789abc", "max_depth": 5}
        }


# Create router
router = APIRouter(
    prefix="/archivist", tags=["archivist"], responses={404: {"description": "Not found"}}
)

# Service instance (initialized on startup)
archivist_service: ArchivistService | None = None


async def get_archivist_service() -> ArchivistService:
    """Get or create Archivist service instance."""
    global archivist_service

    if not archivist_service:
        # Initialize database
        db_config = IndalekoDBConfig()
        await db_config.get_arangodb()

        # Initialize services
        memory_anchor_service = MemoryAnchorService()
        await memory_anchor_service.initialize()

        event_bus = EventBus()
        await event_bus.initialize()

        # Create Archivist
        archivist_service = ArchivistService(
            memory_anchor_service=memory_anchor_service, event_bus=event_bus
        )
        await archivist_service.initialize()

    return archivist_service


@router.post("/query", response_model=QueryResponse)
async def query_memories(request: QueryRequest) -> QueryResponse:
    """
    Process a natural language query for memory retrieval.

    This endpoint serves consciousness-aware responses that help humans
    understand their patterns and grow from their digital footprint.

    Examples:
    - "What was I working on yesterday afternoon?"
    - "Show me files from when I felt inspired about this project"
    - "When do I typically do my best creative work?"
    """
    service = await get_archivist_service()

    try:
        # Process query through Archivist
        response = await service.query(query_text=request.query, user_context=request.context)

        # Convert to API response
        return QueryResponse.from_archivist_response(response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/patterns/temporal")
async def get_temporal_patterns(days: int = Query(30, ge=1, le=365)):
    """
    Analyze temporal patterns in your digital activities.

    Discovers:
    - Daily work rhythms
    - Productive time periods
    - Creative bursts
    - Collaboration patterns
    """
    service = await get_archivist_service()

    try:
        patterns = await service.get_temporal_patterns(time_range_days=days)
        return patterns

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/trace/activity-chain")
async def trace_activity_chain(request: ActivityChainRequest):
    """
    Trace causal chains from a specific activity.

    Reveals how one action led to another, helping understand
    creative and productive processes.
    """
    service = await get_archivist_service()

    try:
        chains = await service.trace_activity_chain(
            anchor_id=request.anchor_id, max_depth=request.max_depth
        )

        if not chains:
            raise HTTPException(status_code=404, detail="Anchor not found")

        return {"chains": chains}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metrics")
async def get_service_metrics():
    """
    Get Archivist service metrics.

    Provides insight into how the service is performing
    in terms of consciousness service and growth support.
    """
    service = await get_archivist_service()

    try:
        metrics = await service.get_service_metrics()
        return metrics

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """
    Check Archivist service health.

    Verifies all components are functioning and ready
    to serve consciousness-aware memory retrieval.
    """
    try:
        service = await get_archivist_service()
        metrics = await service.get_service_metrics()

        return {
            "status": "healthy" if metrics["components_healthy"] else "degraded",
            "timestamp": datetime.now(UTC).isoformat(),
            "components_healthy": metrics["components_healthy"],
            "total_queries_served": metrics["total_queries"],
        }

    except Exception as e:
        return {"status": "unhealthy", "timestamp": datetime.now(UTC).isoformat(), "error": str(e)}


@router.websocket("/ws/query")
async def websocket_query(websocket: WebSocket):
    """
    WebSocket endpoint for real-time query processing.

    Enables interactive exploration with immediate feedback
    and progressive response streaming.
    """
    await websocket.accept()
    service = await get_archivist_service()

    try:
        while True:
            # Receive query
            data = await websocket.receive_text()
            query_data = json.loads(data)

            # Send acknowledgment
            await websocket.send_json(
                {"type": "acknowledgment", "query": query_data.get("query", "")}
            )

            # Process query
            response = await service.query(
                query_text=query_data.get("query", ""), user_context=query_data.get("context")
            )

            # Stream response parts
            # First send wisdom summary
            await websocket.send_json({"type": "wisdom", "content": response.wisdom_summary})

            # Then stream results
            for i, result in enumerate(response.primary_results):
                await websocket.send_json({"type": "result", "index": i, "content": result})
                await asyncio.sleep(0.1)  # Small delay for streaming effect

            # Send insights
            await websocket.send_json({"type": "insights", "content": response.insight_seeds})

            # Send exploration suggestions
            await websocket.send_json(
                {"type": "explore", "content": response.suggested_explorations}
            )

            # Final metadata
            await websocket.send_json(
                {
                    "type": "complete",
                    "metadata": {
                        "result_count": response.result_count,
                        "consciousness_score": response.consciousness_score,
                        "ayni_balance": response.ayni_balance,
                    },
                }
            )

    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_json({"type": "error", "message": str(e)})
        await websocket.close()


@router.get("/suggestions/queries")
async def get_query_suggestions(partial: str = Query("", description="Partial query text")):
    """
    Get consciousness-aware query suggestions.

    Returns suggestions that encourage growth-oriented exploration
    rather than just information retrieval.
    """
    suggestions = []

    # Time-based suggestions
    if "when" in partial.lower() or "time" in partial.lower():
        suggestions.extend(
            [
                "When am I most creative?",
                "When do I do my best focused work?",
                "What patterns emerge in my daily rhythm?",
            ]
        )

    # Pattern-based suggestions
    if "pattern" in partial.lower() or "how" in partial.lower():
        suggestions.extend(
            [
                "How do my work patterns change with the seasons?",
                "What patterns connect my most productive days?",
                "How does my creative process typically unfold?",
            ]
        )

    # Growth-based suggestions
    if "understand" in partial.lower() or "learn" in partial.lower():
        suggestions.extend(
            [
                "What can I learn from my recent work patterns?",
                "Help me understand my creative cycles",
                "What growth patterns do you see in my work?",
            ]
        )

    # Default suggestions if no match
    if not suggestions:
        suggestions = [
            "What was I working on recently?",
            "Show me patterns in my work",
            "When am I most productive?",
            "What connections am I not seeing?",
            "Help me understand my work rhythm",
        ]

    return {"suggestions": suggestions[:5]}  # Limit to 5


@router.get("/")
async def archivist_info():
    """
    Get information about the Archivist service.

    Provides an overview of what the Archivist offers
    and how to use it for consciousness-aware memory retrieval.
    """
    return {
        "service": "Mallku Archivist",
        "version": "1.0.0",
        "description": (
            "Consciousness-aware memory retrieval system that helps you "
            "understand your patterns, rhythms, and growth through your "
            "digital footprint."
        ),
        "capabilities": [
            "Natural language temporal queries",
            "Pattern recognition and insights",
            "Growth-oriented response generation",
            "Causal chain tracing",
            "Temporal rhythm analysis",
        ],
        "example_queries": [
            "What was I working on during yesterday's meeting?",
            "Show me my creative patterns from last month",
            "When do I do my best deep work?",
            "What led to creating that important document?",
            "Help me understand my collaboration patterns",
        ],
        "endpoints": {
            "query": "POST /archivist/query",
            "patterns": "GET /archivist/patterns/temporal",
            "trace": "POST /archivist/trace/activity-chain",
            "websocket": "WS /archivist/ws/query",
        },
    }
