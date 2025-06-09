"""
Secrets Management for Mallku
============================

A consciousness-aware secrets management system that treats API keys and
sensitive data as sacred keys - handled with respect and protection.

This module provides multi-source secret loading, encryption at rest,
and secure injection into Fire Circle adapters. It embodies reciprocity
by protecting the keys that enable AI participation in governance.

Philosophy:
- Secrets are sacred keys that unlock consciousness dialogues
- Protection is reciprocity - we guard what enables connection
- Access requires responsibility - logging and auditing included
- Multiple sources honor diversity while maintaining security

The Cathedral Continues...
"""

import json
import logging
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from cryptography.fernet import Fernet

from .database import get_secured_database
from .security.field_strategies import FieldObfuscationLevel
from .security.secured_model import SecuredField, SecuredModel

logger = logging.getLogger(__name__)


class SecretMetadata(SecuredModel):
    """Metadata about a stored secret for tracking and auditing."""

    key: str = SecuredField(
        obfuscation_level=FieldObfuscationLevel.UUID_ONLY,
        security_notes="Secret identifier"
    )
    source: str = SecuredField(
        default="unknown",
        security_notes="Where this secret came from"
    )
    last_accessed: datetime | None = SecuredField(
        default=None,
        security_notes="Track access patterns"
    )
    access_count: int = SecuredField(
        default=0,
        security_notes="How often this secret is used"
    )
    created_at: datetime = SecuredField(
        default_factory=lambda: datetime.now(UTC),
        security_notes="When secret was first stored"
    )


