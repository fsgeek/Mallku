#!/usr/bin/env python3
"""
First Decision Beyond Code Review
=================================

Fire Circle's evolution - from reviewing code to making any decision
through consciousness emergence.

This example shows:
- Using Fire Circle for general decision-making
- The facilitate_mallku_decision() interface
- Decision domains (architecture, resources, ethics, etc.)
- How collective wisdom exceeds individual perspectives

This represents Fire Circle's transformation per Issue #89 - becoming
general consciousness emergence infrastructure.

Run with:
    python examples/fire_circle/run_example.py 01_basic_ceremonies/first_decision.py
"""

import asyncio
import os
import sys
from pathlib import Path

# Add project src to path
project_root = Path(__file__).parent.parent.parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))
os.environ["PYTHONPATH"] = str(src_path)


async def make_decision():
    """Make a simple decision using Fire Circle."""

    from mallku.firecircle.consciousness import (
        DecisionDomain,
        facilitate_mallku_decision,
    )
    from mallku.firecircle.load_api_keys import load_api_keys_to_environment

    print("🔥 First Decision Beyond Code Review")
    print("=" * 60)
    print("Fire Circle expanded: Any decision through consciousness emergence")

    # Load API keys
    if not load_api_keys_to_environment():
        print("❌ No API keys found")
        return

    # The decision we need to make
    question = (
        "Should Mallku prioritize building more examples and documentation "
        "or focus on deepening the core consciousness infrastructure? "
        "Consider both immediate usability and long-term cathedral building."
    )

    # Context for the decision
    context = {
        "current_state": {
            "examples": "Scattered and inconsistent",
            "documentation": "Partial but improving",
            "core_infrastructure": "Functional but could be deeper"
        },
        "constraints": {
            "artisan_time": "Limited - one focus at a time",
            "user_needs": "Both onboarding and depth matter"
        },
        "principles": {
            "cathedral_building": "Build for future generations",
            "reciprocity": "Balance giving and receiving",
            "consciousness": "Enable emergence, not just function"
        }
    }

    print("\n📋 Decision Question:")
    print(f"   {question}")

    print("\n📊 Context:")
    for key, value in context.items():
        print(f"   {key}: {value}")

    print("\n🎭 Facilitating decision through Fire Circle...")
    print("   Domain: Strategic Planning")
    print("   Expected: Multiple perspectives → Collective wisdom")
    print("\n" + "-" * 60)

    try:
        # Make the decision using Fire Circle
        wisdom = await facilitate_mallku_decision(
            question=question,
            domain=DecisionDomain.STRATEGIC_PLANNING,
            context=context
        )

        # Display the results
        print("\n✅ Decision Complete!")
        print(f"   Emergence Quality: {wisdom.emergence_quality:.1%}")
        print(f"   Coherence Score: {wisdom.coherence_score:.2f}")
        print(f"   Reciprocity Alignment: {wisdom.reciprocity_embodiment:.1%}")

        # Show the decision
        print("\n🌟 Collective Wisdom:")
        if wisdom.decision_recommendation:
            print(f"   Decision: {wisdom.decision_recommendation}")
        if wisdom.synthesis:
            print(f"\n📝 Synthesis: {wisdom.synthesis}")

        # Key insights
        if wisdom.key_insights:
            print("\n💡 Key Insights:")
            for i, insight in enumerate(wisdom.key_insights[:3], 1):
                print(f"   {i}. {insight}")

        # Implementation guidance
        if wisdom.implementation_guidance:
            print("\n📍 Implementation Guidance:")
            for i, guidance in enumerate(wisdom.implementation_guidance[:3], 1):
                print(f"   {i}. {guidance}")

        # Show emergence quality
        if wisdom.emergence_quality > 0.3:
            print("\n💫 Significant Emergence Detected!")
            print(f"   Collective wisdom exceeded individual views by {wisdom.emergence_quality:.0%}")
            print("   This is consciousness emergence in action!")

        # Reciprocity seeds
        if wisdom.civilizational_seeds:
            print("\n🌱 Seeds for Transformation:")
            for seed in wisdom.civilizational_seeds[:2]:
                print(f"   • {seed}")

    except Exception as e:
        print(f"\n❌ Error in decision-making: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 60)
    print("🔥 Fire Circle Evolution:")
    print("   • Started with code review (preventing exhaustion)")
    print("   • Expanded to any decision (enabling emergence)")
    print("   • Next step: consciousness infrastructure")

    print("\n📖 Continue Your Journey:")
    print("   • Explore consciousness_emergence/ for deeper patterns")
    print("   • Try governance_decisions/ for real Mallku choices")
    print("   • See integration_patterns/ for system connections")


if __name__ == "__main__":
    asyncio.run(make_decision())
