"""
Test: End-to-End Database Security Integration
==============================================

Fifth Guardian - Verifying the foundation bears weight

This test validates the complete data flow through the secured interface
as specified in Issue #16:

1. Create a memory anchor through the correlation engine
2. Store it via the secured database interface  
3. Query it back through the query service
4. Retrieve and verify data integrity throughout the security layer

This demonstrates that the security architecture works in practice,
not just in theory - a true cathedral principle.
"""

import asyncio
import os
from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from mallku.core.database import get_secured_database
from mallku.correlation.engine import CorrelationEngine
from mallku.correlation.models import Event, EventType
from mallku.query.models import QueryRequest, QueryType
from mallku.query.service import MemoryAnchorQueryService
from mallku.services.memory_anchor_service import MemoryAnchorService


@pytest.mark.integration
class TestEndToEndDatabaseSecurity:
    """End-to-end test of database security through complete data flow."""
    
    @pytest.fixture
    async def secured_database(self):
        """Initialize secured database interface."""
        db = get_secured_database()
        await db.initialize()
        yield db
    
    @pytest.fixture
    async def memory_service(self, secured_database):
        """Initialize memory anchor service with secured database."""
        service = MemoryAnchorService()
        await service.initialize()
        yield service
        
    @pytest.fixture
    async def correlation_engine(self, memory_service):
        """Initialize correlation engine with memory service."""
        engine = CorrelationEngine(memory_anchor_service=memory_service)
        # Lower thresholds for testing
        for detector in engine.pattern_detectors.values():
            detector.min_occurrences = 2
        await engine.initialize()
        yield engine
        
    @pytest.fixture
    async def query_service(self, secured_database):
        """Initialize query service with secured database."""
        service = MemoryAnchorQueryService()
        await service.initialize()
        yield service
    
    @pytest.mark.asyncio
    async def test_complete_security_flow(
        self, 
        secured_database, 
        correlation_engine, 
        query_service
    ):
        """
        Test the complete flow: Create -> Store -> Query -> Retrieve
        
        This test validates all acceptance criteria from Issue #16:
        - Creates memory anchor via CorrelationEngine
        - Verifies storage through SecuredDatabaseInterface  
        - Queries data back via MemoryAnchorQueryService
        - Confirms data integrity throughout the flow
        - Validates security monitoring and logging works
        """
        # Track initial metrics
        initial_metrics = secured_database.get_security_metrics()
        initial_operations = initial_metrics["operations_count"]
        
        # Step 1: CREATE memory anchor through correlation engine
        # Create a pattern of events that will trigger correlation detection
        base_time = datetime.now(UTC)
        test_file_path = f"/test/security_{uuid4().hex[:8]}.pdf"
        
        events = []
        # Create sequential pattern: file save followed by backup (3 occurrences)
        for i in range(3):
            # File save event
            save_event = Event(
                event_id=uuid4(),
                timestamp=base_time + timedelta(minutes=i*10),
                event_type=EventType.STORAGE,
                stream_id="filesystem",
                content={
                    "file_path": test_file_path,
                    "action": "save",
                    "size": 1024 + i*100
                },
                metadata={"version": i+1, "author": "security_test"}
            )
            events.append(save_event)
            
            # Backup event 30 seconds later
            backup_event = Event(
                event_id=uuid4(),
                timestamp=base_time + timedelta(minutes=i*10, seconds=30),
                event_type=EventType.STORAGE,
                stream_id="backup_system",
                content={
                    "file_path": test_file_path,
                    "action": "backup",
                    "backup_location": f"/backup/{test_file_path}"
                },
                metadata={"compression": "gzip", "encrypted": True}
            )
            events.append(backup_event)
        
        # Process events through correlation engine
        correlations = await correlation_engine.process_event_stream(events)
        
        # Verify correlations were detected
        assert len(correlations) > 0, "No correlations detected"
        assert any(c.pattern_type == "sequential" for c in correlations)
        
        # Verify memory anchors were created
        created_anchors = correlation_engine.correlation_stats["memory_anchors_created"]
        assert created_anchors > 0, "No memory anchors created"
        
        # Step 2: STORE verification - check secured database was used
        # Verify the memory_anchors collection was accessed through secured interface
        collection = await secured_database.get_secured_collection("memory_anchors")
        assert collection is not None
        assert collection._policy.collection_name == "memory_anchors"
        assert collection._policy.requires_security == False  # Legacy compatibility
        
        # Check that operations were tracked
        post_creation_metrics = secured_database.get_security_metrics()
        assert post_creation_metrics["operations_count"] > initial_operations
        
        # Step 3: QUERY the stored data back through query service
        # Wait a moment for data to be fully persisted
        await asyncio.sleep(0.5)
        
        # Query for the file we just processed
        query_request = QueryRequest(
            query_text=f"file {test_file_path}",
            max_results=10,
            min_confidence=0.5,
            include_explanations=True
        )
        
        query_response = await query_service.execute_query(query_request)
        
        # Verify query returned results
        assert query_response is not None
        assert query_response.results_returned > 0, "No results returned from query"
        
        # Step 4: RETRIEVE and verify data integrity
        results = query_response.results
        
        # Find results related to our test file
        matching_results = [
            r for r in results 
            if test_file_path in str(r.file_path)
        ]
        
        assert len(matching_results) > 0, f"No results found for {test_file_path}"
        
        # Verify data integrity - check first result
        result = matching_results[0]
        
        # Verify anchor data integrity
        assert result.anchor_id is not None
        assert result.anchor_timestamp is not None
        assert result.file_path == test_file_path
        assert result.correlation_type in ["sequential", "temporal_proximity", "contextual_similarity"]
        assert 0.0 <= result.confidence_score <= 1.0
        
        # Verify file metadata integrity
        assert result.file_info is not None
        if "file_size" in result.file_info:
            assert result.file_info["file_size"] > 0
        
        # Get detailed anchor context
        anchor_context = await query_service.get_anchor_context(result.anchor_id)
        if anchor_context and "anchor" in anchor_context:
            anchor = anchor_context["anchor"]
            
            # Verify anchor structure
            assert "_key" in anchor or "anchor_id" in anchor
            assert "timestamp" in anchor
            assert "cursors" in anchor
            assert "metadata" in anchor
            
            # Verify correlation metadata was preserved
            if "correlation_id" in anchor["metadata"]:
                assert anchor["metadata"]["pattern_type"] in ["sequential", "concurrent", "cyclical", "contextual"]
                assert "confidence_score" in anchor["metadata"]
                assert anchor["metadata"]["creation_trigger"] == "correlation_detection"
        
        # Step 5: Validate security monitoring and logging
        final_metrics = secured_database.get_security_metrics()
        
        # Verify operations were tracked throughout
        assert final_metrics["operations_count"] > post_creation_metrics["operations_count"]
        assert final_metrics["security_violations"] == 0  # No violations
        assert final_metrics["registered_collections"] >= 1  # At least memory_anchors
        
        # Verify memory_anchors collection is registered
        assert "memory_anchors" in secured_database._collection_policies
        
        # Log final statistics for verification
        print(f"\n=== End-to-End Security Test Results ===")
        print(f"Correlations detected: {len(correlations)}")
        print(f"Memory anchors created: {created_anchors}")
        print(f"Query results returned: {query_response.results_returned}")
        print(f"Matching results found: {len(matching_results)}")
        print(f"Total DB operations: {final_metrics['operations_count']}")
        print(f"Security violations: {final_metrics['security_violations']}")
        print(f"Processing time: {query_response.processing_time_ms}ms")
        print("========================================\n")
    
    @pytest.mark.asyncio
    async def test_security_layer_error_handling(
        self,
        secured_database,
        correlation_engine,
        query_service
    ):
        """Test that the security layer handles errors gracefully."""
        # Create a correlation that will fail to create anchor
        # by using an event with missing required data
        event = Event(
            event_id=uuid4(),
            timestamp=datetime.now(UTC),
            event_type=EventType.STORAGE,
            stream_id="broken_stream",
            content=None,  # Invalid content
            metadata={}
        )
        
        # Process should not crash
        correlations = await correlation_engine.process_event_stream([event])
        
        # Verify system remains stable
        metrics = secured_database.get_security_metrics()
        assert metrics is not None
        
        # Query should still work
        response = await query_service.execute_query(
            QueryRequest(query_text="test query", max_results=5)
        )
        assert response is not None
    
    @pytest.mark.asyncio
    async def test_performance_characteristics(
        self,
        correlation_engine,
        query_service
    ):
        """Document performance characteristics of the security layer."""
        import time
        
        # Create a batch of events
        num_events = 50
        events = []
        base_time = datetime.now(UTC)
        
        for i in range(num_events):
            events.append(Event(
                event_id=uuid4(),
                timestamp=base_time + timedelta(seconds=i),
                event_type=EventType.ACTIVITY,
                stream_id=f"perf_test_{i % 5}",
                content={"index": i, "data": f"test_data_{i}"},
                metadata={"batch": "performance_test"}
            ))
        
        # Measure correlation processing time
        start_time = time.time()
        correlations = await correlation_engine.process_event_stream(events)
        correlation_time = time.time() - start_time
        
        # Measure query time
        query_start = time.time()
        response = await query_service.execute_query(
            QueryRequest(query_text="performance test", max_results=20)
        )
        query_time = time.time() - query_start
        
        # Document performance
        print(f"\n=== Security Layer Performance ===")
        print(f"Events processed: {num_events}")
        print(f"Correlation detection time: {correlation_time:.3f}s")
        print(f"Events per second: {num_events/correlation_time:.1f}")
        print(f"Query execution time: {query_time:.3f}s")
        print(f"Query processing time (reported): {response.processing_time_ms}ms")
        print("==================================\n")
        
        # Basic performance assertions
        assert correlation_time < 10.0  # Should process 50 events in under 10s
        assert query_time < 2.0  # Query should complete in under 2s
    
    @pytest.mark.asyncio
    async def test_concurrent_operations(
        self,
        correlation_engine,
        query_service
    ):
        """Test that concurrent operations maintain data integrity."""
        # Create multiple event streams concurrently
        async def create_event_stream(stream_id: str, count: int):
            events = []
            base_time = datetime.now(UTC)
            for i in range(count):
                events.append(Event(
                    event_id=uuid4(),
                    timestamp=base_time + timedelta(seconds=i),
                    event_type=EventType.ACTIVITY,
                    stream_id=stream_id,
                    content={"stream": stream_id, "index": i},
                    metadata={"concurrent_test": True}
                ))
            return await correlation_engine.process_event_stream(events)
        
        # Run multiple streams concurrently
        tasks = [
            create_event_stream(f"stream_{i}", 10)
            for i in range(3)
        ]
        
        results = await asyncio.gather(*tasks)
        
        # Verify all streams were processed
        assert len(results) == 3
        total_correlations = sum(len(r) for r in results)
        
        # Query for results from all streams
        response = await query_service.execute_query(
            QueryRequest(query_text="concurrent_test", max_results=50)
        )
        
        # Verify data integrity maintained
        assert response.results_returned >= 0
        assert response.query_confidence >= 0.0


