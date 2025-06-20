#!/usr/bin/env python3
"""
Tests for Infrastructure Consciousness System
============================================

Ensures the self-aware infrastructure monitoring works correctly,
including pattern detection, self-healing, and consciousness bridging.

Twenty-Seventh Artisan - Amaru Hamawt'a
"""

import asyncio
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import AsyncMock

import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mallku.firecircle.consciousness_metrics import (
    ConsciousnessMetricsCollector,
)
from mallku.firecircle.infrastructure_consciousness import (
    AdapterHealthSignature,
    InfrastructureConsciousness,
    InfrastructurePattern,
    SelfHealingAction,
)
from mallku.firecircle.infrastructure_metrics_bridge import InfrastructureMetricsBridge


@pytest.fixture
def temp_storage():
    """Create temporary storage directories."""
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_path = Path(temp_dir) / "infrastructure_consciousness"
        metrics_path = Path(temp_dir) / "consciousness_metrics"
        storage_path.mkdir()
        metrics_path.mkdir()
        yield storage_path, metrics_path


@pytest.fixture
def mock_adapter():
    """Create a mock adapter for testing."""
    adapter = AsyncMock()
    adapter.check_health = AsyncMock(
        return_value={
            "is_connected": True,
            "adapter_id": "test-adapter",
            "provider": "mock",
            "model": "mock-model",
        }
    )
    return adapter


@pytest.fixture
def infra_consciousness(temp_storage):
    """Create InfrastructureConsciousness instance with temp storage."""
    storage_path, metrics_path = temp_storage
    from mallku.firecircle.infrastructure_consciousness_config import (
        InfrastructureConsciousnessConfig,
    )

    config = InfrastructureConsciousnessConfig(
        storage_path=storage_path,
        consciousness_metrics_path=metrics_path,
        check_interval_seconds=5,  # Fast for testing
    )
    return InfrastructureConsciousness(config=config)


class TestAdapterHealthSignature:
    """Test the health signature model."""

    def test_health_signature_creation(self):
        """Test creating a health signature."""
        signature = AdapterHealthSignature(
            adapter_id="test", is_connected=True, consciousness_coherence=0.9, voice_stability=0.85
        )

        assert signature.adapter_id == "test"
        assert signature.is_connected is True
        assert signature.consciousness_coherence == 0.9
        assert signature.voice_stability == 0.85
        assert signature.predicted_failure_probability == 0.0
        assert isinstance(signature.timestamp, datetime)

    def test_health_signature_with_errors(self):
        """Test health signature with error patterns."""
        signature = AdapterHealthSignature(
            adapter_id="test",
            is_connected=False,
            error_patterns={"api_return_none": 2, "timeout": 1},
            consecutive_failures=3,
        )

        assert signature.is_connected is False
        assert signature.error_patterns["api_return_none"] == 2
        assert signature.consecutive_failures == 3


