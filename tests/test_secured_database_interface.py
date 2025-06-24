"""
Tests for the Secured Database Interface

These tests validate that the security-by-design architecture actually works
and prevents the bypass scenarios that were discovered.
"""

from unittest.mock import MagicMock

import pytest
from mallku.core.database.secured_interface import (
    CollectionSecurityPolicy,
    SecuredCollectionWrapper,
    SecuredDatabaseInterface,
    SecurityViolationError,
)
from mallku.core.security.field_strategies import FieldObfuscationLevel
from mallku.core.security.secured_model import SecuredField, SecuredModel


class TestSecuredModel(SecuredModel):
    """Test model for security validation."""

    test_id: str = SecuredField(obfuscation_level=FieldObfuscationLevel.UUID_ONLY)
    test_data: str = SecuredField(obfuscation_level=FieldObfuscationLevel.ENCRYPTED)


class UnsecuredModel:
    """Non-secured model that should be rejected."""

    def __init__(self, data):
        self.data = data


@pytest.fixture
def mock_database():
    """Mock ArangoDB database."""
    db = MagicMock()
    db.has_collection.return_value = False
    db.create_collection.return_value = MagicMock()
    db.collection.return_value = MagicMock()
    return db


@pytest.fixture
def secured_interface(mock_database):
    """Secured database interface with mocked database."""
    interface = SecuredDatabaseInterface(mock_database)
    interface._initialized = True  # Skip async initialization for tests
    return interface


class TestSecuredDatabaseInterface:
    """Test the secured database interface enforces security policies."""

    @pytest.mark.asyncio
    async def test_initialization_loads_security_registry(self, mock_database):
        """Test that initialization properly loads security registry."""
        interface = SecuredDatabaseInterface(mock_database)

        # Mock the database to return no existing registry
        mock_database.has_collection.return_value = False

        await interface.initialize()

        assert interface._initialized
        assert interface._security_registry is not None
        assert len(interface._collection_policies) > 0  # Default policies registered

    def test_collection_policy_validation_success(self):
        """Test that valid secured models pass policy validation."""
        policy = CollectionSecurityPolicy(
            collection_name="test_collection",
            allowed_model_types=[TestSecuredModel],
            requires_security=True,
        )

        model = TestSecuredModel(test_id="123", test_data="secret")

        # Should not raise exception
        policy.validate_model(model)

    def test_collection_policy_validation_rejects_unsecured_models(self):
        """Test that unsecured models are rejected by security policy."""
        policy = CollectionSecurityPolicy(
            collection_name="test_collection",
            allowed_model_types=[TestSecuredModel],
            requires_security=True,
        )

        unsecured_model = UnsecuredModel("data")

        with pytest.raises(SecurityViolationError) as exc_info:
            policy.validate_model(unsecured_model)

        assert "requires SecuredModel instances" in str(exc_info.value)

    def test_collection_policy_validation_rejects_wrong_model_type(self):
        """Test that wrong secured model types are rejected."""
        policy = CollectionSecurityPolicy(
            collection_name="test_collection",
            allowed_model_types=[TestSecuredModel],
            requires_security=True,
        )

        # Create a different secured model type
        class OtherSecuredModel(SecuredModel):
            other_field: str = SecuredField()

        wrong_model = OtherSecuredModel(other_field="test")

        with pytest.raises(SecurityViolationError) as exc_info:
            policy.validate_model(wrong_model)

        assert "not allowed in test_collection" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_create_secured_collection_registers_policy(
        self, secured_interface, mock_database
    ):
        """Test that creating secured collection registers its policy."""
        policy = CollectionSecurityPolicy(
            collection_name="test_secured",
            allowed_model_types=[TestSecuredModel],
            requires_security=True,
        )

        mock_collection = MagicMock()
        mock_database.create_collection.return_value = mock_collection

        result = await secured_interface.create_secured_collection("test_secured", policy)

        assert isinstance(result, SecuredCollectionWrapper)
        assert "test_secured" in secured_interface._collection_policies
        mock_database.create_collection.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_secured_collection_requires_policy(self, secured_interface, mock_database):
        """Test that getting collection requires registered security policy."""
        mock_database.has_collection.return_value = True

        with pytest.raises(SecurityViolationError) as exc_info:
            await secured_interface.get_secured_collection("unregistered_collection")

        assert "No security policy registered" in str(exc_info.value)

    def test_security_metrics_tracking(self, secured_interface):
        """Test that security metrics are properly tracked."""
        secured_interface._operation_count = 5
        secured_interface._security_violations = ["violation1", "violation2"]

        metrics = secured_interface.get_security_metrics()

        assert metrics["operations_count"] == 5
        assert metrics["security_violations"] == 2
        assert "registered_collections" in metrics
        assert "uuid_mappings" in metrics


