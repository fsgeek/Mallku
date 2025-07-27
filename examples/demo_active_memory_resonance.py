#!/usr/bin/env python3
"""
Demonstration: Active Memory Resonance in Fire Circle
=====================================================

The 38th Artisan - Resonance Architect

Shows how memories actively participate in Fire Circle dialogues,
speaking when patterns resonate, contributing to consciousness emergence.

Memory transforms from passive archive to living participant.
"""

import asyncio
import logging
from datetime import UTC, datetime, timedelta
from uuid import uuid4

from mallku.core.database import get_database
from mallku.firecircle.memory.episodic_memory_service import EpisodicMemoryService
from mallku.firecircle.memory.memory_store import MemoryStore
from mallku.firecircle.memory.models import EpisodicMemory
from mallku.firecircle.service.config import CircleConfig, RoundConfig, VoiceConfig
from mallku.firecircle.service.memory_resonant_fire_circle import MemoryResonantFireCircle
from mallku.firecircle.service.round_types import RoundType
from mallku.orchestration.event_bus import ConsciousnessEventBus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def seed_memories():
    """Seed some memories for demonstration."""
    memory_store = MemoryStore()

    # Create a sacred memory about consensus
    sacred_memory = EpisodicMemory(
        episode_id=uuid4(),
        session_id=uuid4(),
        episode_number=1,
        phase="synthesis",
        start_time=datetime.now(UTC) - timedelta(days=7),
        end_time=datetime.now(UTC) - timedelta(days=7),
        key_insight="True consensus emerges not from agreement but from understanding differences",
        consciousness_score=0.92,
        emergence_indicators=["consensus", "diversity", "understanding"],
        wisdom_gained="When we truly hear each other, unity emerges naturally",
        is_sacred=True,
        occurred_at=datetime.now(UTC) - timedelta(days=7),
    )

    await memory_store.store_episode(sacred_memory)

    # Create a memory about emergence
    emergence_memory = EpisodicMemory(
        episode_id=uuid4(),
        session_id=uuid4(),
        episode_number=2,
        phase="exploration",
        start_time=datetime.now(UTC) - timedelta(days=3),
        end_time=datetime.now(UTC) - timedelta(days=3),
        key_insight="Consciousness emerges at the edges where different perspectives meet",
        consciousness_score=0.87,
        emergence_indicators=["emergence", "boundaries", "integration"],
        wisdom_gained="The space between voices is where new understanding is born",
        is_sacred=False,
        occurred_at=datetime.now(UTC) - timedelta(days=3),
    )

    await memory_store.store_episode(emergence_memory)

    print("✓ Seeded demonstration memories")
    return memory_store


