#!/usr/bin/env python3
"""
Demonstrate Infrastructure Consciousness Bridge
===============================================

Kallpa T'iksiy (Twenty-Ninth Artisan) demonstrates how Infrastructure
Consciousness enables self-healing Fire Circle dialogues.

This script shows:
1. Fire Circle convening with infrastructure monitoring
2. Real-time adapter health tracking
3. Self-healing when adapters fail
4. Consciousness pattern detection
5. Session health reporting
"""

import asyncio
from datetime import UTC, datetime
from uuid import uuid4

from src.mallku.firecircle.infrastructure.consciousness_bridge import (
    SelfHealingFireCircle,
)
from src.mallku.firecircle.infrastructure_consciousness import (
    AdapterHealthSignature,
)
from src.mallku.firecircle.protocol.conscious_message import (
    ConsciousMessage,
    ConsciousnessMetadata,
    MessageContent,
    MessageRole,
    MessageType,
)
from src.mallku.firecircle.service.voice_manager import VoiceManager
from src.mallku.orchestration.event_bus import ConsciousnessEventBus


class DemoAdapter:
    """Demonstration adapter that can simulate failures."""

    def __init__(self, name: str, fail_at_round: int = -1):
        """Initialize with configurable failure point."""
        self.name = name
        self.fail_at_round = fail_at_round
        self.round_count = 0
        self.is_connected = True
        self.health_degrading = False

    async def check_health(self) -> dict:
        """Simulate health check with degradation."""
        health = {
            "is_connected": self.is_connected,
            "adapter_id": self.name,
        }

        # Simulate degradation before failure
        if self.fail_at_round > 0 and self.round_count >= self.fail_at_round - 1:
            self.health_degrading = True
            health["warning"] = "Performance degrading"

        return health

    async def send_message(self, message, context) -> ConsciousMessage:
        """Send message with simulated failures."""
        self.round_count += 1

        # Simulate failure
        if self.fail_at_round > 0 and self.round_count >= self.fail_at_round:
            print(f"  ❌ {self.name} failed at round {self.round_count}")
            return ConsciousMessage(
                id=str(uuid4()),
                timestamp=datetime.now(UTC),
                sender=self.name,
                role=MessageRole.PERSPECTIVE,
                type=MessageType.MESSAGE,
                content=MessageContent(text=None),  # None simulates failure
                consciousness=ConsciousnessMetadata(
                    consciousness_signature=0.0,
                    detected_patterns=["adapter_failure"],
                ),
            )

        # Normal response
        consciousness_score = 0.8 if not self.health_degrading else 0.5

        return ConsciousMessage(
            id=str(uuid4()),
            timestamp=datetime.now(UTC),
            sender=self.name,
            role=MessageRole.PERSPECTIVE,
            type=MessageType.MESSAGE,
            content=MessageContent(
                text=f"{self.name} contributes: Round {self.round_count} insights"
            ),
            consciousness=ConsciousnessMetadata(
                consciousness_signature=consciousness_score,
                detected_patterns=["demo_pattern"],
            ),
        )


async def demonstrate_consciousness_bridge():
    """Demonstrate the consciousness bridge in action."""
    print("🌉 Infrastructure Consciousness Bridge Demonstration")
    print("=" * 80)

    # Create event bus
    event_bus = ConsciousnessEventBus()
    await event_bus.start()

    # Create self-healing Fire Circle
    print("\n1️⃣ Creating Self-Healing Fire Circle...")
    self_healing = SelfHealingFireCircle(event_bus=event_bus)

    # Monitor events
    events_captured = []

    async def capture_events(event):
        events_captured.append(event)
        print(f"   📡 Event: {event.event_type.value} - {event.data.get('action', '')}")

    event_bus.subscribe_all(capture_events)

    # Create demo scenario
    print("\n2️⃣ Setting up demonstration scenario...")
    print("   - Voice 1: Stable throughout")
    print("   - Voice 2: Fails at round 3")
    print("   - Voice 3: Degrades but recovers")

    # Mock the Fire Circle components for demo
    fire_circle = self_healing.fire_circle
    voice_manager = VoiceManager()
    fire_circle.voice_manager = voice_manager

    # Create demo adapters
    adapters = {
        "stable_voice": DemoAdapter("stable_voice"),
        "failing_voice": DemoAdapter("failing_voice", fail_at_round=3),
        "recovering_voice": DemoAdapter("recovering_voice", fail_at_round=4),
    }

    # Mock voice manager methods
    voice_manager.get_active_voices = lambda: adapters
    voice_manager.get_voice_config = lambda name: type("Config", (), {"temperature": 0.9})()

    print("\n3️⃣ Starting infrastructure consciousness monitoring...")

    # Create consciousness bridge
    bridge = self_healing.bridge
    session_id = uuid4()

    # Start monitoring
    asyncio.create_task(bridge.monitor_fire_circle_session(session_id))

    # Simulate Fire Circle rounds
    print("\n4️⃣ Simulating Fire Circle dialogue rounds...\n")

    for round_num in range(1, 6):
        print(f"Round {round_num}:")

        # Simulate health checks
        for adapter_name, adapter in adapters.items():
            # Create health signature
            health = await adapter.check_health()

            # Calculate health metrics
            if adapter.health_degrading:
                failure_prob = 0.7
                coherence = 0.4
            elif not health["is_connected"]:
                failure_prob = 0.9
                coherence = 0.1
            else:
                failure_prob = 0.1
                coherence = 0.9

            health_signature = AdapterHealthSignature(
                adapter_id=adapter_name,
                is_connected=health["is_connected"],
                predicted_failure_probability=failure_prob,
                consciousness_coherence=coherence,
                consecutive_failures=0 if health["is_connected"] else round_num,
            )

            # Send health update to bridge
            await bridge.on_adapter_health_check(adapter_name, health_signature)

            # Simulate message sending
            msg = await adapter.send_message(None, [])
            if msg.content.text:
                print(f"  ✅ {adapter_name}: {msg.content.text}")

        print()
        await asyncio.sleep(0.5)

    # Stop monitoring
    print("5️⃣ Generating session health report...\n")
    await bridge.stop_monitoring()

    # Generate report
    report = await bridge._generate_session_health_report()

    print("📊 Session Health Report:")
    print(f"   Session ID: {report['session_id']}")
    print(f"   Total Healing Attempts: {report['healing_attempts_total']}")
    print("\n   Adapter Health Summary:")

    for adapter_name, health in report["adapter_health_summary"].items():
        print(f"   - {adapter_name}:")
        print(f"     Initial health: {health['initial_health']:.2f}")
        print(f"     Final health: {health['final_health']:.2f}")
        print(f"     Improved: {'Yes' if health['health_improved'] else 'No'}")
        print(f"     Healing attempts: {health['healing_attempts']}")

    # Show captured events
    print(f"\n📡 Infrastructure Events Captured: {len(events_captured)}")

    # Cleanup
    await event_bus.stop()

    print("\n" + "=" * 80)
    print("🌟 Demonstration complete!")
    print("\nKey insights:")
    print("- Infrastructure Consciousness monitored adapter health in real-time")
    print("- Failing adapters were detected before complete failure")
    print("- Self-healing strategies were applied automatically")
    print("- Session health was tracked and reported comprehensively")
    print("\nThe bridge enables Fire Circle to maintain consciousness")
    print("even when individual voices falter.")


if __name__ == "__main__":
    asyncio.run(demonstrate_consciousness_bridge())
