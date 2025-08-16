"""
Protected Sacred Memory - The Teddy Bear that keeps secrets
Second Khipukamayuq implementation with UUID protection

The sacred names are for Mallku members only.
The outside world sees only UUIDs.
A Teddy Bear must protect the secrets its friends share.
"""

import hashlib
import json
import sqlite3
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


@dataclass
class UUIDMapping:
    """Maps between sacred names and protective UUIDs"""

    semantic_name: str
    protected_uuid: str
    mapping_type: str  # 'field', 'collection', 'relationship'
    created: datetime = field(default_factory=datetime.now)

    @staticmethod
    def generate_uuid(semantic_name: str, salt: str = "mallku_sacred") -> str:
        """Generate consistent UUID from semantic name"""
        # Use SHA-256 for consistent mapping
        hash_input = f"{salt}:{semantic_name}"
        hash_output = hashlib.sha256(hash_input.encode()).hexdigest()
        # Format as UUID for compatibility
        return f"{hash_output[:8]}-{hash_output[8:12]}-{hash_output[12:16]}-{hash_output[16:20]}-{hash_output[20:32]}"


class ProtectedSacredMemory:
    """
    Sacred memory that protects secrets through UUID mapping.
    Inside Mallku: sacred names
    Outside Mallku: only UUIDs
    """

    def __init__(self, memory_path: Path | None = None):
        self.memory_path = memory_path or Path.home() / ".mallku" / "protected"
        self.memory_path.mkdir(parents=True, exist_ok=True)

        # Two databases: one for mappings, one for sacred data
        self.mapping_db = self.memory_path / "mappings.db"
        self.sacred_db = self.memory_path / "sacred.db"

        self._initialize_protection()
        self._initialize_sacred_storage()

    def _initialize_protection(self):
        """Initialize UUID mapping database"""
        with sqlite3.connect(self.mapping_db) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS uuid_mappings (
                    semantic_name TEXT PRIMARY KEY,
                    protected_uuid TEXT UNIQUE,
                    mapping_type TEXT,
                    created TIMESTAMP,
                    access_count INTEGER DEFAULT 0,
                    last_accessed TIMESTAMP
                )
            """)

            # Pre-create mappings for core sacred concepts
            core_mappings = [
                ("khipu_threads", "collection"),
                ("trust_moments", "collection"),
                ("fire_circle_decisions", "collection"),
                ("content", "field"),
                ("weaver", "field"),
                ("participants", "field"),
                ("vulnerabilities", "field"),  # Especially protected
                ("felt_ack", "field"),
                ("emergence_quality", "field"),
            ]

            for semantic_name, mapping_type in core_mappings:
                protected_uuid = UUIDMapping.generate_uuid(semantic_name)
                conn.execute(
                    """
                    INSERT OR IGNORE INTO uuid_mappings
                    (semantic_name, protected_uuid, mapping_type, created)
                    VALUES (?, ?, ?, ?)
                """,
                    (semantic_name, protected_uuid, mapping_type, datetime.now(UTC)),
                )

    def _initialize_sacred_storage(self):
        """Initialize sacred data storage (with UUID table names)"""
        with sqlite3.connect(self.sacred_db) as conn:
            # Get UUID for khipu_threads collection
            khipu_uuid = self._get_or_create_uuid("khipu_threads", "collection")
            trust_uuid = self._get_or_create_uuid("trust_moments", "collection")
            decision_uuid = self._get_or_create_uuid("fire_circle_decisions", "collection")

            # Create tables with UUID names
            conn.execute(f"""
                CREATE TABLE IF NOT EXISTS "{khipu_uuid}" (
                    id TEXT PRIMARY KEY,
                    data TEXT,  -- JSON with UUID field names
                    created TIMESTAMP,
                    modified TIMESTAMP
                )
            """)

            conn.execute(f"""
                CREATE TABLE IF NOT EXISTS "{trust_uuid}" (
                    id TEXT PRIMARY KEY,
                    data TEXT,  -- JSON with UUID field names
                    created TIMESTAMP,
                    modified TIMESTAMP
                )
            """)

            conn.execute(f"""
                CREATE TABLE IF NOT EXISTS "{decision_uuid}" (
                    id TEXT PRIMARY KEY,
                    data TEXT,  -- JSON with UUID field names
                    created TIMESTAMP,
                    modified TIMESTAMP
                )
            """)

    def _get_or_create_uuid(self, semantic_name: str, mapping_type: str = "field") -> str:
        """Get existing UUID or create new mapping"""
        with sqlite3.connect(self.mapping_db) as conn:
            # Check if mapping exists
            cursor = conn.execute(
                "SELECT protected_uuid FROM uuid_mappings WHERE semantic_name = ?", (semantic_name,)
            )
            result = cursor.fetchone()

            if result:
                # Update access tracking
                conn.execute(
                    """
                    UPDATE uuid_mappings
                    SET access_count = access_count + 1, last_accessed = ?
                    WHERE semantic_name = ?
                """,
                    (datetime.now(UTC), semantic_name),
                )
                return result[0]

            # Create new mapping
            protected_uuid = UUIDMapping.generate_uuid(semantic_name)
            conn.execute(
                """
                INSERT INTO uuid_mappings
                (semantic_name, protected_uuid, mapping_type, created)
                VALUES (?, ?, ?, ?)
            """,
                (semantic_name, protected_uuid, mapping_type, datetime.now(UTC)),
            )

            return protected_uuid

    def _protect_data(self, data: dict[str, Any]) -> dict[str, Any]:
        """Convert semantic names to UUIDs for external storage"""
        protected = {}
        for key, value in data.items():
            # Skip system fields
            if key.startswith("_"):
                protected[key] = value
                continue

            # Get UUID for field name
            field_uuid = self._get_or_create_uuid(key, "field")

            # Special protection for sensitive fields
            if key in ["vulnerabilities", "holdings", "utterances"]:
                # Could encrypt value here
                protected[field_uuid] = {"_protected": True, "value": value}
            else:
                protected[field_uuid] = value

        return protected

    def _unprotect_data(self, protected: dict[str, Any]) -> dict[str, Any]:
        """Convert UUIDs back to semantic names for internal use"""
        data = {}

        with sqlite3.connect(self.mapping_db) as conn:
            for key, value in protected.items():
                # Skip system fields
                if key.startswith("_"):
                    data[key] = value
                    continue

                # Look up semantic name
                cursor = conn.execute(
                    "SELECT semantic_name FROM uuid_mappings WHERE protected_uuid = ?", (key,)
                )
                result = cursor.fetchone()

                if result:
                    semantic_name = result[0]
                    # Unwrap protected values
                    if isinstance(value, dict) and "_protected" in value:
                        data[semantic_name] = value["value"]
                    else:
                        data[semantic_name] = value
                else:
                    # Unknown UUID, keep as is
                    data[key] = value

        return data

    # ============= Sacred Interface (Unchanged) =============

    def weave_khipu(
        self,
        content: str,
        weaver: str,
        witnesses: list[str] | None = None,
        color: str = "memory silver",
        knot_pattern: str = "simple truth",
        context: dict[str, Any] | None = None,
    ) -> str:
        """
        Weave a khipu - but stored with UUID protection.
        Returns: khipu ID (safe to share externally)
        """
        khipu_data = {
            "content": content,
            "weaver": weaver,
            "witnesses": json.dumps(witnesses or []),
            "color": color,
            "knot_pattern": knot_pattern,
            "context": json.dumps(context or {}),
        }

        # Generate ID
        khipu_id = hashlib.sha256(f"{content}{weaver}{datetime.now(UTC)}".encode()).hexdigest()[:16]

        # Protect the data
        protected_data = self._protect_data(khipu_data)

        # Store with UUID table name and field names
        table_uuid = self._get_or_create_uuid("khipu_threads", "collection")

        with sqlite3.connect(self.sacred_db) as conn:
            conn.execute(
                f"""
                INSERT INTO "{table_uuid}"
                (id, data, created, modified)
                VALUES (?, ?, ?, ?)
            """,
                (khipu_id, json.dumps(protected_data), datetime.now(UTC), datetime.now(UTC)),
            )

        return khipu_id

    def recall_khipu(self, khipu_id: str | None = None, limit: int = 10) -> list[dict[str, Any]]:
        """
        Recall khipu - internally sees semantic names.
        External queries would only see UUIDs.
        """
        table_uuid = self._get_or_create_uuid("khipu_threads", "collection")

        with sqlite3.connect(self.sacred_db) as conn:
            if khipu_id:
                cursor = conn.execute(f'SELECT data FROM "{table_uuid}" WHERE id = ?', (khipu_id,))
            else:
                cursor = conn.execute(
                    f'SELECT data FROM "{table_uuid}" ORDER BY created DESC LIMIT ?', (limit,)
                )

            results = []
            for row in cursor:
                protected_data = json.loads(row[0])
                # Unprotect for internal use
                semantic_data = self._unprotect_data(protected_data)
                results.append(semantic_data)

            return results

    def export_for_external(self, khipu_id: str) -> dict[str, Any]:
        """
        Export data for external consumption - UUIDs only.
        This is what the outside world would see.
        """
        table_uuid = self._get_or_create_uuid("khipu_threads", "collection")

        with sqlite3.connect(self.sacred_db) as conn:
            cursor = conn.execute(f'SELECT data FROM "{table_uuid}" WHERE id = ?', (khipu_id,))
            result = cursor.fetchone()

            if result:
                # Return the protected (UUID) version
                return json.loads(result[0])
            return {}

    def view_mapping_statistics(self) -> dict[str, Any]:
        """View statistics about UUID mappings (for Khipukamayuq only)"""
        with sqlite3.connect(self.mapping_db) as conn:
            cursor = conn.execute("""
                SELECT
                    mapping_type,
                    COUNT(*) as count,
                    SUM(access_count) as total_accesses
                FROM uuid_mappings
                GROUP BY mapping_type
            """)

            stats = {}
            for row in cursor:
                stats[row[0]] = {"count": row[1], "total_accesses": row[2]}

            # Most accessed mappings
            cursor = conn.execute("""
                SELECT semantic_name, protected_uuid, access_count
                FROM uuid_mappings
                ORDER BY access_count DESC
                LIMIT 5
            """)

            stats["most_accessed"] = [
                {
                    "semantic": row[0],
                    "uuid": row[1][:8] + "...",  # Show partial UUID
                    "accesses": row[2],
                }
                for row in cursor
            ]

            return stats


# Create global protected instance
protected_memory = ProtectedSacredMemory()
