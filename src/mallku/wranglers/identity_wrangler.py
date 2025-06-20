"""
Identity Wrangler - Direct pass-through implementation

The simplest possible wrangler - connects producer directly to consumer
with no intermediate storage or buffering.
"""

import asyncio
from datetime import UTC, datetime
from typing import Any

from .interface import BaseWrangler, WranglerCapabilities


class IdentityWrangler(BaseWrangler):
    """
    Direct pass-through wrangler with no buffering.

    Perfect for:
    - Low-volume data flows
    - Testing and development
    - Cases where producer and consumer are tightly coupled
    - Minimal overhead requirements

    This demonstrates the minimal implementation of the wrangler interface.
    """

    def __init__(self, name: str = "identity"):
        capabilities = WranglerCapabilities(
            supports_priority=False,
            supports_subscriptions=False,
            supports_queries=False,
            supports_transactions=False,
            supports_persistence=False,
        )
        super().__init__(name, capabilities)

        # Simple queue for demonstration
        self._queue: asyncio.Queue = asyncio.Queue()
        self._in_flight: dict[str, dict] = {}

    async def put(
        self, items: dict | list[dict], priority: int = 0, metadata: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Accept items and immediately queue them."""
        items_list = self._validate_items(items)
        message_ids = []

        for item in items_list:
            msg_id = self._generate_message_id()
            wrapped = {"_id": msg_id, "_timestamp": datetime.now(UTC), "data": item}
            await self._queue.put(wrapped)
            message_ids.append(msg_id)
            self.total_in += 1

        return {
            "success": True,
            "count": len(items_list),
            "message_ids": message_ids,
            "timestamp": datetime.now(UTC),
        }

    async def get(
        self, count: int = 1, timeout: float | None = None, auto_ack: bool = True
    ) -> list[dict]:
        """Retrieve items from queue."""
        items = []

        try:
            # Get first item with timeout
            if timeout is not None:
                item = await asyncio.wait_for(self._queue.get(), timeout=timeout)
            else:
                item = self._queue.get_nowait()

            items.append(item["data"])
            if not auto_ack:
                self._in_flight[item["_id"]] = item
            self.total_out += 1

            # Get additional items without waiting
            for _ in range(count - 1):
                try:
                    item = self._queue.get_nowait()
                    items.append(item["data"])
                    if not auto_ack:
                        self._in_flight[item["_id"]] = item
                    self.total_out += 1
                except asyncio.QueueEmpty:
                    break

        except (TimeoutError, asyncio.QueueEmpty):
            pass

        return items

    async def peek(self, count: int = 1, offset: int = 0) -> list[dict]:
        """
        Peek at queue contents.

        Note: This is inefficient for IdentityWrangler as it requires
        copying the queue. Real implementations might maintain indexes.
        """
        # Convert queue to list temporarily
        temp_items = []
        while not self._queue.empty():
            try:
                temp_items.append(self._queue.get_nowait())
            except asyncio.QueueEmpty:
                break

        # Put items back
        for item in temp_items:
            await self._queue.put(item)

        # Return requested slice
        result_items = temp_items[offset : offset + count]
        return [item["data"] for item in result_items]

    async def ack(self, message_ids: str | list[str]) -> bool:
        """Acknowledge items (remove from in-flight)."""
        if isinstance(message_ids, str):
            message_ids = [message_ids]

        for msg_id in message_ids:
            self._in_flight.pop(msg_id, None)

        return True

    async def nack(
        self, message_ids: str | list[str], requeue: bool = True, reason: str | None = None
    ) -> bool:
        """Return items to queue if requested."""
        if isinstance(message_ids, str):
            message_ids = [message_ids]

        for msg_id in message_ids:
            item = self._in_flight.pop(msg_id, None)
            if item and requeue:
                await self._queue.put(item)

        return True

    async def get_stats(self) -> dict[str, Any]:
        """Get current statistics."""
        return {
            "depth": self._queue.qsize(),
            "in_flight": len(self._in_flight),
            "total_in": self.total_in,
            "total_out": self.total_out,
            "throughput": {
                "in_per_sec": 0,  # Would need time tracking
                "out_per_sec": 0,
            },
            "health": "OK",
            "implementation": {
                "type": "IdentityWrangler",
                "buffering": "memory",
                "persistence": False,
            },
        }

    async def close(self) -> None:
        """Clean shutdown - nothing to do for identity wrangler."""
        # In a real implementation might:
        # - Drain the queue
        # - Log final stats
        # - Clean up resources
        pass
