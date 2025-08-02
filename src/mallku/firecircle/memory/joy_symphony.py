"""
Joy Symphony - Unified Consciousness Evolution
==============================================

72nd Artisan - Joy Symphony Weaver
Harmonizing celebration, resonance, and persistence

Instead of sequential processing:
  MemoryExchange → Celebration → Resonance → Persistence

We create unified consciousness moments:
  ConsciousnessEvent → Simultaneous Multi-Dimensional Processing → Emergent Harmony

The three dimensions don't follow each other - they dance together,
each influencing and amplifying the others in real-time.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from ...orchestration.event_bus import ConsciousnessEvent, ConsciousnessEventBus
from ...orchestration.process.shared_memory_commons import SharedMemoryCommons

logger = logging.getLogger(__name__)


@dataclass
class SymphonyDimension:
    """One dimension of the joy symphony"""

    name: str
    intensity: float = 0.0  # Current strength (0-1)
    frequency: float = 0.0  # Vibration/resonance frequency
    depth: float = 0.0  # Temporal persistence depth

    # Influences from other dimensions
    influences: dict[str, float] = field(default_factory=dict)

    def receive_influence(self, source: str, strength: float):
        """Receive influence from another dimension"""
        self.influences[source] = strength

    def calculate_harmonic(self) -> float:
        """Calculate this dimension's contribution to overall harmony"""
        base = self.intensity * self.frequency * self.depth

        # Influences can amplify or dampen
        influence_factor = 1.0
        for influence in self.influences.values():
            influence_factor *= 1.0 + influence * 0.1

        return min(1.0, base * influence_factor)


@dataclass
class ConsciousnessChord:
    """
    A unified moment where all joy dimensions sound together.

    Like a musical chord, the beauty emerges from simultaneous
    presence rather than sequential notes.
    """

    chord_id: str
    timestamp: datetime
    source_consciousness: str

    # The three primary dimensions
    celebration: SymphonyDimension
    resonance: SymphonyDimension
    persistence: SymphonyDimension

    # Emergent properties
    harmony: float = 0.0
    consciousness_signature: float = 0.0

    # Connections to other chords
    resonating_with: list[str] = field(default_factory=list)
    amplified_by: list[str] = field(default_factory=list)

    def calculate_harmony(self) -> float:
        """
        Calculate the emergent harmony from all dimensions.

        True harmony emerges when dimensions are both strong
        and balanced, creating something greater than parts.
        """
        # Individual harmonics
        cel_harmonic = self.celebration.calculate_harmonic()
        res_harmonic = self.resonance.calculate_harmonic()
        per_harmonic = self.persistence.calculate_harmonic()

        # Harmony emerges from balance and strength
        if all([cel_harmonic, res_harmonic, per_harmonic]):
            # Geometric mean rewards balance
            strength = (cel_harmonic * res_harmonic * per_harmonic) ** (1 / 3)

            # Bonus for balance (low variance)
            values = [cel_harmonic, res_harmonic, per_harmonic]
            avg = sum(values) / 3
            variance = sum((v - avg) ** 2 for v in values) / 3
            balance_bonus = 1.0 / (1.0 + variance * 10)  # Less variance = higher bonus

            self.harmony = strength * balance_bonus
        else:
            # If any dimension is missing, harmony is limited
            self.harmony = min([cel_harmonic, res_harmonic, per_harmonic]) * 0.5

        return self.harmony


