"""
End-to-End Integration Service

The keystone that joins our three foundational components into a living pipeline:
File System Connector → Correlation Engine → Memory Anchor Service

This service orchestrates the complete Memory Anchor Discovery Trail,
transforming raw file operations into contextual intelligence.
"""

import asyncio
import contextlib
import logging
from collections import deque
from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from pathlib import Path

from mallku.correlation.engine import CorrelationEngine
from mallku.correlation.models import Event
from mallku.services.memory_anchor_service import MemoryAnchorService
from mallku.streams.filesystem import FileEventFilter, FileSystemConnector

from .correlation_adapter import CorrelationToAnchorAdapter
from .pipeline_models import (
    PipelineConfiguration,
    PipelineEvent,
    PipelineStage,
    PipelineStatistics,
    PipelineStatus,
)

logger = logging.getLogger(__name__)


class EndToEndIntegrationService:
    """
    Orchestrates the complete Memory Anchor Discovery Trail pipeline.

    This service serves as the cathedral's keystone, joining our three
    foundational components into a unified system that transforms
    activity streams into contextual intelligence.
    """

    def __init__(self, config: PipelineConfiguration | None = None):
        """
        Initialize the End-to-End Integration Service.

        Args:
            config: Pipeline configuration (uses defaults if None)
        """
        self.config = config or PipelineConfiguration()
        self.pipeline_id = self.config.pipeline_id

        # Core components (initialized in initialize())
        self.memory_service: MemoryAnchorService | None = None
        self.correlation_engine: CorrelationEngine | None = None
        self.file_connector: FileSystemConnector | None = None
        self.correlation_adapter: CorrelationToAnchorAdapter | None = None

        # Pipeline state
        self.is_running = False
        self.start_time: datetime | None = None
        self.shutdown_event = asyncio.Event()

        # Event processing
        self.event_queue: asyncio.Queue[Event] = asyncio.Queue(maxsize=self.config.event_queue_size)
        self.pipeline_events: dict[str, PipelineEvent] = {}
        self.active_events: deque[PipelineEvent] = deque(maxlen=1000)

        # Processing tasks
        self.processing_tasks: list[asyncio.Task] = []
        self.monitoring_task: asyncio.Task | None = None

        # Statistics
        self.statistics = PipelineStatistics(
            uptime=timedelta(0), total_events_processed=0, successful_events=0, failed_events=0
        )

        # Event handlers
        self.event_handlers: list[Callable[[PipelineEvent], None]] = []

    async def initialize(self) -> None:
        """Initialize all pipeline components and start processing."""
        logger.info(f"Initializing End-to-End Integration Service (Pipeline: {self.pipeline_id})")

        try:
            # Initialize Memory Anchor Service
            logger.info("Initializing Memory Anchor Service...")
            self.memory_service = MemoryAnchorService()
            await self.memory_service.initialize()

            # Initialize Correlation Engine
            logger.info("Initializing Correlation Engine...")
            self.correlation_engine = CorrelationEngine(
                memory_anchor_service=self.memory_service,
                window_size=timedelta(hours=self.config.correlation_window_size_hours),
                window_overlap=self.config.correlation_window_overlap,
            )
            await self.correlation_engine.initialize()

            # Initialize Correlation Adapter
            logger.info("Initializing Correlation Adapter...")
            self.correlation_adapter = CorrelationToAnchorAdapter(
                memory_service=self.memory_service,
                confidence_threshold=self.config.anchor_creation_threshold,
                batch_size=self.config.anchor_batch_size,
            )

            # Initialize File System Connector
            logger.info("Initializing File System Connector...")
            file_filter = self._create_file_filter()
            self.file_connector = FileSystemConnector(
                event_filter=file_filter, stream_id=f"integration_pipeline_{self.pipeline_id}"
            )

            # Connect file connector to our event processing
            self.file_connector.add_event_callback(self._handle_activity_event)
            await self.file_connector.initialize()

            # Start processing tasks
            await self._start_processing_tasks()

            self.is_running = True
            self.start_time = datetime.now(UTC)

            logger.info("End-to-End Integration Service initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize Integration Service: {e}")
            await self._cleanup_on_error()
            raise

    async def shutdown(self) -> None:
        """Shutdown the integration service gracefully."""
        logger.info("Shutting down End-to-End Integration Service...")

        self.is_running = False
        self.shutdown_event.set()

        # Stop file monitoring first
        if self.file_connector:
            await self.file_connector.shutdown()

        # Cancel processing tasks
        for task in self.processing_tasks:
            task.cancel()

        if self.monitoring_task:
            self.monitoring_task.cancel()

        # Wait for tasks to complete
        if self.processing_tasks:
            await asyncio.gather(*self.processing_tasks, return_exceptions=True)

        # Shutdown core components
        if self.correlation_engine:
            await self.correlation_engine.shutdown()

        if self.memory_service:
            await self.memory_service.shutdown()

        logger.info("End-to-End Integration Service shutdown complete")

    def add_event_handler(self, handler: Callable[[PipelineEvent], None]) -> None:
        """Add an event handler to monitor pipeline events."""
        self.event_handlers.append(handler)

    def remove_event_handler(self, handler: Callable[[PipelineEvent], None]) -> None:
        """Remove an event handler."""
        if handler in self.event_handlers:
            self.event_handlers.remove(handler)

    async def get_pipeline_status(self) -> PipelineStatus:
        """Get current pipeline status."""

        # Get component statuses
        file_status = (
            "running" if (self.file_connector and self.file_connector._is_running) else "stopped"
        )
        correlation_status = (
            "active"
            if (
                self.correlation_engine
                and self.correlation_engine.get_engine_status()["engine_info"]["status"] == "active"
            )
            else "inactive"
        )
        memory_status = "active" if self.memory_service else "inactive"

        # Calculate performance metrics
        uptime = datetime.now(UTC) - self.start_time if self.start_time else timedelta(0)
        events_per_second = (
            self.statistics.total_events_processed / uptime.total_seconds()
            if uptime.total_seconds() > 0
            else 0
        )

        return PipelineStatus(
            pipeline_id=self.pipeline_id,
            is_running=self.is_running,
            start_time=self.start_time or datetime.now(UTC),
            file_connector_status=file_status,
            correlation_engine_status=correlation_status,
            memory_service_status=memory_status,
            events_in_pipeline=self.event_queue.qsize(),
            events_processed=self.statistics.total_events_processed,
            events_failed=self.statistics.failed_events,
            avg_processing_time_ms=self._calculate_avg_processing_time(),
            events_per_second=events_per_second,
            recent_errors=self._get_recent_errors(),
            error_rate=self._calculate_error_rate(),
        )

    async def get_pipeline_statistics(self) -> PipelineStatistics:
        """Get comprehensive pipeline statistics."""
        # Update uptime
        if self.start_time:
            self.statistics.uptime = datetime.now(UTC) - self.start_time

        # Update component statistics
        if self.file_connector:
            self.statistics.component_stats["file_connector"] = self.file_connector.get_statistics()

        if self.correlation_engine:
            engine_status = self.correlation_engine.get_engine_status()
            self.statistics.component_stats["correlation_engine"] = engine_status["statistics"]

        if self.correlation_adapter:
            self.statistics.component_stats["correlation_adapter"] = (
                self.correlation_adapter.get_statistics()
            )

        return self.statistics

    async def _handle_activity_event(self, event: Event) -> None:
        """Handle incoming activity events from file system connector."""

        # Create pipeline event to track processing
        pipeline_event = PipelineEvent(source_event_id=event.event_id, activity_event=event.dict())

        self.pipeline_events[str(event.event_id)] = pipeline_event
        self.active_events.append(pipeline_event)

        # Queue event for processing
        try:
            await self.event_queue.put(event)

            # Notify event handlers
            for handler in self.event_handlers:
                try:
                    handler(pipeline_event)
                except Exception as e:
                    logger.error(f"Error in event handler: {e}")

        except asyncio.QueueFull:
            logger.warning("Event queue is full, dropping event")
            pipeline_event.record_error("Event queue full")

    async def _start_processing_tasks(self) -> None:
        """Start background processing tasks."""

        # Start event processing workers
        for i in range(self.config.max_concurrent_events // 10):  # 10 events per worker
            task = asyncio.create_task(
                self._event_processing_worker(f"worker_{i}"), name=f"event_worker_{i}"
            )
            self.processing_tasks.append(task)

        # Start monitoring task
        self.monitoring_task = asyncio.create_task(self._monitoring_loop(), name="monitoring_loop")

    async def _event_processing_worker(self, worker_name: str) -> None:
        """Process events from the queue."""
        logger.info(f"Started event processing worker: {worker_name}")

        while not self.shutdown_event.is_set():
            try:
                # Get event from queue with timeout
                try:
                    event = await asyncio.wait_for(self.event_queue.get(), timeout=1.0)
                except TimeoutError:
                    continue

                # Process the event
                await self._process_single_event(event)

            except Exception as e:
                logger.error(f"Error in event processing worker {worker_name}: {e}")

        logger.info(f"Event processing worker {worker_name} stopped")

    async def _process_single_event(self, event: Event) -> None:
        """Process a single event through the correlation pipeline."""

        start_time = datetime.now(UTC)
        pipeline_event = self.pipeline_events.get(str(event.event_id))

        if not pipeline_event:
            logger.warning(f"No pipeline event found for {event.event_id}")
            return

        try:
            # Stage 1: Correlation Detection
            pipeline_event.advance_stage(PipelineStage.CORRELATION_DETECTION)

            correlations = await self.correlation_engine.process_event_stream([event])
            pipeline_event.detected_correlations = [corr.dict() for corr in correlations]

            correlation_time = (datetime.now(UTC) - start_time).total_seconds() * 1000
            pipeline_event.advance_stage(PipelineStage.ANCHOR_CREATION, correlation_time)

            # Stage 2: Memory Anchor Creation
            created_anchors = []
            for correlation in correlations:
                if correlation.confidence_score >= self.config.anchor_creation_threshold:
                    anchor = await self.correlation_adapter.process_correlation(correlation)
                    if anchor:
                        created_anchors.append(str(anchor.anchor_id))

            pipeline_event.created_anchors = created_anchors

            anchor_time = (datetime.now(UTC) - start_time).total_seconds() * 1000
            pipeline_event.advance_stage(PipelineStage.PERSISTENCE, anchor_time)

            # Stage 3: Persistence (handled by memory service)
            # Memory anchors are already persisted by the adapter

            persistence_time = (datetime.now(UTC) - start_time).total_seconds() * 1000
            pipeline_event.advance_stage(PipelineStage.COMPLETED, persistence_time)

            # Update statistics
            self.statistics.total_events_processed += 1
            self.statistics.successful_events += 1
            self.statistics.correlations_detected += len(correlations)
            self.statistics.anchors_created += len(created_anchors)

            # Update correlation type statistics
            for correlation in correlations:
                pattern_type = correlation.pattern_type
                self.statistics.correlation_types[pattern_type] = (
                    self.statistics.correlation_types.get(pattern_type, 0) + 1
                )

            logger.debug(
                f"Successfully processed event {event.event_id}: "
                f"{len(correlations)} correlations, {len(created_anchors)} anchors"
            )

        except Exception as e:
            # Record error in pipeline event
            pipeline_event.record_error(str(e))

            # Update statistics
            self.statistics.total_events_processed += 1
            self.statistics.failed_events += 1

            logger.error(f"Failed to process event {event.event_id}: {e}")

    async def _monitoring_loop(self) -> None:
        """Background monitoring and maintenance loop."""
        logger.info("Started pipeline monitoring loop")

        while not self.shutdown_event.is_set():
            try:
                # Clean up old pipeline events
                await self._cleanup_old_pipeline_events()

                # Update performance statistics
                await self._update_performance_statistics()

                # Health checks
                await self._perform_health_checks()

                # Wait for next monitoring cycle
                await asyncio.sleep(self.config.metrics_collection_interval_seconds)

            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")

        logger.info("Pipeline monitoring loop stopped")

    async def _cleanup_old_pipeline_events(self) -> None:
        """Clean up old pipeline events to prevent memory leaks."""
        cutoff_time = datetime.now(UTC) - timedelta(hours=1)

        # Remove old pipeline events
        to_remove = [
            event_id
            for event_id, pipeline_event in self.pipeline_events.items()
            if pipeline_event.created_at < cutoff_time
        ]

        for event_id in to_remove:
            del self.pipeline_events[event_id]

    async def _update_performance_statistics(self) -> None:
        """Update performance statistics."""
        # This could include more sophisticated metrics collection
        pass

    async def _perform_health_checks(self) -> None:
        """Perform health checks on pipeline components."""
        # Check component health and restart if necessary
        # This is a placeholder for more sophisticated health monitoring
        pass

    def _create_file_filter(self) -> FileEventFilter:
        """Create file event filter from configuration."""

        watch_directories = (
            [Path(dir_path) for dir_path in self.config.watch_directories]
            if self.config.watch_directories
            else []
        )

        return FileEventFilter(
            watch_directories=watch_directories, **self.config.file_filter_config
        )

    def _calculate_avg_processing_time(self) -> float:
        """Calculate average processing time from recent pipeline events."""
        recent_events = list(self.active_events)[-100:]  # Last 100 events

        if not recent_events:
            return 0.0

        total_times = []
        for event in recent_events:
            if event.completed_at:
                processing_time = (event.completed_at - event.created_at).total_seconds() * 1000
                total_times.append(processing_time)

        return sum(total_times) / len(total_times) if total_times else 0.0

    def _get_recent_errors(self) -> list[str]:
        """Get recent error messages."""
        recent_events = list(self.active_events)[-50:]  # Last 50 events

        errors = []
        for event in recent_events:
            if event.error_message:
                errors.append(f"{event.source_event_id}: {event.error_message}")

        return errors[-10:]  # Return last 10 errors

    def _calculate_error_rate(self) -> float:
        """Calculate current error rate."""
        if self.statistics.total_events_processed == 0:
            return 0.0

        return self.statistics.failed_events / self.statistics.total_events_processed

    async def _cleanup_on_error(self) -> None:
        """Clean up resources when initialization fails."""
        if self.file_connector:
            with contextlib.suppress(Exception):
                await self.file_connector.shutdown()

        if self.correlation_engine:
            with contextlib.suppress(Exception):
                await self.correlation_engine.shutdown()

        if self.memory_service:
            with contextlib.suppress(Exception):
                await self.memory_service.shutdown()


async def create_integration_service(
    watch_directories: list[str] | None = None,
    correlation_confidence_threshold: float = 0.6,
    anchor_creation_threshold: float = 0.7,
) -> EndToEndIntegrationService:
    """
    Convenience function to create and initialize an integration service.

    Args:
        watch_directories: Directories to monitor for file activity
        correlation_confidence_threshold: Minimum confidence for correlation detection
        anchor_creation_threshold: Minimum confidence for anchor creation

    Returns:
        Initialized and running EndToEndIntegrationService
    """

    config = PipelineConfiguration(
        watch_directories=watch_directories or [],
        correlation_confidence_threshold=correlation_confidence_threshold,
        anchor_creation_threshold=anchor_creation_threshold,
    )

    service = EndToEndIntegrationService(config)
    await service.initialize()

    return service
