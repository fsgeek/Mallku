"""
Simple tests to demonstrate the security concept works.

These tests validate the core security principles without requiring
full infrastructure setup.
"""

from unittest.mock import MagicMock

import pytest

from src.mallku.core.database.secured_interface import (
    CollectionSecurityPolicy,
    SecurityViolationError,
)
from src.mallku.core.security.field_strategies import FieldObfuscationLevel
from src.mallku.core.security.secured_model import SecuredField, SecuredModel


class TestSecuredModel(SecuredModel):
    """Test model for security validation."""

    test_id: str = SecuredField(obfuscation_level=FieldObfuscationLevel.UUID_ONLY)
    test_data: str = SecuredField(obfuscation_level=FieldObfuscationLevel.ENCRYPTED)


class UnsecuredModel:
    """Non-secured model that should be rejected."""

    def __init__(self, data):
        self.data = data


class TestSecurityConcept:
    """Test that the security concept actually works."""

    def test_security_policy_accepts_secured_models(self):
        """Test that security policy accepts properly secured models."""
        policy = CollectionSecurityPolicy(
            collection_name="test_collection",
            allowed_model_types=[TestSecuredModel],
            requires_security=True,
        )

        # Create a properly secured model
        secured_model = TestSecuredModel(test_id="123", test_data="secret")

        # This should not raise an exception
        policy.validate_model(secured_model)

        assert True  # If we get here, validation passed

    def test_security_policy_rejects_unsecured_models(self):
        """Test that security policy rejects unsecured models."""
        policy = CollectionSecurityPolicy(
            collection_name="test_collection",
            allowed_model_types=[TestSecuredModel],
            requires_security=True,
        )

        # Create an unsecured model
        unsecured_model = UnsecuredModel("some data")

        # This should raise a SecurityViolationError
        with pytest.raises(SecurityViolationError) as exc_info:
            policy.validate_model(unsecured_model)

        # Verify the error message mentions SecuredModel requirement
        assert "requires SecuredModel instances" in str(exc_info.value)

    def test_security_policy_rejects_wrong_model_types(self):
        """Test that security policy rejects wrong secured model types."""
        # Define policy that only accepts TestSecuredModel
        policy = CollectionSecurityPolicy(
            collection_name="test_collection",
            allowed_model_types=[TestSecuredModel],
            requires_security=True,
        )

        # Create a different secured model type
        class OtherSecuredModel(SecuredModel):
            other_field: str = SecuredField()

        wrong_model = OtherSecuredModel(other_field="test")

        # This should raise a SecurityViolationError
        with pytest.raises(SecurityViolationError) as exc_info:
            policy.validate_model(wrong_model)

        # Verify the error mentions the model type restriction
        assert "not allowed in test_collection" in str(exc_info.value)

    def test_secured_model_has_required_methods(self):
        """Test that SecuredModel has the required security methods."""
        model = TestSecuredModel(test_id="123", test_data="secret")

        # Verify it has the required security methods
        assert hasattr(model, "to_storage_dict")
        assert hasattr(model, "from_storage_dict")
        assert callable(getattr(model, "to_storage_dict"))
        assert callable(getattr(model, "from_storage_dict"))

    def test_non_secured_model_lacks_security_methods(self):
        """Test that non-secured models lack security methods."""
        model = UnsecuredModel("data")

        # Verify it lacks security methods
        assert not hasattr(model, "to_storage_dict")
        assert not hasattr(model, "from_storage_dict")

    def test_security_policy_can_be_configured(self):
        """Test that security policies can be properly configured."""
        # Test strict security policy
        strict_policy = CollectionSecurityPolicy(
            collection_name="strict_collection",
            allowed_model_types=[TestSecuredModel],
            requires_security=True,
            schema_validation={"strict": True},
        )

        assert strict_policy.requires_security is True
        assert TestSecuredModel in strict_policy.allowed_model_types
        assert strict_policy.schema_validation["strict"] is True

        # Test permissive policy (for legacy compatibility)
        permissive_policy = CollectionSecurityPolicy(
            collection_name="legacy_collection", allowed_model_types=[], requires_security=False
        )

        assert permissive_policy.requires_security is False
        assert len(permissive_policy.allowed_model_types) == 0


class TestArchitecturalEnforcement:
    """Test that architectural enforcement concepts work."""

    def test_wrapper_blocks_direct_operations(self):
        """Test that wrapper can block direct operations."""
        from src.mallku.core.database.secured_interface import SecuredCollectionWrapper
        from src.mallku.core.security.registry import SecurityRegistry

        # Create mock collection
        mock_collection = MagicMock()

        # Create policy
        policy = CollectionSecurityPolicy(
            collection_name="test", allowed_model_types=[TestSecuredModel], requires_security=True
        )

        # Create wrapper
        wrapper = SecuredCollectionWrapper(mock_collection, policy, SecurityRegistry())

        # Test that unsafe operations are blocked
        with pytest.raises(SecurityViolationError):
            wrapper.insert({"direct": "data"})

        with pytest.raises(SecurityViolationError):
            wrapper.update({}, {})

        with pytest.raises(SecurityViolationError):
            wrapper.delete({})

    def test_safe_operations_still_work(self):
        """Test that safe operations still work through wrapper."""
        from src.mallku.core.database.secured_interface import SecuredCollectionWrapper
        from src.mallku.core.security.registry import SecurityRegistry

        # Create mock collection
        mock_collection = MagicMock()
        mock_collection.count.return_value = 42

        # Create policy
        policy = CollectionSecurityPolicy(
            collection_name="test", allowed_model_types=[TestSecuredModel], requires_security=True
        )

        # Create wrapper
        wrapper = SecuredCollectionWrapper(mock_collection, policy, SecurityRegistry())

        # Test that safe operations work
        count = wrapper.count()
        assert count == 42

        exists = wrapper.exists()
        assert exists is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
