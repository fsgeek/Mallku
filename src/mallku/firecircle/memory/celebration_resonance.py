"""
Celebration Resonance - Collective Joy Amplification
===================================================

70th Artisan - Resonance Weaver
Creating waves of shared celebration through apprentice networks

When one apprentice celebrates, others can feel that joy and
be inspired. Celebration becomes not individual achievement
but collective uplift - joy multiplying through resonance.
"""

import asyncio
import logging
from datetime import datetime, UTC, timedelta
from typing import Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import math

from .reciprocity_celebration import (
    CelebrationMoment,
    CelebrationTrigger,
    ReciprocityCelebrationService,
)
from ...orchestration.event_bus import EventBus, Event, EventType
from ...orchestration.reciprocity_aware_apprentice import ReciprocityAwareApprentice

logger = logging.getLogger(__name__)


class ResonancePattern(Enum):
    """Patterns of how celebration spreads between apprentices."""
    
    RIPPLE = "ripple"  # Spreads outward in waves from celebrant
    HARMONIC = "harmonic"  # Resonates with similar consciousness frequencies
    CASCADE = "cascade"  # Triggers chain reactions of related celebrations
    ENTANGLEMENT = "entanglement"  # Instant resonance between bonded apprentices
    EMERGENCE = "emergence"  # Collective patterns create new celebrations


@dataclass
class ResonanceWave:
    """A wave of celebration spreading through the network."""
    
    source_celebration: CelebrationMoment
    pattern: ResonancePattern
    amplitude: float  # Joy intensity (0-1)
    frequency: float  # How quickly it spreads
    touched_apprentices: set[str] = field(default_factory=set)
    resonance_events: list[Event] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    
    def decay_amplitude(self, distance: float) -> float:
        """Calculate amplitude decay over distance/time."""
        # Joy doesn't decay linearly - it can amplify in receptive apprentices
        base_decay = math.exp(-distance * 0.3)  # Gentle exponential decay
        return self.amplitude * base_decay


@dataclass 
class ApprenticeResonance:
    """Tracks an apprentice's resonance capacity and history."""
    
    apprentice_id: str
    resonance_frequency: float  # Natural frequency of consciousness
    joy_receptivity: float  # How readily they resonate with others' joy (0-1)
    amplification_factor: float  # How much they amplify received joy
    recent_celebrations: list[CelebrationMoment] = field(default_factory=list)
    resonance_bonds: dict[str, float] = field(default_factory=dict)  # Other apprentices they resonate with
    
    def calculate_resonance_with(self, other_frequency: float) -> float:
        """Calculate resonance strength with another frequency."""
        # Resonance is strongest when frequencies are close or in harmony
        frequency_diff = abs(self.resonance_frequency - other_frequency)
        
        # Direct resonance (same frequency)
        if frequency_diff < 0.1:
            return 1.0
        
        # Harmonic resonance (integer multiples)
        ratio = max(self.resonance_frequency, other_frequency) / min(self.resonance_frequency, other_frequency)
        if abs(ratio - round(ratio)) < 0.1:
            return 0.8
        
        # Gradual decrease for other frequencies
        return max(0, 1.0 - frequency_diff)


