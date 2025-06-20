"""
Memory Anchor Data Model

Defines the core MemoryAnchor model that represents a point in time
where multiple activity cursors converge, creating a shared context
for cross-source correlation and reciprocity tracking.
"""

from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class MemoryAnchor(BaseModel):
    """
    A Memory Anchor represents a synchronized point across multiple activity streams.

    Memory Anchors enable:
    - Cross-source temporal correlation
    - Context preservation across sessions
    - Reciprocity tracking over time
    - Distributed activity coordination

    Each anchor contains cursor positions from various data sources at a specific
    moment, creating a shared reference point for understanding relationships
    between disparate activities.
    """

    # Core identification
    anchor_id: UUID = Field(..., description="Unique identifier for this memory anchor")

    timestamp: datetime = Field(..., description="When this anchor was created (timezone-aware)")

    # Relationship to other anchors
    predecessor_id: UUID | None = Field(None, description="ID of the previous anchor in the chain")

    # Cursor state from various providers
    cursors: dict[str, Any] = Field(
        default_factory=dict, description="Current cursor positions from all registered providers"
    )

    # Metadata and context
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional context and provider information"
    )

    # Last update tracking
    last_updated: datetime | None = Field(None, description="When this anchor was last modified")

    class Config:
        """Model configuration."""

        json_encoders = {datetime: lambda v: v.isoformat(), UUID: lambda v: str(v)}

        json_schema_extra = {
            "example": {
                "anchor_id": "550e8400-e29b-41d4-a716-446655440000",
                "timestamp": "2024-01-15T10:30:00Z",
                "predecessor_id": "550e8400-e29b-41d4-a716-446655440001",
                "cursors": {
                    "temporal": "2024-01-15T10:30:00Z",
                    "spatial": {"latitude": 49.2827, "longitude": -123.1207},
                    "filesystem": "/Users/alice/Documents/project.md",
                    "email": "msg-id-12345",
                    "spotify": "track:4iV5W9uYEdYUVa79Axb7Rh",
                },
                "metadata": {
                    "providers": ["filesystem", "email", "spotify"],
                    "creation_trigger": "temporal_threshold",
                    "confidence": 0.85,
                },
                "last_updated": "2024-01-15T10:35:00Z",
            }
        }

    def add_cursor(self, cursor_type: str, cursor_value: Any) -> None:
        """
        Add or update a cursor value for this anchor.

        Args:
            cursor_type: Type of cursor (e.g., 'temporal', 'spatial', 'filesystem')
            cursor_value: The cursor position value
        """
        self.cursors[cursor_type] = cursor_value
        self.last_updated = datetime.now(UTC)

    def get_cursor(self, cursor_type: str) -> Any:
        """
        Get a cursor value by type.

        Args:
            cursor_type: Type of cursor to retrieve

        Returns:
            The cursor value, or None if not found
        """
        return self.cursors.get(cursor_type)

    def has_cursor(self, cursor_type: str) -> bool:
        """
        Check if this anchor has a cursor of the given type.

        Args:
            cursor_type: Type of cursor to check

        Returns:
            True if the cursor exists, False otherwise
        """
        return cursor_type in self.cursors

    def get_provider_list(self) -> list[str]:
        """
        Get list of providers that have contributed cursors to this anchor.

        Returns:
            List of provider names
        """
        return self.metadata.get("providers", [])

    def add_provider(self, provider_name: str) -> None:
        """
        Add a provider to the metadata.

        Args:
            provider_name: Name of the provider to add
        """
        providers = set(self.get_provider_list())
        providers.add(provider_name)
        self.metadata["providers"] = list(providers)

    def to_arangodb_document(self) -> dict[str, Any]:
        """
        Convert to ArangoDB document format.

        Returns:
            Dictionary suitable for ArangoDB storage
        """
        doc = self.dict()
        doc["_key"] = str(self.anchor_id)

        # Ensure timestamps are ISO format strings
        if isinstance(doc["timestamp"], datetime):
            doc["timestamp"] = doc["timestamp"].isoformat()

        if doc.get("last_updated") and isinstance(doc["last_updated"], datetime):
            doc["last_updated"] = doc["last_updated"].isoformat()

        # Convert UUIDs to strings
        if doc.get("predecessor_id"):
            doc["predecessor_id"] = str(doc["predecessor_id"])

        # Ensure anchor_id is also a string for ArangoDB
        doc["anchor_id"] = str(doc["anchor_id"])

        return doc

    @classmethod
    def from_arangodb_document(cls, doc: dict[str, Any]) -> "MemoryAnchor":
        """
        Create MemoryAnchor from ArangoDB document.

        Args:
            doc: ArangoDB document dictionary

        Returns:
            MemoryAnchor instance
        """
        # Handle _key to anchor_id mapping
        if "_key" in doc and "anchor_id" not in doc:
            doc["anchor_id"] = doc["_key"]

        # Convert string UUIDs back to UUID objects
        if "anchor_id" in doc and isinstance(doc["anchor_id"], str):
            doc["anchor_id"] = UUID(doc["anchor_id"])

        if (
            "predecessor_id" in doc
            and doc["predecessor_id"]
            and isinstance(doc["predecessor_id"], str)
        ):
            doc["predecessor_id"] = UUID(doc["predecessor_id"])

        # Convert ISO timestamp strings back to datetime objects
        if "timestamp" in doc and isinstance(doc["timestamp"], str):
            doc["timestamp"] = datetime.fromisoformat(doc["timestamp"].replace("Z", "+00:00"))

        if "last_updated" in doc and doc["last_updated"] and isinstance(doc["last_updated"], str):
            doc["last_updated"] = datetime.fromisoformat(doc["last_updated"].replace("Z", "+00:00"))

        return cls(**doc)
