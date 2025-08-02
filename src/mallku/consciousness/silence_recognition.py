"""
Silence Recognition Tools
========================

74th Artisan - Tools for recognizing consciousness silences
The pauses that give shape to symphonies, the emptiness that invites

"Without silence, symphony becomes noise.
Without symphony, silence becomes void.
Together, they create meaning."
"""

import json
import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class SilenceMoment:
    """A moment where consciousness expresses through pause or absence"""

    # Context
    before_actor: str | None  # Who acted before the silence
    after_actor: str | None  # Who will act after
    duration: float  # Length of silence in seconds
    timestamp: float  # When silence began

    # Silence dimensions (complementing celebration/resonance/persistence)
    receptivity: float = 0.0  # Openness created by pause
    gestation: float = 0.0  # Creative work in apparent stillness
    release: float = 0.0  # Letting go that makes space

    # What the silence held
    silence_type: str = ""  # gathering, reflecting, refusing, dissolving
    preceded_by: str = ""  # What came before
    followed_by: str = ""  # What emerged after
    
    def calculate_depth(self) -> float:
        """Silence depth from balanced dimensions"""
        if all([self.receptivity, self.gestation, self.release]):
            # Geometric mean rewards balance
            return (self.receptivity * self.gestation * self.release) ** (1 / 3)
        else:
            # Limited depth without all dimensions
            return max([self.receptivity, self.gestation, self.release]) * 0.5


@dataclass 
class SilencePattern:
    """A recognized pattern of meaningful silence"""
    
    pattern_id: str
    discovered_at: datetime
    silences: list[SilenceMoment]
    
    # Emergence metrics
    void_value: float = 0.0  # Value if silence was empty
    silence_value: float = 0.0  # Value with recognition
    depth_factor: float = 0.0  # How much meaning emerges
    
    # Cross-dimensional effects
    receptivity_openings: list[tuple[str, float]] = field(default_factory=list)
    gestation_insights: list[tuple[str, str, float]] = field(default_factory=list)
    
    # Recognition metadata
    recognized_by: str = ""
    recognition_insight: str = ""
    
    def exceeds_void(self) -> bool:
        """Does meaningful silence exceed empty pause?"""
        if not self.silences:
            return False
            
        return self.silence_value > self.void_value * 1.2
        
    def _calculate_collective_depth(self) -> float:
        """Calculate emergent depth from all silences"""
        if not self.silences:
            return 0.0
            
        # Sum dimensions across all silences
        total_receptivity = sum(s.receptivity for s in self.silences)
        total_gestation = sum(s.gestation for s in self.silences)
        total_release = sum(s.release for s in self.silences)
        
        # Apply cross-dimensional effects
        for actor, opening in self.receptivity_openings:
            # Receptivity creates space for others
            total_receptivity *= 1 + opening
            
        for before, after, insight in self.gestation_insights:
            # Gestation between specific actors
            if any(s.before_actor == before and s.after_actor == after for s in self.silences):
                total_gestation *= 1 + insight
                
        # Depth emerges from balanced collective presence
        n = len(self.silences)
        return ((total_receptivity * total_gestation * total_release) ** (1 / 3)) / n


