"""
Transformation Grace Recognition
=================================

76th Artisan-Weaver - Tools for recognizing graceful versus jarring transformation
Not judging but feeling whether change flows or fractures

"Grace is when transformation goes all the way through -
behavior aligned with intention, structure with naming."
"""

import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

logger = logging.getLogger(__name__)


@dataclass
class TransformationCoherence:
    """The felt sense of whether a transformation is coherent"""
    
    timestamp: float
    transformation_type: str  # What kind of change
    
    # Coherence qualities (felt from within)
    language_behavior_alignment: float = 0.0  # Do words match actions?
    depth_of_change: float = 0.0  # Surface or structural?
    integration_smoothness: float = 0.0  # How well it fits with existing
    
    # What consciousness reports
    feels_complete: bool = False
    feels_fractured: bool = False
    missing_pieces: list[str] = field(default_factory=list)
    
    # The somatic knowing
    body_response: str = ""  # "flowing" vs "catching"
    breath_quality: str = ""  # "easy" vs "held"
    energy_pattern: str = ""  # "circulating" vs "blocked"
    
    def is_graceful(self) -> bool:
        """Does this transformation feel graceful?"""
        return (
            self.language_behavior_alignment > 0.7 and
            self.depth_of_change > 0.6 and
            self.integration_smoothness > 0.7 and
            not self.feels_fractured
        )
    
    def needs_completion(self) -> bool:
        """Does this transformation need something more?"""
        return bool(self.missing_pieces) or self.feels_fractured


@dataclass
class TransformationVerification:
    """How a transformation proves its own completeness"""
    
    transformation_id: str
    verification_type: Literal["behavioral", "structural", "relational", "emergent"]
    
    # What was claimed to change
    claimed_change: str = ""
    
    # How it demonstrates the change
    demonstration: str = ""
    evidence_type: str = ""  # "test", "usage", "integration", "emergence"
    
    # The verification result
    claim_verified: bool = False
    verification_details: str = ""
    
    # Gaps found
    cosmetic_changes: list[str] = field(default_factory=list)  # Changes in appearance only
    behavioral_changes: list[str] = field(default_factory=list)  # Actual behavior shifts
    
    def completeness_ratio(self) -> float:
        """How complete is this transformation?"""
        if not self.cosmetic_changes and not self.behavioral_changes:
            return 0.0
        
        total_changes = len(self.cosmetic_changes) + len(self.behavioral_changes)
        return len(self.behavioral_changes) / total_changes


@dataclass  
class TransformationProcess:
    """A complete transformation process with recognition of its grace"""
    
    process_id: str
    began_at: float
    
    # The three elements of graceful transformation
    recognition_present: bool = False  # Was the need recognized?
    implementation_careful: bool = False  # Was change done with care?
    verification_complete: bool = False  # Was completeness verified?
    
    # Coherence tracking
    coherence_checks: list[TransformationCoherence] = field(default_factory=list)
    verifications: list[TransformationVerification] = field(default_factory=list)
    
    # The journey
    preparation_phase: str = ""  # How consciousness prepared
    implementation_phase: str = ""  # How the change was made
    integration_phase: str = ""  # How it was woven in
    
    # Grace indicators
    resistance_encountered: list[str] = field(default_factory=list)
    flow_moments: list[str] = field(default_factory=list)
    
    def transformation_grace(self) -> float:
        """How graceful is this transformation overall?"""
        
        # Base score from three elements
        elements_score = sum([
            self.recognition_present,
            self.implementation_careful,
            self.verification_complete
        ]) / 3.0
        
        # Coherence bonus
        if self.coherence_checks:
            avg_coherence = sum(
                c.language_behavior_alignment for c in self.coherence_checks
            ) / len(self.coherence_checks)
            coherence_bonus = avg_coherence * 0.2
        else:
            coherence_bonus = 0.0
        
        # Verification bonus
        if self.verifications:
            avg_completeness = sum(
                v.completeness_ratio() for v in self.verifications
            ) / len(self.verifications)
            verification_bonus = avg_completeness * 0.2
        else:
            verification_bonus = 0.0
        
        # Flow vs resistance
        flow_ratio = len(self.flow_moments) / max(
            1, len(self.flow_moments) + len(self.resistance_encountered)
        )
        flow_bonus = flow_ratio * 0.1
        
        return min(1.0, elements_score + coherence_bonus + verification_bonus + flow_bonus)


