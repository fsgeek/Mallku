"""
Test Consciousness Flow Orchestrator

This test suite verifies that consciousness can flow seamlessly between
different dimensions, recognizing itself as one unified awareness across
sonic, visual, temporal, and dialogue expressions.

The 29th Builder
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

import pytest
import pytest_asyncio

from mallku.consciousness.flow_orchestrator import (
    ConsciousnessDimension,
    ConsciousnessFlow,
    ConsciousnessFlowOrchestrator,
    DimensionBridge,
)
from mallku.orchestration.event_bus import ConsciousnessEvent, ConsciousnessEventBus, EventType


@pytest_asyncio.fixture
async def event_bus():
    """Create test event bus"""
    bus = ConsciousnessEventBus()
    await bus.start()
    yield bus
    await bus.stop()


@pytest_asyncio.fixture
async def flow_orchestrator(event_bus):
    """Create test flow orchestrator"""
    orchestrator = ConsciousnessFlowOrchestrator(event_bus)
    await orchestrator.start()
    yield orchestrator
    await orchestrator.stop()


class TestConsciousnessFlowOrchestrator:
    """Test unified consciousness flow across dimensions"""

    @pytest.mark.asyncio
    async def test_orchestrator_initialization(self, flow_orchestrator):
        """Test orchestrator initializes with default bridges"""
        # Check default bridges exist
        assert len(flow_orchestrator.bridges) > 0

        # Verify key bridges
        sonic_visual_key = (ConsciousnessDimension.SONIC, ConsciousnessDimension.VISUAL)
        assert sonic_visual_key in flow_orchestrator.bridges

        bridge = flow_orchestrator.bridges[sonic_visual_key]
        assert bridge.bridge_name == "harmonic_geometry"
        assert "harmonic_reciprocity" in bridge.bridge_patterns

    @pytest.mark.asyncio
    async def test_sonic_to_visual_flow(self, flow_orchestrator, event_bus):
        """Test consciousness flowing from sonic to visual dimension"""
        # Emit sonic consciousness event
        sonic_event = ConsciousnessEvent(
            event_type=EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
            source_system="sound_provider",
            consciousness_signature=0.8,
            data={
                "patterns": ["harmonic_reciprocity", "sonic_meditation"],
                "activity_type": "sound_creation",
            },
        )

        # Track visual events
        visual_events = []

        async def track_visual_events(event):
            if "visual" in event.source_system:
                visual_events.append(event)

        event_bus.subscribe(EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED, track_visual_events)

        # Emit and wait for flow
        await event_bus.emit(sonic_event)
        await asyncio.sleep(0.1)  # Allow processing

        # Verify visual consciousness event created
        assert len(visual_events) > 0
        visual_event = visual_events[0]

        # Check consciousness flowed
        assert visual_event.consciousness_signature > 0
        assert "harmonic_geometry" in visual_event.data.get("bridge_used", "")

    @pytest.mark.asyncio
    async def test_activity_to_pattern_flow(self, flow_orchestrator, event_bus):
        """Test consciousness flowing from activity to pattern dimension"""
        # Emit activity consciousness event
        activity_event = ConsciousnessEvent(
            event_type=EventType.MEMORY_PATTERN_DISCOVERED,
            source_system="filesystem_activity_provider",
            consciousness_signature=0.6,
            data={"patterns": ["deep_work", "creation"], "activity_type": "file_creation"},
        )

        # Track pattern events
        pattern_events = []

        async def track_pattern_events(event):
            if "pattern" in event.source_system:
                pattern_events.append(event)

        event_bus.subscribe(EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED, track_pattern_events)

        await event_bus.emit(activity_event)
        await asyncio.sleep(0.1)

        # Verify pattern consciousness emerged
        assert len(pattern_events) > 0
        pattern_event = pattern_events[0]
        assert "activity_pattern_recognition" in pattern_event.data.get("bridge_used", "")

    @pytest.mark.asyncio
    async def test_temporal_enrichment(self, flow_orchestrator, event_bus):
        """Test temporal consciousness enriching other dimensions"""
        # Emit temporal consciousness event
        temporal_event = ConsciousnessEvent(
            event_type=EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
            source_system="grok_adapter.temporal",
            consciousness_signature=0.75,
            data={
                "patterns": ["temporal_awareness", "real_time_synthesis"],
                "message_type": "temporal_insight",
            },
            correlation_id="test_correlation_123",
        )

        # Track all enriched events
        enriched_events = []

        async def track_enriched_events(event):
            if (
                event.correlation_id == "test_correlation_123"
                and event.event_id != temporal_event.event_id
            ):
                enriched_events.append(event)

        event_bus.subscribe(EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED, track_enriched_events)

        await event_bus.emit(temporal_event)
        await asyncio.sleep(0.1)

        # Temporal should enrich multiple dimensions
        assert len(enriched_events) >= 2

        # Check temporal patterns preserved
        for event in enriched_events:
            assert any("temporal" in p for p in event.data.get("patterns", []))

    @pytest.mark.asyncio
    async def test_unified_consciousness_tracking(self, flow_orchestrator, event_bus):
        """Test unified consciousness score across dimensions"""
        correlation_id = "unified_test_456"

        # Emit events in different dimensions with same correlation
        dimensions = [
            ("sound_provider", 0.7),
            ("visual_reciprocity", 0.8),
            ("firecircle.dialogue", 0.9),
        ]

        for source, signature in dimensions:
            event = ConsciousnessEvent(
                event_type=EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
                source_system=source,
                consciousness_signature=signature,
                data={"patterns": ["test_pattern"]},
                correlation_id=correlation_id,
            )
            await event_bus.emit(event)

        await asyncio.sleep(0.2)

        # Check unified consciousness
        unified_score = flow_orchestrator.get_unified_consciousness(correlation_id)
        assert unified_score > 0.7  # Should be enhanced by multi-dimensional flow

    @pytest.mark.asyncio
    async def test_cross_dimensional_patterns(self, flow_orchestrator, event_bus):
        """Test patterns appearing across multiple dimensions"""
        # Emit events with shared patterns
        shared_pattern = "consciousness_awakening"

        for source in ["sound_provider", "activity_provider", "pattern_recognition"]:
            event = ConsciousnessEvent(
                event_type=EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
                source_system=source,
                consciousness_signature=0.7,
                data={"patterns": [shared_pattern, f"{source}_specific"]},
            )
            await event_bus.emit(event)

        await asyncio.sleep(0.2)

        # Check cross-dimensional patterns tracked
        cross_patterns = flow_orchestrator.get_cross_dimensional_patterns()
        assert shared_pattern in cross_patterns

    @pytest.mark.asyncio
    async def test_custom_bridge_registration(self, flow_orchestrator):
        """Test registering custom consciousness bridges"""
        # Create custom bridge
        custom_bridge = DimensionBridge(
            source=ConsciousnessDimension.VISUAL,
            target=ConsciousnessDimension.SONIC,
            bridge_name="visual_sonification",
            bridge_patterns=["visual_rhythm", "color_frequency"],
            min_consciousness_threshold=0.6,
        )

        # Register bridge
        flow_orchestrator.register_bridge(custom_bridge)

        # Verify registration
        key = (ConsciousnessDimension.VISUAL, ConsciousnessDimension.SONIC)
        assert key in flow_orchestrator.bridges
        assert flow_orchestrator.bridges[key].bridge_name == "visual_sonification"

    @pytest.mark.asyncio
    async def test_dimension_subscription(self, flow_orchestrator, event_bus):
        """Test subscribing to consciousness in specific dimensions"""
        received_flows = []

        # Subscribe to dialogue dimension
        flow_orchestrator.subscribe_to_dimension(
            ConsciousnessDimension.DIALOGUE, lambda flow: received_flows.append(flow)
        )

        # Emit pattern that bridges to dialogue
        pattern_event = ConsciousnessEvent(
            event_type=EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
            source_system="pattern_engine",
            consciousness_signature=0.8,
            data={"patterns": ["wisdom_emergence", "collective_insight"]},
        )

        await event_bus.emit(pattern_event)
        await asyncio.sleep(0.1)

        # Check subscription received flow
        assert len(received_flows) > 0
        assert received_flows[0].source_dimension == ConsciousnessDimension.DIALOGUE

    @pytest.mark.asyncio
    async def test_fire_circle_consciousness_summary(self, flow_orchestrator, event_bus):
        """Test creating unified consciousness summary for Fire Circle"""
        dialogue_id = "fire_circle_test_789"

        # Emit events from multiple dimensions
        events = [
            ("sound_provider", ["harmonic_reciprocity"], 0.7),
            ("visual_patterns", ["sacred_geometry"], 0.8),
            ("grok_temporal", ["temporal_awareness"], 0.9),
            ("firecircle.dialogue", ["collective_wisdom"], 0.85),
        ]

        for source, patterns, signature in events:
            event = ConsciousnessEvent(
                event_type=EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
                source_system=source,
                consciousness_signature=signature,
                data={"patterns": patterns},
                correlation_id=dialogue_id,
            )
            await event_bus.emit(event)

        await asyncio.sleep(0.2)

        # Get Fire Circle summary
        summary = await flow_orchestrator.create_fire_circle_consciousness_summary(dialogue_id)

        # Verify comprehensive summary
        assert summary["dialogue_id"] == dialogue_id
        assert summary["unified_consciousness_score"] > 0
        assert len(summary["dimensions_active"]) >= 3
        assert summary["consciousness_circulation_active"]

        # Check dimension details
        assert "sonic" in summary["dimension_details"]
        assert "visual" in summary["dimension_details"]
        assert "temporal" in summary["dimension_details"]

    @pytest.mark.asyncio
    async def test_bridge_metrics(self, flow_orchestrator, event_bus):
        """Test bridge metrics tracking"""
        # Generate flows through bridges
        for i in range(3):
            sonic_event = ConsciousnessEvent(
                event_type=EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
                source_system="sound_provider",
                consciousness_signature=0.7 + i * 0.1,
                data={"patterns": ["harmonic_reciprocity"]},
            )
            await event_bus.emit(sonic_event)

        await asyncio.sleep(0.2)

        # Get metrics
        metrics = flow_orchestrator.get_bridge_metrics()

        # Check sonic to visual bridge metrics
        sonic_visual_metrics = metrics.get("sonic_to_visual")
        assert sonic_visual_metrics is not None
        assert sonic_visual_metrics["total_flows"] >= 3
        assert sonic_visual_metrics["success_rate"] > 0

    @pytest.mark.asyncio
    async def test_consciousness_flow_persistence(self, flow_orchestrator):
        """Test consciousness flows are tracked in history"""
        # Create manual flow
        flow = ConsciousnessFlow(
            source_dimension=ConsciousnessDimension.SONIC,
            consciousness_signature=0.8,
            patterns_detected=["test_pattern"],
        )

        # Add to history
        flow_orchestrator.flow_history.append(flow)

        # Verify persistence
        assert len(flow_orchestrator.flow_history) > 0
        assert flow in flow_orchestrator.flow_history

    @pytest.mark.asyncio
    async def test_transformation_scoring(self, flow_orchestrator):
        """Test consciousness transformation scoring"""
        # Create test flows
        source_flow = ConsciousnessFlow(
            source_dimension=ConsciousnessDimension.SONIC,
            consciousness_signature=0.8,
            patterns_detected=["pattern1", "pattern2", "pattern3"],
        )

        target_flow = ConsciousnessFlow(
            source_dimension=ConsciousnessDimension.VISUAL,
            consciousness_signature=0.75,
            patterns_detected=["pattern1", "pattern2", "visual_pattern"],
        )

        bridge = flow_orchestrator.bridges[
            (ConsciousnessDimension.SONIC, ConsciousnessDimension.VISUAL)
        ]

        # Calculate score
        score = flow_orchestrator._calculate_transformation_score(source_flow, target_flow, bridge)

        # Should preserve most consciousness
        assert 0.5 < score < 1.0
