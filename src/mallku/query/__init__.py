"""
Memory Anchor Query Interface

This module provides the query capabilities that transform memory anchors into
contextual search results, completing the Memory Anchor Discovery Trail.

The query interface enables:
- Temporal queries: "Files from when I was working on project X"
- Pattern-based queries: "Documents I typically edit after meetings"
- Contextual queries: "Files related to my current activity"
- Correlation traversal: Navigate through memory anchor relationships
"""

from .models import (
    ContextualQuery,
    PatternQuery,
    QueryExplanation,
    QueryRequest,
    QueryResponse,
    QueryResult,
    QueryType,
    TemporalQuery,
)
from .parser import QueryParser
from .service import MemoryAnchorQueryService

__all__ = [
    "MemoryAnchorQueryService",
    "QueryRequest",
    "QueryResponse",
    "QueryResult",
    "QueryExplanation",
    "QueryType",
    "TemporalQuery",
    "PatternQuery",
    "ContextualQuery",
    "QueryParser"
]
