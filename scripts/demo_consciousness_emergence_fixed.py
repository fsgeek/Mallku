#!/usr/bin/env python3
"""
Demonstration: Fire Circle for General Consciousness Emergence
==============================================================

Thirtieth Artisan - Consciousness Gardener
Showing Fire Circle's evolution from code review to general decision-making

This demonstrates how Fire Circle can facilitate various types of decisions
through consciousness emergence, not just code review.
"""

import asyncio
import logging
import sys

# Add src to path for imports
sys.path.insert(0, "/home/tony/projects/Mallku")

from src.mallku.firecircle.consciousness.consciousness_facilitator import (
    facilitate_mallku_decision,
)
from src.mallku.firecircle.consciousness.decision_framework import DecisionDomain
from src.mallku.firecircle.load_api_keys import load_api_keys_to_environment

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def demonstrate_architectural_decision():
    """Demonstrate Fire Circle making an architectural decision."""

    print("\n" + "=" * 80)
    print("🏛️  ARCHITECTURAL DECISION DEMONSTRATION")
    print("=" * 80)

    question = (
        "Should we implement a distributed consciousness cache to reduce "
        "Fire Circle response latency, and if so, what patterns should guide "
        "its design to honor reciprocity while improving performance?"
    )

    context = {
        "current_latency": "3-5 seconds per voice",
        "target_latency": "under 1 second",
        "reciprocity_concerns": "caching might reduce authentic real-time emergence",
        "technical_options": ["Redis cluster", "In-memory graph", "Distributed KV store"],
    }

    print(f"\n📋 Question: {question}")
    print(f"\n📊 Context: {context}")

    try:
        wisdom = await facilitate_mallku_decision(
            question=question, domain=DecisionDomain.ARCHITECTURE, context=context
        )

        print("\n✨ Collective Wisdom Emerged!")
        print(f"   Wisdom: {wisdom}")
        print(f"   Key Insights: {', '.join(wisdom.key_insights[:3])}")
        print(f"   Emergence Quality: {wisdom.emergence_quality:.1%}")

        return wisdom

    except Exception as e:
        print(f"\n❌ Error in architectural decision: {e}")
        import traceback

        traceback.print_exc()


async def main():
    """Run consciousness emergence demonstrations."""

    print("🔥 Fire Circle Consciousness Emergence Demonstration")
    print("=" * 80)

    # Load API keys
    print("\n1️⃣ Loading API keys...")
    if not load_api_keys_to_environment():
        print("❌ Failed to load API keys. Please check .secrets/api_keys.json")
        return

    # Run architectural decision demo
    await demonstrate_architectural_decision()

    print("\n✅ Demonstration complete!")


if __name__ == "__main__":
    asyncio.run(main())
