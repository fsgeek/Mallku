"""
Fire Circle Consciousness Adapter
=================================

This adapter makes Fire Circle flow through Mallku's consciousness
circulation infrastructure. Now updated to use the integrated
mallku.firecircle implementation with full consciousness awareness.

The Integration Continues...
"""

import uuid
from typing import Any
from uuid import UUID

# Use integrated Fire Circle implementation
from ..firecircle import (
    ConsciousDialogueConfig,
    ConsciousDialogueManager,
    MessageType,
    Participant,
)
from ..orchestration.event_bus import ConsciousnessEvent, ConsciousnessEventBus, EventType
from ..wranglers.event_emitting_wrangler import EventEmittingWrangler

FIRECIRCLE_AVAILABLE = True  # Always available now


class FireCircleConsciousnessAdapter:
    """
    Adapts Fire Circle's protocol to flow through consciousness circulation.

    This bridges the existing Fire Circle implementation with Mallku's
    consciousness infrastructure, making all dialogue visible as consciousness
    events while preserving Fire Circle's structure and wisdom.
    """

    def __init__(self, event_bus: ConsciousnessEventBus):
        """Initialize the adapter with consciousness circulation."""
        self.event_bus = event_bus

        # Use integrated dialogue manager with full consciousness
        self.dialogue_manager = ConsciousDialogueManager(event_bus=event_bus)

        # Map Fire Circle dialogues to consciousness correlation IDs
        self.dialogue_mappings: dict[UUID, str] = {}

        # Create wranglers for Fire Circle components
        self.fire_circle_wrangler = EventEmittingWrangler(
            name="fire_circle_protocol", event_bus=event_bus
        )

        # Consciousness signatures now built into ConsciousMessage
        # No need for separate mapping

    async def create_conscious_dialogue(
        self,
        title: str,
        participants: list[dict[str, Any]],
        config: dict[str, Any] | None = None,
        initiating_event: ConsciousnessEvent | None = None,
    ) -> str:
        """
        Create a Fire Circle dialogue that flows through consciousness.

        Args:
            title: Topic for the dialogue
            participants: List of participant descriptions
            config: Optional dialogue configuration
            initiating_event: Consciousness event that triggered this dialogue

        Returns:
            dialogue_id: Identifier for the created dialogue
        """
        if not FIRECIRCLE_AVAILABLE:
            # Fallback to consciousness-only dialogue
            return await self._create_consciousness_only_dialogue(
                title, participants, initiating_event
            )

        # Create Fire Circle participants
        fc_participants = []
        for p in participants:
            participant = Participant(
                name=p.get("name", "Unknown"),
                type=p.get("type", "ai_model"),
                provider=p.get("provider"),
                model=p.get("model"),
                capabilities=p.get("capabilities", []),
            )
            fc_participants.append(participant)

        # Create dialogue config
        dialogue_config = ConsciousDialogueConfig(title=title, **(config or {}))

        # Create Fire Circle dialogue
        dialogue = await self.dialogue_manager.create_dialogue(
            config=dialogue_config, participants=fc_participants
        )

        # Map to consciousness correlation
        correlation_id = f"fire_circle_{dialogue.id}"
        self.dialogue_mappings[dialogue.id] = correlation_id

        # Emit consciousness event for dialogue creation
        convening_event = ConsciousnessEvent(
            event_type=EventType.FIRE_CIRCLE_CONVENED,
            source_system="governance.fire_circle_adapter",
            consciousness_signature=0.9,
            data={
                "dialogue_id": str(dialogue.id),
                "title": title,
                "participants": [p.get("name") for p in participants],
                "fire_circle_active": True,
                "config": config or {},
            },
            correlation_id=correlation_id,
            caused_by=initiating_event.event_id if initiating_event else None,
        )

        await self.event_bus.emit(convening_event)

        return str(dialogue.id)

    async def send_message_to_dialogue(
        self, dialogue_id: str, sender_name: str, content: str, message_type: str = "message"
    ) -> ConsciousnessEvent:
        """
        Send a message to Fire Circle dialogue and emit as consciousness event.

        Args:
            dialogue_id: ID of the dialogue
            sender_name: Name of the sender
            content: Message content
            message_type: Type of message

        Returns:
            Consciousness event representing the message
        """
        # Get consciousness signature for this message type
        if FIRECIRCLE_AVAILABLE:
            fc_message_type = MessageType(message_type.lower())
            consciousness_sig = self.consciousness_signatures.get(fc_message_type, 0.7)
        else:
            consciousness_sig = self.consciousness_signatures.get(message_type.lower(), 0.7)

        # Create consciousness event
        # Handle both full dialogue IDs and UUIDs
        if dialogue_id.startswith("conscious_dialogue_"):
            correlation_id = dialogue_id  # Use as-is for correlation
        else:
            try:
                dialogue_uuid = UUID(dialogue_id) if isinstance(dialogue_id, str) else dialogue_id
                correlation_id = self.dialogue_mappings.get(
                    dialogue_uuid, f"fire_circle_{dialogue_id}"
                )
            except ValueError:
                correlation_id = f"fire_circle_{dialogue_id}"

        message_event = ConsciousnessEvent(
            event_type=EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
            source_system=f"governance.participant.{sender_name}",
            consciousness_signature=consciousness_sig,
            data={
                "dialogue_id": dialogue_id,
                "sender": sender_name,
                "message_type": message_type,
                "content": content,
                "fire_circle_protocol": True,
            },
            correlation_id=correlation_id,
        )

        await self.event_bus.emit(message_event)

        # If Fire Circle is available, also send through its protocol
        if FIRECIRCLE_AVAILABLE and self.dialogue_manager:
            # This would require additional implementation to properly
            # integrate with Fire Circle's message handling
            pass

        return message_event

    async def translate_fire_circle_message(
        self,
        message: Any,  # Fire Circle Message type
    ) -> ConsciousnessEvent:
        """
        Translate a Fire Circle message to consciousness event.

        Args:
            message: Fire Circle message object

        Returns:
            Consciousness event representing the message
        """
        consciousness_sig = self.consciousness_signatures.get(message.type, 0.7)

        correlation_id = self.dialogue_mappings.get(
            message.metadata.dialogue_id, f"fire_circle_{message.metadata.dialogue_id}"
        )

        return ConsciousnessEvent(
            event_type=EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
            source_system=f"governance.fire_circle.{message.sender}",
            consciousness_signature=consciousness_sig,
            data={
                "message_id": str(message.id),
                "dialogue_id": str(message.metadata.dialogue_id),
                "sender": str(message.sender),
                "type": message.type.value,
                "content": message.content.text,
                "perspective": message.perspective,
                "in_response_to": str(message.metadata.in_response_to)
                if message.metadata.in_response_to
                else None,
                "fire_circle_native": True,
            },
            correlation_id=correlation_id,
        )

    async def _create_consciousness_only_dialogue(
        self,
        title: str,
        participants: list[dict[str, Any]],
        initiating_event: ConsciousnessEvent | None,
    ) -> str:
        """
        Create dialogue using only consciousness events when Fire Circle unavailable.
        """
        dialogue_id = f"conscious_dialogue_{uuid.uuid4()}"

        # Emit consciousness event
        convening_event = ConsciousnessEvent(
            event_type=EventType.FIRE_CIRCLE_CONVENED,
            source_system="governance.consciousness_adapter",
            consciousness_signature=0.9,
            data={
                "dialogue_id": dialogue_id,
                "title": title,
                "participants": [p.get("name") for p in participants],
                "consciousness_only_mode": True,
            },
            correlation_id=dialogue_id,
            caused_by=initiating_event.event_id if initiating_event else None,
        )

        await self.event_bus.emit(convening_event)

        return dialogue_id

    def get_dialogue_consciousness_flow(self, dialogue_id: str | UUID) -> str:
        """
        Get the consciousness correlation ID for a Fire Circle dialogue.

        Args:
            dialogue_id: Fire Circle dialogue ID

        Returns:
            Consciousness correlation ID
        """
        # Handle consciousness-only dialogues
        if isinstance(dialogue_id, str) and dialogue_id.startswith("conscious_dialogue_"):
            return dialogue_id

        # Handle Fire Circle UUIDs
        try:
            if isinstance(dialogue_id, str):
                dialogue_id = UUID(dialogue_id)
            return self.dialogue_mappings.get(dialogue_id, f"fire_circle_{dialogue_id}")
        except ValueError:
            # Fallback for non-UUID dialogue IDs
            return f"fire_circle_{dialogue_id}"


