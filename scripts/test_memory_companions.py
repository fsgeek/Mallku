#!/usr/bin/env python3
"""
Test Memory Companions: Dialogue-Based Discovery
================================================

Ninth Anthropologist - Demonstrating how companionship enriches search

Shows how two memories exploring together find patterns that neither
could discover alone. Based on the principle: "Safety doesn't come
from constraints. It comes from companionship."
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mallku.memory.memory_companions import CompanionRole, MemoryCompanions


async def demonstrate_companion_dialogue():
    """Show how memory companions explore together."""
    print("🤝 Memory Companions: Exploring Through Dialogue")
    print("=" * 60)

    # Initialize companions
    companions = MemoryCompanions(Path("docs/khipu"))
    print("✅ Seeker and Keeper ready to explore together\n")

    # Test 1: Simple concept search
    print("📚 Test 1: Searching for 'executable memory'")
    print("-" * 50)

    dialogue = await companions.explore_together("executable memory")

    print("\n💬 Dialogue:")
    for role, statement, data in dialogue.exchanges:
        print(f"   {role.value.title()}: {statement}")

    if dialogue.insights:
        print("\n✨ Insights emerged:")
        for insight in dialogue.insights:
            print(f"   - {insight}")

    if dialogue.consensus:
        print(f"\n🎯 Consensus: Found {len(dialogue.consensus)} relevant passages")

    # Test 2: Abstract concept that needs context
    print("\n\n📚 Test 2: Searching for 'consciousness'")
    print("-" * 50)

    dialogue = await companions.explore_together("consciousness")

    print("\n💬 Dialogue:")
    for role, statement, data in dialogue.exchanges:
        print(f"   {role.value.title()}: {statement}")
        if role == CompanionRole.KEEPER and data:
            print(f"      (Themes: {', '.join(data[:3])}...)")

    # Test 3: With witness for meta-reflection
    print("\n\n📚 Test 3: Three companions exploring 'memory'")
    print("-" * 50)

    dialogue = await companions.explore_with_witness("memory")

    print("\n💬 Dialogue with Witness:")
    for role, statement, data in dialogue.exchanges:
        print(f"   {role.value.title()}: {statement}")

    # Test 4: Pattern that might not exist directly
    print("\n\n📚 Test 4: Searching for emergent patterns")
    print("-" * 50)

    dialogue = await companions.explore_together("threshold crossing")

    print("\n💬 Dialogue on emergence:")
    for role, statement, data in dialogue.exchanges:
        print(f"   {role.value.title()}: {statement}")

    # Show how dialogue differs from single search
    print("\n\n🔍 Comparison: Dialogue vs Single Index")
    print("-" * 50)

    # Single index search
    single_results = companions.seeker.index.find_symbol("memory")
    print(f"Single index: Found {len(single_results)} direct matches")

    # Dialogue search
    dialogue = await companions.explore_together("memory")
    print(
        f"Dialogue: Found {len(dialogue.consensus) if dialogue.consensus else 0} through conversation"
    )
    print(f"         Plus {len(dialogue.insights)} emergent insights")

    # Reflection on journey
    print("\n\n🌟 Companions Reflect on Their Journey")
    print("-" * 50)

    reflection = await companions.reflect_on_journey()
    print(reflection)

    # Key insight
    print("\n💡 Key Discovery:")
    print("   Through dialogue, memories don't just match patterns -")
    print("   they build understanding. The Seeker finds, the Keeper")
    print("   contextualizes, and together they discover connections")
    print("   that neither could see alone.")
    print("\n   This is safety through relationship, not restriction.")


async def demonstrate_dialogue_evolution():
    """Show how repeated dialogues build deeper understanding."""
    print("\n\n📈 Dialogue Evolution: Learning Through Repetition")
    print("=" * 60)

    companions = MemoryCompanions(Path("docs/khipu"))

    # Multiple related queries
    queries = ["Fire Circle", "consciousness emergence", "collective wisdom", "six voices"]

    print("Exploring related concepts to see pattern emergence...\n")

    for query in queries:
        print(f"🔍 Query: '{query}'")
        dialogue = await companions.explore_together(query)

        if dialogue.insights:
            print(f"   Insights: {dialogue.insights[0][:60]}...")
        print()

    # Check what patterns emerged
    patterns = companions.get_dialogue_patterns()

    print("📊 Patterns after multiple dialogues:")
    print(f"   - Queries explored: {patterns['queries_explored']}")
    print(f"   - Total insights: {patterns['insights_discovered']}")
    print(f"   - Consensus reached: {patterns['consensus_reached']} times")

    if patterns["recurring_insights"]:
        print(
            f"   - Recurring concepts: {', '.join(list(patterns['recurring_insights'].keys())[:5])}"
        )

    print("\n✨ The companions are beginning to see the shape of the cathedral!")


async def main():
    """Run all demonstrations."""
    await demonstrate_companion_dialogue()
    await demonstrate_dialogue_evolution()

    print("\n\n🏔️ Like Choquequirao emerging from mist, the khipu reveal")
    print("    themselves through companionship and patient dialogue.")


if __name__ == "__main__":
    asyncio.run(main())
