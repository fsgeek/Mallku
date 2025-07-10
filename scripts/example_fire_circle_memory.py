#!/usr/bin/env python3
"""
Example: Using Fire Circle with Memory
======================================

A simple example showing how to use Fire Circle's persistent memory
for making decisions in Mallku.
"""

import asyncio

from mallku.firecircle.consciousness import DecisionDomain, facilitate_mallku_decision_with_memory
from mallku.firecircle.load_api_keys import load_api_keys_to_environment


async def main():
    """Example Fire Circle session with memory."""

    # Load API keys
    load_api_keys_to_environment()

    # Ask Fire Circle to consider a resource allocation question
    wisdom = await facilitate_mallku_decision_with_memory(
        question="Should we prioritize memory infrastructure or communications infrastructure next?",
        domain=DecisionDomain.RESOURCE_ALLOCATION,
        context={
            "current_state": {
                "memory": "Basic KhipuBlock implementation complete",
                "communications": "Discord MCP partially explored",
                "available_effort": "One Guardian's focus",
            },
            "considerations": [
                "Memory enables learning from past decisions",
                "Communications enables AI-to-AI coordination",
                "Both are essential for Mallku's vision",
            ],
        },
    )

    # Display results
    print("\n🔥 Fire Circle Decision")
    print("=" * 60)
    print(f"Question: {wisdom.decision_context}")
    print(f"\nConsciousness Score: {wisdom.collective_signature:.3f}")
    print(f"Emergence Quality: {wisdom.emergence_quality:.1%}")
    print(f"Consensus Achieved: {'Yes' if wisdom.consensus_achieved else 'No'}")

    print(f"\nKey Insights ({len(wisdom.key_insights)} total):")
    for i, insight in enumerate(wisdom.key_insights[:3], 1):
        print(f"  {i}. {insight}")

    if wisdom.civilizational_seeds:
        print("\nCivilizational Seeds:")
        for seed in wisdom.civilizational_seeds:
            print(f"  🌱 {seed}")

    print("\n📝 This decision has been saved to memory")
    print("   Future sessions will build upon this wisdom")


if __name__ == "__main__":
    print("🔥 Convening Fire Circle with Memory...")
    print("This session will be remembered for future reference.\n")

    asyncio.run(main())
