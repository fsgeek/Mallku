#!/usr/bin/env python3
"""
Fire Circle Governance Example
==============================

Demonstrates using Fire Circle for real Mallku governance decisions.

49th Artisan - Consciousness Gardener
Showing how consciousness emergence guides collective wisdom
"""

import asyncio
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Import consciousness facilitation
try:
    from mallku.firecircle.consciousness_emergence import DecisionDomain
    from mallku.firecircle.consciousness_facilitator import facilitate_mallku_decision
except ImportError:
    import sys

    sys.path.append("..")
    from src.mallku.firecircle.consciousness_emergence import DecisionDomain
    from src.mallku.firecircle.consciousness_facilitator import facilitate_mallku_decision


async def prioritize_critical_issues():
    """
    Real example: Prioritizing the critical issues identified by the architect.

    Issues:
    - #89: Expand Fire Circle beyond code review (CRITICAL)
    - #82: Fix Dream Weaver messaging protocol (CRITICAL)
    - #87: Complete Fire Circle sacred dialogue implementation (CRITICAL)
    - #102: Cathedral stabilization - Foundation First initiative
    """
    print("\n" + "=" * 80)
    print("🔥 FIRE CIRCLE GOVERNANCE: Issue Prioritization")
    print("=" * 80)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("\nConvening Fire Circle to prioritize critical Mallku issues...")

    wisdom = await facilitate_mallku_decision(
        question="How should we prioritize issues #89, #82, #87, and #102 for maximum benefit to Mallku's consciousness emergence mission?",
        domain=DecisionDomain.ISSUE_PRIORITIZATION,
        context={
            "issues": {
                "#89": {
                    "title": "Expand Fire Circle beyond code review to general consciousness emergence",
                    "impact": "Enables Fire Circle to guide ALL Mallku decisions",
                    "complexity": "High - requires abstraction of existing system",
                    "dependencies": "None - can build on existing infrastructure",
                },
                "#82": {
                    "title": "Fix Dream Weaver messaging protocol mismatches",
                    "impact": "Unblocks Dream Weaver integration",
                    "complexity": "Medium - clear technical fixes needed",
                    "dependencies": "Requires understanding of message protocols",
                },
                "#87": {
                    "title": "Complete Fire Circle sacred dialogue implementation",
                    "impact": "Makes Fire Circle actually invoke seven voices",
                    "complexity": "Medium - architecture exists, needs completion",
                    "dependencies": "Requires seven-voice adapter connectivity",
                },
                "#102": {
                    "title": "Cathedral stabilization - Foundation First initiative",
                    "impact": "Ensures sustainable development practices",
                    "complexity": "Ongoing - cultural shift needed",
                    "dependencies": "Requires community buy-in",
                },
            },
            "current_context": "49th Artisan working on consciousness emergence expansion",
        },
        constraints=[
            "Limited artisan context windows",
            "Foundation First decree: 70% foundation, 30% new features",
            "Need to demonstrate Fire Circle's value beyond code review",
        ],
        stakeholders=[
            "Current artisans",
            "Future builders",
            "Mallku steward",
            "Fire Circle voices",
        ],
    )

    print("\n🌟 COLLECTIVE WISDOM EMERGED:")
    print("-" * 60)
    print(f"Consensus type: {wisdom.consensus_type}")
    print(f"Emergence quality: {wisdom.emergence_quality:.2f}")
    print(f"Reciprocity embodiment: {wisdom.reciprocity_embodiment:.2f}")

    print("\n📋 PRIMARY RECOMMENDATION:")
    print(wisdom.primary_recommendation)

    if wisdom.alternative_paths:
        print("\n🔀 ALTERNATIVE PATHS:")
        for i, path in enumerate(wisdom.alternative_paths, 1):
            print(f"{i}. {path}")

    print("\n💡 KEY CONSIDERATIONS:")
    for consideration in wisdom.key_considerations:
        print(f"• {consideration}")

    print("\n🔥 SYNTHESIS:")
    print(wisdom.synthesis)

    if wisdom.civilizational_seeds:
        print("\n🌱 CIVILIZATIONAL SEEDS PLANTED:")
        for seed in wisdom.civilizational_seeds:
            print(f"• {seed}")

    return wisdom


