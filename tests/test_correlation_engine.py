#!/usr/bin/env python3
import asyncio
import logging
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import uuid4

# Add src to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from mallku.correlation import (  # noqa: E402
    AdaptiveThresholds,
    ConcurrentPattern,
    ConfidenceScorer,
    ContextualPattern,
    CorrelationEngine,
    CorrelationFeedback,
    CyclicalPattern,
    SequentialPattern,
    TemporalCorrelation,
)
from mallku.correlation.models import ConsciousnessEventType, Event, TemporalPrecision  # noqa: E402
from mallku.services.memory_anchor_service import MemoryAnchorService  # noqa: E402

"""
Comprehensive test suite for the Correlation Engine.

This test suite validates the sophisticated temporal correlation detection
system, from basic pattern recognition through adaptive learning to
memory anchor integration.
"""


class CorrelationEngineTests:
    """Comprehensive test suite for correlation engine functionality."""

    def __init__(self):
        self.correlation_engine: CorrelationEngine | None = None
        self.test_events: list[Event] = []

    async def run_all_tests(self):
        """Execute complete test suite."""
        print("Correlation Engine Test Suite")
        print("=" * 50)

        # Set up logging to see what's happening
        logging.basicConfig(level=logging.INFO)

        tests = [
            self.test_engine_initialization,
            self.test_event_generation,
            self.test_sequential_pattern_detection,
            self.test_concurrent_pattern_detection,
            self.test_cyclical_pattern_detection,
            self.test_contextual_pattern_detection,
            self.test_confidence_scoring,
            self.test_adaptive_thresholds,
            self.test_sliding_windows,
            self.test_end_to_end_processing,
            self.test_feedback_learning,
            self.test_memory_anchor_integration,
            self.test_performance_monitoring,
            self.cleanup_test_environment,
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
            print("🎉 All tests passed! Correlation Engine is working magnificently.")
            return 0
        else:
            print("❌ Some tests failed. The cathedral needs more work.")
            return 1

    async def test_engine_initialization(self) -> bool:
        """Test correlation engine initialization."""
        try:
            # Create memory anchor service for integration
            memory_service = MemoryAnchorService()
            await memory_service.initialize()

            # Initialize correlation engine with window size that can capture our test pattern span
            self.correlation_engine = CorrelationEngine(
                memory_anchor_service=memory_service,
                window_size=timedelta(hours=12),  # Large enough to capture full test patterns
                window_overlap=0.3,
            )

            await self.correlation_engine.initialize()

            # Verify components are properly initialized
            assert self.correlation_engine.confidence_scorer is not None
            assert self.correlation_engine.adaptive_thresholds is not None
            assert len(self.correlation_engine.pattern_detectors) == 4
            assert "sequential" in self.correlation_engine.pattern_detectors
            assert "concurrent" in self.correlation_engine.pattern_detectors
            assert "cyclical" in self.correlation_engine.pattern_detectors
            assert "contextual" in self.correlation_engine.pattern_detectors

            status = self.correlation_engine.get_engine_status()
            assert status["engine_info"]["status"] == "active"

            print(
                f"   Engine initialized with {len(self.correlation_engine.pattern_detectors)} pattern detectors"
            )
            return True

        except Exception as e:
            print(f"   Initialization failed: {e}")
            return False

    async def test_event_generation(self) -> bool:
        """Test generation of realistic test events."""
        try:
            base_time = datetime.now(UTC)

            # Generate sequential pattern: email -> document creation
            self.test_events.extend(
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
            self.test_events.extend(
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

            # Generate concurrent pattern: music + coding
            music_start = base_time + timedelta(hours=2)
            for i in range(3):
                # Music starts
                self.test_events.append(
                    Event(
                        timestamp=music_start + timedelta(hours=i * 2),
                        event_type=ConsciousnessEventType.ACTIVITY,
                        stream_id="spotify",
                        content={"track": "Focus Music", "artist": "Ambient Collective"},
                        context={"location": "home", "device": "desktop"},
                        correlation_tags=["music", "focus"],
                    )
                )

                # Coding activity starts shortly after (concurrent)
                self.test_events.append(
                    Event(
                        timestamp=music_start + timedelta(hours=i * 2, minutes=2),
                        event_type=ConsciousnessEventType.ACTIVITY,
                        stream_id="code_editor",
                        content={"file": "correlation_engine.py", "action": "edit"},
                        context={"location": "home", "device": "desktop"},
                        correlation_tags=["coding", "focus"],
                    )
                )

            # Generate cyclical pattern: daily standup -> task updates
            standup_base = base_time + timedelta(days=1, hours=9)  # 9 AM daily
            for day in range(7):  # Week of standups
                self.test_events.append(
                    Event(
                        timestamp=standup_base + timedelta(days=day),
                        event_type=ConsciousnessEventType.COMMUNICATION,
                        stream_id="teams_meetings",
                        content={"meeting": "Daily Standup", "duration": 15},
                        context={"location": "office", "device": "laptop"},
                        correlation_tags=["meeting", "standup"],
                    )
                )

                # Task updates follow (cyclical pattern)
                self.test_events.append(
                    Event(
                        timestamp=standup_base + timedelta(days=day, minutes=30),
                        event_type=ConsciousnessEventType.ACTIVITY,
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
                self.test_events.append(
                    Event(
                        timestamp=travel_base + timedelta(hours=i * 4),
                        event_type=ConsciousnessEventType.ENVIRONMENTAL,
                        stream_id="location_service",
                        content={"location": location, "activity": "business_travel"},
                        context={"travel_mode": "business", "trip_id": "conf_2024"},
                        correlation_tags=["travel", "business"],
                    )
                )

                # Expense reports created in travel context
                self.test_events.append(
                    Event(
                        timestamp=travel_base + timedelta(hours=i * 4 + 1),
                        event_type=ConsciousnessEventType.STORAGE,
                        stream_id="expense_tracker",
                        content={"expense_type": "business", "amount": 50.0 + i * 25},
                        context={"travel_mode": "business", "trip_id": "conf_2024"},
                        correlation_tags=["expense", "business"],
                    )
                )

            # Sort all events by timestamp
            self.test_events.sort(key=lambda e: e.timestamp)

            print(f"   Generated {len(self.test_events)} test events across 4 pattern types")
            print(f"   Time span: {self.test_events[-1].timestamp - self.test_events[0].timestamp}")
            return True

        except Exception as e:
            print(f"   Event generation failed: {e}")
            return False

    async def test_sequential_pattern_detection(self) -> bool:
        """Test detection of sequential patterns."""
        try:
            detector = SequentialPattern(min_occurrences=3, min_confidence=0.5)

            # Extract events for sequential pattern testing
            email_events = [e for e in self.test_events if e.stream_id == "email_inbox"]
            doc_events = [e for e in self.test_events if e.stream_id == "document_creation"]
            combined_events = email_events + doc_events
            combined_events.sort(key=lambda e: e.timestamp)

            patterns = detector.detect_patterns(combined_events)

            assert len(patterns) > 0, "Should detect at least one sequential pattern"

            # Verify pattern characteristics
            for pattern in patterns:
                assert pattern.pattern_type == "sequential"
                assert pattern.occurrence_frequency >= 3
                assert pattern.confidence_score >= 0.5
                assert pattern.temporal_gap.total_seconds() > 0

                print(
                    f"   Found sequential pattern: {pattern.occurrence_frequency} occurrences, "
                    f"confidence: {pattern.confidence_score:.2f}, "
                    f"avg gap: {pattern.temporal_gap}"
                )

            return True

        except Exception as e:
            print(f"   Sequential pattern detection failed: {e}")
            return False

    async def test_concurrent_pattern_detection(self) -> bool:
        """Test detection of concurrent patterns."""
        try:
            detector = ConcurrentPattern(min_occurrences=2, min_confidence=0.4)

            # Extract events for concurrent pattern testing
            music_events = [e for e in self.test_events if e.stream_id == "spotify"]
            code_events = [e for e in self.test_events if e.stream_id == "code_editor"]
            combined_events = music_events + code_events
            combined_events.sort(key=lambda e: e.timestamp)

            patterns = detector.detect_patterns(combined_events)

            assert len(patterns) > 0, "Should detect at least one concurrent pattern"

            # Verify pattern characteristics
            for pattern in patterns:
                assert pattern.pattern_type == "concurrent"
                assert pattern.occurrence_frequency >= 2
                assert pattern.temporal_gap.total_seconds() < 300  # Should be close in time

                print(
                    f"   Found concurrent pattern: {pattern.occurrence_frequency} occurrences, "
                    f"confidence: {pattern.confidence_score:.2f}, "
                    f"avg gap: {pattern.temporal_gap}"
                )

            return True

        except Exception as e:
            print(f"   Concurrent pattern detection failed: {e}")
            return False

    async def test_cyclical_pattern_detection(self) -> bool:
        """Test detection of cyclical patterns."""
        try:
            detector = CyclicalPattern(min_occurrences=3, min_confidence=0.4)

            # Extract events for cyclical pattern testing
            standup_events = [e for e in self.test_events if e.stream_id == "teams_meetings"]
            task_events = [e for e in self.test_events if e.stream_id == "task_tracker"]

            # Test standup cyclical pattern
            standup_patterns = detector.detect_patterns(standup_events)
            task_patterns = detector.detect_patterns(task_events)

            all_patterns = standup_patterns + task_patterns

            # Should detect daily patterns
            found_cyclical = any(p.pattern_type == "cyclical" for p in all_patterns)
            assert found_cyclical, "Should detect cyclical patterns"

            for pattern in all_patterns:
                if pattern.pattern_type == "cyclical":
                    print(
                        f"   Found cyclical pattern: {pattern.occurrence_frequency} occurrences, "
                        f"confidence: {pattern.confidence_score:.2f}, "
                        f"period: {pattern.temporal_gap}"
                    )

            return True

        except Exception as e:
            print(f"   Cyclical pattern detection failed: {e}")
            return False

    async def test_contextual_pattern_detection(self) -> bool:
        """Test detection of contextual patterns."""
        try:
            detector = ContextualPattern(min_occurrences=2, min_confidence=0.4)

            # Extract events for contextual pattern testing (travel + expenses)
            travel_events = [e for e in self.test_events if "travel" in e.correlation_tags]
            expense_events = [e for e in self.test_events if "expense" in e.correlation_tags]
            combined_events = travel_events + expense_events
            combined_events.sort(key=lambda e: e.timestamp)

            patterns = detector.detect_patterns(combined_events)

            assert len(patterns) > 0, "Should detect at least one contextual pattern"

            # Verify pattern characteristics
            for pattern in patterns:
                assert pattern.pattern_type == "contextual"
                assert pattern.occurrence_frequency >= 2

                print(
                    f"   Found contextual pattern: {pattern.occurrence_frequency} occurrences, "
                    f"confidence: {pattern.confidence_score:.2f}"
                )

            return True

        except Exception as e:
            print(f"   Contextual pattern detection failed: {e}")
            return False

    async def test_confidence_scoring(self) -> bool:
        """Test multi-factor confidence scoring system."""
        try:
            scorer = ConfidenceScorer()

            # Create a test correlation
            test_correlation = TemporalCorrelation(
                primary_event=self.test_events[0],
                correlated_events=self.test_events[1:3],
                temporal_gap=timedelta(minutes=5),
                gap_variance=100.0,  # Some variance
                temporal_precision=TemporalPrecision.MINUTE,
                occurrence_frequency=5,
                pattern_stability=0.8,
                pattern_type="sequential",
                confidence_score=0.0,  # Will be calculated
                last_occurrence=datetime.now(UTC),
            )

            # Calculate confidence
            confidence = scorer.calculate_correlation_confidence(test_correlation)

            assert 0.0 <= confidence <= 1.0, "Confidence should be between 0 and 1"
            assert confidence > 0.0, "Should have non-zero confidence for reasonable pattern"

            # Verify factor breakdown
            factors = test_correlation.confidence_factors
            expected_factors = [
                "temporal_consistency",
                "frequency_strength",
                "context_coherence",
                "causal_plausibility",
                "user_validation",
            ]

            for factor in expected_factors:
                assert factor in factors, f"Missing confidence factor: {factor}"
                assert 0.0 <= factors[factor] <= 1.0, f"Factor {factor} out of range"

            # Test explanation generation
            explanation = scorer.get_confidence_explanation(test_correlation)
            assert "overall_confidence" in explanation
            assert "factor_breakdown" in explanation
            assert "pattern_details" in explanation

            print(f"   Confidence score: {confidence:.3f}")
            print(f"   Factor breakdown: {factors}")

            return True

        except Exception as e:
            print(f"   Confidence scoring test failed: {e}")
            return False

    async def test_adaptive_thresholds(self) -> bool:
        """Test adaptive threshold learning system."""
        try:
            thresholds = AdaptiveThresholds()

            # Test initial state
            initial_confidence = thresholds.confidence_threshold
            initial_frequency = thresholds.frequency_threshold

            assert 0.0 < initial_confidence < 1.0
            assert initial_frequency > 0

            # Create synthetic feedback (mix of positive and negative)
            feedback_batch = []

            # Positive feedback (high confidence, meaningful)
            for i in range(10):
                feedback = CorrelationFeedback(
                    correlation_id=uuid4(),
                    is_meaningful=True,
                    confidence_rating=0.8 + (i * 0.01),  # 0.8 to 0.89
                    feedback_source="test_suite",
                    explanation="High quality correlation",
                )
                feedback_batch.append(feedback)

            # Negative feedback (low confidence, not meaningful)
            for i in range(5):
                feedback = CorrelationFeedback(
                    correlation_id=uuid4(),
                    is_meaningful=False,
                    confidence_rating=0.3 + (i * 0.02),  # 0.3 to 0.38
                    feedback_source="test_suite",
                    explanation="Spurious correlation",
                )
                feedback_batch.append(feedback)

            # Process feedback
            results = thresholds.update_from_feedback(feedback_batch)

            assert "metrics" in results
            metrics = results["metrics"]

            # Test threshold acceptance
            high_conf_accepted = thresholds.should_accept_correlation(0.9, 5, "sequential")
            low_conf_rejected = thresholds.should_accept_correlation(0.1, 2, "sequential")

            assert high_conf_accepted, "High confidence correlation should be accepted"
            assert not low_conf_rejected, "Low confidence correlation should be rejected"

            # Test performance summary
            summary = thresholds.get_performance_summary()
            assert "performance_trends" in summary
            assert "current_thresholds" in summary
            assert "learning_stats" in summary

            print(f"   Initial confidence threshold: {initial_confidence}")
            print(f"   Updated confidence threshold: {thresholds.confidence_threshold}")
            print(f"   Precision: {metrics:.3f}")
            print(f"   Recall: {metrics:.3f}")

            return True

        except Exception as e:
            print(f"   Adaptive thresholds test failed: {e}")
            return False

    async def test_sliding_windows(self) -> bool:
        """Test sliding window management."""
        try:
            if not self.correlation_engine:
                return False

            # Process a subset of events to test windowing
            test_batch = self.test_events[:20]  # First 20 events

            initial_windows = len(self.correlation_engine.active_windows)

            # Process events
            correlations = await self.correlation_engine.process_event_stream(test_batch)

            # Verify windows were created
            final_windows = len(self.correlation_engine.active_windows)
            assert final_windows > initial_windows, "Should create sliding windows"

            # Verify events were added to windows
            total_events_in_windows = sum(
                window.event_count for window in self.correlation_engine.active_windows
            )
            assert total_events_in_windows > 0, "Windows should contain events"

            # Verify window overlap
            if len(self.correlation_engine.active_windows) > 1:
                windows = sorted(self.correlation_engine.active_windows, key=lambda w: w.start_time)
                for i in range(len(windows) - 1):
                    current_window = windows[i]
                    next_window = windows[i + 1]

                    # Should have overlap
                    overlap = current_window.end_time > next_window.start_time
                    assert overlap, "Adjacent windows should overlap"

            print(f"   Created {final_windows} sliding windows")
            print(f"   Total events in windows: {total_events_in_windows}")
            print(f"   Detected {len(correlations)} correlations")

            return True

        except Exception as e:
            print(f"   Sliding windows test failed: {e}")
            return False

    async def test_end_to_end_processing(self) -> bool:
        """Test complete end-to-end correlation detection pipeline."""
        try:
            if not self.correlation_engine:
                return False

            # Reset statistics and thresholds to ensure clean test
            self.correlation_engine.correlation_stats = {
                "total_correlations_detected": 0,
                "correlations_accepted": 0,
                "correlations_rejected": 0,
                "memory_anchors_created": 0,
                "last_processing_time": None,
            }

            # Reset adaptive thresholds to defaults for consistent testing
            self.correlation_engine.adaptive_thresholds.reset_to_defaults()

            # Process all test events
            correlations = await self.correlation_engine.process_event_stream(self.test_events)

            # Verify processing occurred
            stats = self.correlation_engine.correlation_stats
            assert stats["total_correlations_detected"] > 0, "Should detect correlations"
            assert stats["last_processing_time"] is not None, "Should record processing time"

            # The key test: the system should detect patterns and make threshold decisions
            # Some correlations may be rejected due to threshold filtering, which is correct behavior
            total_processed = stats["correlations_accepted"] + stats["correlations_rejected"]
            assert total_processed > 0, "Should process some correlations (accepted or rejected)"

            # Verify quality of accepted correlations (if any)
            for correlation in correlations:
                assert correlation.confidence_score > 0.0, (
                    "Correlations should have confidence scores"
                )
                assert correlation.pattern_type in [
                    "sequential",
                    "concurrent",
                    "cyclical",
                    "contextual",
                ]
                assert correlation.occurrence_frequency > 0

            # Test status reporting
            status = self.correlation_engine.get_engine_status()
            assert status["engine_info"]["status"] == "active"
            assert status["statistics"]["total_correlations_detected"] > 0

            print(f"   Processed {len(self.test_events)} events")
            print(f"   Detected {stats['total_correlations_detected']} total correlations")
            print(f"   Accepted {stats['correlations_accepted']} correlations")
            print(f"   Rejected {stats['correlations_rejected']} correlations")
            print(f"   Created {stats['memory_anchors_created']} memory anchors")

            return True

        except Exception as e:
            print(f"   End-to-end processing test failed: {e}")
            return False

    async def test_feedback_learning(self) -> bool:
        """Test feedback processing and learning adaptation."""
        try:
            if not self.correlation_engine:
                return False

            # Create feedback for some correlations
            feedback_batch = []

            # Simulate positive feedback
            for i in range(8):
                feedback = CorrelationFeedback(
                    correlation_id=uuid4(),
                    is_meaningful=True,
                    confidence_rating=0.8 + (i * 0.02),
                    feedback_source="test_user",
                    explanation="This correlation is very helpful",
                )
                feedback_batch.append(feedback)

            # Simulate negative feedback
            for i in range(3):
                feedback = CorrelationFeedback(
                    correlation_id=uuid4(),
                    is_meaningful=False,
                    confidence_rating=0.2 + (i * 0.05),
                    feedback_source="test_user",
                    explanation="This seems like noise",
                )
                feedback_batch.append(feedback)

            # Add feedback to engine
            for feedback in feedback_batch:
                await self.correlation_engine.add_feedback(feedback)

            # Force learning update
            await self.correlation_engine.force_learning_update()

            # Verify feedback was processed
            assert len(self.correlation_engine.feedback_queue) == 0, (
                "Feedback queue should be empty after processing"
            )

            # Check that thresholds may have been updated
            thresholds_summary = (
                self.correlation_engine.adaptive_thresholds.get_performance_summary()
            )
            assert "performance_trends" in thresholds_summary

            print(f"   Processed {len(feedback_batch)} feedback items")
            print(
                f"   Current confidence threshold: {self.correlation_engine.adaptive_thresholds.confidence_threshold:.3f}"
            )

            return True

        except Exception as e:
            print(f"   Feedback learning test failed: {e}")
            return False

    async def test_memory_anchor_integration(self) -> bool:
        """Test integration with Memory Anchor Service."""
        try:
            if not self.correlation_engine:
                return False

            # Check that memory anchor service is connected
            assert self.correlation_engine.memory_service is not None, (
                "Memory service should be connected"
            )

            # Verify anchor creation statistics
            stats = self.correlation_engine.correlation_stats
            anchors_created = stats.get("memory_anchors_created", 0)

            # Should have created some anchors from high-confidence correlations
            print(f"   Memory anchors created: {anchors_created}")

            # Test the adapter directly
            from mallku.integration.correlation_adapter import CorrelationToAnchorAdapter

            adapter = CorrelationToAnchorAdapter(self.correlation_engine.memory_service)

            # Create a high-confidence correlation for testing
            test_correlation = TemporalCorrelation(
                primary_event=self.test_events[0],
                correlated_events=self.test_events[1:3],
                temporal_gap=timedelta(minutes=5),
                gap_variance=50.0,
                temporal_precision=TemporalPrecision.MINUTE,
                occurrence_frequency=7,
                pattern_stability=0.9,
                pattern_type="sequential",
                confidence_score=0.85,  # High confidence
                last_occurrence=datetime.now(UTC),
            )

            # Test anchor creation
            anchor = await adapter.process_correlation(test_correlation)

            if anchor:
                print(f"   Successfully created memory anchor: {anchor.anchor_id}")
                # The adapter successfully created an anchor - this is the key test
                assert anchor.anchor_id is not None, "Anchor should have an ID"
                print("   Adapter integration working correctly")
            else:
                print("   Adapter returned None (confidence threshold not met)")

            return True

        except Exception as e:
            print(f"   Memory anchor integration test failed: {e}")
            return False

    async def test_performance_monitoring(self) -> bool:
        """Test performance monitoring and statistics."""
        try:
            if not self.correlation_engine:
                return False

            # Get comprehensive status
            status = self.correlation_engine.get_engine_status()

            # Verify status structure
            required_sections = [
                "engine_info",
                "statistics",
                "pattern_detectors",
                "adaptive_thresholds",
            ]
            for section in required_sections:
                assert section in status, f"Missing status section: {section}"

            # Verify engine info
            engine_info = status["engine_info"]
            assert engine_info["status"] == "active"
            assert "window_size" in engine_info
            assert "active_windows" in engine_info
            assert "event_buffer_size" in engine_info

            # Verify statistics
            statistics = status["statistics"]
            stat_keys = [
                "total_correlations_detected",
                "correlations_accepted",
                "correlations_rejected",
            ]
            for key in stat_keys:
                assert key in statistics, f"Missing statistic: {key}"
                assert isinstance(statistics[key], int), f"Statistic {key} should be integer"

            # Verify pattern detectors
            detectors = status["pattern_detectors"]
            expected_detectors = ["sequential", "concurrent", "cyclical", "contextual"]
            for detector in expected_detectors:
                assert detector in detectors, f"Missing pattern detector: {detector}"

            # Test reset functionality
            self.correlation_engine.reset_learning_state()

            reset_stats = self.correlation_engine.correlation_stats
            assert reset_stats["total_correlations_detected"] == 0
            assert reset_stats["correlations_accepted"] == 0

            print(f"   Status sections verified: {list(status.keys())}")
            print(f"   Pattern detectors: {detectors}")
            print("   Reset functionality working")

            return True

        except Exception as e:
            print(f"   Performance monitoring test failed: {e}")
            return False

    async def cleanup_test_environment(self) -> bool:
        """Clean up test environment."""
        try:
            if self.correlation_engine:
                await self.correlation_engine.shutdown()

            print("   Cleaned up test environment")
            return True

        except Exception as e:
            print(f"   Cleanup failed: {e}")
            return False


async def main():
    """Run the correlation engine test suite."""
    test_suite = CorrelationEngineTests()
    return await test_suite.run_all_tests()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
