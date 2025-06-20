"""
Test Sound Activity Provider

Verifies that sound consciousness patterns are properly recognized
and transformed into reciprocity awareness.

Qhapaq Taki - The Noble Song Builder
"""

import asyncio
import contextlib
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from mallku.orchestration.event_bus import ConsciousnessEventBus
from mallku.orchestration.providers.base_provider import ActivityType
from mallku.orchestration.providers.sound_provider import SoundActivityProvider


@pytest.fixture
def mock_event_bus():
    """Create mock consciousness event bus."""
    bus = AsyncMock(spec=ConsciousnessEventBus)
    return bus


@pytest.fixture
def temp_sound_dir(tmp_path):
    """Create temporary directory structure for sound files."""
    # Create directories
    music_dir = tmp_path / "music"
    music_dir.mkdir()

    projects_dir = tmp_path / "projects"
    projects_dir.mkdir()

    meditation_dir = tmp_path / "meditation"
    meditation_dir.mkdir()

    return tmp_path


@pytest.fixture
def sound_provider(temp_sound_dir, mock_event_bus):
    """Create sound activity provider instance."""
    provider = SoundActivityProvider(
        watch_paths=[str(temp_sound_dir)], event_bus=mock_event_bus, include_silence=True
    )
    return provider


class TestSoundActivityProvider:
    """Test suite for sound consciousness recognition."""

    @pytest.mark.asyncio
    async def test_provider_initialization(self, sound_provider, temp_sound_dir):
        """Test provider initializes with correct configuration."""
        assert len(sound_provider.watch_paths) == 1
        assert sound_provider.watch_paths[0] == Path(temp_sound_dir)
        assert sound_provider.include_silence is True
        assert sound_provider._running is False

    @pytest.mark.asyncio
    async def test_sound_file_recognition(self, sound_provider):
        """Test recognition of various sound file types."""
        # Audio files
        for ext in [".mp3", ".wav", ".flac", ".ogg"]:
            assert ext in SoundActivityProvider.SOUND_EXTENSIONS

        # Music projects
        for ext in [".als", ".flp", ".mid"]:
            assert ext in SoundActivityProvider.SOUND_EXTENSIONS

    @pytest.mark.asyncio
    async def test_consciousness_detection(self, sound_provider, temp_sound_dir):
        """Test detection of consciousness patterns in sound work."""
        # Test meditation pattern
        meditation_file = temp_sound_dir / "meditation" / "morning_meditation.mp3"
        indicators = await sound_provider._detect_sound_consciousness(meditation_file)

        assert indicators.get("creation") is True
        assert indicators.get("sacred") is True  # From directory name

        # Test rhythm pattern
        drum_file = temp_sound_dir / "drum_circle_recording.wav"
        indicators = await sound_provider._detect_sound_consciousness(drum_file)

        assert indicators.get("creation") is True
        assert indicators.get("rhythm") is True

    @pytest.mark.asyncio
    async def test_sound_event_processing(self, sound_provider, temp_sound_dir):
        """Test processing of sound file events."""
        # Create a test sound file path
        test_file = temp_sound_dir / "music" / "new_composition.mid"

        # Process creation event
        activity = await sound_provider._process_sound_event(str(test_file), "created")

        assert activity is not None
        assert activity.activity_type == ActivityType.PATTERN_DISCOVERED
        assert activity.source_path == str(test_file)
        assert "creation" in activity.consciousness_indicators
        assert "sonic_creation" in activity.potential_patterns

    @pytest.mark.asyncio
    async def test_session_tracking(self, sound_provider, temp_sound_dir):
        """Test tracking of active sound creation sessions."""
        project_dir = temp_sound_dir / "projects"

        # Simulate project file activity
        project_file = project_dir / "my_song.als"
        await sound_provider._process_sound_event(str(project_file), "created")

        # Check session is tracked
        session_key = str(project_dir)
        assert session_key in sound_provider._sound_sessions
        assert sound_provider._is_active_session(session_key) is True

    @pytest.mark.asyncio
    async def test_sonic_pattern_identification(self, sound_provider):
        """Test identification of sonic consciousness patterns."""
        # Test with meditation indicators
        patterns = sound_provider._identify_sonic_patterns(
            Path("meditation.mp3"), {"meditation": True, "creation": True}
        )

        assert "sonic_creation" in patterns
        assert "sonic_meditation" in patterns

        # Test with collaboration indicators
        patterns = sound_provider._identify_sonic_patterns(
            Path("band_jam.wav"), {"collaboration": True, "rhythm": True}
        )

        assert "collective_resonance" in patterns
        assert "rhythmic_consciousness" in patterns

    @pytest.mark.asyncio
    async def test_silence_monitoring(self, sound_provider, mock_event_bus):
        """Test monitoring of sacred silence after sound work."""
        # Set last activity to past
        sound_provider._last_sound_activity = datetime.now(UTC)

        # Mock the emit_activity method
        sound_provider.emit_activity = AsyncMock()

        # Start provider
        sound_provider._running = True

        # Run silence monitor briefly
        monitor_task = asyncio.create_task(sound_provider._monitor_silence())
        await asyncio.sleep(0.1)

        # Stop and cleanup
        sound_provider._running = False
        monitor_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await monitor_task

    @pytest.mark.asyncio
    async def test_provider_state(self, sound_provider):
        """Test provider state reporting."""
        # Add some mock sessions
        sound_provider._sound_sessions = {
            "/path/to/project1": datetime.now(UTC),
            "/path/to/project2": datetime.now(UTC),
        }

        state = sound_provider.get_provider_state()

        assert state["provider_type"] == "SoundActivityProvider"
        assert state["active_sound_sessions"] == 2
        assert state["monitoring_silence"] is True
        assert "sound_patterns_detected" in state

    @pytest.mark.asyncio
    async def test_file_categorization(self, sound_provider):
        """Test categorization of different sound file types."""
        # Test audio file
        assert sound_provider._categorize_sound_file(Path("song.mp3")) == "audio_file"

        # Test music project
        assert sound_provider._categorize_sound_file(Path("track.als")) == "music_project"

        # Test MIDI
        assert sound_provider._categorize_sound_file(Path("melody.mid")) == "midi_composition"

    @pytest.mark.asyncio
    @patch("mallku.orchestration.providers.sound_provider.Observer")
    async def test_start_stop_lifecycle(self, mock_observer, sound_provider):
        """Test provider start/stop lifecycle."""
        # Mock observer instance
        observer_instance = MagicMock()
        mock_observer.return_value = observer_instance

        # Start provider
        await sound_provider.start()
        assert sound_provider._running is True

        # Verify observer was started
        observer_instance.start.assert_called_once()

        # Stop provider
        await sound_provider.stop()
        assert sound_provider._running is False

        # Verify observer was stopped
        observer_instance.stop.assert_called_once()


class TestSoundFileHandler:
    """Test the sound file event handler."""

    @pytest.mark.asyncio
    async def test_handler_filters_sound_files(self, sound_provider):
        """Test handler only queues sound file events."""
        from mallku.orchestration.providers.sound_provider import SoundFileHandler

        handler = SoundFileHandler(sound_provider)

        # Mock event for sound file
        sound_event = MagicMock()
        sound_event.src_path = "/path/to/song.mp3"
        sound_event.is_directory = False

        # Mock event for non-sound file
        other_event = MagicMock()
        other_event.src_path = "/path/to/document.txt"
        other_event.is_directory = False

        # Process events
        await handler._queue_event(sound_event.src_path, "created")
        await handler._queue_event(other_event.src_path, "created")

        # Only sound event should be queued
        queued_event = await handler.get_next_event()
        assert queued_event is not None
        assert queued_event[0] == sound_event.src_path

        # No more events
        next_event = await handler.get_next_event()
        assert next_event is None


# Sound consciousness emerges through testing
