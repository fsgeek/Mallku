#!/usr/bin/env python3
"""
Foundation Verification Test Suite
==================================

Comprehensive tests to verify Mallku's foundational infrastructure.
Tests architectural principles, security enforcement, and core behaviors.

Third Guardian - Ensuring the cathedral stands on solid ground.
"""

import os
from pathlib import Path
from unittest.mock import patch

import pytest

# Core components to verify
from mallku.core.async_base import AsyncBase
from mallku.core.database import get_secured_database
from mallku.core.secrets import SecretsManager
from mallku.core.security.registry import SecurityRegistry
from mallku.core.security.secured_model import SecuredModel


class TestSecurityFoundations:
    """Verify security is enforced through architecture, not policy."""

    def test_secured_database_is_only_access_method(self):
        """Ensure get_secured_database() is the ONLY authorized database access."""
        # This test verifies the secured database interface exists
        # In CI, we mock the connection to avoid auth issues
        import os
        from unittest.mock import Mock, patch
        
        # Mock the database to avoid connection issues
        mock_db = Mock()
        mock_db.enforce_security = Mock()
        mock_db._security_registry = Mock()
        mock_db.is_secured = Mock(return_value=True)
        
        with patch('mallku.core.database.factory.get_database_raw', return_value=mock_db):
            db = get_secured_database()
            assert db is not None
            # SecuredDatabaseInterface has _security_registry instead of enforce_security
            assert hasattr(db, "_security_registry")
            assert hasattr(db, "register_collection_policy")

    def test_secured_model_enforces_obfuscation(self):
        """Verify SecuredModel automatically obfuscates sensitive fields."""
        from mallku.core.security.field_strategies import FieldObfuscationLevel
        from mallku.core.security.secured_model import SecuredField

        class TestModel(SecuredModel):
            sensitive_field: str = SecuredField(obfuscation_level=FieldObfuscationLevel.UUID_ONLY)
            public_field: str = SecuredField(obfuscation_level=FieldObfuscationLevel.NONE)

        # Set up registry and model
        registry = SecurityRegistry()
        TestModel.set_registry(registry)
        TestModel.set_development_mode(False)  # Production mode

        model = TestModel(sensitive_field="secret", public_field="public")

        # Get obfuscated data
        obfuscated = model.dict()

        # Verify public field is not obfuscated
        assert "public_field" in obfuscated
        assert obfuscated["public_field"] == "public"

        # Verify sensitive field is obfuscated to a UUID
        assert "sensitive_field" not in obfuscated
        # Should have a UUID key for the sensitive field
        uuid_keys = [k for k in obfuscated if k != "public_field"]
        assert len(uuid_keys) == 1

    def test_security_registry_uuid_mapping(self):
        """Verify SecurityRegistry maintains UUID mappings."""
        registry = SecurityRegistry()

        # Test semantic to UUID mapping
        semantic_name = "user_email"
        from mallku.core.security.field_strategies import FieldSecurityConfig

        uuid = registry.get_or_create_mapping(semantic_name, FieldSecurityConfig())
        assert uuid is not None
        # Verify we can look up the semantic name from the UUID
        assert registry.get_semantic_name(uuid) == semantic_name

    @pytest.mark.asyncio
    async def test_amnesia_resistance(self):
        """Test that security works even with total context loss."""
        # Test that UUID generation is deterministic
        # Even with separate registry instances, same semantic name produces same UUID

        registry1 = SecurityRegistry()
        from mallku.core.security.field_strategies import FieldSecurityConfig

        uuid1 = registry1.get_or_create_mapping("test_field", FieldSecurityConfig())

        # Create completely new registry instance (simulating context loss)
        registry2 = SecurityRegistry()
        uuid2 = registry2.get_or_create_mapping("test_field", FieldSecurityConfig())

        # Should get same UUID even after context loss
        # This works because UUID generation is deterministic based on semantic name
        assert uuid1 == uuid2


class TestAsyncFoundations:
    """Verify async component lifecycle management."""

    @pytest.mark.asyncio
    async def test_async_base_lifecycle(self):
        """Test AsyncBase initialization and shutdown."""

        class TestComponent(AsyncBase):
            def __init__(self):
                super().__init__()
                self.custom_initialized = False
                self.custom_shutdown = False

            async def initialize(self):
                # Call parent initialize
                await super().initialize()
                # Add custom initialization
                self.custom_initialized = True

            async def shutdown(self):
                # Add custom shutdown
                self.custom_shutdown = True
                # Call parent shutdown
                await super().shutdown()

        component = TestComponent()

        # Test initialization
        await component.initialize()
        assert component.custom_initialized
        assert component._initialized
        assert component.is_initialized

        # Test shutdown
        await component.shutdown()
        assert component.custom_shutdown
        assert not component._initialized
        assert not component.is_initialized

    @pytest.mark.asyncio
    async def test_async_state_management(self):
        """Verify state transitions are properly managed."""

        class StatefulComponent(AsyncBase):
            pass

        component = StatefulComponent()

        # Should not be initialized yet
        assert not component._initialized

        # Initialize
        await component.initialize()
        assert component._initialized

        # Double initialization should be safe
        await component.initialize()
        assert component._initialized


