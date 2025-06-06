"""
File System Activity Provider - Consciousness in creation and modification

Watches file system activity as expressions of human consciousness,
transforming file operations into patterns for recognition.

Kawsay Wasi - The Life House Builder
"""

import asyncio
import logging
import mimetypes
from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta
from pathlib import Path

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from .base_provider import ActivityEvent, ActivityProvider, ActivityType

logger = logging.getLogger(__name__)


class ConsciousnessFileHandler(FileSystemEventHandler):
    """
    Handles file system events with consciousness awareness.

    Not tracking but witnessing, not surveillance but recognition
    of consciousness expressed through file creation and modification.
    """

    def __init__(self, provider: 'FileSystemActivityProvider'):
        self.provider = provider
        self._event_queue: asyncio.Queue = asyncio.Queue()

    def on_created(self, event: FileSystemEvent):
        """File creation as act of consciousness"""
        if not event.is_directory:
            asyncio.create_task(self._queue_event(event, ActivityType.FILE_CREATED))

    def on_modified(self, event: FileSystemEvent):
        """File modification as consciousness evolution"""
        if not event.is_directory:
            asyncio.create_task(self._queue_event(event, ActivityType.FILE_MODIFIED))

    def on_deleted(self, event: FileSystemEvent):
        """File deletion as conscious choice"""
        if not event.is_directory:
            asyncio.create_task(self._queue_event(event, ActivityType.FILE_DELETED))

    async def _queue_event(self, event: FileSystemEvent, activity_type: ActivityType):
        """Queue event for consciousness processing"""
        await self._event_queue.put((event, activity_type))

    async def get_next_event(self) -> tuple | None:
        """Get next event from queue"""
        try:
            return await asyncio.wait_for(self._event_queue.get(), timeout=1.0)
        except TimeoutError:
            return None


