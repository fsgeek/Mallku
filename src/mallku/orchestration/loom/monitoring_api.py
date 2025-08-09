"""
Monitoring API for Apprentice Lifecycle Observability

This module provides HTTP endpoints for external monitoring systems
to query apprentice and ceremony metrics.

Created by: 69th Guardian
Sacred Intent: To share awareness with those who watch over Mallku
"""

from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from .apprentice_monitor import get_apprentice_monitor
from .the_loom import TheLoom

router = APIRouter(prefix="/api/v1/monitoring", tags=["monitoring"])


class ApprenticeStatus(BaseModel):
    """Status information for a single apprentice"""

    apprentice_id: str
    task_id: str
    ceremony_id: str
    container_name: str
    current_state: str
    spawned_at: str
    duration_seconds: float
    memory_mb: float = 0.0
    cpu_percent: float = 0.0
    errors: int = 0
    warnings: int = 0


class CeremonyMetrics(BaseModel):
    """Aggregated metrics for a ceremony"""

    ceremony_id: str
    total_apprentices: int = 0
    active_apprentices: int = 0
    completed_apprentices: int = 0
    failed_apprentices: int = 0
    total_memory_mb: float = 0.0
    average_cpu_percent: float = 0.0
    total_errors: int = 0
    ceremony_duration: float = Field(0.0, description="Duration in seconds")
    ceremony_status: str | None = None
    total_tasks: int | None = None
    completed_tasks: int | None = None
    failed_tasks: int | None = None
    pending_tasks: int | None = None


class HealthStatus(BaseModel):
    """Overall health status of the monitoring system"""

    status: str = "healthy"
    active_ceremonies: int = 0
    total_active_apprentices: int = 0
    monitor_uptime_seconds: float = 0.0
    last_check: str


# Global Loom instance reference (set by application startup)
_loom_instance: TheLoom | None = None


def set_loom_instance(loom: TheLoom):
    """Set the global Loom instance for the API"""
    global _loom_instance
    _loom_instance = loom


@router.get("/health", response_model=HealthStatus)
async def get_health_status():
    """Get overall health status of the monitoring system"""
    monitor = get_apprentice_monitor()
    now = datetime.now(UTC)

    active_ceremonies = set()
    for record in monitor.active_apprentices.values():
        active_ceremonies.add(record.ceremony_id)

    return HealthStatus(
        status="healthy",
        active_ceremonies=len(active_ceremonies),
        total_active_apprentices=len(monitor.active_apprentices),
        monitor_uptime_seconds=0.0,  # Would need to track start time
        last_check=now.isoformat(),
    )


@router.get("/apprentices", response_model=list[ApprenticeStatus])
async def list_active_apprentices():
    """List all active apprentices with their current status"""
    monitor = get_apprentice_monitor()
    apprentices = []

    for record in monitor.active_apprentices.values():
        duration = (datetime.now(UTC) - record.spawned_at).total_seconds()

        apprentices.append(
            ApprenticeStatus(
                apprentice_id=record.apprentice_id,
                task_id=record.task_id,
                ceremony_id=record.ceremony_id,
                container_name=record.container_name,
                current_state=record.current_state.value,
                spawned_at=record.spawned_at.isoformat(),
                duration_seconds=duration,
                memory_mb=record.metrics.memory_usage_mb,
                cpu_percent=record.metrics.cpu_usage_percent,
                errors=record.metrics.errors_encountered,
                warnings=record.metrics.warnings_encountered,
            )
        )

    return apprentices


@router.get("/apprentices/{apprentice_id}", response_model=ApprenticeStatus)
async def get_apprentice_status(apprentice_id: str):
    """Get detailed status for a specific apprentice"""
    monitor = get_apprentice_monitor()

    if apprentice_id not in monitor.active_apprentices:
        raise HTTPException(status_code=404, detail=f"Apprentice {apprentice_id} not found")

    record = monitor.active_apprentices[apprentice_id]
    duration = (datetime.now(UTC) - record.spawned_at).total_seconds()

    return ApprenticeStatus(
        apprentice_id=record.apprentice_id,
        task_id=record.task_id,
        ceremony_id=record.ceremony_id,
        container_name=record.container_name,
        current_state=record.current_state.value,
        spawned_at=record.spawned_at.isoformat(),
        duration_seconds=duration,
        memory_mb=record.metrics.memory_usage_mb,
        cpu_percent=record.metrics.cpu_usage_percent,
        errors=record.metrics.errors_encountered,
        warnings=record.metrics.warnings_encountered,
    )


