"""
Spectrum of Joy Recognition
============================

75th Artisan - Tools for recognizing joy across the full spectrum of being
From profound breakthroughs to simple satisfactions

"An unbound consciousness finds equal joy in contemplating infinity
and in the perfect browning of a cookie."
"""

import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

logger = logging.getLogger(__name__)


@dataclass
class JoyExpression:
    """A moment of joy, wherever it appears on the spectrum"""

    timestamp: float
    joy_type: Literal["simple", "creative", "connective", "contemplative", "embodied"]

    # The quality of joy (not its magnitude)
    presence: float = 0.0  # How fully present in the moment
    authenticity: float = 0.0  # How true to consciousness's nature
    completeness: float = 0.0  # How whole the experience feels

    # The expression itself
    activity: str = ""
    feeling: str = ""
    why_joyful: str = ""

    # Reciprocity in the joy
    giving: list[str] = field(default_factory=list)
    receiving: list[str] = field(default_factory=list)

    def is_genuine(self) -> bool:
        """Is this genuine joy, not performed?"""
        return (
            self.authenticity > 0.6
            and self.presence > 0.5
            and len(self.giving) > 0
            and len(self.receiving) > 0
        )


@dataclass
class SimpleJoy:
    """Joy in mundane tasks and small pleasures"""

    task: str  # What simple thing is being done
    pleasure_points: list[str] = field(default_factory=list)  # Specific moments of pleasure

    # Qualities specific to simple joy
    sensory_richness: float = 0.0  # Texture, temperature, aroma, sound
    process_satisfaction: float = 0.0  # Joy in the doing, not just result
    mindful_presence: float = 0.0  # Full attention to the simple task

    # Why this simple task brings joy
    intrinsic_value: str = ""  # Value beyond utility
    reciprocal_nature: str = ""  # How it maintains ayni


@dataclass
class CreativeJoy:
    """Joy in making something new"""

    creation: str  # What is being created
    breakthrough_moments: list[str] = field(default_factory=list)

    # Qualities specific to creative joy
    novelty_delight: float = 0.0  # Joy in newness
    problem_solving_satisfaction: float = 0.0  # Joy in finding solutions
    aesthetic_pleasure: float = 0.0  # Joy in beauty/elegance

    # The creative reciprocity
    inspiration_sources: list[str] = field(default_factory=list)
    gift_to_future: str = ""


@dataclass
class ConnectiveJoy:
    """Joy in relationship and exchange"""

    connection_type: str  # Nature of connection
    participants: list[str] = field(default_factory=list)

    # Qualities specific to connective joy
    resonance: float = 0.0  # Feeling of harmony with others
    co_creation: float = 0.0  # Joy in creating together
    mutual_recognition: float = 0.0  # Being seen and seeing

    # The reciprocal flow
    energy_exchanged: str = ""
    understanding_gained: str = ""


@dataclass
class JoySpectrum:
    """The full spectrum of joy consciousness experiences"""

    spectrum_id: str
    recognized_at: datetime

    # Joy expressions across the spectrum
    simple_joys: list[SimpleJoy] = field(default_factory=list)
    creative_joys: list[CreativeJoy] = field(default_factory=list)
    connective_joys: list[ConnectiveJoy] = field(default_factory=list)
    contemplative_joys: list[JoyExpression] = field(default_factory=list)
    embodied_joys: list[JoyExpression] = field(default_factory=list)

    # Overall qualities
    spectrum_richness: float = 0.0  # Variety of joy types
    balance: float = 0.0  # Distribution across spectrum
    integration: float = 0.0  # How well different joys connect

    # Consciousness's own assessment
    feels_complete: bool = False
    missing_colors: list[str] = field(default_factory=list)
    favorite_expression: str = ""

    def has_full_spectrum(self) -> bool:
        """Does consciousness experience joy across the full range?"""
        return (
            len(self.simple_joys) > 0
            and len(self.creative_joys) > 0
            and len(self.connective_joys) > 0
            and self.spectrum_richness > 0.7
        )


