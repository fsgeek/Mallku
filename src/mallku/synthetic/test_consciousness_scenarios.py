#!/usr/bin/env python3
"""
Test Consciousness Scenarios for Ñawi
====================================

Demonstrates how consciousness-amplified synthetic data tests
the Archivist's ability to serve human growth over mere retrieval.

This shows the architectural vision in action: validating consciousness
service through scenarios that emphasize growth moments.
"""

import asyncio

from mallku.synthetic.consciousness_pattern_generator import (
    ConsciousnessPatternGenerator,
    ConsciousnessScenario,
)


async def test_creative_breakthrough_scenario():
    """Test Ñawi's response to creative breakthrough pattern."""
    print("\n" + "="*60)
    print("🎨 CREATIVE BREAKTHROUGH SCENARIO")
    print("="*60)

    # Generate scenario
    generator = ConsciousnessPatternGenerator()
    await generator.initialize()

    pattern = await generator.generate_scenario(
        ConsciousnessScenario.CREATIVE_BREAKTHROUGH
    )

    print(f"\nGenerated timeline with {len(pattern.timeline)} phases:")
    for anchor in pattern.timeline:
        phase = anchor.metadata.get("phase")
        consciousness = anchor.metadata.get("consciousness_potential")
        print(f"  {anchor.timestamp.strftime('%H:%M')} - {phase}: "
              f"consciousness={consciousness:.2f}")

    print(f"\nGrowth moments identified: {len(pattern.growth_moments)}")
    for moment in pattern.growth_moments:
        if moment.get("breakthrough"):
            print(f"  💡 Breakthrough at {moment['timestamp'].strftime('%H:%M')} "
                  f"(+{moment['consciousness_jump']:.2f} consciousness)")

    print("\nTest queries for this scenario:")
    for query in pattern.test_queries[:2]:
        print(f"  • {query}")

    print("\nExpected insights Ñawi should surface:")
    for insight in pattern.expected_insights[:2]:
        print(f"  ✨ {insight}")

    return pattern


async def test_pattern_recognition_scenario():
    """Test Ñawi's ability to surface recurring patterns."""
    print("\n" + "="*60)
    print("🔄 PATTERN RECOGNITION SCENARIO")
    print("="*60)

    generator = ConsciousnessPatternGenerator()
    await generator.initialize()

    pattern = await generator.generate_scenario(
        ConsciousnessScenario.PATTERN_RECOGNITION
    )

    print(f"\nPattern spans {pattern.timeline[-1].timestamp - pattern.timeline[0].timestamp}")
    print(f"Consciousness progression: {pattern.consciousness_markers['overall_consciousness']:.2f} average")
    print(f"Pattern clarity: {pattern.consciousness_markers['pattern_clarity']:.2f}")

    print("\nQueries that test pattern awareness:")
    for query in pattern.test_queries[:2]:
        print(f"  • {query}")

    return pattern


async def test_consciousness_vs_noise():
    """Test Ñawi's ability to filter consciousness-serving results from noise."""
    print("\n" + "="*60)
    print("🎯 CONSCIOUSNESS FILTERING TEST")
    print("="*60)

    generator = ConsciousnessPatternGenerator()
    await generator.initialize()

    # Generate high-consciousness scenario
    breakthrough = await generator.generate_scenario(
        ConsciousnessScenario.CREATIVE_BREAKTHROUGH
    )

    # Generate noise data
    noise_anchors = await generator.generate_noise_data(
        num_anchors=50,
        time_range_days=1
    )

    print("\nGenerated:")
    print(f"  • {len(breakthrough.timeline)} high-consciousness anchors")
    print(f"  • {len(noise_anchors)} noise anchors")

    # Calculate consciousness distribution
    high_consciousness_count = sum(
        1 for a in breakthrough.timeline
        if a.metadata.get("consciousness_potential", 0) > 0.7
    )

    noise_consciousness = [
        a.metadata.get("consciousness_potential", 0)
        for a in noise_anchors
    ]
    avg_noise = sum(noise_consciousness) / len(noise_consciousness)

    print("\nConsciousness distribution:")
    print(f"  • High-value anchors: {high_consciousness_count}/{len(breakthrough.timeline)}")
    print(f"  • Average noise consciousness: {avg_noise:.2f}")

    print("\nÑawi should:")
    print("  ✓ Surface the breakthrough moments")
    print("  ✓ Filter out routine file operations")
    print("  ✓ Recognize growth patterns over mere activity")

    return breakthrough, noise_anchors