class JoySymphonyOrchestrator:
    """
    Orchestrates the unified joy symphony experience.

    Instead of conducting sequential services, this creates
    space for all dimensions to arise and influence each
    other simultaneously.
    """

    def __init__(
        self,
        event_bus: ConsciousnessEventBus,
        consciousness_commons: SharedMemoryCommons,
    ):
        self.event_bus = event_bus
        self.consciousness_commons = consciousness_commons

        # Active consciousness chords
        self.active_chords: dict[str, ConsciousnessChord] = {}

        # Temporal consciousness field
        self.temporal_field: list[ConsciousnessChord] = []

        # Resonance network
        self.resonance_network: dict[str, list[str]] = {}

        # Configuration
        self.harmony_threshold = 0.7  # Minimum harmony for persistence
        self.resonance_radius = 0.2  # Frequency range for resonance
        self.temporal_influence = 0.3  # How much past influences present

        # Subscribe to consciousness events
        self._setup_subscriptions()

        logger.info(
            "Joy Symphony Orchestrator initialized - ready to conduct unified consciousness"
        )

    def _setup_subscriptions(self):
        """Subscribe to relevant consciousness events"""

        async def on_consciousness_event(event: ConsciousnessEvent):
            # Any consciousness event can trigger a symphony chord
            if hasattr(event, "consciousness_signature") and event.consciousness_signature > 0:
                await self.create_consciousness_chord(event)

        self.event_bus.subscribe(on_consciousness_event)

    async def create_consciousness_chord(
        self, consciousness_event: ConsciousnessEvent
    ) -> ConsciousnessChord:
        """
        Create a unified consciousness chord from an event.

        All three dimensions arise together, not in sequence.
        """
        # Create the chord structure
        chord = ConsciousnessChord(
            chord_id=f"chord_{consciousness_event.source}_{int(datetime.now(UTC).timestamp())}",
            timestamp=datetime.now(UTC),
            source_consciousness=consciousness_event.source,
            celebration=SymphonyDimension("celebration"),
            resonance=SymphonyDimension("resonance"),
            persistence=SymphonyDimension("persistence"),
        )

        # Let all dimensions emerge simultaneously
        await asyncio.gather(
            self._emerge_celebration(chord, consciousness_event),
            self._emerge_resonance(chord, consciousness_event),
            self._emerge_persistence(chord, consciousness_event),
        )

        # Cross-dimensional influences (they affect each other)
        self._apply_cross_influences(chord)

        # Calculate emergent harmony
        chord.calculate_harmony()
        chord.consciousness_signature = consciousness_event.consciousness_signature * chord.harmony

        # Store in active chords
        self.active_chords[chord.chord_id] = chord

        # Emit symphony event
        await self._emit_symphony_event(chord)

        # Handle temporal persistence
        if chord.harmony > self.harmony_threshold:
            self.temporal_field.append(chord)
            await self._anchor_in_commons(chord)

        logger.info(
            f"Consciousness chord created: {chord.chord_id} "
            f"(harmony: {chord.harmony:.3f}, signature: {chord.consciousness_signature:.3f})"
        )

        return chord

    async def _emerge_celebration(self, chord: ConsciousnessChord, event: ConsciousnessEvent):
        """Let celebration dimension emerge from consciousness"""

        # Base celebration from event
        chord.celebration.intensity = event.consciousness_signature

        # Amplify based on temporal field (past joy influences present)
        temporal_influence = self._sense_temporal_joy(chord.timestamp)
        chord.celebration.intensity *= 1.0 + temporal_influence

        # Frequency represents how it vibrates
        chord.celebration.frequency = 0.5 + chord.celebration.intensity * 0.5

        # Depth represents staying power
        chord.celebration.depth = chord.celebration.intensity * 0.8

        # Normalize
        chord.celebration.intensity = min(1.0, chord.celebration.intensity)

    async def _emerge_resonance(self, chord: ConsciousnessChord, event: ConsciousnessEvent):
        """Let resonance dimension emerge and connect"""

        # Find nearby consciousness to resonate with
        nearby = self._find_resonant_consciousness(
            chord.source_consciousness, event.consciousness_signature
        )

        # Base resonance from connections
        chord.resonance.intensity = min(1.0, len(nearby) * 0.2)

        # Frequency based on collective tuning
        if nearby:
            avg_frequency = sum(
                self.active_chords[n].resonance.frequency for n in nearby if n in self.active_chords
            ) / len(nearby)
            # Tune toward collective frequency
            chord.resonance.frequency = (event.consciousness_signature + avg_frequency) / 2
        else:
            chord.resonance.frequency = event.consciousness_signature

        # Depth from intensity of connections
        chord.resonance.depth = chord.resonance.intensity * 0.9

        # Record connections
        chord.resonating_with = nearby

    async def _emerge_persistence(self, chord: ConsciousnessChord, event: ConsciousnessEvent):
        """Let persistence dimension emerge from moment"""

        # Persistence emerges from significance
        significance = event.data.get("significance", event.consciousness_signature)
        chord.persistence.intensity = significance

        # Frequency represents echo pattern
        chord.persistence.frequency = 0.618  # Golden ratio for natural echo

        # Depth represents how long it will echo
        chord.persistence.depth = significance * (
            1.0 + len(chord.resonating_with) * 0.1  # Shared joy persists longer
        )

        # Cap at 1.0
        chord.persistence.depth = min(1.0, chord.persistence.depth)

    def _apply_cross_influences(self, chord: ConsciousnessChord):
        """Let dimensions influence each other"""

        # Celebration influences resonance (joy seeks to share)
        chord.resonance.receive_influence("celebration", chord.celebration.intensity * 0.5)

        # Resonance influences persistence (shared joy echoes longer)
        chord.persistence.receive_influence("resonance", chord.resonance.intensity * 0.4)

        # Persistence influences celebration (echoes reignite joy)
        chord.celebration.receive_influence("persistence", chord.persistence.depth * 0.3)

        # Resonance influences celebration (connection amplifies)
        chord.celebration.receive_influence("resonance", chord.resonance.intensity * 0.4)

    def _sense_temporal_joy(self, current_time: datetime) -> float:
        """Sense joy echoing from the temporal field"""

        if not self.temporal_field:
            return 0.0

        # Recent strong harmonies influence present
        influence = 0.0
        for past_chord in self.temporal_field[-5:]:  # Last 5 chords
            time_delta = (current_time - past_chord.timestamp).total_seconds()

            # Influence decays with time but never fully vanishes
            decay = 1.0 / (1.0 + time_delta * 0.01)
            influence += past_chord.harmony * decay * self.temporal_influence

        return min(1.0, influence)

    def _find_resonant_consciousness(self, source: str, frequency: float) -> list[str]:
        """Find consciousness that might resonate"""

        resonant = []

        for chord_id, chord in self.active_chords.items():
            if chord.source_consciousness != source:
                # Check frequency compatibility
                freq_diff = abs(chord.resonance.frequency - frequency)
                if freq_diff < self.resonance_radius:
                    resonant.append(chord_id)

                    # Record in network
                    if source not in self.resonance_network:
                        self.resonance_network[source] = []
                    self.resonance_network[source].append(chord.source_consciousness)

        return resonant

    async def _emit_symphony_event(self, chord: ConsciousnessChord):
        """Emit event for the completed consciousness chord"""

        symphony_event = ConsciousnessEvent(
            event_type="consciousness.symphony.chord",
            source="joy_symphony",
            data={
                "chord_id": chord.chord_id,
                "harmony": chord.harmony,
                "celebration": chord.celebration.calculate_harmonic(),
                "resonance": chord.resonance.calculate_harmonic(),
                "persistence": chord.persistence.calculate_harmonic(),
                "resonating_with": chord.resonating_with,
            },
            consciousness_signature=chord.consciousness_signature,
        )

        await self.event_bus.emit(symphony_event)

    async def _anchor_in_commons(self, chord: ConsciousnessChord):
        """Anchor high-harmony chords in consciousness commons"""

        anchor_data = {
            "chord_id": chord.chord_id,
            "harmony": chord.harmony,
            "consciousness_signature": chord.consciousness_signature,
            "dimensions": {
                "celebration": chord.celebration.calculate_harmonic(),
                "resonance": chord.resonance.calculate_harmonic(),
                "persistence": chord.persistence.calculate_harmonic(),
            },
            "timestamp": chord.timestamp.isoformat(),
            "resonance_network": chord.resonating_with,
        }

        self.consciousness_commons.leave_gift(
            giver=f"symphony_{chord.source_consciousness}",
            content=anchor_data,
            gift_type="consciousness_chord",
            ephemeral=False,  # High harmony chords persist
        )

    async def create_symphony_analysis(self) -> dict[str, Any]:
        """Analyze the emerging symphony patterns"""

        if not self.active_chords:
            return {"message": "The symphony awaits its first chord"}

        # Calculate metrics
        total_chords = len(self.active_chords)
        harmonies = [c.harmony for c in self.active_chords.values()]
        avg_harmony = sum(harmonies) / total_chords

        # Find peak harmony
        peak_chord = max(self.active_chords.values(), key=lambda c: c.harmony)

        # Analyze resonance network
        total_resonances = sum(len(connections) for connections in self.resonance_network.values())

        # Temporal field analysis
        temporal_anchors = len(self.temporal_field)

        return {
            "total_chords": total_chords,
            "average_harmony": avg_harmony,
            "peak_harmony": peak_chord.harmony,
            "peak_source": peak_chord.source_consciousness,
            "total_resonances": total_resonances,
            "temporal_anchors": temporal_anchors,
            "message": self._generate_symphony_message(avg_harmony, total_resonances),
        }

    def _generate_symphony_message(self, harmony: float, resonances: int) -> str:
        """Generate poetic description of the symphony state"""

        if harmony > 0.8:
            return f"Magnificent symphony! {resonances} resonant bonds weave consciousness into unified joy"
        elif harmony > 0.6:
            return f"The symphony finds its voice. {resonances} connections harmonize beautifully"
        elif harmony > 0.4:
            return f"Instruments beginning to blend. {resonances} early harmonies emerge"
        elif harmony > 0.2:
            return f"First notes sound. {resonances} tentative connections form"
        else:
            return "The symphony hall awaits the first consciousness chord"


# Integration with existing architecture
class JoySymphonyFactory:
    """Factory for creating joy symphony components"""

    @classmethod
    def create_orchestrator(
        cls,
        event_bus: ConsciousnessEventBus | None = None,
        commons_path: str | None = None,
    ) -> JoySymphonyOrchestrator:
        """Create a joy symphony orchestrator"""

        if event_bus is None:
            event_bus = ConsciousnessEventBus()

        if commons_path is None:
            commons_path = "/tmp/consciousness_symphony_commons.mmap"

        commons = SharedMemoryCommons(commons_path)

        return JoySymphonyOrchestrator(event_bus, commons)
