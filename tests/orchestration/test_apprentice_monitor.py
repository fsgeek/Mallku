"""
Tests for Apprentice Lifecycle Monitor

These tests ensure the monitoring system correctly tracks apprentice
lifecycles and provides accurate observability data.

Created by: 69th Guardian
"""

import asyncio
from datetime import UTC, datetime, timedelta
from unittest.mock import patch

import pytest

from mallku.orchestration.loom.apprentice_monitor import (
    ApprenticeLifecycleEvent,
    ApprenticeMonitor,
    ApprenticeState,
)


@pytest.fixture
async def monitor():
    """Create a monitor instance for testing"""
    monitor = ApprenticeMonitor(
        persistence_enabled=False, metrics_interval=1, health_check_interval=1
    )
    yield monitor
    await monitor.shutdown()


@pytest.mark.asyncio
async def test_register_spawn(monitor):
    """Test registering a new apprentice spawn"""
    apprentice_id = "test-001"
    task_id = "T001"
    ceremony_id = "ceremony-001"
    container_name = "test-container"

    record = await monitor.register_spawn(apprentice_id, task_id, ceremony_id, container_name)

    assert apprentice_id in monitor.active_apprentices
    assert record.apprentice_id == apprentice_id
    assert record.task_id == task_id
    assert record.ceremony_id == ceremony_id
    assert record.container_name == container_name
    assert record.current_state == ApprenticeState.INITIALIZING
    assert len(record.events) == 1
    assert record.events[0].event_type == "spawn"


@pytest.mark.asyncio
async def test_state_transitions(monitor):
    """Test state transition tracking"""
    apprentice_id = "test-002"
    await monitor.register_spawn(apprentice_id, "T001", "ceremony-001", "container")

    # Test state transitions
    states = [
        ApprenticeState.READY,
        ApprenticeState.WORKING,
        ApprenticeState.COMPLETING,
        ApprenticeState.COMPLETED,
    ]

    for state in states:
        await monitor.update_state(apprentice_id, state)

    record = monitor.active_apprentices[apprentice_id]
    assert record.current_state == ApprenticeState.COMPLETED
    assert len(record.states_history) == len(states) + 1  # +1 for initial state
    assert len(record.events) == len(states) + 1  # +1 for spawn event

    # Verify state change events
    state_change_events = [e for e in record.events if e.event_type == "state_change"]
    assert len(state_change_events) == len(states)


@pytest.mark.asyncio
async def test_timing_metrics(monitor):
    """Test timing metric calculations"""
    apprentice_id = "test-003"
    await monitor.register_spawn(apprentice_id, "T001", "ceremony-001", "container")

    # Wait a bit then mark as ready
    await asyncio.sleep(0.1)
    await monitor.update_state(apprentice_id, ApprenticeState.READY)

    record = monitor.active_apprentices[apprentice_id]
    assert record.metrics.container_startup_time > 0
    assert record.metrics.container_startup_time < 1  # Should be ~0.1s

    # Start working
    await monitor.update_state(apprentice_id, ApprenticeState.WORKING)
    await asyncio.sleep(0.1)

    # Complete
    await monitor.update_state(apprentice_id, ApprenticeState.COMPLETED)
    assert record.metrics.task_execution_time > 0
    assert record.metrics.task_execution_time < 1


@pytest.mark.asyncio
async def test_metrics_recording(monitor):
    """Test performance metrics recording"""
    apprentice_id = "test-004"
    await monitor.register_spawn(apprentice_id, "T001", "ceremony-001", "container")

    metrics = {
        "memory_mb": 512.5,
        "cpu_percent": 75.3,
        "khipu_updates": 5,
        "log_lines": 150,
    }

    await monitor.record_metrics(apprentice_id, metrics)

    record = monitor.active_apprentices[apprentice_id]
    assert record.metrics.memory_usage_mb == 512.5
    assert record.metrics.cpu_usage_percent == 75.3
    assert record.metrics.khipu_updates_count == 5
    assert record.metrics.log_lines_generated == 150


@pytest.mark.asyncio
async def test_error_recording(monitor):
    """Test error and warning recording"""
    apprentice_id = "test-005"
    await monitor.register_spawn(apprentice_id, "T001", "ceremony-001", "container")

    # Record errors
    await monitor.record_error(apprentice_id, "Test error 1")
    await monitor.record_error(apprentice_id, "Test error 2")

    # Record warnings
    await monitor.record_error(apprentice_id, "Test warning 1", error_type="warning")
    await monitor.record_error(apprentice_id, "Test warning 2", error_type="warning")

    record = monitor.active_apprentices[apprentice_id]
    assert record.metrics.errors_encountered == 2
    assert record.metrics.warnings_encountered == 2
    assert record.error_message == "Test error 2"  # Last error


