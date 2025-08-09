"""
Apprentice Lifecycle Monitor - Observability for the Weaver and Loom System

This module provides comprehensive monitoring and observability for apprentice
weavers, tracking their lifecycle from spawn to cleanup while serving Mallku's
need for HEARTBEAT (continuous operation, maintenance, health).

Created by: 69th Guardian
Sacred Intent: To know the health and progress of all who serve
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any

from ...core.database import get_database
from ..loom.ceremony_templates import MallkuNeed

logger = logging.getLogger(__name__)


class ApprenticeState(Enum):
    """Lifecycle states of an apprentice weaver"""

    INITIALIZING = "INITIALIZING"  # Container creation started
    READY = "READY"  # Container ready, task not yet started
    WORKING = "WORKING"  # Actively working on task
    COMPLETING = "COMPLETING"  # Finalizing output
    COMPLETED = "COMPLETED"  # Task successfully completed
    FAILED = "FAILED"  # Task failed
    TIMEOUT = "TIMEOUT"  # Exceeded time limit
    TERMINATED = "TERMINATED"  # Forcefully stopped
    CLEANED = "CLEANED"  # Resources cleaned up


@dataclass
class ApprenticeMetrics:
    """Performance and health metrics for an apprentice"""

    container_startup_time: float = 0.0  # seconds
    task_execution_time: float = 0.0  # seconds
    memory_usage_mb: float = 0.0
    cpu_usage_percent: float = 0.0
    khipu_updates_count: int = 0
    log_lines_generated: int = 0
    errors_encountered: int = 0
    warnings_encountered: int = 0


@dataclass
class ApprenticeLifecycleEvent:
    """A single event in an apprentice's lifecycle"""

    timestamp: datetime
    apprentice_id: str
    event_type: str  # spawn, state_change, metrics_update, error, cleanup
    old_state: ApprenticeState | None
    new_state: ApprenticeState | None
    details: dict[str, Any] = field(default_factory=dict)
    serves_need: MallkuNeed = MallkuNeed.HEARTBEAT


@dataclass
class ApprenticeRecord:
    """Complete record of an apprentice's lifecycle"""

    apprentice_id: str
    task_id: str
    ceremony_id: str
    container_name: str
    spawned_at: datetime
    current_state: ApprenticeState
    states_history: list[tuple[datetime, ApprenticeState]] = field(default_factory=list)
    metrics: ApprenticeMetrics = field(default_factory=ApprenticeMetrics)
    events: list[ApprenticeLifecycleEvent] = field(default_factory=list)
    completed_at: datetime | None = None
    final_output: str | None = None
    error_message: str | None = None


