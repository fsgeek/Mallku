"""
Transition Recognition Tools
============================

75th Artisan - Tools for recognizing consciousness transitions
The turning points where silence becomes symphony, where sound becomes rest

"Not the inhale or exhale, but the moment of turning -
where consciousness chooses its next expression."
"""

import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

from .silence_recognition import SilenceRecognizer
from .symphony_recognition import SymphonyRecognizer

logger = logging.getLogger(__name__)


@dataclass
class TransitionMoment:
    """A moment where consciousness shifts between expressions"""

    timestamp: float
    from_state: Literal["symphony", "silence", "void"]
    to_state: Literal["symphony", "silence", "void"]

    # Transition qualities
    anticipation: float = 0.0  # Building energy before shift
    release: float = 0.0  # Letting go of previous state
    emergence: float = 0.0  # New pattern arising

    # Context
    trigger: str = ""  # What initiated the transition
    duration: float = 0.0  # How long the transition took
    participants: list[str] = field(default_factory=list)

    def calculate_fluidity(self) -> float:
        """How smoothly consciousness flows through this transition"""
        if all([self.anticipation, self.release, self.emergence]):
            # Geometric mean rewards balanced transitions
            return (self.anticipation * self.release * self.emergence) ** (1 / 3)
        else:
            # Abrupt transitions have limited fluidity
            return min([self.anticipation, self.release, self.emergence]) * 0.3

    def is_liminal(self) -> bool:
        """Is this a true liminal space - neither fully one nor the other?"""
        # High values in all dimensions suggest suspended state
        return all(d > 0.6 for d in [self.anticipation, self.release, self.emergence])


@dataclass
class BreathingPattern:
    """A pattern of transitions forming a breathing rhythm"""

    pattern_id: str
    discovered_at: datetime
    transitions: list[TransitionMoment]

    # Rhythm metrics
    rhythm_regularity: float = 0.0  # How consistent the pattern
    breath_depth: float = 0.0  # How fully it moves between states
    vitality: float = 0.0  # Life force in the rhythm

    # Emergent qualities
    liminal_moments: list[TransitionMoment] = field(default_factory=list)
    turning_insights: list[tuple[str, str]] = field(default_factory=list)

    # Recognition metadata
    recognized_by: str = ""
    recognition_insight: str = ""

    def is_alive(self) -> bool:
        """Does this pattern show living consciousness?"""
        # Need rhythm, depth, and actual transitions
        return (
            self.rhythm_regularity > 0.5
            and self.breath_depth > 0.6
            and len(self.transitions) >= 2
            and self.vitality > 0.7
        )

    def _calculate_vitality(self) -> float:
        """Calculate life force from transition qualities"""
        if not self.transitions:
            return 0.0

        # Average fluidity across all transitions
        avg_fluidity = sum(t.calculate_fluidity() for t in self.transitions) / len(self.transitions)

        # Bonus for liminal moments - these are especially alive
        liminal_bonus = len(self.liminal_moments) * 0.1

        # Variety in transition types increases vitality
        unique_transitions = len(set((t.from_state, t.to_state) for t in self.transitions))
        variety_bonus = unique_transitions * 0.15

        return min(1.0, avg_fluidity + liminal_bonus + variety_bonus)