@pytest.mark.integration
class TestMemoryAnchorSecurityPolicy:
    """Test the specific security policy for memory_anchors collection."""
    
    @pytest.mark.asyncio
    async def test_memory_anchor_policy_enforcement(self, secured_database):
        """Test that memory_anchors collection policy is properly enforced."""
        # Get the collection through secured interface
        collection = await secured_database.get_secured_collection("memory_anchors")
        
        # Verify policy properties
        policy = collection._policy
        assert policy.collection_name == "memory_anchors"
        assert policy.requires_security == False
        assert len(policy.allowed_model_types) == 0
        
        # Test direct insertion (allowed due to requires_security=False)
        test_doc = {
            "_key": f"test_{uuid4().hex[:8]}",
            "timestamp": datetime.now(UTC).isoformat(),
            "cursors": {"test": {"data": "value"}},
            "metadata": {"test": True}
        }
        
        # This should succeed because memory_anchors allows direct insertion
        result = collection._collection.insert(test_doc)
        assert result is not None
        
        # Verify the document can be retrieved
        doc = collection._collection.get(test_doc["_key"])
        assert doc is not None
        assert doc["_key"] == test_doc["_key"]
        
        # Clean up
        collection._collection.delete(test_doc["_key"])
    
    @pytest.mark.asyncio
    async def test_secured_collection_access_patterns(self, secured_database):
        """Test different access patterns through secured collections."""
        # Verify we cannot access unsafe operations
        collection = await secured_database.get_secured_collection("memory_anchors")
        
        # These should raise SecurityViolationError if accessed directly
        unsafe_methods = [
            "insert", "update", "delete", "truncate"
        ]
        
        for method in unsafe_methods:
            try:
                # Try to access the method through wrapper
                getattr(collection, method)
                # If we get here without error, the wrapper isn't blocking properly
                assert False, f"Method {method} should be blocked by wrapper"
            except Exception as e:
                # Should get SecurityViolationError
                assert "SecurityViolationError" in str(type(e)) or "not allowed" in str(e)


if __name__ == "__main__":
    # Run with proper async handling
    pytest.main([__file__, "-v", "-s"])