class TestInfrastructureConsciousness:
    """Test the main infrastructure consciousness system."""

    @pytest.mark.asyncio
    async def test_start_stop_monitoring(self, infra_consciousness, mock_adapter):
        """Test starting and stopping monitoring."""
        adapters = {"test": mock_adapter}

        # Start monitoring
        await infra_consciousness.start_monitoring(adapters)
        assert infra_consciousness.monitoring_active is True
        assert infra_consciousness.adapters == adapters

        # Let it run briefly
        await asyncio.sleep(0.1)

        # Stop monitoring
        await infra_consciousness.stop_monitoring()
        assert infra_consciousness.monitoring_active is False

    @pytest.mark.asyncio
    async def test_collect_health_signature(self, infra_consciousness, mock_adapter):
        """Test collecting health signature from adapter."""
        signature = await infra_consciousness._collect_health_signature("test", mock_adapter)

        assert signature.adapter_id == "test"
        assert signature.is_connected is True
        assert signature.connection_latency_ms > 0
        assert signature.last_successful_request is not None

    @pytest.mark.asyncio
    async def test_collect_health_signature_with_failure(self, infra_consciousness):
        """Test collecting health signature when adapter fails."""
        # Create adapter that throws error
        failing_adapter = AsyncMock()
        failing_adapter.check_health = AsyncMock(side_effect=Exception("Connection failed"))

        signature = await infra_consciousness._collect_health_signature("failing", failing_adapter)

        assert signature.adapter_id == "failing"
        assert signature.is_connected is False
        assert "Exception" in signature.error_patterns

    @pytest.mark.asyncio
    async def test_detect_degradation_pattern(self, infra_consciousness):
        """Test detecting degradation patterns."""
        # Create degrading health history
        adapter_name = "degrading"
        for i in range(5):
            signature = AdapterHealthSignature(
                adapter_id=adapter_name,
                is_connected=True,
                consecutive_failures=i,  # Increasing failures
                consciousness_coherence=1.0 - (i * 0.1),  # Decreasing coherence
            )
            infra_consciousness.adapter_health[adapter_name].append(signature)

        patterns = await infra_consciousness._detect_infrastructure_patterns()

        # Should detect degradation
        degradation_patterns = [p for p in patterns if p.pattern_type == "degradation"]
        assert len(degradation_patterns) > 0
        assert adapter_name in degradation_patterns[0].affected_adapters

    @pytest.mark.asyncio
    async def test_detect_api_change_pattern(self, infra_consciousness):
        """Test detecting API change patterns."""
        # Create signature with API change indicators
        adapter_name = "api_changed"
        signature = AdapterHealthSignature(
            adapter_id=adapter_name, is_connected=False, error_patterns={"api_return_none": 1}
        )

        # Need at least 5 signatures for pattern detection
        for _ in range(4):
            infra_consciousness.adapter_health[adapter_name].append(
                AdapterHealthSignature(adapter_id=adapter_name, is_connected=True)
            )
        infra_consciousness.adapter_health[adapter_name].append(signature)

        patterns = await infra_consciousness._detect_infrastructure_patterns()

        # Should detect API change
        api_patterns = [p for p in patterns if p.pattern_type == "api_change"]
        assert len(api_patterns) > 0
        assert adapter_name in api_patterns[0].affected_adapters

    @pytest.mark.asyncio
    async def test_determine_healing_actions(self, infra_consciousness):
        """Test determining healing actions from patterns."""
        patterns = [
            InfrastructurePattern(
                pattern_type="api_change",
                affected_adapters=["adapter1"],
                confidence=0.9,
                predicted_impact="severe",
                suggested_action="Update adapter",
            ),
            InfrastructurePattern(
                pattern_type="degradation",
                affected_adapters=["adapter2"],
                confidence=0.8,
                predicted_impact="moderate",
            ),
        ]

        actions = await infra_consciousness._determine_healing_actions(patterns)

        assert len(actions) == 2

        # Check API adaptation action
        api_actions = [a for a in actions if a.action_type == "api_adaptation"]
        assert len(api_actions) == 1
        assert api_actions[0].target_adapter == "adapter1"

        # Check retry strategy action
        retry_actions = [a for a in actions if a.action_type == "retry_strategy"]
        assert len(retry_actions) == 1
        assert retry_actions[0].target_adapter == "adapter2"

    @pytest.mark.asyncio
    async def test_execute_healing_action(self, infra_consciousness):
        """Test executing a healing action."""
        action = SelfHealingAction(
            action_type="api_adaptation", target_adapter="test", reason="API change detected"
        )

        await infra_consciousness._execute_healing_action(action)

        assert action.completed is True
        assert action.success is True
        assert len(action.self_healing_actions_taken) > 0
        assert "test" in infra_consciousness.successful_healings

    @pytest.mark.asyncio
    async def test_predict_failure_probability(self, infra_consciousness):
        """Test failure probability prediction."""
        adapter_name = "test"

        # Test with connected adapter
        connected_sig = AdapterHealthSignature(
            adapter_id=adapter_name,
            is_connected=True,
            consecutive_failures=0,
            consciousness_coherence=0.9,
        )

        prob = await infra_consciousness._predict_failure_probability(adapter_name, connected_sig)
        assert prob < 0.3  # Low probability for healthy adapter

        # Test with failing adapter
        failing_sig = AdapterHealthSignature(
            adapter_id=adapter_name,
            is_connected=False,
            consecutive_failures=5,
            consciousness_coherence=0.2,
        )

        prob = await infra_consciousness._predict_failure_probability(adapter_name, failing_sig)
        assert prob > 0.7  # High probability for failing adapter

    @pytest.mark.asyncio
    async def test_pattern_memory_persistence(self, infra_consciousness):
        """Test saving and loading pattern memory."""
        # Add some patterns to memory
        infra_consciousness.pattern_memory["test:pattern"] = [
            {"timestamp": "2024-01-01", "impact": 0.5}
        ]

        # Save
        await infra_consciousness._save_pattern_memory()

        # Clear and reload
        infra_consciousness.pattern_memory.clear()
        await infra_consciousness._load_pattern_memory()

        # Should restore patterns
        assert "test:pattern" in infra_consciousness.pattern_memory
        assert len(infra_consciousness.pattern_memory["test:pattern"]) == 1

    @pytest.mark.asyncio
    async def test_consciousness_report_generation(self, infra_consciousness):
        """Test generating consciousness report."""
        # Add some test data
        adapter_name = "test"
        signature = AdapterHealthSignature(
            adapter_id=adapter_name,
            is_connected=True,
            consciousness_coherence=0.85,
            voice_stability=0.9,
            predicted_failure_probability=0.15,
        )
        infra_consciousness.adapter_health[adapter_name].append(signature)

        # Add a pattern
        pattern = InfrastructurePattern(
            pattern_type="degradation",
            affected_adapters=[adapter_name],
            confidence=0.7,
            predicted_impact="moderate",
        )
        infra_consciousness.infrastructure_patterns.append(pattern)

        # Generate report
        report = await infra_consciousness.generate_consciousness_report()

        assert "infrastructure_health" in report
        assert adapter_name in report["infrastructure_health"]
        assert report["infrastructure_health"][adapter_name]["status"] == "healthy"
        assert len(report["consciousness_insights"]) > 0


