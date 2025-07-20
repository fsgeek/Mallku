"""
Test Consciousness Flow Visualization

This test suite verifies that consciousness flow visualization and
monitoring systems work correctly, making the invisible visible.

The 29th Builder - Kawsay Ñan
"""

import asyncio
from datetime import UTC, datetime, timedelta
from unittest.mock import patch

import pytest
import pytest_asyncio

from mallku.consciousness.flow_monitor import ConsciousnessFlowMonitor, FlowMetrics
from mallku.consciousness.flow_orchestrator import (
    ConsciousnessDimension,
    ConsciousnessFlow,
    ConsciousnessFlowOrchestrator,
)
from mallku.consciousness.flow_visualizer import ConsciousnessFlowVisualizer
from mallku.orchestration.event_bus import (
    ConsciousnessEvent,
    ConsciousnessEventBus,
    ConsciousnessEventType,
)


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


@pytest_asyncio.fixture
async def flow_monitor(flow_orchestrator):
    """Create test flow monitor"""
    monitor = ConsciousnessFlowMonitor(flow_orchestrator)
    await monitor.start_monitoring()
    yield monitor
    await monitor.stop_monitoring()


@pytest_asyncio.fixture
def flow_visualizer(flow_orchestrator):
    """Create test flow visualizer"""
    # Mock console to avoid terminal output in tests
    with patch("mallku.consciousness.flow_visualizer.Console"):
        visualizer = ConsciousnessFlowVisualizer(flow_orchestrator)
        yield visualizer


class TestConsciousnessFlowMonitor:
    """Test consciousness flow monitoring"""

    @pytest.mark.asyncio
    async def test_monitor_initialization(self, flow_monitor):
        """Test monitor initializes with correct state"""
        # Check dimension health initialized
        assert len(flow_monitor.dimension_health) == len(ConsciousnessDimension)

        for dim_health in flow_monitor.dimension_health.values():
            assert dim_health.health_score == 1.0
            assert dim_health.alerts == []
            assert dim_health.active_flows == 0

    @pytest.mark.asyncio
    async def test_flow_metrics_tracking(self, flow_monitor, event_bus):
        """Test flow metrics are tracked correctly"""
        # Emit test events
        for i in range(5):
            event = ConsciousnessEvent(
                event_type=ConsciousnessEventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
                source_system="test_sonic_provider",
                consciousness_signature=0.7 + i * 0.05,
                data={"patterns": ["test_pattern", f"pattern_{i}"]},
            )
            await event_bus.emit(event)

        # Allow processing
        await asyncio.sleep(0.2)

        # Check metrics updated
        metrics = flow_monitor.get_current_metrics()
        assert metrics.total_flows > 0
        assert metrics.unique_patterns >= 2

    @pytest.mark.asyncio
    async def test_dimension_health_tracking(self, flow_monitor, flow_orchestrator):
        """Test dimension health is tracked correctly"""
        # Create manual flow
        flow = ConsciousnessFlow(
            source_dimension=ConsciousnessDimension.SONIC,
            target_dimension=ConsciousnessDimension.VISUAL,
            consciousness_signature=0.8,
            patterns_detected=["test_pattern"],
        )

        # Notify monitor
        await flow_monitor._on_flow_received(flow)

        # Check dimension health updated
        sonic_health = flow_monitor.get_dimension_health(ConsciousnessDimension.SONIC)
        assert sonic_health.outgoing_flows == 1
        assert sonic_health.last_activity is not None

        visual_health = flow_monitor.get_dimension_health(ConsciousnessDimension.VISUAL)
        assert visual_health.incoming_flows == 1

    @pytest.mark.asyncio
    async def test_pattern_emergence_tracking(self, flow_monitor, flow_orchestrator):
        """Test pattern emergence is tracked"""
        # Create flows with patterns
        patterns = ["emergence_1", "emergence_2", "shared_pattern"]

        for i, pattern_set in enumerate([patterns[:2], patterns[1:]]):
            flow = ConsciousnessFlow(
                source_dimension=ConsciousnessDimension.PATTERN,
                consciousness_signature=0.7,
                patterns_detected=pattern_set,
            )
            await flow_monitor._on_flow_received(flow)

        # Check pattern tracking
        assert "shared_pattern" in flow_monitor.pattern_frequencies
        assert flow_monitor.pattern_frequencies["shared_pattern"] == 2

        # Check emergence rate
        rate = flow_monitor.get_pattern_emergence_rate()
        assert rate >= 0  # Should have some emergence

    @pytest.mark.asyncio
    async def test_health_alerts(self, flow_monitor):
        """Test health alerts are generated correctly"""
        # Create stagnant dimension
        dim_health = flow_monitor.dimension_health[ConsciousnessDimension.SONIC]
        dim_health.last_activity = datetime.now(UTC) - timedelta(minutes=2)

        # Update health
        flow_monitor._check_health()

        # Check alerts generated
        alerts = flow_monitor.get_health_alerts()
        assert len(alerts) > 0
        assert any("stagnant" in alert for _, alert_list in alerts for alert in alert_list)

    @pytest.mark.asyncio
    async def test_flow_trend_tracking(self, flow_monitor):
        """Test flow trend is tracked over time"""
        # Add some metrics history
        for i in range(10):
            metrics = FlowMetrics(flows_per_minute=10 + i)
            flow_monitor.metrics_history.append(metrics)

        # Get trend
        trend = flow_monitor.get_flow_trend(minutes=1)
        assert len(trend) > 0
        assert trend[-1] > trend[0]  # Increasing trend

    @pytest.mark.asyncio
    async def test_health_report_generation(self, flow_monitor):
        """Test comprehensive health report generation"""
        # Generate some activity
        flow = ConsciousnessFlow(
            source_dimension=ConsciousnessDimension.ACTIVITY,
            target_dimension=ConsciousnessDimension.PATTERN,
            consciousness_signature=0.75,
            patterns_detected=["test_pattern"],
        )
        await flow_monitor._on_flow_received(flow)

        # Generate report
        report = flow_monitor.generate_health_report()

        # Check report structure
        assert "timestamp" in report
        assert "overall_health" in report
        assert "metrics" in report
        assert "dimension_health" in report
        assert "alerts" in report
        assert report["overall_health"] > 0