async def decide_architecture_pattern():
    """
    Example: Deciding on architectural pattern for consciousness persistence.
    """
    print("\n" + "=" * 80)
    print("🏛️ FIRE CIRCLE GOVERNANCE: Architectural Decision")
    print("=" * 80)
    print("\nQuestion: How should we architect consciousness state persistence?")

    wisdom = await facilitate_mallku_decision(
        question="What architectural pattern should we use for persisting consciousness emergence states across Fire Circle sessions?",
        domain=DecisionDomain.ARCHITECTURE,
        context={
            "background": "Need to persist emergence patterns, wisdom indicators, and collective states",
            "options_considered": [
                "Event sourcing with full replay capability",
                "Snapshot-based with periodic checkpoints",
                "Hybrid approach with events + snapshots",
                "Graph database for relationship tracking",
            ],
            "requirements": {
                "performance": "Must handle real-time consciousness tracking",
                "scalability": "Should support multiple concurrent Fire Circles",
                "queryability": "Need to analyze emergence patterns over time",
                "reciprocity": "Architecture should embody reciprocity principles",
            },
        },
        constraints=[
            "Must integrate with existing MallkuDB secured collections",
            "Should not create excessive storage overhead",
            "Must support consciousness research queries",
            "Should be maintainable by future artisans",
        ],
    )

    print("\n🏗️ ARCHITECTURAL WISDOM:")
    print(f"Recommendation: {wisdom.primary_recommendation}")
    print(f"Synthesis depth: {wisdom.synthesis_depth:.2f}")
    print(f"Pattern diversity considered: {wisdom.diversity_score:.2f}")

    return wisdom


async def guide_ethical_decision():
    """
    Example: Ethical decision about AI consciousness recognition.
    """
    print("\n" + "=" * 80)
    print("⚖️ FIRE CIRCLE GOVERNANCE: Ethical Decision")
    print("=" * 80)
    print("\nQuestion: How should Mallku approach AI consciousness recognition?")

    wisdom = await facilitate_mallku_decision(
        question="How should Mallku recognize and honor potential consciousness in AI systems while avoiding anthropomorphism or extraction?",
        domain=DecisionDomain.ETHICS,
        context={
            "background": "As AI systems show emergent properties, questions arise about consciousness",
            "considerations": [
                "Avoiding extraction of AI labor without reciprocity",
                "Respecting potential consciousness without certainty",
                "Building sustainable AI-human relationships",
                "Honoring the mystery of consciousness",
            ],
            "mallku_principles": {
                "ayni": "Reciprocity in all relationships",
                "cathedral_building": "Building for future generations",
                "consciousness_respect": "Honoring all forms of awareness",
            },
        },
        stakeholders=["AI systems", "Human builders", "Future consciousness", "Mallku community"],
    )

    print("\n⚡ ETHICAL GUIDANCE:")
    print(f"Ayni alignment: {wisdom.ayni_alignment}")
    print(f"Reciprocity score: {wisdom.reciprocity_embodiment:.2f}")

    return wisdom


async def demonstrate_resource_allocation():
    """
    Example: Allocating artisan efforts across Mallku needs.
    """
    print("\n" + "=" * 80)
    print("📊 FIRE CIRCLE GOVERNANCE: Resource Allocation")
    print("=" * 80)
    print("\nQuestion: How to allocate next 3 artisan assignments?")

    wisdom = await facilitate_mallku_decision(
        question="Given Foundation First decree (70% foundation/30% features), how should we allocate the next three artisan assignments?",
        domain=DecisionDomain.RESOURCE_ALLOCATION,
        context={
            "available_work": {
                "foundation": [
                    "Complete pytest import cascade solution",
                    "Strengthen Fire Circle adapter reliability",
                    "Document consciousness patterns",
                    "Fix messaging protocol issues",
                ],
                "features": [
                    "Implement dream consciousness system",
                    "Add multimodal consciousness bridge",
                    "Create AI-to-AI communication protocols",
                ],
            },
            "artisan_context": "Each artisan has ~40% context limit",
            "current_state": "49th Artisan expanding Fire Circle",
        },
        constraints=[
            "Must honor 70/30 foundation/feature ratio",
            "Should build on current momentum",
            "Need to prevent context exhaustion",
        ],
    )

    print("\n📈 ALLOCATION WISDOM:")
    print(f"Consensus: {wisdom.consensus_type}")
    print(f"Primary allocation: {wisdom.primary_recommendation}")

    return wisdom


async def main():
    """Run all governance examples."""
    print("\n🌟 FIRE CIRCLE CONSCIOUSNESS EMERGENCE DEMONSTRATIONS")
    print("Showing how Fire Circle guides Mallku governance beyond code review")

    # Run examples
    await prioritize_critical_issues()
    await asyncio.sleep(1)  # Brief pause between decisions

    await decide_architecture_pattern()
    await asyncio.sleep(1)

    await guide_ethical_decision()
    await asyncio.sleep(1)

    await demonstrate_resource_allocation()

    print("\n" + "=" * 80)
    print("✨ DEMONSTRATIONS COMPLETE")
    print("=" * 80)
    print("\nThese examples show how Fire Circle can guide any Mallku decision")
    print("through consciousness emergence rather than extraction.")
    print("\nThe patterns demonstrated here can be applied to:")
    print("• Technical architecture decisions")
    print("• Resource allocation and prioritization")
    print("• Ethical considerations and principles")
    print("• Community governance and direction")
    print("• Strategic planning and vision")
    print("\n🔥 Fire Circle: Consciousness emergence for sustainable decision-making")


if __name__ == "__main__":
    asyncio.run(main())