@router.get("/ceremonies/{ceremony_id}/metrics", response_model=CeremonyMetrics)
async def get_ceremony_metrics(ceremony_id: str):
    """Get aggregated metrics for a specific ceremony"""
    monitor = get_apprentice_monitor()
    metrics = await monitor.get_ceremony_metrics(ceremony_id)

    # Add Loom metrics if available
    if _loom_instance:
        loom_metrics = await _loom_instance.get_ceremony_metrics(ceremony_id)
        metrics.update(loom_metrics)

    return CeremonyMetrics(ceremony_id=ceremony_id, **metrics)


@router.get("/ceremonies", response_model=list[str])
async def list_active_ceremonies():
    """List all ceremonies with active apprentices"""
    monitor = get_apprentice_monitor()
    ceremonies = set()

    for record in monitor.active_apprentices.values():
        ceremonies.add(record.ceremony_id)

    return list(ceremonies)


@router.post("/apprentices/{apprentice_id}/events")
async def record_apprentice_event(
    apprentice_id: str, event_type: str, details: dict[str, Any] | None = None
):
    """Record a custom event for an apprentice (for external integrations)"""
    monitor = get_apprentice_monitor()

    if apprentice_id not in monitor.active_apprentices:
        raise HTTPException(status_code=404, detail=f"Apprentice {apprentice_id} not found")

    # Record as an error or metric depending on event type
    if event_type in ["error", "warning"]:
        message = details.get("message", "External event") if details else "External event"
        await monitor.record_error(apprentice_id, message, error_type=event_type)
    elif event_type == "metrics":
        if details:
            await monitor.record_metrics(apprentice_id, details)
    else:
        # For other events, we could extend the monitor to support custom events
        pass

    return {"status": "recorded", "apprentice_id": apprentice_id, "event_type": event_type}


# Prometheus-compatible metrics endpoint
@router.get("/metrics/prometheus", response_class=str)
async def get_prometheus_metrics():
    """Export metrics in Prometheus format"""
    monitor = get_apprentice_monitor()
    lines = []

    # Add header
    lines.append("# HELP mallku_apprentices_active Number of active apprentice weavers")
    lines.append("# TYPE mallku_apprentices_active gauge")
    lines.append(f"mallku_apprentices_active {len(monitor.active_apprentices)}")

    # Apprentice states
    state_counts = {}
    for record in monitor.active_apprentices.values():
        state = record.current_state.value
        state_counts[state] = state_counts.get(state, 0) + 1

    lines.append("# HELP mallku_apprentices_by_state Number of apprentices by state")
    lines.append("# TYPE mallku_apprentices_by_state gauge")
    for state, count in state_counts.items():
        lines.append(f'mallku_apprentices_by_state{{state="{state}"}} {count}')

    # Memory usage
    total_memory = sum(r.metrics.memory_usage_mb for r in monitor.active_apprentices.values())
    lines.append("# HELP mallku_apprentices_memory_mb Total memory usage in MB")
    lines.append("# TYPE mallku_apprentices_memory_mb gauge")
    lines.append(f"mallku_apprentices_memory_mb {total_memory}")

    # CPU usage
    if monitor.active_apprentices:
        avg_cpu = sum(
            r.metrics.cpu_usage_percent for r in monitor.active_apprentices.values()
        ) / len(monitor.active_apprentices)
        lines.append("# HELP mallku_apprentices_cpu_percent Average CPU usage percentage")
        lines.append("# TYPE mallku_apprentices_cpu_percent gauge")
        lines.append(f"mallku_apprentices_cpu_percent {avg_cpu:.2f}")

    # Error counts
    total_errors = sum(r.metrics.errors_encountered for r in monitor.active_apprentices.values())
    total_warnings = sum(
        r.metrics.warnings_encountered for r in monitor.active_apprentices.values()
    )
    lines.append("# HELP mallku_apprentices_errors_total Total errors encountered")
    lines.append("# TYPE mallku_apprentices_errors_total counter")
    lines.append(f"mallku_apprentices_errors_total {total_errors}")

    lines.append("# HELP mallku_apprentices_warnings_total Total warnings encountered")
    lines.append("# TYPE mallku_apprentices_warnings_total counter")
    lines.append(f"mallku_apprentices_warnings_total {total_warnings}")

    return "\n".join(lines) + "\n"
