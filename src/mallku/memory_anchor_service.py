#!/usr/bin/env python3
"""
Memory Anchor Service - Minimal Prototype Implementation

This prototype validates the Memory Anchor Schema by implementing
basic anchor creation, storage, and retrieval using ArangoDB.

Purpose: Test whether the schema design actually works in practice.
"""

import hashlib
import json
import uuid
from datetime import UTC, datetime
from enum import Enum
from typing import Any

from arango import ArangoClient
from pydantic import BaseModel, Field


class AnchorType(str, Enum):
    """Types of memory anchors as defined in schema"""

    TEMPORAL = "temporal"
    CONTEXTUAL = "contextual"
    SEMANTIC = "semantic"
    SOCIAL = "social"
    CAUSAL = "causal"
    RITUAL = "ritual"


class TemporalPrecision(str, Enum):
    """Precision levels for temporal windows"""

    INSTANT = "instant"
    MINUTE = "minute"
    SESSION = "session"
    DAILY = "daily"
    CYCLICAL = "cyclical"


class TemporalWindow(BaseModel):
    """Time span associated with an anchor"""

    start_time: datetime
    end_time: datetime
    precision: TemporalPrecision


class SpatialContext(BaseModel):
    """Optional spatial binding for anchors"""

    coordinates: list[float] | None = None  # [lat, lon]
    location_name: str | None = None
    precision_radius: float | None = None  # meters


class MemoryAnchor(BaseModel):
    """Core memory anchor entity following the schema"""

    # Identity and lifecycle
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    last_accessed: datetime = Field(default_factory=lambda: datetime.now(UTC))
    last_reinforced: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # Classification and strength
    anchor_type: AnchorType
    strength: float = Field(ge=0.0, le=1.0, default=0.5)
    confidence: float = Field(ge=0.0, le=1.0, default=0.5)
    decay_rate: float = Field(ge=0.0, le=1.0, default=0.01)

    # Temporal and spatial binding
    temporal_window: TemporalWindow
    spatial_context: SpatialContext | None = None

    # Correlation data
    context_signature: str
    activity_streams: list[str] = Field(default_factory=list)
    storage_events: list[str] = Field(default_factory=list)

    # Utilitarian metrics
    access_frequency: int = 0
    correlation_accuracy: float = 0.0
    computational_cost: float = 0.0


