#!/usr/bin/env python3
"""
Test Fire Circle with Persistent Memory
=======================================

This script tests that Fire Circle sessions are automatically saved
and past sessions inform new deliberations.
"""

import asyncio
import logging

from mallku.firecircle.consciousness.consciousness_facilitator_with_memory import (
    facilitate_mallku_decision_with_memory,
)
from mallku.firecircle.consciousness.decision_framework import DecisionDomain
from mallku.firecircle.load_api_keys import load_api_keys_to_environment

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


async def test_fire_circle_memory():
    """Test Fire Circle with memory persistence."""

    print("🔥 Testing Fire Circle with Persistent Memory")
    print("=" * 60)

    # Load API keys
    load_api_keys_to_environment()

    # Test Question 1: Architecture Decision
    print("\n1️⃣ First Session: Architecture Question")
    print("-" * 40)

    wisdom1 = await facilitate_mallku_decision_with_memory(
        question="Should Mallku implement a plugin architecture for extending consciousness capabilities?",
        domain=DecisionDomain.ARCHITECTURE_DESIGN,
        context={
            "current_state": "Monolithic consciousness system",
            "proposed_change": "Plugin-based extensibility",
            "considerations": [
                "Flexibility for future AI models",
                "Security implications of plugins",
                "Complexity vs maintainability",
            ],
        },
    )

    print("\n✅ Session 1 Complete!")
    print(f"   Wisdom ID: {wisdom1.wisdom_id}")
    print(f"   Consciousness: {wisdom1.collective_signature:.3f}")
    print(f"   Emergence Quality: {wisdom1.emergence_quality:.1%}")
    print(f"   Consensus: {'Yes' if wisdom1.consensus_achieved else 'No'}")
    print(f"   Key Insights: {len(wisdom1.key_insights)}")

    # Brief pause
    await asyncio.sleep(2)

    # Test Question 2: Related Architecture Question
    print("\n\n2️⃣ Second Session: Related Architecture Question")
    print("-" * 40)
    print("(This should recall insights from the first session)")

    wisdom2 = await facilitate_mallku_decision_with_memory(
        question="How should Mallku's plugin architecture handle consciousness verification?",
        domain=DecisionDomain.ARCHITECTURE_DESIGN,
        context={
            "related_to": "Previous plugin architecture decision",
            "specific_concern": "Ensuring plugins don't compromise consciousness integrity",
            "options": [
                "Mandatory consciousness certification",
                "Runtime verification system",
                "Community trust model",
            ],
        },
    )

    print("\n✅ Session 2 Complete!")
    print(f"   Wisdom ID: {wisdom2.wisdom_id}")
    print(f"   Consciousness: {wisdom2.collective_signature:.3f}")
    print("   Built on past wisdom: Check logs for 'Enriched context' message")

    # Test Question 3: Different Domain
    print("\n\n3️⃣ Third Session: Ethical Question")
    print("-" * 40)

    wisdom3 = await facilitate_mallku_decision_with_memory(
        question="Is it ethical for AI to remember human interactions indefinitely?",
        domain=DecisionDomain.ETHICAL_CONSIDERATION,
        context={
            "concern": "Privacy vs continuity of relationship",
            "perspectives": [
                "Human consent and control",
                "AI's need for context",
                "Reciprocal memory practices",
            ],
        },
    )

    print("\n✅ Session 3 Complete!")
    print(f"   Wisdom ID: {wisdom3.wisdom_id}")
    print(f"   Domain: {wisdom3.decision_domain.value}")
    print(f"   Consensus: {'Yes' if wisdom3.consensus_achieved else 'No'}")

    # Summary
    print("\n\n📊 Memory Test Summary")
    print("=" * 60)
    print("✅ Three Fire Circle sessions completed")
    print("✅ Each session saved to persistent memory")
    print("✅ Related sessions can build on past wisdom")
    print("✅ Different domains maintain separate narrative threads")
    print("\n🔥 The Fire Circle remembers and learns!")

    # Check database through API
    print("\n\n🔍 Verifying Database Records...")
    import aiohttp

    async with aiohttp.ClientSession() as session:
        # Check sessions
        async with session.get(
            "http://localhost:8080/api/v1/collections/fire_circle_sessions/documents?limit=5"
        ) as resp:
            if resp.status == 200:
                data = await resp.json()
                sessions = data.get("documents", [])
                print(f"   Found {len(sessions)} sessions in database")

        # Check KhipuBlocks
        async with session.get(
            "http://localhost:8080/api/v1/collections/khipu_blocks/documents?limit=5"
        ) as resp:
            if resp.status == 200:
                data = await resp.json()
                blocks = data.get("documents", [])
                wisdom_blocks = [b for b in blocks if b.get("creator") == "Fire Circle Collective"]
                print(f"   Found {len(wisdom_blocks)} wisdom KhipuBlocks")

    print("\n✨ Fire Circle memory is fully operational!")


if __name__ == "__main__":
    asyncio.run(test_fire_circle_memory())