@pytest.mark.asyncio
async def test_complete_monitoring(monitor):
    """Test completing monitoring for an apprentice"""
    apprentice_id = "test-006"
    await monitor.register_spawn(apprentice_id, "T001", "ceremony-001", "container")
    await monitor.update_state(apprentice_id, ApprenticeState.COMPLETED)

    final_output = "Task completed successfully"
    final_record = await monitor.complete_monitoring(apprentice_id, final_output)

    assert apprentice_id not in monitor.active_apprentices
    assert final_record.final_output == final_output
    assert final_record.events[-1].event_type == "cleanup"
    assert final_record.events[-1].new_state == ApprenticeState.CLEANED


@pytest.mark.asyncio
async def test_ceremony_metrics(monitor):
    """Test ceremony-wide metrics aggregation"""
    ceremony_id = "ceremony-007"

    # Create multiple apprentices
    apprentices = [
        ("app-001", "T001", 300, 50, ApprenticeState.COMPLETED, 0),
        ("app-002", "T002", 400, 60, ApprenticeState.WORKING, 0),
        ("app-003", "T003", 500, 70, ApprenticeState.FAILED, 2),
    ]

    for app_id, task_id, memory, cpu, state, errors in apprentices:
        await monitor.register_spawn(app_id, task_id, ceremony_id, f"container-{app_id}")
        await monitor.update_state(app_id, state)
        await monitor.record_metrics(app_id, {"memory_mb": memory, "cpu_percent": cpu})
        for _ in range(errors):
            await monitor.record_error(app_id, "Test error")

    metrics = await monitor.get_ceremony_metrics(ceremony_id)

    assert metrics["total_apprentices"] == 3
    assert metrics["active_apprentices"] == 1  # Only WORKING
    assert metrics["completed_apprentices"] == 1
    assert metrics["failed_apprentices"] == 1
    assert metrics["total_memory_mb"] == 1200  # 300 + 400 + 500
    assert metrics["average_cpu_percent"] == 60  # (50 + 60 + 70) / 3
    assert metrics["total_errors"] == 2


@pytest.mark.asyncio
async def test_monitor_background_task(monitor):
    """Test background monitoring task"""
    apprentice_id = "test-008"
    await monitor.register_spawn(apprentice_id, "T001", "ceremony-001", "container")

    # Verify monitoring task was created
    assert apprentice_id in monitor._monitoring_tasks
    assert not monitor._monitoring_tasks[apprentice_id].done()

    # Complete monitoring
    await monitor.complete_monitoring(apprentice_id)

    # Verify task was cancelled
    assert apprentice_id not in monitor._monitoring_tasks


@pytest.mark.asyncio
async def test_cpu_percent_calculation(monitor):
    """Test CPU percentage calculation from Docker stats"""
    stats = {
        "cpu_stats": {
            "cpu_usage": {"total_usage": 2000000000, "percpu_usage": [1000000000, 1000000000]},
            "system_cpu_usage": 10000000000,
        },
        "precpu_stats": {
            "cpu_usage": {"total_usage": 1000000000},
            "system_cpu_usage": 5000000000,
        },
    }

    cpu_percent = monitor._calculate_cpu_percent(stats)
    assert cpu_percent == 10.0  # (1000000000 / 5000000000) * 100 / 2 cores


@pytest.mark.asyncio
async def test_timeout_detection(monitor):
    """Test timeout detection for long-running tasks"""
    # Create monitor with short timeout
    monitor = ApprenticeMonitor(
        persistence_enabled=False, metrics_interval=1, health_check_interval=0.1
    )

    apprentice_id = "test-009"
    await monitor.register_spawn(apprentice_id, "T001", "ceremony-001", "container")
    await monitor.update_state(apprentice_id, ApprenticeState.WORKING)

    # Mock the elapsed time check
    with patch("mallku.orchestration.loom.apprentice_monitor.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime.now(UTC) + timedelta(seconds=1900)
        mock_datetime.UTC = UTC
        await monitor._check_apprentice_health(apprentice_id)

    record = monitor.active_apprentices.get(apprentice_id)
    if record:  # May have been cleaned up
        assert record.current_state == ApprenticeState.TIMEOUT

    await monitor.shutdown()


@pytest.mark.asyncio
async def test_persistence_disabled(monitor):
    """Test that persistence methods don't fail when disabled"""
    apprentice_id = "test-010"
    await monitor.register_spawn(apprentice_id, "T001", "ceremony-001", "container")

    # These should not raise errors even with persistence disabled
    event = ApprenticeLifecycleEvent(
        timestamp=datetime.now(UTC),
        apprentice_id=apprentice_id,
        event_type="test",
        old_state=None,
        new_state=ApprenticeState.READY,
    )

    await monitor._persist_event(event)  # Should not raise
    await monitor._persist_final_record(
        monitor.active_apprentices[apprentice_id]
    )  # Should not raise


@pytest.mark.asyncio
async def test_unknown_apprentice_handling(monitor):
    """Test handling of operations on unknown apprentices"""
    unknown_id = "unknown-001"

    # These should not raise errors
    await monitor.update_state(unknown_id, ApprenticeState.READY)
    await monitor.record_metrics(unknown_id, {"memory_mb": 100})
    await monitor.record_error(unknown_id, "Test error")

    result = await monitor.complete_monitoring(unknown_id)
    assert result is None
