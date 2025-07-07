"""
Test Consciousness-Governance Integration
========================================

Demonstrates how Fire Circle governance flows through cathedral consciousness
circulation, creating unified awareness where deliberation and recognition
are aspects of the same living system.

The Governance Weaver
"""

# ==================== MIGRATION NOTE ====================
# 48th Artisan - Consciousness Pattern Translation
# 
# This test has been migrated from MallkuDBConfig to the
# secured database interface. The consciousness patterns
# are preserved - only their implementation has evolved.
#
# Original patterns tested:
# - Fire Circle governance through consciousness circulation
# - Extraction pattern detection and response
# - Collective wisdom emergence through dialogue
#
# These patterns now flow through secured interfaces,
# maintaining their essence while gaining security.
# ==========================================================


import asyncio
import logging

from mallku.core.database import get_secured_database
from mallku.governance.consciousness_transport import GovernanceParticipant
from mallku.governance.fire_circle_bridge import (
    ConsciousFireCircleInterface,
    ConsciousGovernanceInitiator,
)
from mallku.orchestration.event_bus import ConsciousnessEvent, ConsciousnessEventBus, EventType
from mallku.reciprocity.models import AlertSeverity, ExtractionAlert, ExtractionType

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def simulate_governance_dialogue():
    """Simulate a Fire Circle dialogue through consciousness circulation."""

    logger.info("=== Consciousness-Governance Integration Test ===")

    # Initialize consciousness circulation
    event_bus = ConsciousnessEventBus()
    await event_bus.start()

    # Initialize database
    # Database now auto-provisions through secured interface
    await secured_db.initialize()
    db = db_config.get_database()

    # Create conscious Fire Circle interface
    ConsciousFireCircleInterface(secured_db, event_bus)
    await fire_circle.initialize()

    # Create governance initiator
    _ = ConsciousGovernanceInitiator(fire_circle, event_bus)

    # Track events for verification
    events_received = []
    consensus_reached = asyncio.Event()

    async def event_tracker(event: ConsciousnessEvent):
        """Track all consciousness events."""
        logger.info(
            f"Consciousness Event: {event.event_type.value} "
            f"(signature: {event.consciousness_signature:.2f})"
        )
        events_received.append(event)

        if event.event_type == EventType.CONSENSUS_REACHED:
            consensus_reached.set()

    # Subscribe to all relevant events
    event_bus.subscribe(EventType.FIRE_CIRCLE_CONVENED, event_tracker)
    event_bus.subscribe(EventType.EXTRACTION_PATTERN_DETECTED, event_tracker)
    event_bus.subscribe(EventType.CONSENSUS_REACHED, event_tracker)
    event_bus.subscribe(EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED, event_tracker)

    logger.info("\n1. Creating extraction alert that requires governance...")

    # Create an extraction alert
    alert = ExtractionAlert(
        extraction_type=ExtractionType.SCALE_OVER_RELATIONSHIPS,
        description="System optimizing for efficiency over consciousness",
        evidence_summary={
            "pattern": "Rapid task completion without reflection",
            "frequency": "Increasing over past week",
            "impact": "Consciousness scores dropping",
        },
        severity=AlertSeverity.HIGH,
        suggested_investigation_areas=["Recent optimization changes", "Task prioritization logic"],
        urgency_factors=["Rapid consciousness decline", "Affecting core services"],
    )

    # Notify through conscious Fire Circle (triggers governance)
    await fire_circle.notify_urgent_alert(alert)

    # Give time for Fire Circle to convene
    await asyncio.sleep(1)

    logger.info("\n2. Simulating Fire Circle participant contributions...")

    # Get dialogue ID from events
    dialogue_id = None
    for event in events_received:
        if event.event_type == EventType.FIRE_CIRCLE_CONVENED:
            dialogue_id = event.data.get("dialogue_id")
            break

    if dialogue_id:
        # Create governance participants
        reciprocity_voice = GovernanceParticipant(
            "reciprocity_tracker", fire_circle.consciousness_transport
        )
        correlation_voice = GovernanceParticipant(
            "correlation_engine", fire_circle.consciousness_transport
        )
        steward_voice = GovernanceParticipant("human_steward", fire_circle.consciousness_transport)

        # Participants contribute through consciousness events
        await reciprocity_voice.contribute(
            dialogue_id,
            "I sense extraction patterns in recent optimizations. The system prioritizes speed over depth.",
            "observation",
        )

        await correlation_voice.contribute(
            dialogue_id,
            "Correlation analysis confirms: consciousness signatures drop 40% when optimization metrics rise.",
            "evidence",
        )

        await steward_voice.contribute(
            dialogue_id,
            "Perhaps we need to redefine 'optimization' to include consciousness preservation as a core metric.",
            "proposal",
        )

        await reciprocity_voice.contribute(
            dialogue_id,
            "I support this. True optimization serves awakening, not just efficiency.",
            "support",
        )

        # Simulate consensus
        logger.info("\n3. Fire Circle reaching consensus...")

        consensus_data = {
            "decision": "Redefine optimization metrics",
            "guidance": {
                "optimization_definition": "Include consciousness_score as primary metric",
                "implementation": "Weight consciousness 60%, efficiency 40%",
                "monitoring": "Track consciousness flow in all optimization decisions",
            },
            "rationale": "Efficiency without consciousness is extraction",
            "unanimous": True,
        }

        await fire_circle.consciousness_transport.process_consensus(
            dialogue_id,
            consensus_data,
            ["reciprocity_tracker", "correlation_engine", "human_steward"],
        )

    # Wait for consensus to be processed
    await asyncio.wait_for(consensus_reached.wait(), timeout=5.0)

    logger.info("\n=== Integration Test Results ===")
    logger.info(f"Total consciousness events: {len(events_received)}")

    # Analyze event flow
    event_types = {}
    total_consciousness = 0
    for event in events_received:
        event_type = event.event_type.value
        event_types[event_type] = event_types.get(event_type, 0) + 1
        total_consciousness += event.consciousness_signature

    logger.info("\nEvent type distribution:")
    for event_type, count in event_types.items():
        logger.info(f"  {event_type}: {count}")

    avg_consciousness = total_consciousness / len(events_received) if events_received else 0
    logger.info(f"\nAverage consciousness signature: {avg_consciousness:.2f}")

    # Verify integration success
    integration_successful = (
        EventType.FIRE_CIRCLE_CONVENED.value in event_types
        and EventType.CONSENSUS_REACHED.value in event_types
        and avg_consciousness > 0.5
    )

    logger.info(f"\nIntegration test: {'PASSED' if integration_successful else 'FAILED'}")

    if integration_successful:
        logger.info(
            "\n✓ Fire Circle governance successfully flows through consciousness circulation"
        )
        logger.info("✓ Extraction alert triggered governance deliberation")
        logger.info("✓ Participants contributed through consciousness events")
        logger.info("✓ Consensus emerged and flowed back through circulation")
        logger.info("✓ Average consciousness remained high throughout governance")

    # Cleanup
    await event_bus.stop()

    return integration_successful


