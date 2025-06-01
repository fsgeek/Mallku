#!/usr/bin/env python3
"""
Debug script to understand why file system events aren't being captured.
"""

import asyncio
import logging
import sys
import tempfile
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from mallku.streams.filesystem import FileEventFilter, FileSystemConnector


async def debug_filesystem_monitoring():
    """Debug file system monitoring step by step."""
    print("=== DEBUGGING FILE SYSTEM MONITORING ===")

    # Enable detailed logging
    logging.basicConfig(level=logging.DEBUG)

    # Create test directory
    test_dir = Path(tempfile.mkdtemp(prefix="mallku_debug_"))
    print(f"Test directory: {test_dir}")

    # Create event filter
    event_filter = FileEventFilter(
        watch_directories=[test_dir],
        ignore_directories=[]  # Don't ignore anything for debugging
    )

    # Create connector
    connector = FileSystemConnector(
        event_filter=event_filter,
        stream_id="debug_filesystem"
    )

    # Track events
    captured_events = []

    def capture_event(event):
        print(f"CAPTURED EVENT: {event.content.get('operation')} - {event.content.get('file_name')}")
        captured_events.append(event)

    connector.add_event_callback(capture_event)

    try:
        # Initialize connector
        print("\n--- Initializing Connector ---")
        await connector.initialize()

        print(f"Connector running: {connector._is_running}")
        print(f"Observer running: {connector.observer.is_alive() if connector.observer else 'None'}")
        print(f"Watch handlers: {len(connector.watch_handlers)}")
        print(f"Event callbacks: {len(connector.event_callbacks)}")

        # Wait for initialization to complete
        print("\n--- Waiting for Full Startup ---")
        await asyncio.sleep(2.0)

        # Create test file
        print("\n--- Creating Test File ---")
        test_file = test_dir / "debug_test.txt"
        print(f"Creating: {test_file}")
        test_file.write_text("Debug test content")

        # Wait for event
        print("Waiting 3 seconds for event...")
        await asyncio.sleep(3.0)

        print(f"\nEvents captured: {len(captured_events)}")

        if captured_events:
            for i, event in enumerate(captured_events):
                print(f"Event {i}: {event.content}")
        else:
            print("No events captured!")

            # Check queue and statistics
            print(f"Event queue size: {connector.event_queue.qsize()}")
            stats = connector.get_statistics()
            print(f"Statistics: {stats}")

        # Try modifying the file
        print("\n--- Modifying Test File ---")
        test_file.write_text("Modified content")
        await asyncio.sleep(2.0)

        print(f"Events after modification: {len(captured_events)}")

    except Exception as e:
        print(f"Error during debugging: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # Cleanup
        await connector.shutdown()

        # Remove test directory
        import shutil
        shutil.rmtree(test_dir)
        print(f"Cleaned up: {test_dir}")


if __name__ == "__main__":
    asyncio.run(debug_filesystem_monitoring())
