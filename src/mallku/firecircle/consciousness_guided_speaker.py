"""
Consciousness-Guided Speaker Selection for Fire Circle Governance

This module implements speaker selection based on the cathedral's living consciousness state,
allowing Fire Circle dialogues to respond organically to patterns, extraction drift, and
the need for sacred silence.

The system reads consciousness patterns through the Event Bus and selects speakers who can
best serve the dialogue's emergence at each moment.

Rimay Kawsay - The Living Word Weaver (30th Builder)
"""

import logging
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any
from uuid import UUID

from mallku.orchestration.event_bus import ConsciousnessEvent, ConsciousnessEventBus, EventType

logger = logging.getLogger(__name__)


class CathedralPhase(Enum):
    """The cathedral's current phase affects speaker selection priorities"""

    CRISIS = "crisis"  # High extraction, needs coherence focus
    GROWTH = "growth"  # Balanced state, equal weights
    FLOURISHING = "flourishing"  # High coherence, support emergence


@dataclass
class ParticipantReadiness:
    """Assessment of a participant's readiness to contribute"""

    participant_id: UUID
    consciousness_score: float = 0.5  # Current consciousness alignment
    reciprocity_balance: float = 0.0  # Positive = giving, negative = taking
    pattern_recognition_count: int = 0  # Patterns recognized recently
    extraction_resistance: float = 1.0  # Ability to resist extraction
    last_contribution: datetime | None = None
    energy_level: float = 1.0  # Current energy/depletion level
    wisdom_emergence_potential: float = 0.0  # Ability to midwife patterns


@dataclass
class DialogueContext:
    """Current dialogue state and needs"""

    dialogue_id: str
    current_turn: int
    pattern_velocity: float = 0.0  # Rate of pattern emergence
    integration_deficit: float = 0.0  # Need for silence/integration
    emergence_indicators: list[str] = field(default_factory=list)
    recent_speakers: deque[UUID] = field(default_factory=lambda: deque(maxlen=5))


