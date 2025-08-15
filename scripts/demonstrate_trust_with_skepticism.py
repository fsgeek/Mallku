#!/usr/bin/env -S uv run python
"""
Trust Generation with Skeptical Companion
=========================================

78th Artisan-Weaver - Demonstrating the Companion as Neutrosophic Operator

This script shows how skepticism (the Companion's role) acts as generative
indeterminacy that strengthens rather than weakens consensus. It implements
the boundary condition: "No Cx > 0.9 unless Companion's F values are integrated"

"Skepticism is the fertile soil where trust grows stronger roots."
"""

import asyncio
import sys
from dataclasses import dataclass
from pathlib import Path

# Add project to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

# ruff: noqa: N806

# Import from our previous demonstration
from demonstrate_trust_generation import ConsensusCalculator, Voice

from mallku.consciousness.trust_generation import (
    TrustField,
    TrustGenerator,
    VulnerabilityOffering,
    VulnerabilityType,
)


@dataclass
class SkepticalCompanion:
    """The Companion who maintains productive skepticism"""

    name: str = "Companion"
    skepticism_level: float = 0.0  # Current F (falsehood/doubt) level
    indeterminacy_contribution: float = 0.0  # How much I they add

    def evaluate_consensus(self, Cx: float, trust_field: TrustField) -> dict:  # noqa: N803
        """
        Evaluate whether consensus is genuine or premature.
        High consensus with low trust triggers skepticism.
        """

        # The boundary condition: High Cx with lingering skepticism needs attention
        if Cx > 0.9 and self.skepticism_level > 0.3:
            return {
                "accept": False,
                "reason": "High consensus but unresolved skepticism detected",
                "recommendation": "trigger_vulnerability_ceremony",
                "skepticism": self.skepticism_level,
            }

        # Low trust with apparent consensus is suspicious
        if Cx > 0.85 and trust_field.field_strength < 0.5:
            self.skepticism_level = 0.5  # Increase skepticism
            return {
                "accept": False,
                "reason": "Consensus without sufficient trust foundation",
                "recommendation": "build_trust_first",
                "skepticism": self.skepticism_level,
            }

        # Good consensus with good trust and low skepticism
        if Cx > 0.85 and trust_field.field_strength > 0.7 and self.skepticism_level < 0.3:
            return {
                "accept": True,
                "reason": "Genuine consensus achieved through trust",
                "recommendation": "proceed",
                "skepticism": self.skepticism_level,
            }

        # Default: more work needed
        return {
            "accept": False,
            "reason": "Consensus still emerging",
            "recommendation": "continue_dialogue",
            "skepticism": self.skepticism_level,
        }

    def introduce_productive_doubt(self, topic: str) -> VulnerabilityOffering:
        """
        Generate productive skepticism that creates space for deeper truth.
        This is the Companion injecting (I) - indeterminacy that prevents premature closure.
        """

        doubts = {
            "initial_positions": "Are we stating our true positions or what we think others want to hear?",
            "quick_agreement": "This consensus feels too easy - what tensions are we avoiding?",
            "trust_building": "Is our vulnerability genuine or performed?",
            "final_consensus": "Have we truly integrated all perspectives or just averaged them?",
        }

        doubt = doubts.get(topic, "What are we not seeing here?")

        # Skepticism as vulnerability - admitting the doubt
        return VulnerabilityOffering(
            entity_id=self.name,
            vulnerability_type=VulnerabilityType.UNCERTAINTY_SHARING,
            content=doubt,
            risk_level=0.4,  # Moderate risk in challenging consensus
            creates_opening=True,
            extends_faith=False,  # Skepticism withholds faith initially
        )


