"""
Data Wrangler Interface - Universal abstraction for data movement in Mallku

This interface defines the contract that all data wranglers must implement,
enabling pluggable data transport strategies throughout the system.

The beauty of this pattern is its reciprocity:
- Wranglers give: Consistent interface, reliability guarantees
- Components give: Data in standard format
- Wranglers receive: Freedom to implement optimally
- Components receive: Freedom from transport concerns
"""

import uuid
from abc import ABC, abstractmethod
from datetime import UTC, datetime
from typing import Any, Protocol


class DataWranglerInterface(Protocol):
    """
    Universal interface for data movement in Mallku.

    Any component in the system can use wranglers for data transport,
    not just collectors and recorders. This enables:
    - Memory Anchor Service event distribution
    - Reciprocity measurement flows
    - Query result pagination
    - Inter-service communication
    - Fire Circle message passing
    """

    @abstractmethod
    async def put(
        self,
        items: dict | list[dict],
        priority: int = 0,
        metadata: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """
        Accept data from any source.

        Args:
            items: Single item or list of items to wrangle
            priority: Priority level (0 = normal, higher = more urgent)
            metadata: Optional metadata about the items

        Returns:
            Receipt containing:
            - success: bool
            - count: number of items accepted
            - message_ids: list of assigned IDs (if applicable)
            - timestamp: when items were accepted
        """
        pass

    @abstractmethod
    async def get(
        self,
        count: int = 1,
        timeout: float | None = None,
        auto_ack: bool = True
    ) -> list[dict]:
        """
        Provide data to any consumer.

        Args:
            count: Maximum number of items to retrieve
            timeout: Max seconds to wait for items (None = no wait)
            auto_ack: Automatically acknowledge receipt

        Returns:
            List of items (may be empty if none available)
        """
        pass

    @abstractmethod
    async def peek(
        self,
        count: int = 1,
        offset: int = 0
    ) -> list[dict]:
        """
        Preview items without consuming them.

        Args:
            count: Maximum number of items to preview
            offset: Skip this many items before peeking

        Returns:
            List of items (not removed from wrangler)
        """
        pass

    @abstractmethod
    async def ack(
        self,
        message_ids: str | list[str]
    ) -> bool:
        """
        Acknowledge successful processing of items.

        Args:
            message_ids: ID(s) of successfully processed items

        Returns:
            True if all acknowledgments succeeded
        """
        pass

    @abstractmethod
    async def nack(
        self,
        message_ids: str | list[str],
        requeue: bool = True,
        reason: str | None = None
    ) -> bool:
        """
        Negative acknowledgment - processing failed.

        Args:
            message_ids: ID(s) of failed items
            requeue: Whether to make items available again
            reason: Optional failure reason for diagnostics

        Returns:
            True if all nacks succeeded
        """
        pass

    @abstractmethod
    async def get_stats(self) -> dict[str, Any]:
        """
        Get wrangler statistics and health information.

        Returns:
            Dictionary containing:
            - depth: Current number of items
            - in_flight: Items retrieved but not acked
            - total_in: Total items received
            - total_out: Total items delivered
            - throughput: Items/second rates
            - health: OK/DEGRADED/FAILED
            - implementation: Wrangler type details
        """
        pass

    @abstractmethod
    async def close(self) -> None:
        """
        Gracefully shut down the wrangler.

        Should:
        - Flush any pending items
        - Close connections
        - Release resources
        - Save state if applicable
        """
        pass

    # Optional enhanced capabilities

    async def subscribe(
        self,
        callback: Any,  # Callable[[Dict], Awaitable[None]]
        filter_expr: str | None = None
    ) -> str:
        """
        Subscribe to items matching a filter (if supported).

        Args:
            callback: Async function to call with matching items
            filter_expr: Optional filter expression

        Returns:
            Subscription ID for later unsubscribe

        Raises:
            NotImplementedError: If wrangler doesn't support subscriptions
        """
        raise NotImplementedError("This wrangler does not support subscriptions")

    async def unsubscribe(self, subscription_id: str) -> bool:
        """
        Cancel a subscription.

        Args:
            subscription_id: ID returned from subscribe()

        Returns:
            True if successfully unsubscribed

        Raises:
            NotImplementedError: If wrangler doesn't support subscriptions
        """
        raise NotImplementedError("This wrangler does not support subscriptions")

    async def query(
        self,
        filter_expr: str,
        limit: int = 100,
        since: datetime | None = None
    ) -> list[dict]:
        """
        Query historical items (if supported).

        Args:
            filter_expr: Query expression
            limit: Maximum results
            since: Only items after this time

        Returns:
            Matching items

        Raises:
            NotImplementedError: If wrangler doesn't support queries
        """
        raise NotImplementedError("This wrangler does not support queries")


class WranglerCapabilities:
    """
    Declares what optional features a wrangler supports.
    """

    def __init__(
        self,
        supports_priority: bool = False,
        supports_subscriptions: bool = False,
        supports_queries: bool = False,
        supports_transactions: bool = False,
        supports_persistence: bool = False,
        max_item_size: int | None = None,
        max_batch_size: int | None = None
    ):
        self.supports_priority = supports_priority
        self.supports_subscriptions = supports_subscriptions
        self.supports_queries = supports_queries
        self.supports_transactions = supports_transactions
        self.supports_persistence = supports_persistence
        self.max_item_size = max_item_size
        self.max_batch_size = max_batch_size


class BaseWrangler(ABC):
    """
    Base implementation providing common functionality.
    """

    def __init__(self, name: str, capabilities: WranglerCapabilities | None = None):
        self.name = name
        self.capabilities = capabilities or WranglerCapabilities()
        self.total_in = 0
        self.total_out = 0
        self.created_at = datetime.now(UTC)

    def _validate_items(self, items: dict | list[dict]) -> list[dict]:
        """Ensure items are in list format."""
        if isinstance(items, dict):
            return [items]
        return items

    def _generate_message_id(self) -> str:
        """Generate unique message ID."""
        return str(uuid.uuid4())