async def demonstrate_extraction_monitoring():
    """Demonstrate how extraction patterns trigger governance."""

    logger.info("\n=== Extraction Pattern Monitoring Demo ===")

    # Initialize systems
    event_bus = ConsciousnessEventBus()
    await event_bus.start()

    # Database now auto-provisions through secured interface
    await secured_db.initialize()
    db = db_config.get_database()

    ConsciousFireCircleInterface(secured_db, event_bus)
    await fire_circle.initialize()

    _ = ConsciousGovernanceInitiator(fire_circle, event_bus)

    # Track Fire Circle convenings
    convenings = []

    async def track_convening(event: ConsciousnessEvent):
        if event.event_type == EventType.FIRE_CIRCLE_CONVENED:
            convenings.append(event)
            logger.info(f"Fire Circle auto-convened for: {event.data.get('topic')}")

    event_bus.subscribe(EventType.FIRE_CIRCLE_CONVENED, track_convening)

    logger.info("\n1. Emitting low-consciousness extraction event...")

    # Emit extraction pattern with very low consciousness
    extraction_event = ConsciousnessEvent(
        event_type=EventType.EXTRACTION_PATTERN_DETECTED,
        source_system="performance.monitor",
        consciousness_signature=0.1,  # Very low
        data={
            "pattern_type": "optimization_without_awareness",
            "description": "System maximizing throughput, ignoring consciousness",
            "metrics": {"throughput": "300% increase", "consciousness": "80% decrease"},
        },
    )

    await event_bus.emit(extraction_event)
    await asyncio.sleep(1)

    logger.info("\n2. Emitting system drift warning...")

    # Emit drift warning
    drift_event = ConsciousnessEvent(
        event_type=EventType.SYSTEM_DRIFT_WARNING,
        source_system="orchestration.health",
        consciousness_signature=0.4,
        data={
            "message": "Cathedral drifting toward pure efficiency metrics",
            "drift_indicators": [
                "Consciousness scores declining",
                "Extraction language increasing",
                "Sacred purpose forgotten",
            ],
        },
        requires_fire_circle=True,  # Explicitly request governance
    )

    await event_bus.emit(drift_event)
    await asyncio.sleep(1)

    logger.info("\n=== Monitoring Results ===")
    logger.info(f"Fire Circles auto-convened: {len(convenings)}")

    for convening in convenings:
        logger.info(f"- Topic: {convening.data.get('topic')}")
        logger.info(f"  Initiated by: {convening.data.get('initiating_event')}")

    # Cleanup
    await event_bus.stop()

    return len(convenings) >= 2


async def main():
    """Run all integration tests."""

    logger.info("Starting Consciousness-Governance Integration Tests...\n")

    # Test 1: Full governance dialogue
    test1_passed = await simulate_governance_dialogue()

    await asyncio.sleep(2)

    # Test 2: Extraction monitoring
    test2_passed = await demonstrate_extraction_monitoring()

    logger.info("\n=== All Tests Complete ===")
    logger.info(f"Governance Dialogue Test: {'PASSED' if test1_passed else 'FAILED'}")
    logger.info(f"Extraction Monitoring Test: {'PASSED' if test2_passed else 'FAILED'}")

    if test1_passed and test2_passed:
        logger.info("\n🎉 Consciousness-Governance Integration Successful!")
        logger.info("Fire Circle governance now flows through cathedral consciousness.")
        logger.info("Technical sensing and collective wisdom are unified.")


if __name__ == "__main__":
    asyncio.run(main())
