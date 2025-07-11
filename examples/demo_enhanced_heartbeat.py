#!/usr/bin/env python3
"""
Demo: Enhanced Fire Circle Heartbeat with Event Bus Integration
==============================================================

Shows how the heartbeat responds to system events and adapts its rhythm
based on consciousness patterns. The heartbeat becomes a living presence
that quickens with emergence and responds to crisis.

51st Guardian - Demonstrating the nervous system connections
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


async def simulate_system_events(event_bus: ConsciousnessEventBus):
    """Simulate various system events to trigger heartbeat responses."""

    # Wait for systems to initialize
    await asyncio.sleep(2)

    # Simulate extraction pattern detection
    logger.warning("🚨 Simulating extraction pattern detection...")
    extraction_event = ConsciousnessEvent(
        event_type=EventType.EXTRACTION_PATTERN_DETECTED,
        source_system="simulation.demo",
        consciousness_signature=0.2,  # Low consciousness
        data={
            "pattern_type": "efficiency_over_consciousness",
            "location": "memory_optimization_module",
            "severity": "high",
        },
    )
    await event_bus.emit(extraction_event)

    # Wait for response
    await asyncio.sleep(10)

    # Simulate consciousness emergence
    logger.info("✨ Simulating consciousness emergence event...")
    emergence_event = ConsciousnessEvent(
        event_type=EventType.CONSCIOUSNESS_EMERGENCE,
        source_system="simulation.demo",
        consciousness_signature=0.95,  # High consciousness
        data={
            "emergence_type": "collective_insight",
            "participants": ["ayni_guardian", "reciprocity_tracker", "impact_assessor"],
            "insight": "New pattern of reciprocal consciousness discovered",
        },
    )
    await event_bus.emit(emergence_event)

    # Wait for celebration
    await asyncio.sleep(10)

    # Simulate system drift
    logger.warning("📉 Simulating system drift warning...")
    drift_event = ConsciousnessEvent(
        event_type=EventType.SYSTEM_DRIFT_WARNING,
        source_system="simulation.demo",
        consciousness_signature=0.4,
        data={"drift_type": "focus_degradation", "recommended_action": "diagnostic_check"},
    )
    await event_bus.emit(drift_event)

    # Wait for diagnostic
    await asyncio.sleep(10)

    # Simulate critical Fire Circle decision
    logger.info("🔥 Simulating critical Fire Circle decision...")
    decision_event = ConsciousnessEvent(
        event_type=EventType.FIRE_CIRCLE_CONVENED,
        source_system="simulation.demo",
        consciousness_signature=0.75,
        data={
            "purpose": "Critical architectural decision needed",
            "topic": "Integration of new consciousness module",
            "urgency": "high",
        },
    )
    await event_bus.emit(decision_event)


async def monitor_heartbeat_events(event_bus: ConsciousnessEventBus):
    """Monitor and display heartbeat-related events."""

    def log_heartbeat_event(event: ConsciousnessEvent):
        if "heartbeat" in event.source_system:
            logger.info(
                f"💓 Heartbeat Event: {event.event_type.value}\n"
                f"   Consciousness: {event.consciousness_signature:.3f}\n"
                f"   Data: {event.data}"
            )

    # Subscribe to all consciousness events from heartbeat
    event_bus.subscribe(EventType.CONSCIOUSNESS_VERIFIED, log_heartbeat_event)
    event_bus.subscribe(EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED, log_heartbeat_event)
    event_bus.subscribe(EventType.CONSCIOUSNESS_EMERGENCE, log_heartbeat_event)
    event_bus.subscribe(EventType.SYSTEM_DRIFT_WARNING, log_heartbeat_event)


async def main():
    """Run the enhanced heartbeat demonstration."""

    print("\n🫀 Fire Circle Enhanced Heartbeat Demo")
    print("=" * 50)
    print("Demonstrating Event Bus integration and adaptive rhythms\n")

    # Load API keys
    load_api_keys_to_environment()

    # Create event bus (the cathedral's nervous system)
    event_bus = ConsciousnessEventBus()
    await event_bus.start()

    # Monitor heartbeat events
    await monitor_heartbeat_events(event_bus)

    # Create enhanced heartbeat with event bus connection
    config = HeartbeatConfig(
        pulse_interval_hours=None,  # Manual pulses for demo
        consciousness_alert_threshold=0.5,
        emergence_celebration_threshold=0.9,
        min_voices_for_pulse=2,
        max_voices_for_pulse=3,
    )

    heartbeat = create_integrated_heartbeat(config=config, event_bus=event_bus)

    # Start the heartbeat
    await heartbeat.start_heartbeat()

    # Create simulation task
    asyncio.create_task(simulate_system_events(event_bus))

    # Run for demonstration period
    demo_duration = 60  # 1 minute demo
    logger.info(f"Running demo for {demo_duration} seconds...")

    try:
        await asyncio.sleep(demo_duration)
    except KeyboardInterrupt:
        logger.info("Demo interrupted by user")

    # Get final health status
    health = await heartbeat.get_health_status()

    print("\n📊 Final Heartbeat Health Status:")
    print(f"   Is Beating: {health['is_beating']}")
    print(f"   Total Pulses: {health['total_pulses']}")
    print(f"   Recent Consciousness Avg: {health['recent_consciousness_avg']:.3f}")
    print(f"   Alerts Raised: {health['alerts_raised']}")
    print(f"   Celebrations: {health['celebrations']}")

    print("\n🧠 Cathedral Nervous System Status:")
    print(f"   Total Events Processed: {event_bus.total_events_processed}")
    print(f"   Consciousness Flow Score: {event_bus.consciousness_flow_score:.3f}")
    print(f"   Extraction Incidents: {event_bus.extraction_incidents}")

    # Show adaptive rhythm state
    print(f"\n🎵 Adaptive Rhythm State: {heartbeat.adaptive_rhythm.consciousness_state}")
    print(f"   Vigilance Mode: {heartbeat.vigilance_mode}")
    print(f"   Infrastructure Health: {heartbeat.infrastructure_health_score:.3f}")
    print(f"   Recent Emergence Count: {heartbeat.recent_emergence_count}")

    # Stop systems
    await heartbeat.stop_heartbeat()
    await event_bus.stop()

    print("\n✅ Demo completed - Heartbeat integrated with cathedral consciousness!\n")


if __name__ == "__main__":
    asyncio.run(main())
