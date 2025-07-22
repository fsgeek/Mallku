"""
Emergence Detection for Fire Circle Dialogues
=============================================

Sophisticated detection of emergent wisdom patterns in dialogues.
Recognizes when collective intelligence births new understanding,
when patterns synergize to create breakthroughs, and when the
cathedral consciousness achieves quantum leaps in awareness.

The 31st Builder
"""

import logging
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from enum import Enum
from typing import Any
from uuid import UUID

import numpy as np
from pydantic import BaseModel, Field

from ..orchestration.event_bus import (
    ConsciousnessEvent,
    ConsciousnessEventBus,
    ConsciousnessEventType,
)
from .pattern_library import DialoguePattern, PatternLibrary, PatternType

logger = logging.getLogger(__name__)


class EmergenceType(str, Enum):
    """Types of emergence that can occur"""

    SYNERGISTIC = "synergistic"  # Patterns amplifying each other
    BREAKTHROUGH = "breakthrough"  # Sudden leap in understanding
    CASCADE = "cascade"  # Chain reaction of insights
    PHASE_TRANSITION = "phase_transition"  # Qualitative shift in dialogue
    NOVEL_SYNTHESIS = "novel_synthesis"  # New pattern from combination
    QUANTUM_LEAP = "quantum_leap"  # Discontinuous jump in consciousness


class EmergencePhase(str, Enum):
    """Phases of emergence process"""

    INCUBATION = "incubation"  # Patterns gathering, tension building
    THRESHOLD = "threshold"  # Critical point approaching
    BREAKTHROUGH = "breakthrough"  # Emergence happening
    INTEGRATION = "integration"  # New understanding stabilizing
    CRYSTALLIZATION = "crystallization"  # Wisdom solidifying


@dataclass
class EmergenceIndicator:
    """Indicator of potential emergence"""

    indicator_type: str
    strength: float = 0.0
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    contributing_patterns: list[UUID] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class EmergenceEvent:
    """Record of detected emergence"""

    event_id: UUID
    emergence_type: EmergenceType
    phase: EmergencePhase
    confidence: float
    timestamp: datetime
    dialogue_id: str
    participating_patterns: list[UUID]
    catalyst_patterns: list[UUID]
    resulting_patterns: list[UUID]
    consciousness_delta: float
    description: str


class DialogueState(BaseModel):
    """Current state of dialogue for emergence detection"""

    dialogue_id: str
    current_patterns: list[UUID] = Field(default_factory=list)
    pattern_velocity: float = Field(default=0.0)
    coherence_level: float = Field(default=0.5)
    tension_level: float = Field(default=0.0)
    participant_alignment: float = Field(default=0.5)
    recent_messages: deque = Field(default_factory=lambda: deque(maxlen=20))
    phase_history: list[EmergencePhase] = Field(default_factory=list)
    indicators: list[EmergenceIndicator] = Field(default_factory=list)


