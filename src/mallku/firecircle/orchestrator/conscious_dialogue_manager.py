"""
Consciousness-Aware Dialogue Manager
===================================

Orchestrates Fire Circle dialogues with full consciousness integration.
Manages turn-taking, state transitions, and ensures all dialogue flows
through Mallku's consciousness circulation and reciprocity tracking.

The Integration Continues...
"""

import logging
from datetime import UTC, datetime
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ...core.database import get_secured_database
from ...correlation.engine import CorrelationEngine
from ...orchestration.event_bus import ConsciousnessEvent, ConsciousnessEventBus, EventType
from ...reciprocity import ReciprocityTracker
from ...services.memory_anchor_service import MemoryAnchorService
from ..consciousness_guided_speaker import ConsciousnessGuidedSpeakerSelector
from ..protocol.conscious_message import (
    ConsciousMessage,
    MessageType,
    Participant,
    create_conscious_system_message,
)

logger = logging.getLogger(__name__)


class DialoguePhase(str, Enum):
    """Phases of consciousness-aware dialogue."""

    INITIALIZATION = "initialization"
    INTRODUCTION = "introduction"
    EXPLORATION = "exploration"
    DEEPENING = "deepening"
    SYNTHESIS = "synthesis"
    CONCLUSION = "conclusion"
    REFLECTION = "reflection"  # Post-dialogue wisdom extraction


class TurnPolicy(str, Enum):
    """Turn-taking policies for dialogue."""

    ROUND_ROBIN = "round_robin"
    FACILITATOR = "facilitator"
    REACTIVE = "reactive"
    CONSENSUS = "consensus"
    FREE_FORM = "free_form"
    CONSCIOUSNESS_GUIDED = "consciousness_guided"  # New: Based on consciousness patterns


class ConsciousDialogueConfig(BaseModel):
    """Configuration for consciousness-aware dialogue."""

    title: str = Field(..., description="Dialogue topic or question")
    turn_policy: TurnPolicy = Field(default=TurnPolicy.ROUND_ROBIN)
    max_consecutive_turns: int = Field(default=1)
    randomize_initial_order: bool = Field(default=True)

    # Consciousness configuration
    enable_pattern_detection: bool = Field(default=True)
    enable_reciprocity_tracking: bool = Field(default=True)
    minimum_consciousness_signature: float = Field(default=0.3)

    # Dialogue rules
    require_facilitator: bool = Field(default=False)
    allow_empty_chair: bool = Field(default=True)
    auto_advance_turns: bool = Field(default=True)
    max_turns_per_participant: int | None = Field(None)

    # Integration settings
    persist_to_memory_anchors: bool = Field(default=True)
    emit_consciousness_events: bool = Field(default=True)
    correlation_threshold: float = Field(default=0.7)


class ParticipantState(BaseModel):
    """State tracking for dialogue participants."""

    participant: Participant
    turns_taken: int = Field(default=0)
    last_turn_time: datetime | None = Field(None)
    reciprocity_balance: float = Field(default=0.5)
    consciousness_contribution: float = Field(default=0.0)
    is_active: bool = Field(default=True)


