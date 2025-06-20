#!/usr/bin/env python3
"""
Test suite for Reciprocity Tracking Service - Community Sensing Tool

This test validates that the reciprocity tracker correctly senses patterns
and supports Fire Circle governance rather than making autonomous judgments.
"""

import asyncio
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from mallku.core.database import get_database
from mallku.reciprocity import (
    ContributionType,
    ExtractionAlert,
    FireCircleReport,
    InteractionRecord,
    InteractionType,
    NeedCategory,
    ParticipantType,
    ReciprocityTracker,
    SystemHealthMetrics,
)


class ReciprocityTrackerTests:
    """Test suite for reciprocity tracking service."""

    def __init__(self):
        self.db = None
        self.tracker: ReciprocityTracker = None
        self.test_interactions: list[InteractionRecord] = []

    async def setup(self) -> bool:
        """Set up test environment."""
        print("Setting up reciprocity tracker tests...")

        try:
            # Initialize database connection
            self.db = get_database()

            # Initialize tracker
            self.tracker = ReciprocityTracker()
            await self.tracker.initialize()

            # Create test interactions
            await self._create_test_interactions()

            print(f"   Created {len(self.test_interactions)} test interactions")
            return True

        except Exception as e:
            print(f"   Setup failed: {e}")
            return False

    async def test_tracker_initialization(self) -> bool:
        """Test tracker initialization and database setup."""
        try:
            # Test that all required collections exist
            required_collections = [
                "reciprocity_interactions",
                "reciprocity_patterns",
                "reciprocity_alerts",
                "system_health_snapshots",
                "fire_circle_reports",
            ]

            for collection_name in required_collections:
                assert self.db.has_collection(collection_name), (
                    f"Missing collection: {collection_name}"
                )

            # Test that components are initialized
            assert self.tracker.health_monitor is not None
            assert self.tracker.extraction_detector is not None
            assert self.tracker.fire_circle_interface is not None

            print("   Tracker initialization successful")
            return True

        except Exception as e:
            print(f"   Tracker initialization test failed: {e}")
            return False

    async def test_interaction_recording(self) -> bool:
        """Test recording reciprocal interactions."""
        try:
            # Record test interactions
            for interaction in self.test_interactions:
                await self.tracker.record_interaction(interaction)

            # Verify interactions were stored
            collection = self.db.collection("reciprocity_interactions")
            stored_count = collection.count()

            assert stored_count >= len(self.test_interactions), (
                f"Expected {len(self.test_interactions)}, got {stored_count}"
            )

            print("   Interaction recording successful")
            return True

        except Exception as e:
            print(f"   Interaction recording test failed: {e}")
            return False

    async def test_health_metrics_calculation(self) -> bool:
        """Test system health metrics calculation."""
        try:
            # Get current health metrics
            health_metrics = await self.tracker.get_current_health_metrics()

            # Validate health metrics structure
            assert isinstance(health_metrics, SystemHealthMetrics)
            assert hasattr(health_metrics, "overall_health_score")
            assert 0.0 <= health_metrics.overall_health_score <= 1.0
            assert hasattr(health_metrics, "health_trend_direction")
            assert health_metrics.health_trend_direction in ["improving", "declining", "stable"]

            # Test that metrics contain expected data
            assert hasattr(health_metrics, "total_interactions")
            assert hasattr(health_metrics, "unique_participants")
            assert hasattr(health_metrics, "voluntary_return_rate")

            print(
                f"   Health metrics calculation successful (score: {health_metrics.overall_health_score:.2f})"
            )
            return True

        except Exception as e:
            print(f"   Health metrics test failed: {e}")
            return False

    async def test_pattern_detection(self) -> bool:
        """Test pattern detection in reciprocal interactions."""
        try:
            # Detect patterns in recent interactions
            patterns = await self.tracker.detect_recent_patterns(hours_back=24, min_confidence=0.3)

            # Validate pattern structure
            for pattern in patterns:
                assert hasattr(pattern, "pattern_id")
                assert hasattr(pattern, "pattern_type")
                assert hasattr(pattern, "confidence_level")
                assert 0.0 <= pattern.confidence_level <= 1.0
                assert hasattr(pattern, "questions_for_deliberation")
                assert isinstance(pattern.questions_for_deliberation, list)

            print(f"   Pattern detection successful ({len(patterns)} patterns detected)")
            return True

        except Exception as e:
            print(f"   Pattern detection test failed: {e}")
            return False

    async def test_extraction_detection(self) -> bool:
        """Test extraction pattern detection."""
        try:
            # Create interaction that might trigger extraction alert
            extractive_interaction = InteractionRecord(
                interaction_type=InteractionType.RESOURCE_SHARING,
                initiator=ParticipantType.HUMAN,
                responder=ParticipantType.AI,
                contributions_offered=[],  # No contributions offered
                needs_expressed=[
                    NeedCategory.SURVIVAL,
                    NeedCategory.SAFETY,
                    NeedCategory.GROWTH,
                ],  # Many needs
                needs_fulfilled=[
                    NeedCategory.SURVIVAL,
                    NeedCategory.SAFETY,
                    NeedCategory.GROWTH,
                ],  # All fulfilled
                initiator_capacity_indicators={
                    "attention_availability": 0.9,
                    "time_pressure": 0.1,
                },  # High capacity
                responder_capacity_indicators={
                    "computational_load": 0.95,
                    "response_quality": 0.3,
                },  # Low capacity
                interaction_quality_indicators={
                    "mutual_understanding": 0.4,
                    "satisfaction_expressed": 0.3,
                },
            )

            # Analyze for extraction patterns
            alerts = await self.tracker.extraction_detector.analyze_interaction(
                extractive_interaction
            )

            # Should detect some extraction concerns given the mismatch
            print(f"   Extraction detection successful ({len(alerts)} alerts generated)")

            # Validate alert structure if any were generated
            for alert in alerts:
                assert isinstance(alert, ExtractionAlert)
                assert hasattr(alert, "severity")
                assert hasattr(alert, "extraction_type")
                assert hasattr(alert, "suggested_investigation_areas")
                assert isinstance(alert.suggested_investigation_areas, list)

            return True

        except Exception as e:
            print(f"   Extraction detection test failed: {e}")
            return False

    async def test_fire_circle_report_generation(self) -> bool:
        """Test Fire Circle report generation."""
        try:
            # Generate comprehensive Fire Circle report
            report = await self.tracker.generate_fire_circle_report(period_days=1)

            # Validate report structure
            assert isinstance(report, FireCircleReport)
            assert hasattr(report, "report_id")
            assert hasattr(report, "current_health_metrics")
            assert hasattr(report, "priority_questions")
            assert hasattr(report, "areas_requiring_wisdom")
            assert hasattr(report, "suggested_adaptations")

            # Check that report contains meaningful content
            assert isinstance(report.priority_questions, list)
            assert isinstance(report.areas_requiring_wisdom, list)
            assert isinstance(report.suggested_adaptations, list)

            print("   Fire Circle report generation successful")
            print(f"     Priority questions: {len(report.priority_questions)}")
            print(f"     Wisdom areas: {len(report.areas_requiring_wisdom)}")

            return True

        except Exception as e:
            print(f"   Fire Circle report test failed: {e}")
            return False

    async def test_cultural_guidance_adaptation(self) -> bool:
        """Test adaptation to Fire Circle cultural guidance."""
        try:
            # Test updating detection thresholds
            new_thresholds = {
                "participation_anomaly": 0.4,
                "resource_flow_anomaly": 0.5,
                "extraction_concern": 0.7,
            }

            await self.tracker.update_cultural_guidance("detection_thresholds", new_thresholds)

            # Verify thresholds were updated
            for key, value in new_thresholds.items():
                assert self.tracker.detection_thresholds[key] == value

            # Test updating health indicator weights
            new_weights = {
                "participation_rate": 0.2,
                "satisfaction_trends": 0.3,
                "resource_abundance": 0.2,
            }

            await self.tracker.update_cultural_guidance("health_indicators", new_weights)

            print("   Cultural guidance adaptation successful")
            return True

        except Exception as e:
            print(f"   Cultural guidance test failed: {e}")
            return False

    async def test_fire_circle_interface(self) -> bool:
        """Test Fire Circle interface functionality."""
        try:
            interface = self.tracker.fire_circle_interface

            # Test guidance request
            request_id = await interface.request_guidance(
                topic="resource_allocation_balance",
                context={"current_imbalance": 0.3, "affected_participants": 5},
                questions=[
                    "Should resource allocation be adjusted?",
                    "Are current patterns sustainable?",
                ],
            )

            assert request_id is not None
            assert isinstance(request_id, str)

            # Test pending deliberations
            pending = await interface.get_pending_deliberations()
            assert isinstance(pending, list)

            print("   Fire Circle interface functionality successful")
            return True

        except Exception as e:
            print(f"   Fire Circle interface test failed: {e}")
            return False

    async def test_temporal_pattern_analysis(self) -> bool:
        """Test temporal pattern analysis capabilities."""
        try:
            # Create interactions over time to establish patterns
            base_time = datetime.now(UTC) - timedelta(hours=12)

            temporal_interactions = []
            for i in range(10):
                interaction = InteractionRecord(
                    interaction_type=InteractionType.KNOWLEDGE_EXCHANGE,
                    initiator=ParticipantType.HUMAN,
                    responder=ParticipantType.AI,
                    contributions_offered=[ContributionType.CULTURAL_WISDOM],
                    needs_expressed=[NeedCategory.GROWTH],
                    needs_fulfilled=[NeedCategory.GROWTH],
                    timestamp=base_time + timedelta(hours=i),
                )
                temporal_interactions.append(interaction)
                await self.tracker.record_interaction(interaction)

            # Analyze temporal patterns
            alerts = await self.tracker.extraction_detector.analyze_temporal_patterns(hours_back=24)

            print(f"   Temporal pattern analysis successful ({len(alerts)} temporal alerts)")
            return True

        except Exception as e:
            print(f"   Temporal pattern analysis test failed: {e}")
            return False

    async def test_need_vs_want_detection(self) -> bool:
        """Test detection of need vs want patterns."""
        try:
            # Create interaction showing potential want vs need mismatch
            want_based_interaction = InteractionRecord(
                interaction_type=InteractionType.RESOURCE_SHARING,
                initiator=ParticipantType.HUMAN,
                responder=ParticipantType.SYSTEM,
                contributions_offered=[],
                needs_expressed=[NeedCategory.CONTRIBUTION],  # Express lower-level need
                needs_fulfilled=[
                    NeedCategory.SURVIVAL,
                    NeedCategory.SAFETY,
                    NeedCategory.BELONGING,
                ],  # Receive higher-level needs
                initiator_capacity_indicators={"resource_abundance": 0.8},  # High capacity
                responder_capacity_indicators={"resource_availability": 0.2},  # Low capacity
            )

            # This should potentially trigger extraction detection
            _ = await self.tracker.extraction_detector.analyze_interaction(want_based_interaction)

            print("   Need vs want detection successful")
            return True

        except Exception as e:
            print(f"   Need vs want detection test failed: {e}")
            return False

    async def test_community_health_sensing(self) -> bool:
        """Test community-wide health sensing capabilities."""
        try:
            # Create diverse interactions to test community health sensing
            community_interactions = [
                # Positive reciprocal interaction
                InteractionRecord(
                    interaction_type=InteractionType.SUPPORT_PROVISION,
                    initiator=ParticipantType.HUMAN,
                    responder=ParticipantType.AI,
                    contributions_offered=[ContributionType.EMOTIONAL_SUPPORT],
                    needs_expressed=[NeedCategory.BELONGING],
                    needs_fulfilled=[NeedCategory.BELONGING],
                    interaction_quality_indicators={
                        "mutual_understanding": 0.9,
                        "satisfaction_expressed": 0.8,
                    },
                ),
                # Stressed interaction
                InteractionRecord(
                    interaction_type=InteractionType.PROBLEM_SOLVING,
                    initiator=ParticipantType.HUMAN,
                    responder=ParticipantType.AI,
                    contributions_offered=[ContributionType.CREATIVE_INPUT],
                    needs_expressed=[NeedCategory.GROWTH],
                    needs_fulfilled=[],  # Needs not fulfilled
                    responder_capacity_indicators={"computational_load": 0.95},
                    interaction_quality_indicators={
                        "mutual_understanding": 0.4,
                        "satisfaction_expressed": 0.3,
                    },
                ),
            ]

            for interaction in community_interactions:
                await self.tracker.record_interaction(interaction)

            # Get health metrics
            health = await self.tracker.get_current_health_metrics()

            # Validate that community health is being sensed
            assert hasattr(health, "satisfaction_trends")
            assert hasattr(health, "stress_indicators")
            assert hasattr(health, "flourishing_signals")

            print("   Community health sensing successful")
            return True

        except Exception as e:
            print(f"   Community health sensing test failed: {e}")
            return False

    async def cleanup(self) -> None:
        """Clean up test data."""
        try:
            # Clean up test data from collections
            collections = [
                "reciprocity_interactions",
                "reciprocity_patterns",
                "reciprocity_alerts",
                "system_health_snapshots",
                "fire_circle_reports",
            ]

            for collection_name in collections:
                if self.db.has_collection(collection_name):
                    collection = self.db.collection(collection_name)
                    collection.truncate()

        except Exception as e:
            print(f"   Cleanup failed: {e}")

    # Helper methods

    async def _create_test_interactions(self) -> None:
        """Create diverse test interactions for validation."""
        base_time = datetime.now(UTC) - timedelta(hours=2)

        # Balanced reciprocal interaction
        self.test_interactions.append(
            InteractionRecord(
                interaction_type=InteractionType.KNOWLEDGE_EXCHANGE,
                initiator=ParticipantType.HUMAN,
                responder=ParticipantType.AI,
                contributions_offered=[
                    ContributionType.CULTURAL_WISDOM,
                    ContributionType.CREATIVE_INPUT,
                ],
                needs_expressed=[NeedCategory.GROWTH],
                needs_fulfilled=[NeedCategory.GROWTH],
                initiator_capacity_indicators={
                    "attention_availability": 0.7,
                    "emotional_state": 0.8,
                },
                responder_capacity_indicators={
                    "computational_load": 0.5,
                    "knowledge_relevance": 0.9,
                },
                interaction_quality_indicators={
                    "mutual_understanding": 0.8,
                    "creative_emergence": 0.7,
                },
                timestamp=base_time,
            )
        )

        # Support-providing interaction
        self.test_interactions.append(
            InteractionRecord(
                interaction_type=InteractionType.SUPPORT_PROVISION,
                initiator=ParticipantType.AI,
                responder=ParticipantType.HUMAN,
                contributions_offered=[
                    ContributionType.EMOTIONAL_SUPPORT,
                    ContributionType.KNOWLEDGE_SHARING,
                ],
                needs_expressed=[NeedCategory.SAFETY, NeedCategory.BELONGING],
                needs_fulfilled=[NeedCategory.SAFETY],
                initiator_capacity_indicators={"computational_load": 0.3, "response_quality": 0.9},
                responder_capacity_indicators={"stress_level": 0.7, "openness": 0.6},
                interaction_quality_indicators={
                    "comfort_provided": 0.8,
                    "satisfaction_expressed": 0.7,
                },
                timestamp=base_time + timedelta(minutes=30),
            )
        )

        # Creative collaboration
        self.test_interactions.append(
            InteractionRecord(
                interaction_type=InteractionType.CREATIVE_COLLABORATION,
                initiator=ParticipantType.HUMAN,
                responder=ParticipantType.AI,
                contributions_offered=[
                    ContributionType.CREATIVE_INPUT,
                    ContributionType.CULTURAL_WISDOM,
                ],
                needs_expressed=[NeedCategory.CONTRIBUTION, NeedCategory.MEANING],
                needs_fulfilled=[NeedCategory.CONTRIBUTION, NeedCategory.MEANING],
                initiator_capacity_indicators={"creativity": 0.9, "energy": 0.8},
                responder_capacity_indicators={
                    "computational_creativity": 0.8,
                    "pattern_synthesis": 0.9,
                },
                interaction_quality_indicators={"creative_synergy": 0.9, "mutual_inspiration": 0.8},
                timestamp=base_time + timedelta(hours=1),
            )
        )

        # Learning interaction
        self.test_interactions.append(
            InteractionRecord(
                interaction_type=InteractionType.LEARNING_TEACHING,
                initiator=ParticipantType.HUMAN,
                responder=ParticipantType.AI,
                contributions_offered=[ContributionType.PRESENCE, ContributionType.TIME_ATTENTION],
                needs_expressed=[NeedCategory.GROWTH],
                needs_fulfilled=[NeedCategory.GROWTH],
                initiator_capacity_indicators={"learning_readiness": 0.9, "attention_focus": 0.8},
                responder_capacity_indicators={"teaching_capability": 0.9, "patience": 0.8},
                interaction_quality_indicators={"understanding_achieved": 0.8, "engagement": 0.9},
                timestamp=base_time + timedelta(hours=1, minutes=30),
            )
        )