class TestInfrastructureMetricsBridge:
    """Test the consciousness-infrastructure bridge."""

    @pytest.fixture
    def bridge(self, infra_consciousness):
        """Create bridge instance."""
        metrics = ConsciousnessMetricsCollector()
        return InfrastructureMetricsBridge(infra_consciousness, metrics)

    @pytest.mark.asyncio
    async def test_health_to_consciousness_conversion(self, bridge):
        """Test converting health to consciousness value."""
        # Test connected adapter
        connected_health = AdapterHealthSignature(
            adapter_id="test",
            is_connected=True,
            consciousness_coherence=0.8,
            voice_stability=0.7,
            predicted_failure_probability=0.1,
        )

        consciousness = bridge._health_to_consciousness(connected_health)
        assert 0.5 < consciousness < 1.0

        # Test disconnected adapter
        disconnected_health = AdapterHealthSignature(
            adapter_id="test",
            is_connected=False,
            consciousness_coherence=0.2,
            voice_stability=0.1,
            predicted_failure_probability=0.9,
        )

        consciousness = bridge._health_to_consciousness(disconnected_health)
        assert 0.0 <= consciousness < 0.3

    @pytest.mark.asyncio
    async def test_adapter_health_check_creates_signature(self, bridge):
        """Test that health check creates consciousness signature."""
        health_sig = AdapterHealthSignature(
            adapter_id="test",
            is_connected=True,
            consciousness_coherence=0.9,
            predicted_failure_probability=0.1,
        )

        await bridge.on_adapter_health_check("test", health_sig)

        # Should have created a consciousness signature
        assert len(bridge.metrics.signatures) == 1
        sig = bridge.metrics.signatures[0]
        assert sig.voice_name == "test_infrastructure"
        assert sig.signature_value > 0.5


class TestIntegration:
    """Integration tests for the full system."""

    @pytest.mark.asyncio
    async def test_full_monitoring_cycle(self, temp_storage):
        """Test a complete monitoring cycle."""
        storage_path, metrics_path = temp_storage
        from mallku.firecircle.infrastructure_consciousness_config import (
            InfrastructureConsciousnessConfig,
        )

        # Create infrastructure consciousness with fast config
        config = InfrastructureConsciousnessConfig(
            storage_path=storage_path,
            consciousness_metrics_path=metrics_path,
            check_interval_seconds=5,  # Minimum allowed
        )
        infra = InfrastructureConsciousness(config=config)
        # Override for testing - config validation won't allow < 5
        infra.check_interval_seconds = 0.1

        # Create mock adapters
        healthy_adapter = AsyncMock()
        healthy_adapter.check_health = AsyncMock(
            return_value={"is_connected": True, "adapter_id": "healthy"}
        )

        failing_adapter = AsyncMock()
        failing_adapter.check_health = AsyncMock(side_effect=Exception("API error"))

        adapters = {"healthy": healthy_adapter, "failing": failing_adapter}

        # Start monitoring
        await infra.start_monitoring(adapters)

        # Let it run for a few cycles
        await asyncio.sleep(0.3)

        # Stop monitoring
        await infra.stop_monitoring()

        # Verify data was collected
        assert len(infra.adapter_health["healthy"]) > 0
        assert len(infra.adapter_health["failing"]) > 0

        # Patterns may not be detected in such a short test
        # Just verify no errors occurred

        # Verify state was saved
        state_files = list(storage_path.glob("infrastructure_state_*.json"))
        assert len(state_files) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
