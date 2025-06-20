"""
Memory Anchor Query Service

This service executes queries against memory anchors and their associated
correlation data to provide contextual search capabilities.
"""

import logging
import time
from datetime import datetime, timedelta
from typing import Any
from uuid import UUID

from mallku.core.database import get_secured_database

from .models import (
    QueryExplanation,
    QueryRequest,
    QueryResponse,
    QueryResult,
    QueryType,
)
from .parser import QueryParser

logger = logging.getLogger(__name__)


class MemoryAnchorQueryService:
    """
    Service for executing queries against memory anchor data.

    Provides temporal, pattern-based, and contextual search capabilities
    across memory anchors and their associated file correlations.
    """

    def __init__(self):
        self.db = None
        self.parser = QueryParser()

    async def initialize(self):
        """Initialize database connection."""
        self.db = get_secured_database()
        await self.db.initialize()
        logger.info("MemoryAnchorQueryService initialized")

    async def shutdown(self):
        """Clean shutdown of service."""
        self.db = None
        logger.info("MemoryAnchorQueryService shutdown")

    async def execute_query(self, query_request: QueryRequest) -> QueryResponse:
        """
        Execute a query against memory anchor data.

        Args:
            query_request: The query request to execute

        Returns:
            Query response with results and metadata
        """
        start_time = time.time()

        try:
            # Parse the natural language query
            parsed_query = self.parser.parse_query(query_request)
            query_type = parsed_query["query_type"]

            logger.info(f"Executing {query_type} query: {query_request.query_text}")

            # Execute based on query type
            if query_type == QueryType.TEMPORAL:
                results, explanation = await self._execute_temporal_query(
                    parsed_query, query_request
                )
            elif query_type == QueryType.PATTERN:
                results, explanation = await self._execute_pattern_query(
                    parsed_query, query_request
                )
            elif query_type == QueryType.CONTEXTUAL:
                results, explanation = await self._execute_contextual_query(
                    parsed_query, query_request
                )
            else:
                # Default to contextual
                results, explanation = await self._execute_contextual_query(
                    parsed_query, query_request
                )

            # Filter and rank results
            filtered_results = self._filter_results(results, query_request)
            ranked_results = self._rank_results(filtered_results, query_type)

            # Limit results
            final_results = ranked_results[: query_request.max_results]

            processing_time = int((time.time() - start_time) * 1000)

            return QueryResponse(
                query_text=query_request.query_text,
                query_type=query_type,
                results=final_results,
                total_results=len(results),
                results_returned=len(final_results),
                explanation=explanation if query_request.include_explanations else None,
                query_confidence=parsed_query.get("confidence", 0.7),
                processing_time_ms=processing_time,
            )

        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            processing_time = int((time.time() - start_time) * 1000)

            return QueryResponse(
                query_text=query_request.query_text,
                query_type=QueryType.CONTEXTUAL,
                results=[],
                total_results=0,
                results_returned=0,
                query_confidence=0.0,
                processing_time_ms=processing_time,
            )

    async def _execute_temporal_query(
        self, parsed_query: dict[str, Any], request: QueryRequest
    ) -> tuple[list[QueryResult], QueryExplanation]:
        """Execute temporal-based query."""

        temporal_query = parsed_query["temporal_query"]
        results = []

        # Build temporal constraint for ArangoDB query
        temporal_filter = []

        if temporal_query.start_time and temporal_query.end_time:
            temporal_filter.append(f"anchor.timestamp >= '{temporal_query.start_time.isoformat()}'")
            temporal_filter.append(f"anchor.timestamp <= '{temporal_query.end_time.isoformat()}'")
        elif temporal_query.time_window_minutes and request.temporal_context:
            # Use window around reference time
            start_time = request.temporal_context - timedelta(
                minutes=temporal_query.time_window_minutes // 2
            )
            end_time = request.temporal_context + timedelta(
                minutes=temporal_query.time_window_minutes // 2
            )
            temporal_filter.append(f"anchor.timestamp >= '{start_time.isoformat()}'")
            temporal_filter.append(f"anchor.timestamp <= '{end_time.isoformat()}'")

        # Build the AQL query
        filter_clause = f"FILTER {' AND '.join(temporal_filter)}" if temporal_filter else ""
        aql_query = f"""
        FOR anchor IN memory_anchors
            {filter_clause}
            FILTER anchor.cursors.filesystem != null
            SORT anchor.timestamp DESC
            RETURN {{
                anchor_id: anchor._key,
                anchor_timestamp: anchor.timestamp,
                file_info: anchor.cursors.filesystem,
                confidence: 0.8,
                correlation_type: "temporal_proximity"
            }}
        """

        try:
            query_results = await self.db.execute_secured_query(
                aql_query, collection_name="memory_anchors"
            )

            for doc in query_results:
                if isinstance(doc["file_info"], dict) and "file_path" in doc["file_info"]:
                    result = QueryResult.from_memory_anchor_and_file(
                        anchor_id=UUID(doc["anchor_id"]),
                        anchor_timestamp=datetime.fromisoformat(
                            doc["anchor_timestamp"].replace("Z", "+00:00")
                        ),
                        file_info=doc["file_info"],
                        correlation_type=doc["correlation_type"],
                        confidence_score=doc["confidence"],
                        correlation_tags=["temporal", "filesystem"],
                    )
                    results.append(result)

        except Exception as e:
            logger.error(f"Temporal query failed: {e}")

        explanation = QueryExplanation(
            query_interpretation=f"Searching for files within temporal range: {temporal_query.relative_time or 'specified time period'}",
            search_strategy="Temporal proximity matching on memory anchor timestamps",
            filters_applied=["temporal_range", "filesystem_cursors"],
            anchors_searched=len(results),
            correlations_found=len(results),
            ranking_factors=["temporal_proximity", "confidence_score"],
        )

        return results, explanation

    async def _execute_pattern_query(
        self, parsed_query: dict[str, Any], request: QueryRequest
    ) -> tuple[list[QueryResult], QueryExplanation]:
        """Execute pattern-based query."""

        pattern_query = parsed_query["pattern_query"]
        results = []

        # Build pattern matching query
        context_filter = []

        if pattern_query.context_keywords:
            keyword_conditions = []
            for keyword in pattern_query.context_keywords:
                keyword_conditions.append(
                    f'CONTAINS(LOWER(TO_STRING(anchor.metadata)), "{keyword}")'
                )
            context_filter.append(f"({' OR '.join(keyword_conditions)})")

        # Look for recurring patterns in correlation data
        pattern_filter_clause = f"FILTER {' AND '.join(context_filter)}" if context_filter else ""
        aql_query = f"""
        FOR anchor IN memory_anchors
            {pattern_filter_clause}
            COLLECT file_path = anchor.cursors.filesystem.file_path WITH COUNT INTO frequency
            FILTER frequency >= {pattern_query.frequency_threshold}
            FOR anchor2 IN memory_anchors
                FILTER anchor2.cursors.filesystem.file_path == file_path
                SORT anchor2.timestamp DESC
                LIMIT 1
                RETURN {{
                    anchor_id: anchor2._key,
                    anchor_timestamp: anchor2.timestamp,
                    file_info: anchor2.cursors.filesystem,
                    confidence: 0.7 + (frequency * 0.05),
                    correlation_type: "behavioral_pattern",
                    pattern_frequency: frequency
                }}
        """

        try:
            query_results = await self.db.execute_secured_query(
                aql_query, collection_name="memory_anchors"
            )

            for doc in query_results:
                if isinstance(doc["file_info"], dict) and "file_path" in doc["file_info"]:
                    result = QueryResult.from_memory_anchor_and_file(
                        anchor_id=UUID(doc["anchor_id"]),
                        anchor_timestamp=datetime.fromisoformat(
                            doc["anchor_timestamp"].replace("Z", "+00:00")
                        ),
                        file_info=doc["file_info"],
                        correlation_type=doc["correlation_type"],
                        confidence_score=min(1.0, doc["confidence"]),
                        correlation_tags=[
                            "pattern",
                            "behavioral",
                            f"frequency_{doc['pattern_frequency']}",
                        ],
                    )
                    result.context["pattern_frequency"] = doc["pattern_frequency"]
                    results.append(result)

        except Exception as e:
            logger.error(f"Pattern query failed: {e}")

        explanation = QueryExplanation(
            query_interpretation=f"Searching for behavioral patterns with context: {', '.join(pattern_query.context_keywords)}",
            search_strategy="Frequency analysis across memory anchor correlations",
            filters_applied=[
                "context_keywords",
                f"min_frequency_{pattern_query.frequency_threshold}",
            ],
            anchors_searched=len(results),
            correlations_found=len(results),
            ranking_factors=["pattern_frequency", "confidence_score", "recency"],
        )

        return results, explanation

    async def _execute_contextual_query(
        self, parsed_query: dict[str, Any], request: QueryRequest
    ) -> tuple[list[QueryResult], QueryExplanation]:
        """Execute contextual/similarity-based query."""

        contextual_query = parsed_query["contextual_query"]
        context_tags = parsed_query.get("context_tags", [])
        results = []

        # Build contextual matching query
        filters = []

        if context_tags:
            tag_conditions = []
            for tag in context_tags:
                tag_conditions.append(f'CONTAINS(LOWER(TO_STRING(anchor.metadata)), "{tag}")')
            filters.append(f"({' OR '.join(tag_conditions)})")

        if contextual_query.reference_file:
            # Find anchors related to the reference file
            filters.append(
                f'CONTAINS(anchor.cursors.filesystem.file_path, "{contextual_query.reference_file}")'
            )

        # Base query for contextual search
        contextual_filter_clause = f"FILTER {' AND '.join(filters)}" if filters else ""
        aql_query = f"""
        FOR anchor IN memory_anchors
            {contextual_filter_clause}
            FILTER anchor.cursors.filesystem != null
            SORT anchor.timestamp DESC
            LIMIT 100
            RETURN {{
                anchor_id: anchor._key,
                anchor_timestamp: anchor.timestamp,
                file_info: anchor.cursors.filesystem,
                confidence: 0.6,
                correlation_type: "contextual_similarity"
            }}
        """

        try:
            query_results = await self.db.execute_secured_query(
                aql_query, collection_name="memory_anchors"
            )

            for doc in query_results:
                if isinstance(doc["file_info"], dict) and "file_path" in doc["file_info"]:
                    # Calculate contextual similarity score
                    similarity_score = self._calculate_contextual_similarity(
                        doc["file_info"], context_tags, contextual_query.reference_file
                    )

                    if similarity_score >= contextual_query.similarity_threshold:
                        result = QueryResult.from_memory_anchor_and_file(
                            anchor_id=UUID(doc["anchor_id"]),
                            anchor_timestamp=datetime.fromisoformat(
                                doc["anchor_timestamp"].replace("Z", "+00:00")
                            ),
                            file_info=doc["file_info"],
                            correlation_type=doc["correlation_type"],
                            confidence_score=similarity_score,
                            correlation_tags=["contextual"] + context_tags,
                        )
                        result.context["similarity_score"] = similarity_score
                        results.append(result)

        except Exception as e:
            logger.error(f"Contextual query failed: {e}")

        explanation = QueryExplanation(
            query_interpretation=f"Searching for contextually similar files with tags: {', '.join(context_tags)}",
            search_strategy="Contextual similarity matching across memory anchor metadata",
            filters_applied=[
                "context_tags",
                f"similarity_threshold_{contextual_query.similarity_threshold}",
            ],
            anchors_searched=len(results),
            correlations_found=len(results),
            ranking_factors=["contextual_similarity", "recency", "confidence_score"],
        )

        return results, explanation

    def _calculate_contextual_similarity(
        self, file_info: dict[str, Any], context_tags: list[str], reference_file: str | None
    ) -> float:
        """Calculate contextual similarity score for a file."""
        score = 0.5  # Base score

        # File type similarity
        if reference_file and file_info.get("file_extension"):
            ref_ext = reference_file.split(".")[-1] if "." in reference_file else ""
            file_ext = file_info.get("file_extension", "").lstrip(".")
            if ref_ext.lower() == file_ext.lower():
                score += 0.2

        # Context tag matching
        file_path = file_info.get("file_path", "").lower()
        file_category = file_info.get("file_category", "").lower()

        for tag in context_tags:
            if tag.lower() in file_path or tag.lower() in file_category:
                score += 0.1

        # Directory similarity
        if reference_file and file_info.get("file_path"):
            ref_dir = "/".join(reference_file.split("/")[:-1])
            file_dir = "/".join(file_info.get("file_path", "").split("/")[:-1])
            if ref_dir and file_dir and ref_dir in file_dir:
                score += 0.15

        return min(1.0, score)

    def _filter_results(
        self, results: list[QueryResult], request: QueryRequest
    ) -> list[QueryResult]:
        """Filter results based on request criteria."""
        filtered = []

        for result in results:
            # Apply confidence threshold
            if result.confidence_score >= request.min_confidence:
                filtered.append(result)

        return filtered

    def _rank_results(self, results: list[QueryResult], query_type: QueryType) -> list[QueryResult]:
        """Rank results based on query type and relevance factors."""

        def ranking_key(result: QueryResult) -> tuple[float, float]:
            # Primary sort by confidence, secondary by recency
            confidence = result.confidence_score
            recency = result.anchor_timestamp.timestamp() if result.anchor_timestamp else 0

            # Adjust ranking based on query type
            if query_type == QueryType.TEMPORAL:
                # For temporal queries, prioritize exact time matches
                return (-confidence, -recency)
            elif query_type == QueryType.PATTERN:
                # For pattern queries, prioritize frequency and confidence
                frequency = result.context.get("pattern_frequency", 1)
                return (-(confidence + frequency * 0.1), -recency)
            else:
                # For contextual queries, prioritize similarity and confidence
                similarity = result.context.get("similarity_score", confidence)
                return (-(confidence + similarity * 0.2), -recency)

        return sorted(results, key=ranking_key)

    async def get_anchor_context(self, anchor_id: UUID) -> dict[str, Any]:
        """Get detailed context for a specific memory anchor."""

        try:
            # Query for the specific anchor and related data
            aql_query = """
            FOR anchor IN memory_anchors
                FILTER anchor._key == @anchor_id
                RETURN {
                    anchor: anchor,
                    predecessor: (
                        FOR pred IN memory_anchors
                            FILTER pred._key == anchor.predecessor_id
                            RETURN pred
                    )[0],
                    successors: (
                        FOR succ IN memory_anchors
                            FILTER succ.predecessor_id == anchor._key
                            RETURN succ
                    )
                }
            """

            query_results = await self.db.execute_secured_query(
                aql_query, bind_vars={"anchor_id": str(anchor_id)}, collection_name="memory_anchors"
            )

            for doc in query_results:
                return {
                    "anchor": doc["anchor"],
                    "predecessor": doc["predecessor"],
                    "successors": doc["successors"],
                    "lineage_depth": len(doc["successors"]) + (1 if doc["predecessor"] else 0),
                }

        except Exception as e:
            logger.error(f"Failed to get anchor context: {e}")

        return {}
