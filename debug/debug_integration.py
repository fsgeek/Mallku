#!/usr/bin/env python3
"""
Debug script for the Integration Service to understand event flow.
"""

import asyncio
import logging
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# ruff: noqa: E402
from mallku.integration import EndToEndIntegrationService, PipelineConfiguration


async def debug_integration_pipeline():
    """Debug the integration pipeline step by step."""
    print("=== DEBUGGING INTEGRATION PIPELINE ===")

    # Enable detailed logging
    logging.basicConfig(level=logging.DEBUG)

    # Create test directory
    test_dir = Path(tempfile.mkdtemp(prefix="mallku_integration_debug_"))
    print(f"Test directory: {test_dir}")

    # Track events at different levels
    captured_pipeline_events = []
    captured_file_events = []

    def capture_pipeline_event(event):
        print(f"PIPELINE EVENT: {event.source_event_id} - {event.current_stage.value}")
        captured_pipeline_events.append(event)

    def capture_file_event(event):
        print(f"FILE EVENT: {event.content.get('operation')} - {event.content.get('file_name')}")
        captured_file_events.append(event)

    try:
        # Create configuration
        config = PipelineConfiguration(
            watch_directories=[str(test_dir)],
            correlation_confidence_threshold=0.3,  # Very low for debugging
            anchor_creation_threshold=0.4,
            file_filter_config={"test_mode": True},
        )

        # Create and initialize service
        print("\n--- Creating Integration Service ---")
        service = EndToEndIntegrationService(config)
        service.add_event_handler(capture_pipeline_event)

        print("\n--- Initializing Service ---")
        await service.initialize()

        # Add file event handler directly to file connector for debugging
        service.file_connector.add_event_callback(capture_file_event)  # type: ignore

        print(f"Service running: {service.is_running}")
        print(f"File connector running: {service.file_connector._is_running}")  # type: ignore
        print(f"Pipeline ID: {service.pipeline_id}")

        # Wait for full startup
        print("\n--- Waiting for Full Startup ---")
        await asyncio.sleep(3.0)

        # Create test file
        print("\n--- Creating Test File ---")
        test_file = test_dir / "debug_test.txt"
        print(f"Creating: {test_file}")
        test_file.write_text(f"Debug content created at {datetime.now(UTC)}")

        # Wait for event processing
        print("Waiting 5 seconds for event processing...")
        await asyncio.sleep(5.0)

        print(f"\nFile events captured: {len(captured_file_events)}")
        print(f"Pipeline events captured: {len(captured_pipeline_events)}")

        if captured_file_events:
            print("\nFile Events:")
            for i, event in enumerate(captured_file_events):
                print(f"  {i}: {event.event_type.value} - {event.content}")

        if captured_pipeline_events:
            print("\nPipeline Events:")
            for i, event in enumerate(captured_pipeline_events):
                print(f"  {i}: {event.source_event_id} - {event.current_stage.value}")
        else:
            print("\nNo pipeline events captured!")

            # Check integration service internals
            print("\nDebugging Integration Service:")
            print(f"  Event queue size: {service.event_queue.qsize()}")
            print(f"  Active pipeline events: {len(service.pipeline_events)}")
            print(f"  Event handlers: {len(service.event_handlers)}")

            # Check file connector statistics
            if service.file_connector:
                stats = service.file_connector.get_statistics()
                print("\nFile Connector Stats:")
                print(f"  Events captured: {stats['events_captured']}")
                print(f"  Events filtered: {stats['events_filtered']}")
                print(f"  Events processed: {stats['events_processed']}")
                print(f"  Callbacks: {stats['callback_count']}")

        # Try modifying the file
        print("\n--- Modifying Test File ---")
        test_file.write_text(f"Modified content at {datetime.now(UTC)}")
        await asyncio.sleep(3.0)

        print("\nAfter modification:")
        print(f"File events: {len(captured_file_events)}")
        print(f"Pipeline events: {len(captured_pipeline_events)}")

        # Get final status
        status = await service.get_pipeline_status()
        print("\nFinal Pipeline Status:")
        print(f"  Events processed: {status.events_processed}")
        print(f"  Events in pipeline: {status.events_in_pipeline}")
        print(f"  Events failed: {status.events_failed}")

    except Exception as e:
        print(f"Error during debugging: {e}")
        import traceback

        traceback.print_exc()

    finally:
        # Cleanup
        await service.shutdown()  # type: ignore

        # Remove test directory
        import shutil

        shutil.rmtree(test_dir)
        print(f"Cleaned up: {test_dir}")


if __name__ == "__main__":
    asyncio.run(debug_integration_pipeline())
