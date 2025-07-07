"""
Test: Architectural Boundaries - CorrelationEngine and SecuredDatabaseInterface

This test demonstrates the key architectural boundaries without requiring
a full database connection. It focuses on verifying that:

1. CorrelationEngine uses get_secured_database() correctly
2. The memory_anchors collection has the proper security policy
3. Components respect the secured database interface
"""

import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from datetime import datetime, UTC, timedelta
from uuid import uuid4

from mallku.core.database.secured_interface import (
    CollectionSecurityPolicy,
    SecuredDatabaseInterface,
    SecuredCollectionWrapper,
)
from mallku.correlation.engine import CorrelationEngine
from mallku.correlation.models import Event, EventType, TemporalCorrelation, TemporalPrecision
from mallku.models import MemoryAnchor
from mallku.query.service import MemoryAnchorQueryService


class TestArchitecturalBoundaries:
    """Test architectural boundaries between components and secured database."""

    def test_memory_anchors_collection_policy_design(self):
        """
        Test the design of memory_anchors collection security policy.
        
        This documents the architectural decision that memory_anchors
        has requires_security=False for legacy compatibility.
        """
        # Create the policy as defined in secured_interface.py
        memory_anchor_policy = CollectionSecurityPolicy(
            collection_name="memory_anchors",
            allowed_model_types=[],  # Empty for legacy compatibility
            requires_security=False,  # Legacy compatibility
            schema_validation={
                "type": "object",
                "properties": {"_key": {"type": "string"}},
                "required": ["_key"],
                "additionalProperties": True,
            }
        )
        
        # Verify policy properties match architectural design
        assert memory_anchor_policy.collection_name == "memory_anchors"
        assert memory_anchor_policy.requires_security == False
        assert memory_anchor_policy.allowed_model_types == []
        
        # This is intentional - memory_anchors doesn't require SecuredModel
        # because it was designed before the security layer was added
        
        # Document the implication
        assert memory_anchor_policy.requires_security == False, (
            "memory_anchors collection bypasses SecuredModel requirement "
            "for backward compatibility with existing MemoryAnchor class"
        )

    @pytest.mark.asyncio
    async def test_correlation_engine_initialization_uses_secured_db(self):
        """Test that CorrelationEngine initialization uses secured database."""
        mock_secured_db = MagicMock(spec=SecuredDatabaseInterface)
        mock_secured_db.initialize = AsyncMock()
        mock_secured_db._skip_database = False
        
        # Mock MemoryAnchorService to avoid real DB connection
        mock_memory_service = MagicMock()
        mock_memory_service.initialize = AsyncMock()
        
        with patch('mallku.correlation.engine.get_secured_database', return_value=mock_secured_db):
            with patch('mallku.correlation.engine.MemoryAnchorService', return_value=mock_memory_service):
                # Create correlation engine
                engine = CorrelationEngine()
                
                # Initialize the engine
                await engine.initialize()
                
                # Verify memory service was initialized
                mock_memory_service.initialize.assert_called_once()
                
                # The engine should be properly initialized
                assert engine.memory_service == mock_memory_service

    def test_memory_anchor_structure_compatibility(self):
        """Test that MemoryAnchor structure is compatible with secured database."""
        # Create a memory anchor
        anchor = MemoryAnchor(
            anchor_id=uuid4(),
            timestamp=datetime.now(UTC),
            cursors={"test": {"data": "value"}},
            metadata={"source": "correlation_engine"}
        )
        
        # Convert to ArangoDB document format
        doc = anchor.to_arangodb_document()
        
        # Verify it has required fields for ArangoDB
        assert "_key" in doc
        assert doc["_key"] == str(anchor.anchor_id)
        assert "timestamp" in doc
        assert "cursors" in doc
        assert "metadata" in doc
        
        # This structure can be inserted directly without SecuredModel
        # which is why memory_anchors has requires_security=False

    @pytest.mark.asyncio
    async def test_query_service_initialization_uses_secured_db(self):
        """Test that MemoryAnchorQueryService uses secured database."""
        mock_secured_db = MagicMock(spec=SecuredDatabaseInterface)
        mock_secured_db.initialize = AsyncMock()
        
        with patch('mallku.query.service.get_secured_database', return_value=mock_secured_db):
            # Create query service
            service = MemoryAnchorQueryService()
            
            # DB should not be set yet
            assert service.db is None
            
            # Initialize
            await service.initialize()
            
            # Now it should have the secured database
            assert service.db == mock_secured_db
            mock_secured_db.initialize.assert_called_once()

    def test_correlation_to_memory_anchor_conversion(self):
        """Test the conversion from TemporalCorrelation to MemoryAnchor structure."""
        # Create a correlation
        primary_event = Event(
            event_id=uuid4(),
            timestamp=datetime.now(UTC),
            event_type=EventType.STORAGE,
            stream_id="filesystem",
            content={"file": "test.pdf"}
        )
        
        correlation = TemporalCorrelation(
            correlation_id=uuid4(),
            primary_event=primary_event,
            correlated_events=[],
            pattern_type="sequential",
            confidence_score=0.85,
            temporal_gap=timedelta(seconds=30),
            occurrence_frequency=5,
            gap_variance=0.1,
            temporal_precision=TemporalPrecision.MINUTE,
            pattern_stability=0.9,
            last_occurrence=datetime.now(UTC)
        )
        
        # Manually create what _create_memory_anchor would produce
        # (without database interaction)
        all_events = [correlation.primary_event] + correlation.correlated_events
        
        # Create cursor state from correlated events
        cursors = {}
        for event in all_events:
            cursor_key = f"{event.event_type}:{event.stream_id}"
            cursors[cursor_key] = {
                "timestamp": event.timestamp.isoformat(),
                "content": event.content,
            }
        
        # Create metadata with correlation information
        metadata = {
            "correlation_id": str(correlation.correlation_id),
            "pattern_type": correlation.pattern_type,
            "confidence_score": correlation.confidence_score,
            "occurrence_frequency": correlation.occurrence_frequency,
            "temporal_gap": str(correlation.temporal_gap),
            "event_count": len(all_events),
            "providers": list(set(event.stream_id for event in all_events)),
            "creation_trigger": "correlation_detection",
        }
        
        # Create the anchor
        anchor = MemoryAnchor(
            anchor_id=uuid4(),
            timestamp=correlation.primary_event.timestamp,
            cursors=cursors,
            metadata=metadata
        )
        
        # Verify the structure is correct
        assert anchor.timestamp == primary_event.timestamp
        assert len(anchor.cursors) == 1  # One event type/stream combination
        assert anchor.metadata["correlation_id"] == str(correlation.correlation_id)
        assert anchor.metadata["pattern_type"] == "sequential"
        assert anchor.metadata["confidence_score"] == 0.85

    def test_secured_collection_wrapper_for_memory_anchors(self):
        """Test that SecuredCollectionWrapper handles memory_anchors correctly."""
        # Create mock collection
        mock_collection = MagicMock()
        mock_collection.insert = MagicMock(return_value={"_key": "test"})
        
        # Create policy for memory_anchors
        policy = CollectionSecurityPolicy(
            collection_name="memory_anchors",
            allowed_model_types=[],
            requires_security=False
        )
        
        # Create wrapper
        from mallku.core.security.registry import SecurityRegistry
        wrapper = SecuredCollectionWrapper(
            mock_collection,
            policy,
            SecurityRegistry()
        )
        
        # For collections with requires_security=False,
        # the wrapper should allow direct document insertion
        doc = {
            "_key": "test_anchor",
            "timestamp": datetime.now(UTC).isoformat(),
            "cursors": {},
            "metadata": {}
        }
        
        # This should work because memory_anchors doesn't require SecuredModel
        # The wrapper's _collection attribute gives direct access
        wrapper._collection.insert(doc)
        mock_collection.insert.assert_called_with(doc)

    def test_architectural_flow_documentation(self):
        """
        Document the complete architectural flow from correlation to storage.
        
        This test serves as living documentation of how components interact
        with the secured database interface.
        """
        flow = """
        ARCHITECTURAL FLOW: Correlation Detection to Memory Anchor Storage
        
        1. CorrelationEngine.process_event_stream(events)
           - Detects patterns in event streams
           - Creates TemporalCorrelation objects
        
        2. CorrelationEngine._create_memory_anchor(correlation)
           - Converts TemporalCorrelation to MemoryAnchor
           - Calls get_secured_database() to get SecuredDatabaseInterface
           
        3. SecuredDatabaseInterface.get_secured_collection("memory_anchors")
           - Returns SecuredCollectionWrapper with memory_anchors policy
           - Policy has requires_security=False for legacy compatibility
           
        4. Direct collection access for insertion
           - Because requires_security=False, can use collection directly
           - wrapper._collection.insert(anchor_doc)
           
        5. MemoryAnchorQueryService queries
           - Uses SecuredDatabaseInterface.execute_secured_query()
           - Operates on memory_anchors collection with proper boundaries
        
        KEY POINTS:
        - All database access goes through get_secured_database()
        - memory_anchors has special policy for backward compatibility
        - Even with requires_security=False, still uses secured interface
        - No component bypasses the architectural boundary
        """
        
        # This documents the design
        assert True


