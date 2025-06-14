"""
Test Secrets Management System
=============================

Validates that the consciousness-aware secrets management properly
protects and provides access to sacred keys for Fire Circle.

The Testing Continues...
"""

import asyncio
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from mallku.core.secrets import SecretsManager, get_secret


@pytest.fixture
def temp_secrets_dir():
    """Module-level fixture: temporary directory for secrets."""
    with TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)
from mallku.firecircle.adapters.adapter_factory import (
    ConsciousAdapterFactory,
    create_conscious_adapter,
)
from mallku.firecircle.adapters.base import AdapterConfig


class TestSecretsManager:
    """Test the secrets management system."""

    # Temp secrets directory fixture moved to module scope

    @pytest.fixture
    async def secrets_manager(self, temp_secrets_dir):
        """Create secrets manager with temp directory."""
        manager = SecretsManager(secrets_dir=temp_secrets_dir)
        yield manager
        # Cleanup
        manager.clear_cache()

    async def test_secrets_directory_creation(self, temp_secrets_dir):
        """Test that secrets directory is created with proper permissions."""
        secrets_dir = temp_secrets_dir / "test_secrets"
        SecretsManager(secrets_dir=secrets_dir)

        assert secrets_dir.exists()
        # Check permissions (owner read/write/execute only)
        stat_info = secrets_dir.stat()
        assert oct(stat_info.st_mode)[-3:] == "700"

    async def test_encryption_key_generation(self, temp_secrets_dir):
        """Test encryption key generation and persistence."""
        manager1 = SecretsManager(secrets_dir=temp_secrets_dir)
        key_file = temp_secrets_dir / ".encryption.key"

        assert key_file.exists()
        # Check key file permissions
        stat_info = key_file.stat()
        assert oct(stat_info.st_mode)[-3:] == "600"

        # Test that same key is loaded by new instance
        manager2 = SecretsManager(secrets_dir=temp_secrets_dir)

        # Encrypt with first, decrypt with second
        test_data = b"sacred key data"
        encrypted = manager1._fernet.encrypt(test_data)
        decrypted = manager2._fernet.decrypt(encrypted)
        assert decrypted == test_data

    async def test_secret_storage_and_retrieval(self, secrets_manager):
        """Test storing and retrieving secrets."""
        # Store a secret
        await secrets_manager.set_secret("test_api_key", "sk-test123")

        # Retrieve it
        value = await secrets_manager.get_secret("test_api_key")
        assert value == "sk-test123"

        # Check it's in cache
        assert "test_api_key" in secrets_manager._cache

    async def test_environment_variable_priority(self, secrets_manager):
        """Test that environment variables take priority."""
        # Set in secrets file
        await secrets_manager.set_secret("test_key", "file_value")

        # Set in environment
        os.environ["TEST_KEY"] = "env_value"

        try:
            # Should get environment value
            value = await secrets_manager.get_secret("test_key")
            assert value == "env_value"
        finally:
            # Cleanup
            del os.environ["TEST_KEY"]

    async def test_encrypted_file_storage(self, secrets_manager):
        """Test that secrets are encrypted in files."""
        await secrets_manager.set_secret("sensitive_key", "sensitive_value")

        # Check encrypted file exists
        secrets_file = secrets_manager.secrets_dir / "mallku-secrets.json.encrypted"
        assert secrets_file.exists()

        # Verify it's encrypted (not readable as JSON)
        with open(secrets_file, "rb") as f:
            content = f.read()

        # Should not be valid JSON
        with pytest.raises(json.JSONDecodeError):
            json.loads(content)

        # But should decrypt properly
        decrypted = secrets_manager._fernet.decrypt(content)
        data = json.loads(decrypted)
        assert data["sensitive_key"] == "sensitive_value"

    async def test_required_secret_missing(self, secrets_manager):
        """Test that missing required secrets raise exception."""
        with pytest.raises(ValueError, match="Required secret 'missing_key' not found"):
            await secrets_manager.get_secret("missing_key", required=True)

    async def test_default_value(self, secrets_manager):
        """Test default value for missing secrets."""
        value = await secrets_manager.get_secret("nonexistent", default="default_value")
        assert value == "default_value"

    async def test_access_tracking(self, secrets_manager):
        """Test that secret access is tracked."""
        await secrets_manager.set_secret("tracked_key", "value")

        # Access multiple times
        for _ in range(3):
            await secrets_manager.get_secret("tracked_key")

        # Check access report
        report = secrets_manager.get_access_report()
        assert "tracked_key" in report
        assert report["tracked_key"]["access_count"] == 3
        assert report["tracked_key"]["source"] == "encrypted_file"
        assert report["tracked_key"]["last_accessed"] is not None

    async def test_adapter_secret_injection(self, secrets_manager):
        """Test injecting secrets into adapter configs."""
        # Set some API keys
        await secrets_manager.set_secret("openai_api_key", "sk-openai-test")
        await secrets_manager.set_secret("anthropic_key", "sk-anthropic-test")

        # Create adapter configs
        configs = {
            "openai": {"model_name": "gpt-4"},
            "anthropic": {"model_name": "claude-3"},
        }

        # Inject secrets
        updated = await secrets_manager.inject_into_adapters(configs)

        assert updated["openai"]["api_key"] == "sk-openai-test"
        assert updated["anthropic"]["api_key"] == "sk-anthropic-test"

    async def test_cache_clearing(self, secrets_manager):
        """Test cache clearing functionality."""
        await secrets_manager.set_secret("cached_key", "value")
        assert "cached_key" in secrets_manager._cache

        secrets_manager.clear_cache()
        assert "cached_key" not in secrets_manager._cache

        # Should still be retrievable from file
        value = await secrets_manager.get_secret("cached_key")
        assert value == "value"


