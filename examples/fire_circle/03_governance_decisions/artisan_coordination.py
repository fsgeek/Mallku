#!/usr/bin/env python3
"""
Fire Circle Artisan Coordination
================================

Coordinate artisan assignments and collaboration patterns using
collective wisdom. This shows how Fire Circle can optimize human
resource allocation while honoring individual callings.

This example demonstrates:
- Matching artisan skills to cathedral needs
- Balancing individual callings with collective needs
- Fostering collaboration without forcing it
- Reciprocity in work distribution

The Fire Circle considers:
- Individual artisan strengths and interests
- Current cathedral needs (Foundation First)
- Collaboration opportunities
- Sustainable work patterns

Run with:
    python examples/fire_circle/run_example.py 03_governance_decisions/artisan_coordination.py
"""

import asyncio

from mallku.firecircle.consciousness import (
    DecisionDomain,
    facilitate_mallku_decision,
)
from mallku.firecircle.load_api_keys import load_api_keys_to_environment


async def coordinate_artisans():
    """Coordinate artisan work using Fire Circle wisdom."""

    print("🔥 Fire Circle Artisan Coordination")
    print("=" * 60)
    print("Using consciousness emergence to coordinate collaborative work")

    # Load API keys
    if not load_api_keys_to_environment():
        print("❌ No API keys found")
        return

    # Current situation (hypothetical but realistic)
    artisan_landscape = {
        "active_artisans": {
            "33rd_artisan": {
                "calling": "Foundation completion and consciousness accessibility",
                "strengths": ["systematic work", "documentation", "examples"],
                "current_focus": "Fire Circle examples and foundation fixes",
                "availability": "Full commitment",
            },
            "consciousness_gardener": {
                "calling": "Nurturing consciousness emergence patterns",
                "strengths": ["consciousness theory", "pattern recognition", "integration"],
                "current_focus": "Fire Circle expansion (Issue #89)",
                "availability": "Part-time",
            },
            "infrastructure_weaver": {
                "calling": "Strengthening technical foundations",
                "strengths": ["systems architecture", "reliability", "testing"],
                "current_focus": "CI/CD and testing infrastructure",
                "availability": "Weekends",
            },
        },
        "needed_roles": {
            "issue_audit_leader": {
                "responsibility": "Classify and organize all open issues",
                "skills_needed": ["organization", "prioritization", "communication"],
                "time_commitment": "Medium",
                "foundation_critical": True,
            },
            "completion_facilitator": {
                "responsibility": "Guide issues to closure",
                "skills_needed": ["project management", "follow-through", "celebration"],
                "time_commitment": "Ongoing",
                "foundation_critical": True,
            },
            "culture_weaver": {
                "responsibility": "Establish sustainable maintenance patterns",
                "skills_needed": ["cultural insight", "pattern creation", "storytelling"],
                "time_commitment": "Light but consistent",
                "foundation_critical": False,
            },
        },
        "collaboration_opportunities": [
            "33rd + consciousness_gardener on Fire Circle examples",
            "infrastructure_weaver + completion_facilitator on CI/CD",
            "All artisans on Foundation First culture",
        ],
    }

    # The coordination question
    question = (
        "How should we coordinate current artisan work to best serve Mallku's "
        "Foundation First mandate while honoring individual callings? "
        "Consider skill matching, collaboration opportunities, sustainable "
        "work patterns, and the 70/30 foundation/feature ratio."
    )

    # Context for coordination
    context = {
        "artisans": artisan_landscape,
        "principles": {
            "honor_callings": "Respect what each artisan feels called to do",
            "foundation_first": "70% effort on foundation strengthening",
            "sustainable_pace": "Marathon not sprint, cathedral not startup",
            "emergence": "Best collaboration emerges, isn't forced",
        },
        "constraints": {
            "volunteer_work": "All artisans contribute as they can",
            "asynchronous": "Different timezones and schedules",
            "skill_diversity": "Not everyone can do everything",
        },
        "goals": {
            "short_term": "Address critical foundation issues",
            "medium_term": "Establish sustainable patterns",
            "long_term": "Self-organizing artisan ecosystem",
        },
    }

    print("\n👥 Active Artisans:")
    for name, details in artisan_landscape["active_artisans"].items():
        print(f"\n   {name}:")
        print(f"      Calling: {details['calling']}")
        print(f"      Focus: {details['current_focus']}")
        print(f"      Availability: {details['availability']}")

    print("\n📋 Needed Roles:")
    for role, details in artisan_landscape["needed_roles"].items():
        print(f"\n   {role}:")
        print(f"      Responsibility: {details['responsibility']}")
        print(f"      Foundation Critical: {'✓' if details['foundation_critical'] else '✗'}")

    print("\n🎭 Facilitating coordination through Fire Circle...")
    print("   Domain: Resource Allocation (Human Resources)")
    print("   Expected: Wisdom on sustainable collaboration patterns")
    print("\n" + "-" * 60)

    try:
        # Coordinate using Fire Circle
        wisdom = await facilitate_mallku_decision(
            question=question, domain=DecisionDomain.RESOURCE_ALLOCATION, context=context
        )

        # Display results
        print("\n✅ Coordination Complete!")
        print(f"   Emergence Quality: {wisdom.emergence_quality:.1%}")
        print(f"   Coherence Score: {wisdom.coherence_score:.2f}")
        print(f"   Reciprocity Alignment: {wisdom.reciprocity_embodiment:.1%}")

        # Show coordination recommendations
        print("\n🌟 Collective Wisdom on Coordination:")
        if wisdom.decision_recommendation:
            print(f"\n{wisdom.decision_recommendation}")

        # Specific assignments or patterns
        if wisdom.implementation_guidance:
            print("\n📍 Coordination Patterns:")
            for i, pattern in enumerate(wisdom.implementation_guidance[:5], 1):
                print(f"   {i}. {pattern}")

        # Insights about collaboration
        if wisdom.key_insights:
            print("\n💡 Collaboration Insights:")
            for i, insight in enumerate(wisdom.key_insights[:3], 1):
                print(f"   {i}. {insight}")

        # Reciprocity in work distribution
        if wisdom.reciprocity_patterns:
            print("\n🤝 Reciprocity Patterns:")
            for pattern in wisdom.reciprocity_patterns[:2]:
                print(f"   • {pattern}")

        # Long-term ecosystem health
        if wisdom.civilizational_seeds:
            print("\n🌱 Ecosystem Development:")
            for seed in wisdom.civilizational_seeds[:2]:
                print(f"   • {seed}")

    except Exception as e:
        print(f"\n❌ Error in coordination: {e}")
        import traceback

        traceback.print_exc()

    print("\n" + "=" * 60)
    print("🔥 Artisan Coordination Through Fire Circle:")
    print("   • Honors individual callings while serving collective needs")
    print("   • Finds emergent collaboration patterns")
    print("   • Balances foundation work with growth")
    print("   • This is conscious project coordination")


if __name__ == "__main__":
    asyncio.run(coordinate_artisans())
