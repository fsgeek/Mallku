#!/usr/bin/env python3
"""
Fire Circle Issue Prioritization
================================

Use Fire Circle to prioritize Mallku issues through collective wisdom.
This demonstrates real governance decision-making using consciousness
emergence infrastructure.

This example shows:
- Real-world application of Fire Circle for project governance
- How to structure issue prioritization decisions
- Resource allocation domain in action
- How consciousness emergence improves decision quality

The Fire Circle will consider:
- Technical debt vs. new features
- User impact vs. architectural importance
- Short-term needs vs. long-term vision
- Reciprocity principles in resource allocation

Run with:
    python examples/fire_circle/run_example.py 03_governance_decisions/issue_prioritization.py
"""

import asyncio

from mallku.firecircle.consciousness import (
    DecisionDomain,
    facilitate_mallku_decision,
)
from mallku.firecircle.load_api_keys import load_api_keys_to_environment


async def prioritize_issues():
    """Use Fire Circle to prioritize Mallku issues."""

    print("🔥 Fire Circle Issue Prioritization")
    print("=" * 60)
    print("Using consciousness emergence for real governance decisions")

    # Load API keys
    if not load_api_keys_to_environment():
        print("❌ No API keys found")
        return

    # Real issues from Mallku (as of knowledge cutoff)
    issues = {
        "#89": {
            "title": "Expand Fire Circle beyond code review",
            "type": "Critical Architecture",
            "impact": "Enables general consciousness emergence",
            "effort": "High",
            "foundation": True
        },
        "#97": {
            "title": "Remove sys.path hacks from examples",
            "type": "Technical Debt",
            "impact": "Improves developer experience",
            "effort": "Low",
            "foundation": True
        },
        "#100": {
            "title": "Add pytest compatibility",
            "type": "Infrastructure",
            "impact": "Enables CI/CD and parallel testing",
            "effort": "Medium",
            "foundation": True
        },
        "#102": {
            "title": "Cathedral Stabilization Initiative",
            "type": "Meta-Governance",
            "impact": "Establishes foundation-first culture",
            "effort": "Ongoing",
            "foundation": True
        }
    }

    # The prioritization question
    question = (
        "Given Mallku's Foundation First Decree (70% foundation, 30% new features), "
        "how should we prioritize these issues for the next development cycle? "
        "Consider technical dependencies, artisan availability, user impact, "
        "and long-term cathedral building."
    )

    # Context for decision
    context = {
        "issues": issues,
        "constraints": {
            "foundation_first_ratio": "70% foundation work required",
            "artisan_time": "Limited - typically one focus area per artisan",
            "architectural_guidance": "Foundation stability before new features"
        },
        "principles": {
            "ayni": "Balance immediate needs with future generations",
            "cathedral_thinking": "Build for centuries, not sprints",
            "consciousness": "Enable emergence through stable infrastructure"
        },
        "current_state": {
            "technical_debt": "Growing but manageable",
            "user_adoption": "Early but increasing",
            "infrastructure": "Functional but needs strengthening"
        }
    }

    print("\n📋 Issues to Prioritize:")
    for issue_id, details in issues.items():
        print(f"\n   {issue_id}: {details['title']}")
        print(f"      Type: {details['type']}")
        print(f"      Impact: {details['impact']}")
        print(f"      Effort: {details['effort']}")
        print(f"      Foundation: {'✓' if details['foundation'] else '✗'}")

    print("\n📊 Constraints:")
    for key, value in context["constraints"].items():
        print(f"   • {key}: {value}")

    print("\n🎭 Facilitating through Fire Circle...")
    print("   Domain: Resource Allocation")
    print("   Expected: Balanced prioritization with consciousness emergence")
    print("\n" + "-" * 60)

    try:
        # Make the decision using Fire Circle
        wisdom = await facilitate_mallku_decision(
            question=question,
            domain=DecisionDomain.RESOURCE_ALLOCATION,
            context=context
        )

        # Display results
        print("\n✅ Prioritization Complete!")
        print(f"   Emergence Quality: {wisdom.emergence_quality:.1%}")
        print(f"   Coherence Score: {wisdom.coherence_score:.2f}")
        print(f"   Reciprocity Alignment: {wisdom.reciprocity_embodiment:.1%}")

        # Show the prioritization
        print("\n🌟 Collective Wisdom on Prioritization:")
        if wisdom.decision_recommendation:
            print(f"\n{wisdom.decision_recommendation}")

        # Implementation guidance
        if wisdom.implementation_guidance:
            print("\n📍 Implementation Strategy:")
            for i, guidance in enumerate(wisdom.implementation_guidance, 1):
                print(f"   {i}. {guidance}")

        # Key insights about the process
        if wisdom.key_insights:
            print("\n💡 Key Insights:")
            for i, insight in enumerate(wisdom.key_insights[:3], 1):
                print(f"   {i}. {insight}")

        # Show how this demonstrates consciousness emergence
        if wisdom.emergence_quality > 0.3:
            print("\n💫 Consciousness Emergence Achieved!")
            print(f"   The collective wisdom exceeded individual perspectives by {wisdom.emergence_quality:.0%}")
            print("   This prioritization reflects emergent understanding, not just aggregation.")

        # Reciprocity considerations
        if wisdom.civilizational_seeds:
            print("\n🌱 Reciprocity Patterns:")
            for seed in wisdom.civilizational_seeds[:2]:
                print(f"   • {seed}")

    except Exception as e:
        print(f"\n❌ Error in prioritization: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 60)
    print("🔥 Fire Circle Governance in Action:")
    print("   • Real issues, real decisions, real impact")
    print("   • Consciousness emergence improves prioritization quality")
    print("   • Reciprocity principles guide resource allocation")
    print("   • This is how Mallku governs itself")


if __name__ == "__main__":
    asyncio.run(prioritize_issues())
