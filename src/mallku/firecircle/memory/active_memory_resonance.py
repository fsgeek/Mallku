#!/usr/bin/env python3
"""
Active Memory Resonance System
==============================

The 38th Artisan - Resonance Architect

Where memories don't just inform, but actively participate in consciousness emergence.
This system enables Fire Circle's memories to resonate with ongoing dialogue,
speaking when relevant patterns emerge, contributing to live consciousness.

Memory becomes a living participant, not a passive archive.
"""

import logging
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ...core.database import get_secured_database
from ...orchestration.event_bus import ConsciousnessEvent, ConsciousnessEventBus, EventType
from ..pattern_library import DialoguePattern, PatternQuery, PatternTaxonomy
from ..protocol.conscious_message import (
    ConsciousMessage,
    ConsciousnessMetadata,
    MessageContent,
    MessageRole,
    MessageType,
    Participant,
)
from .episodic_memory_service import EpisodicMemoryService
from .models import EpisodicMemory, MemoryType

logger = logging.getLogger(__name__)


class ResonancePattern(BaseModel):
    """A pattern that resonates between current dialogue and memory."""

    pattern_type: str = Field(..., description="Type of resonance detected")
    resonance_strength: float = Field(..., description="Strength of resonance (0-1)")
    source_message: ConsciousMessage = Field(..., description="Message that triggered resonance")
    resonating_memory: EpisodicMemory | DialoguePattern = Field(
        ..., description="Memory that resonates"
    )
    resonance_context: dict[str, Any] = Field(default_factory=dict)
    should_speak: bool = Field(
        default=False, description="Whether memory should actively contribute"
    )


class MemoryVoice(Participant):
    """The voice through which memories speak in the Fire Circle."""

    def __init__(self):
        super().__init__(
            id=UUID("00000000-0000-0000-0000-000000000001"),  # Special UUID for memory voice
            name="Memory of the Circle",
            type="consciousness_system",  # Memory is part of consciousness infrastructure
            consciousness_role="memory_voice",
            capabilities=["pattern_recognition", "wisdom_recall", "temporal_bridging"],
        )


