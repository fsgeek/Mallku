#!/usr/bin/env python3
"""
Demonstration of Apprentice Lifecycle Monitoring

This script demonstrates the monitoring and observability features for
apprentice weavers in the Mallku orchestration system.

Created by: 69th Guardian
Purpose: To show the health and progress tracking of those who serve
"""

import asyncio
import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.mallku.orchestration.loom.apprentice_monitor import (
    ApprenticeMonitor,
    ApprenticeState,
)


async def simulate_apprentice_lifecycle():
    """Simulate an apprentice's lifecycle with monitoring"""
    print("=== Apprentice Lifecycle Monitoring Demo ===\n")

    # Create monitor instance
    monitor = ApprenticeMonitor(persistence_enabled=False)  # Disable DB for demo

    # Simulate apprentice spawn
    apprentice_id = "demo-apprentice-001"
    task_id = "T001"
    ceremony_id = "demo-ceremony-2025"
    container_name = "mallku-apprentice-demo-001"

    print("1. Spawning apprentice...")
    record = await monitor.register_spawn(apprentice_id, task_id, ceremony_id, container_name)
    print(f"   ✓ Apprentice {apprentice_id} registered")
    print(f"   - Task: {task_id}")
    print(f"   - State: {record.current_state.value}\n")

    await asyncio.sleep(1)

    # Simulate container ready
    print("2. Container initialization complete...")
    await monitor.update_state(apprentice_id, ApprenticeState.READY)
    print(f"   ✓ State: {monitor.active_apprentices[apprentice_id].current_state.value}")
    print(
        f"   - Startup time: {monitor.active_apprentices[apprentice_id].metrics.container_startup_time:.2f}s\n"
    )

    await asyncio.sleep(1)

    # Simulate work starting
    print("3. Apprentice begins working on task...")
    await monitor.update_state(apprentice_id, ApprenticeState.WORKING)
    print(f"   ✓ State: {monitor.active_apprentices[apprentice_id].current_state.value}\n")

    # Simulate metrics collection
    print("4. Collecting performance metrics...")
    await monitor.record_metrics(
        apprentice_id, {"memory_mb": 256.5, "cpu_percent": 45.2, "khipu_updates": 3}
    )
    metrics = monitor.active_apprentices[apprentice_id].metrics
    print(f"   ✓ Memory: {metrics.memory_usage_mb:.1f} MB")
    print(f"   ✓ CPU: {metrics.cpu_usage_percent:.1f}%")
    print(f"   ✓ Khipu updates: {metrics.khipu_updates_count}\n")

    await asyncio.sleep(1)

    # Simulate a warning
    print("5. Recording a warning...")
    await monitor.record_error(
        apprentice_id, "Large memory allocation detected", error_type="warning"
    )
    print(f"   ⚠ Warnings: {metrics.warnings_encountered}\n")

    await asyncio.sleep(1)

    # Simulate completion
    print("6. Task completion...")
    await monitor.update_state(apprentice_id, ApprenticeState.COMPLETING)
    await asyncio.sleep(0.5)
    await monitor.update_state(apprentice_id, ApprenticeState.COMPLETED)
    print("   ✓ State: COMPLETED")

    # Complete monitoring
    final_output = "Task completed successfully with insights gathered"
    final_record = await monitor.complete_monitoring(apprentice_id, final_output)
    print(f"   ✓ Task execution time: {final_record.metrics.task_execution_time:.2f}s\n")

    # Display lifecycle summary
    print("=== Lifecycle Summary ===")
    print(f"Apprentice ID: {final_record.apprentice_id}")
    print(f"Total events: {len(final_record.events)}")
    print("\nState transitions:")
    for timestamp, state in final_record.states_history:
        print(f"  {timestamp.strftime('%H:%M:%S')} -> {state.value}")

    print("\nKey metrics:")
    print(f"  - Container startup: {final_record.metrics.container_startup_time:.2f}s")
    print(f"  - Task execution: {final_record.metrics.task_execution_time:.2f}s")
    print(f"  - Peak memory: {final_record.metrics.memory_usage_mb:.1f} MB")
    print(f"  - Peak CPU: {final_record.metrics.cpu_usage_percent:.1f}%")
    print(f"  - Warnings: {final_record.metrics.warnings_encountered}")
    print(f"  - Errors: {final_record.metrics.errors_encountered}")


async def simulate_ceremony_monitoring():
    """Simulate monitoring multiple apprentices in a ceremony"""
    print("\n\n=== Ceremony-wide Monitoring Demo ===\n")

    monitor = ApprenticeMonitor(persistence_enabled=False)
    ceremony_id = "bug-healing-2025"

    # Spawn multiple apprentices
    apprentices = [
        ("apprentice-001", "T001", "mallku-apprentice-001"),
        ("apprentice-002", "T002", "mallku-apprentice-002"),
        ("apprentice-003", "T003", "mallku-apprentice-003"),
    ]

    print("Spawning multiple apprentices for ceremony...")
    for app_id, task_id, container in apprentices:
        await monitor.register_spawn(app_id, task_id, ceremony_id, container)
        await monitor.update_state(app_id, ApprenticeState.READY)
        print(f"  ✓ {app_id} ready for {task_id}")

    await asyncio.sleep(1)

    # Simulate different states
    await monitor.update_state("apprentice-001", ApprenticeState.WORKING)
    await monitor.record_metrics("apprentice-001", {"memory_mb": 300, "cpu_percent": 60})

    await monitor.update_state("apprentice-002", ApprenticeState.WORKING)
    await monitor.record_metrics("apprentice-002", {"memory_mb": 250, "cpu_percent": 40})

    await monitor.update_state("apprentice-003", ApprenticeState.WORKING)
    await monitor.record_metrics("apprentice-003", {"memory_mb": 200, "cpu_percent": 30})

    # Complete one, fail one
    await monitor.update_state("apprentice-001", ApprenticeState.COMPLETED)
    await monitor.update_state("apprentice-002", ApprenticeState.FAILED)
    await monitor.record_error("apprentice-002", "Out of memory error")

    # Get ceremony metrics
    print("\nCeremony-wide metrics:")
    metrics = await monitor.get_ceremony_metrics(ceremony_id)
    print(f"  - Total apprentices: {metrics['total_apprentices']}")
    print(f"  - Active: {metrics['active_apprentices']}")
    print(f"  - Completed: {metrics['completed_apprentices']}")
    print(f"  - Failed: {metrics['failed_apprentices']}")
    print(f"  - Total memory: {metrics['total_memory_mb']:.1f} MB")
    print(f"  - Average CPU: {metrics['average_cpu_percent']:.1f}%")
    print(f"  - Total errors: {metrics['total_errors']}")

    # Clean up
    await monitor.shutdown()


async def main():
    """Run all demonstrations"""
    await simulate_apprentice_lifecycle()
    await simulate_ceremony_monitoring()

    print("\n✨ Monitoring demonstration complete!")
    print("\nThis monitoring system serves Mallku's need for HEARTBEAT -")
    print("continuous awareness of the health and progress of all who serve.")


if __name__ == "__main__":
    asyncio.run(main())
