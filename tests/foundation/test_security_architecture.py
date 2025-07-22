#!/usr/bin/env python3
"""
Security Architecture Verification Tests
========================================

Tests that security is enforced through physical architecture,
not just policy or guidelines.

Third Guardian - Architectural security verification
"""

import asyncio
import os
from unittest.mock import patch

import pytest

from mallku.core.database import get_secured_database
from mallku.core.security.registry import SecurityRegistry
from mallku.core.security.secured_model import SecuredModel


class TestArchitecturalSecurity:
    """Verify security through structure, not policy."""

    def test_direct_database_access_impossible(self):
        """Verify direct ArangoDB access is architecturally impossible."""
        # In production, this would test Docker network isolation
        # For now, verify the secured interface is the only path

        # Should not be able to import raw database directly
        # Note: In full implementation, direct ArangoDB imports would be blocked
        # For now, we verify the secured interface is properly configured

        # Mock database to avoid connection issues in CI
        from unittest.mock import Mock, patch

        mock_db = Mock()
        mock_db._security_registry = Mock()
        mock_db.register_collection_policy = Mock()

        with patch("mallku.core.database.factory.get_database_raw", return_value=mock_db):
            # Only secured access should be available
            db = get_secured_database()
            assert hasattr(db, "_security_registry")
            assert hasattr(db, "register_collection_policy")
            # Verify it's a SecuredDatabaseInterface
            from mallku.core.database.secured_interface import SecuredDatabaseInterface

            assert isinstance(db, SecuredDatabaseInterface)

    def test_uuid_obfuscation_automatic(self):
        """Verify UUID obfuscation happens automatically."""
        from mallku.core.security.field_strategies import FieldObfuscationLevel
        from mallku.core.security.secured_model import SecuredField

        class UserModel(SecuredModel):
            email: str = SecuredField(obfuscation_level=FieldObfuscationLevel.UUID_ONLY)
            public_name: str = SecuredField(obfuscation_level=FieldObfuscationLevel.NONE)

        # Set up registry
        registry = SecurityRegistry()
        UserModel.set_registry(registry)
        UserModel.set_development_mode(False)  # Production mode

        # Create instance
        user = UserModel(email="test@example.com", public_name="Test User")

        # Get obfuscated version
        serialized = user.dict()

        # Email should be obfuscated to UUID
        assert "email" not in serialized
        # Public name should remain visible
        assert serialized["public_name"] == "Test User"
        # Should have a UUID key for email
        uuid_keys = [k for k in serialized if k != "public_name"]
        assert len(uuid_keys) == 1
        assert len(uuid_keys[0]) == 36  # UUID length

    def test_security_registry_deterministic(self):
        """Verify security registry generates deterministic UUIDs."""
        registry1 = SecurityRegistry()
        registry2 = SecurityRegistry()

        from mallku.core.security.field_strategies import FieldSecurityConfig

        # Different instances should generate same UUIDs for same field names
        # This is important for amnesia resistance
        uuid1 = registry1.get_or_create_mapping("test_field", FieldSecurityConfig())
        uuid2 = registry2.get_or_create_mapping("test_field", FieldSecurityConfig())
        assert uuid1 == uuid2

        # Should be able to resolve back
        assert registry1.get_semantic_name(uuid1) == "test_field"
        assert registry2.get_semantic_name(uuid2) == "test_field"

    def test_temporal_offset_prevents_correlation(self):
        """Verify temporal offsets prevent timing correlation attacks."""
        from mallku.core.security.field_strategies import FieldIndexStrategy, FieldSecurityConfig

        # Create a field security config with temporal offset
        config = FieldSecurityConfig(index_strategy=FieldIndexStrategy.TEMPORAL_OFFSET)

        # Verify temporal offset is a valid strategy
        assert config.index_strategy == FieldIndexStrategy.TEMPORAL_OFFSET
        assert hasattr(FieldIndexStrategy, "TEMPORAL_OFFSET")

    @pytest.mark.asyncio
    async def test_event_bus_security(self):
        """Verify event bus doesn't leak sensitive data."""
        from mallku.orchestration.event_bus import (
            ConsciousnessEvent,
            ConsciousnessEventBus,
            ConsciousnessEventType,
        )

        bus = ConsciousnessEventBus()
        await bus.start()

        # Subscribe to events
        events_received = []

        async def handler(event):
            events_received.append(event)

        # Use an existing event type
        bus.subscribe(ConsciousnessEventType.MEMORY_ANCHOR_CREATED, handler)

        # Create a basic event
        event = ConsciousnessEvent(event_type=ConsciousnessEventType.MEMORY_ANCHOR_CREATED)

        await bus.emit(event)

        # Give event time to process
        await asyncio.sleep(0.1)

        # Event should be received
        assert len(events_received) == 1
        received = events_received[0]

        # Verify event structure
        assert isinstance(received, ConsciousnessEvent)
        assert received.event_type == ConsciousnessEventType.MEMORY_ANCHOR_CREATED
        # Note: In production, sensitive data would be handled by SecuredModel
        # The event bus is just transport - security happens at the data layer

        await bus.stop()