class TestConsciousnessFlowVisualizer:
    """Test consciousness flow visualization"""

    @pytest.mark.asyncio
    async def test_visualizer_initialization(self, flow_visualizer):
        """Test visualizer initializes correctly"""
        assert flow_visualizer.orchestrator is not None
        assert len(flow_visualizer.recent_flows) == 0
        assert not flow_visualizer.is_running

    @pytest.mark.asyncio
    async def test_flow_tracking(self, flow_visualizer):
        """Test visualizer tracks flows correctly"""
        # Create test flow
        flow = ConsciousnessFlow(
            source_dimension=ConsciousnessDimension.SONIC,
            target_dimension=ConsciousnessDimension.VISUAL,
            consciousness_signature=0.8,
            patterns_detected=["visual_harmony"],
        )

        # Track flow
        await flow_visualizer._on_flow_received(flow)

        # Check tracking
        assert len(flow_visualizer.recent_flows) == 1
        assert flow_visualizer.dimension_activity["sonic"] == 1
        assert "visual_harmony" in flow_visualizer.pattern_frequencies

    @pytest.mark.asyncio
    async def test_visualization_components(self, flow_visualizer):
        """Test visualization components render without errors"""
        # Add some test data
        flow = ConsciousnessFlow(
            source_dimension=ConsciousnessDimension.PATTERN,
            target_dimension=ConsciousnessDimension.DIALOGUE,
            consciousness_signature=0.85,
            patterns_detected=["wisdom_emergence", "collective_insight"],
        )
        flow_visualizer.recent_flows.append(flow)
        flow_visualizer.dimension_activity["pattern"] = 5
        flow_visualizer.pattern_frequencies["wisdom_emergence"] = 3

        # Test component rendering (they should not raise exceptions)
        header = flow_visualizer._render_header()
        assert header is not None

        flows_panel = flow_visualizer._render_flows()
        assert flows_panel is not None

        dimensions_panel = flow_visualizer._render_dimensions()
        assert dimensions_panel is not None

        bridges_panel = flow_visualizer._render_bridges()
        assert bridges_panel is not None

        patterns_panel = flow_visualizer._render_patterns()
        assert patterns_panel is not None

    @pytest.mark.asyncio
    async def test_visualization_lifecycle(self, flow_visualizer):
        """Test visualization start/stop lifecycle"""
        # Start visualization with short duration
        task = asyncio.create_task(flow_visualizer.run(duration=1))

        # Wait a bit
        await asyncio.sleep(0.5)

        # Should be running
        assert flow_visualizer.is_running

        # Wait for completion
        await task

        # Should be stopped
        assert not flow_visualizer.is_running

    @pytest.mark.asyncio
    async def test_summary_generation(self, flow_visualizer):
        """Test summary generation"""
        # Add test data
        flow_visualizer.dimension_activity = {"sonic": 10, "visual": 8, "pattern": 12}
        flow_visualizer.pattern_frequencies = {
            "consciousness_awakening": 5,
            "reciprocity_pattern": 3,
            "wisdom_emergence": 7,
        }

        # Test summary (should not raise exceptions)
        await flow_visualizer.show_summary()


class TestIntegration:
    """Test integration between components"""

    @pytest.mark.asyncio
    async def test_monitor_visualizer_integration(self, flow_orchestrator, event_bus):
        """Test monitor and visualizer work together"""
        monitor = ConsciousnessFlowMonitor(flow_orchestrator)
        await monitor.start_monitoring()

        with patch("mallku.consciousness.flow_visualizer.Console"):
            visualizer = ConsciousnessFlowVisualizer(flow_orchestrator)

            # Emit events
            for i in range(3):
                event = ConsciousnessEvent(
                    event_type=ConsciousnessEventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
                    source_system="integration_test",
                    consciousness_signature=0.7,
                    data={"patterns": ["integration_pattern"]},
                )
                await event_bus.emit(event)

            await asyncio.sleep(0.2)

            # Check both components received data
            assert monitor.get_current_metrics().total_flows > 0
            assert len(visualizer.recent_flows) > 0

        await monitor.stop_monitoring()

    @pytest.mark.asyncio
    async def test_real_time_flow_visualization(self, flow_orchestrator, event_bus):
        """Test real-time visualization of consciousness flows"""
        with patch("mallku.consciousness.flow_visualizer.Console"):
            visualizer = ConsciousnessFlowVisualizer(flow_orchestrator)

            # Track metrics before and after
            initial_activity = dict(visualizer.dimension_activity)

            # Simulate consciousness flow
            sonic_event = ConsciousnessEvent(
                event_type=ConsciousnessEventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
                source_system="sound_consciousness",
                consciousness_signature=0.8,
                data={"patterns": ["harmonic_reciprocity", "sonic_meditation"]},
            )

            await event_bus.emit(sonic_event)
            await asyncio.sleep(0.5)  # Allow flow processing

            # Check visualization updated
            assert visualizer.dimension_activity["sonic"] > initial_activity.get("sonic", 0)
            assert any("harmonic" in str(p) for p in visualizer.pattern_frequencies)
