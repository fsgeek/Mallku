#!/usr/bin/env python3
"""
Debug sliding window behavior to understand the integration imbalance.
"""

import asyncio
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from mallku.correlation.engine import CorrelationEngine
from mallku.correlation.models import Event, EventType
from mallku.services.memory_anchor_service import MemoryAnchorService


def generate_test_events():
    """Generate the same test events as the test suite."""
    test_events = []
    base_time = datetime.now(UTC)

    # Generate sequential pattern: email -> document creation
    test_events.extend([
        Event(
            timestamp=base_time + timedelta(minutes=i*60),
            event_type=EventType.COMMUNICATION,
            stream_id="email_inbox",
            content={"subject": f"Project Update {i}", "sender": "boss@company.com"},
            context={"location": "office", "device": "laptop"},
            correlation_tags=["work", "communication"]
        ) for i in range(5)
    ])

    # Followed by document creation (sequential pattern)
    test_events.extend([
        Event(
            timestamp=base_time + timedelta(minutes=i*60 + 5),
            event_type=EventType.STORAGE,
            stream_id="document_creation",
            content={"filename": f"response_{i}.docx", "type": "document"},
            context={"location": "office", "device": "laptop"},
            correlation_tags=["work", "document"]
        ) for i in range(5)
    ])

    # Sort all events by timestamp
    test_events.sort(key=lambda e: e.timestamp)
    return test_events

async def debug_correlation_engine():
    """Debug the correlation engine's window and threshold behavior."""
    print("=== DEBUGGING CORRELATION ENGINE ===")

    # Create memory anchor service
    memory_service = MemoryAnchorService()
    await memory_service.initialize()

    # Initialize correlation engine with smaller windows to ensure events fit
    engine = CorrelationEngine(
        memory_anchor_service=memory_service,
        window_size=timedelta(hours=6),  # Larger window to capture all events
        window_overlap=0.3
    )

    await engine.initialize()

    # Generate test events
    events = generate_test_events()
    print(f"Generated {len(events)} test events")
    print(f"Time span: {events[-1].timestamp - events[0].timestamp}")
    print(f"Window size: {engine.window_size}")

    # Check adaptive thresholds
    print("\nAdaptive Thresholds:")
    print(f"  Confidence threshold: {engine.adaptive_thresholds.confidence_threshold}")
    print(f"  Frequency threshold: {engine.adaptive_thresholds.frequency_threshold}")

    # Process events and monitor windows
    print("\n--- Processing Events ---")
    correlations = await engine.process_event_stream(events)

    print("\nResults:")
    print(f"  Windows created: {len(engine.active_windows)}")
    print(f"  Correlations detected: {engine.correlation_stats['total_correlations_detected']}")
    print(f"  Correlations accepted: {engine.correlation_stats['correlations_accepted']}")
    print(f"  Correlations rejected: {engine.correlation_stats['correlations_rejected']}")
    print(f"  Returned correlations: {len(correlations)}")

    # Examine windows
    for i, window in enumerate(engine.active_windows):
        print(f"\nWindow {i}:")
        print(f"  Start: {window.start_time}")
        print(f"  End: {window.end_time}")
        print(f"  Events: {window.event_count}")
        print(f"  Detected correlations: {len(window.detected_correlations)}")

        if hasattr(window, 'detected_correlations'):
            for j, corr in enumerate(window.detected_correlations):
                print(f"    Corr {j}: {corr.pattern_type}, conf={corr.confidence_score:.3f}, freq={corr.occurrence_frequency}")

    await engine.shutdown()

if __name__ == "__main__":
    asyncio.run(debug_correlation_engine())
