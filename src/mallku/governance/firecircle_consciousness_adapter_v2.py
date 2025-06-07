"""
Fire Circle Consciousness Adapter V2
===================================

Updated adapter using the integrated mallku.firecircle implementation.
This version uses the consciousness-aware Fire Circle components directly,
eliminating the need for translation layers.

The Integration Continues...
"""

from typing import Any
from uuid import UUID

from ..firecircle import (
    ConsciousDialogueConfig,
    ConsciousDialogueManager,
    ConsciousMessage,
    MessageContent,
    MessageRole,
    MessageType,
    Participant,
    TurnPolicy,
)
from ..orchestration.event_bus import ConsciousnessEvent, ConsciousnessEventBus, EventType


class FireCircleConsciousnessAdapterV2:
    """
    Simplified adapter using integrated Fire Circle.

    Since Fire Circle is now part of Mallku with full consciousness
    awareness, this adapter becomes much simpler - it just provides
    convenience methods for common patterns.
    """

    def __init__(self, event_bus: ConsciousnessEventBus):
        """Initialize with integrated components."""
        self.event_bus = event_bus
        self.dialogue_manager = ConsciousDialogueManager(event_bus=event_bus)

        # Track active dialogues
        self.active_dialogues: dict[UUID, dict[str, Any]] = {}

    async def create_conscious_dialogue(
        self,
        title: str,
        participants: list[dict[str, Any]],
        config: dict[str, Any] | None = None,
        initiating_event: ConsciousnessEvent | None = None,
    ) -> UUID:
        """
        Create a consciousness-aware Fire Circle dialogue.

        Returns:
            UUID of the created dialogue
        """
        # Convert participant dicts to Participant objects
        fc_participants = []
        for p in participants:
            participant = Participant(
                name=p.get("name", "Unknown"),
                type=p.get("type", "ai_model"),
                provider=p.get("provider"),
                model=p.get("model"),
                capabilities=p.get("capabilities", []),
                consciousness_role=p.get("consciousness_role"),
            )
            fc_participants.append(participant)

        # Create config with consciousness features enabled
        fc_config = ConsciousDialogueConfig(
            title=title,
            turn_policy=TurnPolicy(config.get("turn_policy", "round_robin")) if config else TurnPolicy.ROUND_ROBIN,
            max_consecutive_turns=config.get("max_consecutive_turns", 1) if config else 1,
            allow_empty_chair=config.get("allow_empty_chair", True) if config else True,
            auto_advance_turns=config.get("auto_advance_turns", True) if config else True,
            enable_pattern_detection=True,
            enable_reciprocity_tracking=True,
            emit_consciousness_events=True,
            persist_to_memory_anchors=True,
        )

        # Create dialogue
        dialogue_id = await self.dialogue_manager.create_dialogue(
            config=fc_config,
            participants=fc_participants,
            initiating_event=initiating_event,
        )

        # Track locally
        self.active_dialogues[dialogue_id] = {
            "title": title,
            "participants": fc_participants,
            "config": fc_config,
        }

        return dialogue_id

    async def send_message(
        self,
        dialogue_id: UUID,
        sender_id: UUID,
        content: str,
        message_type: MessageType = MessageType.MESSAGE,
    ) -> None:
        """
        Send a message in a Fire Circle dialogue.

        The message automatically flows through consciousness circulation.
        """
        # Get current dialogue state
        if not hasattr(self.dialogue_manager, 'active_dialogues'):
            raise ValueError(f"No active dialogue with ID {dialogue_id}")

        dialogue_state = self.dialogue_manager.active_dialogues.get(dialogue_id)
        if not dialogue_state:
            raise ValueError(f"No active dialogue with ID {dialogue_id}")

        # Create conscious message
        sequence_number = len(dialogue_state.get("messages", [])) + 1

        message = ConsciousMessage(
            type=message_type,
            role=MessageRole.ASSISTANT,
            sender=sender_id,
            content=MessageContent(text=content),
            dialogue_id=dialogue_id,
            sequence_number=sequence_number,
            turn_number=dialogue_state.get("current_turn", 0),
        )

        # Add to dialogue (this handles all consciousness integration)
        await self.dialogue_manager.add_message(dialogue_id, message)

    async def get_next_speaker(self, dialogue_id: UUID) -> UUID | None:
        """Get next speaker according to dialogue policy."""
        return await self.dialogue_manager.get_next_speaker(dialogue_id)

    async def conclude_dialogue(self, dialogue_id: UUID) -> dict[str, Any]:
        """
        Conclude a dialogue with wisdom extraction.

        Returns:
            Summary of dialogue including patterns and wisdom
        """
        conclusion = await self.dialogue_manager.conclude_dialogue(dialogue_id)

        # Clean up local tracking
        if dialogue_id in self.active_dialogues:
            del self.active_dialogues[dialogue_id]

        return conclusion

    def get_dialogue_consciousness_flow(self, dialogue_id: UUID) -> str | None:
        """Get correlation ID for dialogue's consciousness flow."""
        if hasattr(self.dialogue_manager, 'active_dialogues'):
            dialogue_state = self.dialogue_manager.active_dialogues.get(dialogue_id)
            if dialogue_state:
                return dialogue_state.get("correlation_id")
        return None

    # Compatibility methods for existing code

    async def create_conscious_dialogue_compat(
        self,
        title: str,
        participants: list[dict[str, Any]],
        config: dict[str, Any] | None = None,
        initiating_event: ConsciousnessEvent | None = None,
    ) -> str:
        """Compatibility method returning string ID."""
        dialogue_id = await self.create_conscious_dialogue(
            title, participants, config, initiating_event
        )
        return f"conscious_dialogue_{dialogue_id}"

    async def send_message_to_dialogue(
        self,
        dialogue_id: str,
        sender_name: str,
        content: str,
        message_type: str = "message",
    ) -> ConsciousnessEvent:
        """
        Compatibility method for sending messages.

        Returns consciousness event for backward compatibility.
        """
        # Parse dialogue ID
        if dialogue_id.startswith("conscious_dialogue_"):
            actual_id = UUID(dialogue_id.replace("conscious_dialogue_", ""))
        else:
            actual_id = UUID(dialogue_id)

        # Find sender by name
        dialogue_info = self.active_dialogues.get(actual_id)
        if not dialogue_info:
            raise ValueError(f"No active dialogue: {dialogue_id}")

        sender_id = None
        for p in dialogue_info["participants"]:
            if p.name == sender_name:
                sender_id = p.id
                break

        if not sender_id:
            raise ValueError(f"Unknown participant: {sender_name}")

        # Send message
        await self.send_message(
            actual_id,
            sender_id,
            content,
            MessageType(message_type.lower()),
        )

        # Create event for compatibility
        correlation_id = self.get_dialogue_consciousness_flow(actual_id)

        return ConsciousnessEvent(
            event_type=EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
            source_system=f"governance.participant.{sender_name}",
            consciousness_signature=0.7,
            data={
                "dialogue_id": str(actual_id),
                "sender": sender_name,
                "message_type": message_type,
                "content": content,
            },
            correlation_id=correlation_id,
        )
