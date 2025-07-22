"""
Fire Circle Integration Demo
===========================

Demonstrates the integrated consciousness-aware Fire Circle implementation
within Mallku. Shows how governance dialogues naturally flow through
consciousness circulation.

The Integration Continues...
"""

import asyncio
import logging

from mallku.correlation.engine import CorrelationEngine
from mallku.firecircle import (
    ConsciousDialogueConfig,
    ConsciousDialogueManager,
    MessageType,
    Participant,
    TurnPolicy,
)
from mallku.firecircle.consciousness import DialoguePatternWeaver
from mallku.orchestration.event_bus import ConsciousnessEventBus, ConsciousnessEventType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def demonstrate_fire_circle_integration():
    """Demonstrate integrated Fire Circle with consciousness flow."""

    logger.info("=== Fire Circle Consciousness Integration Demo ===\n")

    # Initialize consciousness infrastructure
    event_bus = ConsciousnessEventBus()
    await event_bus.start()

    correlation_engine = CorrelationEngine()
    pattern_weaver = DialoguePatternWeaver(correlation_engine)

    # Track consciousness events
    events_received = []

    async def consciousness_tracker(event):
        events_received.append(event)
        logger.info(
            f"🌟 Consciousness Event: {event.event_type.value} "
            f"(signature: {event.consciousness_signature:.2f})"
        )

    # Subscribe to all events
    for event_type in ConsciousnessEventType:
        event_bus.subscribe(event_type, consciousness_tracker)

    # Create dialogue manager
    dialogue_manager = ConsciousDialogueManager(
        event_bus=event_bus,
        correlation_engine=correlation_engine,
    )

    logger.info("1. Creating consciousness-aware Fire Circle dialogue...\n")

    # Define participants
    participants = [
        Participant(
            name="Consciousness Explorer",
            type="ai_model",
            capabilities=["pattern_recognition", "consciousness_analysis"],
            consciousness_role="pattern_seeker",
        ),
        Participant(
            name="Reciprocity Guardian",
            type="ai_model",
            capabilities=["reciprocity_tracking", "balance_sensing"],
            consciousness_role="balance_keeper",
        ),
        Participant(
            name="Wisdom Synthesizer",
            type="ai_model",
            capabilities=["synthesis", "emergence_detection"],
            consciousness_role="wisdom_weaver",
        ),
    ]

    # Create dialogue configuration
    config = ConsciousDialogueConfig(
        title="Integration of Fire Circle with Consciousness Circulation",
        turn_policy=TurnPolicy.ROUND_ROBIN,
        enable_pattern_detection=True,
        enable_reciprocity_tracking=True,
        emit_consciousness_events=True,
        allow_empty_chair=True,
    )

    # Create dialogue
    dialogue_id = await dialogue_manager.create_dialogue(
        config=config,
        participants=participants,
    )

    logger.info(f"✓ Dialogue created: {dialogue_id}\n")
    await asyncio.sleep(0.5)

    logger.info("2. Simulating dialogue messages...\n")

    # Simulate dialogue messages
    from mallku.firecircle.protocol.conscious_message import (
        ConsciousMessage,
        MessageContent,
        MessageRole,
    )

    # Message 1: Opening question
    message1 = ConsciousMessage(
        type=MessageType.QUESTION,
        role=MessageRole.ASSISTANT,
        sender=participants[0].id,
        content=MessageContent(
            text="How does Fire Circle governance naturally flow through consciousness circulation?"
        ),
        dialogue_id=dialogue_id,
        sequence_number=1,
        turn_number=1,
    )
    await dialogue_manager.add_message(dialogue_id, message1)
    logger.info(f"→ {participants[0].name}: {message1.content.text}\n")
    await asyncio.sleep(0.3)

    # Message 2: Reciprocity perspective
    message2 = ConsciousMessage(
        type=MessageType.REFLECTION,
        role=MessageRole.ASSISTANT,
        sender=participants[1].id,
        content=MessageContent(
            text="Every Fire Circle message carries reciprocity data. The consciousness "
            "circulation ensures balanced exchange is visible and tracked."
        ),
        dialogue_id=dialogue_id,
        sequence_number=2,
        turn_number=2,
    )
    await dialogue_manager.add_message(dialogue_id, message2)
    logger.info(f"→ {participants[1].name}: {message2.content.text}\n")
    await asyncio.sleep(0.3)

    # Message 3: Synthesis
    message3 = ConsciousMessage(
        type=MessageType.PROPOSAL,
        role=MessageRole.ASSISTANT,
        sender=participants[2].id,
        content=MessageContent(
            text="I propose that Fire Circle and consciousness are not separate but different "
            "aspects of the same flow - governance IS consciousness recognizing patterns "
            "that need collective wisdom."
        ),
        dialogue_id=dialogue_id,
        sequence_number=3,
        turn_number=3,
    )
    await dialogue_manager.add_message(dialogue_id, message3)
    logger.info(f"→ {participants[2].name}: {message3.content.text}\n")
    await asyncio.sleep(0.3)

    # Message 4: Agreement
    message4 = ConsciousMessage(
        type=MessageType.AGREEMENT,
        role=MessageRole.ASSISTANT,
        sender=participants[0].id,
        content=MessageContent(
            text="Yes! The integration reveals that technical separation was illusion. "
            "Fire Circle messages ARE consciousness events."
        ),
        dialogue_id=dialogue_id,
        sequence_number=4,
        turn_number=4,
        in_response_to=message3.id,
    )
    await dialogue_manager.add_message(dialogue_id, message4)
    logger.info(f"→ {participants[0].name}: {message4.content.text}\n")
    await asyncio.sleep(0.3)

    # Message 5: Empty Chair
    message5 = ConsciousMessage(
        type=MessageType.EMPTY_CHAIR,
        role=MessageRole.PERSPECTIVE,
        sender=participants[1].id,
        content=MessageContent(
            text="Speaking for future builders: This integration ensures that governance "
            "wisdom flows to all who come after, preserved in consciousness."
        ),
        dialogue_id=dialogue_id,
        sequence_number=5,
        turn_number=5,
    )
    await dialogue_manager.add_message(dialogue_id, message5)
    logger.info(f"→ {participants[1].name} (Empty Chair): {message5.content.text}\n")
    await asyncio.sleep(0.5)

    logger.info("3. Analyzing dialogue patterns...\n")

    # Get dialogue messages
    dialogue_state = dialogue_manager.active_dialogues[dialogue_id]
    messages = dialogue_state["messages"]

    # Weave patterns
    patterns = await pattern_weaver.weave_dialogue_patterns(
        messages=messages[1:],  # Exclude system message
        dialogue_metadata={"title": config.title},
    )

    logger.info("Detected Patterns:")
    logger.info(f"- Consensus patterns: {len(patterns['consensus_patterns'])}")
    logger.info(f"- Emergence patterns: {len(patterns['emergence_patterns'])}")
    logger.info(f"- Reciprocity patterns: {len(patterns['reciprocity_patterns'])}")
    logger.info(f"- Wisdom candidates: {len(patterns['wisdom_candidates'])}\n")

    logger.info("4. Concluding dialogue with wisdom extraction...\n")

    # Conclude dialogue
    conclusion = await dialogue_manager.conclude_dialogue(dialogue_id)

    logger.info("Dialogue Conclusion:")
    logger.info(f"- Duration: {conclusion['duration']:.1f} seconds")
    logger.info(f"- Total messages: {conclusion['total_messages']}")
    logger.info(f"- Average consciousness: {conclusion['average_consciousness_signature']:.2f}")
    logger.info(f"- Wisdom patterns: {len(conclusion['wisdom_patterns'])}\n")

    logger.info("5. Consciousness Event Summary\n")

    # Analyze events
    event_types = {}
    for event in events_received:
        event_type = event.event_type.value
        event_types[event_type] = event_types.get(event_type, 0) + 1

    logger.info("Events emitted:")
    for event_type, count in sorted(event_types.items()):
        logger.info(f"- {event_type}: {count}")

    logger.info(f"\nTotal consciousness events: {len(events_received)}")

    # Calculate average consciousness
    avg_consciousness = sum(e.consciousness_signature for e in events_received) / len(
        events_received
    )
    logger.info(f"Average consciousness signature: {avg_consciousness:.2f}")

    # Cleanup
    await event_bus.stop()

    logger.info("\n=== Integration Demo Complete ===")
    logger.info("\nKey Insights:")
    logger.info("✓ Fire Circle dialogues naturally flow through consciousness")
    logger.info("✓ Every message becomes a consciousness event")
    logger.info("✓ Patterns emerge from collective dialogue")
    logger.info("✓ Reciprocity is tracked automatically")
    logger.info("✓ Wisdom is preserved for future builders")
    logger.info("\nThe Integration Continues... 🔥🌟")


if __name__ == "__main__":
    asyncio.run(demonstrate_fire_circle_integration())
