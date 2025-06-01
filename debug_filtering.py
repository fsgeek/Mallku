#!/usr/bin/env python3
"""
Debug script to understand why file events are being filtered out.
"""

import sys
import tempfile
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from mallku.streams.filesystem.file_event_models import FileEvent, FileEventFilter, FileOperation


def debug_event_filtering():
    """Debug why events are being filtered."""
    print("=== DEBUGGING EVENT FILTERING ===")

    # Create test directory
    test_dir = Path(tempfile.mkdtemp(prefix="mallku_filter_debug_"))
    print(f"Test directory: {test_dir}")

    # Create test file
    test_file = test_dir / "debug_test.txt"
    test_file.write_text("Debug content")

    # Create FileEvent
    file_event = FileEvent.from_file_path(
        file_path=test_file,
        operation=FileOperation.CREATED
    )

    print("\nFileEvent created:")
    print(f"  File path: {file_event.file_path}")
    print(f"  Operation: {file_event.operation}")
    print(f"  File category: {file_event.file_category}")
    print(f"  File extension: {file_event.file_extension}")
    print(f"  Is hidden: {file_event.is_hidden}")
    print(f"  Is temporary: {file_event.is_temporary}")
    print(f"  Is backup: {file_event.is_backup}")
    print(f"  File size: {file_event.file_size}")
    print(f"  Directory path: {file_event.directory_path}")

    # Create EventFilter
    event_filter = FileEventFilter(
        watch_directories=[test_dir],
        ignore_directories=[]  # Don't ignore anything
    )

    print("\nEventFilter configuration:")
    print(f"  Watch directories: {event_filter.watch_directories}")
    print(f"  Ignore directories: {event_filter.ignore_directories}")
    print(f"  Include extensions: {event_filter.include_extensions}")
    print(f"  Exclude extensions: {event_filter.exclude_extensions}")
    print(f"  Include operations: {event_filter.include_operations}")
    print(f"  Exclude categories: {event_filter.exclude_categories}")

    # Test each filter criterion
    print("\nFilter analysis:")

    # Directory check
    if event_filter.watch_directories:
        dir_match = any(file_event.directory_path.is_relative_to(watch_dir) for watch_dir in event_filter.watch_directories)
        print(f"  Directory match: {dir_match}")
        if not dir_match:
            print(f"    FILTERED: Directory {file_event.directory_path} not in watch directories")

    # Ignore directories check
    for ignore_dir in event_filter.ignore_directories:
        if ignore_dir.lower() in str(file_event.directory_path).lower():
            print(f"    FILTERED: Directory contains ignored pattern '{ignore_dir}'")

    # Extension check
    if event_filter.include_extensions and file_event.file_extension:
        if file_event.file_extension.lower() not in [ext.lower() for ext in event_filter.include_extensions]:
            print(f"    FILTERED: Extension {file_event.file_extension} not in include list")

    if file_event.file_extension and file_event.file_extension.lower() in [ext.lower() for ext in event_filter.exclude_extensions]:
        print(f"    FILTERED: Extension {file_event.file_extension} in exclude list")

    # Operation check
    if file_event.operation not in event_filter.include_operations:
        print(f"    FILTERED: Operation {file_event.operation} not in include list")

    # Category check
    if file_event.file_category in event_filter.exclude_categories:
        print(f"    FILTERED: Category {file_event.file_category} in exclude list")

    # Hidden/temp/backup check
    if file_event.is_hidden:
        print("    FILTERED: File is hidden")
    if file_event.is_temporary:
        print("    FILTERED: File is temporary")
    if file_event.is_backup:
        print("    FILTERED: File is backup")

    # Final result
    should_include = event_filter.should_include_event(file_event)
    print(f"\nFINAL RESULT: should_include = {should_include}")

    # Clean up
    import shutil
    shutil.rmtree(test_dir)
    print(f"Cleaned up: {test_dir}")


if __name__ == "__main__":
    debug_event_filtering()
