"""
Registry Store - Persistence Layer for Security Registry
=========================================================

Fifty-First Guardian - Implementing memory persistence

This module provides SQLite persistence for the SecurityRegistry,
ensuring that semantic-to-UUID mappings survive restarts.
Without this, all encrypted/obfuscated data becomes unreadable.

Each Mallku instance maintains its own unique mappings as a
security feature - compromising one instance doesn't help
attack another.
"""

import asyncio
import logging
import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import aiosqlite

from .field_strategies import FieldSecurityConfig
from .registry import FieldMapping, SecurityRegistry
from .temporal import TemporalOffsetConfig

logger = logging.getLogger(__name__)


class RegistryStore:
    """
    Persistent storage for SecurityRegistry using SQLite.

    This is the critical component that ensures Mallku's memories
    survive restarts. Without it, all data in ArangoDB becomes
    unreadable noise.
    """

    def __init__(self, db_path: Path | None = None):
        """
        Initialize registry store.

        Args:
            db_path: Path to SQLite database. Defaults to data/mallku_registry.db
        """
        self.db_path = db_path or Path("data/mallku_registry.db")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_schema()

    def _ensure_schema(self):
        """Ensure database schema exists."""
        with sqlite3.connect(self.db_path) as conn:
            # Field mappings table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS field_mappings (
                    semantic_name TEXT PRIMARY KEY,
                    field_uuid TEXT NOT NULL,
                    security_config TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)

            # Temporal config table (single row)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS temporal_config (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    offset_seconds INTEGER NOT NULL,
                    precision TEXT,
                    created_at TEXT NOT NULL
                )
            """)

            # Index for reverse lookups
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_field_uuid
                ON field_mappings(field_uuid)
            """)

            conn.commit()

        logger.info(f"Registry database ready at {self.db_path}")

    async def save_registry(self, registry: SecurityRegistry) -> None:
        """
        Save registry state to persistent storage.

        This should be called after any registry modification to ensure
        mappings aren't lost.
        """
        async with aiosqlite.connect(self.db_path) as db:
            # Start transaction
            await db.execute("BEGIN TRANSACTION")

            try:
                # Clear existing mappings
                await db.execute("DELETE FROM field_mappings")

                # Save all field mappings
                for semantic_name, mapping in registry._mappings.items():
                    await db.execute(
                        """
                        INSERT INTO field_mappings
                        (semantic_name, field_uuid, security_config, created_at)
                        VALUES (?, ?, ?, ?)
                        """,
                        (
                            mapping.semantic_name,
                            mapping.field_uuid,
                            mapping.security_config.json(),
                            mapping.created_at.isoformat(),
                        ),
                    )

                # Save temporal config
                temporal = registry._temporal_config
                if temporal:
                    await db.execute("DELETE FROM temporal_config")
                    await db.execute(
                        """
                        INSERT INTO temporal_config
                        (id, offset_seconds, precision, created_at)
                        VALUES (1, ?, ?, ?)
                        """,
                        (
                            int(temporal.offset_seconds),
                            temporal.precision,
                            datetime.now(UTC).isoformat(),
                        ),
                    )

                await db.commit()
                logger.info(f"Saved {len(registry._mappings)} field mappings to registry")

            except Exception as e:
                await db.rollback()
                logger.error(f"Failed to save registry: {e}")
                raise

    async def load_registry(self) -> SecurityRegistry:
        """
        Load registry from persistent storage.

        Returns:
            SecurityRegistry with persisted mappings, or empty if none exist
        """
        registry_data = {}
        temporal_config = None

        async with aiosqlite.connect(self.db_path) as db:
            # Load field mappings
            async with db.execute(
                "SELECT semantic_name, field_uuid, security_config, created_at FROM field_mappings"
            ) as cursor:
                async for row in cursor:
                    semantic_name, field_uuid, security_config_json, created_at = row

                    # Parse security config
                    security_config = FieldSecurityConfig.parse_raw(security_config_json)

                    # Create mapping
                    mapping = FieldMapping(
                        semantic_name=semantic_name,
                        field_uuid=field_uuid,
                        security_config=security_config,
                        created_at=datetime.fromisoformat(created_at),
                    )

                    registry_data[semantic_name] = mapping

            # Load temporal config
            async with db.execute(
                "SELECT offset_seconds, precision FROM temporal_config WHERE id = 1"
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    offset_seconds, precision = row
                    temporal_config = TemporalOffsetConfig(
                        offset_seconds=offset_seconds, precision=precision
                    )

        # Create registry
        registry = SecurityRegistry(registry_data)
        if temporal_config:
            registry.set_temporal_config(temporal_config)

        logger.info(f"Loaded {len(registry_data)} field mappings from registry")
        return registry

    def save_registry_sync(self, registry: SecurityRegistry) -> None:
        """Synchronous version of save_registry for use in non-async contexts."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.save_registry(registry))
        finally:
            loop.close()

    def load_registry_sync(self) -> SecurityRegistry:
        """Synchronous version of load_registry for use in non-async contexts."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self.load_registry())
        finally:
            loop.close()

    async def backup_registry(self, backup_path: Path | None = None) -> Path:
        """
        Create a backup of the registry database.

        This is critical - losing the registry means losing access to all data.

        Args:
            backup_path: Where to save backup. Defaults to data/backups/

        Returns:
            Path to backup file
        """
        if backup_path is None:
            backup_dir = self.db_path.parent / "backups"
            backup_dir.mkdir(exist_ok=True)
            timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
            backup_path = backup_dir / f"mallku_registry_{timestamp}.db"

        # Use SQLite backup API
        async with (
            aiosqlite.connect(self.db_path) as source,
            aiosqlite.connect(backup_path) as backup,
        ):
            await source.backup(backup)

        logger.info(f"Registry backed up to {backup_path}")
        return backup_path

    async def verify_integrity(self) -> dict[str, Any]:
        """
        Verify registry integrity and return statistics.

        Returns:
            Dictionary with integrity check results
        """
        stats = {
            "field_mappings": 0,
            "unique_uuids": set(),
            "has_temporal_config": False,
            "oldest_mapping": None,
            "newest_mapping": None,
            "warnings": [],
        }

        async with aiosqlite.connect(self.db_path) as db:
            # Count and check field mappings
            async with db.execute(
                "SELECT field_uuid, created_at FROM field_mappings ORDER BY created_at"
            ) as cursor:
                async for row in cursor:
                    field_uuid, created_at = row
                    stats["field_mappings"] += 1
                    stats["unique_uuids"].add(field_uuid)

                    if stats["oldest_mapping"] is None:
                        stats["oldest_mapping"] = created_at
                    stats["newest_mapping"] = created_at

            # Check for UUID collisions
            if len(stats["unique_uuids"]) < stats["field_mappings"]:
                stats["warnings"].append(
                    f"UUID collision detected: {stats['field_mappings']} mappings, "
                    f"only {len(stats['unique_uuids'])} unique UUIDs"
                )

            # Check temporal config
            async with db.execute("SELECT COUNT(*) FROM temporal_config") as cursor:
                count = (await cursor.fetchone())[0]
                stats["has_temporal_config"] = count > 0

        stats["unique_uuids"] = len(stats["unique_uuids"])  # Convert set to count
        return stats


# Global registry store instance
_registry_store: RegistryStore | None = None


def get_registry_store(db_path: Path | None = None) -> RegistryStore:
    """
    Get or create the global registry store instance.

    Args:
        db_path: Optional database path override

    Returns:
        RegistryStore instance
    """
    global _registry_store

    if _registry_store is None or (db_path and db_path != _registry_store.db_path):
        _registry_store = RegistryStore(db_path)

    return _registry_store