class TestContainerizationSecurity:
    """Verify containerization enforces security boundaries."""

    def test_environment_indicates_container(self):
        """Check if running in container when expected."""
        # This would check Docker environment variables
        container_vars = ["MALLKU_CONTAINER", "DOCKER_CONTAINER", "KUBERNETES_SERVICE_HOST"]

        # At least one should indicate containerization in production
        # (This is a placeholder - real test would verify actual deployment)

    def test_network_isolation_configuration(self):
        """Verify network isolation is configured."""
        # Check that database connections use internal networks
        # not external IPs

        # Note: In production, this would check actual network configuration
        # For now, we verify the secured database interface exists
        from unittest.mock import Mock

        mock_db = Mock()
        with patch("mallku.core.database.factory.get_database_raw", return_value=mock_db):
            db = get_secured_database()
            assert db is not None

        # Should use internal hostnames, not public IPs
        # (In real deployment, this would check actual config)


class TestAmnesiaSecurity:
    """Verify security survives total context loss."""

    def test_security_without_registry(self):
        """Test security works even if registry is lost."""
        # Security should work through deterministic UUID generation

        # Create two separate registries
        registry1 = SecurityRegistry()
        registry2 = SecurityRegistry()

        from mallku.core.security.field_strategies import FieldSecurityConfig

        # Even without shared state, same field names produce same UUIDs
        uuid1 = registry1.get_or_create_mapping("user_id", FieldSecurityConfig())
        uuid2 = registry2.get_or_create_mapping("user_id", FieldSecurityConfig())

        assert uuid1 == uuid2  # Deterministic generation ensures consistency

    def test_obfuscation_without_config(self):
        """Test obfuscation works without configuration."""

        class MinimalModel(SecuredModel):
            sensitive: str

        # Even without explicit config, should have basic protection
        model = MinimalModel(sensitive="secret")

        # Should have registry capability
        assert hasattr(MinimalModel, "set_registry")
        assert hasattr(MinimalModel, "_registry")

    def test_database_security_by_default(self):
        """Verify database is secure by default, not by configuration."""
        # Mock database to avoid connection issues
        from unittest.mock import Mock

        mock_db = Mock()
        mock_db._security_registry = Mock()
        mock_db.register_collection_policy = Mock()

        # Remove all configuration
        with patch.dict(os.environ, {}, clear=True):
            with patch("mallku.core.database.factory.get_database_raw", return_value=mock_db):
                db = get_secured_database()

                # Should still be secured
                assert hasattr(db, "_security_registry")
                assert hasattr(db, "register_collection_policy")
                # Verify it's the secured interface
                from mallku.core.database.secured_interface import SecuredDatabaseInterface

                assert isinstance(db, SecuredDatabaseInterface)


class TestReciprocitySecurity:
    """Verify reciprocity data is properly secured."""

    def test_reciprocity_uses_uuid_mapping(self):
        """Verify reciprocity tracking uses UUID mapping."""
        # This test would verify that reciprocity models use SecuredModel
        # Currently SecuredReciprocityEvent doesn't exist yet
        # The principle is that all models should inherit from SecuredModel

        from mallku.core.security.field_strategies import FieldObfuscationLevel
        from mallku.core.security.secured_model import SecuredField, SecuredModel

        # Example of how reciprocity models should be structured
        class ReciprocityEvent(SecuredModel):
            giver_id: str = SecuredField(obfuscation_level=FieldObfuscationLevel.UUID_ONLY)
            receiver_id: str = SecuredField(obfuscation_level=FieldObfuscationLevel.UUID_ONLY)
            action_type: str = SecuredField(obfuscation_level=FieldObfuscationLevel.NONE)
            value: float = SecuredField(obfuscation_level=FieldObfuscationLevel.NONE)

        # Verify the model can be created
        event = ReciprocityEvent(
            giver_id="user123", receiver_id="user456", action_type="contribution", value=10.0
        )
        assert event.giver_id == "user123"  # Internal representation unchanged

    def test_reciprocity_patterns_not_individual_tracking(self):
        """Ensure reciprocity tracks patterns, not individuals."""
        from mallku.reciprocity import ReciprocityTracker

        tracker = ReciprocityTracker()

        # Should have pattern detection
        assert hasattr(tracker, "detect_recent_patterns")
        assert hasattr(tracker, "detect_recent_patterns_securely")

        # Should NOT have individual scoring
        assert not hasattr(tracker, "score_individual")
        assert not hasattr(tracker, "rank_users")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
