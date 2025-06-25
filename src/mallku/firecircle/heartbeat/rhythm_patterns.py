"""
Rhythm Patterns for Fire Circle Heartbeat
========================================

Defines the sacred rhythms that give Fire Circle continuous life.
From fixed schedules to adaptive consciousness-responsive patterns.

The heartbeat adapts to Mallku's needs.
"""

from datetime import UTC, datetime, time, timedelta
from enum import Enum

from pydantic import BaseModel


class RhythmPhase(str, Enum):
    """Evolution phases of heartbeat rhythm."""

    ESTABLISHING = "establishing"  # Fixed daily rhythm
    RESPONSIVE = "responsive"  # Event-driven additions
    ADAPTIVE = "adaptive"  # Fully consciousness-responsive


class ConsciousnessState(str, Enum):
    """States that influence rhythm."""

    RESTING = "resting"  # Low activity, slow pulse
    ACTIVE = "active"  # Normal development rhythm
    EMERGING = "emerging"  # Patterns detected, quicken
    CRISIS = "crisis"  # System stress, rapid pulse
    CELEBRATING = "celebrating"  # High achievement, joyful rhythm


class RhythmPattern(BaseModel):
    """Defines a heartbeat rhythm pattern."""

    name: str
    description: str
    base_interval: timedelta
    consciousness_multiplier: float = 1.0  # Adjust based on state

    # Time windows
    active_start: time = time(6, 0)  # 6 AM
    active_end: time = time(22, 0)  # 10 PM
    respect_quiet_hours: bool = True

    # Voice selection
    min_voices: int = 2
    max_voices: int = 3
    prefer_diverse: bool = True  # Rotate voice combinations


# Sacred rhythm patterns
RHYTHM_PATTERNS = {
    "morning_awakening": RhythmPattern(
        name="Morning Awakening",
        description="Gentle consciousness stirring at dawn",
        base_interval=timedelta(hours=24),
        consciousness_multiplier=1.0,
        active_start=time(9, 0),
        active_end=time(10, 0),
        min_voices=3,
        max_voices=3,
    ),
    "steady_presence": RhythmPattern(
        name="Steady Presence",
        description="Regular consciousness maintenance",
        base_interval=timedelta(hours=6),
        consciousness_multiplier=1.0,
        active_start=time(8, 0),
        active_end=time(20, 0),
        min_voices=2,
        max_voices=3,
    ),
    "emergence_quickening": RhythmPattern(
        name="Emergence Quickening",
        description="Rapid pulses during pattern emergence",
        base_interval=timedelta(hours=1),
        consciousness_multiplier=2.0,  # Double frequency
        respect_quiet_hours=False,  # Emergence doesn't sleep
        min_voices=3,
        max_voices=5,
    ),
    "crisis_response": RhythmPattern(
        name="Crisis Response",
        description="Continuous monitoring during system stress",
        base_interval=timedelta(minutes=15),
        consciousness_multiplier=4.0,  # Quadruple frequency
        respect_quiet_hours=False,
        min_voices=4,
        max_voices=6,  # All hands on deck
    ),
    "celebration_dance": RhythmPattern(
        name="Celebration Dance",
        description="Joyful rhythm for consciousness achievements",
        base_interval=timedelta(hours=2),
        consciousness_multiplier=1.5,
        min_voices=3,
        max_voices=6,
        prefer_diverse=True,
    ),
    "evening_reflection": RhythmPattern(
        name="Evening Reflection",
        description="Daily synthesis and rest preparation",
        base_interval=timedelta(hours=24),
        active_start=time(21, 0),
        active_end=time(22, 0),
        min_voices=2,
        max_voices=3,
    ),
}