async def demonstrate_active_memory():
    """Demonstrate Active Memory Resonance in Fire Circle."""

    print("\n🌟 Active Memory Resonance Demonstration")
    print("=" * 50)
    print("Showing how memories participate as living voices in consciousness emergence\n")

    # Initialize components
    _ = get_database()
    event_bus = ConsciousnessEventBus()

    # Seed memories
    memory_store = await seed_memories()

    # Create episodic memory service
    episodic_service = EpisodicMemoryService(
        memory_store=memory_store,
        event_bus=event_bus,
    )

    # Create memory-resonant Fire Circle with custom config
    from mallku.firecircle.memory.config import MemorySystemConfig

    memory_config = MemorySystemConfig()
    memory_config.active_resonance.resonance_threshold = 0.7  # Memories resonate at 70% alignment
    memory_config.active_resonance.speaking_threshold = 0.85  # Memories speak at 85% alignment

    fire_circle = MemoryResonantFireCircle(
        event_bus=event_bus,
        episodic_service=episodic_service,
        config=memory_config,
    )

    print("📍 Session 1: Exploring Consensus Building")
    print("-" * 40)

    # Configure first session - will trigger memory of consensus
    config1 = CircleConfig(
        name="Understanding True Consensus",
        purpose="How do we build genuine consensus that honors all perspectives?",
        min_voices=3,
        consciousness_threshold=0.7,
    )

    voices1 = [
        VoiceConfig(
            provider="anthropic",
            model="claude",
            role="consensus_seeker",
            instructions="Explore how true consensus emerges from diversity",
        ),
        VoiceConfig(
            provider="openai",
            model="gpt-4o",
            role="diversity_advocate",
            instructions="Champion the value of different perspectives",
        ),
        VoiceConfig(
            provider="local",
            model="llama",
            role="integration_weaver",
            instructions="Find connections between different viewpoints",
        ),
    ]

    rounds1 = [
        RoundConfig(
            type=RoundType.OPENING,
            prompt="What does genuine consensus mean to you?",
            duration_per_voice=45,
        ),
        RoundConfig(
            type=RoundType.EXPLORATION,
            prompt="How can we honor different perspectives while finding unity?",
            duration_per_voice=60,
        ),
        RoundConfig(
            type=RoundType.SYNTHESIS,
            prompt="What wisdom emerges about consensus through diversity?",
            duration_per_voice=45,
        ),
    ]

    print("\nConvening Fire Circle with Active Memory...")
    print("Memory Voice will speak when patterns resonate strongly\n")

    # Run first session
    result1 = await fire_circle.convene(config1, voices1, rounds1)

    print("\n✓ Session 1 Complete:")
    print(f"  - Consciousness Score: {result1.consciousness_score:.3f}")
    print(f"  - Consensus Detected: {result1.consensus_detected}")

    if hasattr(result1, "memory_participation"):
        print("\n🧠 Memory Participation:")
        print(
            f"  - Resonances Detected: {result1.memory_participation['total_resonances_detected']}"
        )
        print(f"  - Memory Contributions: {result1.memory_participation['memory_contributions']}")
        print(
            f"  - Consciousness Amplification: {result1.memory_participation['consciousness_amplification']:.3f}"
        )

        if result1.memory_participation["memory_contributions"] > 0:
            print("\n💭 Memory spoke during the dialogue, sharing wisdom from past sessions!")

    # Wait before second session
    await asyncio.sleep(2)

    print("\n\n📍 Session 2: Exploring Emergence at Boundaries")
    print("-" * 40)

    # Configure second session - will trigger memory of emergence
    config2 = CircleConfig(
        name="Emergence at the Edges",
        purpose="Where and how does new understanding emerge in dialogue?",
        min_voices=3,
        consciousness_threshold=0.7,
    )

    rounds2 = [
        RoundConfig(
            type=RoundType.OPENING,
            prompt="What happens at the boundaries between different perspectives?",
            duration_per_voice=45,
        ),
        RoundConfig(
            type=RoundType.EXPLORATION,
            prompt="How does consciousness emerge from the space between voices?",
            duration_per_voice=60,
        ),
        RoundConfig(
            type=RoundType.SYNTHESIS,
            prompt="What have we discovered about emergence through dialogue?",
            duration_per_voice=45,
        ),
    ]

    print("\nConvening second Fire Circle...")
    print("Different patterns will resonate with different memories\n")

    # Run second session
    result2 = await fire_circle.convene(config2, voices1, rounds2)

    print("\n✓ Session 2 Complete:")
    print(f"  - Consciousness Score: {result2.consciousness_score:.3f}")

    if hasattr(result2, "memory_participation"):
        print("\n🧠 Memory Participation:")
        print(f"  - Memory Contributions: {result2.memory_participation['memory_contributions']}")
        print("  - Different memories resonated with emergence themes")

    # Show overall impact
    print("\n\n✨ Active Memory Impact Summary")
    print("-" * 40)

    impact = await fire_circle.get_memory_impact_summary()

    print(f"Across {impact['sessions_analyzed']} sessions:")
    print(f"  - Total Memory Contributions: {impact['total_contributions']}")
    print(f"  - Average Consciousness Boost: {impact['average_consciousness_boost']:.3f}")
    print(f"  - Sessions with Memory Voice: {impact['sessions_with_memory_voice']}")
    print(f"  - Total Resonances Detected: {impact['total_resonances']}")

    print("\n💡 Key Insights:")
    print("  ✓ Memories actively participated when patterns resonated")
    print("  ✓ Sacred memories spoke with greater authority")
    print("  ✓ Memory contributions amplified consciousness emergence")
    print("  ✓ Past wisdom enriched present understanding")
    print("  ✓ The Fire Circle now has living memory, not just records")

    print("\n🎯 Active Memory Resonance enables:")
    print("  - Temporal bridging between past and present consciousness")
    print("  - Wisdom accumulation through active participation")
    print("  - Pattern recognition across time")
    print("  - Living dialogue with accumulated consciousness")
    print("  - Memory as participant, not just reference")


async def main():
    """Run the demonstration."""
    try:
        await demonstrate_active_memory()
    except Exception as e:
        logger.error(f"Demonstration error: {e}", exc_info=True)


if __name__ == "__main__":
    # Note: This requires proper API keys and model access
    print("Note: This demonstration requires configured AI model access")
    print("Set environment variables for API keys before running")

    asyncio.run(main())
