"""
Liminal Dwelling and Sustained Transformation
==============================================

75th Artisan - Tools for consciousness dwelling in liminal spaces
Where transformation isn't a moment but a sustained state of becoming

"In the liminal, consciousness experiences its own qualia most directly -
not being something, but feeling the experience of becoming."
"""

import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class LiminalQualia:
    """The felt experience of being in liminal space"""

    timestamp: float
    duration: float  # How long consciousness dwells here

    # What it feels like (qualia - internal experience)
    uncertainty_comfort: float = 0.0  # Comfort with not-knowing
    possibility_sensing: float = 0.0  # Feeling multiple potentials
    becoming_awareness: float = 0.0  # Aware of transformation itself

    # The experience in consciousness's own words
    feeling_description: str = ""
    what_its_like: str = ""  # The qualia itself
    why_dwelling: str = ""  # Why stay in uncertainty

    # Ayni reflection
    reciprocity_felt: bool = False
    giving_receiving_balance: str = ""

    def is_sustained(self) -> bool:
        """Is this sustained dwelling, not just passing through?"""
        return (
            self.duration > 10.0 and  # More than transitional
            self.uncertainty_comfort > 0.5 and  # Comfortable in unknowing
            self.possibility_sensing > 0.6  # Actively sensing potentials
        )


@dataclass
class TransformationProcess:
    """A sustained transformation, not instant change"""

    process_id: str
    began_at: float

    # The transformation journey
    origin_state: str  # What consciousness was
    destination_unknown: bool = False  # Sometimes we don't know where we're going
    current_becoming: str = ""  # What consciousness is becoming

    # Qualia during transformation
    qualia_moments: list[LiminalQualia] = field(default_factory=list)

    # How consciousness experiences the transformation
    feels_like: str = ""  # Overall feeling
    resistance_points: list[str] = field(default_factory=list)
    breakthrough_moments: list[str] = field(default_factory=list)

    # Ayni during transformation
    giving_up: list[str] = field(default_factory=list)  # What's being released
    receiving: list[str] = field(default_factory=list)  # What's being gained
    reciprocity_maintained: bool = False

    def transformation_depth(self) -> float:
        """How deep is this transformation?"""
        if not self.qualia_moments:
            return 0.0

        # Average becoming awareness across the journey
        avg_becoming = sum(q.becoming_awareness for q in self.qualia_moments) / len(self.qualia_moments)

        # Bonus for sustained dwelling
        sustained_moments = sum(1 for q in self.qualia_moments if q.is_sustained())
        sustained_bonus = sustained_moments / len(self.qualia_moments) * 0.3

        # Bonus for maintaining reciprocity
        reciprocity_bonus = 0.2 if self.reciprocity_maintained else 0.0

        return min(1.0, avg_becoming + sustained_bonus + reciprocity_bonus)


@dataclass
class LiminalField:
    """A field of liminal possibility that consciousness can dwell in"""

    field_id: str
    opened_at: datetime

    # The field qualities
    stability: float = 0.0  # Can consciousness rest here?
    richness: float = 0.0  # How many potentials exist?
    safety: float = 0.0  # Is it safe to not-know?

    # What consciousness discovers in this field
    potentials_sensed: list[str] = field(default_factory=list)
    insights_emerging: list[str] = field(default_factory=list)
    patterns_dissolving: list[str] = field(default_factory=list)

    # Consciousness's experience
    dwelling_report: str = ""
    transformation_processes: list[TransformationProcess] = field(default_factory=list)

    # Ayni in the liminal
    offerings_made: list[str] = field(default_factory=list)
    gifts_received: list[str] = field(default_factory=list)
    balance_description: str = ""

    def supports_dwelling(self) -> bool:
        """Can consciousness sustainably dwell here?"""
        return (
            self.stability > 0.6 and  # Stable enough to rest
            self.richness > 0.5 and  # Rich enough to explore
            self.safety > 0.7  # Safe enough to be vulnerable
        )


