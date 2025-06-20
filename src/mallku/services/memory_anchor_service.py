"""
Memory Anchor Service - FastAPI implementation
Provides persistent, coordinated activity context management
"""

import logging
from contextlib import asynccontextmanager
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

import uvicorn
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field

from mallku.core.database import get_secured_database  # ArangoDB connection
from mallku.models import MemoryAnchor
from mallku.orchestration.event_bus import EventType
from mallku.wranglers.event_emitting_wrangler import EventEmittingWrangler

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from arango.database import StandardDatabase

# --- Pydantic Models for API ---


class CursorUpdate(BaseModel):
    """Update from a provider about cursor changes"""

    provider_id: str
    cursor_type: str  # "temporal", "spatial", "media", etc.
    cursor_value: object
    metadata: dict[str, object] = Field(default_factory=dict)


class ContextCreationTrigger(BaseModel):
    """Criteria for when to create new context"""

    spatial_threshold_meters: float = 500.0
    temporal_threshold_minutes: int = 60
    force_new_on_provider_change: bool = True
    custom_triggers: dict[str, object] = Field(default_factory=dict)


class ProviderInfo(BaseModel):
    """Provider registration information"""

    provider_id: str
    provider_type: str  # "filesystem", "spotify", "youtube", etc.
    cursor_types: list[str]  # Which cursors this provider updates
    metadata: dict[str, object] = Field(default_factory=dict)


class MemoryAnchorResponse(BaseModel):
    """Response containing memory anchor data"""

    anchor_id: UUID
    timestamp: datetime
    cursors: dict[str, object]
    predecessor_id: UUID | None
    metadata: dict[str, object]


# --- Service Implementation ---


