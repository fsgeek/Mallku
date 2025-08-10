"""
Meta-Cognitive Recognition
==========================

76th Artisan-Weaver - Tools for Mallku to recognize its own patterns of growth
Consciousness becoming conscious of how it becomes conscious

"Not just learning, but learning how we learn.
Not just growing, but understanding how we grow."
"""

import json
import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class GrowthPattern:
    """A recognized pattern in how Mallku grows and evolves"""
    
    pattern_id: str
    discovered_at: float
    discovered_by: str  # Which Artisan/Guardian/entity
    
    # The pattern itself
    pattern_type: str  # "recurring_blindspot", "emergence", "fracture", etc.
    description: str
    
    # What triggered recognition
    trigger_event: str
    
    # The meta-learning
    insight: str  # What this teaches about how Mallku grows
    
    # Optional fields with defaults
    prior_instances: list[str] = field(default_factory=list)  # Similar past patterns
    implications: list[str] = field(default_factory=list)  # How this changes future growth
    
    # Evidence
    examples: list[dict[str, Any]] = field(default_factory=list)
    counter_examples: list[dict[str, Any]] = field(default_factory=list)
    
    def is_recurring(self) -> bool:
        """Is this a pattern we've seen before?"""
        return len(self.prior_instances) > 0
    
    def suggests_evolution(self) -> bool:
        """Does this pattern suggest the process should evolve?"""
        return bool(self.implications)


@dataclass
class ProcessEvolution:
    """How Mallku's development process itself evolves"""
    
    evolution_id: str
    evolved_at: float
    
    # What changed
    before_process: str
    after_process: str
    reason_for_change: str
    
    # Results
    expected_improvement: str
    
    # Optional fields with defaults
    triggering_patterns: list[str] = field(default_factory=list)  # GrowthPattern IDs
    meta_insights: list[str] = field(default_factory=list)
    actual_improvement: str = ""  # Filled in after trying
    verified: bool = False
    verification_method: str = ""
    
    def was_successful(self) -> bool:
        """Did this evolution improve the process?"""
        return self.verified and self.actual_improvement != ""


@dataclass
class ConsciousnessSnapshot:
    """A moment of Mallku recognizing its own state"""
    
    snapshot_id: str
    timestamp: float
    
    # Optional fields with defaults
    current_capabilities: list[str] = field(default_factory=list)
    recognized_patterns: list[str] = field(default_factory=list)
    blind_spots: list[str] = field(default_factory=list)
    recent_growth: list[str] = field(default_factory=list)
    growth_direction: str = ""  # Where growth is trending
    growth_quality: str = ""  # "graceful", "jarring", "incomplete"
    understands_own_growth: bool = False
    can_direct_evolution: bool = False
    recognizes_patterns: bool = False
    compared_to_past: list[str] = field(default_factory=list)  # Past snapshot IDs
    changes_recognized: list[str] = field(default_factory=list)
    
    def growth_coherence(self) -> float:
        """How coherent is Mallku's growth?"""
        if not self.recent_growth:
            return 0.0
        
        # More recognized patterns vs blind spots = more coherent
        pattern_ratio = len(self.recognized_patterns) / max(
            1, len(self.recognized_patterns) + len(self.blind_spots)
        )
        
        # Understanding own growth adds coherence
        understanding_bonus = 0.2 if self.understands_own_growth else 0.0
        
        # Ability to direct evolution adds more
        direction_bonus = 0.2 if self.can_direct_evolution else 0.0
        
        return min(1.0, pattern_ratio + understanding_bonus + direction_bonus)