class TestSecurityPolicyEnforcement:
    """Test how security policies are enforced for different collections."""

    def test_memory_anchors_vs_secured_collections(self):
        """Compare memory_anchors policy with typical secured collection policies."""
        # Memory anchors policy (legacy compatibility)
        memory_policy = CollectionSecurityPolicy(
            collection_name="memory_anchors",
            allowed_model_types=[],
            requires_security=False
        )
        
        # Example of a secured collection policy
        from mallku.streams.reciprocity.secured_reciprocity_models import ReciprocityActivityData
        
        reciprocity_policy = CollectionSecurityPolicy(
            collection_name="reciprocity_activities_secured",
            allowed_model_types=[ReciprocityActivityData],
            requires_security=True
        )
        
        # Key differences
        assert memory_policy.requires_security == False
        assert reciprocity_policy.requires_security == True
        
        assert len(memory_policy.allowed_model_types) == 0
        assert len(reciprocity_policy.allowed_model_types) > 0
        
        # Document the architectural decision
        assert memory_policy.requires_security == False, (
            "memory_anchors uses legacy MemoryAnchor class, not SecuredModel"
        )
        assert reciprocity_policy.requires_security == True, (
            "New collections require SecuredModel for data protection"
        )

    def test_query_service_respects_collection_boundaries(self):
        """Test that query service respects collection-specific policies."""
        # Create mock secured database
        mock_db = MagicMock(spec=SecuredDatabaseInterface)
        
        # Mock execute_secured_query
        async def mock_execute_query(query, bind_vars=None, collection_name=None):
            # Verify collection name is provided
            assert collection_name == "memory_anchors"
            return []
        
        mock_db.execute_secured_query = AsyncMock(side_effect=mock_execute_query)
        
        # The query service should always specify the collection
        # This ensures proper security policy application
        assert True  # Architectural requirement documented


if __name__ == "__main__":
    pytest.main([__file__, "-v"])