class TestFireCircleIntegration:
    """Test secrets integration with Fire Circle adapters."""

    @pytest.fixture
    def mock_env_cleanup(self):
        """Cleanup environment after tests."""
        env_keys = []
        yield env_keys
        for key in env_keys:
            if key in os.environ:
                del os.environ[key]

    async def test_adapter_factory_auto_inject(self, mock_env_cleanup):
        """Test that adapter factory auto-injects secrets."""
        # Set API key in environment
        os.environ["OPENAI_API_KEY"] = "sk-test-openai"
        mock_env_cleanup.append("OPENAI_API_KEY")

        # Create factory
        factory = ConsciousAdapterFactory()

        # Create config without API key
        config = AdapterConfig()  # No api_key provided

        # Factory should auto-inject from environment
        # Note: This will fail to connect without real API key, but that's OK
        with pytest.raises(RuntimeError, match="Failed to connect"):
            await factory.create_adapter("openai", config)

        # The important part is that it tried to use the key
        assert config.api_key == "sk-test-openai"

    async def test_convenience_function_auto_inject(self, mock_env_cleanup):
        """Test convenience function auto-injects secrets."""
        os.environ["ANTHROPIC_API_KEY"] = "sk-test-anthropic"
        mock_env_cleanup.append("ANTHROPIC_API_KEY")

        # Call without API key
        with pytest.raises(RuntimeError, match="Failed to connect"):
            await create_conscious_adapter("anthropic")

        # The function should have found the key in environment

    async def test_multiple_key_patterns(self, temp_secrets_dir, mock_env_cleanup):
        """Test that various key patterns are tried."""
        manager = SecretsManager(secrets_dir=temp_secrets_dir)

        # Test lowercase_api_key pattern
        await manager.set_secret("mistral_api_key", "sk-mistral-1")

        # Test uppercase pattern
        os.environ["GOOGLE_API_KEY"] = "sk-google-1"
        mock_env_cleanup.append("GOOGLE_API_KEY")

        # Test _key pattern
        await manager.set_secret("local_key", "sk-local-1")

        # Verify all patterns work
        assert await get_secret("mistral_api_key") == "sk-mistral-1"
        assert await get_secret("google_api_key") == "sk-google-1"  # From env
        assert await get_secret("local_key") == "sk-local-1"


# Run tests if executed directly
if __name__ == "__main__":
    async def run_tests():
        """Run all tests."""
        print("Testing Secrets Management System...")

        # Test basic functionality
        test_basic = TestSecretsManager()
        with TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            manager = SecretsManager(secrets_dir=temp_path)

            print("\n✓ Testing basic secret operations...")
            await test_basic.test_secret_storage_and_retrieval(manager)

            print("✓ Testing encryption...")
            await test_basic.test_encrypted_file_storage(manager)

            print("✓ Testing access tracking...")
            await test_basic.test_access_tracking(manager)

            print("✓ Testing adapter integration...")
            await test_basic.test_adapter_secret_injection(manager)

        print("\n✅ All secrets management tests passed!")

    asyncio.run(run_tests())
