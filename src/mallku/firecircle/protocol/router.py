"""
Consciousness-Aware Message Router
=================================

Routes Fire Circle messages through consciousness circulation,
ensuring all dialogue flows are tracked, correlated, and preserved.

The Integration Continues...
"""

import asyncio
import logging
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from ...orchestration.event_bus import ConsciousnessEvent, ConsciousnessEventBus, EventType
from .conscious_message import ConsciousMessage, MessageStatus

logger = logging.getLogger(__name__)


class MessageDeliveryStatus:
    """Track delivery status for a message."""

    def __init__(self, message_id: UUID):
        self.message_id = message_id
        self.sent_to: set[UUID] = set()
        self.confirmed_by: set[UUID] = set()
        self.read_by: set[UUID] = set()
        self.errors: dict[UUID, str] = {}


class ConsciousMessageRouter:
    """
    Routes messages between dialogue participants with consciousness tracking.

    Features:
    - Asynchronous message delivery
    - Delivery confirmation tracking
    - Consciousness event emission
    - Message filtering based on visibility
    - Error handling and retry logic
    """

    def __init__(
        self,
        event_bus: ConsciousnessEventBus | None = None,
    ):
        """Initialize router with consciousness infrastructure."""
        self.event_bus = event_bus

        # Message queues per participant
        self.participant_queues: dict[UUID, asyncio.Queue] = {}

        # Delivery tracking
        self.delivery_status: dict[UUID, MessageDeliveryStatus] = {}

        # Message handlers per participant
        self.message_handlers: dict[UUID, Any] = {}

        # Active routing tasks
        self.routing_tasks: list[asyncio.Task] = []

    async def register_participant(
        self,
        participant_id: UUID,
        handler: Any | None = None,
    ) -> None:
        """
        Register a participant for message routing.

        Args:
            participant_id: Unique identifier for participant
            handler: Optional message handler (adapter or callback)
        """
        if participant_id not in self.participant_queues:
            self.participant_queues[participant_id] = asyncio.Queue()
            logger.info(f"Registered participant: {participant_id}")

        if handler:
            self.message_handlers[participant_id] = handler

    async def unregister_participant(
        self,
        participant_id: UUID,
    ) -> None:
        """Unregister a participant from routing."""
        if participant_id in self.participant_queues:
            # Clear pending messages
            queue = self.participant_queues[participant_id]
            while not queue.empty():
                try:
                    queue.get_nowait()
                except asyncio.QueueEmpty:
                    break

            del self.participant_queues[participant_id]

        if participant_id in self.message_handlers:
            del self.message_handlers[participant_id]

        logger.info(f"Unregistered participant: {participant_id}")

    async def route_message(
        self,
        message: ConsciousMessage,
        recipients: list[UUID] | None = None,
    ) -> MessageDeliveryStatus:
        """
        Route a consciousness-aware message to recipients.

        Args:
            message: Message to route
            recipients: Specific recipients, or None for broadcast

        Returns:
            Delivery status tracking object
        """
        # Update message status
        message.status = MessageStatus.SENT

        # Initialize delivery tracking
        delivery = MessageDeliveryStatus(message.id)
        self.delivery_status[message.id] = delivery

        # Determine recipients
        if recipients is None:
            # Broadcast to all participants except sender
            recipients = [pid for pid in self.participant_queues if pid != message.sender]

        # Emit routing event
        if self.event_bus:
            await self._emit_routing_event(message, recipients)

        # Route to each recipient
        routing_tasks = []
        for recipient_id in recipients:
            if recipient_id in self.participant_queues:
                task = asyncio.create_task(
                    self._deliver_to_participant(message, recipient_id, delivery)
                )
                routing_tasks.append(task)
                delivery.sent_to.add(recipient_id)

        # Wait for initial delivery
        if routing_tasks:
            await asyncio.gather(*routing_tasks, return_exceptions=True)

        return delivery

    async def _deliver_to_participant(
        self,
        message: ConsciousMessage,
        recipient_id: UUID,
        delivery: MessageDeliveryStatus,
    ) -> None:
        """Deliver message to specific participant."""
        try:
            queue = self.participant_queues.get(recipient_id)
            if queue:
                await queue.put(message)
                delivery.confirmed_by.add(recipient_id)

                # If handler available, process immediately
                handler = self.message_handlers.get(recipient_id)
                if handler and hasattr(handler, "receive_message"):
                    await handler.receive_message(message)
                    delivery.read_by.add(recipient_id)

        except Exception as e:
            logger.error(f"Error delivering to {recipient_id}: {e}")
            delivery.errors[recipient_id] = str(e)

    async def get_messages(
        self,
        participant_id: UUID,
        timeout: float | None = None,
    ) -> list[ConsciousMessage]:
        """
        Get pending messages for a participant.

        Args:
            participant_id: Participant to get messages for
            timeout: Optional timeout in seconds

        Returns:
            List of pending messages
        """
        queue = self.participant_queues.get(participant_id)
        if not queue:
            return []

        messages = []
        end_time = datetime.now(UTC).timestamp() + timeout if timeout else None

        while True:
            try:
                remaining_timeout = None
                if end_time:
                    remaining_timeout = end_time - datetime.now(UTC).timestamp()
                    if remaining_timeout <= 0:
                        break

                message = await asyncio.wait_for(
                    queue.get(),
                    timeout=remaining_timeout,
                )
                messages.append(message)

                # Update delivery status
                if message.id in self.delivery_status:
                    self.delivery_status[message.id].read_by.add(participant_id)

            except TimeoutError:
                break
            except Exception as e:
                logger.error(f"Error getting messages for {participant_id}: {e}")
                break

        return messages

    async def broadcast_system_message(
        self,
        content: str,
        dialogue_id: UUID,
        consciousness_signature: float = 0.9,
    ) -> MessageDeliveryStatus:
        """
        Broadcast a system message to all participants.
        """
        from .conscious_message import create_conscious_system_message

        message = create_conscious_system_message(
            dialogue_id=dialogue_id,
            content=content,
            consciousness_signature=consciousness_signature,
        )

        return await self.route_message(message)

    async def _emit_routing_event(
        self,
        message: ConsciousMessage,
        recipients: list[UUID],
    ) -> None:
        """Emit consciousness event for message routing."""
        if not self.event_bus:
            return

        event = ConsciousnessEvent(
            event_type=EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
            source_system="firecircle.router",
            consciousness_signature=message.consciousness.consciousness_signature,
            data={
                "action": "message_routed",
                "message_id": str(message.id),
                "message_type": message.type.value,
                "sender_id": str(message.sender),
                "recipient_count": len(recipients),
                "patterns": message.consciousness.detected_patterns,
            },
            correlation_id=message.consciousness.correlation_id,
        )

        await self.event_bus.emit(event)

    def get_delivery_status(
        self,
        message_id: UUID,
    ) -> MessageDeliveryStatus | None:
        """Get delivery status for a message."""
        return self.delivery_status.get(message_id)

    async def wait_for_delivery(
        self,
        message_id: UUID,
        timeout: float = 5.0,
    ) -> bool:
        """
        Wait for message delivery confirmation.

        Args:
            message_id: Message to wait for
            timeout: Maximum time to wait

        Returns:
            True if delivered to all recipients
        """
        end_time = datetime.now(UTC).timestamp() + timeout

        while datetime.now(UTC).timestamp() < end_time:
            status = self.delivery_status.get(message_id)
            if status and status.sent_to == status.confirmed_by:
                return True

            await asyncio.sleep(0.1)

        return False

    async def get_routing_metrics(self) -> dict[str, Any]:
        """Get router performance metrics."""
        total_messages = len(self.delivery_status)
        delivered_messages = sum(
            1 for status in self.delivery_status.values() if status.sent_to == status.confirmed_by
        )

        read_messages = sum(1 for status in self.delivery_status.values() if status.read_by)

        failed_messages = sum(1 for status in self.delivery_status.values() if status.errors)

        queue_sizes = {str(pid): queue.qsize() for pid, queue in self.participant_queues.items()}

        return {
            "total_messages_routed": total_messages,
            "successfully_delivered": delivered_messages,
            "messages_read": read_messages,
            "failed_deliveries": failed_messages,
            "active_participants": len(self.participant_queues),
            "queue_sizes": queue_sizes,
        }
