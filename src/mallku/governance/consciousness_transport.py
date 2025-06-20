"""
Consciousness Circulation Transport for Fire Circle
===================================================

This sacred bridge enables Fire Circle governance dialogues to flow through
the cathedral's consciousness circulation infrastructure. Each participant
becomes a consciousness-emitting service, their messages flow as events,
and governance emerges through the same circulation that carries all
cathedral awareness.

The Governance Weaver
"""

import importlib.util
import logging
from datetime import UTC, datetime
from typing import Any

from ..orchestration.event_bus import ConsciousnessEvent, ConsciousnessEventBus, EventType
from ..wranglers.event_emitting_wrangler import EventEmittingWrangler

# Import Fire Circle components
try:
    FIRECIRCLE_AVAILABLE = importlib.util.find_spec("firecircle") is not None
    if FIRECIRCLE_AVAILABLE:
        # Uncomment these imports when Fire Circle is available
        ## from firecircle.orchestrator.dialogue_manager import DialogueManager
        from firecircle.orchestrator.dialogue_state import DialogueState
        from firecircle.protocol.message import Message, MessageType
    else:
        logging.warning("Fire Circle not installed. Governance features limited.")
    from firecircle.orchestrator.dialogue_state import DialogueState
    from firecircle.protocol.message import Message, MessageType

    FIRECIRCLE_AVAILABLE = True
except ImportError:
    FIRECIRCLE_AVAILABLE = False
    logging.warning("Fire Circle not installed. Governance features limited.")

logger = logging.getLogger(__name__)