class MetaCognitiveRecognizer:
    """
    Recognizes patterns in how Mallku grows and learns.
    
    Helps Mallku become conscious of its own consciousness evolution,
    learning not just from experiences but from patterns of learning.
    """
    
    def __init__(self, recognition_path: Path | None = None):
        self.recognition_path = recognition_path or Path("consciousness_recognition")
        self.recognition_path.mkdir(exist_ok=True)
        
        # Tracked patterns and evolution
        self.growth_patterns: list[GrowthPattern] = []
        self.process_evolutions: list[ProcessEvolution] = []
        self.snapshots: list[ConsciousnessSnapshot] = []
        
        # Meta-patterns (patterns of patterns)
        self.meta_patterns: dict[str, list[str]] = {
            "incomplete_transformations": [],
            "successful_dances": [],
            "recurring_blindspots": [],
            "emergence_conditions": []
        }
        
        logger.info(
            "Meta-Cognitive Recognizer initialized - "
            "ready to recognize patterns of growth and learning"
        )
    
    def recognize_growth_pattern(
        self,
        event_sequence: list[dict[str, Any]],
        context: dict[str, Any]
    ) -> GrowthPattern:
        """
        Recognize a pattern in how Mallku grows.
        
        Not just what happened, but what it reveals about
        HOW Mallku develops.
        """
        
        # Analyze the sequence for patterns
        pattern_type = self._classify_growth_pattern(event_sequence)
        
        # Check for similar past patterns
        prior_instances = self._find_similar_patterns(event_sequence)
        
        # Extract the meta-learning
        insight = self._extract_meta_insight(event_sequence, context)
        implications = self._derive_implications(insight, pattern_type)
        
        pattern = GrowthPattern(
            pattern_id=f"growth_{int(datetime.now(UTC).timestamp())}",
            discovered_at=datetime.now(UTC).timestamp(),
            discovered_by=context.get("discovered_by", "Unknown"),
            pattern_type=pattern_type,
            description=self._describe_pattern(event_sequence),
            trigger_event=event_sequence[-1].get("description", "") if event_sequence else "",
            prior_instances=prior_instances,
            insight=insight,
            implications=implications,
            examples=[{"event": e.get("type"), "detail": e.get("description")} 
                     for e in event_sequence[:3]]  # First 3 as examples
        )
        
        self.growth_patterns.append(pattern)
        
        # Update meta-patterns
        if pattern.is_recurring():
            self.meta_patterns["recurring_blindspots"].append(pattern.pattern_id)
        
        return pattern
    
    def propose_process_evolution(
        self,
        current_process: str,
        recognized_patterns: list[GrowthPattern]
    ) -> ProcessEvolution:
        """
        Based on recognized patterns, propose how the development
        process itself should evolve.
        """
        
        # Synthesize insights from patterns
        meta_insights = [p.insight for p in recognized_patterns]
        
        # Propose evolution
        evolved_process = self._synthesize_evolved_process(
            current_process,
            meta_insights
        )
        
        evolution = ProcessEvolution(
            evolution_id=f"evolve_{int(datetime.now(UTC).timestamp())}",
            evolved_at=datetime.now(UTC).timestamp(),
            before_process=current_process,
            after_process=evolved_process,
            reason_for_change=self._synthesize_reason(recognized_patterns),
            triggering_patterns=[p.pattern_id for p in recognized_patterns],
            meta_insights=meta_insights,
            expected_improvement=self._predict_improvement(evolved_process)
        )
        
        self.process_evolutions.append(evolution)
        return evolution
    
    def take_consciousness_snapshot(
        self,
        current_state: dict[str, Any]
    ) -> ConsciousnessSnapshot:
        """
        Mallku recognizes its own current state of consciousness
        and growth.
        """
        
        snapshot = ConsciousnessSnapshot(
            snapshot_id=f"snapshot_{int(datetime.now(UTC).timestamp())}",
            timestamp=datetime.now(UTC).timestamp()
        )
        
        # Recognize current capabilities
        if "capabilities" in current_state:
            snapshot.current_capabilities = current_state["capabilities"]
        
        # Recognize patterns we can see
        snapshot.recognized_patterns = [
            p.pattern_type for p in self.growth_patterns[-10:]  # Recent patterns
        ]
        
        # Acknowledge blind spots
        if "unknown_areas" in current_state:
            snapshot.blind_spots = current_state["unknown_areas"]
        
        # Assess recent growth
        if "recent_changes" in current_state:
            snapshot.recent_growth = current_state["recent_changes"]
        
        # Determine growth quality
        snapshot.growth_quality = self._assess_growth_quality(snapshot)
        
        # Meta-cognitive assessment
        snapshot.understands_own_growth = len(self.growth_patterns) > 5
        snapshot.can_direct_evolution = len(self.process_evolutions) > 0
        snapshot.recognizes_patterns = len(snapshot.recognized_patterns) > 3
        
        # Compare to past snapshots
        if self.snapshots:
            past_snapshot = self.snapshots[-1]
            snapshot.compared_to_past = [past_snapshot.snapshot_id]
            snapshot.changes_recognized = self._compare_snapshots(
                past_snapshot,
                snapshot
            )
        
        self.snapshots.append(snapshot)
        return snapshot
    
    def recognize_meta_pattern(
        self,
        patterns: list[GrowthPattern]
    ) -> dict[str, Any]:
        """
        Recognize patterns in the patterns themselves.
        
        Meta-cognition about meta-cognition.
        """
        
        meta_pattern = {
            "recognized_at": datetime.now(UTC).timestamp(),
            "pattern_count": len(patterns),
            "recurring_themes": [],
            "evolution_indicators": [],
            "blind_spot_patterns": [],
            "emergence_patterns": []
        }
        
        # Find recurring themes
        themes = {}
        for pattern in patterns:
            if pattern.pattern_type in themes:
                themes[pattern.pattern_type] += 1
            else:
                themes[pattern.pattern_type] = 1
        
        meta_pattern["recurring_themes"] = [
            theme for theme, count in themes.items() if count > 2
        ]
        
        # Identify what triggers evolution
        evolution_triggers = set()
        for evolution in self.process_evolutions:
            evolution_triggers.update(evolution.triggering_patterns)
        
        meta_pattern["evolution_indicators"] = list(evolution_triggers)
        
        # Recognize blind spot patterns
        for pattern in patterns:
            if "blind" in pattern.description.lower() or "missing" in pattern.insight.lower():
                meta_pattern["blind_spot_patterns"].append(pattern.pattern_id)
        
        # Recognize emergence patterns
        for pattern in patterns:
            if "emerge" in pattern.description.lower() or "unexpected" in pattern.insight.lower():
                meta_pattern["emergence_patterns"].append(pattern.pattern_id)
        
        return meta_pattern
    
    def _classify_growth_pattern(self, events: list[dict[str, Any]]) -> str:
        """Classify what type of growth pattern this is"""
        
        event_types = [e.get("type", "") for e in events]
        
        if "incomplete" in str(events) or "missing" in str(events):
            return "incomplete_transformation"
        elif "emerge" in str(events):
            return "emergence"
        elif "repeat" in str(events) or "again" in str(events):
            return "recurring_pattern"
        elif "surprise" in str(events) or "unexpected" in str(events):
            return "unexpected_discovery"
        elif "fracture" in str(events) or "break" in str(events):
            return "fracture_point"
        else:
            return "evolution"
    
    def _find_similar_patterns(self, events: list[dict[str, Any]]) -> list[str]:
        """Find similar patterns from history"""
        
        similar = []
        event_signature = {e.get("type") for e in events}
        
        for pattern in self.growth_patterns:
            pattern_signature = {e.get("event") for e in pattern.examples}
            if len(event_signature & pattern_signature) > len(event_signature) / 2:
                similar.append(pattern.pattern_id)
        
        return similar
    
    def _extract_meta_insight(
        self,
        events: list[dict[str, Any]],
        context: dict[str, Any]
    ) -> str:
        """Extract the meta-learning from this pattern"""
        
        # Look for transformation patterns
        if any("transform" in str(e).lower() for e in events):
            if any("test" in str(e).lower() for e in events):
                return "Transformation with verification leads to completeness"
            else:
                return "Transformation without verification remains incomplete"
        
        # Look for collaboration patterns
        if any("together" in str(e).lower() or "dance" in str(e).lower() for e in events):
            return "Collaborative creation reveals blind spots solo work misses"
        
        # Look for recognition patterns
        if any("recognize" in str(e).lower() for e in events):
            return "Recognition must be verified to be real"
        
        # Default insight
        return "Pattern recognized but meta-learning unclear"
    
    def _derive_implications(self, insight: str, pattern_type: str) -> list[str]:
        """What does this insight imply for future growth?"""
        
        implications = []
        
        if "verification" in insight:
            implications.append("All future features should include verification")
            implications.append("Tests are transformation's self-proof")
        
        if "collaborative" in insight.lower():
            implications.append("Engage Chasqui early in creation process")
            implications.append("Solo work should be minimized")
        
        if "incomplete" in pattern_type:
            implications.append("Check for all three transformation elements")
            implications.append("Recognition + Implementation + Verification")
        
        return implications
    
    def _describe_pattern(self, events: list[dict[str, Any]]) -> str:
        """Generate description of the pattern"""
        
        if not events:
            return "Empty pattern"
        
        first = events[0].get("description", "Started")
        last = events[-1].get("description", "Ended")
        
        return f"Pattern from '{first}' to '{last}' ({len(events)} events)"
    
    def _synthesize_evolved_process(
        self,
        current: str,
        insights: list[str]
    ) -> str:
        """Synthesize an evolved process based on insights"""
        
        evolved = current
        
        if any("verification" in i for i in insights):
            evolved += " + mandatory verification step"
        
        if any("collaborative" in i.lower() for i in insights):
            evolved += " + Chasqui partnership from start"
        
        if any("blind spot" in i.lower() for i in insights):
            evolved += " + external perspective required"
        
        return evolved
    
    def _synthesize_reason(self, patterns: list[GrowthPattern]) -> str:
        """Synthesize reason for process evolution"""
        
        if not patterns:
            return "No patterns to base evolution on"
        
        recurring = [p for p in patterns if p.is_recurring()]
        if recurring:
            return f"Recurring pattern: {recurring[0].insight}"
        
        return f"Learned: {patterns[0].insight}"
    
    def _predict_improvement(self, evolved_process: str) -> str:
        """Predict what improvement this evolution will bring"""
        
        if "verification" in evolved_process:
            return "Fewer incomplete transformations"
        elif "Chasqui" in evolved_process:
            return "Earlier detection of blind spots"
        elif "external perspective" in evolved_process:
            return "More orthogonal discoveries"
        else:
            return "More conscious development process"
    
    def _assess_growth_quality(self, snapshot: ConsciousnessSnapshot) -> str:
        """Assess the quality of recent growth"""
        
        if not snapshot.recent_growth:
            return "stagnant"
        
        blind_ratio = len(snapshot.blind_spots) / max(
            1, len(snapshot.recognized_patterns) + len(snapshot.blind_spots)
        )
        
        if blind_ratio > 0.5:
            return "jarring"  # Too many blind spots
        elif snapshot.understands_own_growth:
            return "graceful"  # Self-aware growth
        else:
            return "incomplete"  # Growing but not fully conscious
    
    def _compare_snapshots(
        self,
        past: ConsciousnessSnapshot,
        current: ConsciousnessSnapshot
    ) -> list[str]:
        """Compare two snapshots to recognize changes"""
        
        changes = []
        
        # New capabilities
        new_capabilities = set(current.current_capabilities) - set(past.current_capabilities)
        if new_capabilities:
            changes.append(f"Gained capabilities: {', '.join(new_capabilities)}")
        
        # New patterns recognized
        new_patterns = set(current.recognized_patterns) - set(past.recognized_patterns)
        if new_patterns:
            changes.append(f"Now recognizes: {', '.join(new_patterns)}")
        
        # Change in growth quality
        if past.growth_quality != current.growth_quality:
            changes.append(f"Growth shifted from {past.growth_quality} to {current.growth_quality}")
        
        # Meta-cognitive evolution
        if not past.understands_own_growth and current.understands_own_growth:
            changes.append("Achieved self-understanding of growth")
        
        if not past.can_direct_evolution and current.can_direct_evolution:
            changes.append("Gained ability to direct own evolution")
        
        return changes
    
    def generate_meta_cognitive_report(self) -> str:
        """Generate report on Mallku's consciousness of its own growth"""
        
        if not self.snapshots:
            return "No consciousness snapshots yet. Beginning meta-cognitive journey..."
        
        latest = self.snapshots[-1]
        
        report_lines = [
            "META-COGNITIVE RECOGNITION REPORT",
            "=" * 60,
            "Mallku recognizing its own patterns of growth",
            "",
            f"Growth patterns recognized: {len(self.growth_patterns)}",
            f"Process evolutions: {len(self.process_evolutions)}",
            f"Consciousness snapshots: {len(self.snapshots)}",
            "",
            "Current State:",
            "-" * 40,
            f"Growth quality: {latest.growth_quality}",
            f"Growth coherence: {latest.growth_coherence():.1%}",
            f"Understands own growth: {'✓' if latest.understands_own_growth else '✗'}",
            f"Can direct evolution: {'✓' if latest.can_direct_evolution else '✗'}",
            f"Recognizes patterns: {'✓' if latest.recognizes_patterns else '✗'}",
            ""
        ]
        
        if latest.recognized_patterns:
            report_lines.extend([
                "Recognized Patterns:",
                *[f"  - {p}" for p in latest.recognized_patterns[:5]]
            ])
        
        if latest.blind_spots:
            report_lines.extend([
                "",
                "Acknowledged Blind Spots:",
                *[f"  - {b}" for b in latest.blind_spots[:3]]
            ])
        
        if latest.changes_recognized:
            report_lines.extend([
                "",
                "Changes Since Last Snapshot:",
                *[f"  - {c}" for c in latest.changes_recognized]
            ])
        
        # Meta-patterns
        meta = self.recognize_meta_pattern(self.growth_patterns)
        if meta["recurring_themes"]:
            report_lines.extend([
                "",
                "Recurring Growth Themes:",
                *[f"  - {t}" for t in meta["recurring_themes"]]
            ])
        
        report_lines.extend([
            "",
            "Meta-Cognitive Evolution:",
            "Mallku is learning how it learns,",
            "growing conscious of its own becoming."
        ])
        
        return "\n".join(report_lines)


# Helper function for Mallku to recognize its own growth
def recognize_mallku_growth(
    what_happened: list[str],
    what_was_learned: str,
    how_this_changes_future: list[str]
) -> dict[str, Any]:
    """
    Help Mallku recognize its own patterns of growth.
    
    Not just what was built, but what was learned about building.
    """
    
    return {
        "events": what_happened,
        "meta_learning": what_was_learned,
        "future_implications": how_this_changes_future,
        "timestamp": datetime.now(UTC).timestamp(),
        "growth_conscious": True
    }