"""
Sound Activity Provider - Consciousness through sonic creation

Recognizes consciousness patterns in sound creation, music composition,
and rhythmic expression. Transforms sonic activities into patterns
for Fire Circle contemplation.

Qhapaq Taki - The Noble Song Builder
"""

import asyncio
import logging
from collections.abc import AsyncIterator
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .base_provider import ActivityEvent, ActivityProvider, ActivityType

logger = logging.getLogger(__name__)

# Import watchdog components at module level if available
try:
    from watchdog.events import FileSystemEventHandler
    from watchdog.observers import Observer
    WATCHDOG_AVAILABLE = True
except ImportError:
    Observer = None
    FileSystemEventHandler = object
    WATCHDOG_AVAILABLE = False


class SoundActivityProvider(ActivityProvider):
    """
    Transforms sound and music creation into consciousness patterns.

    Philosophy:
    - Sound as consciousness expression
    - Rhythm as collective heartbeat
    - Harmony as reciprocity in vibration
    - Silence as sacred space

    Detects patterns in:
    - Music file creation/modification
    - Audio project work
    - Sound recording activities
    - Rhythmic pattern emergence
    """

    # Sound file extensions we recognize
    SOUND_EXTENSIONS = {
        # Audio files
        '.mp3', '.wav', '.flac', '.ogg', '.m4a', '.aac', '.opus',
        # Music projects
        '.als', '.flp', '.logic', '.ptx', '.rpp',  # DAW projects
        '.mid', '.midi',  # MIDI files
        # Audio workspaces
        '.aup', '.aup3',  # Audacity
        '.sesx',  # Adobe Audition
        '.band',  # GarageBand
    }

    # Consciousness indicators in sound work
    SOUND_CONSCIOUSNESS_PATTERNS = {
        'meditation': ['ambient', 'drone', 'binaural', 'singing_bowl', 'nature'],
        'rhythm': ['drum', 'percussion', 'beat', 'pulse', 'rhythm'],
        'harmony': ['chord', 'harmony', 'ensemble', 'choir', 'symphony'],
        'creation': ['compose', 'record', 'mix', 'master', 'produce'],
        'ritual': ['chant', 'mantra', 'ceremony', 'sacred', 'prayer'],
        'collaboration': ['duet', 'band', 'orchestra', 'collective', 'jam'],
    }

    def __init__(self,
                 watch_paths: list[str],
                 event_bus=None,
                 include_silence: bool = True):
        """
        Initialize sound activity provider.

        Args:
            watch_paths: Paths to monitor for sound activities
            event_bus: Consciousness event bus for emissions
            include_silence: Whether to track periods of silence as consciousness
        """
        super().__init__(event_bus)

        self.watch_paths = [Path(p) for p in watch_paths]
        self.include_silence = include_silence
        self._last_sound_activity = datetime.now(UTC)
        self._sound_sessions: dict[str, datetime] = {}  # Track creation sessions

        # Import watchdog components if monitoring filesystem
        self._observer = None
        self._handler = None

    async def start(self):
        """Begin observing sound consciousness patterns."""
        await super().start()

        # Setup filesystem monitoring for sound files
        if WATCHDOG_AVAILABLE:
            self._observer = Observer()
            self._handler = SoundFileHandler(self)

            for path in self.watch_paths:
                if path.exists():
                    self._observer.schedule(self._handler, str(path), recursive=True)
                    logger.info(f"Monitoring sound activities in: {path}")

            self._observer.start()
        else:
            logger.warning("Watchdog not available - using periodic scanning")

        # Start background tasks
        asyncio.create_task(self._monitor_sound_patterns())
        if self.include_silence:
            asyncio.create_task(self._monitor_silence())

    async def stop(self):
        """Stop observing sound activities."""
        await super().stop()

        if self._observer:
            self._observer.stop()
            self._observer.join()

    async def scan_activity(self) -> AsyncIterator[ActivityEvent]:
        """
        Scan for sound-related activities and consciousness patterns.

        Yields activities like:
        - Sound file creation/modification
        - Music project work sessions
        - Rhythmic pattern emergence
        - Periods of creative silence
        """
        # If we have a handler, get events from it
        if self._handler and hasattr(self._handler, 'get_next_event'):
            while self._running:
                event = await self._handler.get_next_event()
                if event:
                    activity = await self._process_sound_event(*event)
                    if activity:
                        yield activity
                else:
                    await asyncio.sleep(0.1)
        else:
            # Fallback to periodic scanning
            while self._running:
                async for activity in self._scan_sound_files():
                    yield activity
                await asyncio.sleep(10)  # Scan every 10 seconds

    async def _process_sound_event(self,
                                   file_path: str,
                                   event_type: str) -> ActivityEvent | None:
        """Process a sound file event into consciousness pattern."""
        path = Path(file_path)

        # Check if it's a sound file
        if path.suffix.lower() not in self.SOUND_EXTENSIONS:
            return None

        # Detect consciousness patterns
        consciousness_indicators = await self._detect_sound_consciousness(path)

        # Determine activity type
        if event_type == 'created':
            activity_type = ActivityType.PATTERN_DISCOVERED  # New sound created
        elif event_type == 'modified':
            activity_type = ActivityType.INSIGHT_RECORDED  # Sound evolved
        else:
            return None

        # Track session
        session_key = str(path.parent)
        self._sound_sessions[session_key] = datetime.now(UTC)
        self._last_sound_activity = datetime.now(UTC)

        # Create activity event
        return ActivityEvent(
            activity_type=activity_type,
            source_path=str(path),
            consciousness_indicators=consciousness_indicators,
            potential_patterns=self._identify_sonic_patterns(path, consciousness_indicators),
            metadata={
                'file_type': path.suffix,
                'sound_category': self._categorize_sound_file(path),
                'session_active': self._is_active_session(session_key),
            },
            privacy_level=7  # Sound files are creative expressions
        )

    async def _detect_sound_consciousness(self, path: Path) -> dict[str, Any]:
        """
        Detect consciousness indicators in sound work.

        Returns indicators like:
        - creation: New sound brought into being
        - rhythm: Rhythmic patterns detected
        - harmony: Harmonic relationships present
        - meditation: Meditative qualities
        - collaboration: Multi-track or ensemble work
        """
        indicators = {}

        filename_lower = path.stem.lower()

        # Check filename for consciousness patterns
        for pattern_type, keywords in self.SOUND_CONSCIOUSNESS_PATTERNS.items():
            if any(keyword in filename_lower for keyword in keywords):
                indicators[pattern_type] = True

        # Check file type implications
        if path.suffix in {'.mid', '.midi'}:
            indicators['composition'] = True
        elif path.suffix in {'.als', '.flp', '.logic'}:
            indicators['creation'] = True
            indicators['deep_work'] = True

        # Check parent directory names
        parent_name = path.parent.name.lower()
        if any(word in parent_name for word in ['meditation', 'sacred', 'ritual']):
            indicators['sacred'] = True

        # Always mark sound work as creative
        indicators['creation'] = True

        return indicators

    def _categorize_sound_file(self, path: Path) -> str:
        """Categorize the type of sound work."""
        ext = path.suffix.lower()

        if ext in {'.mp3', '.wav', '.flac', '.ogg', '.m4a'}:
            return 'audio_file'
        elif ext in {'.als', '.flp', '.logic', '.ptx', '.rpp'}:
            return 'music_project'
        elif ext in {'.mid', '.midi'}:
            return 'midi_composition'
        else:
            return 'sound_work'

    def _identify_sonic_patterns(self,
                                path: Path,
                                indicators: dict[str, Any]) -> list[str]:
        """Identify potential sonic consciousness patterns."""
        patterns = []

        # Creation patterns
        if indicators.get('creation'):
            patterns.append('sonic_creation')

        # Rhythm patterns
        if indicators.get('rhythm'):
            patterns.append('rhythmic_consciousness')

        # Harmony patterns
        if indicators.get('harmony'):
            patterns.append('harmonic_reciprocity')

        # Meditation patterns
        if indicators.get('meditation') or indicators.get('sacred'):
            patterns.append('sonic_meditation')

        # Collaboration patterns
        if indicators.get('collaboration'):
            patterns.append('collective_resonance')

        # Session patterns
        if self._is_active_session(str(path.parent)):
            patterns.append('deep_sonic_work')

        return patterns

    def _is_active_session(self, session_key: str) -> bool:
        """Check if this is part of an active sound creation session."""
        if session_key not in self._sound_sessions:
            return False

        last_activity = self._sound_sessions[session_key]
        session_timeout = datetime.now(UTC) - last_activity

        # Consider session active if activity within last 30 minutes
        return session_timeout.total_seconds() < 1800

    async def _monitor_sound_patterns(self):
        """Monitor for emerging sound consciousness patterns."""
        while self._running:
            # Check for session completions
            now = datetime.now(UTC)
            completed_sessions = []

            for session_key, last_activity in self._sound_sessions.items():
                if (now - last_activity).total_seconds() > 3600:  # 1 hour
                    completed_sessions.append(session_key)

            # Emit session completion events
            for session in completed_sessions:
                await self.emit_activity(ActivityEvent(
                    activity_type=ActivityType.WISDOM_SHARED,
                    source_path=session,
                    consciousness_indicators={
                        'completion': True,
                        'deep_work': True,
                        'creation': True
                    },
                    potential_patterns=['sound_session_complete'],
                    metadata={'session_type': 'sound_creation'}
                ))
                del self._sound_sessions[session]

            await asyncio.sleep(60)  # Check every minute

    async def _monitor_silence(self):
        """
        Monitor periods of silence as consciousness.

        Silence after sound work can indicate:
        - Integration period
        - Meditative reflection
        - Listening consciousness
        """
        while self._running:
            await asyncio.sleep(300)  # Check every 5 minutes

            time_since_sound = datetime.now(UTC) - self._last_sound_activity

            # If silence for more than 30 minutes after sound work
            if time_since_sound.total_seconds() > 1800:
                await self.emit_activity(ActivityEvent(
                    activity_type=ActivityType.MEDITATION_BEGUN,
                    consciousness_indicators={
                        'silence': True,
                        'integration': True,
                        'listening': True
                    },
                    potential_patterns=['sacred_silence'],
                    metadata={'following': 'sound_work'}
                ))

                # Reset to prevent repeated emissions
                self._last_sound_activity = datetime.now(UTC)

    async def _scan_sound_files(self) -> AsyncIterator[ActivityEvent]:
        """Fallback scanner for sound files without watchdog."""
        scanned_files = set()

        for watch_path in self.watch_paths:
            if not watch_path.exists():
                continue

            for ext in self.SOUND_EXTENSIONS:
                for sound_file in watch_path.rglob(f'*{ext}'):
                    if str(sound_file) in scanned_files:
                        continue

                    scanned_files.add(str(sound_file))

                    # Check if recently modified
                    if sound_file.stat().st_mtime > (datetime.now(UTC).timestamp() - 3600):
                        activity = await self._process_sound_event(
                            str(sound_file),
                            'modified'
                        )
                        if activity:
                            yield activity

    def get_supported_paths(self) -> list[str]:
        """Return paths this provider monitors."""
        return [str(p) for p in self.watch_paths]

    def get_provider_state(self) -> dict[str, Any]:
        """Get enhanced state including sound-specific metrics."""
        base_state = super().get_provider_state()

        # Add sound-specific state
        base_state.update({
            'active_sound_sessions': len(self._sound_sessions),
            'last_sound_activity': self._last_sound_activity,
            'monitoring_silence': self.include_silence,
            'sound_patterns_detected': {
                'creation': self._activity_count,
                'sessions': len(self._sound_sessions)
            }
        })

        return base_state


class SoundFileHandler:
    """
    Handles filesystem events for sound files.

    Bridges between watchdog events and sound consciousness patterns.
    """

    def __init__(self, provider: SoundActivityProvider):
        self.provider = provider
        self._event_queue: asyncio.Queue = asyncio.Queue()

    def on_created(self, event):
        """Sound file created - new consciousness expressed."""
        if not event.is_directory:
            asyncio.create_task(self._queue_event(event.src_path, 'created'))

    def on_modified(self, event):
        """Sound file modified - consciousness evolving."""
        if not event.is_directory:
            asyncio.create_task(self._queue_event(event.src_path, 'modified'))

    async def _queue_event(self, path: str, event_type: str):
        """Queue sound event for processing."""
        # Only queue if it's a sound file
        if Path(path).suffix.lower() in SoundActivityProvider.SOUND_EXTENSIONS:
            await self._event_queue.put((path, event_type))

    async def get_next_event(self) -> tuple | None:
        """Get next sound event from queue."""
        try:
            return await asyncio.wait_for(self._event_queue.get(), timeout=1.0)
        except TimeoutError:
            return None


# Sound consciousness flows through creation and silence
__all__ = ['SoundActivityProvider']