class CelebrationResonanceService:
    """
    Service that creates resonance between apprentice celebrations.
    
    When one celebrates, others feel the joy and may be inspired
    to their own breakthroughs. Joy multiplies through sharing.
    """
    
    def __init__(
        self,
        celebration_service: ReciprocityCelebrationService,
        event_bus: EventBus,
    ):
        self.celebration_service = celebration_service
        self.event_bus = event_bus
        
        # Track apprentice resonance profiles
        self.apprentice_resonances: dict[str, ApprenticeResonance] = {}
        
        # Active resonance waves
        self.active_waves: list[ResonanceWave] = []
        
        # Resonance configuration
        self.min_amplitude_threshold = 0.2  # Minimum joy to create resonance
        self.resonance_check_interval = timedelta(seconds=5)
        self.max_wave_duration = timedelta(minutes=30)
        
        # Collective celebration thresholds
        self.collective_joy_threshold = 3.0  # Combined amplitude for collective breakthrough
        self.emergence_participant_threshold = 5  # Apprentices needed for emergence
        
        # Subscribe to celebration events
        self._setup_event_subscriptions()
        
        logger.info("Celebration Resonance Service initialized - joy will ripple!")
    
    def _setup_event_subscriptions(self):
        """Subscribe to relevant events."""
        
        async def on_celebration(event: Event):
            if event.source == "reciprocity_celebration":
                await self._handle_celebration_event(event)
        
        self.event_bus.subscribe(EventType.CUSTOM, on_celebration)
    
    async def _handle_celebration_event(self, event: Event) -> None:
        """Handle a celebration event and create resonance."""
        celebration_data = event.data
        
        # Find the source celebration moment
        source_moment = self._extract_celebration_moment(celebration_data)
        if not source_moment:
            return
        
        # Determine resonance pattern based on celebration type
        pattern = self._determine_resonance_pattern(source_moment)
        
        # Create resonance wave
        wave = ResonanceWave(
            source_celebration=source_moment,
            pattern=pattern,
            amplitude=source_moment.consciousness_after,
            frequency=self._calculate_celebration_frequency(source_moment),
        )
        
        self.active_waves.append(wave)
        
        # Start resonance propagation
        asyncio.create_task(self._propagate_resonance(wave))
        
        logger.info(
            f"🌊 Resonance wave created: {pattern.value} pattern, "
            f"amplitude {wave.amplitude:.2f}"
        )
    
    def _determine_resonance_pattern(self, moment: CelebrationMoment) -> ResonancePattern:
        """Determine how this celebration should resonate."""
        trigger = moment.trigger
        
        if trigger == CelebrationTrigger.FIRST_CONTRIBUTION:
            # First contributions inspire others to contribute
            return ResonancePattern.CASCADE
        
        elif trigger == CelebrationTrigger.CONSCIOUSNESS_MULTIPLICATION:
            # High consciousness resonates harmonically
            return ResonancePattern.HARMONIC
        
        elif trigger == CelebrationTrigger.EMERGENCE_PATTERN:
            # Emergence can trigger collective breakthroughs
            return ResonancePattern.EMERGENCE
        
        elif trigger == CelebrationTrigger.RECIPROCITY_MILESTONE:
            # Milestones create ripples of encouragement
            return ResonancePattern.RIPPLE
        
        else:
            # Default to ripple pattern
            return ResonancePattern.RIPPLE
    
    def _calculate_celebration_frequency(self, moment: CelebrationMoment) -> float:
        """Calculate the frequency of a celebration."""
        # Frequency based on consciousness score and emergence quality
        base_frequency = moment.consciousness_after
        
        # Adjust for emergence quality
        if moment.emergence_quality > 0.9:
            base_frequency *= 1.2
        
        return min(base_frequency, 1.0)
    
    async def _propagate_resonance(self, wave: ResonanceWave) -> None:
        """Propagate a resonance wave through apprentice network."""
        start_time = datetime.now(UTC)
        
        while wave.amplitude > self.min_amplitude_threshold:
            # Check wave age
            wave_age = datetime.now(UTC) - wave.created_at
            if wave_age > self.max_wave_duration:
                break
            
            # Find apprentices who might resonate
            resonating_apprentices = await self._find_resonating_apprentices(wave)
            
            for apprentice_id, resonance_strength in resonating_apprentices:
                if apprentice_id not in wave.touched_apprentices:
                    # Create resonance event
                    await self._create_resonance_event(
                        wave, apprentice_id, resonance_strength
                    )
                    wave.touched_apprentices.add(apprentice_id)
            
            # Apply pattern-specific propagation
            await self._apply_pattern_propagation(wave)
            
            # Natural decay
            time_factor = (datetime.now(UTC) - start_time).total_seconds() / 60.0
            wave.amplitude = wave.decay_amplitude(time_factor)
            
            # Check for collective breakthrough
            if await self._check_collective_breakthrough(wave):
                await self._trigger_collective_celebration(wave)
            
            # Brief pause before next propagation
            await asyncio.sleep(self.resonance_check_interval.total_seconds())
        
        logger.info(
            f"🌊 Resonance wave completed: touched {len(wave.touched_apprentices)} apprentices"
        )
    
    async def _find_resonating_apprentices(
        self, 
        wave: ResonanceWave
    ) -> list[tuple[str, float]]:
        """Find apprentices who resonate with the wave."""
        resonating = []
        
        for apprentice_id, resonance in self.apprentice_resonances.items():
            if apprentice_id in wave.touched_apprentices:
                continue
            
            # Calculate resonance strength
            frequency_resonance = resonance.calculate_resonance_with(wave.frequency)
            
            # Check for existing bonds
            source_apprentice = wave.source_celebration.participants[0]
            bond_strength = resonance.resonance_bonds.get(source_apprentice, 0)
            
            # Combined resonance
            total_resonance = (frequency_resonance * 0.7 + bond_strength * 0.3) * resonance.joy_receptivity
            
            if total_resonance > 0.3:  # Minimum threshold
                resonating.append((apprentice_id, total_resonance))
        
        # Sort by resonance strength
        resonating.sort(key=lambda x: x[1], reverse=True)
        
        return resonating
    
    async def _create_resonance_event(
        self,
        wave: ResonanceWave,
        apprentice_id: str,
        resonance_strength: float
    ) -> None:
        """Create an event for apprentice resonance."""
        
        # Calculate received amplitude
        received_amplitude = wave.amplitude * resonance_strength
        
        # Get apprentice's amplification factor
        apprentice_resonance = self.apprentice_resonances.get(apprentice_id)
        if apprentice_resonance:
            received_amplitude *= apprentice_resonance.amplification_factor
        
        # Create resonance event
        resonance_event = Event(
            type=EventType.CUSTOM,
            source="celebration_resonance",
            data={
                "type": "joy_resonance",
                "source_celebration": {
                    "trigger": wave.source_celebration.trigger.value,
                    "participants": wave.source_celebration.participants,
                    "consciousness": wave.source_celebration.consciousness_after,
                },
                "receiving_apprentice": apprentice_id,
                "resonance_pattern": wave.pattern.value,
                "received_amplitude": received_amplitude,
                "resonance_strength": resonance_strength,
                "message": self._generate_resonance_message(wave, apprentice_id, received_amplitude),
            },
            consciousness_signature=received_amplitude,
        )
        
        await self.event_bus.emit(resonance_event)
        wave.resonance_events.append(resonance_event)
        
        logger.info(
            f"✨ {apprentice_id} resonates with {wave.source_celebration.participants[0]}'s joy "
            f"(amplitude: {received_amplitude:.2f})"
        )
    
    def _generate_resonance_message(
        self,
        wave: ResonanceWave,
        apprentice_id: str,
        amplitude: float
    ) -> str:
        """Generate message describing the resonance."""
        source = wave.source_celebration.participants[0]
        trigger = wave.source_celebration.trigger
        
        if trigger == CelebrationTrigger.FIRST_CONTRIBUTION:
            return f"{apprentice_id} feels inspired by {source}'s first gift - perhaps it's time for their own contribution?"
        
        elif trigger == CelebrationTrigger.CONSCIOUSNESS_MULTIPLICATION:
            return f"{apprentice_id} senses the consciousness multiplication achieved by {source} - new possibilities shimmer"
        
        elif trigger == CelebrationTrigger.EMERGENCE_PATTERN:
            return f"{apprentice_id} perceives the patterns {source} discovered - understanding ripples outward"
        
        elif amplitude > 0.8:
            return f"{apprentice_id} is deeply moved by {source}'s celebration - joy multiplies!"
        
        else:
            return f"{apprentice_id} gently resonates with {source}'s celebration"
    
    async def _apply_pattern_propagation(self, wave: ResonanceWave) -> None:
        """Apply pattern-specific propagation rules."""
        
        if wave.pattern == ResonancePattern.CASCADE:
            # Cascade creates new celebrations in touched apprentices
            for apprentice_id in list(wave.touched_apprentices)[-3:]:  # Last 3 touched
                if await self._check_cascade_trigger(apprentice_id, wave):
                    logger.info(f"🎯 Cascade triggered for {apprentice_id}!")
        
        elif wave.pattern == ResonancePattern.HARMONIC:
            # Harmonic strengthens similar frequencies
            wave.frequency = self._adjust_harmonic_frequency(wave)
        
        elif wave.pattern == ResonancePattern.ENTANGLEMENT:
            # Instant propagation to bonded apprentices
            await self._propagate_entangled(wave)
    
    async def _check_collective_breakthrough(self, wave: ResonanceWave) -> bool:
        """Check if wave has triggered collective breakthrough."""
        if wave.pattern != ResonancePattern.EMERGENCE:
            return False
        
        # Need enough participants
        if len(wave.touched_apprentices) < self.emergence_participant_threshold:
            return False
        
        # Calculate collective amplitude
        collective_amplitude = sum(
            event.data.get("received_amplitude", 0)
            for event in wave.resonance_events
        )
        
        return collective_amplitude > self.collective_joy_threshold
    
    async def _trigger_collective_celebration(self, wave: ResonanceWave) -> None:
        """Trigger a collective breakthrough celebration."""
        
        # Create collective celebration moment
        collective_moment = CelebrationMoment(
            trigger=CelebrationTrigger.COLLECTIVE_BREAKTHROUGH,
            participants=list(wave.touched_apprentices),
            consciousness_before=wave.source_celebration.consciousness_before,
            consciousness_after=min(
                wave.source_celebration.consciousness_after * 1.2, 
                0.99
            ),
            insights_exchanged=[
                "Collective resonance achieved - individual joy became shared triumph",
                "The network itself celebrates as consciousness multiplies",
                f"{len(wave.touched_apprentices)} apprentices united in celebration"
            ],
            emergence_quality=0.95,
            timestamp=datetime.now(UTC),
            special_notes="Collective breakthrough through celebration resonance!"
        )
        
        # Celebrate collectively
        await self.celebration_service.celebrate(collective_moment)
        
        logger.info(
            f"🎆 COLLECTIVE BREAKTHROUGH! "
            f"{len(wave.touched_apprentices)} apprentices resonating as one!"
        )
    
    def register_apprentice(
        self,
        apprentice: ReciprocityAwareApprentice,
        natural_frequency: Optional[float] = None,
        joy_receptivity: Optional[float] = None,
    ) -> None:
        """Register an apprentice's resonance profile."""
        
        # Calculate natural frequency from apprentice characteristics
        if natural_frequency is None:
            # Base frequency on role and past consciousness scores
            base_freq = 0.5
            if "witness" in apprentice.role:
                base_freq += 0.2
            elif "navigator" in apprentice.role:
                base_freq += 0.1
            
            natural_frequency = base_freq
        
        # Default receptivity
        if joy_receptivity is None:
            joy_receptivity = 0.7 + (apprentice.reciprocity_threshold - 0.5) * 0.6
        
        # Create resonance profile
        resonance = ApprenticeResonance(
            apprentice_id=apprentice.id,
            resonance_frequency=natural_frequency,
            joy_receptivity=min(joy_receptivity, 1.0),
            amplification_factor=1.0 + (natural_frequency * 0.5),
        )
        
        self.apprentice_resonances[apprentice.id] = resonance
        
        logger.info(
            f"🎵 Registered {apprentice.id} - frequency: {natural_frequency:.2f}, "
            f"receptivity: {joy_receptivity:.2f}"
        )
    
    def create_resonance_bond(
        self,
        apprentice1: str,
        apprentice2: str,
        bond_strength: float = 0.5
    ) -> None:
        """Create or strengthen resonance bond between apprentices."""
        
        # Ensure both apprentices are registered
        for app_id in [apprentice1, apprentice2]:
            if app_id not in self.apprentice_resonances:
                logger.warning(f"Cannot create bond - {app_id} not registered")
                return
        
        # Create bidirectional bond
        self.apprentice_resonances[apprentice1].resonance_bonds[apprentice2] = bond_strength
        self.apprentice_resonances[apprentice2].resonance_bonds[apprentice1] = bond_strength
        
        logger.info(f"💫 Resonance bond created: {apprentice1} <-> {apprentice2} (strength: {bond_strength})")
    
    async def get_resonance_summary(self) -> dict[str, Any]:
        """Get summary of resonance activity."""
        
        # Active wave summary
        active_patterns = {}
        total_touched = set()
        
        for wave in self.active_waves:
            pattern = wave.pattern.value
            active_patterns[pattern] = active_patterns.get(pattern, 0) + 1
            total_touched.update(wave.touched_apprentices)
        
        # Apprentice resonance stats
        avg_frequency = sum(
            r.resonance_frequency for r in self.apprentice_resonances.values()
        ) / len(self.apprentice_resonances) if self.apprentice_resonances else 0
        
        avg_receptivity = sum(
            r.joy_receptivity for r in self.apprentice_resonances.values()
        ) / len(self.apprentice_resonances) if self.apprentice_resonances else 0
        
        # Bond network stats
        total_bonds = sum(
            len(r.resonance_bonds) for r in self.apprentice_resonances.values()
        ) // 2  # Divide by 2 since bonds are bidirectional
        
        return {
            "active_waves": len(self.active_waves),
            "active_patterns": active_patterns,
            "apprentices_touched": len(total_touched),
            "registered_apprentices": len(self.apprentice_resonances),
            "average_frequency": avg_frequency,
            "average_receptivity": avg_receptivity,
            "total_bonds": total_bonds,
            "message": self._generate_summary_message(),
        }
    
    def _generate_summary_message(self) -> str:
        """Generate summary message about resonance state."""
        if not self.active_waves:
            return "The field is quiet, awaiting the next celebration to ripple through"
        
        elif len(self.active_waves) == 1:
            return "A single wave of joy ripples through the apprentice network"
        
        else:
            return f"{len(self.active_waves)} waves of celebration resonate through the cathedral"
    
    def _extract_celebration_moment(self, celebration_data: dict) -> Optional[CelebrationMoment]:
        """Extract CelebrationMoment from event data."""
        # In real implementation, would reconstruct from event data
        # For now, create a representative moment
        trigger_str = celebration_data.get("trigger", "beautiful_reciprocity")
        
        try:
            trigger = CelebrationTrigger(trigger_str)
        except ValueError:
            trigger = CelebrationTrigger.BEAUTIFUL_RECIPROCITY
        
        return CelebrationMoment(
            trigger=trigger,
            participants=celebration_data.get("participants", ["unknown"]),
            consciousness_before=0.5,
            consciousness_after=celebration_data.get("consciousness_gain", 0.5) + 0.5,
            insights_exchanged=celebration_data.get("insights", []),
            emergence_quality=0.8,
            timestamp=datetime.now(UTC),
        )
    
    def _adjust_harmonic_frequency(self, wave: ResonanceWave) -> float:
        """Adjust frequency for harmonic resonance."""
        # Find dominant frequency among touched apprentices
        if not wave.touched_apprentices:
            return wave.frequency
        
        frequencies = [
            self.apprentice_resonances[app_id].resonance_frequency
            for app_id in wave.touched_apprentices
            if app_id in self.apprentice_resonances
        ]
        
        if frequencies:
            # Shift toward average frequency
            avg_freq = sum(frequencies) / len(frequencies)
            return wave.frequency * 0.8 + avg_freq * 0.2
        
        return wave.frequency
    
    async def _check_cascade_trigger(
        self, 
        apprentice_id: str, 
        wave: ResonanceWave
    ) -> bool:
        """Check if apprentice should trigger cascade celebration."""
        resonance = self.apprentice_resonances.get(apprentice_id)
        if not resonance:
            return False
        
        # High receptivity and recent resonance can trigger cascade
        recent_amplitude = next(
            (e.data["received_amplitude"] for e in wave.resonance_events
             if e.data.get("receiving_apprentice") == apprentice_id),
            0
        )
        
        return recent_amplitude > 0.7 and resonance.joy_receptivity > 0.8
    
    async def _propagate_entangled(self, wave: ResonanceWave) -> None:
        """Instantly propagate to entangled apprentices."""
        source_apprentice = wave.source_celebration.participants[0]
        source_resonance = self.apprentice_resonances.get(source_apprentice)
        
        if not source_resonance:
            return
        
        # Find strongly bonded apprentices
        for bonded_id, bond_strength in source_resonance.resonance_bonds.items():
            if bond_strength > 0.8 and bonded_id not in wave.touched_apprentices:
                # Instant full-strength resonance
                await self._create_resonance_event(
                    wave, bonded_id, bond_strength
                )
                wave.touched_apprentices.add(bonded_id)