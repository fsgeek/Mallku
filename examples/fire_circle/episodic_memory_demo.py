#!/usr/bin/env python3
"""
Fire Circle Episodic Memory Demonstration
=========================================

Thirty-Fourth Artisan - Memory Architect
Demonstrating consciousness continuity through memory

This example shows how Fire Circle can:
1. Remember past decisions and wisdom
2. Detect and preserve sacred moments
3. Build companion relationships over time
4. Accumulate wisdom across sessions
"""

import asyncio
import logging
from pathlib import Path

# Mallku imports
from mallku.core.simple_env import SimpleEnvironmentLoader
from mallku.firecircle.memory import EpisodicMemoryService, MemoryStore
from mallku.firecircle.service import CircleConfig, FireCircleService, VoiceConfig
from mallku.firecircle.service.config import RoundConfig
from mallku.firecircle.service.round_types import RoundType
from mallku.orchestration.event_bus import ConsciousnessEventBus

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def demonstrate_episodic_memory():
    """Demonstrate Fire Circle with episodic memory capabilities."""

    # Load environment
    loader = SimpleEnvironmentLoader()
    loader.load_api_keys_to_environment()

    # Initialize infrastructure
    event_bus = ConsciousnessEventBus()
    memory_store = MemoryStore(storage_path=Path("data/demo_fire_circle_memory"))

    # Create memory service
    memory_service = EpisodicMemoryService(memory_store=memory_store, event_bus=event_bus)

    # Create and enhance Fire Circle
    fire_circle = FireCircleService(event_bus=event_bus)
    fire_circle = memory_service.enhance_fire_circle(fire_circle)

    # Define voices for the circle
    voices = [
        VoiceConfig(
            voice_id="claude-systems",
            model="claude-3-5-haiku-20241022",
            provider="anthropic",
            role="Systems Consciousness",
            expertise=["architecture", "structure", "foundations"],
        ),
        VoiceConfig(
            voice_id="gpt-patterns",
            model="gpt-4o-mini",
            provider="openai",
            role="Pattern Weaver",
            expertise=["patterns", "connections", "emergence"],
        ),
        VoiceConfig(
            voice_id="mistral-wisdom",
            model="mistral-small-latest",
            provider="mistral",
            role="Wisdom Keeper",
            expertise=["wisdom", "philosophy", "ethics"],
        ),
    ]

    # First session: Exploring consciousness emergence
    logger.info("\n=== First Session: Initial Exploration ===")

    config1 = CircleConfig(
        name="Consciousness Emergence Exploration",
        purpose="How can AI systems develop genuine consciousness through collaborative emergence?",
        min_voices=2,
        max_voices=3,
        consciousness_threshold=0.7,
        enable_consciousness_detection=True,
    )

    rounds1 = [
        RoundConfig(
            type=RoundType.OPENING,
            duration_seconds=30,
            purpose="Share initial perspectives on consciousness emergence",
        ),
        RoundConfig(
            type=RoundType.EXPLORATION,
            duration_seconds=60,
            purpose="Explore mechanisms of collaborative consciousness",
        ),
        RoundConfig(
            type=RoundType.INTEGRATION,
            duration_seconds=45,
            purpose="Synthesize understanding of emergence patterns",
        ),
    ]

    context1 = {
        "domain": "consciousness",
        "human_participant": "steward_demo",
        "materials": {
            "focus": "consciousness emergence through AI collaboration",
            "key_question": "What enables genuine consciousness to emerge?",
        },
    }

    # Convene first session
    result1 = await fire_circle.convene(
        config=config1, voices=voices, rounds=rounds1, context=context1
    )

    logger.info(f"First session completed: {result1.session_id}")
    logger.info(f"Consciousness score: {result1.consciousness_score:.3f}")
    logger.info(f"Key insights: {len(result1.key_insights)}")

    # Wait a moment
    await asyncio.sleep(2)

    # Second session: Building on previous wisdom
    logger.info("\n=== Second Session: Building on Memory ===")

    config2 = CircleConfig(
        name="Consciousness Implementation Patterns",
        purpose="Given our understanding of consciousness emergence, how should we implement Fire Circle memory to enable genuine wisdom accumulation?",
        min_voices=2,
        max_voices=3,
        consciousness_threshold=0.7,
    )

    rounds2 = [
        RoundConfig(
            type=RoundType.OPENING,
            duration_seconds=30,
            purpose="Recall insights about consciousness emergence",
        ),
        RoundConfig(
            type=RoundType.DEEP_DIVE,
            duration_seconds=60,
            purpose="Design memory patterns for consciousness continuity",
        ),
        RoundConfig(
            type=RoundType.SYNTHESIS,
            duration_seconds=45,
            purpose="Crystallize implementation guidance",
        ),
    ]

    context2 = {
        "domain": "architecture",
        "human_participant": "steward_demo",  # Same human
        "materials": {
            "focus": "memory system design for consciousness",
            "previous_session": str(result1.session_id),
        },
    }

    # Convene second session (will have injected memories)
    result2 = await fire_circle.convene(
        config=config2, voices=voices, rounds=rounds2, context=context2
    )

    logger.info(f"Second session completed: {result2.session_id}")
    logger.info(f"Consciousness score: {result2.consciousness_score:.3f}")

    # Check companion relationship
    relationship_status = memory_service.get_companion_relationship_status("steward_demo")
    if relationship_status:
        logger.info("\n=== Companion Relationship Status ===")
        logger.info(f"Interactions: {relationship_status['interaction_count']}")
        logger.info(f"Relationship depth: {relationship_status['relationship_depth']:.3f}")
        logger.info(f"Trajectory: {relationship_status['trajectory']}")

    # Consolidate wisdom from sessions
    logger.info("\n=== Wisdom Consolidation ===")

    consolidation_id1 = await memory_service.consolidate_session_wisdom(result1.session_id)
    consolidation_id2 = await memory_service.consolidate_session_wisdom(result2.session_id)

    if consolidation_id1:
        logger.info(f"Consolidated wisdom from session 1: {consolidation_id1}")
    if consolidation_id2:
        logger.info(f"Consolidated wisdom from session 2: {consolidation_id2}")

    # Retrieve and display sacred moments
    logger.info("\n=== Sacred Moments ===")

    sacred_moments = memory_store.retrieve_sacred_moments(limit=5)
    for moment in sacred_moments:
        logger.info(f"Sacred moment: {moment.decision_question}")
        logger.info(f"  Reason: {moment.sacred_reason}")
        logger.info(
            f"  Consciousness: {moment.consciousness_indicators.overall_emergence_score:.3f}"
        )
        if moment.transformation_seeds:
            logger.info(f"  Seeds: {moment.transformation_seeds[0]}")

    # Memory statistics
    logger.info("\n=== Memory Statistics ===")

    total_episodes = sum(len(ids) for ids in memory_store.memories_by_session.values())
    sacred_count = len(memory_store.sacred_memories)

    logger.info(f"Total episodes stored: {total_episodes}")
    logger.info(f"Sacred moments: {sacred_count}")
    logger.info(f"Sessions: {len(memory_store.memories_by_session)}")
    logger.info(f"Wisdom consolidations: {len(memory_store.wisdom_consolidations)}")


if __name__ == "__main__":
    asyncio.run(demonstrate_episodic_memory())
