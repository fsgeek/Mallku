#!/usr/bin/env python3
"""
Debug script to understand why correlations aren't being detected.
"""

import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# ruff: noqa: E402
from mallku.correlation.models import ConsciousnessEventType, Event
from mallku.correlation.patterns import (
    ConcurrentPattern,
    ContextualPattern,
    CyclicalPattern,
    SequentialPattern,
)

# ruff: qa E402


def generate_test_events():
    """Generate the same test events as the test suite."""
    test_events = []
    base_time = datetime.now(UTC)

    # Generate sequential pattern: email -> document creation
    test_events.extend(
        [
            Event(
                timestamp=base_time + timedelta(minutes=i * 60),
                event_type=ConsciousnessEventType.COMMUNICATION,
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
                event_type=ConsciousnessEventType.STORAGE,
                stream_id="document_creation",
                content={"filename": f"response_{i}.docx", "type": "document"},
                context={"location": "office", "device": "laptop"},
                correlation_tags=["work", "document"],
            )
            for i in range(5)
        ]
    )

    # Sort all events by timestamp
    test_events.sort(key=lambda e: e.timestamp)
    return test_events


def debug_sequential_patterns():
    """Debug sequential pattern detection."""
    print("=== DEBUGGING SEQUENTIAL PATTERNS ===")

    events = generate_test_events()
    print(f"Generated {len(events)} test events")

    # Print event details
    for i, event in enumerate(events):
        print(f"Event {i}: {event.stream_id} at {event.timestamp} (type: {event.event_type})")

    print("\n--- Testing Sequential Pattern Detector ---")
    detector = SequentialPattern(
        min_occurrences=2, min_confidence=0.1
    )  # Lower thresholds for debugging

    patterns = detector.detect_patterns(events)
    print(f"Detected {len(patterns)} sequential patterns")

    for pattern in patterns:
        print(
            f"Pattern: {pattern.pattern_type}, freq: {pattern.occurrence_frequency}, conf: {pattern.confidence_score:.3f}"
        )
        print(f"  Gap: {pattern.temporal_gap}")
        print(f"  Primary: {pattern.primary_event.stream_id}")
        print(f"  Correlated: {[e.stream_id for e in pattern.correlated_events]}")


def debug_all_patterns():
    """Debug all pattern types."""
    events = generate_test_events()

    detectors = {
        "Sequential": SequentialPattern(min_occurrences=2, min_confidence=0.1),
        "Concurrent": ConcurrentPattern(min_occurrences=2, min_confidence=0.1),
        "Cyclical": CyclicalPattern(min_occurrences=2, min_confidence=0.1),
        "Contextual": ContextualPattern(min_occurrences=2, min_confidence=0.1),
    }

    for name, detector in detectors.items():
        print(f"\n=== {name.upper()} PATTERNS ===")
        try:
            patterns = detector.detect_patterns(events)
            print(f"Detected {len(patterns)} patterns")

            for pattern in patterns:
                print(
                    f"  {pattern.pattern_type}: freq={pattern.occurrence_frequency}, conf={pattern.confidence_score:.3f}"
                )
        except Exception as e:
            print(f"  Error: {e}")


if __name__ == "__main__":
    debug_sequential_patterns()
    debug_all_patterns()
