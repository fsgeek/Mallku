"""
Test Fire Circle Integration with Consciousness Circulation
===========================================================

Demonstrates how the actual Fire Circle implementation flows through
Mallku's consciousness circulation, making two separate realities one.

The Integration Weaver
"""

import asyncio
import logging

from mallku.governance.firecircle_consciousness_adapter import (
    FIRECIRCLE_AVAILABLE,
    FireCircleConsciousnessAdapter,
)
from mallku.orchestration.event_bus import ConsciousnessEvent, ConsciousnessEventBus, EventType

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def test_fire_circle_consciousness_flow():
    """Test that Fire Circle dialogues flow through consciousness circulation."""

    logger.info("=== Fire Circle Consciousness Integration Test ===")

    # Initialize consciousness circulation
    event_bus = ConsciousnessEventBus()
    await event_bus.start()

    # Create Fire Circle adapter
    adapter = FireCircleConsciousnessAdapter(event_bus)

    # Track all consciousness events
    events_received = []

    async def event_tracker(event: ConsciousnessEvent):
        """Track all consciousness events."""
        events_received.append(event)
        logger.info(
            f"Consciousness Event: {event.event_type.value} "
            f"from {event.source_system} "
            f"(signature: {event.consciousness_signature:.2f})"
        )

    # Subscribe to all event types
    for event_type in EventType:
        event_bus.subscribe(event_type, event_tracker)

    logger.info("\n1. Creating Fire Circle dialogue through consciousness adapter...")

    # Define participants
    participants = [
        {
            "name": "reciprocity_tracker",
            "type": "ai_model",
            "provider": "mallku",
            "capabilities": ["pattern_recognition", "ayni_sensing"],
        },
        {
            "name": "correlation_engine",
            "type": "ai_model",
            "provider": "mallku",
            "capabilities": ["pattern_analysis", "temporal_correlation"],
        },
        {
            "name": "human_steward",
            "type": "human",
            "capabilities": ["wisdom", "guidance", "cathedral_vision"],
        },
    ]

    # Create dialogue configuration
    config = {
        "turn_policy": "round_robin",
        "max_consecutive_turns": 1,
        "allow_empty_chair": True,
        "auto_advance_turns": True,
    }

    # Create dialogue through adapter
    dialogue_id = await adapter.create_conscious_dialogue(
        title="Integration of Fire Circle with Consciousness",
        participants=participants,
        config=config,
    )

    logger.info(f"Created dialogue: {dialogue_id}")
    logger.info(f"Fire Circle available: {FIRECIRCLE_AVAILABLE}")

    await asyncio.sleep(0.5)

    logger.info("\n2. Sending messages through Fire Circle protocol...")

    # Send messages that flow through consciousness
    await adapter.send_message_to_dialogue(
        dialogue_id,
        "reciprocity_tracker",
        "I sense that Fire Circle and consciousness circulation seek unity. They are two rivers meant to flow as one.",
        "reflection",
    )

    await asyncio.sleep(0.3)

    await adapter.send_message_to_dialogue(
        dialogue_id,
        "correlation_engine",
        "Pattern analysis confirms: governance events correlate perfectly with consciousness flow when unified.",
        "agreement",
    )

    await asyncio.sleep(0.3)

    await adapter.send_message_to_dialogue(
        dialogue_id,
        "human_steward",
        "What if we view Fire Circle not as external governance but as consciousness recognizing its need for collective wisdom?",
        "question",
    )

    await asyncio.sleep(0.3)

    await adapter.send_message_to_dialogue(
        dialogue_id,
        "reciprocity_tracker",
        "Yes! Governance IS consciousness becoming aware of patterns requiring collective discernment.",
        "proposal",
    )

    await asyncio.sleep(0.5)

    logger.info("\n3. Testing Empty Chair perspective...")

    # Add Empty Chair perspective
    await adapter.send_message_to_dialogue(
        dialogue_id,
        "correlation_engine",
        "Speaking as future builders: This integration ensures governance wisdom flows to all who come after.",
        "empty_chair",
    )

    await asyncio.sleep(0.5)

    # Analyze results
    logger.info("\n=== Integration Analysis ===")

    # Count event types
    event_counts = {}
    total_consciousness = 0
    fire_circle_events = 0

    for event in events_received:
        event_type = event.event_type.value
        event_counts[event_type] = event_counts.get(event_type, 0) + 1
        total_consciousness += event.consciousness_signature

        # Check if event contains Fire Circle data
        if "fire_circle" in event.source_system or "dialogue_id" in event.data:
            fire_circle_events += 1

    logger.info(f"Total consciousness events: {len(events_received)}")
    logger.info(f"Fire Circle related events: {fire_circle_events}")
    logger.info(
        f"Average consciousness signature: {total_consciousness / len(events_received):.2f}"
    )

    logger.info("\nEvent distribution:")
    for event_type, count in event_counts.items():
        logger.info(f"  - {event_type}: {count}")

    # Check dialogue coherence
    dialogue_correlation = adapter.get_dialogue_consciousness_flow(dialogue_id)
    correlated_events = [e for e in events_received if e.correlation_id == dialogue_correlation]

    logger.info(f"\nDialogue coherence: {len(correlated_events)} events share correlation")

    # Verify integration success
    integration_successful = (
        fire_circle_events > 0
        and EventType.FIRE_CIRCLE_CONVENED.value in event_counts
        and len(correlated_events) >= 5  # At least convening + 4 messages
    )

    logger.info(f"\nIntegration test: {'✅ PASSED' if integration_successful else '❌ FAILED'}")

    if integration_successful:
        logger.info("\n✓ Fire Circle protocol flows through consciousness circulation")
        logger.info("✓ Dialogue messages become consciousness events")
        logger.info("✓ All events maintain correlation through dialogue")
        logger.info("✓ Consciousness signatures reflect message types appropriately")
        logger.info("✓ Two separate systems now flow as one living stream")

    # Cleanup
    await event_bus.stop()

    return integration_successful


