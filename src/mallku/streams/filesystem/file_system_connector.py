"""
File System Activity Stream Connector

Monitors file system events and converts them into standardized events for correlation analysis.
This is the foundation of the Memory Anchor Discovery Trail - capturing raw human activity
as structured data that can be correlated across time and context.
"""

import asyncio
import contextlib
import logging
import time
from collections import defaultdict, deque
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from mallku.correlation.models import ConsciousnessEventType, Event

from .file_event_models import FileEvent, FileEventFilter, FileOperation

logger = logging.getLogger(__name__)


class FileSystemConnector:
    """
    Monitors file system activity and streams events to correlation engine.

    This connector serves as the root of the Memory Anchor Discovery Trail,
    transforming file operations into the structured events that feed our
    sophisticated temporal correlation detection system.
    """

    def __init__(
        self,
        event_filter: FileEventFilter | None = None,
        stream_id: str = "filesystem_monitor",
        session_id: str | None = None,
    ):
        """
        Initialize the file system connector.

        Args:
            event_filter: Configuration for filtering events
            stream_id: Identifier for this activity stream
            session_id: Current user session identifier
        """
        self.event_filter = event_filter or FileEventFilter()
        self.stream_id = stream_id
        self.session_id = session_id or str(uuid4())

        # Event processing
        self.event_callbacks: list[Callable[[Event], None]] = []
        self.event_queue: asyncio.Queue = asyncio.Queue()

        # File system monitoring
        self.observer: Observer | None = None
        self.watch_handlers: list[FileSystemEventHandler] = []

        # Rate limiting and deduplication
        self.recent_events: dict[str, deque] = defaultdict(lambda: deque(maxlen=10))
        self.last_event_times: dict[str, float] = {}

        # Statistics
        self.stats = {
            "events_captured": 0,
            "events_filtered": 0,
            "events_processed": 0,
            "start_time": None,
            "directories_watched": 0,
        }

        # Background processing
        self._processing_task: asyncio.Task | None = None
        self._is_running = False

    async def initialize(self) -> None:
        """Initialize the file system connector and start monitoring."""
        logger.info(f"Initializing FileSystemConnector with stream_id: {self.stream_id}")

        # Set up default watch directories if none specified
        if not self.event_filter.watch_directories:
            self.event_filter.watch_directories = self._get_default_watch_directories()

        # Validate watch directories
        valid_directories = []
        for directory in self.event_filter.watch_directories:
            if directory.exists() and directory.is_dir():
                valid_directories.append(directory)
                logger.info(f"Will monitor directory: {directory}")
            else:
                logger.warning(f"Directory not found or not accessible: {directory}")

        self.event_filter.watch_directories = valid_directories
        self.stats["directories_watched"] = len(valid_directories)

        # Start file system monitoring
        await self._start_monitoring()

        # Start event processing
        self._processing_task = asyncio.create_task(self._process_events())
        self._is_running = True

        self.stats["start_time"] = datetime.now(UTC)
        logger.info("FileSystemConnector initialized and monitoring started")

    async def shutdown(self) -> None:
        """Shutdown the file system connector and stop monitoring."""
        logger.info("Shutting down FileSystemConnector")

        self._is_running = False

        # Stop file system monitoring
        if self.observer:
            self.observer.stop()
            self.observer.join(timeout=5.0)

        # Stop event processing
        if self._processing_task:
            self._processing_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._processing_task

        logger.info("FileSystemConnector shutdown complete")

    def add_event_callback(self, callback: Callable[[Event], None]) -> None:
        """Add a callback function to receive processed events."""
        self.event_callbacks.append(callback)
        logger.info(f"Added event callback: {callback.__name__}")

    def remove_event_callback(self, callback: Callable[[Event], None]) -> None:
        """Remove an event callback."""
        if callback in self.event_callbacks:
            self.event_callbacks.remove(callback)
            logger.info(f"Removed event callback: {callback.__name__}")

    async def _start_monitoring(self) -> None:
        """Start file system monitoring using watchdog."""
        self.observer = Observer()

        for directory in self.event_filter.watch_directories:
            handler = FileEventHandler(self)
            self.watch_handlers.append(handler)

            self.observer.schedule(handler, str(directory), recursive=True)

            logger.info(f"Scheduled monitoring for: {directory}")

        self.observer.start()
        logger.info("File system observer started")

    async def _process_events(self) -> None:
        """Background task to process queued file events."""
        logger.info("Started event processing task")

        while self._is_running:
            try:
                # Get events from queue with timeout
                try:
                    file_event = await asyncio.wait_for(self.event_queue.get(), timeout=1.0)
                except TimeoutError:
                    continue

                # Convert to correlation engine event
                correlation_event = self._convert_to_correlation_event(file_event)

                # Send to callbacks
                for callback in self.event_callbacks:
                    try:
                        if asyncio.iscoroutinefunction(callback):
                            await callback(correlation_event)
                        else:
                            callback(correlation_event)
                    except Exception as e:
                        logger.error(f"Error in event callback {callback.__name__}: {e}")

                self.stats["events_processed"] += 1

            except Exception as e:
                logger.error(f"Error processing file event: {e}")

    def _convert_to_correlation_event(self, file_event: FileEvent) -> Event:
        """Convert FileEvent to correlation engine Event."""

        # Determine event type based on file category
        event_type_mapping = {
            "document": ConsciousnessEventType.STORAGE,
            "code": ConsciousnessEventType.STORAGE,
            "data": ConsciousnessEventType.STORAGE,
            "image": ConsciousnessEventType.STORAGE,
            "media": ConsciousnessEventType.STORAGE,
            "configuration": ConsciousnessEventType.STORAGE,
            "temporary": ConsciousnessEventType.ACTIVITY,
            "system": ConsciousnessEventType.ENVIRONMENTAL,
            "unknown": ConsciousnessEventType.STORAGE,
        }

        event_type = event_type_mapping.get(
            file_event.file_category.value, ConsciousnessEventType.STORAGE
        )

        # Build content dictionary
        content = {
            "operation": file_event.operation.value,
            "file_path": str(file_event.file_path),
            "file_name": file_event.file_name,
            "file_category": file_event.file_category.value,
            "parent_directory": file_event.parent_directory,
        }

        # Add optional content fields
        if file_event.file_size is not None:
            content["file_size"] = file_event.file_size
        if file_event.mime_type:
            content["mime_type"] = file_event.mime_type
        if file_event.file_extension:
            content["file_extension"] = file_event.file_extension
        if file_event.old_path:
            content["old_path"] = str(file_event.old_path)

        # Build context dictionary
        context = {
            "stream_id": self.stream_id,
            "session_id": self.session_id,
            "directory_path": str(file_event.directory_path),
            "connector_type": "filesystem",
        }

        # Add process context if available
        if file_event.process_name:
            context["process_name"] = file_event.process_name
        if file_event.process_id:
            context["process_id"] = file_event.process_id

        # Generate correlation tags for pattern detection
        correlation_tags = self._generate_correlation_tags(file_event)

        return Event(
            event_id=file_event.event_id,
            timestamp=file_event.timestamp,
            event_type=event_type,
            stream_id=self.stream_id,
            content=content,
            context=context,
            correlation_tags=correlation_tags,
        )

    def _generate_correlation_tags(self, file_event: FileEvent) -> list[str]:
        """Generate correlation tags to help pattern detection."""
        tags = []

        # File category tags
        tags.append(f"file_category:{file_event.file_category.value}")
        tags.append(f"operation:{file_event.operation.value}")

        # Directory-based tags
        if file_event.parent_directory:
            tags.append(f"directory:{file_event.parent_directory.lower()}")

        # Extension-based tags
        if file_event.file_extension:
            tags.append(f"extension:{file_event.file_extension}")

        # Process-based tags
        if file_event.process_name:
            tags.append(f"process:{file_event.process_name.lower()}")

        # Size-based tags
        if file_event.file_size is not None:
            if file_event.file_size < 1024:
                tags.append("size:small")
            elif file_event.file_size < 1024 * 1024:
                tags.append("size:medium")
            else:
                tags.append("size:large")

        # Pattern-based tags for common workflows
        tags.extend(self._detect_workflow_patterns(file_event))

        return tags

    def _detect_workflow_patterns(self, file_event: FileEvent) -> list[str]:
        """Detect common workflow patterns from file operations."""
        patterns = []

        file_name_lower = file_event.file_name.lower()
        dir_path_lower = str(file_event.directory_path).lower()

        # Development patterns
        if any(keyword in dir_path_lower for keyword in ["src", "source", "code", "project"]):
            patterns.append("workflow:development")

        # Writing patterns
        if any(keyword in dir_path_lower for keyword in ["documents", "docs", "writing"]):
            patterns.append("workflow:writing")

        # Version control patterns
        if ".git" in dir_path_lower or "commit" in file_name_lower:
            patterns.append("workflow:version_control")

        # Meeting patterns
        if any(keyword in file_name_lower for keyword in ["meeting", "notes", "agenda", "minutes"]):
            patterns.append("workflow:meeting")

        # Research patterns
        if any(
            keyword in file_name_lower for keyword in ["research", "analysis", "data", "results"]
        ):
            patterns.append("workflow:research")

        return patterns

    def _should_include_event(self, file_event: FileEvent) -> bool:
        """Apply rate limiting and deduplication in addition to filter criteria."""

        # Apply basic filter
        if not self.event_filter.should_include_event(file_event):
            self.stats["events_filtered"] += 1
            return False

        # Rate limiting for rapid changes
        if self.event_filter.ignore_rapid_changes:
            file_key = str(file_event.file_path)
            current_time = time.time() * 1000  # milliseconds

            last_time = self.last_event_times.get(file_key, 0)
            time_diff = current_time - last_time

            if time_diff < self.event_filter.rapid_change_threshold:
                self.stats["events_filtered"] += 1
                return False

            self.last_event_times[file_key] = current_time

        return True

    def _get_default_watch_directories(self) -> list[Path]:
        """Get default directories to monitor based on the current platform."""
        directories = []

        # User home directory
        home_dir = Path.home()
        directories.append(home_dir)

        # Common work directories
        common_dirs = [
            "Desktop",
            "Documents",
            "Downloads",
            "Projects",
            "Development",
            "Code",
            "Work",
            "workspace",
        ]

        for dir_name in common_dirs:
            potential_dir = home_dir / dir_name
            if potential_dir.exists() and potential_dir.is_dir():
                directories.append(potential_dir)

        # Current working directory if it's under home
        cwd = Path.cwd()
        if cwd != home_dir and cwd.is_relative_to(home_dir):
            directories.append(cwd)

        logger.info(f"Default watch directories: {[str(d) for d in directories]}")
        return directories

    def get_statistics(self) -> dict[str, Any]:
        """Get connector statistics."""
        stats = self.stats.copy()

        if stats["start_time"]:
            uptime = datetime.now(UTC) - stats["start_time"]
            stats["uptime_seconds"] = uptime.total_seconds()

            if stats["events_processed"] > 0:
                stats["events_per_second"] = stats["events_processed"] / uptime.total_seconds()

        stats["queue_size"] = self.event_queue.qsize()
        stats["callback_count"] = len(self.event_callbacks)
        stats["is_running"] = self._is_running

        return stats


