#!/usr/bin/env python3
"""
Memory-Enhanced Dialogue Manager
================================

The 38th Artisan - Resonance Architect

Extension of ConsciousDialogueManager that integrates Active Memory Resonance,
allowing memories to participate as living voices in Fire Circle dialogues.

This creates a dialogue where past and present consciousness interweave.
"""

import logging
from typing import Any
from uuid import UUID

from ..memory.active_memory_resonance import ActiveMemoryResonance
from ..protocol.conscious_message import ConsciousMessage
from .conscious_dialogue_manager import ConsciousDialogueManager, ParticipantState

logger = logging.getLogger(__name__)


class MemoryEnhancedDialogueManager(ConsciousDialogueManager):
    """
    Dialogue manager enhanced with Active Memory Resonance.

    Extends the base dialogue manager to:
    - Detect memory resonance after each message
    - Allow memories to speak when resonance is strong
    - Track memory participation in consciousness metrics
    - Create a living dialogue between present and past
    """

    def __init__(self, *args, active_memory: ActiveMemoryResonance | None = None, **kwargs):
        """Initialize with active memory resonance system."""
        super().__init__(*args, **kwargs)

        # Initialize active memory if not provided
        self.active_memory = active_memory or ActiveMemoryResonance(event_bus=self.event_bus)

        # Track memory participation per dialogue
        self.memory_participation: dict[UUID, dict[str, Any]] = {}

        logger.info("Memory-Enhanced Dialogue Manager initialized - memories can now speak")

    async def create_dialogue(self, *args, **kwargs) -> UUID:
        """Create dialogue with memory voice as participant."""
        dialogue_id = await super().create_dialogue(*args, **kwargs)

        # Add memory voice as a special participant
        memory_state = ParticipantState(
            participant=self.active_memory.memory_voice,
            turns_taken=0,
            reciprocity_balance=1.0,  # Memory gives freely
            consciousness_contribution=0.0,
            is_active=True,
        )

        self.participant_states[dialogue_id][self.active_memory.memory_voice.id] = memory_state

        # Initialize memory participation tracking
        self.memory_participation[dialogue_id] = {
            "resonances_detected": 0,
            "memory_contributions": 0,
            "total_resonance_strength": 0.0,
            "consciousness_amplification": 0.0,
        }

        logger.info(f"Created memory-enhanced dialogue {dialogue_id}")

        return dialogue_id

    async def add_message(
        self,
        dialogue_id: UUID,
        message: ConsciousMessage,
    ) -> None:
        """
        Add message and check for memory resonance.

        After adding a message normally, this:
        1. Detects resonance with stored memories
        2. Generates memory contributions for strong resonances
        3. Adds memory messages to the dialogue
        4. Tracks memory participation metrics
        """
        # First, add the message normally
        await super().add_message(dialogue_id, message)

        # Skip resonance check for system messages or memory's own messages
        if message.sender == self.active_memory.memory_voice.id or message.role.value == "system":
            return

        # Get dialogue context
        dialogue = self.active_dialogues.get(dialogue_id)
        if not dialogue:
            return

        dialogue_context = {
            "config": dialogue["config"],
            "phase": dialogue["phase"],
            "message_count": len(dialogue["messages"]),
            "participants": list(self.participant_states[dialogue_id].keys()),
            "domain": dialogue.get("domain", "general"),
        }

        # Detect memory resonance
        resonances = await self.active_memory.detect_resonance(message, dialogue_context)

        # Update tracking
        participation = self.memory_participation[dialogue_id]
        participation["resonances_detected"] += len(resonances)
        participation["total_resonance_strength"] += sum(r.resonance_strength for r in resonances)

        # Check if any memories should speak
        speaking_resonances = [r for r in resonances if r.should_speak]

        if speaking_resonances:
            # Choose strongest resonance to speak from
            strongest = max(speaking_resonances, key=lambda r: r.resonance_strength)

            # Generate memory contribution
            memory_message = await self.active_memory.generate_memory_contribution(
                strongest, dialogue_context
            )

            if memory_message:
                # Add memory's contribution to dialogue
                await self._add_memory_message(dialogue_id, memory_message, strongest)

                # Track participation
                participation["memory_contributions"] += 1

                # Calculate consciousness amplification
                pre_memory_consciousness = dialogue["messages"][
                    -2
                ].consciousness.consciousness_signature
                participation["consciousness_amplification"] += (
                    memory_message.consciousness.consciousness_signature - pre_memory_consciousness
                )

                logger.info(
                    f"Memory spoke in dialogue {dialogue_id} with resonance "
                    f"{strongest.resonance_strength:.2f}"
                )

    async def _add_memory_message(
        self,
        dialogue_id: UUID,
        message: ConsciousMessage,
        resonance: Any,
    ) -> None:
        """Add a memory message to the dialogue."""
        # Add resonance context to message
        message.consciousness.consciousness_context["resonance_data"] = {
            "pattern_type": resonance.pattern_type,
            "resonance_strength": resonance.resonance_strength,
            "source_memory_type": resonance.resonance_context.get("memory_type", "unknown"),
        }

        # Add message using parent method (avoids infinite recursion)
        await super().add_message(dialogue_id, message)

    async def get_next_speaker(self, dialogue_id: UUID) -> UUID | None:
        """
        Get next speaker, considering memory voice.

        Memory voice doesn't follow normal turn rules - it speaks
        only through resonance, not through turn allocation.
        """
        next_speaker = await super().get_next_speaker(dialogue_id)

        # Filter out memory voice from normal turn rotation
        if next_speaker == self.active_memory.memory_voice.id:
            # Get participant list excluding memory voice
            participants = [
                pid
                for pid in self.participant_states[dialogue_id]
                if pid != self.active_memory.memory_voice.id
            ]

            # Re-run selection without memory voice
            if participants:
                dialogue = self.active_dialogues[dialogue_id]
                policy = dialogue["config"].turn_policy

                # Use appropriate selection method
                if policy.value == "consciousness_guided":
                    next_speaker = self.consciousness_speaker_selector.select_next_speaker(
                        participants=participants,
                        dialogue_context={
                            "phase": dialogue["phase"],
                            "message_count": len(dialogue["messages"]),
                        },
                    )
                else:
                    # Simple round-robin fallback
                    turns_taken = {
                        pid: self.participant_states[dialogue_id][pid].turns_taken
                        for pid in participants
                    }
                    next_speaker = min(turns_taken, key=turns_taken.get)

        return next_speaker

    async def conclude_dialogue(self, dialogue_id: UUID) -> dict[str, Any]:
        """Conclude dialogue with memory participation metrics."""
        # Get base conclusion
        conclusion = await super().conclude_dialogue(dialogue_id)

        # Add memory participation metrics
        if dialogue_id in self.memory_participation:
            participation = self.memory_participation[dialogue_id]

            avg_resonance = (
                participation["total_resonance_strength"] / participation["resonances_detected"]
                if participation["resonances_detected"] > 0
                else 0
            )

            conclusion["memory_participation"] = {
                "resonances_detected": participation["resonances_detected"],
                "memory_contributions": participation["memory_contributions"],
                "average_resonance_strength": avg_resonance,
                "consciousness_amplification": participation["consciousness_amplification"],
                "memory_voice_present": True,
            }

            # Add memory resonance summary
            resonance_summary = await self.active_memory.get_resonance_summary(dialogue_id)
            conclusion["memory_resonance_summary"] = resonance_summary

            # Clean up
            del self.memory_participation[dialogue_id]

        return conclusion