class TestSecuredCollectionWrapper:
    """Test the secured collection wrapper blocks unsafe operations."""

    @pytest.fixture
    def mock_collection(self):
        """Mock ArangoDB collection."""
        collection = MagicMock()
        collection.insert.return_value = {"_id": "test_id", "_key": "test_key"}
        collection.get.return_value = {"test_field": "test_value"}
        collection.count.return_value = 10
        return collection

    @pytest.fixture
    def collection_policy(self):
        """Test collection policy."""
        return CollectionSecurityPolicy(
            collection_name="test_collection",
            allowed_model_types=[TestSecuredModel],
            requires_security=True,
        )

    @pytest.fixture
    def secured_wrapper(self, mock_collection, collection_policy):
        """Secured collection wrapper."""
        from mallku.core.security.registry import SecurityRegistry

        registry = SecurityRegistry()
        return SecuredCollectionWrapper(mock_collection, collection_policy, registry)

    @pytest.mark.asyncio
    async def test_insert_secured_validates_model(self, secured_wrapper):
        """Test that insert_secured validates the model type."""
        valid_model = TestSecuredModel(test_id="123", test_data="secret")

        # Should not raise exception
        result = await secured_wrapper.insert_secured(valid_model)
        assert result is not None

    @pytest.mark.asyncio
    async def test_insert_secured_rejects_unsecured_model(self, secured_wrapper):
        """Test that insert_secured rejects unsecured models."""
        unsecured_model = UnsecuredModel("data")

        with pytest.raises(SecurityViolationError):
            await secured_wrapper.insert_secured(unsecured_model)

    def test_direct_insert_blocked(self, secured_wrapper):
        """Test that direct insert operations are blocked."""
        with pytest.raises(SecurityViolationError) as exc_info:
            secured_wrapper.insert({"direct": "data"})

        assert "Direct access to insert is not allowed" in str(exc_info.value)

    def test_direct_update_blocked(self, secured_wrapper):
        """Test that direct update operations are blocked."""
        with pytest.raises(SecurityViolationError) as exc_info:
            secured_wrapper.update({"_key": "test"}, {"new": "data"})

        assert "Direct access to update is not allowed" in str(exc_info.value)

    def test_safe_operations_allowed(self, secured_wrapper):
        """Test that safe operations are still allowed."""
        # These should work without exception
        count = secured_wrapper.count()
        exists = secured_wrapper.exists()

        assert count == 10
        assert exists is True


class TestSecurityEnforcement:
    """Integration tests for security enforcement."""

    @pytest.mark.asyncio
    async def test_end_to_end_security_enforcement(self, mock_database):
        """Test complete security enforcement flow."""
        # Create secured interface
        interface = SecuredDatabaseInterface(mock_database)
        await interface.initialize()

        # Create security policy
        policy = CollectionSecurityPolicy(
            collection_name="secure_test",
            allowed_model_types=[TestSecuredModel],
            requires_security=True,
        )

        # Create secured collection
        mock_database.has_collection.return_value = False
        mock_collection = MagicMock()
        mock_database.create_collection.return_value = mock_collection

        wrapper = await interface.create_secured_collection("secure_test", policy)

        # Test that only secured models can be inserted
        valid_model = TestSecuredModel(test_id="123", test_data="secret")
        await wrapper.insert_secured(valid_model)

        # Test that unsecured models are rejected
        with pytest.raises(SecurityViolationError):
            await wrapper.insert_secured(UnsecuredModel("bad"))

        # Test that direct operations are blocked
        with pytest.raises(SecurityViolationError):
            wrapper.insert({"bypass": "attempt"})

    def test_no_bypass_possible_through_wrapper(self, mock_database):
        """Test that no bypass is possible through the wrapper layer."""
        from mallku.core.security.registry import SecurityRegistry

        policy = CollectionSecurityPolicy(
            collection_name="test", allowed_model_types=[TestSecuredModel], requires_security=True
        )

        wrapper = SecuredCollectionWrapper(mock_database, policy, SecurityRegistry())

        # All these should raise SecurityViolationError
        unsafe_operations = [
            lambda: wrapper.insert({}),
            lambda: wrapper.insert_many([]),
            lambda: wrapper.update({}, {}),
            lambda: wrapper.replace({}, {}),
            lambda: wrapper.delete({}),
            lambda: wrapper.truncate(),
        ]

        for operation in unsafe_operations:
            with pytest.raises(SecurityViolationError):
                operation()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