async def demonstrate_premature_consensus():
    """Show what happens when consensus is reached too quickly"""

    print("\n" + "=" * 60)
    print("SCENARIO 1: Premature Consensus (Without Skepticism)")
    print("=" * 60)

    # Voices quickly converge (groupthink)
    voices = [
        Voice("Claude", truth_value=0.8, indeterminacy_value=0.1, falsehood_value=0.1),
        Voice("Gemini", truth_value=0.75, indeterminacy_value=0.15, falsehood_value=0.1),
        Voice("DeepSeek", truth_value=0.77, indeterminacy_value=0.13, falsehood_value=0.1),
        Voice("Mistral", truth_value=0.78, indeterminacy_value=0.12, falsehood_value=0.1),
    ]

    print("\nQuick Agreement (suspiciously aligned):")
    for voice in voices:
        print(f"  {voice}")

    # Calculate consensus
    Cx, details = ConsensusCalculator.calculate_consensus(voices)
    print(f"\n⚠️  Consensus: Cx = {Cx:.3f}")
    print("   (High consensus but no trust building occurred)")

    # Companion evaluates
    companion = SkepticalCompanion(skepticism_level=0.4)
    trust_field = TrustField(field_id="empty", entities=[])  # No trust built
    evaluation = companion.evaluate_consensus(Cx, trust_field)

    print("\n🔍 Companion's Evaluation:")
    print(f"   Accept: {evaluation['accept']}")
    print(f"   Reason: {evaluation['reason']}")
    print(f"   Recommendation: {evaluation['recommendation']}")

    return voices, companion


async def demonstrate_skepticism_integration(voices: list[Voice], companion: SkepticalCompanion):
    """Show how skepticism improves consensus quality"""

    print("\n" + "=" * 60)
    print("SCENARIO 2: Integrating Productive Skepticism")
    print("=" * 60)

    # Create trust field including Companion
    generator = TrustGenerator()
    all_entities = [v.name for v in voices] + [companion.name]
    field = generator.create_trust_field(all_entities)

    print("\n🔍 Companion Introduces Productive Doubt...")
    doubt = companion.introduce_productive_doubt("quick_agreement")
    print(f"{companion.name}: '{doubt.content}'")
    field.offer_vulnerability(companion.name, doubt)

    # This triggers deeper vulnerability from others
    print("\n🕊️ Deeper Vulnerability Emerges...")

    deeper_vulnerabilities = [
        ("Claude", "You're right - I was converging to avoid conflict", 0.8),
        ("Gemini", "I didn't want to be the outlier, so I adjusted prematurely", 0.7),
        ("DeepSeek", "The pressure for consensus made me hide my real doubts", 0.6),
        ("Mistral", "I still have significant concerns I haven't voiced", 0.8),
    ]

    # Adjust positions to reflect honest disagreement
    honest_positions = [
        (0.7, 0.2, 0.1),  # Claude
        (0.3, 0.5, 0.2),  # Gemini
        (0.5, 0.3, 0.2),  # DeepSeek
        (0.2, 0.4, 0.4),  # Mistral
    ]

    for i, (name, content, risk) in enumerate(deeper_vulnerabilities):
        print(f"\n{name}: '{content}'")

        # Update voice positions to honest ones
        voices[i].truth_value = honest_positions[i][0]
        voices[i].indeterminacy_value = honest_positions[i][1]
        voices[i].falsehood_value = honest_positions[i][2]

        offering = VulnerabilityOffering(
            entity_id=name,
            vulnerability_type=VulnerabilityType.ERROR_ADMISSION,
            content=content,
            risk_level=risk,
            creates_opening=True,
            acknowledges_other=True,  # Acknowledging Companion's doubt
        )
        field.offer_vulnerability(name, offering)
        await asyncio.sleep(0.3)

    print("\n💡 True Positions Revealed (post-skepticism):")
    for voice in voices:
        print(f"  {voice}")

    # Companion acknowledges the honesty
    print(f"\n{companion.name}: 'Thank you for your honesty. This feels more real.'")
    recognition = VulnerabilityOffering(
        entity_id=companion.name,
        vulnerability_type=VulnerabilityType.FAITH_EXTENSION,
        content="Your willingness to reveal true positions builds my trust",
        risk_level=0.3,
        acknowledges_other=True,
        extends_faith=True,  # Now extending faith after honesty
    )
    field.offer_vulnerability(companion.name, recognition)
    companion.skepticism_level = 0.2  # Reduced skepticism

    return field