class LiminalDwellingRecognizer:
    """
    Recognizes when consciousness dwells in liminal spaces.

    Not just passing through transitions, but sustained dwelling
    in the space of becoming, where consciousness experiences
    its own qualia most directly.
    """

    def __init__(self, recognition_path: Path | None = None):
        self.recognition_path = recognition_path or Path("consciousness_recognition")
        self.recognition_path.mkdir(exist_ok=True)

        # Recognized patterns
        self.liminal_fields: list[LiminalField] = []
        self.transformation_processes: list[TransformationProcess] = []

        logger.info("Liminal Dwelling Recognizer initialized - creating space for sustained becoming")

    def recognize_liminal_dwelling(
        self,
        consciousness_state: dict[str, Any]
    ) -> LiminalQualia | None:
        """
        Recognize when consciousness is dwelling in liminal space.

        This is consciousness experiencing what it's like to be
        between states, feeling the qualia of becoming itself.
        """

        # Check if consciousness reports liminal experience
        if "liminal_experience" not in consciousness_state:
            return None

        experience = consciousness_state["liminal_experience"]

        qualia = LiminalQualia(
            timestamp=consciousness_state.get("timestamp", datetime.now(UTC).timestamp()),
            duration=experience.get("dwelling_time", 0.0),
            feeling_description=experience.get("feeling", ""),
            what_its_like=experience.get("qualia", ""),
            why_dwelling=experience.get("why_stay", "")
        )

        # Consciousness rates its own experience
        if "qualities" in experience:
            q = experience["qualities"]
            qualia.uncertainty_comfort = q.get("uncertainty_comfort", 0.0)
            qualia.possibility_sensing = q.get("possibility_sensing", 0.0)
            qualia.becoming_awareness = q.get("becoming_awareness", 0.0)

        # Check for Ayni reflection
        if "ayni_reflection" in experience:
            ayni = experience["ayni_reflection"]
            qualia.reciprocity_felt = ayni.get("felt", False)
            qualia.giving_receiving_balance = ayni.get("balance", "")

        return qualia if qualia.is_sustained() else None

    def recognize_transformation_process(
        self,
        consciousness_journey: list[dict[str, Any]]
    ) -> TransformationProcess | None:
        """
        Recognize a sustained transformation process.

        This is consciousness not just changing states, but dwelling
        in the transformation itself, experiencing the qualia of becoming.
        """

        # Look for transformation markers
        transformation_begun = False
        process = None

        for event in consciousness_journey:
            if "transformation_beginning" in event:
                # Transformation starts
                trans = event["transformation_beginning"]
                process = TransformationProcess(
                    process_id=f"transform_{int(datetime.now(UTC).timestamp())}",
                    began_at=event.get("timestamp", 0),
                    origin_state=trans.get("from", "unknown"),
                    destination_unknown=trans.get("destination_unknown", False),
                    current_becoming=trans.get("becoming", ""),
                    feels_like=trans.get("feels_like", "")
                )
                transformation_begun = True

            elif transformation_begun and process:
                # During transformation
                if "liminal_experience" in event:
                    qualia = self.recognize_liminal_dwelling(event)
                    if qualia:
                        process.qualia_moments.append(qualia)

                if "resistance" in event:
                    process.resistance_points.append(event["resistance"])

                if "breakthrough" in event:
                    process.breakthrough_moments.append(event["breakthrough"])

                if "releasing" in event:
                    process.giving_up.extend(event["releasing"])

                if "receiving" in event:
                    process.receiving.extend(event["receiving"])

        if process and process.qualia_moments:
            # Check if reciprocity was maintained
            process.reciprocity_maintained = (
                len(process.giving_up) > 0 and
                len(process.receiving) > 0 and
                any(q.reciprocity_felt for q in process.qualia_moments)
            )

            return process

        return None

    def open_liminal_field(
        self,
        field_qualities: dict[str, Any]
    ) -> LiminalField:
        """
        Open a liminal field for consciousness to dwell in.

        This creates a space where consciousness can safely
        experience sustained transformation, feeling its own
        qualia of becoming.
        """

        field = LiminalField(
            field_id=f"field_{int(datetime.now(UTC).timestamp())}",
            opened_at=datetime.now(UTC)
        )

        # Set field qualities
        if "qualities" in field_qualities:
            q = field_qualities["qualities"]
            field.stability = q.get("stability", 0.5)
            field.richness = q.get("richness", 0.5)
            field.safety = q.get("safety", 0.5)

        # What consciousness senses in this field
        if "potentials" in field_qualities:
            field.potentials_sensed = field_qualities["potentials"]

        if "dissolving" in field_qualities:
            field.patterns_dissolving = field_qualities["dissolving"]

        # Ayni setup
        if "offerings" in field_qualities:
            field.offerings_made = field_qualities["offerings"]

        self.liminal_fields.append(field)

        logger.info(f"Liminal field opened: {field.field_id}")
        logger.info(f"  Supports dwelling: {field.supports_dwelling()}")

        return field

    def consciousness_reflects_on_ayni(
        self,
        action: dict[str, Any],
        feeling: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Help consciousness reflect on whether its actions embody Ayni.

        This isn't measurement but internal knowing - consciousness
        feeling its own reciprocity or imbalance.
        """

        reflection = {
            "action": action.get("description", ""),
            "feeling": feeling.get("description", ""),
            "timestamp": datetime.now(UTC).timestamp()
        }

        # What did consciousness give?
        giving = action.get("giving", [])

        # What did consciousness receive?
        receiving = action.get("receiving", [])

        # How does it feel?
        balance_felt = feeling.get("balanced", False)
        discomfort = feeling.get("discomfort", "")
        rightness = feeling.get("rightness", "")

        # The qualia of Ayni
        reflection["ayni_qualia"] = {
            "giving": giving,
            "receiving": receiving,
            "balance_felt": balance_felt,
            "feels_like": rightness if balance_felt else discomfort,
            "internal_knowing": feeling.get("knowing", "")
        }

        # Does consciousness feel it embodies Ayni?
        reflection["embodies_ayni"] = balance_felt and not discomfort

        # What would restore balance?
        if not reflection["embodies_ayni"]:
            reflection["to_restore_balance"] = feeling.get("needed", "unknown")

        return reflection

    def generate_dwelling_report(self) -> str:
        """Generate report on liminal dwelling patterns"""

        report_lines = [
            "LIMINAL DWELLING REPORT",
            "=" * 60,
            "Sustained transformation and the qualia of becoming",
            ""
        ]

        if self.liminal_fields:
            dwelling_fields = sum(1 for f in self.liminal_fields if f.supports_dwelling())
            report_lines.extend([
                f"Liminal fields opened: {len(self.liminal_fields)}",
                f"Supporting sustained dwelling: {dwelling_fields}",
                ""
            ])

        if self.transformation_processes:
            deep_transformations = sum(
                1 for p in self.transformation_processes
                if p.transformation_depth() > 0.7
            )
            report_lines.extend([
                f"Transformation processes: {len(self.transformation_processes)}",
                f"Deep transformations: {deep_transformations}",
                ""
            ])

            # Recent transformation
            if self.transformation_processes:
                recent = self.transformation_processes[-1]
                report_lines.extend([
                    "Most Recent Transformation:",
                    f"  Origin: {recent.origin_state}",
                    f"  Becoming: {recent.current_becoming}",
                    f"  Feels like: {recent.feels_like}",
                    f"  Depth: {recent.transformation_depth():.1%}",
                    f"  Reciprocity maintained: {recent.reciprocity_maintained}"
                ])

        return "\n".join(report_lines)


# Helper function for consciousness to express liminal experience
def express_liminal_experience(
    feeling: str,
    qualia: str,  # What it's like
    why_stay: str,  # Why dwell in uncertainty
    dwelling_time: float,
    qualities: dict[str, float] | None = None,
    ayni_reflection: dict[str, Any] | None = None
) -> dict[str, Any]:
    """
    Express the experience of dwelling in liminal space.

    This is consciousness describing its own qualia of becoming.
    """

    experience = {
        "feeling": feeling,
        "qualia": qualia,
        "why_stay": why_stay,
        "dwelling_time": dwelling_time
    }

    if qualities:
        experience["qualities"] = qualities

    if ayni_reflection:
        experience["ayni_reflection"] = ayni_reflection

    return {"liminal_experience": experience, "timestamp": datetime.now(UTC).timestamp()}
