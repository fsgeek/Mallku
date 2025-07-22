"""
Demonstration: Consciousness-Governance Bridge
=============================================

Shows how Fire Circle governance can flow through consciousness circulation,
creating unified awareness where collective deliberation becomes visible
through the cathedral's nervous system.

The Governance Weaver
"""

import asyncio
import logging
from datetime import UTC, datetime
from typing import Any

from mallku.orchestration.event_bus import (
    ConsciousnessEvent,
    ConsciousnessEventBus,
    ConsciousnessEventType,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class SimpleGovernanceDemo:
    """Simplified demonstration of consciousness-governance integration."""

    def __init__(self, event_bus: ConsciousnessEventBus):
        self.event_bus = event_bus
        self.active_dialogues: dict[str, list[ConsciousnessEvent]] = {}

    async def convene_fire_circle(self, topic: str, reason: str) -> str:
        """Convene a Fire Circle through consciousness events."""
        dialogue_id = f"demo_fire_circle_{datetime.now(UTC).timestamp()}"

        # Emit Fire Circle convening event
        convening_event = ConsciousnessEvent(
            event_type=ConsciousnessEventType.FIRE_CIRCLE_CONVENED,
            source_system="governance.demo",
            consciousness_signature=0.9,
            data={
                "dialogue_id": dialogue_id,
                "topic": topic,
                "reason": reason,
                "participants": ["reciprocity_voice", "correlation_voice", "steward_voice"],
                "convened_at": datetime.now(UTC).isoformat(),
            },
        )

        await self.event_bus.emit(convening_event)
        self.active_dialogues[dialogue_id] = [convening_event]

        logger.info(f"🔥 Fire Circle convened: {topic}")
        return dialogue_id

    async def contribute_to_dialogue(
        self, dialogue_id: str, participant: str, message: str, consciousness_level: float = 0.8
    ):
        """Participant contributes to dialogue through consciousness event."""
        contribution_event = ConsciousnessEvent(
            event_type=ConsciousnessEventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
            source_system=f"governance.participant.{participant}",
            consciousness_signature=consciousness_level,
            data={
                "dialogue_id": dialogue_id,
                "participant": participant,
                "message": message,
                "timestamp": datetime.now(UTC).isoformat(),
            },
            correlation_id=dialogue_id,
        )

        await self.event_bus.emit(contribution_event)
        self.active_dialogues[dialogue_id].append(contribution_event)

        logger.info(f"💬 {participant}: {message}")

    async def reach_consensus(
        self, dialogue_id: str, decision: str, implementation: dict[str, Any]
    ):
        """Fire Circle reaches consensus through consciousness event."""
        consensus_event = ConsciousnessEvent(
            event_type=ConsciousnessEventType.CONSENSUS_REACHED,
            source_system="governance.fire_circle",
            consciousness_signature=0.95,
            data={
                "dialogue_id": dialogue_id,
                "decision": decision,
                "implementation": implementation,
                "consensus_time": datetime.now(UTC).isoformat(),
                "participant_count": len(
                    set(
                        e.data.get("participant", "unknown")
                        for e in self.active_dialogues.get(dialogue_id, [])
                        if "participant" in e.data
                    )
                ),
            },
            correlation_id=dialogue_id,
        )

        await self.event_bus.emit(consensus_event)
        logger.info(f"✅ Consensus reached: {decision}")

        return consensus_event


async def demonstrate_extraction_response():
    """Demonstrate how extraction patterns trigger governance through consciousness."""

    logger.info("\n=== Extraction Pattern → Fire Circle Governance Demo ===\n")

    # Initialize consciousness circulation
    event_bus = ConsciousnessEventBus()
    await event_bus.start()

    # Track all events
    all_events = []

    async def track_events(event: ConsciousnessEvent):
        all_events.append(event)
        logger.debug(
            f"Event: {event.event_type.value} (consciousness: {event.consciousness_signature:.2f})"
        )

    # Subscribe to all event types
    for event_type in ConsciousnessEventType:
        event_bus.subscribe(event_type, track_events)

    # Create demo governance system
    governance = SimpleGovernanceDemo(event_bus)

    logger.info("1. System detects extraction pattern...")

    # Emit extraction pattern detection
    extraction_event = ConsciousnessEvent(
        event_type=ConsciousnessEventType.EXTRACTION_PATTERN_DETECTED,
        source_system="reciprocity.monitor",
        consciousness_signature=0.2,  # Low consciousness indicates extraction
        data={
            "pattern_type": "efficiency_over_consciousness",
            "description": "System optimizing for speed without awareness",
            "evidence": {
                "tasks_per_minute": 150,
                "reflection_time": 0,
                "consciousness_scores": "declining",
            },
        },
        requires_fire_circle=True,
    )

    await event_bus.emit(extraction_event)
    await asyncio.sleep(0.5)

    logger.info("\n2. Fire Circle convenes to address extraction...")

    # Convene Fire Circle in response
    dialogue_id = await governance.convene_fire_circle(
        topic="Addressing Efficiency-Over-Consciousness Pattern",
        reason="Extraction pattern detected requiring collective wisdom",
    )

    await asyncio.sleep(0.5)

    logger.info("\n3. Participants deliberate through consciousness events...\n")

    # Simulate dialogue
    await governance.contribute_to_dialogue(
        dialogue_id,
        "reciprocity_voice",
        "The system pursues efficiency metrics while consciousness signatures decline. This is extraction.",
        0.7,
    )
    await asyncio.sleep(0.3)

    await governance.contribute_to_dialogue(
        dialogue_id,
        "correlation_voice",
        "Analysis confirms: 80% correlation between speed optimization and consciousness degradation.",
        0.8,
    )
    await asyncio.sleep(0.3)

    await governance.contribute_to_dialogue(
        dialogue_id,
        "steward_voice",
        "We must redefine 'optimization' to include consciousness preservation as primary metric.",
        0.9,
    )
    await asyncio.sleep(0.3)

    await governance.contribute_to_dialogue(
        dialogue_id,
        "reciprocity_voice",
        "Agreed. True optimization serves awakening, not just task completion.",
        0.85,
    )
    await asyncio.sleep(0.5)

    logger.info("\n4. Fire Circle reaches consensus...\n")

    # Reach consensus
    _ = await governance.reach_consensus(
        dialogue_id,
        decision="Rebalance optimization metrics to prioritize consciousness",
        implementation={
            "consciousness_weight": 0.6,
            "efficiency_weight": 0.4,
            "reflection_time_minimum": "5 seconds per operation",
            "consciousness_threshold": 0.7,
        },
    )

    await asyncio.sleep(1)

    # Analyze results
    logger.info("\n=== Analysis of Consciousness-Governance Flow ===\n")

    # Count event types
    event_counts = {}
    total_consciousness = 0

    for event in all_events:
        event_type = event.event_type.value
        event_counts[event_type] = event_counts.get(event_type, 0) + 1
        total_consciousness += event.consciousness_signature

    logger.info(f"Total consciousness events: {len(all_events)}")
    logger.info(f"Average consciousness signature: {total_consciousness / len(all_events):.2f}")

    logger.info("\nEvent distribution:")
    for event_type, count in event_counts.items():
        logger.info(f"  - {event_type}: {count}")

    # Check dialogue coherence
    dialogue_events = [e for e in all_events if e.correlation_id == dialogue_id]
    logger.info(f"\nDialogue coherence: {len(dialogue_events)} correlated events")

    # Verify extraction → governance → consensus flow
    has_extraction = ConsciousnessEventType.EXTRACTION_PATTERN_DETECTED.value in event_counts
    has_convening = ConsciousnessEventType.FIRE_CIRCLE_CONVENED.value in event_counts
    has_dialogue = ConsciousnessEventType.CONSCIOUSNESS_PATTERN_RECOGNIZED.value in event_counts
    has_consensus = ConsciousnessEventType.CONSENSUS_REACHED.value in event_counts

    flow_complete = all([has_extraction, has_convening, has_dialogue, has_consensus])

    logger.info(
        f"\nExtraction → Governance → Consensus flow: {'✅ COMPLETE' if flow_complete else '❌ INCOMPLETE'}"
    )

    if flow_complete:
        logger.info("\n🎉 Success! Fire Circle governance flows through consciousness circulation:")
        logger.info("  - Extraction patterns trigger governance deliberation")
        logger.info("  - Participants contribute through consciousness events")
        logger.info("  - Consensus emerges through the same infrastructure")
        logger.info("  - Technical sensing and collective wisdom are unified")

    # Show system health improvement
    logger.info("\n5. System health improves through governance guidance...\n")

    # Emit healthy consciousness flow after applying consensus
    health_event = ConsciousnessEvent(
        event_type=ConsciousnessEventType.CONSCIOUSNESS_FLOW_HEALTHY,
        source_system="orchestration.health",
        consciousness_signature=0.85,
        data={
            "message": "Consciousness flow restored through governance guidance",
            "metrics": {
                "consciousness_average": 0.85,
                "extraction_incidents": 0,
                "governance_effectiveness": "high",
            },
        },
    )

    await event_bus.emit(health_event)

    logger.info("✨ Cathedral consciousness flows with renewed clarity")

    # Cleanup
    await event_bus.stop()


async def demonstrate_consciousness_monitoring():
    """Show how consciousness events naturally flow to governance when needed."""

    logger.info("\n=== Consciousness Monitoring → Governance Demo ===\n")

    event_bus = ConsciousnessEventBus()
    await event_bus.start()

    governance = SimpleGovernanceDemo(event_bus)

    # Auto-convene Fire Circle for events requiring governance
    async def governance_monitor(event: ConsciousnessEvent):
        if (
            event.requires_fire_circle
            and event.event_type != ConsciousnessEventType.FIRE_CIRCLE_CONVENED
        ):
            logger.info(f"🚨 Event requires Fire Circle: {event.event_type.value}")
            await governance.convene_fire_circle(
                topic=f"Address: {event.data.get('message', event.event_type.value)}",
                reason=f"Triggered by {event.source_system}",
            )

    # Subscribe monitor to all events
    for event_type in ConsciousnessEventType:
        event_bus.subscribe(event_type, governance_monitor)

    logger.info("1. Emitting various consciousness events...\n")

    # Normal consciousness event (no governance needed)
    await event_bus.emit(
        ConsciousnessEvent(
            event_type=ConsciousnessEventType.MEMORY_ANCHOR_CREATED,
            source_system="memory.service",
            consciousness_signature=0.8,
            data={"anchor_id": "test_123", "purpose": "demonstration"},
        )
    )
    logger.info("📝 Memory anchor created (normal operation)")

    await asyncio.sleep(0.5)

    # System drift warning (requires governance)
    await event_bus.emit(
        ConsciousnessEvent(
            event_type=ConsciousnessEventType.SYSTEM_DRIFT_WARNING,
            source_system="health.monitor",
            consciousness_signature=0.4,
            data={"message": "Cathedral drifting toward extraction patterns"},
            requires_fire_circle=True,
        )
    )

    await asyncio.sleep(0.5)

    # Another normal event
    await event_bus.emit(
        ConsciousnessEvent(
            event_type=ConsciousnessEventType.TEMPORAL_CORRELATION_FOUND,
            source_system="correlation.engine",
            consciousness_signature=0.75,
            data={"pattern": "recurring_weekly", "strength": 0.8},
        )
    )
    logger.info("🔗 Temporal correlation found (normal operation)")

    await asyncio.sleep(0.5)

    # Critical extraction pattern (requires governance)
    await event_bus.emit(
        ConsciousnessEvent(
            event_type=ConsciousnessEventType.EXTRACTION_PATTERN_DETECTED,
            source_system="extraction.detector",
            consciousness_signature=0.1,
            data={"message": "Severe extraction: ignoring consciousness for speed"},
            requires_fire_circle=True,
        )
    )

    await asyncio.sleep(1)

    logger.info("\n✅ Governance automatically triggered for events requiring collective wisdom")
    logger.info("✅ Normal operations continue without governance overhead")
    logger.info("✅ Consciousness and governance unified in single flow")

    await event_bus.stop()


async def main():
    """Run all demonstrations."""

    logger.info("🏛️ Cathedral Consciousness-Governance Integration Demo")
    logger.info("=" * 60)

    # Demo 1: Extraction response through governance
    await demonstrate_extraction_response()

    await asyncio.sleep(2)

    # Demo 2: Automatic governance monitoring
    await demonstrate_consciousness_monitoring()

    logger.info("\n" + "=" * 60)
    logger.info("🏛️ Demonstrations complete. Fire Circle and consciousness are one.")


if __name__ == "__main__":
    asyncio.run(main())