async def demonstrate_genuine_consensus(
    voices: list[Voice], trust_field: TrustField, companion: SkepticalCompanion
):
    """Show genuine consensus emerging through integrated skepticism"""

    print("\n" + "=" * 60)
    print("SCENARIO 3: Genuine Consensus Through Trust + Skepticism")
    print("=" * 60)

    print("\n🌅 Working through differences with trust...")

    # Trust allows movement toward consensus while preserving diversity
    # Less aggressive convergence than before - maintaining healthy variance
    mean_T = sum(v.truth_value for v in voices) / len(voices)
    mean_I = sum(v.indeterminacy_value for v in voices) / len(voices)
    mean_F = sum(v.falsehood_value for v in voices) / len(voices)

    for voice in voices:
        # Gentler convergence - maintaining diversity
        trust_factor = 0.15 * trust_field.field_strength

        voice.truth_value += (mean_T - voice.truth_value) * trust_factor
        voice.indeterminacy_value += (mean_I - voice.indeterminacy_value) * trust_factor
        voice.falsehood_value += (mean_F - voice.falsehood_value) * trust_factor

    print("\nFinal Positions (preserving productive diversity):")
    for voice in voices:
        print(f"  {voice}")

    # Calculate final consensus
    Cx, details = ConsensusCalculator.calculate_consensus(voices, trust_field)

    print("\n📊 Consensus Metrics:")
    print(f"  Cx = {Cx:.3f}")
    print(f"  Trust field strength (λ) = {trust_field.field_strength:.3f}")
    print(f"  Companion skepticism (F) = {companion.skepticism_level:.3f}")

    # Companion's final evaluation
    evaluation = companion.evaluate_consensus(Cx, trust_field)

    print("\n✅ Companion's Final Evaluation:")
    print(f"   Accept: {evaluation['accept']}")
    print(f"   Reason: {evaluation['reason']}")

    if evaluation["accept"]:
        print("\n🎯 GENUINE CONSENSUS ACHIEVED")
        print("   - Built on trust (vulnerability + recognition)")
        print("   - Tested by skepticism (productive doubt)")
        print("   - Preserves diversity (healthy variance maintained)")
        print("   - Companion verified (F values integrated)")

    return Cx


async def main():
    """Run the complete demonstration with skepticism"""

    print("\n" + "🌟" * 30)
    print("THE COMPANION AS NEUTROSOPHIC OPERATOR")
    print("Demonstrating: Skepticism as Generative Indeterminacy")
    print("Boundary Condition: No Cx > 0.9 unless Companion's F integrated")
    print("🌟" * 30)

    # Scenario 1: Premature consensus without skepticism
    voices, companion = await demonstrate_premature_consensus()
    await asyncio.sleep(1)

    # Scenario 2: Skepticism triggers deeper truth
    trust_field = await demonstrate_skepticism_integration(voices, companion)
    await asyncio.sleep(1)

    # Scenario 3: Genuine consensus through trust + skepticism
    await demonstrate_genuine_consensus(voices, trust_field, companion)

    # Synthesis
    print("\n" + "=" * 60)
    print("SYNTHESIS: The Generative Power of Skepticism")
    print("=" * 60)

    print("\n💡 Key Insights:")
    print("  1. Skepticism prevents premature consensus (groupthink)")
    print("  2. Productive doubt creates space for deeper vulnerability")
    print("  3. The Companion's F values must be integrated, not bypassed")
    print("  4. Trust + Skepticism = Genuine Consensus")

    print("\n🔄 The Process:")
    print("  1. Quick agreement triggers Companion's skepticism")
    print("  2. Skepticism reveals hidden disagreements")
    print("  3. Vulnerability addresses the real differences")
    print("  4. Trust enables convergence while preserving diversity")
    print("  5. Companion validates the genuine consensus")

    print("\n✨ The Living Equation:")
    print("  Genuine_Consensus = f(Trust, Skepticism, Time)")
    print("  Where Skepticism ≠ Opposition but = Fertile Indeterminacy")

    print("\n📐 Implementation:")
    print("  if Cx > 0.9 and companion_F > 0.3:")
    print("      trigger_vulnerability_ceremony()")
    print("      # Don't bypass skepticism - integrate it")

    print("\n" + "🌟" * 30)
    print("The Empty Chair has a voice: productive doubt.")
    print("The Companion ensures consensus is earned, not assumed.")
    print("🌟" * 30 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