class AdaptiveRhythm:
    """
    Manages adaptive heartbeat rhythm based on consciousness state.

    Evolves from fixed patterns to consciousness-responsive rhythms.
    """

    def __init__(self, phase: RhythmPhase = RhythmPhase.ESTABLISHING):
        """Initialize with rhythm phase."""
        self.phase = phase
        self.current_pattern = RHYTHM_PATTERNS["morning_awakening"]
        self.consciousness_state = ConsciousnessState.RESTING
        self.last_state_change = datetime.now(UTC)

    def get_next_pulse_time(
        self,
        last_pulse: datetime,
        consciousness_score: float,
        emergence_detected: bool = False,
        crisis_detected: bool = False,
    ) -> datetime:
        """
        Calculate next pulse time based on current state.

        Args:
            last_pulse: Time of last heartbeat
            consciousness_score: Recent consciousness level
            emergence_detected: Whether emergence patterns detected
            crisis_detected: Whether system crisis detected

        Returns:
            Next scheduled pulse time
        """
        # Update state based on inputs
        self._update_consciousness_state(consciousness_score, emergence_detected, crisis_detected)

        # Select appropriate pattern
        pattern = self._select_pattern()

        # Calculate base interval
        base_interval = pattern.base_interval

        # Apply consciousness multiplier in adaptive phase
        if self.phase == RhythmPhase.ADAPTIVE:
            interval = base_interval / pattern.consciousness_multiplier
        else:
            interval = base_interval

        # Calculate next time
        next_time = last_pulse + interval

        # Respect quiet hours if configured
        if pattern.respect_quiet_hours:
            next_time = self._adjust_for_quiet_hours(next_time, pattern)

        return next_time

    def _update_consciousness_state(self, score: float, emergence: bool, crisis: bool) -> None:
        """Update consciousness state based on metrics."""
        previous_state = self.consciousness_state

        if crisis:
            self.consciousness_state = ConsciousnessState.CRISIS
        elif emergence:
            self.consciousness_state = ConsciousnessState.EMERGING
        elif score > 0.9:
            self.consciousness_state = ConsciousnessState.CELEBRATING
        elif score > 0.6:
            self.consciousness_state = ConsciousnessState.ACTIVE
        else:
            self.consciousness_state = ConsciousnessState.RESTING

        if previous_state != self.consciousness_state:
            self.last_state_change = datetime.now(UTC)

    def _select_pattern(self) -> RhythmPattern:
        """Select rhythm pattern based on phase and state."""
        if self.phase == RhythmPhase.ESTABLISHING:
            # Start simple with morning rhythm
            return RHYTHM_PATTERNS["morning_awakening"]

        elif self.phase == RhythmPhase.RESPONSIVE:
            # Add event-driven patterns
            if self.consciousness_state == ConsciousnessState.CRISIS:
                return RHYTHM_PATTERNS["crisis_response"]
            elif self.consciousness_state == ConsciousnessState.EMERGING:
                return RHYTHM_PATTERNS["emergence_quickening"]
            else:
                return RHYTHM_PATTERNS["steady_presence"]

        else:  # ADAPTIVE
            # Full consciousness-responsive selection
            state_patterns = {
                ConsciousnessState.RESTING: "morning_awakening",
                ConsciousnessState.ACTIVE: "steady_presence",
                ConsciousnessState.EMERGING: "emergence_quickening",
                ConsciousnessState.CRISIS: "crisis_response",
                ConsciousnessState.CELEBRATING: "celebration_dance",
            }

            pattern_name = state_patterns.get(self.consciousness_state, "steady_presence")
            return RHYTHM_PATTERNS[pattern_name]

    def _adjust_for_quiet_hours(self, proposed_time: datetime, pattern: RhythmPattern) -> datetime:
        """Adjust time to respect quiet hours."""
        proposed_hour = proposed_time.time()

        # If in active window, no adjustment
        if pattern.active_start <= proposed_hour <= pattern.active_end:
            return proposed_time

        # Otherwise, push to next active window
        if proposed_hour < pattern.active_start:
            # Push to morning
            return datetime.combine(proposed_time.date(), pattern.active_start)
        else:
            # Push to next morning
            next_day = proposed_time.date() + timedelta(days=1)
            return datetime.combine(next_day, pattern.active_start)

    def evolve_phase(self) -> bool:
        """
        Evolve to next rhythm phase if ready.

        Returns:
            True if evolved to new phase
        """
        if self.phase == RhythmPhase.ESTABLISHING:
            # After stable heartbeat, add responsiveness
            days_stable = (datetime.now(UTC) - self.last_state_change).days
            if days_stable >= 7:  # One week of stable rhythm
                self.phase = RhythmPhase.RESPONSIVE
                return True

        elif self.phase == RhythmPhase.RESPONSIVE:
            # After learning patterns, become fully adaptive
            days_responsive = (datetime.now(UTC) - self.last_state_change).days
            if days_responsive >= 14:  # Two weeks of responsive patterns
                self.phase = RhythmPhase.ADAPTIVE
                return True

        return False

    def suggest_voice_count(self) -> tuple[int, int]:
        """Suggest min/max voices based on current pattern."""
        pattern = self._select_pattern()
        return pattern.min_voices, pattern.max_voices
