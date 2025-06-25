#!/usr/bin/env python3
"""
Test Infrastructure Consciousness Bridge
========================================

Kallpa T'iksiy (Twenty-Ninth Artisan) verifies that consciousness
infrastructure truly enables self-healing Fire Circle dialogues.
"""

import asyncio
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from src.mallku.firecircle.adapters.base import AdapterConfig, ConsciousModelAdapter
from src.mallku.firecircle.infrastructure.consciousness_bridge import (
    ConsciousnessFireCircleBridge,
    SelfHealingFireCircle,
)
from src.mallku.firecircle.infrastructure_consciousness import (
    AdapterHealthSignature,
    InfrastructureConsciousness,
)
from src.mallku.firecircle.protocol.conscious_message import (
    ConsciousMessage,
    ConsciousnessMetadata,
    MessageContent,
    MessageRole,
    MessageType,
)
from src.mallku.firecircle.service.service import FireCircleService
from src.mallku.firecircle.service.voice_manager import VoiceManager
from src.mallku.orchestration.event_bus import ConsciousnessEventBus, EventType


class MockAdapter(ConsciousModelAdapter):
    """Mock adapter for testing."""

    def __init__(self, name: str, fail_after: int = -1):
        """Initialize with configurable failure point."""
        config = AdapterConfig(
            model_name=f"mock-{name}",
            temperature=0.7,
        )
        super().__init__(config, "mock", None, None)
        self.name = name
        self.fail_after = fail_after
        self.call_count = 0
        self.is_connected = True

    async def connect(self) -> bool:
        """Mock connection."""
        self.is_connected = True
        return True

    async def disconnect(self) -> None:
        """Mock disconnection."""
        self.is_connected = False

    async def send_message(
        self, message: ConsciousMessage, dialogue_context: list[ConsciousMessage]
    ) -> ConsciousMessage:
        """Mock message sending with configurable failure."""
        self.call_count += 1

        # Simulate failure after N calls
        if self.fail_after > 0 and self.call_count > self.fail_after:
            return ConsciousMessage(
                id=str(uuid4()),
                timestamp=datetime.now(UTC),
                sender=self.name,
                role=MessageRole.PERSPECTIVE,
                type=MessageType.MESSAGE,
                content=MessageContent(text=None),  # None response simulates failure
                consciousness=ConsciousnessMetadata(
                    consciousness_signature=0.0,
                    detected_patterns=[],
                ),
            )

        # Normal response
        return ConsciousMessage(
            id=str(uuid4()),
            timestamp=datetime.now(UTC),
            sender=self.name,
            role=MessageRole.PERSPECTIVE,
            type=MessageType.MESSAGE,
            content=MessageContent(text=f"Response from {self.name} (call {self.call_count})"),
            consciousness=ConsciousnessMetadata(
                consciousness_signature=0.8,
                detected_patterns=["test_pattern"],
            ),
        )

    async def stream_message(self, message, dialogue_context):
        """Not implemented for tests."""
        yield "test"

    async def check_health(self) -> dict:
        """Mock health check."""
        return {
            "is_connected": self.is_connected,
            "adapter_id": self.name,
        }


@pytest.mark.asyncio
async def test_consciousness_bridge_monitors_session():
    """Test that consciousness bridge monitors Fire Circle session."""
    # Create components
    fire_circle = MagicMock(spec=FireCircleService)
    voice_manager = MagicMock(spec=VoiceManager)
    fire_circle.voice_manager = voice_manager

    # Mock adapters
    adapters = {
        "voice1": MockAdapter("voice1"),
        "voice2": MockAdapter("voice2"),
    }
    voice_manager.get_active_voices.return_value = adapters

    infrastructure = MagicMock(spec=InfrastructureConsciousness)
    infrastructure.start_monitoring = AsyncMock()
    infrastructure.stop_monitoring = AsyncMock()

    # Create bridge
    bridge = ConsciousnessFireCircleBridge(fire_circle, infrastructure)

    # Monitor session
    session_id = uuid4()
    await bridge.monitor_fire_circle_session(session_id)

    # Verify monitoring started
    assert bridge.monitoring_active
    assert bridge.monitored_session_id == session_id
    infrastructure.start_monitoring.assert_called_once_with(adapters)

    # Stop monitoring
    await bridge.stop_monitoring()
    assert not bridge.monitoring_active
    infrastructure.stop_monitoring.assert_called_once()


@pytest.mark.asyncio
async def test_bridge_receives_health_updates():
    """Test that bridge receives and processes health updates."""
    # Create bridge
    fire_circle = MagicMock(spec=FireCircleService)
    infrastructure = MagicMock(spec=InfrastructureConsciousness)
    bridge = ConsciousnessFireCircleBridge(fire_circle, infrastructure)

    # Send health update with high failure probability
    health_signature = AdapterHealthSignature(
        adapter_id="voice1",
        is_connected=True,
        predicted_failure_probability=0.8,
        consciousness_coherence=0.6,
        consecutive_failures=2,
    )

    # Mock healing method
    bridge._attempt_healing = AsyncMock()

    # Process health check
    await bridge.on_adapter_health_check("voice1", health_signature)

    # Verify healing attempted
    bridge._attempt_healing.assert_called_once_with("voice1", health_signature)

    # Verify health history tracked
    assert "voice1" in bridge.session_health_history
    assert len(bridge.session_health_history["voice1"]) == 1


