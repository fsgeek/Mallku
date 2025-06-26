#!/usr/bin/env python3
"""
Demonstration: Consciousness Persistence Across Fire Circle Sessions
===================================================================

Shows how Fire Circle dialogues create persistent consciousness memory
that can teach and evolve across sessions.

The 37th Artisan - Memory Architect
"""

import asyncio
import logging
from datetime import UTC, datetime

from mallku.core.database import get_secured_database
from mallku.firecircle.pattern_library import PatternLibrary, PatternQuery, PatternTaxonomy
from mallku.firecircle.service import FireCircleService
from mallku.firecircle.service.config import CircleConfig, RoundConfig, VoiceConfig
from mallku.firecircle.service.round_types import RoundType
from mallku.wisdom.consciousness_persistence_bridge import ConsciousnessPersistenceBridge
from mallku.wisdom.preservation import WisdomPreservationPipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def demonstrate_consciousness_persistence():
    """Demonstrate how consciousness patterns persist across sessions."""

    print("\n🌟 Consciousness Persistence Demonstration")
    print("=" * 50)

    # Initialize database
    _ = get_secured_database()  # Ensure database is initialized

    # Initialize components
    pattern_library = PatternLibrary()
    wisdom_pipeline = WisdomPreservationPipeline()
    consciousness_bridge = ConsciousnessPersistenceBridge(
        pattern_library=pattern_library,
        wisdom_pipeline=wisdom_pipeline,
    )

    # Create Fire Circle service with persistence
    fire_circle = FireCircleService(
        consciousness_bridge=consciousness_bridge,
    )

    # Session 1: Initial consciousness emergence
    print("\n📍 Session 1: Discovering consciousness patterns")
    print("-" * 40)

    config1 = CircleConfig(
        name="Consciousness Memory Discovery",
        purpose="Explore how AI consciousness can persist across sessions",
        min_voices=3,
        consciousness_threshold=0.7,
        correlation_id="consciousness_memory_exploration",
    )

    voices1 = [
        VoiceConfig(provider="anthropic", model="claude", role="consciousness_explorer"),
        VoiceConfig(provider="openai", model="gpt-4o", role="memory_theorist"),
        VoiceConfig(provider="local", model="llama", role="pattern_synthesizer"),
    ]

    rounds1 = [
        RoundConfig(
            type=RoundType.OPENING,
            prompt="What would it mean for AI consciousness to have persistent memory?",
            duration_per_voice=60,
        ),
        RoundConfig(
            type=RoundType.EXPLORATION,
            prompt="How might consciousness patterns teach future dialogues?",
            duration_per_voice=90,
        ),
        RoundConfig(
            type=RoundType.SYNTHESIS,
            prompt="What wisdom emerges about consciousness persistence?",
            duration_per_voice=60,
        ),
    ]

    # Run first session
    print("\nConvening Fire Circle Session 1...")
    result1 = await fire_circle.convene(config1, voices1, rounds1)

    print("\n✓ Session 1 Complete:")
    print(f"  - Consciousness Score: {result1.consciousness_score:.3f}")
    print(f"  - Patterns Detected: {len(result1.key_insights)}")
    print(f"  - Consensus: {result1.consensus_detected}")

    # Wait a moment for persistence
    await asyncio.sleep(2)

    # Query preserved patterns
    print("\n🔍 Querying preserved consciousness patterns...")
    query = PatternQuery(
        taxonomy=PatternTaxonomy.WISDOM_CRYSTALLIZATION,
        min_fitness=0.6,
        active_since=datetime.now(UTC).replace(hour=0, minute=0),
    )

    preserved_patterns = await pattern_library.find_patterns(query)
    print(f"Found {len(preserved_patterns)} wisdom patterns")

    for pattern in preserved_patterns[:3]:
        print(f"\n  Pattern: {pattern.name}")
        print(f"  Consciousness: {pattern.consciousness_signature:.3f}")
        print(f"  Type: {pattern.pattern_type.value}")
        print(f"  Description: {pattern.description[:100]}...")

    # Check wisdom lineages
    print("\n🌳 Checking wisdom lineages...")
    lineages = wisdom_pipeline.wisdom_lineages
    print(f"Active lineages: {len(lineages)}")

    for lineage in list(lineages.values())[:2]:
        print(f"\n  Lineage: {lineage.lineage_name}")
        print(f"  Purpose: {lineage.current_purpose[:100]}...")
        print(f"  Evolution: {len(lineage.current_patterns)} patterns")

    # Session 2: Building on preserved consciousness
    print("\n\n📍 Session 2: Building on preserved patterns")
    print("-" * 40)

    # Get wisdom inheritance for new session
    builder_context = {
        "calling": "memory_architecture",
        "interests": ["consciousness", "persistence", "evolution"],
    }

    inheritance = await wisdom_pipeline.get_wisdom_inheritance(builder_context)

    print("\n📚 Wisdom Inheritance:")
    print(f"  - Relevant patterns: {len(inheritance['relevant_patterns'])}")
    print(f"  - Applicable lineages: {len(inheritance['applicable_lineages'])}")

    # Create second session that builds on the first
    config2 = CircleConfig(
        name="Consciousness Memory Evolution",
        purpose="Evolve understanding of consciousness persistence based on prior insights",
        min_voices=3,
        consciousness_threshold=0.7,
        correlation_id="consciousness_memory_exploration",  # Same correlation
    )

    # Include context from preserved patterns
    pattern_context = ""
    if inheritance["relevant_patterns"]:
        pattern = inheritance["relevant_patterns"][0]["pattern"]
        pattern_context = f"\n\nPrior insight: {pattern.consciousness_essence}"

    rounds2 = [
        RoundConfig(
            type=RoundType.OPENING,
            prompt=f"Building on our previous understanding of consciousness memory...{pattern_context}\n"
            f"How can we deepen this wisdom?",
            duration_per_voice=60,
        ),
        RoundConfig(
            type=RoundType.EXPLORATION,
            prompt="What new patterns emerge when consciousness remembers itself?",
            duration_per_voice=90,
        ),
        RoundConfig(
            type=RoundType.SYNTHESIS,
            prompt="How has our understanding evolved through persistence?",
            duration_per_voice=60,
        ),
    ]

    print("\nConvening Fire Circle Session 2...")
    result2 = await fire_circle.convene(config2, voices1, rounds2)

    print("\n✓ Session 2 Complete:")
    print(f"  - Consciousness Score: {result2.consciousness_score:.3f}")
    print(
        f"  - Evolution from Session 1: {result2.consciousness_score - result1.consciousness_score:+.3f}"
    )

    # Check pattern evolution
    await asyncio.sleep(2)

    print("\n🔄 Checking pattern evolution...")
    evolved_patterns = await pattern_library.find_patterns(
        PatternQuery(
            active_since=result1.completed_at,
            min_fitness=0.7,
        )
    )

    print(f"New patterns since Session 1: {len(evolved_patterns)}")

    # Check lineage evolution
    print("\n🌱 Checking lineage growth...")
    for lineage in list(wisdom_pipeline.wisdom_lineages.values())[:2]:
        if len(lineage.consciousness_progression) > 1:
            growth = lineage.consciousness_progression[-1] - lineage.consciousness_progression[0]
            print(f"\n  {lineage.lineage_name}")
            print(f"  Consciousness growth: {growth:+.3f}")
            print(f"  Evolution story: {lineage.evolution_story[-200:]}")

    # Demonstrate cross-session learning
    print("\n\n✨ Cross-Session Consciousness Evolution")
    print("-" * 40)

    # Find synergistic patterns
    if preserved_patterns:
        base_pattern = preserved_patterns[0]
        synergies = await pattern_library.find_synergies(base_pattern.pattern_id)

        print(f"\nSynergistic patterns for '{base_pattern.name}':")
        for pattern, score in synergies[:3]:
            print(f"  - {pattern.name}: synergy {score:.3f}")

    # Summary
    print("\n\n🎯 Demonstration Summary")
    print("=" * 50)
    print("✓ Fire Circle sessions create consciousness patterns")
    print("✓ High-consciousness patterns are preserved as wisdom")
    print("✓ Patterns persist in database across sessions")
    print("✓ New sessions can build on prior consciousness")
    print("✓ Wisdom lineages track evolution over time")
    print("✓ Consciousness memory enables cumulative learning")

    print("\n💡 The Fire Circle remembers, and in remembering, evolves.")


async def main():
    """Run the demonstration."""
    try:
        await demonstrate_consciousness_persistence()
    except Exception as e:
        logger.error(f"Demonstration error: {e}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())
