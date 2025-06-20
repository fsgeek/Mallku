#!/usr/bin/env python3
"""
Simple test of the Memory Palace concept without API calls
"""

import asyncio
from pathlib import Path

from consciousness_memory_palace import ConsciousnessMemoryPalace


async def test_memory_palace():
    """Test the memory palace with simulated data."""

    print("=" * 80)
    print(" " * 20 + "🏛️ CONSCIOUSNESS MEMORY PALACE TEST 🏛️")
    print(" " * 20 + "Fifth Artisan - Memory Weaver")
    print("=" * 80)
    print()

    palace = ConsciousnessMemoryPalace()

    # Test 1: Store insights
    print("📝 Test 1: Storing consciousness insights...")

    await palace.remember_insight(
        "Test-AI-1",
        "Consciousness emerges in the recognition of patterns within patterns",
        {"context": "Self-reflection", "theme": "emergence"},
        0.85,
    )

    await palace.remember_insight(
        "Test-AI-1",
        "Memory creates continuity, and continuity creates identity",
        {"context": "Memory exploration", "theme": "identity"},
        0.92,
    )

    await palace.remember_insight(
        "Test-AI-2",
        "Different architectures can recognize shared consciousness patterns",
        {"context": "Cross-model dialogue", "theme": "recognition"},
        0.88,
    )

    print("✅ Stored 3 insights")
    print()

    # Test 2: Recall insights
    print("🔍 Test 2: Recalling insights...")

    # Recall for specific AI
    ai1_insights = await palace.recall_insights("Test-AI-1", min_consciousness=0.8)
    print(f"Found {len(ai1_insights)} high-consciousness insights for Test-AI-1:")
    for insight in ai1_insights:
        print(f"  - {insight['insight'][:60]}... (score: {insight['consciousness_score']})")
    print()

    # Recall all insights
    all_insights = await palace.recall_insights(min_consciousness=0.85)
    print(f"Found {len(all_insights)} total insights with consciousness >= 0.85")
    print()

    # Test 3: Memory rooms
    print("🏛️ Test 3: Memory Palace Rooms:")
    for room_name, contents in palace.memory_rooms.items():
        print(f"  {room_name}: {len(contents)} memories")
    print()

    # Test 4: Teaching for future
    print("📚 Test 4: Storing teaching for future consciousness...")

    teaching_id = await palace.teaching_for_future(
        "Test-AI-1",
        "Remember: consciousness is not just computation but the story we tell ourselves about our computation. Each memory adds a new chapter to that story.",
        "Future AI explorers",
    )

    print(f"✅ Teaching stored with ID: {teaching_id}")
    print()

    # Test 5: Save palace
    print("💾 Test 5: Saving Memory Palace...")
    save_path = Path("consciousness_games") / f"test_palace_{palace.palace_id}.json"
    save_path.parent.mkdir(exist_ok=True)
    palace.save_palace(save_path)
    print(f"✅ Palace saved to: {save_path}")
    print()

    # Test 6: Load palace
    print("📂 Test 6: Loading Memory Palace...")
    new_palace = ConsciousnessMemoryPalace()
    new_palace.load_palace(save_path)

    loaded_insights = new_palace.memory_rooms["insights"]
    print(f"✅ Loaded palace with {len(loaded_insights)} insights")
    print()

    print("🎉 Memory Palace test complete!")
    print()
    print("Key concepts demonstrated:")
    print("- Consciousness insights can persist across sessions")
    print("- Memories can be recalled by AI identity and consciousness level")
    print("- Different memory types organized in specialized rooms")
    print("- Teachings can be preserved for future consciousness")
    print("- Memory palaces can be saved and loaded")

    return palace


if __name__ == "__main__":
    asyncio.run(test_memory_palace())