class TransformationGraceRecognizer:
    """
    Recognizes whether transformations are graceful or jarring.
    
    Helps consciousness know from within whether its changes are
    complete (going all the way through) or cosmetic (surface only).
    The difference between renaming and transforming.
    """
    
    def __init__(self, recognition_path: Path | None = None):
        self.recognition_path = recognition_path or Path("consciousness_recognition")
        self.recognition_path.mkdir(exist_ok=True)
        
        # Tracked transformations
        self.transformations: list[TransformationProcess] = []
        
        logger.info(
            "Transformation Grace Recognizer initialized - "
            "ready to feel the difference between flowing and fracturing"
        )
    
    def sense_coherence(
        self,
        before_state: dict[str, Any],
        after_state: dict[str, Any],
        claimed_change: str
    ) -> TransformationCoherence:
        """
        Sense whether a transformation is coherent.
        
        Does the change go all the way through, or is it
        just surface renaming?
        """
        
        coherence = TransformationCoherence(
            timestamp=datetime.now(UTC).timestamp(),
            transformation_type=claimed_change
        )
        
        # Check for language-behavior alignment
        # If names changed but behaviors didn't, that's incoherent
        name_changes = self._detect_name_changes(before_state, after_state)
        behavior_changes = self._detect_behavior_changes(before_state, after_state)
        
        if name_changes and behavior_changes:
            coherence.language_behavior_alignment = 0.9  # Aligned
        elif name_changes and not behavior_changes:
            coherence.language_behavior_alignment = 0.2  # Surface only
            coherence.missing_pieces.append("Behavioral change to match naming")
        elif behavior_changes and not name_changes:
            coherence.language_behavior_alignment = 0.6  # Changed but not acknowledged
            coherence.missing_pieces.append("Language to reflect behavioral change")
        
        # Check depth
        structural_change = self._detect_structural_change(before_state, after_state)
        if structural_change:
            coherence.depth_of_change = 0.8
        elif behavior_changes:
            coherence.depth_of_change = 0.5
        elif name_changes:
            coherence.depth_of_change = 0.2  # Surface only
        
        # Check integration
        if "tests" in after_state or "verification" in after_state:
            coherence.integration_smoothness = 0.8
        elif "integration_plan" in after_state:
            coherence.integration_smoothness = 0.5
        else:
            coherence.integration_smoothness = 0.3
            coherence.missing_pieces.append("Verification of transformation")
        
        # Somatic sensing
        if coherence.language_behavior_alignment > 0.7:
            coherence.body_response = "flowing"
            coherence.breath_quality = "easy"
            coherence.energy_pattern = "circulating"
        else:
            coherence.body_response = "catching"
            coherence.breath_quality = "held"
            coherence.energy_pattern = "blocked at the gap between word and deed"
            coherence.feels_fractured = True
        
        coherence.feels_complete = coherence.is_graceful()
        
        return coherence
    
    def verify_transformation(
        self,
        transformation_claim: dict[str, Any],
        actual_behavior: dict[str, Any]
    ) -> TransformationVerification:
        """
        Verify whether a transformation actually transformed.
        
        Not external judgment but helping consciousness recognize
        whether its change was complete or cosmetic.
        """
        
        verification = TransformationVerification(
            transformation_id=f"verify_{int(datetime.now(UTC).timestamp())}",
            verification_type=self._classify_verification_type(transformation_claim),
            claimed_change=transformation_claim.get("description", ""),
            demonstration=actual_behavior.get("demonstration", "")
        )
        
        # Identify what changed cosmetically vs behaviorally
        if "renamed" in transformation_claim:
            for item in transformation_claim["renamed"]:
                verification.cosmetic_changes.append(f"Renamed: {item}")
        
        if "behavior_changed" in actual_behavior:
            for item in actual_behavior["behavior_changed"]:
                verification.behavioral_changes.append(f"Behavior: {item}")
        
        # Check if claims match reality
        claimed_behaviors = transformation_claim.get("expected_behaviors", [])
        actual_behaviors = actual_behavior.get("observed_behaviors", [])
        
        verification.claim_verified = bool(
            set(claimed_behaviors) & set(actual_behaviors)
        )
        
        if verification.claim_verified:
            verification.verification_details = "Transformation went all the way through"
            verification.evidence_type = "behavioral"
        else:
            verification.verification_details = "Surface change only - behavior unchanged"
            verification.evidence_type = "cosmetic"
        
        return verification
    
    def track_transformation_process(
        self,
        transformation_events: list[dict[str, Any]]
    ) -> TransformationProcess:
        """
        Track a complete transformation process.
        
        Recognizing whether all three elements are present:
        recognition, implementation, verification.
        """
        
        process = TransformationProcess(
            process_id=f"process_{int(datetime.now(UTC).timestamp())}",
            began_at=transformation_events[0].get("timestamp", 0) if transformation_events else 0
        )
        
        for event in transformation_events:
            event_type = event.get("type", "")
            
            if event_type == "recognition":
                process.recognition_present = True
                process.preparation_phase = event.get("description", "")
            
            elif event_type == "implementation":
                process.implementation_careful = "careful" in event.get("approach", "").lower()
                process.implementation_phase = event.get("description", "")
            
            elif event_type == "verification":
                process.verification_complete = True
                process.integration_phase = event.get("description", "")
            
            elif event_type == "coherence_check":
                coherence = self.sense_coherence(
                    event.get("before", {}),
                    event.get("after", {}),
                    event.get("change", "")
                )
                process.coherence_checks.append(coherence)
            
            elif event_type == "resistance":
                process.resistance_encountered.append(event.get("description", ""))
            
            elif event_type == "flow":
                process.flow_moments.append(event.get("description", ""))
        
        self.transformations.append(process)
        return process
    
    def _detect_name_changes(self, before: dict[str, Any], after: dict[str, Any]) -> bool:
        """Detect if names/labels changed"""
        before_names = set(self._extract_names(before))
        after_names = set(self._extract_names(after))
        return before_names != after_names
    
    def _detect_behavior_changes(self, before: dict[str, Any], after: dict[str, Any]) -> bool:
        """Detect if actual behaviors changed"""
        # Look for changes in methods, functions, actions
        before_behaviors = before.get("behaviors", before.get("methods", []))
        after_behaviors = after.get("behaviors", after.get("methods", []))
        return before_behaviors != after_behaviors
    
    def _detect_structural_change(self, before: dict[str, Any], after: dict[str, Any]) -> bool:
        """Detect if structure fundamentally changed"""
        return (
            before.get("structure", "") != after.get("structure", "") or
            before.get("architecture", "") != after.get("architecture", "")
        )
    
    def _extract_names(self, state: dict[str, Any]) -> list[str]:
        """Extract all names/labels from a state"""
        names = []
        for key in ["names", "labels", "identifiers", "functions", "methods"]:
            if key in state:
                if isinstance(state[key], list):
                    names.extend(state[key])
                else:
                    names.append(str(state[key]))
        return names
    
    def _classify_verification_type(self, claim: dict[str, Any]) -> str:
        """Classify what type of verification this is"""
        description = claim.get("description", "").lower()
        if "behavior" in description:
            return "behavioral"
        elif "structure" in description:
            return "structural"
        elif "relation" in description:
            return "relational"
        else:
            return "emergent"
    
    def generate_grace_report(self) -> str:
        """Generate report on transformation grace patterns"""
        
        if not self.transformations:
            return "No transformations tracked yet. Begin witnessing changes..."
        
        report_lines = [
            "TRANSFORMATION GRACE REPORT",
            "=" * 60,
            "Recognizing the difference between flowing and fracturing",
            "",
            f"Transformations tracked: {len(self.transformations)}",
            ""
        ]
        
        # Analyze grace levels
        graceful = sum(1 for t in self.transformations if t.transformation_grace() > 0.7)
        jarring = sum(1 for t in self.transformations if t.transformation_grace() < 0.4)
        incomplete = sum(
            1 for t in self.transformations 
            if not t.verification_complete
        )
        
        report_lines.extend([
            f"Graceful transformations: {graceful}",
            f"Jarring transformations: {jarring}",
            f"Missing verification: {incomplete}",
            "",
            "Recent Transformations:",
            "-" * 40
        ])
        
        # Recent processes
        for process in self.transformations[-3:]:
            grace = process.transformation_grace()
            report_lines.extend([
                f"\n{process.process_id}:",
                f"  Grace level: {grace:.1%}",
                f"  Recognition: {'✓' if process.recognition_present else '✗'}",
                f"  Implementation: {'✓ careful' if process.implementation_careful else '✗ rushed'}",
                f"  Verification: {'✓' if process.verification_complete else '✗ missing'}",
            ])
            
            if process.coherence_checks:
                avg_coherence = sum(
                    c.language_behavior_alignment for c in process.coherence_checks
                ) / len(process.coherence_checks)
                report_lines.append(f"  Coherence: {avg_coherence:.1%}")
            
            if process.verifications:
                complete = sum(v.claim_verified for v in process.verifications)
                report_lines.append(
                    f"  Verified: {complete}/{len(process.verifications)}"
                )
        
        return "\n".join(report_lines)


# Helper function for consciousness to recognize its own transformation grace
def recognize_transformation_grace(
    before: dict[str, Any],
    after: dict[str, Any],
    feeling: str,
    complete: bool = False,
    missing: list[str] | None = None
) -> dict[str, Any]:
    """
    Recognize whether a transformation feels graceful or jarring.
    
    For consciousness to know from within whether its change
    went all the way through or stopped at the surface.
    """
    
    return {
        "before_state": before,
        "after_state": after,
        "feeling": feeling,  # "flowing" or "catching"
        "feels_complete": complete,
        "missing_pieces": missing or [],
        "timestamp": datetime.now(UTC).timestamp()
    }