class SecretsManager:
    """
    Manages secrets from multiple sources with encryption and auditing.

    Sources hierarchy (first found wins):
    1. Environment variables (runtime override)
    2. Encrypted .secrets files (development)
    3. Secured database (production)
    4. Fire Circle consensus (future: collective governance)
    """

    def __init__(
        self,
        secrets_dir: Path | None = None,
        encryption_key: str | None = None,
    ):
        """
        Initialize secrets manager.

        Args:
            secrets_dir: Directory for .secrets files (default: ./.secrets)
            encryption_key: Fernet key for encryption (auto-generated if None)
        """
        self.secrets_dir = secrets_dir or Path("./.secrets")
        self.secrets_dir.mkdir(exist_ok=True, mode=0o700)  # Owner read/write/execute only

        # Initialize encryption
        self._init_encryption(encryption_key)

        # Cache for loaded secrets
        self._cache: dict[str, Any] = {}
        self._metadata: dict[str, SecretMetadata] = {}

        # Database connection (lazy loaded)
        self._db = None
        self._db_collection = None

        logger.info("Secrets manager initialized")

    def _init_encryption(self, encryption_key: str | None) -> None:
        """Initialize encryption with provided or generated key."""
        key_file = self.secrets_dir / ".encryption.key"

        if encryption_key:
            # Use provided key
            self._fernet = Fernet(encryption_key.encode() if isinstance(encryption_key, str) else encryption_key)
        elif key_file.exists():
            # Load existing key
            with open(key_file, "rb") as f:
                self._fernet = Fernet(f.read())
        else:
            # Generate new key
            key = Fernet.generate_key()
            self._fernet = Fernet(key)

            # Save key with restricted permissions
            with open(key_file, "wb") as f:
                f.write(key)
            key_file.chmod(0o600)  # Owner read/write only

            logger.info("Generated new encryption key")

    async def get_secret(
        self,
        key: str,
        default: Any = None,
        required: bool = False,
    ) -> Any:
        """
        Get a secret from available sources.

        Args:
            key: Secret key to retrieve
            default: Default value if not found
            required: Raise exception if not found

        Returns:
            Secret value or default

        Raises:
            ValueError: If required=True and secret not found
        """
        # Check cache first
        if key in self._cache:
            self._track_access(key)
            return self._cache[key]

        # Try sources in order
        value = None
        source = None

        # 1. Environment variables (highest priority)
        env_key = key.upper().replace(".", "_")
        if env_key in os.environ:
            value = os.environ[env_key]
            source = "environment"
            logger.debug(f"Found secret '{key}' in environment")

        # 2. Encrypted file
        if value is None:
            value = await self._load_from_file(key)
            if value is not None:
                source = "encrypted_file"

        # 3. Secured database
        if value is None:
            value = await self._load_from_database(key)
            if value is not None:
                source = "database"

        # Handle not found
        if value is None:
            if required:
                raise ValueError(f"Required secret '{key}' not found in any source")
            value = default
            source = "default"

        # Cache and track
        if value is not None:
            self._cache[key] = value
            self._track_access(key, source)

        return value

    async def set_secret(
        self,
        key: str,
        value: Any,
        source: str = "manual",
        persist: bool = True,
    ) -> None:
        """
        Set a secret value.

        Args:
            key: Secret key
            value: Secret value
            source: Source identifier for auditing
            persist: Whether to persist to storage
        """
        # Update cache
        self._cache[key] = value

        # Track metadata
        if key not in self._metadata:
            self._metadata[key] = SecretMetadata(
                key=key,
                source=source,
            )

        # Persist if requested
        if persist:
            await self._save_to_file(key, value)
            # Could also save to database here

        logger.info(f"Set secret '{key}' from source '{source}'")

    async def inject_into_adapters(
        self,
        adapter_configs: dict[str, dict[str, Any]],
    ) -> dict[str, dict[str, Any]]:
        """
        Inject API keys into Fire Circle adapter configurations.

        Args:
            adapter_configs: Dict of adapter name to config dict

        Returns:
            Updated configs with injected secrets
        """
        updated_configs = {}

        for adapter_name, config in adapter_configs.items():
            # Look for API key in various patterns
            api_key = None

            # Try adapter-specific key first
            for key_pattern in [
                f"{adapter_name}_api_key",
                f"{adapter_name}_key",
                f"{adapter_name.upper()}_API_KEY",
            ]:
                api_key = await self.get_secret(key_pattern)
                if api_key:
                    break

            # Update config if key found
            if api_key:
                config["api_key"] = api_key
                logger.info(f"Injected API key for {adapter_name} adapter")
            else:
                logger.warning(f"No API key found for {adapter_name} adapter")

            updated_configs[adapter_name] = config

        return updated_configs

    async def _load_from_file(self, key: str) -> Any | None:
        """Load secret from encrypted file."""
        # Try key-specific file first
        key_file = self.secrets_dir / f"{key}.secret"
        if key_file.exists():
            try:
                with open(key_file, "rb") as f:
                    encrypted = f.read()
                decrypted = self._fernet.decrypt(encrypted)
                return json.loads(decrypted)
            except Exception as e:
                logger.error(f"Failed to load secret from {key_file}: {e}")

        # Try consolidated secrets file
        secrets_file = self.secrets_dir / "mallku-secrets.json.encrypted"
        if secrets_file.exists():
            try:
                with open(secrets_file, "rb") as f:
                    encrypted = f.read()
                decrypted = self._fernet.decrypt(encrypted)
                all_secrets = json.loads(decrypted)
                return all_secrets.get(key)
            except Exception as e:
                logger.error(f"Failed to load secrets from {secrets_file}: {e}")

        return None

    async def _save_to_file(self, key: str, value: Any) -> None:
        """Save secret to encrypted file."""
        # Load existing secrets
        secrets_file = self.secrets_dir / "mallku-secrets.json.encrypted"
        all_secrets = {}

        if secrets_file.exists():
            try:
                with open(secrets_file, "rb") as f:
                    encrypted = f.read()
                decrypted = self._fernet.decrypt(encrypted)
                all_secrets = json.loads(decrypted)
            except Exception:
                pass  # Start fresh if decrypt fails

        # Update with new secret
        all_secrets[key] = value

        # Encrypt and save
        encrypted = self._fernet.encrypt(json.dumps(all_secrets).encode())
        with open(secrets_file, "wb") as f:
            f.write(encrypted)
        secrets_file.chmod(0o600)  # Owner read/write only

    async def _load_from_database(self, key: str) -> Any | None:
        """Load secret from secured database."""
        if not self._db:
            try:
                self._db = await get_secured_database()
                # This would need proper setup with security policies
                # For now, return None
            except Exception as e:
                logger.debug(f"Database not available for secrets: {e}")

        return None

    def _track_access(self, key: str, source: str | None = None) -> None:
        """Track secret access for auditing."""
        if key not in self._metadata:
            self._metadata[key] = SecretMetadata(
                key=key,
                source=source or "unknown",
            )

        metadata = self._metadata[key]
        metadata.last_accessed = datetime.now(UTC)
        metadata.access_count += 1

    def get_access_report(self) -> dict[str, dict[str, Any]]:
        """Get report of secret access patterns."""
        report = {}

        for key, metadata in self._metadata.items():
            report[key] = {
                "source": metadata.source,
                "access_count": metadata.access_count,
                "last_accessed": metadata.last_accessed.isoformat() if metadata.last_accessed else None,
                "created_at": metadata.created_at.isoformat(),
            }

        return report

    def clear_cache(self) -> None:
        """Clear the secrets cache (does not affect persistent storage)."""
        self._cache.clear()
        logger.info("Cleared secrets cache")


# Global instance for convenience
_manager = None


def get_secrets_manager() -> SecretsManager:
    """Get or create the global secrets manager."""
    global _manager
    if _manager is None:
        _manager = SecretsManager()
    return _manager


async def get_secret(key: str, default: Any = None, required: bool = False) -> Any:
    """
    Convenience function to get a secret.

    This creates a simple interface for the common case while allowing
    direct access to the manager for advanced usage.
    """
    manager = get_secrets_manager()
    return await manager.get_secret(key, default, required)


async def inject_adapter_secrets(adapter_configs: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """
    Convenience function to inject secrets into adapter configs.

    This is what Fire Circle adapters will call to get their API keys.
    """
    manager = get_secrets_manager()
    return await manager.inject_into_adapters(adapter_configs)