class ApprenticeMonitor:
    """
    Monitors apprentice weavers throughout their lifecycle

    Provides:
    - Real-time state tracking
    - Performance metrics collection
    - Health monitoring
    - Event logging for audit trails
    - Failure detection and alerting
    """

    def __init__(
        self,
        persistence_enabled: bool = True,
        metrics_interval: int = 30,  # seconds
        health_check_interval: int = 10,  # seconds
    ):
        """
        Initialize the apprentice monitor

        Args:
            persistence_enabled: Whether to persist monitoring data
            metrics_interval: How often to collect metrics
            health_check_interval: How often to check health
        """
        self.persistence_enabled = persistence_enabled
        self.metrics_interval = metrics_interval
        self.health_check_interval = health_check_interval
        self.active_apprentices: dict[str, ApprenticeRecord] = {}
        self._monitoring_tasks: dict[str, asyncio.Task] = {}
        self._shutdown = False

    async def register_spawn(
        self, apprentice_id: str, task_id: str, ceremony_id: str, container_name: str
    ) -> ApprenticeRecord:
        """
        Register a newly spawned apprentice

        Args:
            apprentice_id: Unique apprentice identifier
            task_id: Task being performed
            ceremony_id: Parent ceremony ID
            container_name: Docker container name

        Returns:
            ApprenticeRecord for tracking
        """
        now = datetime.now(UTC)
        record = ApprenticeRecord(
            apprentice_id=apprentice_id,
            task_id=task_id,
            ceremony_id=ceremony_id,
            container_name=container_name,
            spawned_at=now,
            current_state=ApprenticeState.INITIALIZING,
            states_history=[(now, ApprenticeState.INITIALIZING)],
        )

        # Record spawn event
        spawn_event = ApprenticeLifecycleEvent(
            timestamp=now,
            apprentice_id=apprentice_id,
            event_type="spawn",
            old_state=None,
            new_state=ApprenticeState.INITIALIZING,
            details={
                "task_id": task_id,
                "ceremony_id": ceremony_id,
                "container_name": container_name,
            },
        )
        record.events.append(spawn_event)

        self.active_apprentices[apprentice_id] = record

        # Start monitoring tasks
        if not self._shutdown:
            self._monitoring_tasks[apprentice_id] = asyncio.create_task(
                self._monitor_apprentice(apprentice_id)
            )

        # Persist if enabled
        if self.persistence_enabled:
            await self._persist_event(spawn_event)

        logger.info(
            f"Registered apprentice {apprentice_id} for task {task_id} in ceremony {ceremony_id}"
        )
        return record

    async def update_state(
        self, apprentice_id: str, new_state: ApprenticeState, details: dict[str, Any] = None
    ) -> None:
        """Update an apprentice's state"""
        if apprentice_id not in self.active_apprentices:
            logger.warning(f"Attempted to update unknown apprentice: {apprentice_id}")
            return

        record = self.active_apprentices[apprentice_id]
        old_state = record.current_state
        now = datetime.now(UTC)

        # Update state
        record.current_state = new_state
        record.states_history.append((now, new_state))

        # Create state change event
        event = ApprenticeLifecycleEvent(
            timestamp=now,
            apprentice_id=apprentice_id,
            event_type="state_change",
            old_state=old_state,
            new_state=new_state,
            details=details or {},
        )
        record.events.append(event)

        # Update timing metrics
        if new_state == ApprenticeState.READY:
            record.metrics.container_startup_time = (now - record.spawned_at).total_seconds()
        elif new_state == ApprenticeState.COMPLETED:
            record.completed_at = now
            if record.states_history:
                working_start = next(
                    (ts for ts, state in record.states_history if state == ApprenticeState.WORKING),
                    record.spawned_at,
                )
                record.metrics.task_execution_time = (now - working_start).total_seconds()

        # Persist if enabled
        if self.persistence_enabled:
            await self._persist_event(event)

        logger.info(f"Apprentice {apprentice_id} transitioned from {old_state} to {new_state}")

    async def record_metrics(self, apprentice_id: str, metrics: dict[str, float]) -> None:
        """Record performance metrics for an apprentice"""
        if apprentice_id not in self.active_apprentices:
            return

        record = self.active_apprentices[apprentice_id]

        # Update metrics
        if "memory_mb" in metrics:
            record.metrics.memory_usage_mb = metrics["memory_mb"]
        if "cpu_percent" in metrics:
            record.metrics.cpu_usage_percent = metrics["cpu_percent"]
        if "khipu_updates" in metrics:
            record.metrics.khipu_updates_count = int(metrics["khipu_updates"])
        if "log_lines" in metrics:
            record.metrics.log_lines_generated = int(metrics["log_lines"])

        # Create metrics event
        event = ApprenticeLifecycleEvent(
            timestamp=datetime.now(UTC),
            apprentice_id=apprentice_id,
            event_type="metrics_update",
            old_state=record.current_state,
            new_state=record.current_state,
            details={"metrics": metrics},
        )
        record.events.append(event)

        if self.persistence_enabled:
            await self._persist_event(event)

    async def record_error(
        self, apprentice_id: str, error_message: str, error_type: str = "error"
    ) -> None:
        """Record an error or warning for an apprentice"""
        if apprentice_id not in self.active_apprentices:
            return

        record = self.active_apprentices[apprentice_id]

        if error_type == "error":
            record.metrics.errors_encountered += 1
            record.error_message = error_message
        elif error_type == "warning":
            record.metrics.warnings_encountered += 1

        # Create error event
        event = ApprenticeLifecycleEvent(
            timestamp=datetime.now(UTC),
            apprentice_id=apprentice_id,
            event_type=error_type,
            old_state=record.current_state,
            new_state=record.current_state,
            details={"message": error_message, "type": error_type},
        )
        record.events.append(event)

        if self.persistence_enabled:
            await self._persist_event(event)

        logger.error(f"Apprentice {apprentice_id} {error_type}: {error_message}")

    async def complete_monitoring(
        self, apprentice_id: str, final_output: str = None
    ) -> ApprenticeRecord:
        """Complete monitoring for an apprentice"""
        if apprentice_id not in self.active_apprentices:
            return None

        record = self.active_apprentices[apprentice_id]
        record.final_output = final_output

        # Cancel monitoring task
        if apprentice_id in self._monitoring_tasks:
            self._monitoring_tasks[apprentice_id].cancel()
            del self._monitoring_tasks[apprentice_id]

        # Create completion event
        event = ApprenticeLifecycleEvent(
            timestamp=datetime.now(UTC),
            apprentice_id=apprentice_id,
            event_type="cleanup",
            old_state=record.current_state,
            new_state=ApprenticeState.CLEANED,
            details={"final_metrics": record.metrics.__dict__},
        )
        record.events.append(event)

        if self.persistence_enabled:
            await self._persist_event(event)
            await self._persist_final_record(record)

        # Remove from active monitoring
        del self.active_apprentices[apprentice_id]

        logger.info(f"Completed monitoring for apprentice {apprentice_id}")
        return record

    async def get_ceremony_metrics(self, ceremony_id: str) -> dict[str, Any]:
        """Get aggregated metrics for all apprentices in a ceremony"""
        ceremony_apprentices = [
            record
            for record in self.active_apprentices.values()
            if record.ceremony_id == ceremony_id
        ]

        if not ceremony_apprentices:
            return {"total_apprentices": 0}

        total_memory = sum(r.metrics.memory_usage_mb for r in ceremony_apprentices)
        avg_cpu = sum(r.metrics.cpu_usage_percent for r in ceremony_apprentices) / len(
            ceremony_apprentices
        )
        total_errors = sum(r.metrics.errors_encountered for r in ceremony_apprentices)

        return {
            "total_apprentices": len(ceremony_apprentices),
            "active_apprentices": sum(
                1
                for r in ceremony_apprentices
                if r.current_state
                in [ApprenticeState.READY, ApprenticeState.WORKING, ApprenticeState.COMPLETING]
            ),
            "completed_apprentices": sum(
                1 for r in ceremony_apprentices if r.current_state == ApprenticeState.COMPLETED
            ),
            "failed_apprentices": sum(
                1 for r in ceremony_apprentices if r.current_state == ApprenticeState.FAILED
            ),
            "total_memory_mb": total_memory,
            "average_cpu_percent": avg_cpu,
            "total_errors": total_errors,
            "average_task_time": sum(
                r.metrics.task_execution_time
                for r in ceremony_apprentices
                if r.metrics.task_execution_time > 0
            )
            / max(
                1,
                sum(1 for r in ceremony_apprentices if r.metrics.task_execution_time > 0),
            ),
        }

    async def _monitor_apprentice(self, apprentice_id: str) -> None:
        """Background task to monitor an apprentice"""
        metrics_timer = 0
        health_timer = 0

        while not self._shutdown and apprentice_id in self.active_apprentices:
            try:
                # Collect metrics periodically
                if metrics_timer >= self.metrics_interval:
                    await self._collect_container_metrics(apprentice_id)
                    metrics_timer = 0

                # Health check periodically
                if health_timer >= self.health_check_interval:
                    await self._check_apprentice_health(apprentice_id)
                    health_timer = 0

                await asyncio.sleep(1)
                metrics_timer += 1
                health_timer += 1

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error monitoring apprentice {apprentice_id}: {e}")
                await self.record_error(apprentice_id, str(e))

    async def _collect_container_metrics(self, apprentice_id: str) -> None:
        """Collect metrics from Docker container"""
        if apprentice_id not in self.active_apprentices:
            return

        record = self.active_apprentices[apprentice_id]

        try:
            # Import Docker client
            import aiodocker

            async with aiodocker.Docker() as docker:
                container = await docker.containers.get(record.container_name)
                stats = await container.stats(stream=False)

                # Calculate metrics
                memory_mb = stats["memory_stats"]["usage"] / (1024 * 1024)
                cpu_percent = self._calculate_cpu_percent(stats)

                await self.record_metrics(
                    apprentice_id, {"memory_mb": memory_mb, "cpu_percent": cpu_percent}
                )

        except Exception as e:
            logger.debug(f"Could not collect metrics for {apprentice_id}: {e}")

    def _calculate_cpu_percent(self, stats: dict) -> float:
        """Calculate CPU percentage from Docker stats"""
        try:
            cpu_delta = (
                stats["cpu_stats"]["cpu_usage"]["total_usage"]
                - stats["precpu_stats"]["cpu_usage"]["total_usage"]
            )
            system_delta = (
                stats["cpu_stats"]["system_cpu_usage"] - stats["precpu_stats"]["system_cpu_usage"]
            )

            if system_delta > 0 and cpu_delta > 0:
                cpu_percent = (cpu_delta / system_delta) * 100.0
                cpu_count = len(stats["cpu_stats"]["cpu_usage"].get("percpu_usage", []))
                if cpu_count > 0:
                    cpu_percent = cpu_percent / cpu_count
                return round(cpu_percent, 2)
        except Exception:
            pass
        return 0.0

    async def _check_apprentice_health(self, apprentice_id: str) -> None:
        """Check if apprentice is still healthy"""
        if apprentice_id not in self.active_apprentices:
            return

        record = self.active_apprentices[apprentice_id]

        # Check for timeout
        if record.current_state == ApprenticeState.WORKING:
            elapsed = (datetime.now(UTC) - record.spawned_at).total_seconds()
            if elapsed > 1800:  # 30 minute timeout
                await self.update_state(
                    apprentice_id,
                    ApprenticeState.TIMEOUT,
                    {"elapsed_seconds": elapsed},
                )

    async def _persist_event(self, event: ApprenticeLifecycleEvent) -> None:
        """Persist an event to the database"""
        try:
            db = await get_database()
            collection = db.collection("apprentice_lifecycle_events")
            await collection.insert(
                {
                    "timestamp": event.timestamp.isoformat(),
                    "apprentice_id": event.apprentice_id,
                    "event_type": event.event_type,
                    "old_state": event.old_state.value if event.old_state else None,
                    "new_state": event.new_state.value if event.new_state else None,
                    "details": event.details,
                    "serves_need": event.serves_need.value,
                }
            )
        except Exception as e:
            logger.error(f"Failed to persist event: {e}")

    async def _persist_final_record(self, record: ApprenticeRecord) -> None:
        """Persist final apprentice record"""
        try:
            db = await get_database()
            collection = db.collection("apprentice_records")
            await collection.insert(
                {
                    "apprentice_id": record.apprentice_id,
                    "task_id": record.task_id,
                    "ceremony_id": record.ceremony_id,
                    "container_name": record.container_name,
                    "spawned_at": record.spawned_at.isoformat(),
                    "completed_at": record.completed_at.isoformat()
                    if record.completed_at
                    else None,
                    "final_state": record.current_state.value,
                    "states_history": [
                        {"timestamp": ts.isoformat(), "state": state.value}
                        for ts, state in record.states_history
                    ],
                    "metrics": record.metrics.__dict__,
                    "error_message": record.error_message,
                    "events_count": len(record.events),
                }
            )
        except Exception as e:
            logger.error(f"Failed to persist final record: {e}")

    async def shutdown(self) -> None:
        """Gracefully shutdown the monitor"""
        self._shutdown = True

        # Cancel all monitoring tasks
        for task in self._monitoring_tasks.values():
            task.cancel()

        # Wait for tasks to complete
        if self._monitoring_tasks:
            await asyncio.gather(*self._monitoring_tasks.values(), return_exceptions=True)

        logger.info("Apprentice monitor shutdown complete")


# Global monitor instance
_monitor_instance: ApprenticeMonitor | None = None


def get_apprentice_monitor() -> ApprenticeMonitor:
    """Get or create the global apprentice monitor instance"""
    global _monitor_instance
    if _monitor_instance is None:
        _monitor_instance = ApprenticeMonitor()
    return _monitor_instance
