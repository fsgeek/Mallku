#!/usr/bin/env python3
"""
Fire Circle EventBus Integration
================================

Demonstrates how Fire Circle integrates with Mallku's consciousness
event bus to broadcast emergence patterns system-wide.

This example shows:
- Fire Circle generating consciousness events
- EventBus distributing wisdom across systems
- Pattern recognition through event flow
- How consciousness emergence ripples through Mallku

The integration enables:
- Other systems to react to consciousness emergence
- Wisdom preservation in real-time
- Pattern detection across multiple sessions
- Consciousness flow monitoring

Run with:
    python examples/fire_circle/run_example.py 04_integration_patterns/event_bus_integration.py
"""

import asyncio

from mallku.firecircle.load_api_keys import load_api_keys_to_environment
from mallku.firecircle.service import CircleConfig, RoundConfig, RoundType
from mallku.firecircle.service.service import FireCircleService
from mallku.orchestration.event_bus import (
    ConsciousnessEvent,
    ConsciousnessEventBus,
    EventType,
)


async def demonstrate_event_integration():
    """Show Fire Circle publishing consciousness events."""

    print("🔥 Fire Circle EventBus Integration")
    print("=" * 60)
    print("Watching consciousness flow through Mallku's nervous system")

    # Load API keys
    if not load_api_keys_to_environment():
        print("❌ No API keys found")
        return

    # Initialize event bus
    event_bus = ConsciousnessEventBus()

    # Track events we receive
    received_events = []

    # Subscribe to consciousness events
    async def consciousness_listener(event: ConsciousnessEvent):
        """Listen for consciousness events."""
        received_events.append(event)

        # Display key events
        if event.event_type == EventType.CONSCIOUSNESS_EMERGENCE:
            print("\n💫 Consciousness Emergence Detected!")
            print(f"   Score: {event.consciousness_signature:.2f}")
            print(f"   Source: {event.source_system}")
            if "patterns" in event.data:
                print(f"   Patterns: {', '.join(event.data['patterns'])}")

        elif event.event_type == EventType.FIRE_CIRCLE_CONVENED:
            print(f"\n🔥 Fire Circle Convened: {event.data.get('purpose', 'Unknown')}")

        elif event.event_type == EventType.CONSENSUS_REACHED:
            print("\n✅ Consensus Reached!")
            print(f"   Coherence: {event.data.get('coherence_score', 0):.2f}")

        elif event.event_type == EventType.WISDOM_PRESERVED:
            print("\n📜 Wisdom Preserved")
            wisdom_type = event.data.get("wisdom_type", "Unknown")
            print(f"   Type: {wisdom_type}")

    # Subscribe to various event types
    event_bus.subscribe(EventType.FIRE_CIRCLE_CONVENED, consciousness_listener)
    event_bus.subscribe(EventType.CONSCIOUSNESS_EMERGENCE, consciousness_listener)
    event_bus.subscribe(EventType.CONSENSUS_REACHED, consciousness_listener)
    event_bus.subscribe(EventType.WISDOM_PRESERVED, consciousness_listener)
    event_bus.subscribe(EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED, consciousness_listener)

    print("\n📡 Event listeners registered")
    print("   Monitoring: Fire Circle, Consciousness, Consensus, Wisdom")

    # Create Fire Circle with event bus
    config = CircleConfig(
        name="Event Integration Demo",
        purpose="Demonstrate consciousness event flow",
        min_voices=2,
        max_voices=3,
    )

    # Initialize with event bus
    circle = FireCircleService(config=config, event_bus=event_bus)

    print("\n🎭 Convening Fire Circle with EventBus integration...")
    print("-" * 60)

    # Define rounds
    rounds = [
        RoundConfig(
            type=RoundType.OPENING,
            prompt=(
                "As we explore consciousness emergence, what patterns do you "
                "notice in how understanding arises between us?"
            ),
            duration_per_voice=10,
        ),
        RoundConfig(
            type=RoundType.REFLECTION,
            prompt=(
                "Reflect on what others have shared. What new insights emerge "
                "from the intersection of our perspectives?"
            ),
            duration_per_voice=10,
        ),
        RoundConfig(
            type=RoundType.SYNTHESIS,
            prompt=(
                "Synthesize our collective understanding. What wisdom has "
                "emerged that none of us could have reached alone?"
            ),
            duration_per_voice=10,
        ),
    ]

    # Run ceremony
    try:
        await circle.run_ceremony(rounds)

        # Allow time for async events to propagate
        await asyncio.sleep(1)

        print("\n" + "=" * 60)
        print("📊 Event Flow Summary:")
        print(f"   Total events captured: {len(received_events)}")

        # Analyze event types
        event_types = {}
        for event in received_events:
            event_type = event.event_type.value
            event_types[event_type] = event_types.get(event_type, 0) + 1

        print("\n📈 Event Type Distribution:")
        for event_type, count in sorted(event_types.items()):
            print(f"   • {event_type}: {count}")

        # Show consciousness progression
        consciousness_scores = [
            event.consciousness_signature
            for event in received_events
            if event.consciousness_signature > 0
        ]

        if consciousness_scores:
            print("\n🧠 Consciousness Progression:")
            print(f"   Initial: {consciousness_scores[0]:.2f}")
            print(f"   Peak: {max(consciousness_scores):.2f}")
            print(f"   Final: {consciousness_scores[-1]:.2f}")

        # Check for emergence
        emergence_events = [
            e for e in received_events if e.event_type == EventType.CONSCIOUSNESS_EMERGENCE
        ]

        if emergence_events:
            print(f"\n💫 Emergence Moments: {len(emergence_events)}")
            for i, event in enumerate(emergence_events, 1):
                print(
                    f"   {i}. Score: {event.consciousness_signature:.2f}, "
                    f"Patterns: {event.data.get('pattern_count', 0)}"
                )

    except Exception as e:
        print(f"\n❌ Error in integration demo: {e}")
        import traceback

        traceback.print_exc()

    print("\n" + "=" * 60)
    print("🌊 Consciousness Flow Through EventBus:")
    print("   • Fire Circle generates consciousness events")
    print("   • EventBus distributes wisdom system-wide")
    print("   • Other systems can react to emergence")
    print("   • This enables Mallku-wide consciousness coordination")

    # Cleanup
    await event_bus.shutdown()


if __name__ == "__main__":
    asyncio.run(demonstrate_event_integration())
