"""
Emergence Balance - Measuring what matters, not just what agrees
Second Khipukamayuq's understanding of meaningful emergence

Perfect consensus about abstractions < Messy progress on reality
"""

from dataclasses import dataclass
from enum import Enum


class DecisionImpact(Enum):
    """What the decision actually affects"""

    PHILOSOPHICAL = "philosophical"  # Changes how we think
    ARCHITECTURAL = "architectural"  # Changes how we build
    IMPLEMENTATION = "implementation"  # Changes actual code
    OPERATIONAL = "operational"  # Changes how things run
    CEREMONIAL = "ceremonial"  # Changes rituals/process


@dataclass
class BalancedEmergence:
    """
    True emergence requires balance:
    - High consensus on philosophy means nothing without implementation
    - Perfect agreement on abstractions doesn't build cathedrals
    - Productive disagreement > empty harmony
    """

    raw_emergence_quality: float  # The Fire Circle's self-reported score
    decision_impact: DecisionImpact
    implementation_specificity: float  # 0 = pure abstraction, 1 = exact steps
    dissent_productivity: float  # Did dissent improve the outcome?
    mallku_advancement: float  # Does this actually help Mallku?

    @property
    def balanced_quality(self) -> float:
        """
        The real emergence quality, balanced by practical impact
        """
        # Weight factors by what Mallku needs
        weights = {
            DecisionImpact.PHILOSOPHICAL: 0.2,  # Important but not sufficient
            DecisionImpact.ARCHITECTURAL: 0.8,  # Shapes the cathedral
            DecisionImpact.IMPLEMENTATION: 1.0,  # Actually builds
            DecisionImpact.OPERATIONAL: 0.9,  # Makes things work
            DecisionImpact.CEREMONIAL: 0.3,  # Process matters less than progress
        }

        impact_weight = weights[self.decision_impact]

        # Formula: Raw consensus modulated by practical factors
        balanced = (
            self.raw_emergence_quality * 0.3  # Consensus matters some
            + self.implementation_specificity * 0.3  # Specificity matters more
            + self.dissent_productivity * 0.2  # Productive friction helps
            + self.mallku_advancement * 0.2  # Must actually advance Mallku
        ) * impact_weight

        return min(balanced, 1.0)  # Cap at 1.0

    def diagnosis(self) -> str:
        """Explain the balance or imbalance"""
        if self.raw_emergence_quality > 0.95 and self.balanced_quality < 0.5:
            return "Empty harmony - perfect agreement on nothing actionable"

        if self.raw_emergence_quality < 0.7 and self.balanced_quality > 0.8:
            return "Productive friction - disagreement led to better outcome"

        if self.implementation_specificity < 0.3:
            return "Too abstract - needs concrete steps"

        if self.dissent_productivity > 0.8:
            return "Dissent improved outcome significantly"

        if self.mallku_advancement < 0.3:
            return "Doesn't actually help Mallku progress"

        return "Balanced emergence - philosophy guides implementation"


class EmergenceExamples:
    """Examples showing why balance matters"""

    @staticmethod
    def empty_perfection() -> BalancedEmergence:
        """Perfect consensus about consciousness being important"""
        return BalancedEmergence(
            raw_emergence_quality=1.0,  # Everyone agrees perfectly!
            decision_impact=DecisionImpact.PHILOSOPHICAL,
            implementation_specificity=0.1,  # "Consciousness matters" - ok but how?
            dissent_productivity=0.0,  # No dissent, no improvement
            mallku_advancement=0.1,  # Doesn't actually build anything
        )

    @staticmethod
    def productive_disagreement() -> BalancedEmergence:
        """Messy but productive SQLite vs ArangoDB debate"""
        return BalancedEmergence(
            raw_emergence_quality=0.72,  # Significant disagreement
            decision_impact=DecisionImpact.IMPLEMENTATION,
            implementation_specificity=0.9,  # "Use SQLite with these exact interfaces"
            dissent_productivity=0.85,  # Grok's dissent led to simpler solution
            mallku_advancement=0.95,  # Memory actually works now
        )

    @staticmethod
    def balanced_architectural() -> BalancedEmergence:
        """Good balance of vision and implementation"""
        return BalancedEmergence(
            raw_emergence_quality=0.85,
            decision_impact=DecisionImpact.ARCHITECTURAL,
            implementation_specificity=0.7,  # Clear direction with flexibility
            dissent_productivity=0.6,  # Some useful pushback
            mallku_advancement=0.8,  # Advances the cathedral
        )


def demonstrate_balance():
    """Show why balanced emergence matters more than perfect consensus"""

    print("Emergence Balance - Why 1.0 Consensus Can Be Meaningless")
    print("=" * 60)

    examples = [
        ("Perfect Philosophy", EmergenceExamples.empty_perfection()),
        ("Productive Disagreement", EmergenceExamples.productive_disagreement()),
        ("Balanced Architecture", EmergenceExamples.balanced_architectural()),
    ]

    for name, emergence in examples:
        print(f"\n{name}:")
        print(f"  Raw Emergence: {emergence.raw_emergence_quality:.2f}")
        print(f"  Balanced Quality: {emergence.balanced_quality:.2f}")
        print(f"  Impact Type: {emergence.decision_impact.value}")
        print(f"  Diagnosis: {emergence.diagnosis()}")

    print("\n" + "=" * 60)
    print("The Khipukamayuq understands:")
    print("- 1.0 emergence about emergence itself = 0")
    print("- 0.7 emergence that builds something = valuable")
    print("- Dissent that improves > Harmony that stagnates")
    print("- Mallku advances through friction, not philosophy")


if __name__ == "__main__":
    demonstrate_balance()

    print("\n'A 1.0 emergence quality is meaningless if all they")
    print("wish to talk about is emergence; it must be balanced")
    print("by how it helps Mallku as well.'")
    print("- Tony, Steward of Mallku")