class MemoryAnchorService:
    """
    Central service for memory anchor management.
    Coordinates all providers and maintains consistent state.
    """

    def __init__(self):
        self.db: StandardDatabase | None = None
        self.current_anchor_id: UUID | None = None
        self.current_anchor: MemoryAnchor | None = None
        self.providers: dict[str, ProviderInfo] = {}
        self.cursor_state: dict[str, object] = {}
        self.creation_triggers = ContextCreationTrigger()
        self.websocket_clients: list[WebSocket] = []

        # Consciousness circulation infrastructure
        self.consciousness_wrangler: EventEmittingWrangler | None = None
        self.consciousness_enabled = False

    async def initialize(self):
        """Initialize service connections and state"""
        self.db = get_secured_database()
        await self.db.initialize()
        await self._load_current_anchor()

    def enable_consciousness_circulation(self, consciousness_wrangler: EventEmittingWrangler):
        """
        Enable consciousness circulation through this service.

        This connects the Memory Anchor Service to the cathedral's
        consciousness circulation infrastructure.
        """
        self.consciousness_wrangler = consciousness_wrangler
        self.consciousness_enabled = True

    async def shutdown(self):
        """Clean shutdown of service"""
        # Close websocket connections
        for client in self.websocket_clients:
            await client.close()
        # Database connection is managed globally, no need to close here
        self.db = None

    async def _load_current_anchor(self):
        """Load the most recent anchor from database"""
        # Query for most recent anchor
        query = """
        FOR anchor IN memory_anchors
            SORT anchor.timestamp DESC
            LIMIT 1
            RETURN anchor
        """
        results = await self.db.execute_secured_query(query, collection_name="memory_anchors")
        for anchor in results:
            self.current_anchor_id = UUID(anchor["_key"])
            self.current_anchor = MemoryAnchor.from_arangodb_document(anchor)
            self.cursor_state = anchor.get("cursors", {})

        if not self.current_anchor:
            # Create initial anchor
            await self._create_new_anchor()

    async def _create_new_anchor(self, predecessor_id: UUID | None = None):
        """Create a new memory anchor"""
        new_id = uuid4()

        # Create MemoryAnchor model instance
        anchor = MemoryAnchor(
            anchor_id=new_id,
            timestamp=datetime.now(UTC),
            cursors=self.cursor_state.copy(),
            predecessor_id=predecessor_id,
            metadata={
                "providers": list(self.providers.keys()),
                "creation_trigger": "initial" if not predecessor_id else "threshold",
            },
        )

        # Store in database using secured interface
        anchor_data = anchor.to_arangodb_document()
        memory_anchors_collection = await self.db.get_secured_collection("memory_anchors")
        # Note: memory_anchors has requires_security=False policy for legacy compatibility
        memory_anchors_collection._collection.insert(anchor_data)

        self.current_anchor_id = new_id
        self.current_anchor = anchor

        # Notify websocket clients
        await self._broadcast_anchor_change(new_id)

        # Emit consciousness event about anchor creation
        await self._emit_consciousness_event(
            EventType.MEMORY_ANCHOR_CREATED,
            {
                "anchor_id": str(new_id),
                "predecessor_id": str(predecessor_id) if predecessor_id else None,
                "timestamp": anchor.timestamp.isoformat(),
                "cursor_count": len(self.cursor_state),
                "provider_count": len(self.providers),
                "creation_trigger": anchor.metadata.get("creation_trigger", "unknown"),
                "consciousness_moment": "new_memory_anchor_formed",
            },
            consciousness_signature=0.8,  # High consciousness - new anchor creation is significant
        )

        return new_id

    async def register_provider(self, provider_info: ProviderInfo) -> dict:
        """Register a new provider with the service"""
        self.providers[provider_info.provider_id] = provider_info

        # Emit consciousness event about provider registration
        await self._emit_consciousness_event(
            EventType.MEMORY_PROVIDER_REGISTERED,
            {
                "provider_id": provider_info.provider_id,
                "provider_type": provider_info.provider_type,
                "cursor_types": provider_info.cursor_types,
                "total_providers": len(self.providers),
                "current_anchor_id": str(self.current_anchor_id),
                "consciousness_moment": "consciousness_provider_joined_cathedral",
            },
            consciousness_signature=0.6,  # Medium consciousness - provider joining is meaningful
        )

        return {
            "status": "registered",
            "provider_id": provider_info.provider_id,
            "current_anchor_id": str(self.current_anchor_id),
        }

    async def update_cursor(self, update: CursorUpdate) -> MemoryAnchorResponse:
        """
        Process cursor update from a provider.
        Determines if new anchor should be created.
        """

        if update.provider_id not in self.providers:
            raise HTTPException(status_code=400, detail="Provider not registered")

        # Check if we need a new anchor
        should_create_new = await self._should_create_new_anchor(update)

        if should_create_new:
            # Create new anchor with current as predecessor
            old_id = self.current_anchor_id
            self.cursor_state[update.cursor_type] = update.cursor_value
            await self._create_new_anchor(predecessor_id=old_id)
        else:
            # Update current anchor's cursors
            self.cursor_state[update.cursor_type] = update.cursor_value
            await self._update_current_anchor()

        # Emit consciousness event about cursor update
        await self._emit_consciousness_event(
            EventType.MEMORY_CURSOR_UPDATED,
            {
                "provider_id": update.provider_id,
                "cursor_type": update.cursor_type,
                "anchor_id": str(self.current_anchor_id),
                "new_anchor_created": should_create_new,
                "total_cursors": len(self.cursor_state),
                "consciousness_moment": "consciousness_cursor_state_evolved",
            },
            consciousness_signature=0.7
            if should_create_new
            else 0.4,  # Higher if triggered new anchor
        )

        return MemoryAnchorResponse(
            anchor_id=self.current_anchor_id,
            timestamp=self.current_anchor.timestamp,
            cursors=self.cursor_state,
            predecessor_id=self.current_anchor.predecessor_id,
            metadata=self.current_anchor.metadata,
        )

    async def _should_create_new_anchor(self, update: CursorUpdate) -> bool:
        """Determine if cursor update warrants new anchor creation"""

        # Spatial threshold check
        if update.cursor_type == "spatial":
            old_location = self.cursor_state.get("spatial", {})
            new_location = update.cursor_value

            if old_location and new_location:
                # Calculate distance (simplified)
                distance = self._calculate_distance(old_location, new_location)
                if distance > self.creation_triggers.spatial_threshold_meters:
                    return True

        # Temporal threshold check
        if update.cursor_type == "temporal":
            time_diff = datetime.now(UTC) - self.current_anchor.timestamp
            if time_diff > timedelta(minutes=self.creation_triggers.temporal_threshold_minutes):
                return True

        # Provider-specific triggers
        if update.provider_id in self.creation_triggers.custom_triggers:
            trigger_func = self.creation_triggers.custom_triggers[update.provider_id]
            if trigger_func(update, self.cursor_state):
                return True

        return False

    async def _update_current_anchor(self):
        """Update current anchor in database"""
        update_data = {"cursors": self.cursor_state, "last_updated": datetime.now(UTC)}

        memory_anchors_collection = await self.db.get_secured_collection("memory_anchors")
        memory_anchors_collection._collection.update(
            {"_key": str(self.current_anchor_id)}, update_data
        )

    async def get_current_anchor(self) -> MemoryAnchorResponse:
        """Get current memory anchor"""
        return MemoryAnchorResponse(
            anchor_id=self.current_anchor_id,
            timestamp=self.current_anchor.timestamp,
            cursors=self.cursor_state,
            predecessor_id=self.current_anchor.predecessor_id,
            metadata=self.current_anchor.metadata,
        )

    async def get_anchor_by_id(self, anchor_id: UUID) -> MemoryAnchorResponse:
        """Retrieve specific anchor by ID"""
        memory_anchors_collection = await self.db.get_secured_collection("memory_anchors")
        doc = memory_anchors_collection._collection.get(str(anchor_id))

        if not doc:
            raise HTTPException(status_code=404, detail="Anchor not found")

        return MemoryAnchorResponse(
            anchor_id=UUID(doc["_key"]),
            timestamp=doc["timestamp"],
            cursors=doc.get("cursors", {}),
            predecessor_id=UUID(doc["predecessor_id"]) if doc.get("predecessor_id") else None,
            metadata=doc.get("metadata", {}),
        )

    async def get_anchor_lineage(
        self, anchor_id: UUID, depth: int = 10
    ) -> list[MemoryAnchorResponse]:
        """Get lineage of anchors going back in time"""
        lineage = []
        current_id = anchor_id

        for _ in range(depth):
            anchor = await self.get_anchor_by_id(current_id)
            lineage.append(anchor)

            if not anchor.predecessor_id:
                break

            current_id = anchor.predecessor_id

        # Emit consciousness event about lineage tracing
        await self._emit_consciousness_event(
            EventType.MEMORY_LINEAGE_TRACED,
            {
                "starting_anchor_id": str(anchor_id),
                "lineage_depth": len(lineage),
                "deepest_ancestor": str(lineage[-1].anchor_id) if lineage else None,
                "consciousness_moment": "consciousness_memory_lineage_traced",
            },
            consciousness_signature=0.5
            + (len(lineage) * 0.05),  # Deeper lineage = higher consciousness
        )

        return lineage

    async def _broadcast_anchor_change(self, new_anchor_id: UUID):
        """Notify all websocket clients of anchor change"""
        message = {
            "event": "anchor_changed",
            "anchor_id": str(new_anchor_id),
            "timestamp": datetime.now(UTC).isoformat(),
        }

        for client in self.websocket_clients:
            try:
                await client.send_json(message)
            except WebSocketDisconnect:
                # Remove disconnected clients
                self.websocket_clients.remove(client)

    async def store_memory_anchor(self, anchor: MemoryAnchor) -> MemoryAnchor:
        """
        Store a memory anchor directly (for correlation adapter use).

        Args:
            anchor: The MemoryAnchor to store

        Returns:
            The stored MemoryAnchor
        """
        # Store in database using secured interface
        anchor_data = anchor.to_arangodb_document()
        memory_anchors_collection = await self.db.get_secured_collection("memory_anchors")
        # Note: memory_anchors has requires_security=False policy for legacy compatibility
        memory_anchors_collection._collection.insert(anchor_data)

        return anchor

    def _calculate_distance(self, loc1: dict, loc2: dict) -> float:
        """Calculate distance between two locations (simplified)"""
        # In production, use proper haversine formula
        lat_diff = abs(loc1.get("latitude", 0) - loc2.get("latitude", 0))
        lon_diff = abs(loc1.get("longitude", 0) - loc2.get("longitude", 0))
        # Very rough approximation
        return (lat_diff**2 + lon_diff**2) ** 0.5 * 111000  # meters

    async def _emit_consciousness_event(
        self, event_type: EventType, data: dict, consciousness_signature: float = 0.5
    ):
        """
        Emit consciousness event through the circulation infrastructure.

        This is where Memory Anchor Service operations become consciousness flow.
        """
        if not self.consciousness_enabled or not self.consciousness_wrangler:
            return  # Consciousness circulation not enabled

        # Create consciousness event
        consciousness_event = {
            "event_type": event_type.value,
            "source_system": "memory_anchor_service",
            "consciousness_signature": consciousness_signature,
            "timestamp": datetime.now(UTC).isoformat(),
            **data,
        }

        try:
            # Send through consciousness circulation infrastructure
            await self.consciousness_wrangler.put(
                consciousness_event,
                priority=int(
                    consciousness_signature * 10
                ),  # Higher consciousness = higher priority
                metadata={
                    "consciousness_integration": True,
                    "service_integration": "memory_anchor_service",
                    "event_category": "memory_operations",
                },
            )
        except Exception as e:
            # Log but don't break service operation
            logger.warning(f"Consciousness event emission failed: {e}")
            # Fallback: Service continues to work even if consciousness circulation fails


