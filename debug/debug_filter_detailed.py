#!/usr/bin/env python3
"""
Detailed debug of the filtering issue in integration service.
"""

import sys
import tempfile
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# ruff: noqa: E402
from mallku.streams.filesystem.file_event_models import (
    FileEvent,
    FileEventFilter,
    FileOperation,
)

# ruff: qa: E402


def debug_filter_in_integration_context():
    """Debug the exact filtering that happens in integration service."""
    print("=== DEBUGGING INTEGRATION FILTER ===")

    # Create test directory (simulating tmp directory like integration test)
    test_dir = Path(tempfile.mkdtemp(prefix="mallku_filter_debug_"))
    print(f"Test directory: {test_dir}")

    # Create test file
    test_file = test_dir / "debug_test.txt"
    test_file.write_text("Debug content")

    # Create FileEvent (simulating what happens in file connector)
    file_event = FileEvent.from_file_path(file_path=test_file, operation=FileOperation.CREATED)

    print("\nFileEvent created:")
    print(f"  File path: {file_event.file_path}")
    print(f"  Is temporary: {file_event.is_temporary}")
    print(f"  File category: {file_event.file_category}")

    # Create filter exactly like integration service does
    config_file_filter_config = {"test_mode": True}

    file_filter = FileEventFilter(watch_directories=[test_dir], **config_file_filter_config)

    print("\nFileEventFilter created:")
    print(f"  Test mode: {file_filter.test_mode}")
    print(f"  Watch directories: {file_filter.watch_directories}")
    print(f"  Ignore directories: {file_filter.ignore_directories}")

    # Test filtering
    should_include = file_filter.should_include_event(file_event)
    print(f"\nFiltering result: should_include = {should_include}")

    # Debug step by step
    print("\nStep-by-step analysis:")

    # Check if we're in test mode
    print(f"  1. Test mode enabled: {file_filter.test_mode}")

    if file_filter.test_mode:
        # Directory check
        if file_filter.watch_directories:
            dir_match = any(
                file_event.directory_path.is_relative_to(watch_dir)
                for watch_dir in file_filter.watch_directories
            )
            print(f"  2. Directory match: {dir_match}")
            if not dir_match:
                print(
                    f"     FAILED: {file_event.directory_path} not relative to {file_filter.watch_directories}"
                )

        # Ignore directories check in test mode
        for ignore_dir in file_filter.ignore_directories:
            if ignore_dir.lower() in str(file_event.directory_path).lower():
                print(f"     FAILED: Directory contains ignored pattern '{ignore_dir}'")
                should_include = False

        # Operation check
        if file_event.operation not in file_filter.include_operations:
            print(
                f"     FAILED: Operation {file_event.operation} not in {file_filter.include_operations}"
            )
            should_include = False
        else:
            print(
                f"  3. Operation check passed: {file_event.operation} in {file_filter.include_operations}"
            )

    print(f"\nFINAL RESULT: should_include = {should_include}")

    # Clean up
    import shutil

    shutil.rmtree(test_dir)
    print(f"Cleaned up: {test_dir}")


if __name__ == "__main__":
    debug_filter_in_integration_context()