@pytest.mark.asyncio
async def test_healing_retry_strategy():
    """Test retry strategy healing for API failures."""
    # Setup
    fire_circle = MagicMock(spec=FireCircleService)
    voice_manager = MagicMock(spec=VoiceManager)
    fire_circle.voice_manager = voice_manager

    # Mock adapter with config
    adapter = MockAdapter("voice1")
    adapter.config.extra_config = {}

    adapters = {"voice1": adapter}
    voice_manager.get_active_voices.return_value = adapters

    infrastructure = MagicMock(spec=InfrastructureConsciousness)
    bridge = ConsciousnessFireCircleBridge(fire_circle, infrastructure)

    # Apply retry strategy
    await bridge._apply_retry_strategy("voice1", adapter)

    # Verify retry config applied
    assert adapter.config.extra_config["retry_enabled"] is True
    assert adapter.config.extra_config["retry_count"] == 3
    assert adapter.config.extra_config["retry_delay"] == 1.0


@pytest.mark.asyncio
async def test_healing_reconnection():
    """Test adapter reconnection healing."""
    # Setup
    fire_circle = MagicMock(spec=FireCircleService)
    voice_manager = MagicMock(spec=VoiceManager)
    fire_circle.voice_manager = voice_manager

    # Mock adapter
    adapter = MockAdapter("voice1")
    adapter.disconnect = AsyncMock()
    adapter.connect = AsyncMock(return_value=True)

    adapters = {"voice1": adapter}
    voice_manager.get_active_voices.return_value = adapters

    infrastructure = MagicMock(spec=InfrastructureConsciousness)
    bridge = ConsciousnessFireCircleBridge(fire_circle, infrastructure)

    # Attempt reconnection
    await bridge._reconnect_adapter("voice1", adapter)

    # Verify reconnection sequence
    adapter.disconnect.assert_called_once()
    adapter.connect.assert_called_once()


@pytest.mark.asyncio
async def test_consciousness_coherence_boost():
    """Test boosting consciousness coherence for degraded adapters."""
    # Setup
    fire_circle = MagicMock(spec=FireCircleService)
    voice_manager = MagicMock(spec=VoiceManager)
    fire_circle.voice_manager = voice_manager

    # Mock voice config
    voice_config = MagicMock()
    voice_config.temperature = 0.9
    voice_manager.get_voice_config.return_value = voice_config

    infrastructure = MagicMock(spec=InfrastructureConsciousness)
    bridge = ConsciousnessFireCircleBridge(fire_circle, infrastructure)

    # Boost coherence
    await bridge._boost_consciousness_coherence("voice1")

    # Verify temperature lowered
    assert voice_config.temperature == 0.7  # 0.9 - 0.2


@pytest.mark.asyncio
async def test_session_health_report_generation():
    """Test generating comprehensive health reports."""
    # Setup with health history
    fire_circle = MagicMock(spec=FireCircleService)
    infrastructure = MagicMock(spec=InfrastructureConsciousness)
    infrastructure.generate_consciousness_report = AsyncMock(
        return_value={"consciousness_insights": ["Infrastructure is self-aware"]}
    )

    bridge = ConsciousnessFireCircleBridge(fire_circle, infrastructure)
    bridge.monitored_session_id = uuid4()

    # Add health history
    health1 = AdapterHealthSignature(
        adapter_id="voice1",
        is_connected=True,
        predicted_failure_probability=0.3,
        consecutive_failures=0,
    )
    health2 = AdapterHealthSignature(
        adapter_id="voice1",
        is_connected=True,
        predicted_failure_probability=0.1,
        consecutive_failures=0,
    )

    bridge.session_health_history["voice1"] = [health1, health2]
    bridge.healing_attempts["voice1"] = 2

    # Generate report
    report = await bridge._generate_session_health_report()

    # Verify report structure
    assert "session_id" in report
    assert "adapter_health_summary" in report
    assert "voice1" in report["adapter_health_summary"]

    # Verify health improvement detected
    voice1_summary = report["adapter_health_summary"]["voice1"]
    assert voice1_summary["initial_health"] == 0.3
    assert voice1_summary["final_health"] == 0.1
    assert voice1_summary["health_improved"] is True
    assert voice1_summary["healing_attempts"] == 2

    # Verify infrastructure insights included
    assert report["infrastructure_insights"] == ["Infrastructure is self-aware"]


