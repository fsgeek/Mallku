"""
Memory Anchor Client - Used by providers to interact with the service
"""

import asyncio
import json
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

import httpx
import websockets


class MemoryAnchorClient:
    """
    Client for providers to interact with Memory Anchor Service.
    Handles registration, cursor updates, and real-time notifications.
    """

    def __init__(
        self,
        service_url: str = "http://localhost:8000",
        provider_id: str | None = None,
        provider_type: str | None = None,
        cursor_types: list | None = None,
    ):
        self.service_url = service_url
        self.ws_url = service_url.replace("http", "ws") + "/ws"
        self.provider_id = provider_id
        self.provider_type = provider_type
        self.cursor_types = cursor_types or []
        self.current_anchor_id: UUID | None = None
        self._ws_connection = None
        self._anchor_change_callback: Callable | None = None

    async def register(self, metadata: dict[str, Any] | None = None) -> dict:
        """Register this provider with the service"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.service_url}/providers/register",
                json={
                    "provider_id": self.provider_id,
                    "provider_type": self.provider_type,
                    "cursor_types": self.cursor_types,
                    "metadata": metadata or {},
                },
            )
            response.raise_for_status()
            result = response.json()
            self.current_anchor_id = UUID(result["current_anchor_id"])
            return result

    async def update_cursor(
        self, cursor_type: str, cursor_value: Any, metadata: dict[str, Any] | None = None
    ) -> dict:
        """Send cursor update to the service"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.service_url}/cursors/update",
                json={
                    "provider_id": self.provider_id,
                    "cursor_type": cursor_type,
                    "cursor_value": cursor_value,
                    "metadata": metadata or {},
                },
            )
            response.raise_for_status()
            result = response.json()
            self.current_anchor_id = UUID(result["anchor_id"])
            return result

    async def get_current_anchor(self) -> dict:
        """Get the current memory anchor"""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.service_url}/anchors/current")
            response.raise_for_status()
            return response.json()

    async def get_anchor(self, anchor_id: UUID) -> dict:
        """Get a specific memory anchor"""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.service_url}/anchors/{anchor_id}")
            response.raise_for_status()
            return response.json()

    async def connect_websocket(self, on_anchor_change: Callable | None = None):
        """Connect to websocket for real-time updates"""
        self._anchor_change_callback = on_anchor_change

        async with websockets.connect(self.ws_url) as websocket:
            self._ws_connection = websocket

            # Send initial connection message
            await websocket.send(json.dumps({"type": "connect", "provider_id": self.provider_id}))

            # Listen for updates
            async for message in websocket:
                data = json.loads(message)
                if data.get("event") == "anchor_changed":
                    new_anchor_id = UUID(data["anchor_id"])
                    self.current_anchor_id = new_anchor_id

                    if self._anchor_change_callback:
                        await self._anchor_change_callback(new_anchor_id, data)

    async def close(self):
        """Close client connections"""
        if self._ws_connection:
            await self._ws_connection.close()


# --- Example Provider Implementation ---


class ExampleLocationProvider:
    """
    Example provider that reports location changes to Memory Anchor Service
    """

    def __init__(self):
        self.client = MemoryAnchorClient(
            provider_id="location_provider_001",
            provider_type="gps",
            cursor_types=["spatial", "temporal"],
        )
        self.last_location = None

    async def initialize(self):
        """Initialize provider and register with service"""
        await self.client.register(metadata={"accuracy": "high", "update_frequency": "on_change"})

        # Set up websocket for notifications
        asyncio.create_task(self.client.connect_websocket(self.on_anchor_change))

    async def on_anchor_change(self, new_anchor_id: UUID, data: dict):
        """Handle anchor change notifications"""
        print(f"Memory anchor changed to: {new_anchor_id}")
        # Could trigger any provider-specific actions here

    async def update_location(self, latitude: float, longitude: float):
        """Report new location to service"""
        location_data = {
            "latitude": latitude,
            "longitude": longitude,
            "timestamp": datetime.now(UTC).isoformat(),
        }

        # Update spatial cursor
        result = await self.client.update_cursor(
            cursor_type="spatial",
            cursor_value=location_data,
            metadata={"source": "gps", "accuracy_meters": 5.0},
        )

        self.last_location = location_data
        print(f"Location updated, anchor: {result['anchor_id']}")

        # Also update temporal cursor
        await self.client.update_cursor(
            cursor_type="temporal", cursor_value=datetime.now(UTC).isoformat()
        )

    async def run_simulation(self):
        """Simulate location updates"""
        await self.initialize()

        # Simulate movement
        locations = [
            (37.7749, -122.4194),  # San Francisco
            (37.7751, -122.4180),  # Small movement
            (37.8044, -122.2712),  # Oakland (should trigger new anchor)
            (37.8046, -122.2710),  # Small movement
        ]

        for lat, lon in locations:
            await self.update_location(lat, lon)
            await asyncio.sleep(2)  # Wait between updates


# --- Usage Example ---


async def main():
    """Example usage of Memory Anchor Client"""

    # Create and run location provider
    provider = ExampleLocationProvider()
    await provider.run_simulation()

    # Query anchor history
    current = await provider.client.get_current_anchor()
    print(f"Current anchor: {current}")

    # Get lineage
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://localhost:8000/anchors/{current['anchor_id']}/lineage")
        lineage = response.json()
        print(f"Anchor lineage ({len(lineage)} entries):")
        for anchor in lineage:
            print(f"  - {anchor['anchor_id']} at {anchor['timestamp']}")


if __name__ == "__main__":
    asyncio.run(main())