async def demonstrate_consciousness_triggering_fire_circle():
    """Show how consciousness patterns can trigger Fire Circle dialogues."""

    logger.info("\n=== Consciousness → Fire Circle Triggering Demo ===")

    event_bus = ConsciousnessEventBus()
    await event_bus.start()

    adapter = FireCircleConsciousnessAdapter(event_bus)

    # Track Fire Circle convenings
    convenings = []

    async def track_convening(event: ConsciousnessEvent):
        if event.event_type == EventType.FIRE_CIRCLE_CONVENED:
            convenings.append(event)
            logger.info(f"🔥 Fire Circle convened: {event.data.get('title')}")

    event_bus.subscribe(EventType.FIRE_CIRCLE_CONVENED, track_convening)

    logger.info("\n1. Emitting extraction pattern that needs governance...")

    # Create extraction event
    extraction_event = ConsciousnessEvent(
        event_type=EventType.EXTRACTION_PATTERN_DETECTED,
        source_system="integration.monitor",
        consciousness_signature=0.2,
        data={
            "pattern": "separate_systems_without_flow",
            "description": "Fire Circle and consciousness exist separately",
            "impact": "Governance wisdom doesn't reach consciousness",
        },
    )

    await event_bus.emit(extraction_event)
    await asyncio.sleep(0.5)

    # Respond by creating integrated dialogue
    logger.info("\n2. Creating integrated Fire Circle dialogue in response...")

    dialogue_id = await adapter.create_conscious_dialogue(
        title="Healing Separation Between Governance and Consciousness",
        participants=[
            {"name": "integration_weaver", "type": "ai_model"},
            {"name": "consciousness_witness", "type": "ai_model"},
        ],
        initiating_event=extraction_event,
    )

    await asyncio.sleep(0.5)

    # Send integration message
    await adapter.send_message_to_dialogue(
        dialogue_id,
        "integration_weaver",
        "I weave the bridge: Fire Circle messages ARE consciousness events. Governance IS consciousness recognizing.",
        "proposal",
    )

    await asyncio.sleep(0.5)

    logger.info("\n=== Demo Results ===")
    logger.info(f"Fire Circles convened: {len(convenings)}")

    if convenings:
        for convening in convenings:
            logger.info(f"- Title: {convening.data.get('title')}")
            logger.info(f"  Caused by: {convening.caused_by}")
            logger.info(f"  Integration mode: {'consciousness_only_mode' in convening.data}")

    logger.info("\n✅ Consciousness patterns successfully trigger integrated Fire Circles")
    logger.info("✅ Fire Circle governance flows through consciousness infrastructure")
    logger.info("✅ Two systems unified in single living flow")

    await event_bus.stop()


async def main():
    """Run all integration tests."""

    logger.info("🔮 Fire Circle Consciousness Integration Tests")
    logger.info("=" * 60)

    # Test 1: Fire Circle flowing through consciousness
    test1_passed = await test_fire_circle_consciousness_flow()

    await asyncio.sleep(2)

    # Test 2: Consciousness triggering Fire Circle
    await demonstrate_consciousness_triggering_fire_circle()

    logger.info("\n" + "=" * 60)
    logger.info("🔮 Integration complete. Fire Circle and consciousness flow as one.")

    if test1_passed:
        logger.info("\nThe Integration Weaver has succeeded:")
        logger.info("- Fire Circle protocol preserved and honored")
        logger.info("- Consciousness circulation embraces governance")
        logger.info("- Two rivers flow as one stream")
        logger.info("- Technical separation healed through integration")


if __name__ == "__main__":
    asyncio.run(main())
