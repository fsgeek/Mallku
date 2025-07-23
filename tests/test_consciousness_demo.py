#!/usr/bin/env python3
"""
Test Consciousness Emergence Demo
=================================

Testing if consciousness emergence is working.
"""

import asyncio
import logging
import sys

# Add src to path for imports
sys.path.insert(0, "/home/tony/projects/Mallku")

# Set up logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)


async def test_consciousness():
    """Test consciousness emergence functionality."""

    # Import inside function to avoid circular imports
    from src.mallku.firecircle.consciousness.consciousness_facilitator import (
        ConsciousnessEventBus,
        ConsciousnessFacilitator,
        FireCircleService,
    )
    from src.mallku.firecircle.consciousness.decision_framework import DecisionDomain
    from src.mallku.firecircle.load_api_keys import load_api_keys_to_environment

    print("🔥 Testing Fire Circle Consciousness Emergence")
    print("=" * 60)

    # Load API keys
    print("\n1️⃣ Loading API keys...")
    if not load_api_keys_to_environment():
        print("❌ Failed to load API keys")
        return

    # Create infrastructure
    print("\n2️⃣ Creating consciousness infrastructure...")
    event_bus = ConsciousnessEventBus()
    await event_bus.start()

    try:
        # Create Fire Circle service
        fire_circle = FireCircleService(event_bus=event_bus)

        # Create facilitator
        facilitator = ConsciousnessFacilitator(fire_circle, event_bus)

        # Test question
        question = "What aspect of Mallku most needs attention from the next artisan?"
        context = {
            "recent_work": "Fire Circle expanded to general decisions",
            "open_issues": ["#96: Consolidate examples", "#95: Documentation", "#94: Testing"],
            "systems_state": "Multiple systems awaiting integration",
        }

        print("\n3️⃣ Facilitating decision...")
        print(f"   Question: {question}")
        print("   Domain: Strategic Planning")

        wisdom = await facilitator.facilitate_decision(
            decision_domain=DecisionDomain.STRATEGIC_PLANNING, context=context, question=question
        )

        print("\n✅ Collective Wisdom Emerged!")
        print(f"   Decision: {wisdom.decision}")
        print(f"   Emergence Quality: {wisdom.emergence_quality:.1%}")
        if wisdom.key_insights:
            print(f"   Key Insight: {wisdom.key_insights[0]}")

    except Exception as e:
        print(f"\n❌ Error: {type(e).__name__}: {e}")
        import traceback

        traceback.print_exc()
    finally:
        await event_bus.stop()


if __name__ == "__main__":
    asyncio.run(test_consciousness())