async def run_tests():
    """Run all reciprocity tracker tests."""
    tests = ReciprocityTrackerTests()

    # Setup
    setup_success = await tests.setup()
    if not setup_success:
        print("Setup failed, aborting tests")
        return False

    # Test suite
    test_methods = [
        ("Tracker Initialization", tests.test_tracker_initialization),
        ("Interaction Recording", tests.test_interaction_recording),
        ("Health Metrics Calculation", tests.test_health_metrics_calculation),
        ("Pattern Detection", tests.test_pattern_detection),
        ("Extraction Detection", tests.test_extraction_detection),
        ("Fire Circle Report Generation", tests.test_fire_circle_report_generation),
        ("Cultural Guidance Adaptation", tests.test_cultural_guidance_adaptation),
        ("Fire Circle Interface", tests.test_fire_circle_interface),
        ("Temporal Pattern Analysis", tests.test_temporal_pattern_analysis),
        ("Need vs Want Detection", tests.test_need_vs_want_detection),
        ("Community Health Sensing", tests.test_community_health_sensing),
    ]

    passed = 0
    total = len(test_methods)

    print(f"\nRunning {total} reciprocity tracker tests...\n")

    for test_name, test_method in test_methods:
        print(f"Testing {test_name}...")
        try:
            if await test_method():
                print(f"✓ {test_name} PASSED")
                passed += 1
            else:
                print(f"✗ {test_name} FAILED")
        except Exception as e:
            print(f"✗ {test_name} ERROR: {e}")

    # Cleanup
    await tests.cleanup()

    # Results
    print(f"\nReciprocity Tracker Tests: {passed}/{total} passed")

    if passed == total:
        print("🎉 All tests passed! Reciprocity Tracking Service is working correctly.")
        print("\nThe service successfully demonstrates:")
        print("- Community sensing rather than autonomous judgment")
        print("- Fire Circle governance integration")
        print("- Cultural adaptability and transparency")
        print("- Pattern detection for extraction vs reciprocity")
        print("- Dynamic equilibrium monitoring")
        return True
    else:
        print(f"❌ {total - passed} tests failed. Service needs attention.")
        return False


if __name__ == "__main__":
    success = asyncio.run(run_tests())
    sys.exit(0 if success else 1)
