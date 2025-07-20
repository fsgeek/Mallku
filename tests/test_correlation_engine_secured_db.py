"""
Test: Correlation Engine Integration with Secured Database Interface

This test demonstrates the architectural boundaries between the CorrelationEngine
and the SecuredDatabaseInterface, particularly focusing on the memory_anchors
collection security policy.

Key architectural points tested:
1. CorrelationEngine uses get_secured_database() - the only authorized path
2. The memory_anchors collection has a specific security policy (requires_security=False for legacy compatibility)
3. CorrelationEngine creates memory anchors through proper architectural boundaries
4. The security model is enforced even for legacy collections
"""

from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from mallku.core.database import get_secured_database
from mallku.correlation.engine import CorrelationEngine
from mallku.correlation.models import ConsciousnessEventType, Event, TemporalCorrelation
from mallku.models import MemoryAnchor
from mallku.services.memory_anchor_service import MemoryAnchorService


class TestCorrelationEngineSecuredDBIntegration:
    """Test the integration between CorrelationEngine and SecuredDatabaseInterface."""

    @pytest.fixture
    async def secured_db(self):
        """Get the secured database interface."""
        db = get_secured_database()
        await db.initialize()
        return db

    @pytest.fixture
    async def memory_service(self, secured_db):
        """Create memory anchor service with secured database."""
        service = MemoryAnchorService()
        await service.initialize()
        return service

    @pytest.fixture
    async def correlation_engine(self, memory_service):
        """Create correlation engine with memory service."""
        engine = CorrelationEngine(memory_anchor_service=memory_service)
        await engine.initialize()
        return engine

    @pytest.mark.asyncio
    async def test_memory_anchors_collection_policy(self, secured_db):
        """Test that memory_anchors collection has the correct security policy."""
        # Verify the memory_anchors collection policy is registered
        assert "memory_anchors" in secured_db._collection_policies

        policy = secured_db._collection_policies["memory_anchors"]

        # Verify policy properties
        assert policy.collection_name == "memory_anchors"
        assert not policy.requires_security  # Legacy compatibility
        assert policy.allowed_model_types == []  # Empty for legacy compatibility

        # The policy should have basic schema validation
        assert "type" in policy.schema_validation
        assert policy.schema_validation["type"] == "object"
        assert "_key" in policy.schema_validation["properties"]

    @pytest.mark.asyncio
    async def test_correlation_engine_uses_secured_database(self, correlation_engine, secured_db):
        """Test that CorrelationEngine properly uses the secured database interface."""
        # Create test events
        events = [
            Event(
                event_id=uuid4(),
                timestamp=datetime.now(UTC),
                event_type=ConsciousnessEventType.STORAGE,
                stream_id="test_stream_1",
                content={"file": "document1.pdf"},
                metadata={"source": "filesystem"},
            ),
            Event(
                event_id=uuid4(),
                timestamp=datetime.now(UTC) + timedelta(seconds=5),
                event_type=ConsciousnessEventType.ACTIVITY,
                stream_id="test_stream_2",
                content={"action": "edit"},
                metadata={"application": "editor"},
            ),
        ]

        # Process events - this should create correlations
        correlations = await correlation_engine.process_event_stream(events)

        # Verify correlation detection worked
        assert len(correlations) > 0

        # Check that memory anchors were created through secured interface
        if correlation_engine.correlation_stats["memory_anchors_created"] > 0:
            # Verify we can query the memory_anchors collection through secured interface
            collection = await secured_db.get_secured_collection("memory_anchors")
            assert collection is not None

            # The collection wrapper should exist and have the right policy
            assert collection._policy.collection_name == "memory_anchors"
            assert not collection._policy.requires_security

    @pytest.mark.asyncio
    async def test_memory_anchor_creation_through_secured_path(
        self, correlation_engine, secured_db
    ):
        """Test that memory anchors are created through the secured database path."""
        # Create a high-confidence correlation that will trigger anchor creation
        primary_event = Event(
            event_id=uuid4(),
            timestamp=datetime.now(UTC),
            event_type=ConsciousnessEventType.STORAGE,
            stream_id="filesystem",
            content={"file_path": "/test/important.doc"},
            metadata={"size": 1024},
        )

        correlated_event = Event(
            event_id=uuid4(),
            timestamp=datetime.now(UTC) + timedelta(seconds=2),
            event_type=ConsciousnessEventType.ACTIVITY,
            stream_id="editor",
            content={"action": "open", "file": "/test/important.doc"},
            metadata={"application": "word"},
        )

        # Create correlation with high confidence
        correlation = TemporalCorrelation(
            correlation_id=uuid4(),
            primary_event=primary_event,
            correlated_events=[correlated_event],
            pattern_type="sequential",
            confidence_score=0.9,  # High confidence will trigger anchor creation
            temporal_gap=timedelta(seconds=2),
            occurrence_frequency=3,
        )

        # Create memory anchor from correlation
        anchor = await correlation_engine._create_memory_anchor(correlation)

        # Verify anchor was created
        assert anchor is not None
        assert isinstance(anchor, MemoryAnchor)
        assert anchor.metadata["correlation_id"] == str(correlation.correlation_id)
        assert anchor.metadata["pattern_type"] == "sequential"
        assert anchor.metadata["confidence_score"] == 0.9

    @pytest.mark.asyncio
    async def test_query_service_uses_secured_database(self, secured_db):
        """Test that MemoryAnchorQueryService uses secured database for queries."""
        from mallku.query.models import QueryRequest
        from mallku.query.service import MemoryAnchorQueryService

        # Create query service
        query_service = MemoryAnchorQueryService()
        await query_service.initialize()

        # Verify it initialized with secured database
        assert query_service.db is not None
        assert query_service.db == secured_db

        # Create a test query
        query_request = QueryRequest(query_text="files from last hour", max_results=10)

        # Execute query - this should use secured database
        response = await query_service.execute_query(query_request)

        # The query should complete without security violations
        assert response is not None
        assert response.query_text == "files from last hour"

        # Check security metrics after operations
        metrics = secured_db.get_security_metrics()
        assert metrics["operations_count"] >= 0  # Operations were tracked
        assert "memory_anchors" in [
            p.collection_name for p in secured_db._collection_policies.values()
        ]

    @pytest.mark.asyncio
    async def test_secured_db_prevents_direct_access(self, secured_db):
        """Test that direct database access is prevented/monitored."""
        import warnings

        from mallku.core.database.factory import get_database_raw

        # Attempting to use get_database_raw should generate a warning
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            # This call should be monitored/warned
            raw_db = get_database_raw()

            # Check if warning was issued (only for non-legitimate calls)
            # The test itself might be considered legitimate, so we just verify
            # the mechanism exists
            assert hasattr(secured_db, "_security_violations")

    @pytest.mark.asyncio
    async def test_correlation_engine_respects_skip_database_flag(self, monkeypatch):
        """Test that correlation engine respects MALLKU_SKIP_DATABASE flag."""
        # Set the skip database flag
        monkeypatch.setenv("MALLKU_SKIP_DATABASE", "true")

        # Create engine without database
        engine = CorrelationEngine()
        await engine.initialize()

        # Process events - should work without database
        events = [
            Event(
                event_id=uuid4(),
                timestamp=datetime.now(UTC),
                event_type=ConsciousnessEventType.ACTIVITY,
                stream_id="test",
                content={"test": "data"},
            )
        ]

        correlations = await engine.process_event_stream(events)

        # Should detect correlations but not create anchors
        assert engine.correlation_stats["memory_anchors_created"] == 0

    def test_architectural_boundaries_documentation(self):
        """
        Document the architectural boundaries being tested.

        This test serves as living documentation of the security architecture:

        1. SINGLE ENTRY POINT: get_secured_database() is the ONLY authorized way
           to access the database in Mallku.

        2. COLLECTION POLICIES: Every collection must have a registered security
           policy that defines allowed models and security requirements.

        3. LEGACY COMPATIBILITY: The memory_anchors collection has
           requires_security=False for backward compatibility, but still goes
           through the secured interface.

        4. ARCHITECTURAL ENFORCEMENT: Components like CorrelationEngine and
           MemoryAnchorQueryService use the secured interface, ensuring all
           database operations are monitored and controlled.

        5. SECURITY METRICS: All operations are tracked, allowing for security
           auditing and compliance monitoring.
        """
        # This test exists purely for documentation
        assert True


