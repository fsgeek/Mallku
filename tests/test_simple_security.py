"""
Simple security concept test - demonstrates core principles work.

This test validates the basic security enforcement concepts without
requiring complex infrastructure setup.
"""

import pytest


class SecurityViolationError(Exception):
    """Raised when security policy is violated."""

    pass


class SecuredModel:
    """Simple base class for secured models."""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class CollectionSecurityPolicy:
    """Simple security policy for testing."""

    def __init__(self, collection_name, allowed_model_types, requires_security=True):
        self.collection_name = collection_name
        self.allowed_model_types = allowed_model_types
        self.requires_security = requires_security

    def validate_model(self, model):
        """Validate model against security policy."""
        if self.requires_security:
            if not isinstance(model, SecuredModel):
                raise SecurityViolationError(
                    f"Collection {self.collection_name} requires SecuredModel instances"
                )

            if self.allowed_model_types and not any(
                isinstance(model, allowed_type) for allowed_type in self.allowed_model_types
            ):
                allowed_names = [t.__name__ for t in self.allowed_model_types]
                raise SecurityViolationError(
                    f"Model type {type(model).__name__} not allowed in {self.collection_name}. "
                    f"Allowed types: {allowed_names}"
                )


class TestSecuredModel(SecuredModel):
    """Test secured model."""

    pass


class UnsecuredModel:
    """Test unsecured model."""

    def __init__(self, data):
        self.data = data


class TestSecurityConcept:
    """Test that security enforcement concept works."""

    def test_policy_accepts_valid_secured_models(self):
        """Test that policy accepts properly secured models."""
        policy = CollectionSecurityPolicy(
            collection_name="test_collection",
            allowed_model_types=[TestSecuredModel],
            requires_security=True,
        )

        model = TestSecuredModel(test_id="123", test_data="secret")

        # Should not raise exception
        policy.validate_model(model)

    def test_policy_rejects_unsecured_models(self):
        """Test that policy rejects unsecured models."""
        policy = CollectionSecurityPolicy(
            collection_name="test_collection",
            allowed_model_types=[TestSecuredModel],
            requires_security=True,
        )

        unsecured_model = UnsecuredModel("data")

        with pytest.raises(SecurityViolationError) as exc_info:
            policy.validate_model(unsecured_model)

        assert "requires SecuredModel instances" in str(exc_info.value)

    def test_policy_rejects_wrong_secured_model_types(self):
        """Test that policy rejects wrong secured model types."""
        policy = CollectionSecurityPolicy(
            collection_name="test_collection",
            allowed_model_types=[TestSecuredModel],
            requires_security=True,
        )

        class OtherSecuredModel(SecuredModel):
            pass

        wrong_model = OtherSecuredModel(other_field="test")

        with pytest.raises(SecurityViolationError) as exc_info:
            policy.validate_model(wrong_model)

        assert "not allowed in test_collection" in str(exc_info.value)

    def test_permissive_policy_for_legacy_compatibility(self):
        """Test that permissive policies work for legacy systems."""
        policy = CollectionSecurityPolicy(
            collection_name="legacy_collection", allowed_model_types=[], requires_security=False
        )

        unsecured_model = UnsecuredModel("legacy data")

        # Should not raise exception for legacy compatibility
        policy.validate_model(unsecured_model)


class MockCollectionWrapper:
    """Mock wrapper that blocks direct operations."""

    def __init__(self, policy):
        self.policy = policy
        self._blocked_operations = ["insert", "update", "delete", "truncate"]

    def __getattr__(self, name):
        if name in self._blocked_operations:
            raise SecurityViolationError(
                f"Direct access to {name} is not allowed. Use secured methods instead."
            )
        # For safe operations, return a mock
        return lambda *args, **kwargs: f"safe_{name}_operation"


class TestSecurityEnforcement:
    """Test security enforcement through wrapper pattern."""

    def test_wrapper_blocks_unsafe_operations(self):
        """Test that wrapper blocks unsafe operations."""
        policy = CollectionSecurityPolicy("test", [TestSecuredModel], True)
        wrapper = MockCollectionWrapper(policy)

        # These should all raise SecurityViolationError
        with pytest.raises(SecurityViolationError):
            wrapper.insert({"direct": "data"})

        with pytest.raises(SecurityViolationError):
            wrapper.update({}, {})

        with pytest.raises(SecurityViolationError):
            wrapper.delete({})

        with pytest.raises(SecurityViolationError):
            wrapper.truncate()

    def test_wrapper_allows_safe_operations(self):
        """Test that wrapper allows safe operations."""
        policy = CollectionSecurityPolicy("test", [TestSecuredModel], True)
        wrapper = MockCollectionWrapper(policy)

        # These should work
        result = wrapper.count()
        assert result == "safe_count_operation"

        result = wrapper.exists()
        assert result == "safe_exists_operation"


def test_architectural_principle():
    """Test the core architectural principle: structure enforces security."""

    # The principle: security violations should be caught by structure, not guidelines

    # Create a strict security environment
    policy = CollectionSecurityPolicy(
        collection_name="secure_data",
        allowed_model_types=[TestSecuredModel],
        requires_security=True,
    )

    # Valid operation succeeds
    valid_model = TestSecuredModel(sensitive_data="protected")
    policy.validate_model(valid_model)  # Should not raise

    # Invalid operation fails structurally
    invalid_model = UnsecuredModel("unprotected")
    with pytest.raises(SecurityViolationError):
        policy.validate_model(invalid_model)

    # This demonstrates the key insight: the architecture makes
    # security violations impossible, not just discouraged


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