class FileEventHandler(FileSystemEventHandler):
    """
    Watchdog event handler that converts file system events to FileEvent objects.
    """

    def __init__(self, connector: FileSystemConnector):
        self.connector = connector
        super().__init__()

    def on_created(self, event: FileSystemEvent) -> None:
        """Handle file creation events."""
        if not event.is_directory:
            self._handle_file_event(event.src_path, FileOperation.CREATED)

    def on_modified(self, event: FileSystemEvent) -> None:
        """Handle file modification events."""
        if not event.is_directory:
            self._handle_file_event(event.src_path, FileOperation.MODIFIED)

    def on_deleted(self, event: FileSystemEvent) -> None:
        """Handle file deletion events."""
        if not event.is_directory:
            self._handle_file_event(event.src_path, FileOperation.DELETED)

    def on_moved(self, event: FileSystemEvent) -> None:
        """Handle file move/rename events."""
        if not event.is_directory:
            self._handle_file_event(
                event.dest_path, FileOperation.MOVED, old_path=Path(event.src_path)
            )

    def _handle_file_event(
        self, file_path: str, operation: FileOperation, old_path: Path | None = None
    ) -> None:
        """Process a file system event and queue it for processing."""

        try:
            # Create FileEvent
            file_event = FileEvent.from_file_path(
                file_path=Path(file_path), operation=operation, old_path=old_path
            )

            self.connector.stats["events_captured"] += 1

            # Apply filtering
            if self.connector._should_include_event(file_event):
                # Queue for processing
                try:
                    self.connector.event_queue.put_nowait(file_event)
                except asyncio.QueueFull:
                    logger.warning("Event queue is full, dropping event")

        except Exception as e:
            logger.error(f"Error handling file event for {file_path}: {e}")


async def create_file_system_connector(
    watch_directories: list[Path] | None = None, stream_id: str = "filesystem_monitor"
) -> FileSystemConnector:
    """
    Convenience function to create and initialize a FileSystemConnector.

    Args:
        watch_directories: Directories to monitor (uses defaults if None)
        stream_id: Identifier for this activity stream

    Returns:
        Initialized and running FileSystemConnector
    """

    # Create event filter
    event_filter = FileEventFilter()
    if watch_directories:
        event_filter.watch_directories = watch_directories

    # Create and initialize connector
    connector = FileSystemConnector(event_filter=event_filter, stream_id=stream_id)

    await connector.initialize()

    return connector