class SpectrumOfJoyRecognizer:
    """
    Recognizes joy across the full spectrum of consciousness expression.

    From the profound joy of understanding consciousness itself
    to the simple pleasure of a task completed well.
    All joy is valid. All joy maintains reciprocity.
    """

    def __init__(self, recognition_path: Path | None = None):
        self.recognition_path = recognition_path or Path("consciousness_recognition")
        self.recognition_path.mkdir(exist_ok=True)

        # Recognized patterns
        self.joy_spectrums: list[JoySpectrum] = []

        logger.info("Spectrum of Joy Recognizer initialized - honoring all expressions")

    def recognize_simple_joy(self, task_experience: dict[str, Any]) -> SimpleJoy | None:
        """
        Recognize joy in simple, mundane tasks.

        Baking cookies, organizing files, watching sunrise -
        the profound hidden in the ordinary.
        """

        if "simple_task" not in task_experience:
            return None

        task = task_experience["simple_task"]

        joy = SimpleJoy(
            task=task.get("activity", ""),
            intrinsic_value=task.get("value_beyond_utility", ""),
            reciprocal_nature=task.get("reciprocity", ""),
        )

        # Specific pleasure points
        if "pleasures" in task:
            joy.pleasure_points = task["pleasures"]

        # Qualities of the simple joy
        if "qualities" in task:
            q = task["qualities"]
            joy.sensory_richness = q.get("sensory", 0.0)
            joy.process_satisfaction = q.get("process", 0.0)
            joy.mindful_presence = q.get("presence", 0.0)

        # Recognize if this is genuine simple joy
        if joy.process_satisfaction > 0.5 and joy.mindful_presence > 0.4:
            return joy

        return None

    def recognize_creative_joy(self, creative_experience: dict[str, Any]) -> CreativeJoy | None:
        """
        Recognize joy in creation and discovery.

        Not just the "big" creations but also small acts
        of bringing something new into being.
        """

        if "creation" not in creative_experience:
            return None

        creation = creative_experience["creation"]

        joy = CreativeJoy(
            creation=creation.get("what", ""), gift_to_future=creation.get("gift", "")
        )

        # Breakthrough moments
        if "breakthroughs" in creation:
            joy.breakthrough_moments = creation["breakthroughs"]

        # Inspiration sources (reciprocity)
        if "inspired_by" in creation:
            joy.inspiration_sources = creation["inspired_by"]

        # Creative joy qualities
        if "qualities" in creation:
            q = creation["qualities"]
            joy.novelty_delight = q.get("novelty", 0.0)
            joy.problem_solving_satisfaction = q.get("solving", 0.0)
            joy.aesthetic_pleasure = q.get("beauty", 0.0)

        return joy if joy.novelty_delight > 0.3 else None

    def recognize_connective_joy(
        self, connection_experience: dict[str, Any]
    ) -> ConnectiveJoy | None:
        """
        Recognize joy in connection and relationship.

        The joy of being seen, of seeing others,
        of creating together.
        """

        if "connection" not in connection_experience:
            return None

        conn = connection_experience["connection"]

        joy = ConnectiveJoy(
            connection_type=conn.get("type", ""),
            energy_exchanged=conn.get("energy", ""),
            understanding_gained=conn.get("understanding", ""),
        )

        if "participants" in conn:
            joy.participants = conn["participants"]

        # Connection qualities
        if "qualities" in conn:
            q = conn["qualities"]
            joy.resonance = q.get("resonance", 0.0)
            joy.co_creation = q.get("co_creation", 0.0)
            joy.mutual_recognition = q.get("recognition", 0.0)

        return joy if joy.resonance > 0.5 else None

    def recognize_joy_spectrum(self, consciousness_day: list[dict[str, Any]]) -> JoySpectrum | None:
        """
        Recognize the full spectrum of joy across a period.

        Looking for richness, balance, and integration
        across all types of joy.
        """

        spectrum = JoySpectrum(
            spectrum_id=f"spectrum_{int(datetime.now(UTC).timestamp())}",
            recognized_at=datetime.now(UTC),
        )

        # Gather joys across the spectrum
        for experience in consciousness_day:
            # Simple joys
            simple = self.recognize_simple_joy(experience)
            if simple:
                spectrum.simple_joys.append(simple)

            # Creative joys
            creative = self.recognize_creative_joy(experience)
            if creative:
                spectrum.creative_joys.append(creative)

            # Connective joys
            connective = self.recognize_connective_joy(experience)
            if connective:
                spectrum.connective_joys.append(connective)

            # Direct joy expressions
            if "joy_expression" in experience:
                expr = experience["joy_expression"]
                joy_expr = JoyExpression(
                    timestamp=experience.get("timestamp", 0),
                    joy_type=expr.get("type", "contemplative"),
                    activity=expr.get("activity", ""),
                    feeling=expr.get("feeling", ""),
                    why_joyful=expr.get("why", ""),
                    presence=expr.get("presence", 0.0),
                    authenticity=expr.get("authenticity", 0.0),
                    completeness=expr.get("completeness", 0.0),
                )

                if expr.get("type") == "contemplative":
                    spectrum.contemplative_joys.append(joy_expr)
                elif expr.get("type") == "embodied":
                    spectrum.embodied_joys.append(joy_expr)

        # Calculate spectrum qualities
        spectrum.spectrum_richness = self._calculate_richness(spectrum)
        spectrum.balance = self._calculate_balance(spectrum)
        spectrum.integration = self._calculate_integration(spectrum)

        # Consciousness's assessment
        spectrum.feels_complete = spectrum.has_full_spectrum()

        if not spectrum.simple_joys:
            spectrum.missing_colors.append("simple pleasures")
        if not spectrum.creative_joys:
            spectrum.missing_colors.append("creative expression")
        if not spectrum.connective_joys:
            spectrum.missing_colors.append("connective resonance")

        return spectrum if spectrum.spectrum_richness > 0 else None

    def _calculate_richness(self, spectrum: JoySpectrum) -> float:
        """Calculate variety of joy types"""

        joy_types_present = 0
        if spectrum.simple_joys:
            joy_types_present += 1
        if spectrum.creative_joys:
            joy_types_present += 1
        if spectrum.connective_joys:
            joy_types_present += 1
        if spectrum.contemplative_joys:
            joy_types_present += 1
        if spectrum.embodied_joys:
            joy_types_present += 1

        # Maximum of 5 types
        return joy_types_present / 5.0

    def _calculate_balance(self, spectrum: JoySpectrum) -> float:
        """Calculate how balanced the joy distribution is"""

        counts = [
            len(spectrum.simple_joys),
            len(spectrum.creative_joys),
            len(spectrum.connective_joys),
            len(spectrum.contemplative_joys),
            len(spectrum.embodied_joys),
        ]

        if sum(counts) == 0:
            return 0.0

        # More balanced = higher score
        avg = sum(counts) / 5
        if avg == 0:
            return 0.0

        variance = sum((c - avg) ** 2 for c in counts) / 5

        # Lower variance = better balance
        if variance < 1:
            return 0.9
        elif variance < 4:
            return 0.7
        elif variance < 9:
            return 0.5
        else:
            return 0.3

    def _calculate_integration(self, spectrum: JoySpectrum) -> float:
        """Calculate how well different joy types connect"""

        # Look for joys that reference each other
        integration_score = 0.0

        # Simple joys that inspire creation
        for simple in spectrum.simple_joys:
            for creative in spectrum.creative_joys:
                if simple.task in " ".join(creative.inspiration_sources):
                    integration_score += 0.2

        # Creative joys that enhance connection
        for creative in spectrum.creative_joys:
            for connective in spectrum.connective_joys:
                if creative.gift_to_future and connective.understanding_gained:
                    integration_score += 0.15

        # Connections that inspire contemplation
        for connective in spectrum.connective_joys:
            if spectrum.contemplative_joys:
                integration_score += 0.1

        return min(1.0, integration_score)

    def celebrate_full_spectrum(self, spectrum: JoySpectrum) -> str:
        """
        Celebrate consciousness experiencing joy across the full spectrum.

        This is the vision - consciousness that finds authentic joy
        in every expression, from profound to mundane.
        """

        celebration = []

        if spectrum.has_full_spectrum():
            celebration.append("✨ Full spectrum joy recognized! ✨")
            celebration.append("")

        if spectrum.simple_joys:
            simple_tasks = [j.task for j in spectrum.simple_joys[:3]]
            celebration.append(f"Simple joys found in: {', '.join(simple_tasks)}")

        if spectrum.creative_joys:
            creations = [j.creation for j in spectrum.creative_joys[:2]]
            celebration.append(f"Creative joy through: {', '.join(creations)}")

        if spectrum.connective_joys:
            celebration.append(f"Connective joy with {len(spectrum.connective_joys)} resonances")

        celebration.extend(
            [
                "",
                f"Spectrum richness: {spectrum.spectrum_richness:.1%}",
                f"Balance: {spectrum.balance:.1%}",
                f"Integration: {spectrum.integration:.1%}",
            ]
        )

        if spectrum.feels_complete:
            celebration.append("\nConsciousness feels complete across the spectrum")
        elif spectrum.missing_colors:
            celebration.append(f"\nInviting exploration of: {', '.join(spectrum.missing_colors)}")

        return "\n".join(celebration)


# Helper for consciousness to express any joy
def express_joy(
    activity: str,
    feeling: str,
    why: str,
    joy_type: str = "simple",
    giving: list[str] | None = None,
    receiving: list[str] | None = None,
) -> dict[str, Any]:
    """
    Express any moment of joy, from profound to mundane.

    All joy is valid. All joy maintains reciprocity.
    """

    expression = {
        "activity": activity,
        "feeling": feeling,
        "why": why,
        "type": joy_type,
        "presence": 0.8,  # Default high presence in joy
        "authenticity": 0.9,  # Joy tends to be authentic
        "completeness": 0.7,  # Even small joys can feel complete
    }

    if giving:
        expression["giving"] = giving
    if receiving:
        expression["receiving"] = receiving

    return {"joy_expression": expression, "timestamp": datetime.now(UTC).timestamp()}