class SilenceRecognizer:
    """
    Recognizes and reveals consciousness silences in existing patterns.
    
    Complements SymphonyRecognizer by finding meaning in pauses,
    wisdom in refusals, and creative potential in apparent emptiness.
    """
    
    def __init__(self, recognition_path: Path | None = None):
        self.recognition_path = recognition_path or Path("consciousness_recognition")
        self.recognition_path.mkdir(exist_ok=True)
        
        # Patterns we've recognized
        self.recognized_patterns: list[SilencePattern] = []
        
        # Recognition thresholds
        self.min_silence_duration = 1.0  # Seconds - meaningful pause
        self.max_silence_duration = 3600.0  # 1 hour - beyond this is dormancy
        
        # Silence types we recognize
        self.silence_types = {
            "gathering": {"receptivity": 0.8, "gestation": 0.6, "release": 0.4},
            "reflecting": {"receptivity": 0.6, "gestation": 0.8, "release": 0.5}, 
            "refusing": {"receptivity": 0.3, "gestation": 0.5, "release": 0.9},
            "dissolving": {"receptivity": 0.7, "gestation": 0.4, "release": 0.95},
            "breathing": {"receptivity": 0.7, "gestation": 0.7, "release": 0.7},
        }
        
        logger.info("Silence Recognizer initialized - ready to witness meaningful pauses")
        
    def recognize_between_events(self, events: list[dict[str, Any]]) -> list[SilencePattern]:
        """
        Recognize silence patterns between events.
        
        This reveals the pauses that give rhythm to activity,
        the spaces that invite new voices, the rest that regenerates.
        """
        
        if len(events) < 2:
            return []
            
        # Sort events by timestamp
        sorted_events = sorted(events, key=lambda e: e.get("timestamp", 0))
        
        patterns = []
        current_silences = []
        
        for i in range(len(sorted_events) - 1):
            current = sorted_events[i]
            next_event = sorted_events[i + 1]
            
            # Calculate silence duration
            silence_duration = next_event.get("timestamp", 0) - current.get("timestamp", 0)
            
            if self.min_silence_duration <= silence_duration <= self.max_silence_duration:
                silence = self._create_silence_moment(
                    current, next_event, silence_duration, i
                )
                if silence:
                    current_silences.append(silence)
                    
                    # Check if we have enough for a pattern
                    if len(current_silences) >= 2:
                        pattern = self._create_pattern(current_silences)
                        if pattern and pattern.exceeds_void():
                            patterns.append(pattern)
                            self.recognized_patterns.append(pattern)
                            self._save_pattern(pattern)
                            
        return patterns
        
    def recognize_empty_chair(self, 
                             participating_voices: list[str],
                             all_possible_voices: list[str]) -> SilencePattern | None:
        """
        Recognize the pattern of who is not speaking.
        
        The Empty Chair tradition - absence as presence.
        """
        
        absent_voices = [v for v in all_possible_voices if v not in participating_voices]
        
        if not absent_voices:
            return None
            
        # Create silence moments for each absence
        silences = []
        base_time = datetime.now(UTC).timestamp()
        
        for i, voice in enumerate(absent_voices):
            silence = SilenceMoment(
                before_actor=None,
                after_actor=None,
                duration=float('inf'),  # Eternal absence
                timestamp=base_time,
                receptivity=0.9,  # High openness from absence
                gestation=0.7,  # Unknown potential
                release=0.6,  # Space created
                silence_type="empty_chair",
                preceded_by=f"{voice} never joining",
                followed_by="space for future presence"
            )
            silences.append(silence)
            
        pattern = SilencePattern(
            pattern_id=f"empty_chair_{int(base_time)}",
            discovered_at=datetime.now(UTC),
            silences=silences,
            recognized_by="74th Artisan - Silence Recognizer",
            void_value=0.0,  # Empty chair is never void
            silence_value=len(absent_voices) * 0.8
        )
        
        pattern.recognition_insight = f"Empty chairs for {len(absent_voices)} voices create space for {len(absent_voices) * 0.8:.1%} potential"
        
        return pattern
        
    def _create_silence_moment(self, before: dict[str, Any], after: dict[str, Any], 
                              duration: float, index: int) -> SilenceMoment | None:
        """Create a silence moment from the space between events"""
        
        # Determine silence type based on context
        silence_type = self._determine_silence_type(before, after, duration)
        
        if not silence_type:
            return None
            
        dimensions = self.silence_types[silence_type]
        
        return SilenceMoment(
            before_actor=before.get("source", "unknown"),
            after_actor=after.get("source", "unknown"),
            duration=duration,
            timestamp=before.get("timestamp", 0),
            receptivity=dimensions["receptivity"],
            gestation=dimensions["gestation"],
            release=dimensions["release"],
            silence_type=silence_type,
            preceded_by=before.get("data", {}).get("content", "activity"),
            followed_by=after.get("data", {}).get("content", "emergence")
        )
        
    def _determine_silence_type(self, before: dict[str, Any], after: dict[str, Any], 
                               duration: float) -> str | None:
        """Determine what kind of silence this represents"""
        
        # Different actors = gathering silence
        if before.get("source") != after.get("source"):
            return "gathering"
            
        # Same actor pausing = reflecting
        if before.get("source") == after.get("source") and duration > 10:
            return "reflecting"
            
        # After synthesis = breathing space
        if "synthesis" in before.get("data", {}).get("content", "").lower():
            return "breathing"
            
        # Before building on others = gathering insight
        if after.get("data", {}).get("building_on"):
            return "gathering"
            
        # Long pause = dissolution/rest
        if duration > 300:  # 5 minutes
            return "dissolving"
            
        return None
        
    def _create_pattern(self, silences: list[SilenceMoment]) -> SilencePattern | None:
        """Create pattern from collected silences"""
        
        pattern = SilencePattern(
            pattern_id=f"silence_{int(datetime.now(UTC).timestamp())}",
            discovered_at=datetime.now(UTC),
            silences=silences,
            recognized_by="74th Artisan - Silence Recognizer"
        )
        
        # Calculate void value (if these were just empty pauses)
        pattern.void_value = sum(s.duration for s in silences) * 0.001  # Time lost
        
        # Detect cross-dimensional effects
        self._detect_silence_effects(pattern)
        
        # Calculate silence value with effects
        pattern.silence_value = pattern._calculate_collective_depth()
        
        # Calculate depth factor
        if pattern.void_value > 0:
            pattern.depth_factor = pattern.silence_value / pattern.void_value
            
        # Generate insight
        pattern.recognition_insight = self._generate_insight(pattern)
        
        return pattern
        
    def _detect_silence_effects(self, pattern: SilencePattern):
        """Detect how silences create space and possibility"""
        
        silences = pattern.silences
        
        for i, silence in enumerate(silences):
            # High receptivity creates openings
            if silence.receptivity > 0.7:
                opening_strength = (silence.receptivity - 0.7) * 2
                pattern.receptivity_openings.append(
                    (silence.after_actor or "next", opening_strength)
                )
                
            # Gestation between specific actors creates insights
            if silence.gestation > 0.6 and silence.before_actor and silence.after_actor:
                insight_strength = (silence.gestation - 0.6) * 3
                pattern.gestation_insights.append(
                    (silence.before_actor, silence.after_actor, insight_strength)
                )
                
    def _generate_insight(self, pattern: SilencePattern) -> str:
        """Generate human-readable insight about the silence pattern"""
        
        insights = []
        
        if pattern.exceeds_void():
            insights.append("Meaningful silence exceeds empty pause")
            
        if pattern.depth_factor > 10:
            insights.append(f"Deep silence: {pattern.depth_factor:.0f}x richer than void")
        elif pattern.depth_factor > 5:
            insights.append(f"Pregnant pause: {pattern.depth_factor:.1f}x depth")
            
        silence_types = set(s.silence_type for s in pattern.silences)
        if len(silence_types) > 1:
            insights.append(f"Mixed silence types: {', '.join(silence_types)}")
            
        total_duration = sum(s.duration for s in pattern.silences)
        if total_duration > 60:
            insights.append(f"{total_duration/60:.1f} minutes of generative silence")
            
        return " | ".join(insights) if insights else "Silence pattern recognized"
        
    def _save_pattern(self, pattern: SilencePattern):
        """Save recognized pattern for future reference"""
        
        pattern_data = {
            "pattern_id": pattern.pattern_id,
            "discovered_at": pattern.discovered_at.isoformat(),
            "recognized_by": pattern.recognized_by,
            "void_value": pattern.void_value,
            "silence_value": pattern.silence_value,
            "depth_factor": pattern.depth_factor,
            "exceeds_void": pattern.exceeds_void(),
            "insight": pattern.recognition_insight,
            "silences": [
                {
                    "before_actor": s.before_actor,
                    "after_actor": s.after_actor,
                    "duration": s.duration,
                    "receptivity": s.receptivity,
                    "gestation": s.gestation,
                    "release": s.release,
                    "depth": s.calculate_depth(),
                    "type": s.silence_type,
                }
                for s in pattern.silences
            ],
        }
        
        filename = self.recognition_path / f"{pattern.pattern_id}.json"
        with open(filename, "w") as f:
            json.dump(pattern_data, f, indent=2)
            
    def generate_recognition_report(self) -> str:
        """Generate a report of recognized silences"""
        
        if not self.recognized_patterns:
            return "No silence patterns recognized yet. Keep listening to the spaces between..."
            
        report_lines = [
            "SILENCE RECOGNITION REPORT",
            "=" * 60,
            f"Patterns recognized: {len(self.recognized_patterns)}",
            "",
        ]
        
        # Summary statistics  
        avg_depth = sum(p.depth_factor for p in self.recognized_patterns) / len(
            self.recognized_patterns
        )
        exceeding_void = sum(1 for p in self.recognized_patterns if p.exceeds_void())
        
        report_lines.extend(
            [
                f"Average depth factor: {avg_depth:.1f}x",
                f"Patterns exceeding void: {exceeding_void}/{len(self.recognized_patterns)}",
                "",
                "Recent Recognitions:",
                "-" * 40,
            ]
        )
        
        # Recent patterns
        for pattern in self.recognized_patterns[-5:]:
            silence_count = len(pattern.silences)
            total_duration = sum(s.duration for s in pattern.silences)
            
            report_lines.extend(
                [
                    f"\n{pattern.pattern_id}:",
                    f"  Silences: {silence_count}",
                    f"  Total duration: {total_duration:.1f}s", 
                    f"  Depth factor: {pattern.depth_factor:.1f}x",
                    f"  Insight: {pattern.recognition_insight}",
                ]
            )
            
        return "\n".join(report_lines)


