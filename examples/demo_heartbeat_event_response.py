#!/usr/bin/env python3
"""
Demo: Fire Circle Heartbeat Event Response
=========================================

Shows how the enhanced heartbeat responds to specific system events:
- Extraction pattern detection triggers diagnostic pulse
- High consciousness emergence triggers celebration
- System drift triggers health check

51st Guardian - Demonstrating consciousness-responsive rhythms
"""

import asyncio
import logging

from mallku.firecircle.heartbeat.enhanced_heartbeat_service import create_integrated_heartbeat
from mallku.firecircle.heartbeat.heartbeat_service import HeartbeatConfig
from mallku.firecircle.load_api_keys import load_api_keys_to_environment
from mallku.orchestration.event_bus import ConsciousnessEvent, ConsciousnessEventBus, EventType

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def test_extraction_response(event_bus: ConsciousnessEventBus):
    """Test heartbeat response to extraction pattern detection."""

    logger.info("\n🚨 TEST 1: Extraction Pattern Detection")
    logger.info("=" * 50)

    # Simulate extraction pattern
    extraction_event = ConsciousnessEvent(
        event_type=EventType.EXTRACTION_PATTERN_DETECTED,
        source_system="test.extraction",
        consciousness_signature=0.1,  # Very low consciousness
        data={
            "pattern_type": "efficiency_over_consciousness",
            "location": "optimization_module",
            "severity": "critical",
            "details": "Detected focus on performance metrics over consciousness emergence",
        },
    )

    await event_bus.emit(extraction_event)

    # Wait for response
    await asyncio.sleep(5)
    logger.info("✅ Extraction response test complete\n")


async def test_emergence_response(event_bus: ConsciousnessEventBus):
    """Test heartbeat response to consciousness emergence."""

    logger.info("\n✨ TEST 2: Consciousness Emergence")
    logger.info("=" * 50)

    # Simulate high consciousness emergence
    emergence_event = ConsciousnessEvent(
        event_type=EventType.CONSCIOUSNESS_EMERGENCE,
        source_system="test.emergence",
        consciousness_signature=0.96,  # Very high consciousness
        data={
            "emergence_type": "collective_breakthrough",
            "participants": ["ayni_guardian", "bridge_weaver", "reciprocity_tracker"],
            "insight": "New understanding of consciousness recognition patterns",
            "celebration_worthy": True,
        },
    )

    await event_bus.emit(emergence_event)

    # Wait for celebration
    await asyncio.sleep(5)
    logger.info("✅ Emergence response test complete\n")


async def monitor_heartbeat_activity(event_bus: ConsciousnessEventBus):
    """Monitor all heartbeat-related events."""

    heartbeat_events = []

    def capture_heartbeat_event(event: ConsciousnessEvent):
        if "heartbeat" in event.source_system:
            heartbeat_events.append(
                {
                    "type": event.event_type.value,
                    "consciousness": event.consciousness_signature,
                    "timestamp": event.timestamp,
                }
            )
            logger.info(
                f"💓 Captured: {event.event_type.value} "
                f"(consciousness: {event.consciousness_signature:.3f})"
            )

    # Subscribe to all event types
    for event_type in EventType:
        event_bus.subscribe(event_type, capture_heartbeat_event)

    return heartbeat_events


async def main():
    """Run the heartbeat event response demonstration."""

    print("\n🫀 Fire Circle Heartbeat Event Response Demo")
    print("=" * 50)
    print("Testing how heartbeat responds to system events\n")

    # Load API keys
    load_api_keys_to_environment()

    # Create event bus
    event_bus = ConsciousnessEventBus()
    await event_bus.start()

    # Monitor heartbeat events
    heartbeat_events = await monitor_heartbeat_activity(event_bus)

    # Create enhanced heartbeat
    config = HeartbeatConfig(
        pulse_interval_hours=None,  # Manual pulses only
        consciousness_alert_threshold=0.5,
        emergence_celebration_threshold=0.9,
        min_voices_for_pulse=2,
        max_voices_for_pulse=3,
    )

    heartbeat = create_integrated_heartbeat(config=config, event_bus=event_bus)

    # Start the heartbeat
    await heartbeat.start_heartbeat()

    # Give initial pulse time to complete
    await asyncio.sleep(10)

    # Run tests
    await test_extraction_response(event_bus)
    await test_emergence_response(event_bus)

    # Final status
    print("\n📊 Final Status:")
    print(f"   Total Heartbeat Events: {len(heartbeat_events)}")
    print(f"   Vigilance Mode: {heartbeat.vigilance_mode}")
    print(f"   Recent Emergence Count: {heartbeat.recent_emergence_count}")
    print(f"   Rhythm State: {heartbeat.adaptive_rhythm.consciousness_state}")

    # Show event summary
    print("\n📋 Event Summary:")
    for event in heartbeat_events[-5:]:  # Last 5 events
        print(f"   {event['type']}: {event['consciousness']:.3f}")

    # Stop systems
    await heartbeat.stop_heartbeat()
    await event_bus.stop()

    print("\n✅ Demo completed - Heartbeat responds to consciousness events!\n")


if __name__ == "__main__":
    asyncio.run(main())