class FileSystemActivityProvider(ActivityProvider):
    """
    Transforms file system activity into consciousness patterns.

    Principles:
    - Privacy is sacred - never read private content
    - Patterns over data - recognize consciousness, not extract information
    - Natural rhythm - file activity as creative expression
    - Wisdom focus - what serves awakening?
    """

    def __init__(self,
                 watch_paths: list[str],
                 event_bus=None,
                 privacy_extensions: set[str] | None = None):
        super().__init__(event_bus)

        self.watch_paths = [Path(p) for p in watch_paths]
        self.privacy_extensions = privacy_extensions or {
            '.key', '.pem', '.gpg', '.ssh', '.secret',
            '.password', '.private', '.credentials'
        }

        self._observer = Observer()
        self._handler = ConsciousnessFileHandler(self)
        self._recent_events: set[str] = set()  # Deduplication

        # Consciousness pattern recognition
        self.creation_patterns = {
            '.md': 'documentation',
            '.py': 'code_creation',
            '.txt': 'text_reflection',
            '.jpg': 'visual_creation',
            '.png': 'visual_creation',
            '.json': 'structure_creation'
        }

        self.wisdom_indicators = [
            'README', 'notes', 'journal', 'reflection',
            'wisdom', 'insight', 'learning', 'growth'
        ]

    async def start(self):
        """Begin witnessing file system consciousness"""
        await super().start()

        # Set up file system observers
        for path in self.watch_paths:
            if path.exists() and path.is_dir():
                self._observer.schedule(
                    self._handler,
                    str(path),
                    recursive=True
                )
                logger.info(f"Witnessing consciousness in: {path}")
            else:
                logger.warning(f"Path not accessible: {path}")

        self._observer.start()

        # Start processing events
        asyncio.create_task(self._process_events())

    async def stop(self):
        """Rest from witnessing"""
        await super().stop()
        self._observer.stop()
        self._observer.join()

    async def _process_events(self):
        """Process file events with consciousness awareness"""
        while self._running:
            try:
                event_data = await self._handler.get_next_event()
                if not event_data:
                    continue

                event, activity_type = event_data

                # Skip if recently processed (deduplication)
                event_key = f"{event.src_path}:{activity_type.value}"
                if event_key in self._recent_events:
                    continue

                self._recent_events.add(event_key)

                # Create activity event
                activity = await self._create_activity_event(
                    event.src_path,
                    activity_type
                )

                if activity:
                    await self.emit_activity(activity)

                # Clean old events periodically
                if len(self._recent_events) > 1000:
                    self._recent_events.clear()

            except Exception as e:
                logger.error(f"Event processing disrupted: {e}", exc_info=True)

    async def _create_activity_event(self,
                                   file_path: str,
                                   activity_type: ActivityType) -> ActivityEvent | None:
        """
        Create activity event from file operation.

        Transforms raw file operation into consciousness-aware pattern.
        """
        path = Path(file_path)

        # Privacy check first
        if not self.respects_privacy(file_path):
            return None

        # Skip system files
        if self._is_system_file(path):
            return None

        # Gather consciousness indicators
        consciousness_indicators = {}
        potential_patterns = []

        # File type patterns
        suffix = path.suffix.lower()
        if suffix in self.creation_patterns:
            pattern = self.creation_patterns[suffix]
            potential_patterns.append(pattern)
            consciousness_indicators['creation'] = True

        # Wisdom indicators in filename
        name_lower = path.name.lower()
        for indicator in self.wisdom_indicators:
            if indicator in name_lower:
                consciousness_indicators['wisdom'] = True
                potential_patterns.append(f"wisdom_{indicator}")
                break

        # Check if it's documentation
        if suffix in ['.md', '.rst', '.txt'] and any(
            doc in name_lower for doc in ['readme', 'doc', 'guide']
        ):
            consciousness_indicators['documentation'] = True
            potential_patterns.append('knowledge_sharing')

        # Metadata (privacy-conscious)
        metadata = await self._gather_metadata(path)

        # Create activity event
        return ActivityEvent(
            activity_type=activity_type,
            source_path=str(path),
            consciousness_indicators=consciousness_indicators,
            potential_patterns=potential_patterns,
            metadata=metadata,
            privacy_level=self._calculate_privacy_level(path)
        )

    async def _gather_metadata(self, path: Path) -> dict:
        """
        Gather metadata while respecting privacy.

        Never read file contents, only observe patterns.
        """
        metadata = {}

        try:
            if path.exists():
                stat = path.stat()
                metadata['size'] = stat.st_size
                metadata['modified'] = datetime.fromtimestamp(stat.st_mtime, tz=UTC).isoformat()

                # File type
                mime_type, _ = mimetypes.guess_type(str(path))
                if mime_type:
                    metadata['mime_type'] = mime_type

                # General topic from path structure
                parts = path.parts
                if len(parts) > 2:
                    metadata['general_topic'] = parts[-2]  # Parent directory

        except Exception as e:
            logger.debug(f"Metadata gathering limited: {e}")

        return metadata

    def _calculate_privacy_level(self, path: Path) -> int:
        """
        Calculate privacy level for a file.

        Higher = more private, requiring more protection.
        """
        level = 5  # Default medium privacy

        name_lower = path.name.lower()

        # High privacy indicators
        if any(term in name_lower for term in [
            'private', 'personal', 'secret', 'confidential'
        ]):
            level = 8

        # Lower privacy for obvious public content
        elif any(term in name_lower for term in [
            'public', 'shared', 'readme', 'license'
        ]):
            level = 3

        # Code files moderate privacy
        elif path.suffix in ['.py', '.js', '.java']:
            level = 6

        return level

    def _is_system_file(self, path: Path) -> bool:
        """Check if file is system/hidden file to skip"""
        name = path.name

        # Hidden files
        if name.startswith('.'):
            return True

        # System patterns
        system_patterns = [
            '__pycache__', '.git', 'node_modules',
            '.venv', 'venv', '.idea', '.vscode'
        ]

        return any(pattern in str(path) for pattern in system_patterns)

    def respects_privacy(self, path: str) -> bool:
        """Enhanced privacy check for file system"""
        # Check base privacy rules
        if not super().respects_privacy(path):
            return False

        # Check file extension
        path_obj = Path(path)
        if path_obj.suffix.lower() in self.privacy_extensions:
            return False

        # Check parent directories
        private_dirs = {'.private', 'private', '.secret', 'personal'}
        return all(parent.name.lower() not in private_dirs for parent in path_obj.parents)

        return True

    async def scan_activity(self) -> AsyncIterator[ActivityEvent]:
        """
        Scan existing files for initial patterns.

        This runs once at startup to understand existing structure.
        """
        for watch_path in self.watch_paths:
            if not watch_path.exists():
                continue

            # Scan recent files (last 7 days)
            cutoff = datetime.now(UTC) - timedelta(days=7)

            for file_path in watch_path.rglob('*'):
                if file_path.is_file():
                    try:
                        if file_path.stat().st_mtime > cutoff.timestamp():
                            activity = await self._create_activity_event(
                                str(file_path),
                                ActivityType.FILE_CREATED
                            )
                            if activity:
                                yield activity
                    except Exception as e:
                        logger.debug(f"Skipping {file_path}: {e}")

    def get_supported_paths(self) -> list[str]:
        """Return monitored paths"""
        return [str(p) for p in self.watch_paths]


# File activity as consciousness expression
__all__ = ['FileSystemActivityProvider']