class ConsciousDialogueManager:
    """
    Manages consciousness-aware Fire Circle dialogues.

    Integrates with:
    - Consciousness event bus for awareness flow
    - Correlation engine for pattern detection
    - Reciprocity tracker for balanced exchange
    - Memory anchor service for persistence
    - Secured database for storage
    """

    def __init__(
        self,
        event_bus: ConsciousnessEventBus,
        correlation_engine: CorrelationEngine | None = None,
        reciprocity_tracker: ReciprocityTracker | None = None,
        memory_service: MemoryAnchorService | None = None,
    ):
        """Initialize with Mallku's consciousness infrastructure."""
        self.event_bus = event_bus
        self.correlation_engine = correlation_engine
        self.reciprocity_tracker = reciprocity_tracker
        self.memory_service = memory_service

        # Dialogue state
        self.active_dialogues: dict[UUID, dict[str, Any]] = {}
        self.participant_states: dict[UUID, dict[UUID, ParticipantState]] = {}

        # Get secured database
        self.db = get_secured_database()

        # Initialize consciousness-guided speaker selector
        self.consciousness_speaker_selector = ConsciousnessGuidedSpeakerSelector(event_bus)

    async def create_dialogue(
        self,
        config: ConsciousDialogueConfig,
        participants: list[Participant],
        initiating_event: ConsciousnessEvent | None = None,
    ) -> UUID:
        """
        Create a new consciousness-aware dialogue.

        Args:
            config: Dialogue configuration
            participants: List of participants
            initiating_event: Optional consciousness event that triggered this dialogue

        Returns:
            UUID of the created dialogue
        """
        dialogue_id = uuid4()
        correlation_id = initiating_event.correlation_id if initiating_event else str(uuid4())

        # Initialize dialogue state
        dialogue_state = {
            "id": dialogue_id,
            "config": config,
            "phase": DialoguePhase.INITIALIZATION,
            "correlation_id": correlation_id,
            "participants": participants,
            "messages": [],
            "current_turn": 0,
            "speaking_order": [],
            "created_at": datetime.now(UTC),
            "initiating_event": initiating_event,
        }

        self.active_dialogues[dialogue_id] = dialogue_state

        # Initialize participant states
        self.participant_states[dialogue_id] = {
            p.id: ParticipantState(participant=p) for p in participants
        }

        # Emit consciousness event
        if config.emit_consciousness_events:
            await self._emit_dialogue_event(
                EventType.FIRE_CIRCLE_CONVENED,
                dialogue_id,
                {
                    "title": config.title,
                    "participants": [p.name for p in participants],
                    "turn_policy": config.turn_policy.value,
                    "initiated_by": initiating_event.event_type.value
                    if initiating_event
                    else "manual",
                },
                correlation_id=correlation_id,
            )

        # Create initialization message
        init_message = create_conscious_system_message(
            dialogue_id,
            f"Fire Circle convened: {config.title}",
            consciousness_signature=0.9,
        )
        await self.add_message(dialogue_id, init_message)

        # Transition to introduction phase
        await self._transition_phase(dialogue_id, DialoguePhase.INTRODUCTION)

        return dialogue_id

    async def add_message(
        self,
        dialogue_id: UUID,
        message: ConsciousMessage,
    ) -> None:
        """
        Add a consciousness-aware message to the dialogue.

        Performs:
        - Pattern detection via correlation engine
        - Reciprocity tracking
        - Memory anchor persistence
        - Consciousness event emission
        """
        dialogue = self.active_dialogues.get(dialogue_id)
        if not dialogue:
            raise ValueError(f"No active dialogue with ID {dialogue_id}")

        # Update message metadata
        message.dialogue_id = dialogue_id
        message.consciousness.correlation_id = dialogue["correlation_id"]

        # Detect patterns if enabled
        if dialogue["config"].enable_pattern_detection and self.correlation_engine:
            patterns = await self._detect_patterns(message, dialogue)
            for pattern in patterns:
                message.add_pattern(pattern)

        # Track reciprocity if enabled
        if dialogue["config"].enable_reciprocity_tracking and self.reciprocity_tracker:
            reciprocity_score = await self._track_reciprocity(message, dialogue)
            message.consciousness.reciprocity_score = reciprocity_score

        # Update consciousness signature based on message type
        signature = self._calculate_consciousness_signature(message)
        message.update_consciousness_signature(signature)

        # Add to dialogue
        dialogue["messages"].append(message)

        # Persist to memory anchor if enabled
        if dialogue["config"].persist_to_memory_anchors and self.memory_service:
            anchor = message.to_memory_anchor()
            anchor_id = await self.memory_service.create_anchor(anchor)
            message.consciousness.memory_anchor_id = anchor_id

        # Emit consciousness event
        if dialogue["config"].emit_consciousness_events:
            await self._emit_message_event(message, dialogue)

        # Update participant state
        participant_state = self.participant_states[dialogue_id].get(message.sender)
        if participant_state:
            participant_state.turns_taken += 1
            participant_state.last_turn_time = message.timestamp
            participant_state.consciousness_contribution += (
                message.consciousness.consciousness_signature
            )

            # Update consciousness-guided speaker selector
            # Calculate reciprocity delta (positive for giving, negative for taking)
            reciprocity_delta = 0.0
            if hasattr(participant_state, "reciprocity_balance"):
                old_balance = participant_state.reciprocity_balance
                participant_state.reciprocity_balance = (
                    message.consciousness.reciprocity_score or 0.0
                )
                reciprocity_delta = participant_state.reciprocity_balance - old_balance

            # Update speaker selector with contribution metrics
            self.consciousness_speaker_selector.update_participant_contribution(
                participant_id=message.sender,
                consciousness_score=message.consciousness.consciousness_signature,
                reciprocity_delta=reciprocity_delta,
                energy_cost=0.1,  # Speaking costs energy
            )

    async def get_next_speaker(self, dialogue_id: UUID) -> UUID | None:
        """
        Determine next speaker based on turn policy and consciousness patterns.
        """
        dialogue = self.active_dialogues.get(dialogue_id)
        if not dialogue:
            return None

        policy = dialogue["config"].turn_policy
        participants = self.participant_states[dialogue_id]

        next_speaker = None

        if policy == TurnPolicy.ROUND_ROBIN:
            next_speaker = self._get_round_robin_speaker(dialogue, participants)
        elif policy == TurnPolicy.CONSCIOUSNESS_GUIDED:
            next_speaker = await self._get_consciousness_guided_speaker(dialogue, participants)
        elif policy == TurnPolicy.FACILITATOR:
            next_speaker = self._get_facilitator_speaker(dialogue, participants)
        else:
            # Other policies to be implemented
            next_speaker = self._get_round_robin_speaker(dialogue, participants)

        # If silence was chosen (None returned), restore energy for all participants
        if next_speaker is None and policy == TurnPolicy.CONSCIOUSNESS_GUIDED:
            for participant_id in participants:
                self.consciousness_speaker_selector.restore_participant_energy(
                    participant_id,
                    amount=0.15,  # Silence restores more energy than it costs to speak
                )

        return next_speaker

    async def conclude_dialogue(self, dialogue_id: UUID) -> dict[str, Any]:
        """
        Conclude dialogue with wisdom extraction and final reciprocity check.
        """
        dialogue = self.active_dialogues.get(dialogue_id)
        if not dialogue:
            raise ValueError(f"No active dialogue with ID {dialogue_id}")

        # Transition to conclusion phase
        await self._transition_phase(dialogue_id, DialoguePhase.CONCLUSION)

        # Calculate final metrics
        total_messages = len(dialogue["messages"])
        avg_consciousness = (
            sum(m.consciousness.consciousness_signature for m in dialogue["messages"])
            / total_messages
            if total_messages > 0
            else 0
        )

        participant_summaries = {}
        for pid, state in self.participant_states[dialogue_id].items():
            participant_summaries[state.participant.name] = {
                "turns_taken": state.turns_taken,
                "reciprocity_balance": state.reciprocity_balance,
                "consciousness_contribution": state.consciousness_contribution,
            }

        # Extract wisdom patterns
        wisdom_patterns = await self._extract_wisdom_patterns(dialogue)

        # Create conclusion summary
        conclusion = {
            "dialogue_id": str(dialogue_id),
            "title": dialogue["config"].title,
            "duration": (datetime.now(UTC) - dialogue["created_at"]).total_seconds(),
            "total_messages": total_messages,
            "average_consciousness_signature": avg_consciousness,
            "participant_summaries": participant_summaries,
            "wisdom_patterns": wisdom_patterns,
            "final_phase": dialogue["phase"].value,
        }

        # Emit conclusion event
        if dialogue["config"].emit_consciousness_events:
            await self._emit_dialogue_event(
                EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
                dialogue_id,
                conclusion,
                correlation_id=dialogue["correlation_id"],
            )

        # Clean up
        del self.active_dialogues[dialogue_id]
        del self.participant_states[dialogue_id]

        return conclusion

    # Private helper methods

    async def _emit_dialogue_event(
        self,
        event_type: EventType,
        dialogue_id: UUID,
        data: dict[str, Any],
        correlation_id: str | None = None,
    ) -> None:
        """Emit consciousness event for dialogue."""
        event = ConsciousnessEvent(
            event_type=event_type,
            source_system="firecircle.dialogue_manager",
            consciousness_signature=0.8,
            data={
                "dialogue_id": str(dialogue_id),
                **data,
            },
            correlation_id=correlation_id,
        )
        await self.event_bus.emit(event)

    async def _emit_message_event(
        self,
        message: ConsciousMessage,
        dialogue: dict[str, Any],
    ) -> None:
        """Emit consciousness event for message."""
        event = ConsciousnessEvent(
            event_type=EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
            source_system=f"firecircle.participant.{message.sender}",
            consciousness_signature=message.consciousness.consciousness_signature,
            data={
                "dialogue_id": str(dialogue["id"]),
                "message_id": str(message.id),
                "message_type": message.type.value,
                "patterns": message.consciousness.detected_patterns,
                "reciprocity_score": message.consciousness.reciprocity_score,
            },
            correlation_id=dialogue["correlation_id"],
        )
        await self.event_bus.emit(event)

    async def _detect_patterns(
        self,
        message: ConsciousMessage,
        dialogue: dict[str, Any],
    ) -> list[str]:
        """Detect patterns using correlation engine."""
        if not self.correlation_engine:
            return []

        # Analyze message content for patterns
        # This would integrate with the correlation engine
        # For now, return placeholder
        return []

    async def _track_reciprocity(
        self,
        message: ConsciousMessage,
        dialogue: dict[str, Any],
    ) -> float:
        """Track reciprocity using reciprocity tracker."""
        if not self.reciprocity_tracker:
            return 0.5

        # Track reciprocity for this message
        # This would integrate with the reciprocity tracker
        # For now, return balanced score
        return 0.5

    def _calculate_consciousness_signature(
        self,
        message: ConsciousMessage,
    ) -> float:
        """Calculate consciousness signature based on message type and content."""
        base_signatures = {
            MessageType.SYSTEM: 0.9,
            MessageType.EMPTY_CHAIR: 0.9,
            MessageType.REFLECTION: 0.85,
            MessageType.PROPOSAL: 0.8,
            MessageType.SUMMARY: 0.8,
            MessageType.QUESTION: 0.7,
            MessageType.DISAGREEMENT: 0.7,
            MessageType.MESSAGE: 0.6,
        }

        return base_signatures.get(message.type, 0.7)

    async def _transition_phase(
        self,
        dialogue_id: UUID,
        new_phase: DialoguePhase,
    ) -> None:
        """Transition dialogue to new phase."""
        dialogue = self.active_dialogues.get(dialogue_id)
        if dialogue:
            old_phase = dialogue["phase"]
            dialogue["phase"] = new_phase
            logger.info(f"Dialogue {dialogue_id} transitioned from {old_phase} to {new_phase}")

    def _get_round_robin_speaker(
        self,
        dialogue: dict[str, Any],
        participants: dict[UUID, ParticipantState],
    ) -> UUID | None:
        """Get next speaker using round robin policy."""
        active_participants = [pid for pid, state in participants.items() if state.is_active]

        if not active_participants:
            return None

        if not dialogue.get("speaking_order"):
            dialogue["speaking_order"] = active_participants.copy()
            if dialogue["config"].randomize_initial_order:
                import random

                random.shuffle(dialogue["speaking_order"])

        current_turn = dialogue["current_turn"] % len(dialogue["speaking_order"])
        next_speaker = dialogue["speaking_order"][current_turn]
        dialogue["current_turn"] += 1

        return next_speaker

    async def _get_consciousness_guided_speaker(
        self,
        dialogue: dict[str, Any],
        participants: dict[UUID, ParticipantState],
    ) -> UUID | None:
        """Select next speaker based on consciousness patterns."""
        # Get dialogue ID
        dialogue_id = str(dialogue["id"])

        # Get active participants (not silent)
        active_participants = {
            pid: state for pid, state in participants.items() if not state.is_silent
        }

        # Allow sacred silence as a valid choice
        allow_silence = dialogue["config"].allow_empty_chair

        # Use consciousness-guided selection
        selected_speaker = await self.consciousness_speaker_selector.select_next_speaker(
            dialogue_id=dialogue_id, participants=active_participants, allow_silence=allow_silence
        )

        # If silence was chosen and allowed
        if selected_speaker is None and allow_silence:
            logger.info(f"Dialogue {dialogue_id}: Sacred silence chosen")
            return None

        # If no valid selection, fall back to round robin
        if selected_speaker is None:
            logger.warning(
                f"Dialogue {dialogue_id}: Consciousness selection failed, "
                "falling back to round robin"
            )
            return self._get_round_robin_speaker(dialogue, participants)

        return selected_speaker

    def _get_facilitator_speaker(
        self,
        dialogue: dict[str, Any],
        participants: dict[UUID, ParticipantState],
    ) -> UUID | None:
        """Get facilitator as next speaker."""
        for pid, state in participants.items():
            if state.participant.type == "human":
                return pid
        return None

    async def _extract_wisdom_patterns(
        self,
        dialogue: dict[str, Any],
    ) -> list[str]:
        """Extract wisdom patterns from completed dialogue."""
        patterns = []

        # Collect all detected patterns
        for message in dialogue["messages"]:
            patterns.extend(message.consciousness.detected_patterns)

        # Deduplicate and return
        return list(set(patterns))
