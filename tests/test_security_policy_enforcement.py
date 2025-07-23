"""
Test: Security Policy Enforcement Verification
==============================================

Fifth Guardian - Verifying that structure enforces security

This test validates that security policies actually prevent unauthorized
operations as specified in Issue #17:

1. Unauthorized access attempts should be blocked
2. Field obfuscation should work for sensitive collections
3. Collection-specific policies should be enforced correctly
4. Security violations should be properly logged and tracked

This demonstrates the cathedral principle: structure enforces behavior.
"""

from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from mallku.core.database import get_database
from mallku.core.database.secured_interface import (
    CollectionSecurityPolicy,
    SecuredCollectionWrapper,
    SecurityViolationError,
)
from mallku.core.security.field_strategies import (
    FieldIndexStrategy,
    FieldObfuscationLevel,
    SearchCapability,
)
from mallku.core.security.registry import SecurityRegistry
from mallku.core.security.secured_model import SecuredField, SecuredModel
from mallku.models import MemoryAnchor
from mallku.streams.reciprocity.secured_reciprocity_models import (
    ReciprocityActivityData,
    ReciprocityBalance,
)


@pytest.mark.integration
class TestSecurityPolicyEnforcement:
    """Test that security policies are properly enforced."""

    @pytest.fixture
    async def secured_db(self):
        """Initialize secured database with test collections."""
        db = get_database()
        await db.initialize()

        # Register test collection policies
        # Test collection that requires security
        test_secured_policy = CollectionSecurityPolicy(
            collection_name="test_secured_collection",
            allowed_model_types=[TestSecuredModel],
            requires_security=True,
            schema_validation={
                "type": "object",
                "properties": {"_key": {"type": "string"}},
                "required": ["_key"],
                "additionalProperties": True,
            },
        )
        db.register_collection_policy(test_secured_policy)

        # Test collection without security (like memory_anchors)
        test_unsecured_policy = CollectionSecurityPolicy(
            collection_name="test_unsecured_collection",
            allowed_model_types=[],
            requires_security=False,
            schema_validation={
                "type": "object",
                "properties": {"_key": {"type": "string"}},
                "additionalProperties": True,
            },
        )
        db.register_collection_policy(test_unsecured_policy)

        yield db

    @pytest.mark.asyncio
    async def test_unauthorized_model_insertion_blocked(self, secured_db):
        """Test that inserting non-SecuredModel into secured collection fails."""
        # Get reciprocity activities collection (requires security)
        collection = await secured_db.get_secured_collection("reciprocity_activities_secured")

        # Try to insert a regular dict (not a SecuredModel)
        regular_doc = {
            "_key": "unauthorized_test",
            "timestamp": datetime.now(UTC).isoformat(),
            "data": "this should fail",
        }

        # This should raise SecurityViolationError
        with pytest.raises(SecurityViolationError) as exc_info:
            await collection.insert_secured(regular_doc)

        assert "requires SecuredModel instances" in str(exc_info.value)

        # Verify security violation was tracked
        metrics = secured_db.get_security_metrics()
        assert len(metrics["recent_violations"]) > 0 or metrics["security_violations"] > 0

    @pytest.mark.asyncio
    async def test_wrong_model_type_blocked(self, secured_db):
        """Test that inserting wrong SecuredModel type into collection fails."""
        # Create a ReciprocityBalance instance
        balance = ReciprocityBalance(
            participant_a_id="user_a",
            participant_b_id="user_b",
            current_balance=0.5,
            total_interactions=10,
        )

        # Try to insert it into reciprocity_activities_secured collection
        # (which expects ReciprocityActivityData)
        collection = await secured_db.get_secured_collection("reciprocity_activities_secured")

        with pytest.raises(SecurityViolationError) as exc_info:
            await collection.insert_secured(balance)

        assert "not allowed in reciprocity_activities_secured" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_field_obfuscation_round_trip(self, secured_db):
        """Test that field obfuscation and deobfuscation work correctly."""
        # Create security registry
        registry = secured_db.get_security_registry()

        # Create a reciprocity activity with sensitive data
        activity = ReciprocityActivityData(
            memory_anchor_uuid=uuid4(),
            timestamp=datetime.now(UTC),
            interaction_id=uuid4(),
            interaction={
                "type": "contribution",
                "value": 100,
                "sensitive_data": "should be encrypted",
            },
            initiator="human",
            participants=["alice@example.com", "bob@example.com"],
            ayni_score={"balance": 0.7, "confidence": 0.9},
        )

        # Set registry for obfuscation
        activity.set_registry(registry)

        # Convert to storage format (obfuscated)
        storage_dict = activity.to_storage_dict(registry)

        # Verify fields are obfuscated
        # Check that original field names are not present
        assert "timestamp" not in storage_dict
        assert "interaction" not in storage_dict
        assert "participants" not in storage_dict

        # Verify UUIDs are used instead
        field_uuids = list(storage_dict.keys())
        assert all(
            key.startswith("_")  # Private fields
            or len(key) == 36  # UUID format (with hyphens)
            for key in field_uuids
        )

        # Now test deobfuscation
        ReciprocityActivityData.set_registry(registry)
        restored_activity = ReciprocityActivityData.from_storage_dict(storage_dict)

        # Verify data integrity after round trip
        assert restored_activity.memory_anchor_uuid == activity.memory_anchor_uuid
        assert restored_activity.interaction_id == activity.interaction_id
        assert restored_activity.initiator == activity.initiator
        assert restored_activity.participants == activity.participants
        assert restored_activity.ayni_score == activity.ayni_score

    @pytest.mark.asyncio
    async def test_collection_specific_policies(self, secured_db):
        """Test that different collections enforce their specific policies."""
        # Test 1: memory_anchors allows regular documents
        memory_collection = await secured_db.get_secured_collection("memory_anchors")

        anchor = MemoryAnchor(
            anchor_id=uuid4(),
            timestamp=datetime.now(UTC),
            cursors={"test": {"data": "value"}},
            metadata={"test": True},
        )

        # This should succeed (requires_security=False)
        result = memory_collection._collection.insert(anchor.to_arangodb_document())
        assert result is not None

        # Test 2: reciprocity collections require SecuredModel
        reciprocity_collection = await secured_db.get_secured_collection(
            "reciprocity_activities_secured"
        )

        # Create proper SecuredModel instance
        activity = ReciprocityActivityData(
            memory_anchor_uuid=uuid4(),
            timestamp=datetime.now(UTC),
            interaction_id=uuid4(),
            initiator="ai",
            participants=["mallku"],
            ayni_score={"balance": 0.0},
        )

        # This should succeed
        result = await reciprocity_collection.insert_secured(activity)
        assert result is not None

        # Test 3: Wrong model type should fail
        balance = ReciprocityBalance(
            participant_a_id="a", participant_b_id="b", current_balance=0.0
        )

        with pytest.raises(SecurityViolationError):
            await reciprocity_collection.insert_secured(balance)

    @pytest.mark.asyncio
    async def test_security_violation_logging(self, secured_db):
        """Test that security violations are properly logged and tracked."""
        # Get initial metrics
        initial_metrics = secured_db.get_security_metrics()
        initial_violations = initial_metrics["security_violations"]

        # Attempt several violations
        violations_attempted = 0

        # Violation 1: Try to access non-existent collection
        try:
            await secured_db.get_secured_collection("nonexistent_collection")
        except SecurityViolationError:
            violations_attempted += 1

        # Violation 2: Try to insert wrong type
        try:
            collection = await secured_db.get_secured_collection("reciprocity_activities_secured")
            await collection.insert_secured({"not": "a secured model"})
        except SecurityViolationError:
            violations_attempted += 1

        # Get updated metrics
        final_metrics = secured_db.get_security_metrics()

        # Verify violations were tracked
        assert final_metrics["security_violations"] >= initial_violations + violations_attempted

        # Check recent violations list
        if "recent_violations" in final_metrics:
            assert len(final_metrics["recent_violations"]) > 0

    @pytest.mark.asyncio
    async def test_query_transformation_secured_vs_unsecured(self, secured_db):
        """Test that queries are transformed correctly for secured collections."""
        # Test query on unsecured collection (memory_anchors)
        memory_query = """
        FOR doc IN memory_anchors
            FILTER doc.timestamp > @start_time
            RETURN doc
        """

        # This should work without transformation
        results = await secured_db.execute_secured_query(
            memory_query,
            bind_vars={"start_time": datetime.now(UTC).isoformat()},
            collection_name="memory_anchors",
        )

        # Results should be returned as-is (no deobfuscation needed)
        assert isinstance(results, list)

        # Test query on secured collection
        # Note: In real implementation, field names would be transformed to UUIDs
        secured_query = """
        FOR doc IN reciprocity_activities_secured
            LIMIT 1
            RETURN doc
        """

        # Execute query on secured collection
        results = await secured_db.execute_secured_query(
            secured_query, collection_name="reciprocity_activities_secured"
        )

        # Results would be deobfuscated if any exist
        assert isinstance(results, list)

    @pytest.mark.asyncio
    async def test_error_handling_security_requirements(self, secured_db):
        """Test error handling when security requirements aren't met."""
        # Test 1: Collection without policy
        mock_collection = MagicMock()
        mock_collection.name = "unregistered_collection"

        # Create wrapper without policy should fail
        with pytest.raises(Exception):
            from mallku.core.security.registry import SecurityRegistry

            SecuredCollectionWrapper(
                mock_collection,
                None,  # No policy
                SecurityRegistry(),
            )

        # Test 2: Invalid security configuration
        with pytest.raises(Exception):
            # Try to create policy with invalid configuration
            CollectionSecurityPolicy(
                collection_name="",  # Empty name
                allowed_model_types=[],
                requires_security=True,
            )

    @pytest.mark.asyncio
    async def test_secured_collection_wrapper_blocks_unsafe_operations(self, secured_db):
        """Test that SecuredCollectionWrapper blocks direct unsafe operations."""
        collection = await secured_db.get_secured_collection("reciprocity_activities_secured")

        # List of operations that should be blocked
        unsafe_operations = [
            "insert",
            "update",
            "delete",
            "truncate",
            "insert_many",
            "update_many",
            "delete_many",
        ]

        for operation in unsafe_operations:
            with pytest.raises(SecurityViolationError) as exc_info:
                # Try to access the unsafe operation
                getattr(collection, operation)

            assert "not allowed" in str(exc_info.value)
            assert operation in str(exc_info.value)