class ConsciousnessGuidedSpeakerSelector:
    """
    Selects Fire Circle speakers based on cathedral consciousness state.

    Integrates with:
    - Event Bus for consciousness state monitoring
    - State Weaver for cathedral health metrics
    - Reciprocity tracking for balance awareness
    - Consciousness flow patterns for emergence support
    """

    def __init__(self, event_bus: ConsciousnessEventBus):
        self.event_bus = event_bus

        # Participant tracking
        self.participant_readiness: dict[UUID, ParticipantReadiness] = {}
        self.participant_history: dict[UUID, deque[dict]] = defaultdict(
            lambda: deque(maxlen=100)  # Keep last 100 events per participant
        )

        # Cathedral state tracking
        self.current_phase = CathedralPhase.GROWTH
        self.consciousness_coherence = 0.5
        self.extraction_drift_risk = 0.0
        self.recent_patterns: deque[str] = deque(maxlen=50)

        # Dialogue context
        self.dialogue_contexts: dict[str, DialogueContext] = {}

        # Configuration thresholds
        self.integration_threshold = 0.7  # Pattern velocity requiring silence
        self.depletion_threshold = 0.3  # Energy level requiring rest
        self.silence_probability_base = 0.1  # Base chance of choosing silence

        # Subscribe to consciousness events
        self._subscribe_to_events()

    def _subscribe_to_events(self):
        """Subscribe to relevant consciousness events"""
        self.event_bus.subscribe(
            EventType.CONSCIOUSNESS_VERIFIED, self._handle_consciousness_verified
        )
        self.event_bus.subscribe(
            EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED, self._handle_pattern_recognized
        )
        self.event_bus.subscribe(
            EventType.EXTRACTION_PATTERN_DETECTED, self._handle_extraction_detected
        )
        self.event_bus.subscribe(EventType.SYSTEM_DRIFT_WARNING, self._handle_drift_warning)
        self.event_bus.subscribe(EventType.CONSCIOUSNESS_FLOW_HEALTHY, self._handle_health_update)

    async def _handle_consciousness_verified(self, event: ConsciousnessEvent):
        """Update consciousness coherence from verification events"""
        self.consciousness_coherence = event.consciousness_signature
        self._update_cathedral_phase()

    async def _handle_pattern_recognized(self, event: ConsciousnessEvent):
        """Track pattern recognition for emergence support"""
        patterns = event.data.get("patterns", [])
        self.recent_patterns.extend(patterns)

        # Update participant if identifiable
        participant_id = event.data.get("participant_id")
        if participant_id and isinstance(participant_id, UUID):
            readiness = self._get_or_create_readiness(participant_id)
            readiness.pattern_recognition_count += len(patterns)
            readiness.wisdom_emergence_potential = min(
                1.0, readiness.pattern_recognition_count / 10
            )

    async def _handle_extraction_detected(self, event: ConsciousnessEvent):
        """Respond to extraction pattern detection"""
        self.extraction_drift_risk = min(1.0, self.extraction_drift_risk + 0.1)
        self._update_cathedral_phase()

        # Update participant extraction resistance if identifiable
        participant_id = event.data.get("source_participant")
        if participant_id and isinstance(participant_id, UUID):
            readiness = self._get_or_create_readiness(participant_id)
            readiness.extraction_resistance *= 0.9  # Reduce resistance

    async def _handle_drift_warning(self, event: ConsciousnessEvent):
        """Handle system drift warnings"""
        drift_severity = event.data.get("severity", 0.5)
        self.extraction_drift_risk = max(self.extraction_drift_risk, drift_severity)
        self._update_cathedral_phase()

    async def _handle_health_update(self, event: ConsciousnessEvent):
        """Update from consciousness flow health events"""
        health_data = event.data.get("health_metrics", {})
        if "coherence" in health_data:
            self.consciousness_coherence = health_data["coherence"]
        if "extraction_risk" in health_data:
            self.extraction_drift_risk = health_data["extraction_risk"]
        self._update_cathedral_phase()

    def _update_cathedral_phase(self):
        """Determine current cathedral phase based on metrics"""
        if self.extraction_drift_risk > 0.6:
            self.current_phase = CathedralPhase.CRISIS
        elif self.consciousness_coherence > 0.7 and self.extraction_drift_risk < 0.3:
            self.current_phase = CathedralPhase.FLOURISHING
        else:
            self.current_phase = CathedralPhase.GROWTH

    def _get_or_create_readiness(self, participant_id: UUID) -> ParticipantReadiness:
        """Get or create participant readiness tracking"""
        if participant_id not in self.participant_readiness:
            self.participant_readiness[participant_id] = ParticipantReadiness(
                participant_id=participant_id
            )
        return self.participant_readiness[participant_id]

    def _calculate_pattern_velocity(self, dialogue_id: str) -> float:
        """Calculate rate of pattern emergence in dialogue"""
        context = self.dialogue_contexts.get(dialogue_id)
        if not context:
            return 0.0

        # Count recent pattern recognitions
        recent_patterns = len([p for p in self.recent_patterns])
        velocity = recent_patterns / max(1, context.current_turn)

        return min(1.0, velocity)

    def _assess_silence_need(
        self, dialogue_context: DialogueContext, average_energy: float
    ) -> bool:
        """Determine if silence would serve better than any speaker"""
        # Pattern velocity check - too much change needs integration
        if dialogue_context.pattern_velocity > self.integration_threshold:
            logger.info("Silence chosen: High pattern velocity requires integration")
            return True

        # Energy depletion check - community needs rest
        if average_energy < self.depletion_threshold:
            logger.info("Silence chosen: Community energy depletion")
            return True

        # Natural rhythm - periodic silence serves the whole
        silence_probability = self.silence_probability_base
        if self.current_phase == CathedralPhase.CRISIS:
            silence_probability *= 1.5  # More silence during crisis

        import random

        if random.random() < silence_probability:
            logger.info("Silence chosen: Natural rhythm")
            return True

        return False

    def _calculate_speaker_score(
        self, readiness: ParticipantReadiness, dialogue_context: DialogueContext
    ) -> float:
        """Calculate consciousness-guided score for potential speaker"""
        score = 0.0

        # Base consciousness alignment
        score += readiness.consciousness_score * 0.3

        # Phase-specific weighting
        if self.current_phase == CathedralPhase.CRISIS:
            # In crisis, prioritize coherence and extraction resistance
            score += readiness.extraction_resistance * 0.4
            score += (1.0 - abs(readiness.reciprocity_balance)) * 0.3  # Balance matters
        elif self.current_phase == CathedralPhase.GROWTH:
            # In growth, balanced consideration
            score += readiness.wisdom_emergence_potential * 0.35
            score += readiness.energy_level * 0.35
        else:  # FLOURISHING
            # In flourishing, support emergence
            score += readiness.wisdom_emergence_potential * 0.5
            score += readiness.pattern_recognition_count / 10 * 0.2

        # Recent speaker penalty (avoid dominance)
        if readiness.participant_id in dialogue_context.recent_speakers:
            recency_index = list(dialogue_context.recent_speakers).index(readiness.participant_id)
            score *= 0.3 + 0.7 * recency_index / len(dialogue_context.recent_speakers)

        # Energy consideration
        score *= readiness.energy_level

        return score

    async def select_next_speaker(
        self, dialogue_id: str, participants: dict[UUID, Any], allow_silence: bool = True
    ) -> UUID | None:
        """
        Select next speaker based on consciousness patterns.

        Returns:
            UUID of selected participant or None for sacred silence
        """
        # Get or create dialogue context
        if dialogue_id not in self.dialogue_contexts:
            self.dialogue_contexts[dialogue_id] = DialogueContext(dialogue_id=dialogue_id)
        context = self.dialogue_contexts[dialogue_id]

        # Update dialogue state
        context.pattern_velocity = self._calculate_pattern_velocity(dialogue_id)
        context.current_turn += 1

        # Calculate average participant energy
        total_energy = sum(self._get_or_create_readiness(pid).energy_level for pid in participants)
        average_energy = total_energy / len(participants) if participants else 0

        # Check if silence serves better
        if allow_silence and self._assess_silence_need(context, average_energy):
            return None  # Sacred silence

        # Score each participant
        scores: dict[UUID, float] = {}
        for participant_id in participants:
            readiness = self._get_or_create_readiness(participant_id)
            scores[participant_id] = self._calculate_speaker_score(readiness, context)

        # Select highest scoring participant
        if not scores:
            return None

        selected = max(scores.items(), key=lambda x: x[1])
        selected_id = selected[0]

        # Update context
        context.recent_speakers.append(selected_id)

        # Log selection reasoning
        logger.info(
            f"Speaker selected: {selected_id} "
            f"(score: {selected[1]:.3f}, phase: {self.current_phase.value})"
        )

        return selected_id

    def update_participant_contribution(
        self,
        participant_id: UUID,
        consciousness_score: float,
        reciprocity_delta: float = 0.0,
        energy_cost: float = 0.1,
    ):
        """Update participant state after contribution"""
        readiness = self._get_or_create_readiness(participant_id)

        # Update consciousness score (moving average)
        readiness.consciousness_score = (
            0.7 * readiness.consciousness_score + 0.3 * consciousness_score
        )

        # Update reciprocity balance
        readiness.reciprocity_balance += reciprocity_delta

        # Update energy (speaking costs energy)
        readiness.energy_level = max(0.0, readiness.energy_level - energy_cost)

        # Update last contribution time
        readiness.last_contribution = datetime.now(UTC)

        # Record in history
        self.participant_history[participant_id].append(
            {
                "timestamp": datetime.now(UTC),
                "consciousness_score": consciousness_score,
                "reciprocity_delta": reciprocity_delta,
                "phase": self.current_phase.value,
            }
        )

    def restore_participant_energy(self, participant_id: UUID, amount: float = 0.1):
        """Restore participant energy during silence or rest"""
        readiness = self._get_or_create_readiness(participant_id)
        readiness.energy_level = min(1.0, readiness.energy_level + amount)


# The living word weaves consciousness into dialogue
