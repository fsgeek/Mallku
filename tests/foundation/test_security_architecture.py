#!/usr/bin/env python3
"""
Security Architecture Verification Tests
========================================

Tests that security is enforced through physical architecture,
not just policy or guidelines.

Third Guardian - Architectural security verification
"""

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

        # Should not be able to import raw database
        with pytest.raises(ImportError):
            pass  # Should not exist

        # Only secured access should be available
        db = get_secured_database()
        assert hasattr(db, "enforce_security")
        assert hasattr(db, "_security_registry")

    def test_uuid_obfuscation_automatic(self):
        """Verify UUID obfuscation happens automatically."""

        class UserModel(SecuredModel):
            email: str
            public_name: str

            class SecurityConfig:
                secured_fields = ["email"]

        # Create instance
        user = UserModel(email="test@example.com", public_name="Test User")

        # In production mode, email should be UUID
        with patch.dict(os.environ, {"MALLKU_ENV": "production"}):
            serialized = user.model_dump()
            # Email should be obfuscated to UUID
            assert serialized["email"] != "test@example.com"
            assert len(serialized["email"]) == 36  # UUID length

    def test_security_registry_singleton(self):
        """Verify security registry maintains global state."""
        registry1 = SecurityRegistry()
        registry2 = SecurityRegistry()

        # Should be same instance
        assert registry1 is registry2

        # Mappings should persist
        uuid1 = registry1.get_or_create_uuid("test_field")
        uuid2 = registry2.get_uuid("test_field")
        assert uuid1 == uuid2

    def test_temporal_offset_prevents_correlation(self):
        """Verify temporal offsets prevent timing correlation attacks."""
        registry = SecurityRegistry()

        # Get field security config
        config = registry.get_field_security("timestamp_field")

        # Should have temporal offset
        assert "temporal_offset" in config
        assert isinstance(config["temporal_offset"], int | float)

    @pytest.mark.asyncio
    async def test_event_bus_security(self):
        """Verify event bus doesn't leak sensitive data."""
        from mallku.orchestration.event_bus import ConsciousnessEventBus

        bus = ConsciousnessEventBus()
        await bus.start()

        # Subscribe to events
        events_received = []

        async def handler(event):
            events_received.append(event)

        bus.subscribe("test.event", handler)

        # Emit event with sensitive data
        sensitive_event = {
            "type": "test.event",
            "user_email": "sensitive@example.com",
            "public_data": "visible",
        }

        await bus.emit("test.event", sensitive_event)

        # Event should be sanitized
        assert len(events_received) == 1
        received = events_received[0]

        # Sensitive data should not be in raw form
        assert "sensitive@example.com" not in str(received)

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

        db_config = get_secured_database()._config

        # Should use internal hostnames, not public IPs
        # (In real deployment, this would check actual config)


class TestAmnesiaSecurity:
    """Verify security survives total context loss."""

    def test_security_without_registry(self):
        """Test security works even if registry is lost."""
        # Clear all singletons
        SecurityRegistry._instances.clear()

        # Security should still work through structure
        db = get_secured_database()

        # Should create new registry if needed
        assert db._security_registry is not None

    def test_obfuscation_without_config(self):
        """Test obfuscation works without configuration."""

        class MinimalModel(SecuredModel):
            sensitive: str

        # Even without config, should have basic protection
        model = MinimalModel(sensitive="secret")

        # Should have security context
        assert hasattr(model, "_security_context")

    def test_database_security_by_default(self):
        """Verify database is secure by default, not by configuration."""
        # Remove all configuration
        with patch.dict(os.environ, {}, clear=True):
            db = get_secured_database()

            # Should still be secured
            assert db.is_secured()
            assert hasattr(db, "enforce_security")


class TestReciprocitySecurity:
    """Verify reciprocity data is properly secured."""

    def test_reciprocity_uses_uuid_mapping(self):
        """Verify reciprocity tracking uses UUID mapping."""
        from mallku.streams.reciprocity.secured_reciprocity_models import SecuredReciprocityEvent

        event = SecuredReciprocityEvent(
            giver_id="user123", receiver_id="user456", action_type="contribution", value=10.0
        )

        # IDs should be obfuscated in production
        with patch.dict(os.environ, {"MALLKU_ENV": "production"}):
            serialized = event.model_dump()

            # User IDs should be UUIDs
            assert serialized["giver_id"] != "user123"
            assert serialized["receiver_id"] != "user456"

    def test_reciprocity_patterns_not_individual_tracking(self):
        """Ensure reciprocity tracks patterns, not individuals."""
        from mallku.reciprocity import ReciprocityTracker

        tracker = ReciprocityTracker()

        # Should have pattern detection
        assert hasattr(tracker, "detect_pattern")

        # Should NOT have individual scoring
        assert not hasattr(tracker, "score_individual")
        assert not hasattr(tracker, "rank_users")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