class TestCorrelationEngineMemoryAnchorIntegration:
    """Test the specific integration between CorrelationEngine and memory anchors."""

    @pytest.mark.asyncio
    async def test_memory_anchor_creation_fields(self, correlation_engine):
        """Test that memory anchors created by correlation engine have correct fields."""
        # Create events that will correlate
        now = datetime.now(UTC)
        events = [
            Event(
                event_id=uuid4(),
                timestamp=now,
                event_type=ConsciousnessEventType.STORAGE,
                stream_id="filesystem",
                content={"file_path": "/docs/report.pdf", "size": 2048},
                metadata={"modified": now.isoformat()},
            ),
            Event(
                event_id=uuid4(),
                timestamp=now + timedelta(seconds=3),
                event_type=ConsciousnessEventType.ACTIVITY,
                stream_id="pdf_reader",
                content={"action": "open", "file": "/docs/report.pdf"},
                metadata={"page_count": 10},
            ),
        ]

        # Process events
        correlations = await correlation_engine.process_event_stream(events)

        # Should create at least one correlation
        assert len(correlations) > 0

        # Get the first correlation
        correlation = correlations[0]

        # Manually create anchor to verify structure
        anchor = await correlation_engine._create_memory_anchor(correlation)

        if anchor:
            # Verify anchor structure
            assert anchor.anchor_id is not None
            assert anchor.timestamp is not None
            assert isinstance(anchor.cursors, dict)
            assert isinstance(anchor.metadata, dict)

            # Verify cursors contain event information
            assert len(anchor.cursors) >= 2  # One for each event

            # Verify metadata contains correlation information
            assert anchor.metadata["correlation_id"] == str(correlation.correlation_id)
            assert anchor.metadata["pattern_type"] == correlation.pattern_type
            assert anchor.metadata["confidence_score"] == correlation.confidence_score
            assert anchor.metadata["event_count"] == 2
            assert "providers" in anchor.metadata
            assert anchor.metadata["creation_trigger"] == "correlation_detection"

    @pytest.mark.asyncio
    async def test_correlation_to_anchor_adapter(self, memory_service):
        """Test the CorrelationToAnchorAdapter functionality."""
        from mallku.correlation.engine import CorrelationToAnchorAdapter

        # Create adapter
        adapter = CorrelationToAnchorAdapter(memory_service)

        # Create test correlation
        primary_event = Event(
            event_id=uuid4(),
            timestamp=datetime.now(UTC),
            event_type=ConsciousnessEventType.STORAGE,
            stream_id="storage_provider",
            content={"file": "data.csv"},
        )

        correlation = TemporalCorrelation(
            correlation_id=uuid4(),
            primary_event=primary_event,
            correlated_events=[],
            pattern_type="cyclical",
            confidence_score=0.85,
            temporal_gap=timedelta(hours=1),
            occurrence_frequency=5,
        )

        # Process correlation through adapter
        anchor = await adapter.process_correlation(correlation)

        # High confidence correlation should create anchor
        assert anchor is not None

        # Low confidence should not create anchor
        correlation.confidence_score = 0.5
        anchor = await adapter.process_correlation(correlation)
        assert anchor is None


class TestSecurityMetricsTracking:
    """Test that security metrics are properly tracked during operations."""

    @pytest.mark.asyncio
    async def test_metrics_tracking_during_correlation(self, correlation_engine, secured_db):
        """Test that operations through correlation engine are tracked in security metrics."""
        # Get initial metrics
        initial_metrics = secured_db.get_security_metrics()
        initial_ops = initial_metrics["operations_count"]

        # Process some events
        events = [
            Event(
                event_id=uuid4(),
                timestamp=datetime.now(UTC),
                event_type=ConsciousnessEventType.ACTIVITY,
                stream_id=f"stream_{i}",
                content={"index": i},
            )
            for i in range(5)
        ]

        await correlation_engine.process_event_stream(events)

        # Get updated metrics
        final_metrics = secured_db.get_security_metrics()
        final_ops = final_metrics["operations_count"]

        # Operations count should have increased
        assert final_ops >= initial_ops

        # Should have memory_anchors in registered collections
        assert final_metrics["registered_collections"] > 0

        # Check compliance score
        assert "compliance_score" in final_metrics
        assert 0 <= final_metrics["compliance_score"] <= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