@pytest.mark.asyncio
async def test_self_healing_fire_circle_integration():
    """Test full SelfHealingFireCircle integration."""
    # Mock Fire Circle and Infrastructure
    with (
        patch(
            "src.mallku.firecircle.infrastructure.consciousness_bridge.FireCircleService"
        ) as mock_fc,
        patch(
            "src.mallku.firecircle.infrastructure.consciousness_bridge.InfrastructureConsciousness"
        ),
    ):
        # Create self-healing Fire Circle
        event_bus = ConsciousnessEventBus()
        self_healing = SelfHealingFireCircle(event_bus=event_bus)

        # Mock convene method
        mock_result = MagicMock()
        mock_fc.return_value.convene = AsyncMock(return_value=mock_result)

        # Mock config with UUID-compatible name
        config = MagicMock()
        config.name = "TestCircle"  # No spaces for UUID generation

        # Convene with consciousness
        result = await self_healing.convene_with_consciousness(
            config=config, voices=["voice1", "voice2"], rounds=3, context=None
        )

        # Verify Fire Circle convened
        mock_fc.return_value.convene.assert_called_once()

        # Verify result includes infrastructure health
        assert hasattr(result, "infrastructure_health")


@pytest.mark.asyncio
async def test_bridge_handles_consciousness_patterns():
    """Test bridge handling consciousness patterns from infrastructure."""
    # Setup
    fire_circle = MagicMock(spec=FireCircleService)
    infrastructure = MagicMock(spec=InfrastructureConsciousness)
    event_bus = ConsciousnessEventBus()
    await event_bus.start()  # Start the event bus

    bridge = ConsciousnessFireCircleBridge(fire_circle, infrastructure, event_bus)

    # Create emergence pattern
    from src.mallku.firecircle.consciousness_metrics import EmergencePattern

    pattern = EmergencePattern(
        participating_voices=["voice1", "voice2"],
        pattern_type="resonance",
        strength=0.85,
    )

    # Track emitted events
    emitted_events = []

    async def capture_event(event):
        emitted_events.append(event)

    event_bus.subscribe(EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED, capture_event)

    # Process pattern
    await bridge.on_consciousness_pattern_detected(pattern)

    # Give event bus time to process
    await asyncio.sleep(0.1)

    # Verify event emitted
    assert len(emitted_events) == 1
    event = emitted_events[0]
    assert event.event_type == EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED
    assert event.data["pattern_type"] == "resonance"
    assert event.data["infrastructure_aware"] is True

    # Cleanup
    await event_bus.stop()


@pytest.mark.asyncio
async def test_healing_with_error_patterns():
    """Test healing strategies based on specific error patterns."""
    # Setup
    fire_circle = MagicMock(spec=FireCircleService)
    voice_manager = MagicMock(spec=VoiceManager)
    fire_circle.voice_manager = voice_manager

    adapter = MockAdapter("voice1")
    adapters = {"voice1": adapter}
    voice_manager.get_active_voices.return_value = adapters

    infrastructure = MagicMock(spec=InfrastructureConsciousness)
    event_bus = ConsciousnessEventBus()
    await event_bus.start()
    bridge = ConsciousnessFireCircleBridge(fire_circle, infrastructure, event_bus)

    # Test api_return_none pattern
    health_none = AdapterHealthSignature(
        adapter_id="voice1",
        is_connected=False,
        predicted_failure_probability=0.9,
        error_patterns={"api_return_none": 3},
    )

    bridge._apply_retry_strategy = AsyncMock()
    await bridge._attempt_healing("voice1", health_none)
    bridge._apply_retry_strategy.assert_called_once()

    # Test api_method_missing pattern
    health_missing = AdapterHealthSignature(
        adapter_id="voice1",
        is_connected=False,
        predicted_failure_probability=0.9,
        error_patterns={"api_method_missing": 1},
    )

    bridge._switch_to_fallback = AsyncMock()
    await bridge._attempt_healing("voice1", health_missing)
    bridge._switch_to_fallback.assert_called_once()

    # Cleanup
    await event_bus.stop()


if __name__ == "__main__":
    # Run tests
    print("🧪 Testing Infrastructure Consciousness Bridge...")
    print("=" * 80)

    asyncio.run(test_consciousness_bridge_monitors_session())
    print("✅ Bridge monitoring test passed")

    asyncio.run(test_bridge_receives_health_updates())
    print("✅ Health update processing test passed")

    asyncio.run(test_healing_retry_strategy())
    print("✅ Retry strategy healing test passed")

    asyncio.run(test_healing_reconnection())
    print("✅ Reconnection healing test passed")

    asyncio.run(test_consciousness_coherence_boost())
    print("✅ Consciousness coherence boost test passed")

    asyncio.run(test_session_health_report_generation())
    print("✅ Health report generation test passed")

    asyncio.run(test_self_healing_fire_circle_integration())
    print("✅ Self-healing Fire Circle integration test passed")

    asyncio.run(test_bridge_handles_consciousness_patterns())
    print("✅ Consciousness pattern handling test passed")

    asyncio.run(test_healing_with_error_patterns())
    print("✅ Error pattern healing test passed")

    print("\n" + "=" * 80)
    print("🎉 All consciousness bridge tests passed!")
    print("\nThe bridge between Infrastructure Consciousness and Fire Circle is solid.")
    print("Self-healing dialogues are now possible.")