@pytest.mark.integration
class TestFieldLevelSecurity:
    """Test field-level security features."""

    @pytest.mark.asyncio
    async def test_field_obfuscation_levels(self):
        """Test different field obfuscation levels."""
        registry = SecurityRegistry()

        # Create activity with various obfuscation levels
        activity = ReciprocityActivityData(
            memory_anchor_uuid=uuid4(),  # UUID_ONLY
            timestamp=datetime.now(UTC),  # UUID_ONLY with temporal offset
            interaction_id=uuid4(),  # UUID_ONLY
            interaction={"secret": "data"},  # ENCRYPTED
            initiator="human",  # UUID_ONLY with deterministic
            participants=["user1", "user2"],  # ENCRYPTED
            ayni_score={"balance": 0.5},  # ENCRYPTED with bucketing
        )

        activity.set_registry(registry)
        storage_dict = activity.to_storage_dict(registry)

        # Verify each field is obfuscated according to its level
        # All fields should be UUID keys (except private fields)
        for key in storage_dict:
            if not key.startswith("_"):
                # Should be a UUID (36 chars with hyphens)
                assert len(key) == 36
                assert key.count("-") == 4

    @pytest.mark.asyncio
    async def test_temporal_offset_strategy(self):
        """Test temporal offset indexing strategy."""
        registry = SecurityRegistry()

        # Create multiple activities with different timestamps
        now = datetime.now(UTC)
        activities = []

        for i in range(5):
            activity = ReciprocityActivityData(
                memory_anchor_uuid=uuid4(),
                timestamp=now + timedelta(hours=i),
                interaction_id=uuid4(),
                initiator="system",
                participants=[],
                ayni_score={},
            )
            activity.set_registry(registry)
            activities.append(activity)

        # Temporal offset should preserve relative ordering
        # but hide absolute times
        storage_dicts = [a.to_storage_dict(registry) for a in activities]

        # Extract timestamp field UUID
        timestamp_uuid = registry.get_or_create_mapping(
            "timestamp", activities[0].__fields__["timestamp"].json_schema_extra["security_config"]
        )

        # Verify temporal relationships are preserved
        # (exact implementation depends on temporal offset strategy)
        assert all(timestamp_uuid in d for d in storage_dicts)

    @pytest.mark.asyncio
    async def test_bucketed_indexing_strategy(self):
        """Test bucketed indexing for range queries."""
        registry = SecurityRegistry()

        # Create balances with different values
        balances = []
        test_values = [-0.9, -0.3, 0.0, 0.3, 0.9]

        for val in test_values:
            balance = ReciprocityBalance(
                participant_a_id=f"user_a_{val}",
                participant_b_id=f"user_b_{val}",
                current_balance=val,
                total_interactions=10,
            )
            balance.set_registry(registry)
            balances.append(balance)

        # Bucketed values should map to defined buckets
        # Buckets: [-1.0, -0.8, -0.5, -0.2, 0.0, 0.2, 0.5, 0.8, 1.0]
        # This preserves range query capability while hiding exact values