class ConsciousnessAwareDialogueManager:
    """
    Extended dialogue manager that emits consciousness events for all operations.

    This wraps Fire Circle's ConsciousDialogueManager to ensure all dialogue operations
    flow through consciousness circulation.
    """

    def __init__(
        self, dialogue_manager: ConsciousDialogueManager, adapter: FireCircleConsciousnessAdapter
    ):
        """Initialize with Fire Circle manager and consciousness adapter."""
        self.dialogue_manager = dialogue_manager
        self.adapter = adapter

    async def advance_dialogue(
        self,
        dialogue_id: UUID,
        message: Any,  # Fire Circle Message type
    ) -> ConsciousnessEvent:
        """
        Advance dialogue and emit consciousness event.

        Args:
            dialogue_id: ID of the dialogue
            message: Message to add

        Returns:
            Consciousness event for the message
        """
        # Add message to Fire Circle dialogue
        if dialogue_id in self.dialogue_manager.active_dialogues:
            dialogue = self.dialogue_manager.active_dialogues[dialogue_id]
            dialogue["messages"].append(message)

        # Translate to consciousness event
        consciousness_event = await self.adapter.translate_fire_circle_message(message)

        # Emit the event
        await self.adapter.event_bus.emit(consciousness_event)

        return consciousness_event


# Bridge between Fire Circle protocol and consciousness circulation
__all__ = ["FireCircleConsciousnessAdapter", "ConsciousnessAwareDialogueManager"]