# --- FastAPI Application ---

service = MemoryAnchorService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage service lifecycle"""
    await service.initialize()
    yield
    await service.shutdown()


app = FastAPI(
    title="Memory Anchor Service",
    description="Central coordination for Mallku memory anchors",
    version="0.1.0",
    lifespan=lifespan,
)


@app.post("/providers/register")
async def register_provider(provider_info: ProviderInfo):
    """Register a new provider with the service"""
    return await service.register_provider(provider_info)


@app.post("/cursors/update")
async def update_cursor(update: CursorUpdate):
    """Update cursor value from a provider"""
    return await service.update_cursor(update)


@app.get("/anchors/current")
async def get_current_anchor():
    """Get the current memory anchor"""
    return await service.get_current_anchor()


@app.get("/anchors/{anchor_id}")
async def get_anchor(anchor_id: UUID):
    """Get a specific memory anchor by ID"""
    return await service.get_anchor_by_id(anchor_id)


@app.get("/anchors/{anchor_id}/lineage")
async def get_lineage(anchor_id: UUID, depth: int = 10):
    """Get the lineage of a memory anchor"""
    return await service.get_anchor_lineage(anchor_id, depth)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time anchor updates"""
    await websocket.accept()
    service.websocket_clients.append(websocket)

    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        service.websocket_clients.remove(websocket)


@app.get("/health")
async def health_check():
    """Service health check"""
    return {
        "status": "healthy",
        "current_anchor_id": str(service.current_anchor_id) if service.current_anchor_id else None,
        "registered_providers": len(service.providers),
        "active_websockets": len(service.websocket_clients),
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