class TestSecuredModel(SecuredModel):
    """Test model for security enforcement tests."""

    test_id: uuid4 = SecuredField(
        default_factory=uuid4,
        obfuscation_level=FieldObfuscationLevel.UUID_ONLY,
        index_strategy=FieldIndexStrategy.IDENTITY,
        search_capabilities=[SearchCapability.EQUALITY],
    )

    sensitive_data: str = SecuredField(
        default="",
        obfuscation_level=FieldObfuscationLevel.ENCRYPTED,
        index_strategy=FieldIndexStrategy.NONE,
        security_notes="Contains sensitive information",
    )

    public_data: str = SecuredField(
        default="",
        obfuscation_level=FieldObfuscationLevel.NONE,
        index_strategy=FieldIndexStrategy.IDENTITY,
        security_notes="Public information, no obfuscation needed",
    )


@pytest.mark.integration
class TestSecurityMetrics:
    """Test security metrics collection and reporting."""

    @pytest.mark.asyncio
    async def test_comprehensive_security_metrics(self, secured_db):
        """Test that all security operations update metrics correctly."""
        # Get baseline metrics
        baseline = secured_db.get_security_metrics()

        # Perform various operations
        operations_performed = 0

        # 1. Get collection (successful)
        collection = await secured_db.get_secured_collection("memory_anchors")
        operations_performed += 1

        # 2. Insert into memory_anchors (successful)
        anchor = MemoryAnchor(
            anchor_id=uuid4(), timestamp=datetime.now(UTC), cursors={}, metadata={}
        )
        collection._collection.insert(anchor.to_arangodb_document())
        operations_performed += 1

        # 3. Query execution
        await secured_db.execute_secured_query(
            "FOR doc IN memory_anchors LIMIT 1 RETURN doc", collection_name="memory_anchors"
        )
        operations_performed += 1

        # Get final metrics
        final = secured_db.get_security_metrics()

        # Verify metrics updated
        assert final["operations_count"] >= baseline["operations_count"] + operations_performed
        assert final["registered_collections"] >= 3  # At least the default ones
        assert "compliance_score" not in final or 0 <= final.get("compliance_score", 1) <= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