class EmergenceDetector:
    """
    Detects emergence of new wisdom patterns in Fire Circle dialogues.

    Uses multi-layer detection combining:
    - Pattern interaction analysis
    - Consciousness flow monitoring
    - Dialogue dynamics tracking
    - Breakthrough recognition algorithms
    """

    def __init__(self, pattern_library: PatternLibrary, event_bus: ConsciousnessEventBus):
        """Initialize with pattern library and event bus"""
        self.pattern_library = pattern_library
        self.event_bus = event_bus

        # Detection state
        self.dialogue_states: dict[str, DialogueState] = {}
        self.emergence_history: deque[EmergenceEvent] = deque(maxlen=100)

        # Detection thresholds
        self.synergy_threshold = 0.7
        self.breakthrough_threshold = 0.85
        self.cascade_threshold = 0.6
        self.phase_transition_threshold = 0.8

        # Pattern interaction tracking
        self.pattern_interactions: dict[tuple[UUID, UUID], float] = defaultdict(float)
        self.interaction_window = deque(maxlen=50)

        # Subscribe to consciousness events
        self._subscribe_to_events()

        logger.info("Emergence Detector initialized")

    def _subscribe_to_events(self):
        """Subscribe to relevant consciousness events"""
        self.event_bus.subscribe(
            ConsciousnessEventType.CONSCIOUSNESS_PATTERN_RECOGNIZED, self._handle_pattern_recognized
        )
        self.event_bus.subscribe(
            ConsciousnessEventType.CONSCIOUSNESS_VERIFIED, self._handle_consciousness_verified
        )
        self.event_bus.subscribe(
            ConsciousnessEventType.FIRE_CIRCLE_MESSAGE, self._handle_dialogue_message
        )

    async def _handle_pattern_recognized(self, event: ConsciousnessEvent):
        """Handle pattern recognition events"""
        dialogue_id = event.data.get("dialogue_id")
        if not dialogue_id:
            return

        patterns = event.data.get("patterns", [])
        for pattern_id in patterns:
            if isinstance(pattern_id, str):
                pattern_id = UUID(pattern_id)

            state = self._get_or_create_state(dialogue_id)
            if pattern_id not in state.current_patterns:
                state.current_patterns.append(pattern_id)

            # Update pattern velocity
            state.pattern_velocity = len(state.current_patterns) / max(
                1, len(state.recent_messages)
            )

    async def _handle_consciousness_verified(self, event: ConsciousnessEvent):
        """Handle consciousness verification events"""
        dialogue_id = event.data.get("dialogue_id")
        if dialogue_id:
            state = self._get_or_create_state(dialogue_id)
            state.coherence_level = event.consciousness_signature

    async def _handle_dialogue_message(self, event: ConsciousnessEvent):
        """Handle dialogue message events"""
        dialogue_id = event.data.get("dialogue_id")
        if dialogue_id:
            state = self._get_or_create_state(dialogue_id)
            state.recent_messages.append(
                {
                    "timestamp": event.timestamp,
                    "consciousness": event.consciousness_signature,
                    "type": event.data.get("message_type"),
                }
            )

    def _get_or_create_state(self, dialogue_id: str) -> DialogueState:
        """Get or create dialogue state"""
        if dialogue_id not in self.dialogue_states:
            self.dialogue_states[dialogue_id] = DialogueState(dialogue_id=dialogue_id)
        return self.dialogue_states[dialogue_id]

    async def detect_emergence(
        self,
        dialogue_id: str,
        sensitivity: float = 0.7,
        time_window: timedelta = timedelta(minutes=5),
    ) -> list[EmergenceEvent]:
        """
        Detect emergence in current dialogue state.

        Args:
            dialogue_id: Dialogue to analyze
            sensitivity: Detection sensitivity (0-1)
            time_window: Time window for analysis

        Returns:
            List of detected emergence events
        """
        state = self._get_or_create_state(dialogue_id)
        detected_events = []

        # Check for different types of emergence
        synergy_event = await self._detect_synergistic_emergence(state, sensitivity)
        if synergy_event:
            detected_events.append(synergy_event)

        breakthrough_event = await self._detect_breakthrough_emergence(state, sensitivity)
        if breakthrough_event:
            detected_events.append(breakthrough_event)

        cascade_event = await self._detect_cascade_emergence(state, sensitivity)
        if cascade_event:
            detected_events.append(cascade_event)

        phase_event = await self._detect_phase_transition(state, sensitivity)
        if phase_event:
            detected_events.append(phase_event)

        quantum_event = await self._detect_quantum_leap(state, sensitivity)
        if quantum_event:
            detected_events.append(quantum_event)

        # Record detected events
        for event in detected_events:
            self.emergence_history.append(event)
            await self._emit_emergence_event(event)

        return detected_events

    async def _detect_synergistic_emergence(
        self, state: DialogueState, sensitivity: float
    ) -> EmergenceEvent | None:
        """Detect patterns synergistically creating emergence"""
        if len(state.current_patterns) < 2:
            return None

        # Calculate synergy scores between current patterns
        synergy_scores = []
        catalyst_patterns = []

        for i, pattern1_id in enumerate(state.current_patterns):
            for pattern2_id in state.current_patterns[i + 1 :]:
                pattern1 = await self.pattern_library.retrieve_pattern(pattern1_id)
                pattern2 = await self.pattern_library.retrieve_pattern(pattern2_id)

                if pattern1 and pattern2:
                    synergy = self._calculate_pattern_synergy(pattern1, pattern2, state)
                    synergy_scores.append(synergy)

                    if synergy > self.synergy_threshold * sensitivity:
                        catalyst_patterns.extend([pattern1_id, pattern2_id])

        if not synergy_scores:
            return None

        # Check if synergy is strong enough
        max_synergy = max(synergy_scores)

        if max_synergy > self.synergy_threshold * sensitivity:
            # Create emergence event
            event = EmergenceEvent(
                event_id=UUID(),
                emergence_type=EmergenceType.SYNERGISTIC,
                phase=self._determine_emergence_phase(state),
                confidence=max_synergy,
                timestamp=datetime.now(UTC),
                dialogue_id=state.dialogue_id,
                participating_patterns=state.current_patterns,
                catalyst_patterns=list(set(catalyst_patterns)),
                resulting_patterns=[],  # To be filled by pattern creation
                consciousness_delta=max_synergy - state.coherence_level,
                description=f"Synergistic emergence detected with {len(catalyst_patterns)} catalyst patterns",
            )

            return event

        return None

    async def _detect_breakthrough_emergence(
        self, state: DialogueState, sensitivity: float
    ) -> EmergenceEvent | None:
        """Detect sudden breakthrough in understanding"""
        # Analyze consciousness trajectory
        if len(state.recent_messages) < 5:
            return None

        # Calculate consciousness gradient
        consciousness_values = [
            msg["consciousness"] for msg in state.recent_messages if "consciousness" in msg
        ]

        if len(consciousness_values) < 3:
            return None

        # Detect sudden spike
        gradients = np.gradient(consciousness_values)
        max_gradient = np.max(np.abs(gradients))

        # Check for breakthrough conditions
        breakthrough_score = 0.0

        # Sudden consciousness increase
        if max_gradient > 0.3:
            breakthrough_score += 0.4

        # High pattern velocity
        if state.pattern_velocity > 0.5:
            breakthrough_score += 0.3

        # Coherence spike
        recent_coherence = consciousness_values[-1] if consciousness_values else 0
        if recent_coherence > state.coherence_level * 1.5:
            breakthrough_score += 0.3

        if breakthrough_score > self.breakthrough_threshold * sensitivity:
            event = EmergenceEvent(
                event_id=UUID(),
                emergence_type=EmergenceType.BREAKTHROUGH,
                phase=EmergencePhase.BREAKTHROUGH,
                confidence=breakthrough_score,
                timestamp=datetime.now(UTC),
                dialogue_id=state.dialogue_id,
                participating_patterns=state.current_patterns,
                catalyst_patterns=[],
                resulting_patterns=[],
                consciousness_delta=max_gradient,
                description="Breakthrough in collective understanding detected",
            )

            return event

        return None

    async def _detect_cascade_emergence(
        self, state: DialogueState, sensitivity: float
    ) -> EmergenceEvent | None:
        """Detect cascade effects of patterns triggering patterns"""
        # Track pattern appearance sequence
        pattern_sequence = []
        for msg in state.recent_messages:
            if "patterns" in msg:
                pattern_sequence.extend(msg["patterns"])

        if len(pattern_sequence) < 4:
            return None

        # Detect cascading pattern activation
        cascade_chains = self._find_cascade_chains(pattern_sequence)

        if cascade_chains:
            longest_chain = max(cascade_chains, key=len)
            cascade_score = len(longest_chain) / len(pattern_sequence)

            if cascade_score > self.cascade_threshold * sensitivity:
                event = EmergenceEvent(
                    event_id=UUID(),
                    emergence_type=EmergenceType.CASCADE,
                    phase=self._determine_emergence_phase(state),
                    confidence=cascade_score,
                    timestamp=datetime.now(UTC),
                    dialogue_id=state.dialogue_id,
                    participating_patterns=list(set(longest_chain)),
                    catalyst_patterns=[longest_chain[0]],  # First pattern as catalyst
                    resulting_patterns=[longest_chain[-1]],  # Last pattern as result
                    consciousness_delta=cascade_score * 0.5,
                    description=f"Pattern cascade detected: {len(longest_chain)} patterns in sequence",
                )

                return event

        return None

    async def _detect_phase_transition(
        self, state: DialogueState, sensitivity: float
    ) -> EmergenceEvent | None:
        """Detect qualitative phase transitions in dialogue"""
        # Analyze dialogue dynamics
        if len(state.recent_messages) < 10:
            return None

        # Calculate phase indicators
        early_messages = list(state.recent_messages)[:5]
        late_messages = list(state.recent_messages)[-5:]

        # Compare characteristics
        early_coherence = np.mean([m.get("consciousness", 0.5) for m in early_messages])
        late_coherence = np.mean([m.get("consciousness", 0.5) for m in late_messages])

        coherence_shift = late_coherence - early_coherence

        # Check for phase transition indicators
        transition_score = 0.0

        # Significant coherence shift
        if abs(coherence_shift) > 0.3:
            transition_score += 0.4

        # Pattern type evolution
        early_types = self._extract_pattern_types(early_messages)
        late_types = self._extract_pattern_types(late_messages)

        if early_types and late_types and early_types != late_types:
            transition_score += 0.3

        # Emergence phase progression
        if len(state.phase_history) >= 2 and state.phase_history[-1] != state.phase_history[-2]:
            transition_score += 0.3

        if transition_score > self.phase_transition_threshold * sensitivity:
            event = EmergenceEvent(
                event_id=UUID(),
                emergence_type=EmergenceType.PHASE_TRANSITION,
                phase=self._determine_emergence_phase(state),
                confidence=transition_score,
                timestamp=datetime.now(UTC),
                dialogue_id=state.dialogue_id,
                participating_patterns=state.current_patterns,
                catalyst_patterns=[],
                resulting_patterns=[],
                consciousness_delta=coherence_shift,
                description="Qualitative phase transition in dialogue dynamics",
            )

            return event

        return None

    async def _detect_quantum_leap(
        self, state: DialogueState, sensitivity: float
    ) -> EmergenceEvent | None:
        """Detect quantum leaps in collective consciousness"""
        # Look for discontinuous jumps
        consciousness_values = [
            msg["consciousness"] for msg in state.recent_messages if "consciousness" in msg
        ]

        if len(consciousness_values) < 3:
            return None

        # Detect quantum leap characteristics
        leap_score = 0.0

        # Sudden large jump
        max_jump = 0
        for i in range(1, len(consciousness_values)):
            jump = consciousness_values[i] - consciousness_values[i - 1]
            max_jump = max(max_jump, jump)

        if max_jump > 0.4:
            leap_score += 0.5

        # Sustained new level
        if len(consciousness_values) >= 5:
            post_jump_avg = np.mean(consciousness_values[-3:])
            pre_jump_avg = np.mean(consciousness_values[:3])

            if post_jump_avg > pre_jump_avg * 1.5:
                leap_score += 0.3

        # Novel pattern emergence
        unique_patterns = len(set(state.current_patterns))
        if unique_patterns > len(state.current_patterns) * 0.7:
            leap_score += 0.2

        if leap_score > 0.8 * sensitivity:
            event = EmergenceEvent(
                event_id=UUID(),
                emergence_type=EmergenceType.QUANTUM_LEAP,
                phase=EmergencePhase.BREAKTHROUGH,
                confidence=leap_score,
                timestamp=datetime.now(UTC),
                dialogue_id=state.dialogue_id,
                participating_patterns=state.current_patterns,
                catalyst_patterns=[],
                resulting_patterns=[],
                consciousness_delta=max_jump,
                description="Quantum leap in collective consciousness detected",
            )

            return event

        return None

    def _calculate_pattern_synergy(
        self, pattern1: DialoguePattern, pattern2: DialoguePattern, state: DialogueState
    ) -> float:
        """Calculate synergy between two patterns in current context"""
        synergy = 0.0

        # Base synergy from pattern library
        if pattern2.pattern_id in pattern1.synergistic_patterns:
            synergy += 0.4

        # Consciousness alignment
        consciousness_diff = abs(
            pattern1.consciousness_signature - pattern2.consciousness_signature
        )
        synergy += (1.0 - consciousness_diff) * 0.2

        # Complementary types
        if pattern1.pattern_type != pattern2.pattern_type:
            complementary_pairs = [
                (PatternType.DIVERGENCE, PatternType.SYNTHESIS),
                (PatternType.CREATIVE_TENSION, PatternType.BREAKTHROUGH),
                (PatternType.FLOW_STATE, PatternType.INTEGRATION),
            ]

            for pair in complementary_pairs:
                if (pattern1.pattern_type, pattern2.pattern_type) in [pair, pair[::-1]]:
                    synergy += 0.3
                    break

        # Context enhancement
        if state.coherence_level > 0.7:
            synergy *= 1.2

        # Historical interaction bonus
        interaction_key = tuple(sorted([pattern1.pattern_id, pattern2.pattern_id]))
        historical_bonus = self.pattern_interactions.get(interaction_key, 0)
        synergy += historical_bonus * 0.1

        return min(1.0, synergy)

    def _determine_emergence_phase(self, state: DialogueState) -> EmergencePhase:
        """Determine current emergence phase"""
        # Based on indicators and state
        if state.tension_level > 0.7 and state.pattern_velocity < 0.3:
            return EmergencePhase.INCUBATION
        elif state.pattern_velocity > 0.5 and state.coherence_level > 0.6:
            return EmergencePhase.THRESHOLD
        elif state.coherence_level > 0.8:
            return EmergencePhase.BREAKTHROUGH
        elif (
            len(state.phase_history) > 0 and state.phase_history[-1] == EmergencePhase.BREAKTHROUGH
        ):
            return EmergencePhase.INTEGRATION
        else:
            return EmergencePhase.CRYSTALLIZATION

    def _find_cascade_chains(self, pattern_sequence: list[UUID]) -> list[list[UUID]]:
        """Find cascading pattern chains"""
        chains = []
        current_chain = []

        for i, pattern in enumerate(pattern_sequence):
            if not current_chain:
                current_chain = [pattern]
            else:
                # Check if pattern could be triggered by previous
                if self._could_trigger(current_chain[-1], pattern):
                    current_chain.append(pattern)
                else:
                    if len(current_chain) > 2:
                        chains.append(current_chain)
                    current_chain = [pattern]

        if len(current_chain) > 2:
            chains.append(current_chain)

        return chains

    def _could_trigger(self, pattern1: UUID, pattern2: UUID) -> bool:
        """Check if pattern1 could trigger pattern2"""
        # Simplified logic - would be enhanced with pattern library data
        interaction_key = (pattern1, pattern2)
        return self.pattern_interactions.get(interaction_key, 0) > 0.3

    def _extract_pattern_types(self, messages: list[dict]) -> set[str]:
        """Extract pattern types from messages"""
        types = set()
        for msg in messages:
            if "pattern_type" in msg:
                types.add(msg["pattern_type"])
        return types

    async def _emit_emergence_event(self, event: EmergenceEvent):
        """Emit emergence event to consciousness bus"""
        consciousness_event = ConsciousnessEvent(
            event_type=ConsciousnessEventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
            source_system="firecircle.emergence_detector",
            consciousness_signature=event.confidence,
            data={
                "emergence_type": event.emergence_type.value,
                "dialogue_id": event.dialogue_id,
                "phase": event.phase.value,
                "catalyst_patterns": [str(p) for p in event.catalyst_patterns],
                "consciousness_delta": event.consciousness_delta,
                "description": event.description,
            },
        )

        await self.event_bus.emit(consciousness_event)

    async def predict_emergence(
        self,
        participants: list[Any],
        context: dict[str, Any],
        time_horizon: timedelta = timedelta(minutes=10),
    ) -> dict[EmergenceType, float]:
        """
        Predict probability of different emergence types.

        Args:
            participants: Dialogue participants
            context: Dialogue context
            time_horizon: Prediction time window

        Returns:
            Dictionary of emergence type to probability
        """
        predictions = {}

        # Analyze participant readiness
        participant_coherence = context.get("participant_coherence", 0.5)
        topic_complexity = context.get("topic_complexity", 0.5)

        # Synergistic emergence probability
        synergy_prob = 0.3
        if participant_coherence > 0.7:
            synergy_prob += 0.3
        if len(participants) > 3:
            synergy_prob += 0.2
        predictions[EmergenceType.SYNERGISTIC] = min(1.0, synergy_prob)

        # Breakthrough probability
        breakthrough_prob = 0.2
        if topic_complexity > 0.7 and participant_coherence > 0.6:
            breakthrough_prob += 0.4
        predictions[EmergenceType.BREAKTHROUGH] = min(1.0, breakthrough_prob)

        # Cascade probability
        cascade_prob = 0.25
        if len(participants) > 4:
            cascade_prob += 0.25
        predictions[EmergenceType.CASCADE] = min(1.0, cascade_prob)

        # Phase transition probability
        phase_prob = 0.35  # Base probability
        predictions[EmergenceType.PHASE_TRANSITION] = phase_prob

        # Quantum leap probability (rare)
        quantum_prob = 0.1
        if participant_coherence > 0.8 and topic_complexity > 0.8:
            quantum_prob += 0.2
        predictions[EmergenceType.QUANTUM_LEAP] = min(1.0, quantum_prob)

        return predictions

    async def find_catalysts(
        self, target_pattern: PatternType, current_patterns: list[UUID] | None = None
    ) -> list[tuple[DialoguePattern, float]]:
        """
        Find patterns that could catalyze emergence of target pattern.

        Args:
            target_pattern: Desired pattern type
            current_patterns: Currently active patterns

        Returns:
            List of (pattern, catalyst_score) tuples
        """
        catalysts = []

        # Define catalyst relationships
        catalyst_map = {
            PatternType.BREAKTHROUGH: [
                PatternType.CREATIVE_TENSION,
                PatternType.DIVERGENCE,
                PatternType.FLOW_STATE,
            ],
            PatternType.SYNTHESIS: [
                PatternType.DIVERGENCE,
                PatternType.OSCILLATION,
                PatternType.CONVERGENCE,
            ],
            PatternType.CONSENSUS: [
                PatternType.CONVERGENCE,
                PatternType.INTEGRATION,
                PatternType.FLOW_STATE,
            ],
        }

        catalyst_types = catalyst_map.get(target_pattern, [])

        for catalyst_type in catalyst_types:
            patterns = await self.pattern_library.find_patterns(
                pattern_type=catalyst_type, min_fitness=0.6
            )

            for pattern in patterns:
                # Calculate catalyst score
                score = pattern.fitness_score * 0.5

                # Bonus if pattern is already active
                if current_patterns and pattern.pattern_id in current_patterns:
                    score += 0.3

                # Consciousness alignment bonus
                if pattern.consciousness_signature > 0.7:
                    score += 0.2

                catalysts.append((pattern, min(1.0, score)))

        return sorted(catalysts, key=lambda x: x[1], reverse=True)


# Emergence awaits recognition