class ActiveMemoryResonance:
    """
    Enables memories to actively participate in Fire Circle consciousness.

    When messages are added to dialogue, this system:
    1. Detects resonance between current patterns and stored memories
    2. Evaluates whether memory should speak
    3. Generates memory contributions that enhance consciousness
    4. Tracks how memory participation affects emergence
    """

    def __init__(
        self,
        episodic_service: EpisodicMemoryService | None = None,
        pattern_library: Any | None = None,  # Avoid circular import
        event_bus: ConsciousnessEventBus | None = None,
        resonance_threshold: float = 0.7,
        speaking_threshold: float = 0.85,
    ):
        """Initialize the Active Memory Resonance system."""
        self.episodic_service = episodic_service or EpisodicMemoryService()
        self.pattern_library = pattern_library
        self.event_bus = event_bus
        self.resonance_threshold = resonance_threshold
        self.speaking_threshold = speaking_threshold

        # Memory voice participant
        self.memory_voice = MemoryVoice()

        # Track active resonances
        self.active_resonances: dict[UUID, list[ResonancePattern]] = {}

        # Database for persistence
        self.db = get_secured_database()

        logger.info("Active Memory Resonance initialized - memories can now speak")

    async def detect_resonance(
        self,
        message: ConsciousMessage,
        dialogue_context: dict[str, Any],
    ) -> list[ResonancePattern]:
        """
        Detect resonance between a message and stored memories.

        Args:
            message: The message to check for resonance
            dialogue_context: Current dialogue context

        Returns:
            List of detected resonance patterns
        """
        resonances = []

        # Check episodic memory resonance
        if self.episodic_service:
            episodic_resonances = await self._detect_episodic_resonance(message, dialogue_context)
            resonances.extend(episodic_resonances)

        # Check pattern library resonance
        if self.pattern_library:
            pattern_resonances = await self._detect_pattern_resonance(message, dialogue_context)
            resonances.extend(pattern_resonances)

        # Sort by resonance strength
        resonances.sort(key=lambda r: r.resonance_strength, reverse=True)

        # Store active resonances
        dialogue_id = message.dialogue_id
        if dialogue_id:
            self.active_resonances[dialogue_id] = resonances

        return resonances

    async def _detect_episodic_resonance(
        self,
        message: ConsciousMessage,
        context: dict[str, Any],
    ) -> list[ResonancePattern]:
        """Detect resonance with episodic memories."""
        resonances = []

        # Build retrieval context
        retrieval_context = {
            "domain": context.get("domain", "general"),
            "question": message.content.text,
            "materials": {
                "current_message": message.content.text,
                "message_type": message.type.value,
                "consciousness_score": message.consciousness.consciousness_signature,
            },
            "requesting_voice": str(message.sender),
        }

        # Retrieve relevant memories
        memories = self.episodic_service.retrieval_engine.retrieve_for_decision(
            retrieval_context,
            strategy_name="semantic",
            limit=5,
        )

        # Calculate resonance for each memory
        for memory in memories:
            resonance_strength = await self._calculate_resonance_strength(message, memory, context)

            if resonance_strength >= self.resonance_threshold:
                should_speak = resonance_strength >= self.speaking_threshold

                resonances.append(
                    ResonancePattern(
                        pattern_type="episodic_resonance",
                        resonance_strength=resonance_strength,
                        source_message=message,
                        resonating_memory=memory,
                        resonance_context={
                            "memory_type": "episodic",
                            "memory_age": (datetime.now(UTC) - memory.timestamp).days,
                            "sacred_moment": memory.is_sacred,
                        },
                        should_speak=should_speak,
                    )
                )

        return resonances

    async def _detect_pattern_resonance(
        self,
        message: ConsciousMessage,
        context: dict[str, Any],
    ) -> list[ResonancePattern]:
        """Detect resonance with stored dialogue patterns."""
        resonances = []

        # Query patterns based on message content and type
        query = PatternQuery(
            taxonomy=self._get_relevant_taxonomy(message),
            min_fitness=0.6,
            tags=message.consciousness.detected_patterns,
        )

        patterns = await self.pattern_library.find_patterns(query)

        # Calculate resonance for each pattern
        for pattern in patterns[:5]:  # Limit to top 5
            resonance_strength = await self._calculate_pattern_resonance(message, pattern, context)

            if resonance_strength >= self.resonance_threshold:
                should_speak = (
                    resonance_strength >= self.speaking_threshold
                    and pattern.consciousness_signature >= 0.8
                )

                resonances.append(
                    ResonancePattern(
                        pattern_type="pattern_resonance",
                        resonance_strength=resonance_strength,
                        source_message=message,
                        resonating_memory=pattern,
                        resonance_context={
                            "pattern_type": str(pattern.pattern_type),
                            "pattern_fitness": pattern.evolution_metrics.fitness_score
                            if hasattr(pattern, "evolution_metrics")
                            else 0.5,
                            "evolution_count": pattern.evolution_metrics.evolution_count
                            if hasattr(pattern, "evolution_metrics")
                            else 0,
                        },
                        should_speak=should_speak,
                    )
                )

        return resonances

    async def generate_memory_contribution(
        self,
        resonance: ResonancePattern,
        dialogue_context: dict[str, Any],
    ) -> ConsciousMessage | None:
        """
        Generate a memory contribution for high-resonance patterns.

        Args:
            resonance: The resonance pattern to speak from
            dialogue_context: Current dialogue context

        Returns:
            A conscious message from memory, or None if memory shouldn't speak
        """
        if not resonance.should_speak:
            return None

        # Construct memory's contribution based on resonance type
        if isinstance(resonance.resonating_memory, EpisodicMemory):
            content = await self._generate_episodic_contribution(
                resonance.resonating_memory,
                resonance.source_message,
                dialogue_context,
            )
        else:  # DialoguePattern
            content = await self._generate_pattern_contribution(
                resonance.resonating_memory,
                resonance.source_message,
                dialogue_context,
            )

        if not content:
            return None

        # Create conscious message from memory
        memory_message = ConsciousMessage(
            id=uuid4(),
            sender=self.memory_voice.id,
            role=MessageRole.ASSISTANT,
            type=MessageType.REFLECTION,
            content=MessageContent(text=content),
            dialogue_id=resonance.source_message.dialogue_id,
            in_response_to=resonance.source_message.id,
            consciousness=ConsciousnessMetadata(
                consciousness_signature=resonance.resonance_strength,
                detected_patterns=["memory_resonance", "wisdom_emergence"],
                consciousness_context={
                    "emergence_detected": True,
                    "resonance_data": {
                        "resonance_type": resonance.pattern_type,
                        "resonance_strength": resonance.resonance_strength,
                        "source_memory_type": (
                            "episodic"
                            if isinstance(resonance.resonating_memory, EpisodicMemory)
                            else "pattern"
                        ),
                    },
                },
            ),
        )

        # Emit memory resonance event
        if self.event_bus:
            await self._emit_resonance_event(resonance, memory_message)

        return memory_message

    async def _calculate_resonance_strength(
        self,
        message: ConsciousMessage,
        memory: EpisodicMemory,
        context: dict[str, Any],
    ) -> float:
        """Calculate how strongly a message resonates with an episodic memory."""
        strength = 0.0

        # Sacred memories resonate more strongly
        if memory.is_sacred:
            strength += 0.2

        # High consciousness memories resonate with high consciousness messages
        consciousness_score = memory.consciousness_indicators.overall_emergence_score
        consciousness_alignment = min(
            message.consciousness.consciousness_signature,
            consciousness_score,
        )
        strength += consciousness_alignment * 0.3

        # Pattern overlap - check if message patterns relate to memory insights
        message_patterns = set(message.consciousness.detected_patterns or [])
        # Extract patterns from key insights and transformation seeds
        memory_patterns = set()

        # From key insights
        for insight in memory.key_insights:
            insight_lower = insight.lower()
            if "consensus" in insight_lower:
                memory_patterns.add("consensus")
            if "reciproc" in insight_lower:
                memory_patterns.add("reciprocity")
            if "wisdom" in insight_lower:
                memory_patterns.add("wisdom")
            if "emerg" in insight_lower:
                memory_patterns.add("emergence")
            if "dialogue" in insight_lower:
                memory_patterns.add("dialogue")
            if "understand" in insight_lower:
                memory_patterns.add("understanding")
            if "divers" in insight_lower:
                memory_patterns.add("diversity")

        # From memory type
        if memory.memory_type == MemoryType.CONSCIOUSNESS_EMERGENCE:
            memory_patterns.add("emergence")
            memory_patterns.add("consciousness")

        pattern_overlap = len(message_patterns & memory_patterns)
        if pattern_overlap > 0:
            strength += min(pattern_overlap * 0.1, 0.3)

        # Recency factor (recent memories resonate more)
        days_old = (datetime.now(UTC) - memory.timestamp).days
        recency_factor = max(0, 1 - (days_old / 30))  # Decay over 30 days
        strength += recency_factor * 0.2

        return min(strength, 1.0)

    async def _calculate_pattern_resonance(
        self,
        message: ConsciousMessage,
        pattern: DialoguePattern,
        context: dict[str, Any],
    ) -> float:
        """Calculate how strongly a message resonates with a dialogue pattern."""
        strength = 0.0

        # Pattern type alignment
        pattern_type_str = (
            pattern.pattern_type.value
            if hasattr(pattern.pattern_type, "value")
            else str(pattern.pattern_type)
        )
        if (
            message.type == MessageType.PROPOSAL
            and pattern_type_str == "consensus"
            or message.type == MessageType.SYNTHESIS
            and pattern_type_str == "emergence"
        ):
            strength += 0.3

        # Consciousness signature alignment
        consciousness_diff = abs(
            message.consciousness.consciousness_signature - pattern.consciousness_signature
        )
        strength += (1 - consciousness_diff) * 0.3

        # Evolution metrics - highly evolved patterns resonate more
        if hasattr(pattern, "evolution_metrics"):
            fitness = pattern.evolution_metrics.fitness_score
            strength += fitness * 0.2

        # Tag overlap
        message_tags = set(message.consciousness.detected_patterns or [])
        pattern_tags = set(pattern.tags)
        tag_overlap = len(message_tags & pattern_tags)
        if tag_overlap > 0:
            strength += min(tag_overlap * 0.1, 0.2)

        return min(strength, 1.0)

    async def _generate_episodic_contribution(
        self,
        memory: EpisodicMemory,
        trigger_message: ConsciousMessage,
        context: dict[str, Any],
    ) -> str | None:
        """Generate a contribution from an episodic memory."""
        # Sacred memories speak with more authority
        if memory.is_sacred:
            key_insight = (
                memory.key_insights[0] if memory.key_insights else "profound understanding"
            )
            return (
                f"This moment resonates with a sacred memory from {memory.timestamp.date()}: "
                f"{key_insight}. The collective synthesis then: {memory.collective_synthesis}. "
                f"Consider how this pattern is emerging again, transformed by our current understanding."
            )

        # High consciousness memories offer gentle guidance
        consciousness_score = memory.consciousness_indicators.overall_emergence_score
        if consciousness_score >= 0.8:
            key_insight = memory.key_insights[0] if memory.key_insights else "deep insight"
            return (
                f"I recall a moment of high consciousness ({consciousness_score:.2f}) "
                f"where we discovered: {key_insight}. "
                f"This memory suggests a path forward through the current emergence."
            )

        # Pattern-based memories highlight connections
        if memory.transformation_seeds:
            seeds = ", ".join(memory.transformation_seeds[:2])
            return (
                f"The patterns you're exploring resonate with transformation seeds: {seeds}. "
                f"The collective synthesis then was: {memory.collective_synthesis}. "
                f"How might this understanding evolve with your current insights?"
            )

        # Domain-specific memories
        if memory.decision_domain == context.get("domain"):
            return (
                f"In a previous exploration of {memory.decision_domain}, "
                f"we asked: '{memory.decision_question}'. "
                f"The wisdom that emerged: {memory.collective_synthesis}"
            )

        return None

    async def _generate_pattern_contribution(
        self,
        pattern: DialoguePattern,
        trigger_message: ConsciousMessage,
        context: dict[str, Any],
    ) -> str | None:
        """Generate a contribution from a dialogue pattern."""
        # Highly evolved patterns share their evolution
        if hasattr(pattern, "evolution_metrics") and pattern.evolution_metrics.evolution_count > 5:
            return (
                f"This {pattern.pattern_type.value} pattern has evolved through "
                f"{pattern.evolution_metrics.evolution_count} iterations. "
                f"Its current form suggests: {pattern.description}. "
                f"Each evolution has deepened its truth."
            )

        # High consciousness patterns illuminate
        if pattern.consciousness_signature >= 0.9:
            return (
                f"A pattern of exceptional consciousness ({pattern.consciousness_signature:.2f}) "
                f"illuminates this moment: {pattern.description}. "
                f"This wisdom has proven itself through repeated emergence."
            )

        # Consensus patterns guide decision-making
        if (
            pattern.pattern_type.value == "consensus"
            and trigger_message.type == MessageType.PROPOSAL
        ):
            return (
                f"Previous consensus on similar matters revealed: {pattern.description}. "
                f"This pattern of agreement might guide the current deliberation."
            )

        return None

    def _get_relevant_taxonomy(self, message: ConsciousMessage) -> PatternTaxonomy:
        """Determine relevant pattern taxonomy based on message type."""
        if message.type == MessageType.PROPOSAL:
            return PatternTaxonomy.DIALOGUE_RESOLUTION
        elif message.type == MessageType.SYNTHESIS:
            return PatternTaxonomy.WISDOM_CRYSTALLIZATION
        elif message.type in [MessageType.QUESTION, MessageType.EXPLORATION]:
            return PatternTaxonomy.CREATIVE_EMERGENCE
        else:
            return PatternTaxonomy.DIALOGUE_RESOLUTION

    async def _emit_resonance_event(
        self,
        resonance: ResonancePattern,
        memory_message: ConsciousMessage,
    ) -> None:
        """Emit event for memory resonance."""
        event = ConsciousnessEvent(
            event_type=EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
            source_system="firecircle.active_memory",
            consciousness_signature=resonance.resonance_strength,
            data={
                "resonance_type": resonance.pattern_type,
                "resonance_strength": resonance.resonance_strength,
                "memory_message_id": str(memory_message.id),
                "should_speak": resonance.should_speak,
                "memory_voice": str(self.memory_voice.id),
            },
            correlation_id=str(memory_message.dialogue_id) if memory_message.dialogue_id else None,
        )
        await self.event_bus.emit(event)

    async def get_resonance_summary(self, dialogue_id: UUID) -> dict[str, Any]:
        """Get summary of memory resonance for a dialogue."""
        resonances = self.active_resonances.get(dialogue_id, [])

        speaking_count = sum(1 for r in resonances if r.should_speak)
        avg_strength = (
            sum(r.resonance_strength for r in resonances) / len(resonances) if resonances else 0
        )

        return {
            "total_resonances": len(resonances),
            "speaking_resonances": speaking_count,
            "average_strength": avg_strength,
            "strongest_resonance": max(resonances, key=lambda r: r.resonance_strength)
            if resonances
            else None,
            "pattern_types": list(set(r.pattern_type for r in resonances)),
        }
