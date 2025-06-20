#!/usr/bin/env python3
"""
Debug the end-to-end test specifically to understand why no correlations are returned.
"""

import asyncio
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# ruff: noqa: E402
from mallku.correlation.engine import CorrelationEngine
from mallku.correlation.models import Event, EventType
from mallku.services.memory_anchor_service import MemoryAnchorService


def generate_complete_test_events():
    """Generate the EXACT same test events as the test suite."""
    test_events = []
    base_time = datetime.now(UTC)

    # Generate sequential pattern: email -> document creation
    test_events.extend(
        [
            Event(
                timestamp=base_time + timedelta(minutes=i * 60),
                event_type=EventType.COMMUNICATION,
                stream_id="email_inbox",
                content={"subject": f"Project Update {i}", "sender": "boss@company.com"},
                context={"location": "office", "device": "laptop"},
                correlation_tags=["work", "communication"],
            )
            for i in range(5)
        ]
    )

    # Followed by document creation (sequential pattern)
    test_events.extend(
        [
            Event(
                timestamp=base_time + timedelta(minutes=i * 60 + 5),
                event_type=EventType.STORAGE,
                stream_id="document_creation",
                content={"filename": f"response_{i}.docx", "type": "document"},
                context={"location": "office", "device": "laptop"},
                correlation_tags=["work", "document"],
            )
            for i in range(5)
        ]
    )

    # Generate concurrent pattern: music + coding
    music_start = base_time + timedelta(hours=2)
    for i in range(3):
        # Music starts
        test_events.append(
            Event(
                timestamp=music_start + timedelta(hours=i * 2),
                event_type=EventType.ACTIVITY,
                stream_id="spotify",
                content={"track": "Focus Music", "artist": "Ambient Collective"},
                context={"location": "home", "device": "desktop"},
                correlation_tags=["music", "focus"],
            )
        )

        # Coding activity starts shortly after (concurrent)
        test_events.append(
            Event(
                timestamp=music_start + timedelta(hours=i * 2, minutes=2),
                event_type=EventType.ACTIVITY,
                stream_id="code_editor",
                content={"file": "correlation_engine.py", "action": "edit"},
                context={"location": "home", "device": "desktop"},
                correlation_tags=["coding", "focus"],
            )
        )

    # Generate cyclical pattern: daily standup -> task updates
    standup_base = base_time + timedelta(days=1, hours=9)  # 9 AM daily
    for day in range(7):  # Week of standups
        test_events.append(
            Event(
                timestamp=standup_base + timedelta(days=day),
                event_type=EventType.COMMUNICATION,
                stream_id="teams_meetings",
                content={"meeting": "Daily Standup", "duration": 15},
                context={"location": "office", "device": "laptop"},
                correlation_tags=["meeting", "standup"],
            )
        )

        # Task updates follow (cyclical pattern)
        test_events.append(
            Event(
                timestamp=standup_base + timedelta(days=day, minutes=30),
                event_type=EventType.ACTIVITY,
                stream_id="task_tracker",
                content={"action": "update_tasks", "count": 3},
                context={"location": "office", "device": "laptop"},
                correlation_tags=["tasks", "planning"],
            )
        )

    # Generate contextual pattern: travel context + expense reports
    travel_base = base_time + timedelta(days=10)
    travel_locations = ["airport", "hotel", "conference_center"]

    for i, location in enumerate(travel_locations):
        test_events.append(
            Event(
                timestamp=travel_base + timedelta(hours=i * 4),
                event_type=EventType.ENVIRONMENTAL,
                stream_id="location_service",
                content={"location": location, "activity": "business_travel"},
                context={"travel_mode": "business", "trip_id": "conf_2024"},
                correlation_tags=["travel", "business"],
            )
        )

        # Expense reports created in travel context
        test_events.append(
            Event(
                timestamp=travel_base + timedelta(hours=i * 4 + 1),
                event_type=EventType.STORAGE,
                stream_id="expense_tracker",
                content={"expense_type": "business", "amount": 50.0 + i * 25},
                context={"travel_mode": "business", "trip_id": "conf_2024"},
                correlation_tags=["expense", "business"],
            )
        )

    # Sort all events by timestamp
    test_events.sort(key=lambda e: e.timestamp)
    return test_events


async def debug_endtoend():
    """Debug the end-to-end processing with exact test configuration."""
    print("=== DEBUGGING END-TO-END PROCESSING ===")

    # Create memory anchor service
    memory_service = MemoryAnchorService()
    await memory_service.initialize()

    # Initialize correlation engine with EXACT same configuration as test
    engine = CorrelationEngine(
        memory_anchor_service=memory_service,
        window_size=timedelta(hours=12),  # Updated window size
        window_overlap=0.3,
    )

    await engine.initialize()

    # Generate EXACT same test events
    events = generate_complete_test_events()
    print(f"Generated {len(events)} test events")
    print(f"Time span: {events[-1].timestamp - events[0].timestamp}")
    print(f"Window size: {engine.window_size}")

    # Check initial thresholds
    print("\nInitial Thresholds:")
    print(f"  Confidence: {engine.adaptive_thresholds.confidence_threshold}")
    print(f"  Frequency: {engine.adaptive_thresholds.frequency_threshold}")

    # Reset stats and thresholds like the test does
    engine.correlation_stats = {
        "total_correlations_detected": 0,
        "correlations_accepted": 0,
        "correlations_rejected": 0,
        "memory_anchors_created": 0,
        "last_processing_time": None,
    }
    engine.adaptive_thresholds.reset_to_defaults()

    print("\nAfter reset:")
    print(f"  Confidence: {engine.adaptive_thresholds.confidence_threshold}")
    print(f"  Frequency: {engine.adaptive_thresholds.frequency_threshold}")

    # Process events
    print("\n--- Processing Events ---")
    correlations = await engine.process_event_stream(events)

    print("\nResults:")
    print(
        f"  Total correlations detected: {engine.correlation_stats['total_correlations_detected']}"
    )
    print(f"  Correlations accepted: {engine.correlation_stats['correlations_accepted']}")
    print(f"  Correlations rejected: {engine.correlation_stats['correlations_rejected']}")
    print(f"  Returned correlations: {len(correlations)}")

    # Analyze what happened in windows
    for i, window in enumerate(engine.active_windows):
        print(f"\nWindow {i}:")
        print(f"  Events: {window.event_count}")
        print(f"  Detected correlations: {len(window.detected_correlations)}")

        for j, corr in enumerate(window.detected_correlations):
            accepted = engine.adaptive_thresholds.should_accept_correlation(
                corr.confidence_score, corr.occurrence_frequency, corr.pattern_type
            )
            print(
                f"    Corr {j}: {corr.pattern_type}, conf={corr.confidence_score:.3f}, freq={corr.occurrence_frequency}, accepted={accepted}"
            )

    await engine.shutdown()


if __name__ == "__main__":
    asyncio.run(debug_endtoend())
