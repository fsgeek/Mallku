"""
Query models for Memory Anchor querying.

These models define the request/response structures for different types
of memory anchor queries and their results.
"""

from datetime import UTC, datetime
from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class QueryType(str, Enum):
    """Types of queries supported by the query interface."""
    TEMPORAL = "temporal"
    PATTERN = "pattern"
    CONTEXTUAL = "contextual"
    ANCHOR_TRAVERSAL = "anchor_traversal"


class ConfidenceLevel(str, Enum):
    """Confidence levels for query results."""
    HIGH = "high"      # > 0.8
    MEDIUM = "medium"  # 0.5 - 0.8
    LOW = "low"        # < 0.5


class QueryRequest(BaseModel):
    """Base query request model."""
    query_text: str = Field(..., description="Natural language query text")
    query_type: QueryType | None = Field(None, description="Explicit query type (auto-detected if None)")
    max_results: int = Field(default=20, description="Maximum number of results to return")
    min_confidence: float = Field(default=0.3, description="Minimum confidence threshold")
    include_explanations: bool = Field(default=True, description="Include query explanations")
    temporal_context: datetime | None = Field(None, description="Reference time for temporal queries")
    context: dict[str, Any] = Field(default_factory=dict, description="Additional context information")


class TemporalQuery(BaseModel):
    """Temporal query with time range constraints."""
    start_time: datetime | None = Field(None, description="Start of time range")
    end_time: datetime | None = Field(None, description="End of time range")
    relative_time: str | None = Field(None, description="Relative time expression (e.g., 'last Tuesday afternoon')")
    time_window_minutes: int | None = Field(None, description="Time window in minutes around reference time")


class PatternQuery(BaseModel):
    """Pattern-based query for recurring behaviors."""
    pattern_type: str = Field(..., description="Type of pattern to search for")
    context_keywords: list[str] = Field(default_factory=list, description="Keywords for pattern context")
    frequency_threshold: int = Field(default=3, description="Minimum pattern occurrences")


class ContextualQuery(BaseModel):
    """Contextual query based on current activity or relationships."""
    reference_file: str | None = Field(None, description="Reference file path for similarity")
    reference_anchor_id: UUID | None = Field(None, description="Reference memory anchor")
    context_tags: list[str] = Field(default_factory=list, description="Context tags to match")
    similarity_threshold: float = Field(default=0.6, description="Similarity threshold")


class QueryResult(BaseModel):
    """Individual query result with correlation metadata."""
    file_path: str = Field(..., description="Path to the file")
    file_name: str = Field(..., description="Name of the file")
    file_size: int | None = Field(None, description="File size in bytes")
    file_type: str | None = Field(None, description="MIME type of the file")

    # Correlation metadata
    anchor_id: UUID = Field(..., description="Memory anchor ID that matched")
    correlation_type: str = Field(..., description="Type of correlation that matched")
    confidence_score: float = Field(..., description="Confidence score (0.0 - 1.0)")
    confidence_level: ConfidenceLevel = Field(..., description="Confidence level category")

    # Temporal information
    last_modified: datetime = Field(..., description="Last modification time")
    anchor_timestamp: datetime = Field(..., description="Timestamp of matching memory anchor")

    # Context and explanation
    correlation_tags: list[str] = Field(default_factory=list, description="Tags that contributed to the match")
    context: dict[str, Any] = Field(default_factory=dict, description="Additional context information")

    @classmethod
    def from_memory_anchor_and_file(
        cls,
        anchor_id: UUID,
        anchor_timestamp: datetime,
        file_info: dict[str, Any],
        correlation_type: str,
        confidence_score: float,
        correlation_tags: list[str] = None
    ) -> "QueryResult":
        """Create QueryResult from memory anchor and file information."""

        # Determine confidence level
        if confidence_score >= 0.8:
            confidence_level = ConfidenceLevel.HIGH
        elif confidence_score >= 0.5:
            confidence_level = ConfidenceLevel.MEDIUM
        else:
            confidence_level = ConfidenceLevel.LOW

        return cls(
            file_path=file_info["file_path"],
            file_name=file_info.get("file_name", file_info["file_path"].split("/")[-1]),
            file_size=file_info.get("file_size"),
            file_type=file_info.get("mime_type"),
            anchor_id=anchor_id,
            correlation_type=correlation_type,
            confidence_score=confidence_score,
            confidence_level=confidence_level,
            last_modified=datetime.fromisoformat(file_info.get("last_modified", anchor_timestamp.isoformat())),
            anchor_timestamp=anchor_timestamp,
            correlation_tags=correlation_tags or [],
            context=file_info.get("context", {})
        )


class QueryExplanation(BaseModel):
    """Explanation of how query results were derived."""
    query_interpretation: str = Field(..., description="How the query was interpreted")
    search_strategy: str = Field(..., description="Search strategy used")
    filters_applied: list[str] = Field(default_factory=list, description="Filters applied during search")
    anchors_searched: int = Field(..., description="Number of memory anchors searched")
    correlations_found: int = Field(..., description="Number of correlations found")
    ranking_factors: list[str] = Field(default_factory=list, description="Factors used for result ranking")


class QueryResponse(BaseModel):
    """Complete query response with results and metadata."""
    query_text: str = Field(..., description="Original query text")
    query_type: QueryType = Field(..., description="Detected or specified query type")

    # Results
    results: list[QueryResult] = Field(default_factory=list, description="Query results")
    total_results: int = Field(..., description="Total number of results found")
    results_returned: int = Field(..., description="Number of results returned")

    # Query metadata
    explanation: QueryExplanation | None = Field(None, description="Query explanation")
    query_confidence: float = Field(..., description="Confidence in query interpretation")
    processing_time_ms: int = Field(..., description="Query processing time in milliseconds")

    # Temporal context
    query_timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC), description="When query was executed")
    temporal_range: dict[str, datetime] | None = Field(None, description="Temporal range searched")

    @property
    def has_results(self) -> bool:
        """Check if query returned any results."""
        return len(self.results) > 0

    @property
    def high_confidence_results(self) -> list[QueryResult]:
        """Get only high confidence results."""
        return [r for r in self.results if r.confidence_level == ConfidenceLevel.HIGH]

    @property
    def average_confidence(self) -> float:
        """Calculate average confidence of all results."""
        if not self.results:
            return 0.0
        return sum(r.confidence_score for r in self.results) / len(self.results)
