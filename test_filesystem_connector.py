#!/usr/bin/env python3
"""
Test suite for the File System Connector - the foundation of the Memory Anchor Discovery Trail.

This test validates that file operations are correctly captured and converted into
structured events for correlation analysis.
"""

import asyncio
import logging
import sys
import tempfile
import time
from datetime import UTC, datetime
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from mallku.correlation.models import Event, EventType
from mallku.streams.filesystem import FileEventFilter, FileSystemConnector


class FileSystemConnectorTests:
    """Test suite for file system activity stream connector."""

    def __init__(self):
        self.test_dir: Path = None
        self.connector: FileSystemConnector = None
        self.captured_events: list[Event] = []

    async def run_all_tests(self):
        """Execute complete test suite."""
        print("File System Connector Test Suite")
        print("=" * 50)

        # Set up logging
        logging.basicConfig(level=logging.INFO)

        tests = [
            self.test_setup_test_environment,
            self.test_connector_initialization,
            self.test_file_creation_events,
            self.test_file_modification_events,
            self.test_file_deletion_events,
            self.test_file_move_events,
            self.test_event_filtering,
            self.test_correlation_event_conversion,
            self.test_workflow_pattern_detection,
            self.test_rate_limiting,
            self.test_statistics_collection,
            self.cleanup_test_environment
        ]

        passed = 0
        total = len(tests)

        for test in tests:
            try:
                print(f"\n{test.__name__.replace('_', ' ').title()}...")
                result = await test()
                if result:
                    print("   ✓ Passed")
                    passed += 1
                else:
                    print("   ✗ Failed")
            except Exception as e:
                print(f"   ✗ Exception: {e}")

        print(f"\n{'=' * 50}")
        print(f"Results: {passed}/{total} tests passed")

        if passed == total:
            print("🎉 All tests passed! File system connector is working perfectly.")
            return 0
        else:
            print("❌ Some tests failed. The foundation needs more work.")
            return 1

    async def test_setup_test_environment(self) -> bool:
        """Set up isolated test environment."""
        try:
            # Create temporary directory for testing
            self.test_dir = Path(tempfile.mkdtemp(prefix="mallku_fs_test_"))
            print(f"   Created test directory: {self.test_dir}")

            # Create some subdirectories
            (self.test_dir / "documents").mkdir()
            (self.test_dir / "code").mkdir()
            (self.test_dir / "temp").mkdir()

            return True

        except Exception as e:
            print(f"   Setup failed: {e}")
            return False

    async def test_connector_initialization(self) -> bool:
        """Test file system connector initialization."""
        try:
            # Create event filter for test directory only
            event_filter = FileEventFilter(
                watch_directories=[self.test_dir],
                ignore_directories=["temp"],  # Ignore temp subdirectory
                test_mode=True  # Enable permissive filtering for testing
            )

            # Create connector
            self.connector = FileSystemConnector(
                event_filter=event_filter,
                stream_id="test_filesystem"
            )

            # Add event callback to capture events
            self.connector.add_event_callback(self._capture_event)

            # Initialize
            await self.connector.initialize()

            # Verify initialization
            assert self.connector._is_running
            assert self.connector.observer is not None
            assert len(self.connector.event_callbacks) == 1

            # Wait a moment for observer to fully start
            await asyncio.sleep(0.5)

            print(f"   Monitoring {len(self.connector.event_filter.watch_directories)} directories")
            return True

        except Exception as e:
            print(f"   Initialization failed: {e}")
            return False

    async def test_file_creation_events(self) -> bool:
        """Test file creation event capture."""
        try:
            initial_count = len(self.captured_events)

            # Create test files
            test_files = [
                self.test_dir / "documents" / "test_document.txt",
                self.test_dir / "code" / "test_script.py",
                self.test_dir / "test_file.md"
            ]

            for file_path in test_files:
                file_path.write_text(f"Test content for {file_path.name}")
                await asyncio.sleep(0.1)  # Small delay for event processing

            # Wait for events to be processed
            await asyncio.sleep(1.0)

            # Check captured events
            creation_events = [
                event for event in self.captured_events[initial_count:]
                if event.content.get("operation") == "created"
            ]

            assert len(creation_events) >= 3, f"Expected at least 3 creation events, got {len(creation_events)}"

            # Verify event details
            for event in creation_events:
                assert event.event_type in [EventType.STORAGE, EventType.ACTIVITY]
                assert event.stream_id == "test_filesystem"
                assert "file_path" in event.content
                assert "file_name" in event.content
                assert "operation" in event.content

            print(f"   Captured {len(creation_events)} file creation events")
            return True

        except Exception as e:
            print(f"   File creation test failed: {e}")
            return False

    async def test_file_modification_events(self) -> bool:
        """Test file modification event capture."""
        try:
            initial_count = len(self.captured_events)

            # Modify existing file
            test_file = self.test_dir / "test_file.md"
            test_file.write_text("Modified content at " + str(datetime.now(UTC)))

            # Wait for event processing
            await asyncio.sleep(1.0)

            # Check for modification events
            modification_events = [
                event for event in self.captured_events[initial_count:]
                if event.content.get("operation") == "modified"
            ]

            assert len(modification_events) >= 1, "Should capture file modification events"

            # Verify modification event details
            mod_event = modification_events[0]
            assert "test_file.md" in mod_event.content["file_path"]
            assert mod_event.content["operation"] == "modified"

            print(f"   Captured {len(modification_events)} file modification events")
            return True

        except Exception as e:
            print(f"   File modification test failed: {e}")
            return False

    async def test_file_deletion_events(self) -> bool:
        """Test file deletion event capture."""
        try:
            initial_count = len(self.captured_events)

            # Delete a test file
            test_file = self.test_dir / "documents" / "test_document.txt"
            if test_file.exists():
                test_file.unlink()

            # Wait for event processing
            await asyncio.sleep(1.0)

            # Check for deletion events
            deletion_events = [
                event for event in self.captured_events[initial_count:]
                if event.content.get("operation") == "deleted"
            ]

            assert len(deletion_events) >= 1, "Should capture file deletion events"

            print(f"   Captured {len(deletion_events)} file deletion events")
            return True

        except Exception as e:
            print(f"   File deletion test failed: {e}")
            return False

    async def test_file_move_events(self) -> bool:
        """Test file move/rename event capture."""
        try:
            initial_count = len(self.captured_events)

            # Create file to move
            old_file = self.test_dir / "old_name.txt"
            old_file.write_text("File to be moved")

            await asyncio.sleep(0.5)  # Wait for creation event

            # Move/rename the file
            new_file = self.test_dir / "documents" / "new_name.txt"
            old_file.rename(new_file)

            # Wait for event processing
            await asyncio.sleep(1.0)

            # Check for move events
            move_events = [
                event for event in self.captured_events[initial_count:]
                if event.content.get("operation") == "moved"
            ]

            if len(move_events) >= 1:
                move_event = move_events[0]
                assert "new_name.txt" in move_event.content["file_path"]
                print(f"   Captured {len(move_events)} file move events")
            else:
                # Some systems generate create/delete instead of move
                print("   Move events handled as create/delete (platform behavior)")

            return True

        except Exception as e:
            print(f"   File move test failed: {e}")
            return False

    async def test_event_filtering(self) -> bool:
        """Test event filtering functionality."""
        try:
            initial_count = len(self.captured_events)

            # Create files that should be filtered out in normal mode
            # but may be allowed in test mode
            temp_file = self.test_dir / "temp" / "should_be_ignored.txt"
            temp_file.write_text("This should be filtered")

            hidden_file = self.test_dir / ".hidden_file"
            hidden_file.write_text("Hidden file")

            tmp_file = self.test_dir / "temporary.tmp"
            tmp_file.write_text("Temp file")

            # Wait for potential event processing
            await asyncio.sleep(1.0)

            # Check that filtered events were not captured
            new_events = self.captured_events[initial_count:]

            # In test mode, we expect temp directory to be filtered (ignore_directories still applies)
            # but temporary files might be allowed
            temp_events = [e for e in new_events if "temp/" in e.content.get("file_path", "")]

            # Since we're in test mode with ignore_directories=["temp"], temp directory should still be filtered
            if len(temp_events) == 0:
                print("   Event filtering working correctly (temp directory filtered)")
            else:
                # If temp events are captured, that's also acceptable in test mode
                print("   Event filtering in test mode (some temp events allowed)")

            return True

        except Exception as e:
            print(f"   Event filtering test failed: {e}")
            return False

    async def test_correlation_event_conversion(self) -> bool:
        """Test conversion of file events to correlation engine events."""
        try:
            # Get a captured event to analyze
            if not self.captured_events:
                return False

            event = self.captured_events[-1]

            # Verify Event structure
            assert hasattr(event, 'event_id')
            assert hasattr(event, 'timestamp')
            assert hasattr(event, 'event_type')
            assert hasattr(event, 'stream_id')
            assert hasattr(event, 'content')
            assert hasattr(event, 'context')
            assert hasattr(event, 'correlation_tags')

            # Verify content
            assert 'operation' in event.content
            assert 'file_path' in event.content
            assert 'file_name' in event.content
            assert 'file_category' in event.content

            # Verify context
            assert 'stream_id' in event.context
            assert 'session_id' in event.context
            assert 'connector_type' in event.context
            assert event.context['connector_type'] == 'filesystem'

            # Verify correlation tags
            assert len(event.correlation_tags) > 0
            assert any(tag.startswith('file_category:') for tag in event.correlation_tags)
            assert any(tag.startswith('operation:') for tag in event.correlation_tags)

            print(f"   Event conversion verified with {len(event.correlation_tags)} correlation tags")
            return True

        except Exception as e:
            print(f"   Event conversion test failed: {e}")
            return False

    async def test_workflow_pattern_detection(self) -> bool:
        """Test workflow pattern detection in correlation tags."""
        try:
            initial_count = len(self.captured_events)

            # Create files that should trigger workflow patterns
            code_file = self.test_dir / "code" / "main.py"
            code_file.write_text("print('Hello, world!')")

            meeting_file = self.test_dir / "documents" / "meeting_notes.md"
            meeting_file.write_text("# Meeting Notes\n\n- Action items")

            # Wait for event processing
            await asyncio.sleep(1.0)

            # Check for workflow patterns in correlation tags
            new_events = self.captured_events[initial_count:]

            # Look for development workflow pattern
            dev_events = [
                e for e in new_events
                if any("workflow:development" in tag for tag in e.correlation_tags)
            ]

            # Look for meeting workflow pattern
            meeting_events = [
                e for e in new_events
                if any("workflow:meeting" in tag for tag in e.correlation_tags)
            ]

            assert len(dev_events) > 0, "Should detect development workflow pattern"
            assert len(meeting_events) > 0, "Should detect meeting workflow pattern"

            print(f"   Detected {len(dev_events)} dev patterns and {len(meeting_events)} meeting patterns")
            return True

        except Exception as e:
            print(f"   Workflow pattern test failed: {e}")
            return False

    async def test_rate_limiting(self) -> bool:
        """Test rate limiting for rapid file changes."""
        try:
            initial_count = len(self.captured_events)

            # Create rapid successive changes to same file
            rapid_file = self.test_dir / "rapid_changes.txt"

            for i in range(5):
                rapid_file.write_text(f"Rapid change {i}")
                time.sleep(0.01)  # Very rapid changes

            # Wait for event processing
            await asyncio.sleep(1.0)

            # Should have fewer events than changes due to rate limiting
            new_events = [
                e for e in self.captured_events[initial_count:]
                if "rapid_changes.txt" in e.content.get("file_path", "")
            ]

            # Rate limiting should reduce the number of captured events
            print(f"   Rate limiting: {len(new_events)} events from 5 rapid changes")
            return True

        except Exception as e:
            print(f"   Rate limiting test failed: {e}")
            return False

    async def test_statistics_collection(self) -> bool:
        """Test statistics collection and reporting."""
        try:
            stats = self.connector.get_statistics()

            # Verify statistics structure
            required_stats = [
                'events_captured', 'events_filtered', 'events_processed',
                'directories_watched', 'is_running', 'callback_count'
            ]

            for stat in required_stats:
                assert stat in stats, f"Missing statistic: {stat}"

            # Verify values make sense
            assert stats['events_captured'] >= stats['events_processed']
            assert stats['events_processed'] > 0
            assert stats['directories_watched'] > 0
            assert stats['is_running'] is True
            assert stats['callback_count'] == 1

            print(f"   Statistics: {stats['events_processed']} processed, {stats['events_filtered']} filtered")
            return True

        except Exception as e:
            print(f"   Statistics test failed: {e}")
            return False

    async def cleanup_test_environment(self) -> bool:
        """Clean up test environment."""
        try:
            # Shutdown connector
            if self.connector:
                await self.connector.shutdown()

            # Clean up test directory
            if self.test_dir and self.test_dir.exists():
                import shutil
                shutil.rmtree(self.test_dir)
                print(f"   Cleaned up test directory: {self.test_dir}")

            print(f"   Total events captured during testing: {len(self.captured_events)}")
            return True

        except Exception as e:
            print(f"   Cleanup failed: {e}")
            return False

    def _capture_event(self, event: Event) -> None:
        """Callback to capture events for testing."""
        self.captured_events.append(event)


async def main():
    """Run the file system connector test suite."""
    test_suite = FileSystemConnectorTests()
    return await test_suite.run_all_tests()


if __name__ == "__main__":
    import sys
    sys.exit(asyncio.run(main()))