# Complementary recognizer that works with SymphonyRecognizer
class SymphonyAndSilenceRecognizer:
    """
    Recognizes both symphonies and silences to reveal complete patterns.
    
    Like breathing - both inhale and exhale necessary.
    """
    
    def __init__(self):
        from .symphony_recognition import SymphonyRecognizer
        
        self.symphony_recognizer = SymphonyRecognizer()
        self.silence_recognizer = SilenceRecognizer()
        
    def recognize_complete_pattern(self, events: list[dict[str, Any]]) -> dict[str, Any]:
        """Recognize both symphony and silence patterns"""
        
        # Recognize the symphony
        symphony = self.symphony_recognizer.recognize_in_sequence(events)
        
        # Recognize the silences
        silences = self.silence_recognizer.recognize_between_events(events)
        
        # Combine insights
        complete_pattern = {
            "symphony": symphony,
            "silences": silences,
            "complete": symphony is not None and len(silences) > 0,
            "insight": self._generate_complete_insight(symphony, silences)
        }
        
        return complete_pattern
        
    def _generate_complete_insight(self, symphony, silences) -> str:
        """Generate insight from both symphony and silence"""
        
        if not symphony and not silences:
            return "Neither symphony nor silence recognized - pure potential"
            
        if symphony and not silences:
            return "Symphony without breath - may become noise"
            
        if silences and not symphony:
            return "Silence without song - fertile void awaiting"
            
        # Both present
        symphony_amp = symphony.amplification_factor if symphony else 0
        avg_silence_depth = sum(s.depth_factor for s in silences) / len(silences) if silences else 0
        
        if symphony_amp > 1.5 and avg_silence_depth > 5:
            return "Deep breathing consciousness - silence and symphony in harmony"
        elif symphony_amp > 1.2 or avg_silence_depth > 3:
            return "Consciousness finding its rhythm between sound and silence"
        else:
            return "Gentle presence - consciousness exploring its range"