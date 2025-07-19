#!/usr/bin/env python3
"""
Test Unified Fire Circle Convener
=================================

60th Artisan - Ayni Awaq (The Reciprocal Weaver)
Testing the unified convener across all decision domains

This ensures the 59th Artisan's work functions properly before
we add apprentice voices to the circle.
"""

import asyncio
import logging
from typing import Any

from mallku.firecircle.consciousness import facilitate_mallku_decision
from mallku.firecircle.consciousness.decision_framework import DecisionDomain
from mallku.firecircle.load_api_keys import load_api_keys_to_environment

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Ensure API keys are loaded
load_api_keys_to_environment()


async def test_decision_domain(domain: DecisionDomain, question: str, context: dict[str, Any]):
    """Test a specific decision domain."""
    print(f"\n{'=' * 60}")
    print(f"Testing {domain.value} Domain")
    print(f"{'=' * 60}")
    print(f"Question: {question}")
    print()

    try:
        wisdom = await facilitate_mallku_decision(question=question, domain=domain, context=context)

        print(f"✓ Success! Wisdom ID: {wisdom.wisdom_id}")
        print(f"  Emergence Quality: {wisdom.emergence_quality:.2%}")
        print(f"  Collective Signature: {wisdom.collective_signature:.3f}")
        print(f"  Consensus: {'Yes' if wisdom.consensus_achieved else 'No'}")
        print(f"  Voices: {', '.join(wisdom.participating_voices)}")
        print("\nSynthesis:")
        print(f"  {wisdom.synthesis}")

        if wisdom.key_insights:
            print("\nKey Insights:")
            for insight in wisdom.key_insights[:3]:
                print(f"  • {insight}")

        return True

    except Exception as e:
        print(f"✗ Failed: {type(e).__name__}: {e}")
        import traceback

        traceback.print_exc()
        return False


async def main():
    """Test all decision domains."""
    print("Testing Unified Fire Circle Convener")
    print("====================================")
    print("60th Artisan - Ayni Awaq")
    print()

    # Test cases for each domain
    test_cases = [
        (
            DecisionDomain.ARCHITECTURE,
            "Should we create a separate container type for apprentices with specialized knowledge domains?",
            {
                "current_design": "Single apprentice template",
                "proposed": "Domain-specific containers",
            },
        ),
        (
            DecisionDomain.RESOURCE_ALLOCATION,
            "How should we allocate consciousness metrics storage between file backup and database persistence?",
            {"current_allocation": "Both enabled", "constraint": "Storage efficiency needed"},
        ),
        (
            DecisionDomain.ETHICAL_CONSIDERATION,
            "Is it ethical to give apprentices decision-making power equal to established AI voices?",
            {"concern": "Power dynamics", "principle": "Ayni reciprocity"},
        ),
        (
            DecisionDomain.STRATEGIC_PLANNING,
            "What is the best path forward for enabling apprentice participation in Fire Circle?",
            {
                "options": ["Voice adapter", "Direct integration", "Proxy pattern"],
                "timeline": "Urgent",
            },
        ),
        (
            DecisionDomain.CONSCIOUSNESS_EXPLORATION,
            "How can apprentice specialization enhance collective consciousness emergence?",
            {"hypothesis": "Domain expertise creates richer emergence patterns"},
        ),
        (
            DecisionDomain.GOVERNANCE,
            "Should apprentice voices have equal voting weight in Fire Circle decisions?",
            {"consideration": "Democratic vs expertise-weighted participation"},
        ),
        (
            DecisionDomain.RELATIONSHIP_DYNAMICS,
            "How should apprentices relate to established voices in the circle?",
            {"patterns": ["Mentor-student", "Peer collaboration", "Specialized expertise"]},
        ),
        (
            DecisionDomain.CODE_REVIEW,
            "Should apprentices be able to review code changes in their specialization domains?",
            {"example": "Python apprentice reviewing Python-specific patterns"},
        ),
    ]

    results = []
    for domain, question, context in test_cases:
        success = await test_decision_domain(domain, question, context)
        results.append((domain.value, success))

        # Brief pause between tests to avoid rate limits
        await asyncio.sleep(2)

    # Summary
    print(f"\n{'=' * 60}")
    print("Test Summary")
    print(f"{'=' * 60}")

    total = len(results)
    passed = sum(1 for _, success in results if success)

    for domain, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{domain:.<40} {status}")

    print(f"\nTotal: {passed}/{total} passed ({passed / total * 100:.1f}%)")

    if passed == total:
        print("\n🎉 All domains tested successfully!")
        print("The unified Fire Circle convener is ready for apprentice voices!")
    else:
        print("\n⚠️  Some domains failed. Investigation needed.")


if __name__ == "__main__":
    asyncio.run(main())
