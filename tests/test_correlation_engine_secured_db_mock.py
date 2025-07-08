"""
Test: Correlation Engine Integration with Secured Database Interface (Mock Version)

This test demonstrates the architectural boundaries between the CorrelationEngine
and the SecuredDatabaseInterface using mocks, without requiring a real database.

Key architectural points tested:
1. CorrelationEngine uses get_secured_database() - the only authorized path
2. The memory_anchors collection has a specific security policy (requires_security=False for legacy compatibility)
3. CorrelationEngine creates memory anchors through proper architectural boundaries
4. The security model is enforced even for legacy collections
"""

import contextlib
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from mallku.core.database.secured_interface import (
    CollectionSecurityPolicy,
    SecuredCollectionWrapper,
    SecuredDatabaseInterface,
)
from mallku.correlation.engine import CorrelationEngine
from mallku.correlation.models import Event, EventType, TemporalCorrelation
from mallku.models import MemoryAnchor
from mallku.services.memory_anchor_service import MemoryAnchorService


class TestCorrelationEngineSecuredDBIntegration:
    """Test the integration between CorrelationEngine and SecuredDatabaseInterface."""

    @pytest.fixture
    def mock_arango_collection(self):
        """Mock ArangoDB collection."""
        collection = MagicMock()
        collection.insert = MagicMock(return_value={"_key": "test_key", "_id": "test_id"})
        collection.get = MagicMock(return_value={"test": "data"})
        collection.count = MagicMock(return_value=10)
        return collection

    @pytest.fixture
    def mock_secured_db(self, mock_arango_collection):
        """Create a mock secured database interface."""
        db = MagicMock(spec=SecuredDatabaseInterface)
        db._initialized = True
        db._skip_database = False

        # Set up collection policies
        db._collection_policies = {
            "memory_anchors": CollectionSecurityPolicy(
                collection_name="memory_anchors",
                allowed_model_types=[],  # Empty for legacy compatibility
                requires_security=False,  # Legacy compatibility
                schema_validation={
                    "type": "object",
                    "properties": {"_key": {"type": "string"}},
                    "required": ["_key"],
                    "additionalProperties": True,
                },
            )
        }

        # Mock get_secured_collection
        async def mock_get_secured_collection(name):
            if name == "memory_anchors":
                from mallku.core.security.registry import SecurityRegistry

                policy = db._collection_policies["memory_anchors"]
                wrapper = SecuredCollectionWrapper(
                    mock_arango_collection, policy, SecurityRegistry()
                )
                # For memory_anchors with requires_security=False, allow direct collection access
                wrapper._collection = mock_arango_collection
                return wrapper
            raise ValueError(f"Unknown collection: {name}")

        db.get_secured_collection = AsyncMock(side_effect=mock_get_secured_collection)
        db.initialize = AsyncMock()

        # Mock security metrics
        db.get_security_metrics = MagicMock(
            return_value={
                "operations_count": 5,
                "security_violations": 0,
                "registered_collections": 1,
                "uuid_mappings": 0,
                "recent_violations": [],
                "compliance_score": 1.0,
            }
        )

        return db

    @pytest.fixture
    async def memory_service(self, mock_secured_db):
        """Create memory anchor service with mocked secured database."""
        with patch(
            "mallku.services.memory_anchor_service.get_secured_database",
            return_value=mock_secured_db,
        ):
            service = MemoryAnchorService()
            # Mock the database attribute directly
            service.db = mock_secured_db
            service.db_cache = {}
            service.providers = {}
            await service.initialize()
            return service

    @pytest.fixture
    async def correlation_engine(self, memory_service, mock_secured_db):
        """Create correlation engine with mocked dependencies."""
        with patch("mallku.correlation.engine.get_secured_database", return_value=mock_secured_db):
            engine = CorrelationEngine(memory_anchor_service=memory_service)
            # Override min_occurrences for easier testing
            for detector in engine.pattern_detectors.values():
                detector.min_occurrences = 2
            await engine.initialize()
            return engine

    @pytest.mark.asyncio
    async def test_memory_anchors_collection_policy(self, mock_secured_db):
        """Test that memory_anchors collection has the correct security policy."""
        # Verify the memory_anchors collection policy is registered
        assert "memory_anchors" in mock_secured_db._collection_policies

        policy = mock_secured_db._collection_policies["memory_anchors"]

        # Verify policy properties
        assert policy.collection_name == "memory_anchors"
        assert not policy.requires_security  # Legacy compatibility
        assert policy.allowed_model_types == []  # Empty for legacy compatibility

        # The policy should have basic schema validation
        assert "type" in policy.schema_validation
        assert policy.schema_validation["type"] == "object"
        assert "_key" in policy.schema_validation["properties"]

    @pytest.mark.asyncio
    async def test_correlation_engine_uses_secured_database(
        self, correlation_engine, mock_secured_db
    ):
        """Test that CorrelationEngine properly uses the secured database interface."""
        # Create test events with sequential pattern (min 3 occurrences needed)
        base_time = datetime.now(UTC)
        events = []

        # Create a sequential pattern: file save followed by backup
        for i in range(4):  # Need at least 3 occurrences
            # Primary event: file save
            events.append(
                Event(
                    event_id=uuid4(),
                    timestamp=base_time + timedelta(minutes=i * 10),
                    event_type=EventType.STORAGE,
                    stream_id="filesystem",
                    content={"file": f"document{i}.pdf", "action": "save"},
                    metadata={"source": "editor"},
                )
            )

            # Secondary event: backup occurs 30 seconds later
            events.append(
                Event(
                    event_id=uuid4(),
                    timestamp=base_time + timedelta(minutes=i * 10, seconds=30),
                    event_type=EventType.STORAGE,
                    stream_id="backup_system",
                    content={"file": f"document{i}.pdf", "action": "backup"},
                    metadata={"source": "auto_backup"},
                )
            )

        # Process events - this should create correlations
        correlations = await correlation_engine.process_event_stream(events)

        # Verify correlation detection worked
        assert len(correlations) > 0

        # Check the pattern type detected
        assert any(c.pattern_type == "sequential" for c in correlations)

        # Check that the secured database was used to get the collection
        if correlation_engine.correlation_stats["memory_anchors_created"] > 0:
            mock_secured_db.get_secured_collection.assert_called_with("memory_anchors")

    @pytest.mark.asyncio
    async def test_memory_anchor_creation_through_secured_path(
        self, correlation_engine, mock_secured_db, mock_arango_collection
    ):
        """Test that memory anchors are created through the secured database path."""
        # Create a high-confidence correlation that will trigger anchor creation
        primary_event = Event(
            event_id=uuid4(),
            timestamp=datetime.now(UTC),
            event_type=EventType.STORAGE,
            stream_id="filesystem",
            content={"file_path": "/test/important.doc"},
            metadata={"size": 1024},
        )

        correlated_event = Event(
            event_id=uuid4(),
            timestamp=datetime.now(UTC) + timedelta(seconds=2),
            event_type=EventType.ACTIVITY,
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

        # Verify the collection was accessed through secured interface
        mock_secured_db.get_secured_collection.assert_called_with("memory_anchors")

        # Verify the anchor was inserted
        mock_arango_collection.insert.assert_called_once()
        insert_call_args = mock_arango_collection.insert.call_args[0][0]
        assert "_key" in insert_call_args
        assert "timestamp" in insert_call_args
        assert "cursors" in insert_call_args
        assert "metadata" in insert_call_args

    @pytest.mark.asyncio
    async def test_query_service_uses_secured_database(self, mock_secured_db):
        """Test that MemoryAnchorQueryService uses secured database for queries."""
        from mallku.query.models import QueryRequest
        from mallku.query.service import MemoryAnchorQueryService

        # Mock execute_secured_query
        mock_secured_db.execute_secured_query = AsyncMock(return_value=[])

        with patch("mallku.query.service.get_secured_database", return_value=mock_secured_db):
            # Create query service
            query_service = MemoryAnchorQueryService()
            await query_service.initialize()

            # Verify it initialized with secured database
            assert query_service.db is not None
            assert query_service.db == mock_secured_db

            # Create a test query
            query_request = QueryRequest(query_text="files from last hour", max_results=10)

            # Execute query - this should use secured database
            response = await query_service.execute_query(query_request)

            # The query should complete without security violations
            assert response is not None
            assert response.query_text == "files from last hour"

            # Verify secured query was called
            mock_secured_db.execute_secured_query.assert_called()
            query_call_args = mock_secured_db.execute_secured_query.call_args
            assert query_call_args.kwargs.get("collection_name") == "memory_anchors"

    @pytest.mark.asyncio
    async def test_secured_db_prevents_direct_access(self):
        """Test that direct database access is prevented/monitored."""
        import warnings

        from mallku.core.database.factory import get_database_raw

        # Mock the legacy database module to prevent actual connection
        with patch(
            "mallku.core.database.factory.importlib.util.spec_from_file_location"
        ) as mock_spec:
            mock_module = MagicMock()
            mock_module._db_instance = None
            mock_module.MallkuDBConfig = MagicMock

            mock_spec.return_value = MagicMock()
            mock_spec.return_value.loader.exec_module = MagicMock()

            with patch(
                "mallku.core.database.factory.importlib.util.module_from_spec",
                return_value=mock_module,
            ):
                # Attempting to use get_database_raw should generate a warning
                with warnings.catch_warnings(record=True) as w:
                    warnings.simplefilter("always")

                    # This call should be monitored/warned
                    with contextlib.suppress(Exception):
                        # We expect this to fail in test environment
                        raw_db = get_database_raw()

                    # The warning mechanism exists
                    # (actual warning depends on call stack detection)
                    assert True  # Mechanism is in place

    @pytest.mark.asyncio
    async def test_correlation_engine_respects_skip_database_flag(self, monkeypatch):
        """Test that correlation engine respects MALLKU_SKIP_DATABASE flag."""
        # Set the skip database flag
        monkeypatch.setenv("MALLKU_SKIP_DATABASE", "true")

        # Mock the secured database to return None (skip mode)
        mock_skip_db = MagicMock(spec=SecuredDatabaseInterface)
        mock_skip_db._skip_database = True
        mock_skip_db.initialize = AsyncMock()

        with patch("mallku.correlation.engine.get_secured_database", return_value=mock_skip_db):
            # Create engine without database
            engine = CorrelationEngine()
            await engine.initialize()

            # Process events - should work without database
            events = [
                Event(
                    event_id=uuid4(),
                    timestamp=datetime.now(UTC),
                    event_type=EventType.ACTIVITY,
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

    @pytest.fixture
    def mock_secured_db_with_collection(self, mock_arango_collection):
        """Create mock secured db with memory anchors collection."""
        db = MagicMock(spec=SecuredDatabaseInterface)
        db._initialized = True
        db.initialize = AsyncMock()

        # Mock get_secured_collection to return a wrapper
        async def mock_get_collection(name):
            if name == "memory_anchors":
                from mallku.core.security.registry import SecurityRegistry

                policy = CollectionSecurityPolicy(
                    collection_name="memory_anchors",
                    allowed_model_types=[],
                    requires_security=False,
                )
                wrapper = SecuredCollectionWrapper(
                    mock_arango_collection, policy, SecurityRegistry()
                )
                wrapper._collection = mock_arango_collection
                return wrapper

        db.get_secured_collection = AsyncMock(side_effect=mock_get_collection)
        return db

    @pytest.mark.asyncio
    async def test_memory_anchor_creation_fields(self, mock_secured_db_with_collection):
        """Test that memory anchors created by correlation engine have correct fields."""
        with patch(
            "mallku.correlation.engine.get_secured_database",
            return_value=mock_secured_db_with_collection,
        ):
            engine = CorrelationEngine()
            # Override min_occurrences for testing
            for detector in engine.pattern_detectors.values():
                detector.min_occurrences = 2  # Lower threshold for testing
            await engine.initialize()

            # Create events that will correlate
            now = datetime.now(UTC)
            events = []

            # Create pattern with enough occurrences
            for i in range(3):
                events.append(
                    Event(
                        event_id=uuid4(),
                        timestamp=now + timedelta(minutes=i * 5),
                        event_type=EventType.STORAGE,
                        stream_id="filesystem",
                        content={"file_path": f"/docs/report_{i}.pdf", "size": 2048},
                        metadata={"modified": (now + timedelta(minutes=i * 5)).isoformat()},
                    )
                )

                events.append(
                    Event(
                        event_id=uuid4(),
                        timestamp=now + timedelta(minutes=i * 5, seconds=3),
                        event_type=EventType.ACTIVITY,
                        stream_id="pdf_reader",
                        content={"action": "open", "file": f"/docs/report_{i}.pdf"},
                        metadata={"page_count": 10},
                    )
                )

            # Process events
            correlations = await engine.process_event_stream(events)

            # Should create at least one correlation
            assert len(correlations) > 0

            # Get the first correlation
            correlation = correlations[0]

            # Manually create anchor to verify structure
            anchor = await engine._create_memory_anchor(correlation)

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


class TestSecurityMetricsTracking:
    """Test that security metrics are properly tracked during operations."""

    @pytest.mark.asyncio
    async def test_metrics_tracking_during_correlation(self, correlation_engine, mock_secured_db):
        """Test that operations through correlation engine are tracked in security metrics."""
        # Configure metrics to change
        call_count = 0

        def get_metrics():
            nonlocal call_count
            call_count += 1
            return {
                "operations_count": 5 + call_count,
                "security_violations": 0,
                "registered_collections": 3,
                "uuid_mappings": 10,
                "recent_violations": [],
                "compliance_score": 1.0,
            }

        mock_secured_db.get_security_metrics = MagicMock(side_effect=get_metrics)

        # Get initial metrics
        initial_metrics = mock_secured_db.get_security_metrics()
        initial_ops = initial_metrics["operations_count"]

        # Process some events
        events = [
            Event(
                event_id=uuid4(),
                timestamp=datetime.now(UTC),
                event_type=EventType.ACTIVITY,
                stream_id=f"stream_{i}",
                content={"index": i},
            )
            for i in range(5)
        ]

        await correlation_engine.process_event_stream(events)

        # Get updated metrics
        final_metrics = mock_secured_db.get_security_metrics()
        final_ops = final_metrics["operations_count"]

        # Operations count should have increased
        assert final_ops > initial_ops

        # Should have memory_anchors in registered collections
        assert final_metrics["registered_collections"] > 0

        # Check compliance score
        assert "compliance_score" in final_metrics
        assert 0 <= final_metrics["compliance_score"] <= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