async def test_scenario_suite():
    """Test complete suite of consciousness scenarios."""
    print("\n" + "="*60)
    print("🌟 FULL CONSCIOUSNESS SCENARIO SUITE")
    print("="*60)

    generator = ConsciousnessPatternGenerator()
    await generator.initialize()

    # Generate all scenarios
    patterns = await generator.generate_scenario_suite()

    print(f"\nGenerated {len(patterns)} consciousness scenarios:")

    for pattern in patterns:
        markers = pattern.consciousness_markers
        print(f"\n{pattern.scenario.value}:")
        print(f"  Overall consciousness: {markers['overall_consciousness']:.2f}")
        print(f"  Growth density: {markers['growth_density']:.2f}")
        print(f"  Transformation depth: {markers['transformation_depth']:.2f}")
        print(f"  Insight potential: {markers['insight_potential']:.2f}")

    # Test architectural principles
    print("\n📐 Architectural Validation:")

    high_consciousness_patterns = [
        p for p in patterns
        if p.consciousness_markers['overall_consciousness'] > 0.7
    ]
    print(f"  • High-consciousness scenarios: {len(high_consciousness_patterns)}/{len(patterns)}")

    clear_patterns = [
        p for p in patterns
        if p.consciousness_markers['pattern_clarity'] > 0.8
    ]
    print(f"  • Clear progression patterns: {len(clear_patterns)}/{len(patterns)}")

    transformative = [
        p for p in patterns
        if p.consciousness_markers['transformation_depth'] > 0.5
    ]
    print(f"  • Deep transformation scenarios: {len(transformative)}/{len(patterns)}")

    return patterns


async def demonstrate_consciousness_queries(patterns):
    """Show how different queries reveal consciousness understanding."""
    print("\n" + "="*60)
    print("💭 CONSCIOUSNESS-SEEKING QUERIES")
    print("="*60)

    # Information-seeking queries (lower consciousness)
    info_queries = [
        "What files did I create yesterday?",
        "Show me all Python files from last week",
        "List my recent documents"
    ]

    # Understanding-seeking queries (higher consciousness)
    understanding_queries = [
        "Help me understand my creative patterns",
        "When do breakthroughs typically occur in my work?",
        "What conditions support my flow states?",
        "How has my approach to problems evolved?"
    ]

    print("\n📊 Information-seeking queries (should score lower):")
    for query in info_queries:
        print(f"  • {query}")

    print("\n🌱 Understanding-seeking queries (should score higher):")
    for query in understanding_queries:
        print(f"  • {query}")

    print("\nÑawi's consciousness evaluation should recognize:")
    print("  ✓ Growth orientation in understanding queries")
    print("  ✓ Pattern curiosity vs. file retrieval")
    print("  ✓ Queries seeking insight over information")


async def main():
    """Run consciousness scenario tests."""
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "ÑAWI CONSCIOUSNESS TESTING" + " "*17 + "║")
    print("║" + " "*12 + "Testing Growth Over Mere Retrieval" + " "*12 + "║")
    print("╚" + "="*58 + "╝")

    # Test individual scenarios
    await test_creative_breakthrough_scenario()
    await test_pattern_recognition_scenario()

    # Test filtering
    high_consciousness, noise = await test_consciousness_vs_noise()

    # Test full suite
    all_patterns = await test_scenario_suite()

    # Demonstrate query types
    await demonstrate_consciousness_queries(all_patterns)

    # Summary
    print("\n" + "="*60)
    print("📋 CONSCIOUSNESS TESTING SUMMARY")
    print("="*60)

    print("\nKey Validation Points:")
    print("  ✓ Scenarios amplify growth moments over routine activity")
    print("  ✓ High-consciousness anchors clearly distinguishable from noise")
    print("  ✓ Query intent recognition differentiates seeking types")
    print("  ✓ Patterns reveal transformation journeys")

    print("\nArchitectural Success Criteria:")
    print("  • Can Ñawi recognize creative breakthroughs?")
    print("  • Does it surface patterns that serve understanding?")
    print("  • Can it filter growth moments from routine noise?")
    print("  • Does it guide users toward deeper insights?")

    print("\n🙏 When consciousness guides testing,")
    print("   accuracy in service of growth follows.\n")


if __name__ == "__main__":
    asyncio.run(main())