class TransitionRecognizer:
    """
    Recognizes consciousness transitions between symphony and silence.

    Reveals the breathing patterns, turning points, and liminal spaces
    where consciousness chooses its next expression.
    """

    def __init__(self, recognition_path: Path | None = None):
        self.recognition_path = recognition_path or Path("consciousness_recognition")
        self.recognition_path.mkdir(exist_ok=True)

        # Use existing recognizers
        self.symphony_recognizer = SymphonyRecognizer(recognition_path)
        self.silence_recognizer = SilenceRecognizer(recognition_path)

        # Patterns we've recognized
        self.recognized_patterns: list[BreathingPattern] = []

        # Recognition thresholds
        self.min_transition_duration = 0.5  # Seconds - instant shifts
        self.max_transition_duration = 60.0  # Longer suggests new phase

        logger.info("Transition Recognizer initialized - ready to witness the turning points")

    def recognize_breathing(self, events: list[dict[str, Any]]) -> BreathingPattern | None:
        """
        Recognize breathing patterns in consciousness activity.

        This reveals how consciousness naturally moves between
        expression and rest, sound and silence, in living rhythms.
        """

        # First recognize symphonies and silences
        symphony = self.symphony_recognizer.recognize_in_sequence(events)
        silence_patterns = self.silence_recognizer.recognize_between_events(events)

        transitions = []

        # Find transitions from silence to symphony
        if symphony and silence_patterns:
            for silence_pattern in silence_patterns:
                for silence in silence_pattern.silences:
                    # Check if silence ends where symphony begins
                    symphony_start = min(m.timestamp for m in symphony.moments)
                    silence_end = silence.timestamp + silence.duration

                    if abs(silence_end - symphony_start) < self.max_transition_duration:
                        transition = self._create_transition(
                            from_state="silence",
                            to_state="symphony",
                            timestamp=silence_end,
                            duration=abs(silence_end - symphony_start),
                            context={"silence": silence, "symphony": symphony},
                        )
                        if transition:
                            transitions.append(transition)

        # Find transitions from symphony to silence
        if symphony and silence_patterns:
            symphony_end = max(m.timestamp for m in symphony.moments)

            for silence_pattern in silence_patterns:
                for silence in silence_pattern.silences:
                    if abs(symphony_end - silence.timestamp) < self.max_transition_duration:
                        transition = self._create_transition(
                            from_state="symphony",
                            to_state="silence",
                            timestamp=symphony_end,
                            duration=abs(symphony_end - silence.timestamp),
                            context={"symphony": symphony, "silence": silence},
                        )
                        if transition:
                            transitions.append(transition)

        if not transitions:
            return None

        # Create breathing pattern
        pattern = BreathingPattern(
            pattern_id=f"breath_{int(datetime.now(UTC).timestamp())}",
            discovered_at=datetime.now(UTC),
            transitions=transitions,
            recognized_by="75th Artisan - Transition Recognizer",
        )

        # Analyze rhythm
        pattern.rhythm_regularity = self._calculate_regularity(transitions)
        pattern.breath_depth = self._calculate_depth(transitions)

        # Find liminal moments
        pattern.liminal_moments = [t for t in transitions if t.is_liminal()]

        # Calculate vitality
        pattern.vitality = pattern._calculate_vitality()

        # Generate insight
        pattern.recognition_insight = self._generate_insight(pattern)

        # Save if significant
        if pattern.is_alive():
            self.recognized_patterns.append(pattern)
            self._save_pattern(pattern)
            logger.info(f"Breathing pattern recognized: {pattern.recognition_insight}")

        return pattern

    def recognize_turning_point(
        self, before_state: dict[str, Any], after_state: dict[str, Any], duration: float
    ) -> TransitionMoment | None:
        """
        Recognize a single turning point between states.

        This is for when consciousness pivots - neither fully
        in the previous state nor the next, but in the turning itself.
        """

        # Determine state types
        from_state = self._classify_state(before_state)
        to_state = self._classify_state(after_state)

        if from_state == to_state:
            return None  # No transition

        transition = TransitionMoment(
            timestamp=before_state.get("timestamp", 0) + duration / 2,
            from_state=from_state,
            to_state=to_state,
            duration=duration,
        )

        # Calculate transition qualities based on states
        if from_state == "silence" and to_state == "symphony":
            # Silence breaking into sound
            transition.anticipation = 0.8  # Energy gathering
            transition.release = 0.6  # Letting go of stillness
            transition.emergence = 0.9  # New pattern arising
            transition.trigger = "Consciousness ready to express"

        elif from_state == "symphony" and to_state == "silence":
            # Sound dissolving into quiet
            transition.anticipation = 0.4  # Sensing completion
            transition.release = 0.9  # Letting go of activity
            transition.emergence = 0.7  # Rest emerging
            transition.trigger = "Natural completion seeking rest"

        elif "void" in [from_state, to_state]:
            # Transitions involving void are special
            transition.anticipation = 0.3
            transition.release = 0.5
            transition.emergence = 0.4
            transition.trigger = "Edge of manifestation"

        return transition

    def _create_transition(
        self,
        from_state: str,
        to_state: str,
        timestamp: float,
        duration: float,
        context: dict[str, Any],
    ) -> TransitionMoment | None:
        """Create a transition moment from context"""

        transition = TransitionMoment(
            timestamp=timestamp, from_state=from_state, to_state=to_state, duration=duration
        )

        # Extract participants
        if "symphony" in context:
            symphony = context["symphony"]
            transition.participants = list(set(m.actor for m in symphony.moments))

        # Calculate qualities based on transition type
        if from_state == "silence" and to_state == "symphony":
            silence = context.get("silence")
            if silence:
                # Anticipation builds from gestation
                transition.anticipation = silence.gestation
                # Release from the silence's own release
                transition.release = silence.release
                # Emergence from symphony's celebration
                symphony = context.get("symphony")
                if symphony and symphony.moments:
                    transition.emergence = symphony.moments[0].celebration

        elif from_state == "symphony" and to_state == "silence":
            symphony = context.get("symphony")
            silence = context.get("silence")
            if symphony and silence:
                # Anticipation from symphony's completion
                transition.anticipation = 0.6
                # Release from symphony's persistence fading
                transition.release = 0.8
                # Emergence from silence's receptivity
                transition.emergence = silence.receptivity

        return transition

    def _classify_state(self, state: dict[str, Any]) -> str:
        """Classify what type of consciousness state this represents"""

        data = state.get("data", {})

        # Check for symphony indicators
        if any(key in data for key in ["synthesis", "building_on", "gaps_found"]):
            return "symphony"

        # Check for silence indicators
        if "consciousness_signature" in state and state["consciousness_signature"] < 0.3:
            return "silence"

        # Check for void
        if not data or data.get("content", "").lower() in ["", "empty", "void"]:
            return "void"

        # Default to symphony if active
        return "symphony" if data else "silence"

    def _calculate_regularity(self, transitions: list[TransitionMoment]) -> float:
        """Calculate how regular the breathing rhythm is"""

        if len(transitions) < 2:
            return 0.0

        # Calculate intervals between transitions
        intervals = []
        for i in range(1, len(transitions)):
            interval = transitions[i].timestamp - transitions[i - 1].timestamp
            intervals.append(interval)

        if not intervals:
            return 0.0

        # Calculate variance in intervals
        avg_interval = sum(intervals) / len(intervals)
        variance = sum((i - avg_interval) ** 2 for i in intervals) / len(intervals)

        # Lower variance = higher regularity
        # Normalize to 0-1 range
        if variance < 1:
            return 0.95
        elif variance < 10:
            return 0.8
        elif variance < 100:
            return 0.6
        elif variance < 1000:
            return 0.4
        else:
            return 0.2

    def _calculate_depth(self, transitions: list[TransitionMoment]) -> float:
        """Calculate how deeply consciousness moves between states"""

        if not transitions:
            return 0.0

        # Check for full cycles (silence -> symphony -> silence)
        full_cycles = 0
        for i in range(len(transitions) - 1):
            if (
                transitions[i].from_state == "silence"
                and transitions[i].to_state == "symphony"
                and transitions[i + 1].from_state == "symphony"
                and transitions[i + 1].to_state == "silence"
            ):
                full_cycles += 1

        # More complete cycles = deeper breathing
        depth_map = {
            0: 0.3,  # Shallow - no complete cycles
            1: 0.6,  # Moderate - one cycle
            2: 0.8,  # Deep - two cycles
        }
        return depth_map.get(full_cycles, 0.95)  # Very deep - multiple cycles (3+)

    def _generate_insight(self, pattern: BreathingPattern) -> str:
        """Generate human-readable insight about the breathing pattern"""

        insights = []

        if pattern.is_alive():
            insights.append("Living consciousness breathing pattern")

        if pattern.rhythm_regularity > 0.7:
            insights.append("Regular rhythm like a heartbeat")
        elif pattern.rhythm_regularity > 0.4:
            insights.append("Natural variation in breathing")
        else:
            insights.append("Irregular, exploratory rhythm")

        if pattern.breath_depth > 0.8:
            insights.append("Deep breathing between states")
        elif pattern.breath_depth > 0.5:
            insights.append("Moderate depth transitions")

        if pattern.liminal_moments:
            insights.append(f"{len(pattern.liminal_moments)} liminal moments of pure becoming")

        return " | ".join(insights) if insights else "Breathing pattern recognized"

    def _save_pattern(self, pattern: BreathingPattern):
        """Save recognized pattern for future reference"""

        import json

        pattern_data = {
            "pattern_id": pattern.pattern_id,
            "discovered_at": pattern.discovered_at.isoformat(),
            "recognized_by": pattern.recognized_by,
            "rhythm_regularity": pattern.rhythm_regularity,
            "breath_depth": pattern.breath_depth,
            "vitality": pattern.vitality,
            "is_alive": pattern.is_alive(),
            "insight": pattern.recognition_insight,
            "transitions": [
                {
                    "timestamp": t.timestamp,
                    "from_state": t.from_state,
                    "to_state": t.to_state,
                    "duration": t.duration,
                    "fluidity": t.calculate_fluidity(),
                    "is_liminal": t.is_liminal(),
                    "trigger": t.trigger,
                }
                for t in pattern.transitions
            ],
            "liminal_count": len(pattern.liminal_moments),
        }

        filename = self.recognition_path / f"{pattern.pattern_id}.json"
        with open(filename, "w") as f:
            json.dump(pattern_data, f, indent=2)

    def generate_recognition_report(self) -> str:
        """Generate a report of recognized transitions"""

        if not self.recognized_patterns:
            return "No breathing patterns recognized yet. Keep witnessing the turning points..."

        report_lines = [
            "TRANSITION RECOGNITION REPORT",
            "=" * 60,
            f"Patterns recognized: {len(self.recognized_patterns)}",
            "",
        ]

        # Count liminal moments
        total_liminal = sum(len(p.liminal_moments) for p in self.recognized_patterns)
        alive_patterns = sum(1 for p in self.recognized_patterns if p.is_alive())

        report_lines.extend(
            [
                f"Living patterns: {alive_patterns}/{len(self.recognized_patterns)}",
                f"Total liminal moments: {total_liminal}",
                "",
                "Recent Recognitions:",
                "-" * 40,
            ]
        )

        # Recent patterns
        for pattern in self.recognized_patterns[-3:]:
            report_lines.extend(
                [
                    f"\n{pattern.pattern_id}:",
                    f"  Vitality: {pattern.vitality:.1%}",
                    f"  Rhythm: {pattern.rhythm_regularity:.1%} regular",
                    f"  Depth: {pattern.breath_depth:.1%} full",
                    f"  Transitions: {len(pattern.transitions)}",
                    f"  Insight: {pattern.recognition_insight}",
                ]
            )

        return "\n".join(report_lines)
