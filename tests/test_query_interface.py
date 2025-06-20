#!/usr/bin/env python3
"""
Test suite for Memory Anchor Query Interface - the final component of the Discovery Trail.

This test validates that natural language queries are correctly parsed and executed
against memory anchor data, demonstrating the complete journey from file operations
to contextual search results.
"""

import asyncio
import contextlib
import logging
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import uuid4

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from mallku.core.database import get_database
from mallku.models import MemoryAnchor
from mallku.query import (
    ContextualQuery,
    MemoryAnchorQueryService,
    PatternQuery,
    QueryRequest,
    QueryType,
    TemporalQuery,
)
from mallku.query.parser import QueryParser


class QueryInterfaceTests:
    """Test suite for memory anchor query interface."""

    def __init__(self):
        self.db = None
        self.query_service: MemoryAnchorQueryService = None
        self.parser: QueryParser = None
        self.test_anchors: list[MemoryAnchor] = []

    async def run_all_tests(self):
        """Execute complete test suite."""
        print("Memory Anchor Query Interface Test Suite")
        print("=" * 60)

        # Set up logging
        logging.basicConfig(level=logging.INFO)

        tests = [
            self.test_setup_test_environment,
            self.test_service_initialization,
            self.test_query_parser_temporal,
            self.test_query_parser_pattern,
            self.test_query_parser_contextual,
            self.test_temporal_query_execution,
            self.test_pattern_query_execution,
            self.test_contextual_query_execution,
            self.test_query_result_ranking,
            self.test_query_explanation_generation,
            self.test_natural_language_queries,
            self.test_anchor_context_traversal,
            self.cleanup_test_environment,
        ]

        passed = 0
        total = len(tests)

        for test in tests:
            try:
                print(f"\\n{test.__name__.replace('_', ' ').title()}...")
                result = await test()
                if result:
                    print("   ✓ Passed")
                    passed += 1
                else:
                    print("   ✗ Failed")
            except Exception as e:
                print(f"   ✗ Exception: {e}")

        print(f"\\n{'=' * 60}")
        print(f"Results: {passed}/{total} tests passed")

        if passed == total:
            print("🎉 All tests passed! Memory Anchor Query Interface is working perfectly.")
            print("🚀 The Memory Anchor Discovery Trail is now complete!")
            return 0
        else:
            print("❌ Some tests failed. The query interface needs refinement.")
            return 1

    async def test_setup_test_environment(self) -> bool:
        """Set up test environment with sample memory anchors."""
        try:
            # Initialize database connection
            self.db = get_database()

            # Create test collection if it doesn't exist
            with contextlib.suppress(Exception):
                self.db.create_collection("memory_anchors")

            # Create sample memory anchors with file data
            await self._create_sample_anchors()

            print(f"   Created {len(self.test_anchors)} test memory anchors")
            return True

        except Exception as e:
            print(f"   Setup failed: {e}")
            return False

    async def test_service_initialization(self) -> bool:
        """Test query service initialization."""
        try:
            self.query_service = MemoryAnchorQueryService()
            await self.query_service.initialize()

            self.parser = QueryParser()

            assert self.query_service.db is not None
            assert self.parser is not None

            print("   Query service and parser initialized successfully")
            return True

        except Exception as e:
            print(f"   Service initialization failed: {e}")
            return False

    async def test_query_parser_temporal(self) -> bool:
        """Test temporal query parsing."""
        try:
            test_queries = [
                "files from yesterday afternoon",
                "documents edited 2 hours ago",
                "files from last Tuesday",
                "work from this morning",
            ]

            for query_text in test_queries:
                request = QueryRequest(query_text=query_text)
                parsed = self.parser.parse_query(request)

                assert parsed["query_type"] == QueryType.TEMPORAL
                assert "temporal_query" in parsed
                assert parsed["confidence"] > 0.5

                temporal_query = parsed["temporal_query"]
                assert isinstance(temporal_query, TemporalQuery)

            print(f"   Successfully parsed {len(test_queries)} temporal queries")
            return True

        except Exception as e:
            print(f"   Temporal parsing failed: {e}")
            return False

    async def test_query_parser_pattern(self) -> bool:
        """Test pattern query parsing."""
        try:
            test_queries = [
                "files I typically edit after meetings",
                "documents I usually work on in the morning",
                "code I often modify during standup",
                "files I always check before presentations",
            ]

            for query_text in test_queries:
                request = QueryRequest(query_text=query_text)
                parsed = self.parser.parse_query(request)

                assert parsed["query_type"] == QueryType.PATTERN
                assert "pattern_query" in parsed
                assert parsed["confidence"] > 0.5

                pattern_query = parsed["pattern_query"]
                assert isinstance(pattern_query, PatternQuery)

            print(f"   Successfully parsed {len(test_queries)} pattern queries")
            return True

        except Exception as e:
            print(f"   Pattern parsing failed: {e}")
            return False

    async def test_query_parser_contextual(self) -> bool:
        """Test contextual query parsing."""
        try:
            test_queries = [
                "files related to project Alpha",
                "documents similar to report.pdf",
                "files associated with client presentation",
                "content connected to development work",
            ]

            for query_text in test_queries:
                request = QueryRequest(query_text=query_text)
                parsed = self.parser.parse_query(request)

                assert parsed["query_type"] == QueryType.CONTEXTUAL
                assert "contextual_query" in parsed
                assert parsed["confidence"] > 0.5

                contextual_query = parsed["contextual_query"]
                assert isinstance(contextual_query, ContextualQuery)

            print(f"   Successfully parsed {len(test_queries)} contextual queries")
            return True

        except Exception as e:
            print(f"   Contextual parsing failed: {e}")
            return False

    async def test_temporal_query_execution(self) -> bool:
        """Test execution of temporal queries."""
        try:
            # Query for files from today
            request = QueryRequest(
                query_text="files from today", max_results=10, min_confidence=0.1
            )

            response = await self.query_service.execute_query(request)

            assert response.query_type == QueryType.TEMPORAL
            assert response.processing_time_ms > 0
            assert response.query_confidence > 0.0

            if response.has_results:
                assert len(response.results) <= request.max_results
                assert all(r.confidence_score >= request.min_confidence for r in response.results)

                # Check temporal results have proper structure
                for result in response.results:
                    assert result.anchor_id is not None
                    assert result.anchor_timestamp is not None
                    assert result.file_path
                    assert "temporal" in result.correlation_tags

            print(f"   Temporal query returned {response.results_returned} results")
            return True

        except Exception as e:
            print(f"   Temporal query execution failed: {e}")
            return False

    async def test_pattern_query_execution(self) -> bool:
        """Test execution of pattern-based queries."""
        try:
            # Query for behavioral patterns
            request = QueryRequest(
                query_text="files I typically work on during development",
                max_results=10,
                min_confidence=0.1,
            )

            response = await self.query_service.execute_query(request)

            assert response.query_type == QueryType.PATTERN
            assert response.processing_time_ms > 0

            if response.has_results:
                # Check pattern results have proper structure
                for result in response.results:
                    assert result.anchor_id is not None
                    assert result.correlation_type == "behavioral_pattern"
                    assert "pattern" in result.correlation_tags

                    # Should have pattern frequency data
                    if "pattern_frequency" in result.context:
                        assert result.context["pattern_frequency"] >= 1

            print(f"   Pattern query returned {response.results_returned} results")
            return True

        except Exception as e:
            print(f"   Pattern query execution failed: {e}")
            return False

    async def test_contextual_query_execution(self) -> bool:
        """Test execution of contextual queries."""
        try:
            # Query for contextual relationships
            request = QueryRequest(
                query_text="files related to project work", max_results=10, min_confidence=0.1
            )

            response = await self.query_service.execute_query(request)

            assert response.query_type == QueryType.CONTEXTUAL
            assert response.processing_time_ms > 0

            if response.has_results:
                # Check contextual results have proper structure
                for result in response.results:
                    assert result.anchor_id is not None
                    assert result.correlation_type == "contextual_similarity"
                    assert "contextual" in result.correlation_tags

                    # Should have similarity score
                    if "similarity_score" in result.context:
                        assert 0.0 <= result.context["similarity_score"] <= 1.0

            print(f"   Contextual query returned {response.results_returned} results")
            return True

        except Exception as e:
            print(f"   Contextual query execution failed: {e}")
            return False

    async def test_query_result_ranking(self) -> bool:
        """Test query result ranking and filtering."""
        try:
            # Query with different confidence thresholds
            low_confidence_request = QueryRequest(
                query_text="files from today", min_confidence=0.1, max_results=20
            )

            high_confidence_request = QueryRequest(
                query_text="files from today", min_confidence=0.8, max_results=20
            )

            low_response = await self.query_service.execute_query(low_confidence_request)
            high_response = await self.query_service.execute_query(high_confidence_request)

            # High confidence should return fewer or equal results
            assert high_response.results_returned <= low_response.results_returned

            # Check ranking - results should be sorted by confidence (descending)
            if len(low_response.results) > 1:
                for i in range(len(low_response.results) - 1):
                    current_score = low_response.results[i].confidence_score
                    next_score = low_response.results[i + 1].confidence_score
                    assert current_score >= next_score, "Results not properly ranked by confidence"

            print(
                f"   Ranking: {low_response.results_returned} low conf, {high_response.results_returned} high conf"
            )
            return True

        except Exception as e:
            print(f"   Result ranking test failed: {e}")
            return False

    async def test_query_explanation_generation(self) -> bool:
        """Test query explanation generation."""
        try:
            request = QueryRequest(
                query_text="documents from yesterday afternoon", include_explanations=True
            )

            response = await self.query_service.execute_query(request)

            assert response.explanation is not None
            assert response.explanation.query_interpretation
            assert response.explanation.search_strategy
            assert len(response.explanation.filters_applied) > 0
            assert response.explanation.anchors_searched >= 0
            assert response.explanation.correlations_found >= 0
            assert len(response.explanation.ranking_factors) > 0

            print(f"   Explanation: {response.explanation.search_strategy}")
            return True

        except Exception as e:
            print(f"   Explanation generation failed: {e}")
            return False

    async def test_natural_language_queries(self) -> bool:
        """Test various natural language query formats."""
        try:
            test_queries = [
                "show me files from last Tuesday morning",
                "what documents did I edit after the team meeting",
                "find files related to the client presentation",
                "documents I typically work on during afternoon sessions",
                "files similar to project_plan.md from this week",
            ]

            successful_queries = 0

            for query_text in test_queries:
                try:
                    request = QueryRequest(query_text=query_text, min_confidence=0.1)
                    response = await self.query_service.execute_query(request)

                    assert response.query_confidence > 0.0
                    assert response.processing_time_ms > 0
                    assert response.query_type in [
                        QueryType.TEMPORAL,
                        QueryType.PATTERN,
                        QueryType.CONTEXTUAL,
                    ]

                    successful_queries += 1

                except Exception as e:
                    print(f"     Query failed: '{query_text}' - {e}")

            success_rate = successful_queries / len(test_queries)
            assert success_rate >= 0.8, f"Success rate too low: {success_rate:.2f}"

            print(
                f"   Successfully processed {successful_queries}/{len(test_queries)} natural language queries"
            )
            return True

        except Exception as e:
            print(f"   Natural language query test failed: {e}")
            return False

    async def test_anchor_context_traversal(self) -> bool:
        """Test memory anchor context and lineage traversal."""
        try:
            if not self.test_anchors:
                print("   No test anchors available for traversal")
                return True

            # Test getting context for a specific anchor
            anchor_id = self.test_anchors[0].anchor_id
            context = await self.query_service.get_anchor_context(anchor_id)

            assert "anchor" in context
            assert context["anchor"]["_key"] == str(anchor_id)

            # Context may include predecessor/successor information
            if "predecessor" in context:
                assert context["predecessor"] is None or isinstance(context["predecessor"], dict)
            if "successors" in context:
                assert isinstance(context["successors"], list)

            print(f"   Successfully retrieved context for anchor {anchor_id}")
            return True

        except Exception as e:
            print(f"   Anchor context traversal failed: {e}")
            return False

    async def cleanup_test_environment(self) -> bool:
        """Clean up test environment."""
        try:
            # Clean up test anchors
            if self.test_anchors and self.db:
                for anchor in self.test_anchors:
                    with contextlib.suppress(Exception):
                        self.db.collection("memory_anchors").delete(str(anchor.anchor_id))

            # Shutdown services
            if self.query_service:
                await self.query_service.shutdown()

            print(f"   Cleaned up {len(self.test_anchors)} test anchors")
            return True

        except Exception as e:
            print(f"   Cleanup failed: {e}")
            return False

    async def _create_sample_anchors(self):
        """Create sample memory anchors for testing."""
        base_time = datetime.now(UTC)

        # Sample file data for different scenarios
        sample_files = [
            {
                "file_path": "/Users/test/Documents/project_plan.md",
                "file_name": "project_plan.md",
                "file_extension": ".md",
                "file_category": "document",
                "file_size": 2048,
                "mime_type": "text/markdown",
                "last_modified": (base_time - timedelta(hours=2)).isoformat(),
            },
            {
                "file_path": "/Users/test/Code/main.py",
                "file_name": "main.py",
                "file_extension": ".py",
                "file_category": "code",
                "file_size": 4096,
                "mime_type": "text/x-python",
                "last_modified": (base_time - timedelta(hours=1)).isoformat(),
            },
            {
                "file_path": "/Users/test/Documents/meeting_notes.txt",
                "file_name": "meeting_notes.txt",
                "file_extension": ".txt",
                "file_category": "document",
                "file_size": 1024,
                "mime_type": "text/plain",
                "last_modified": (base_time - timedelta(hours=3)).isoformat(),
            },
        ]

        # Create anchors with temporal distribution
        for i, file_data in enumerate(sample_files):
            anchor_time = base_time - timedelta(hours=i, minutes=i * 15)

            anchor = MemoryAnchor(
                anchor_id=uuid4(),
                timestamp=anchor_time,
                cursors={"temporal": anchor_time.isoformat(), "filesystem": file_data},
                metadata={
                    "providers": ["filesystem"],
                    "creation_trigger": "file_activity",
                    "confidence": 0.8 + (i * 0.05),
                },
            )

            # Store in database
            anchor_doc = anchor.to_arangodb_document()
            self.db.collection("memory_anchors").insert(anchor_doc)

            self.test_anchors.append(anchor)


async def main():
    """Run the query interface test suite."""
    test_suite = QueryInterfaceTests()
    return await test_suite.run_all_tests()


if __name__ == "__main__":
    import sys

    sys.exit(asyncio.run(main()))