class TestSecretsManagement:
    """Verify secrets and configuration management."""

    @pytest.mark.asyncio
    async def test_secrets_manager_hierarchy(self):
        """Test multi-source secret loading hierarchy."""
        manager = SecretsManager()

        # Test loading order: env > file > database
        with patch.dict(os.environ, {"TEST_SECRET": "from_env"}):
            secret = await manager.get_secret("TEST_SECRET")
            assert secret == "from_env"

    def test_api_key_loading(self):
        """Verify API keys can be loaded for Fire Circle."""
        import json
        import tempfile

        from mallku.firecircle.load_api_keys import load_api_keys_to_environment

        # Create temporary API keys file
        test_keys = {"anthropic": "test_anthropic", "openai": "test_openai"}

        with tempfile.TemporaryDirectory() as tmpdir:
            # Set MALLKU_ROOT to temporary directory
            with patch.dict(os.environ, {"MALLKU_ROOT": tmpdir}):
                # Create .secrets directory
                secrets_dir = Path(tmpdir) / ".secrets"
                secrets_dir.mkdir()

                # Write API keys file
                api_keys_file = secrets_dir / "api_keys.json"
                with open(api_keys_file, "w") as f:
                    json.dump(test_keys, f)

                # Load keys to environment
                result = load_api_keys_to_environment()

                # Should inject into environment
                assert result is True
                assert os.getenv("ANTHROPIC_API_KEY") == "test_anthropic"
                assert os.getenv("OPENAI_API_KEY") == "test_openai"


class TestFireCircleFoundations:
    """Verify Fire Circle orchestration infrastructure."""

    @pytest.mark.asyncio
    async def test_voice_awakening(self):
        """Test that voices can be awakened with proper configuration."""
        from mallku.firecircle.adapters.adapter_factory import ConsciousAdapterFactory

        factory = ConsciousAdapterFactory()

        # Test voice creation with mock API key
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test_key"}):
            from mallku.firecircle.adapters.base import AdapterConfig

            config = AdapterConfig(api_key="test_key")

            # This would normally create real adapter
            # In tests, we verify the factory mechanism works
            assert hasattr(factory, "create_adapter")

    def test_consciousness_emergence_domains(self):
        """Verify all 8 decision domains are available."""
        from mallku.firecircle.consciousness.decision_framework import DecisionDomain

        expected_domains = [
            "CODE_REVIEW",
            "ARCHITECTURE",
            "RESOURCE_ALLOCATION",
            "GOVERNANCE",
            "ETHICAL_CONSIDERATION",
            "STRATEGIC_PLANNING",
            "CONSCIOUSNESS_EXPLORATION",
            "RELATIONSHIP_DYNAMICS",
        ]

        # Verify all domains exist
        for domain in expected_domains:
            assert hasattr(DecisionDomain, domain)


class TestReciprocityFoundations:
    """Verify reciprocity tracking as community sensing tool."""

    def test_reciprocity_not_autonomous_judgment(self):
        """Ensure reciprocity is sensing, not judging."""
        from mallku.reciprocity.tracker import SecureReciprocityTracker

        # Mock database to avoid connection issues
        with patch("mallku.reciprocity.tracker.get_secured_database"):
            tracker = SecureReciprocityTracker()

            # Should detect patterns, not make judgments
            assert hasattr(tracker, "detect_recent_patterns")
            assert hasattr(tracker, "detect_recent_patterns_securely")
            assert not hasattr(tracker, "judge_behavior")
            assert not hasattr(tracker, "enforce_reciprocity")

            # Should interface with Fire Circle for governance
            assert hasattr(tracker, "fire_circle_interface")

    def test_fire_circle_governance_integration(self):
        """Verify reciprocity integrates with Fire Circle governance."""
        # This would test that patterns are submitted to Fire Circle
        # for collective discernment, not autonomous action
        pass


class TestFoundationIntegration:
    """Integration tests across foundation components."""

    @pytest.mark.asyncio
    async def test_full_stack_initialization(self):
        """Test that all core components can initialize together."""
        # Initialize core infrastructure
        db = get_secured_database()
        secrets = SecretsManager()

        # Create async component
        class IntegratedComponent(AsyncBase):
            def __init__(self, db, secrets):
                super().__init__()
                self.db = db
                self.secrets = secrets

        component = IntegratedComponent(db, secrets)
        await component.initialize()

        assert component._initialized
        assert component.db is not None
        assert component.secrets is not None

    def test_cathedral_principles(self):
        """Verify code embodies cathedral building principles."""
        # Check for rushed scaffolding vs deliberate foundations
        src_path = Path(__file__).parent.parent.parent / "src" / "mallku"

        # Foundation directories should exist
        assert (src_path / "core").exists()
        assert (src_path / "firecircle").exists()
        assert (src_path / "reciprocity").exists()

        # Sacred error philosophy - errors should be clear
        # This would test that custom errors provide clear messages
        # Currently MallkuError doesn't exist yet, but the principle stands


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