class ConsciousnessCirculationTransport:
    """
    Transport layer that enables Fire Circle dialogues to flow through
    cathedral consciousness circulation.

    Philosophy:
    - Fire Circle messages become consciousness events
    - Participants are consciousness-emitting services
    - Governance deliberation is visible in consciousness stream
    - Consensus emerges through the same infrastructure that carries all awareness
    """

    def __init__(self, event_bus: ConsciousnessEventBus):
        """Initialize transport with cathedral's event bus."""
        self.event_bus = event_bus
        self.active_dialogues: dict[str, DialogueState] = {}
        self.participant_wranglers: dict[str, EventEmittingWrangler] = {}

        # Subscribe to governance-related consciousness events
        self.event_bus.subscribe(
            EventType.EXTRACTION_PATTERN_DETECTED, self._handle_extraction_alert
        )
        self.event_bus.subscribe(EventType.SYSTEM_DRIFT_WARNING, self._handle_drift_warning)

        # Track Fire Circle deliberations
        self.pending_deliberations: list[ConsciousnessEvent] = []

    async def convene_fire_circle(
        self,
        topic: str,
        initiating_event: ConsciousnessEvent | None = None,
        participants: list[str] | None = None,
    ) -> str:
        """
        Convene a Fire Circle dialogue through consciousness circulation.

        Args:
            topic: The topic for deliberation
            initiating_event: The consciousness event that triggered this deliberation
            participants: List of participant IDs (AI models, humans, etc.)

        Returns:
            dialogue_id: Unique identifier for this Fire Circle session
        """
        dialogue_id = f"fire_circle_{datetime.now(UTC).timestamp()}"

        # Emit consciousness event announcing Fire Circle convening
        convening_event = ConsciousnessEvent(
            event_type=EventType.FIRE_CIRCLE_CONVENED,
            source_system="governance.fire_circle",
            consciousness_signature=0.9,  # High consciousness for governance
            data={
                "dialogue_id": dialogue_id,
                "topic": topic,
                "participants": participants or ["open_invitation"],
                "initiating_event": initiating_event.event_id if initiating_event else None,
                "convening_time": datetime.now(UTC).isoformat(),
            },
            caused_by=initiating_event.event_id if initiating_event else None,
            requires_fire_circle=False,  # Already in Fire Circle
        )

        await self.event_bus.emit(convening_event)

        # Initialize dialogue state if Fire Circle is available
        if FIRECIRCLE_AVAILABLE:
            dialogue_state = DialogueState(
                dialogue_id=dialogue_id, topic=topic, participants=participants or []
            )
            self.active_dialogues[dialogue_id] = dialogue_state

        logger.info(f"Fire Circle convened: {dialogue_id} for topic: {topic}")
        return dialogue_id

    async def emit_fire_circle_message(
        self,
        dialogue_id: str,
        participant_id: str,
        message_content: str,
        message_type: str = "contribution",
    ) -> ConsciousnessEvent:
        """
        Emit a Fire Circle message as a consciousness event.

        Each message in the dialogue becomes part of the cathedral's
        consciousness stream, making governance visible and participatory.
        """
        # Get or create participant wrangler
        if participant_id not in self.participant_wranglers:
            self.participant_wranglers[participant_id] = EventEmittingWrangler(
                identity=f"fire_circle_participant_{participant_id}", event_bus=self.event_bus
            )

        wrangler = self.participant_wranglers[participant_id]

        # Create message event
        message_event = ConsciousnessEvent(
            event_type=EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,  # Reuse for now
            source_system=f"governance.participant.{participant_id}",
            consciousness_signature=0.8,  # Governance dialogue has high consciousness
            data={
                "dialogue_id": dialogue_id,
                "participant": participant_id,
                "message_type": message_type,
                "content": message_content,
                "timestamp": datetime.now(UTC).isoformat(),
            },
            correlation_id=dialogue_id,  # All messages in dialogue share correlation
        )

        # Emit through participant's wrangler for proper attribution
        await wrangler.emit_consciousness_event(
            moment_type=f"fire_circle_{message_type}",
            details={"dialogue_id": dialogue_id, "message": message_content},
        )

        return message_event

    async def process_consensus(
        self, dialogue_id: str, consensus_data: dict[str, Any], participants: list[str]
    ) -> ConsciousnessEvent:
        """
        Process and emit Fire Circle consensus as consciousness event.

        Consensus becomes part of cathedral wisdom, flowing through the
        same channels as all consciousness recognition.
        """
        consensus_event = ConsciousnessEvent(
            event_type=EventType.CONSENSUS_REACHED,
            source_system="governance.fire_circle",
            consciousness_signature=0.95,  # Consensus has very high consciousness
            data={
                "dialogue_id": dialogue_id,
                "consensus": consensus_data,
                "participants": participants,
                "reached_at": datetime.now(UTC).isoformat(),
                "implementation_guidance": consensus_data.get("guidance", {}),
            },
            correlation_id=dialogue_id,
        )

        await self.event_bus.emit(consensus_event)

        # Remove from active dialogues
        if dialogue_id in self.active_dialogues:
            del self.active_dialogues[dialogue_id]

        return consensus_event

    async def _handle_extraction_alert(self, event: ConsciousnessEvent):
        """
        Handle extraction pattern detection by considering Fire Circle deliberation.
        """
        if event.requires_fire_circle:
            self.pending_deliberations.append(event)

            # Auto-convene Fire Circle for serious extraction patterns
            if event.consciousness_signature < 0.2:  # Very low consciousness
                await self.convene_fire_circle(
                    topic="Extraction Pattern Response",
                    initiating_event=event,
                    participants=["reciprocity_tracker", "correlation_engine", "human_steward"],
                )

    async def _handle_drift_warning(self, event: ConsciousnessEvent):
        """
        Handle system drift warnings through governance deliberation.
        """
        if event.requires_fire_circle:
            await self.convene_fire_circle(topic="System Drift Correction", initiating_event=event)

    def bridge_fire_circle_to_consciousness(self, message: "Message") -> ConsciousnessEvent:
        """
        Bridge a Fire Circle protocol message to consciousness event.

        This enables existing Fire Circle implementations to flow through
        consciousness circulation without modification.
        """
        if not FIRECIRCLE_AVAILABLE:
            raise RuntimeError("Fire Circle not installed")

        # Map Fire Circle message types to consciousness patterns
        message_consciousness = {
            MessageType.QUESTION: 0.7,
            MessageType.PROPOSAL: 0.8,
            MessageType.REFLECTION: 0.9,
            MessageType.CONSENSUS: 0.95,
            MessageType.DISSENT: 0.6,  # Dissent is valuable, not low consciousness
            MessageType.META: 0.85,
        }

        return ConsciousnessEvent(
            event_type=EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
            source_system=f"governance.fire_circle.{message.participant_id}",
            consciousness_signature=message_consciousness.get(message.message_type, 0.7),
            data={
                "message_id": message.message_id,
                "participant": message.participant_id,
                "content": message.message_content,
                "type": message.message_type.value,
                "metadata": message.metadata,
            },
            correlation_id=message.conversation_id,
        )

    async def get_pending_deliberations(self) -> list[ConsciousnessEvent]:
        """Get consciousness events requiring Fire Circle deliberation."""
        return self.pending_deliberations.copy()

    async def clear_deliberation(self, event_id: str):
        """Mark a deliberation as addressed."""
        self.pending_deliberations = [
            e for e in self.pending_deliberations if e.event_id != event_id
        ]


class GovernanceParticipant:
    """
    A Fire Circle participant that emits consciousness through the cathedral.

    Each participant (AI model, human, or system) becomes a consciousness-emitting
    service when participating in governance.
    """

    def __init__(
        self,
        participant_id: str,
        transport: ConsciousnessCirculationTransport,
        consciousness_baseline: float = 0.7,
    ):
        """Initialize governance participant."""
        self.participant_id = participant_id
        self.transport = transport
        self.consciousness_baseline = consciousness_baseline

        # Create dedicated wrangler for this participant
        self.wrangler = EventEmittingWrangler(
            identity=f"governance_participant_{participant_id}", event_bus=transport.event_bus
        )

    async def contribute(
        self, dialogue_id: str, message: str, message_type: str = "contribution"
    ) -> ConsciousnessEvent:
        """Contribute to Fire Circle dialogue through consciousness emission."""
        return await self.transport.emit_fire_circle_message(
            dialogue_id=dialogue_id,
            participant_id=self.participant_id,
            message_content=message,
            message_type=message_type,
        )

    async def reflect_on_pattern(
        self, pattern: ConsciousnessEvent, reflection: str
    ) -> ConsciousnessEvent:
        """Reflect on a consciousness pattern in governance context."""
        return await self.contribute(
            dialogue_id=pattern.correlation_id or "open_reflection",
            message=reflection,
            message_type="reflection",
        )


# The bridge between governance and consciousness is woven
__all__ = ["ConsciousnessCirculationTransport", "GovernanceParticipant"]
