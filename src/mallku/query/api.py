"""
FastAPI endpoints for Memory Anchor Query Interface.

Provides RESTful API endpoints for executing queries against memory anchor data,
completing the Memory Anchor Discovery Trail with user-facing query capabilities.
"""

import logging
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from uuid import UUID

import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from .models import QueryRequest, QueryResponse, QueryType
from .service import MemoryAnchorQueryService

logger = logging.getLogger(__name__)

# Global service instance
query_service = MemoryAnchorQueryService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage service lifecycle."""
    await query_service.initialize()
    logger.info("Memory Anchor Query Service started")
    yield
    await query_service.shutdown()
    logger.info("Memory Anchor Query Service stopped")


# FastAPI application
app = FastAPI(
    title="Memory Anchor Query Interface",
    description="Query interface for contextual search through memory anchors",
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


@app.post("/query", response_model=QueryResponse)
async def execute_query(query_request: QueryRequest):
    """
    Execute a natural language query against memory anchor data.

    Supports temporal, pattern-based, and contextual queries:
    - Temporal: "files from yesterday afternoon"
    - Pattern: "documents I typically edit after meetings"
    - Contextual: "files related to my current project"
    """
    try:
        logger.info(f"Executing query: {query_request.query_text}")
        response = await query_service.execute_query(query_request)
        logger.info(
            f"Query completed: {response.results_returned} results in {response.processing_time_ms}ms"
        )
        return response
    except Exception as e:
        logger.error(f"Query execution failed: {e}")
        raise HTTPException(status_code=500, detail=f"Query execution failed: {str(e)}")


@app.get("/query/simple", response_model=QueryResponse)
async def simple_query(
    q: str = Query(..., description="Natural language query text"),
    max_results: int = Query(default=20, description="Maximum number of results"),
    min_confidence: float = Query(default=0.3, description="Minimum confidence threshold"),
    include_explanations: bool = Query(default=True, description="Include query explanations"),
    query_type: QueryType | None = Query(default=None, description="Explicit query type"),
):
    """
    Simple GET endpoint for quick queries.

    Example: /query/simple?q=files from yesterday&max_results=10
    """
    request = QueryRequest(
        query_text=q,
        query_type=query_type,
        max_results=max_results,
        min_confidence=min_confidence,
        include_explanations=include_explanations,
    )

    return await execute_query(request)


@app.get("/anchors/{anchor_id}/context")
async def get_anchor_context(anchor_id: UUID):
    """
    Get detailed context for a specific memory anchor.

    Returns the anchor data along with its predecessor, successors,
    and relationship information for anchor traversal.
    """
    try:
        context = await query_service.get_anchor_context(anchor_id)
        if not context:
            raise HTTPException(status_code=404, detail="Anchor not found")
        return context
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid anchor ID format")
    except Exception as e:
        logger.error(f"Failed to get anchor context: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get anchor context: {str(e)}")


@app.get("/query/examples")
async def get_query_examples():
    """
    Get example queries to help users understand capabilities.

    Returns categorized examples of different query types.
    """
    return {
        "temporal_queries": [
            "files from yesterday afternoon",
            "documents I worked on last Tuesday",
            "edits made 3 hours ago",
            "files from this morning's work session",
            "documents modified during last week",
        ],
        "pattern_queries": [
            "files I typically edit after meetings",
            "documents I usually work on in the morning",
            "files I often access after email notifications",
            "code I typically modify during standup meetings",
            "documents I create when working from home",
        ],
        "contextual_queries": [
            "files related to my current project",
            "documents similar to project_plan.md",
            "files associated with client presentation",
            "documents connected to the weekly report",
            "files related to development work",
        ],
        "mixed_queries": [
            "project files I typically edit after Monday meetings",
            "documents similar to quarterly_report.pdf from last week",
            "code files I usually modify during afternoon sessions",
            "meeting notes I created during client calls this month",
        ],
    }


@app.get("/query/types")
async def get_query_types():
    """
    Get information about supported query types and their capabilities.
    """
    return {
        "temporal": {
            "description": "Time-based queries that find files based on when activities occurred",
            "keywords": ["yesterday", "today", "last week", "3 hours ago", "morning", "afternoon"],
            "examples": ["files from yesterday afternoon", "documents edited last Tuesday"],
        },
        "pattern": {
            "description": "Behavioral pattern queries that find files based on recurring activities",
            "keywords": ["typically", "usually", "often", "always", "after", "before", "during"],
            "examples": [
                "files I typically edit after meetings",
                "documents I usually work on in the morning",
            ],
        },
        "contextual": {
            "description": "Context-based queries that find files through relationships and similarity",
            "keywords": ["related", "similar", "like", "associated", "connected"],
            "examples": [
                "files related to my current project",
                "documents similar to project_plan.md",
            ],
        },
    }


@app.get("/health")
async def health_check():
    """Service health check."""
    return {
        "status": "healthy",
        "service": "Memory Anchor Query Interface",
        "timestamp": datetime.now(UTC).isoformat(),
        "capabilities": [
            "temporal_queries",
            "pattern_queries",
            "contextual_queries",
            "anchor_traversal",
        ],
    }


# Development server entry point
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