class MemoryAnchorService:
    """
    Minimal service for creating, storing, and retrieving memory anchors.

    This prototype tests the schema against real ArangoDB operations.
    """

    def __init__(self, db_config: dict[str, Any]):
        """Initialize with database configuration"""
        self.client = ArangoClient(hosts=db_config.get("host", "http://localhost:8529"))
        self.db_name = db_config.get("database", "mallku")
        self.collection_name = "memory_anchors"
        self.edge_collection = "anchor_relationships"

        # Connect to database
        self.db = self.client.db(
            self.db_name, username=db_config.get("username"), password=db_config.get("password")
        )

        self._ensure_collections()

    def _ensure_collections(self):
        """Ensure required collections exist"""
        if not self.db.has_collection(self.collection_name):
            self.db.create_collection(self.collection_name)

        if not self.db.has_collection(self.edge_collection):
            self.db.create_collection(self.edge_collection, edge=True)

    def create_anchor(
        self,
        anchor_type: AnchorType,
        temporal_window: TemporalWindow,
        activity_streams: list[str],
        storage_events: list[str],
        spatial_context: SpatialContext | None = None,
        initial_strength: float = 0.5,
        initial_confidence: float = 0.5,
    ) -> MemoryAnchor:
        """
        Create a new memory anchor from correlation data.

        Tests: Can we instantiate anchors using the schema?
        """

        # Generate context signature from inputs
        context_data = {
            "temporal": temporal_window.dict(),
            "activities": sorted(activity_streams),
            "storage": sorted(storage_events),
            "spatial": spatial_context.dict() if spatial_context else None,
        }
        context_signature = hashlib.sha256(
            json.dumps(context_data, sort_keys=True).encode()
        ).hexdigest()

        # Create anchor instance
        anchor = MemoryAnchor(
            anchor_type=anchor_type,
            temporal_window=temporal_window,
            spatial_context=spatial_context,
            context_signature=context_signature,
            activity_streams=activity_streams,
            storage_events=storage_events,
            strength=initial_strength,
            confidence=initial_confidence,
        )

        return anchor

    def store_anchor(self, anchor: MemoryAnchor) -> bool:
        """
        Store memory anchor in ArangoDB.

        Tests: Does the schema work with ArangoDB storage?
        """
        try:
            collection = self.db.collection(self.collection_name)

            # Convert to dict for storage
            anchor_doc = anchor.dict()
            anchor_doc["_key"] = anchor.id

            # Store in database
            result = collection.insert(anchor_doc)
            return result is not None

        except Exception as e:
            print(f"Error storing anchor: {e}")
            return False

    def retrieve_anchor(self, anchor_id: str) -> MemoryAnchor | None:
        """
        Retrieve memory anchor by ID.

        Tests: Can we reconstruct anchors from storage?
        """
        try:
            collection = self.db.collection(self.collection_name)
            doc = collection.get(anchor_id)

            if doc:
                # Remove ArangoDB metadata
                doc.pop("_key", None)
                doc.pop("_id", None)
                doc.pop("_rev", None)

                return MemoryAnchor(**doc)

            return None

        except Exception as e:
            print(f"Error retrieving anchor: {e}")
            return None

    def find_anchors_by_timerange(
        self, start_time: datetime, end_time: datetime
    ) -> list[MemoryAnchor]:
        """
        Find anchors whose temporal windows overlap with given range.

        Tests: Can we query by temporal relationships?
        """
        try:
            self.db.collection(self.collection_name)

            # AQL query for temporal overlap
            query = """
            FOR anchor IN @@collection
                FILTER anchor.temporal_window.start_time <= @end_time
                   AND anchor.temporal_window.end_time >= @start_time
                RETURN anchor
            """

            cursor = self.db.aql.execute(
                query,
                bind_vars={
                    "@collection": self.collection_name,
                    "start_time": start_time.isoformat(),
                    "end_time": end_time.isoformat(),
                },
            )

            anchors = []
            for doc in cursor:
                # Remove ArangoDB metadata
                doc.pop("_key", None)
                doc.pop("_id", None)
                doc.pop("_rev", None)
                anchors.append(MemoryAnchor(**doc))

            return anchors

        except Exception as e:
            print(f"Error querying anchors: {e}")
            return []

    def create_relationship(
        self,
        from_anchor_id: str,
        to_anchor_id: str,
        relationship_type: str,
        weight: float = 1.0,
        metadata: dict | None = None,
    ) -> bool:
        """
        Create relationship between two anchors.

        Tests: Can we store and query relationships?
        """
        try:
            edge_collection = self.db.collection(self.edge_collection)

            edge_doc = {
                "_from": f"{self.collection_name}/{from_anchor_id}",
                "_to": f"{self.collection_name}/{to_anchor_id}",
                "relationship_type": relationship_type,
                "weight": weight,
                "created_at": datetime.now(UTC).isoformat(),
                "metadata": metadata or {},
            }

            result = edge_collection.insert(edge_doc)
            return result is not None

        except Exception as e:
            print(f"Error creating relationship: {e}")
            return False


def test_prototype():
    """
    Basic test of the memory anchor prototype.

    This will reveal if the schema works in practice.
    """

    # Mock database config - would normally load from config file
    db_config = {
        "host": "http://localhost:8529",
        "database": "mallku_test",
        "username": "mallku",
        "password": "test_password",
    }

    try:
        # Initialize service
        service = MemoryAnchorService(db_config)

        # Create test temporal window
        now = datetime.now(UTC)
        temporal_window = TemporalWindow(
            start_time=now, end_time=now, precision=TemporalPrecision.SESSION
        )

        # Create test anchor
        anchor = service.create_anchor(
            anchor_type=AnchorType.TEMPORAL,
            temporal_window=temporal_window,
            activity_streams=["calendar_event_123"],
            storage_events=["file_created_456"],
        )

        print(f"Created anchor: {anchor.id}")

        # Test storage
        stored = service.store_anchor(anchor)
        print(f"Storage successful: {stored}")

        if stored:
            # Test retrieval
            retrieved = service.retrieve_anchor(anchor.id)
            print(f"Retrieved anchor: {retrieved is not None}")

            # Test temporal query
            anchors = service.find_anchors_by_timerange(
                now - timedelta(minutes=5), now + timedelta(minutes=5)
            )
            print(f"Found {len(anchors)} anchors in time range")

    except Exception as e:
        print(f"Test failed: {e}")
        return False

    return True


if __name__ == "__main__":
    from datetime import timedelta

    print("Testing Memory Anchor Schema Implementation...")
    success = test_prototype()
    print(f"Test {'PASSED' if success else 'FAILED'}")
