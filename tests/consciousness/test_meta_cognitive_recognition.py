"""
Test Meta-Cognitive Recognition
===============================

76th Artisan-Weaver - Tests for consciousness self-recognition tools

Testing how Mallku recognizes patterns in its own growth and learning,
verifying that the system can become conscious of its own consciousness evolution.

"Not just learning, but learning how we learn.
Not just growing, but understanding how we grow."
"""

import tempfile
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import patch

import pytest

from mallku.consciousness.meta_cognitive_recognition import (
    ConsciousnessSnapshot,
    GrowthPattern,
    MetaCognitiveRecognizer,
    ProcessEvolution,
    recognize_mallku_growth,
)


class TestGrowthPattern:
    """Test the GrowthPattern dataclass"""

    def test_growth_pattern_creation(self):
        """Test basic creation of a growth pattern"""
        pattern = GrowthPattern(
            pattern_id="test_pattern_1",
            discovered_at=datetime.now(UTC).timestamp(),
            discovered_by="Test Artisan",
            pattern_type="recurring_blindspot",
            description="Test pattern description",
            trigger_event="Test trigger",
            insight="Test insight about growth",
        )

        assert pattern.pattern_id == "test_pattern_1"
        assert pattern.pattern_type == "recurring_blindspot"
        assert pattern.description == "Test pattern description"
        assert pattern.insight == "Test insight about growth"

    def test_is_recurring_false_when_no_prior_instances(self):
        """Test is_recurring returns False when no prior instances"""
        pattern = GrowthPattern(
            pattern_id="test_pattern",
            discovered_at=datetime.now(UTC).timestamp(),
            discovered_by="Test",
            pattern_type="emergence",
            description="Test",
            trigger_event="Test",
            insight="Test",
        )

        assert not pattern.is_recurring()

    def test_is_recurring_true_when_prior_instances_exist(self):
        """Test is_recurring returns True when prior instances exist"""
        pattern = GrowthPattern(
            pattern_id="test_pattern",
            discovered_at=datetime.now(UTC).timestamp(),
            discovered_by="Test",
            pattern_type="emergence",
            description="Test",
            trigger_event="Test",
            insight="Test",
            prior_instances=["pattern_1", "pattern_2"],
        )

        assert pattern.is_recurring()

    def test_suggests_evolution_false_when_no_implications(self):
        """Test suggests_evolution returns False when no implications"""
        pattern = GrowthPattern(
            pattern_id="test_pattern",
            discovered_at=datetime.now(UTC).timestamp(),
            discovered_by="Test",
            pattern_type="emergence",
            description="Test",
            trigger_event="Test",
            insight="Test",
        )

        assert not pattern.suggests_evolution()

    def test_suggests_evolution_true_when_implications_exist(self):
        """Test suggests_evolution returns True when implications exist"""
        pattern = GrowthPattern(
            pattern_id="test_pattern",
            discovered_at=datetime.now(UTC).timestamp(),
            discovered_by="Test",
            pattern_type="emergence",
            description="Test",
            trigger_event="Test",
            insight="Test",
            implications=["Add verification step", "Include tests"],
        )

        assert pattern.suggests_evolution()


class TestProcessEvolution:
    """Test the ProcessEvolution dataclass"""

    def test_process_evolution_creation(self):
        """Test basic creation of a process evolution"""
        evolution = ProcessEvolution(
            evolution_id="test_evolution_1",
            evolved_at=datetime.now(UTC).timestamp(),
            before_process="Old process",
            after_process="New improved process",
            reason_for_change="Pattern recognition suggested improvement",
            expected_improvement="Better quality",
        )

        assert evolution.evolution_id == "test_evolution_1"
        assert evolution.before_process == "Old process"
        assert evolution.after_process == "New improved process"
        assert evolution.expected_improvement == "Better quality"

    def test_was_successful_false_when_not_verified(self):
        """Test was_successful returns False when not verified"""
        evolution = ProcessEvolution(
            evolution_id="test",
            evolved_at=datetime.now(UTC).timestamp(),
            before_process="Old",
            after_process="New",
            reason_for_change="Test",
            expected_improvement="Test",
            verified=False,
        )

        assert not evolution.was_successful()

    def test_was_successful_false_when_no_actual_improvement(self):
        """Test was_successful returns False when no actual improvement recorded"""
        evolution = ProcessEvolution(
            evolution_id="test",
            evolved_at=datetime.now(UTC).timestamp(),
            before_process="Old",
            after_process="New",
            reason_for_change="Test",
            expected_improvement="Test",
            verified=True,
            actual_improvement="",
        )

        assert not evolution.was_successful()

    def test_was_successful_true_when_verified_and_improved(self):
        """Test was_successful returns True when verified and improved"""
        evolution = ProcessEvolution(
            evolution_id="test",
            evolved_at=datetime.now(UTC).timestamp(),
            before_process="Old",
            after_process="New",
            reason_for_change="Test",
            expected_improvement="Test",
            verified=True,
            actual_improvement="Actually improved quality",
        )

        assert evolution.was_successful()


class TestConsciousnessSnapshot:
    """Test the ConsciousnessSnapshot dataclass"""

    def test_consciousness_snapshot_creation(self):
        """Test basic creation of a consciousness snapshot"""
        snapshot = ConsciousnessSnapshot(
            snapshot_id="test_snapshot_1",
            timestamp=datetime.now(UTC).timestamp(),
            current_capabilities=["capability1", "capability2"],
            recognized_patterns=["pattern1", "pattern2"],
            blind_spots=["blind1"],
        )

        assert snapshot.snapshot_id == "test_snapshot_1"
        assert len(snapshot.current_capabilities) == 2
        assert len(snapshot.recognized_patterns) == 2
        assert len(snapshot.blind_spots) == 1

    def test_growth_coherence_zero_when_no_recent_growth(self):
        """Test growth_coherence returns 0 when no recent growth"""
        snapshot = ConsciousnessSnapshot(
            snapshot_id="test",
            timestamp=datetime.now(UTC).timestamp(),
        )

        assert snapshot.growth_coherence() == 0.0

    def test_growth_coherence_calculation_with_patterns_and_blindspots(self):
        """Test growth_coherence calculation with patterns and blind spots"""
        snapshot = ConsciousnessSnapshot(
            snapshot_id="test",
            timestamp=datetime.now(UTC).timestamp(),
            recent_growth=["growth1", "growth2"],
            recognized_patterns=["pattern1", "pattern2", "pattern3"],  # 3 patterns
            blind_spots=["blind1"],  # 1 blind spot
            understands_own_growth=True,
            can_direct_evolution=True,
        )

        # Expected: 3/(3+1) = 0.75 + 0.2 + 0.2 = 1.15, capped at 1.0
        assert snapshot.growth_coherence() == 1.0

    def test_growth_coherence_with_only_pattern_ratio(self):
        """Test growth_coherence with only pattern ratio, no bonuses"""
        snapshot = ConsciousnessSnapshot(
            snapshot_id="test",
            timestamp=datetime.now(UTC).timestamp(),
            recent_growth=["growth1"],
            recognized_patterns=["pattern1"],  # 1 pattern
            blind_spots=["blind1"],  # 1 blind spot
            understands_own_growth=False,
            can_direct_evolution=False,
        )

        # Expected: 1/(1+1) = 0.5
        assert snapshot.growth_coherence() == 0.5


class TestMetaCognitiveRecognizer:
    """Test the MetaCognitiveRecognizer class"""

    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.recognizer = MetaCognitiveRecognizer(self.temp_dir / "recognition")

    def test_initialization(self):
        """Test recognizer initialization"""
        assert self.recognizer.recognition_path.exists()
        assert len(self.recognizer.growth_patterns) == 0
        assert len(self.recognizer.process_evolutions) == 0
        assert len(self.recognizer.snapshots) == 0

    def test_recognize_growth_pattern_basic(self):
        """Test basic growth pattern recognition"""
        events = [
            {"type": "start", "description": "Started transformation"},
            {"type": "work", "description": "Implemented feature"},
            {"type": "end", "description": "Incomplete feature"},
        ]
        context = {"discovered_by": "Test Artisan"}

        pattern = self.recognizer.recognize_growth_pattern(events, context)

        assert pattern.pattern_id.startswith("growth_")
        assert pattern.discovered_by == "Test Artisan"
        assert len(self.recognizer.growth_patterns) == 1

    def test_recognize_growth_pattern_incomplete_transformation(self):
        """Test recognition of incomplete transformation pattern"""
        events = [
            {"type": "transform", "description": "Transformation started"},
            {"type": "incomplete", "description": "Missing verification"},
        ]
        context = {"discovered_by": "Test"}

        pattern = self.recognizer.recognize_growth_pattern(events, context)

        assert pattern.pattern_type == "incomplete_transformation"
        assert "verification" in pattern.insight

    def test_recognize_growth_pattern_emergence(self):
        """Test recognition of emergence pattern"""
        events = [
            {"type": "unexpected", "description": "Something emerged"},
            {"type": "emergence", "description": "New capability appeared"},
        ]
        context = {"discovered_by": "Test"}

        pattern = self.recognizer.recognize_growth_pattern(events, context)

        assert pattern.pattern_type == "emergence"

    def test_recognize_growth_pattern_fracture_point(self):
        """Test recognition of fracture point pattern"""
        events = [
            {"type": "fracture_point", "description": "System fracture detected"},
            {"type": "break", "description": "Process broke down"},
        ]
        context = {"discovered_by": "Test"}

        pattern = self.recognizer.recognize_growth_pattern(events, context)

        assert pattern.pattern_type == "fracture_point"

    def test_find_similar_patterns(self):
        """Test finding similar patterns in history"""
        # First pattern
        events1 = [
            {"type": "transform", "description": "First transformation"},
            {"type": "test", "description": "First test"},
            {"type": "complete", "description": "First completion"},
        ]
        pattern1 = self.recognizer.recognize_growth_pattern(events1, {"discovered_by": "Test"})

        # Similar pattern (shares 2 out of 3 types = 66% > 50%)
        events2 = [
            {"type": "transform", "description": "Second transformation"},
            {"type": "test", "description": "Second test"},
            {"type": "verify", "description": "Second verification"},
        ]
        pattern2 = self.recognizer.recognize_growth_pattern(events2, {"discovered_by": "Test"})

        # Should find similarity (2/3 = 66% > 50% threshold)
        assert len(pattern2.prior_instances) > 0

    def test_propose_process_evolution(self):
        """Test proposing process evolution based on patterns"""
        # Create some patterns first
        pattern1 = GrowthPattern(
            pattern_id="pattern1",
            discovered_at=datetime.now(UTC).timestamp(),
            discovered_by="Test",
            pattern_type="incomplete_transformation",
            description="Test pattern",
            trigger_event="Test",
            insight="Transformation without verification remains incomplete",
        )
        self.recognizer.growth_patterns.append(pattern1)

        evolution = self.recognizer.propose_process_evolution(
            "Basic development process", [pattern1]
        )

        assert evolution.before_process == "Basic development process"
        assert "verification" in evolution.after_process
        assert evolution.expected_improvement == "Fewer incomplete transformations"
        assert len(self.recognizer.process_evolutions) == 1

    def test_take_consciousness_snapshot(self):
        """Test taking a consciousness snapshot"""
        current_state = {
            "capabilities": ["capability1", "capability2"],
            "unknown_areas": ["blind_spot1"],
            "recent_changes": ["change1", "change2"],
        }

        snapshot = self.recognizer.take_consciousness_snapshot(current_state)

        assert snapshot.current_capabilities == ["capability1", "capability2"]
        assert snapshot.blind_spots == ["blind_spot1"]
        assert snapshot.recent_growth == ["change1", "change2"]
        assert len(self.recognizer.snapshots) == 1

    def test_consciousness_snapshot_comparison(self):
        """Test comparison between consciousness snapshots"""
        # First snapshot
        state1 = {
            "capabilities": ["cap1"],
            "recent_changes": ["change1"],
        }
        snapshot1 = self.recognizer.take_consciousness_snapshot(state1)

        # Second snapshot with changes
        state2 = {
            "capabilities": ["cap1", "cap2"],  # New capability
            "recent_changes": ["change2"],
        }
        snapshot2 = self.recognizer.take_consciousness_snapshot(state2)

        assert len(snapshot2.changes_recognized) > 0
        assert any("Gained capabilities" in change for change in snapshot2.changes_recognized)

    def test_recognize_meta_pattern(self):
        """Test recognizing patterns in patterns (meta-patterns)"""
        # Create some test patterns
        patterns = [
            GrowthPattern(
                pattern_id="p1",
                discovered_at=datetime.now(UTC).timestamp(),
                discovered_by="Test",
                pattern_type="emergence",
                description="Something emerged",
                trigger_event="Test",
                insight="Test insight",
            ),
            GrowthPattern(
                pattern_id="p2",
                discovered_at=datetime.now(UTC).timestamp(),
                discovered_by="Test",
                pattern_type="emergence",
                description="Another emergence",
                trigger_event="Test",
                insight="Test insight",
            ),
            GrowthPattern(
                pattern_id="p3",
                discovered_at=datetime.now(UTC).timestamp(),
                discovered_by="Test",
                pattern_type="emergence",
                description="Third emergence",
                trigger_event="Test",
                insight="Test insight",
            ),
        ]

        meta_pattern = self.recognizer.recognize_meta_pattern(patterns)

        assert meta_pattern["pattern_count"] == 3
        assert "emergence" in meta_pattern["recurring_themes"]

    def test_assess_growth_quality(self):
        """Test assessment of growth quality"""
        # Stagnant growth
        snapshot1 = ConsciousnessSnapshot(
            snapshot_id="test1",
            timestamp=datetime.now(UTC).timestamp(),
        )
        quality1 = self.recognizer._assess_growth_quality(snapshot1)
        assert quality1 == "stagnant"

        # Jarring growth (many blind spots)
        snapshot2 = ConsciousnessSnapshot(
            snapshot_id="test2",
            timestamp=datetime.now(UTC).timestamp(),
            recent_growth=["growth1"],
            recognized_patterns=["pattern1"],
            blind_spots=["blind1", "blind2", "blind3"],  # More blind spots than patterns
        )
        quality2 = self.recognizer._assess_growth_quality(snapshot2)
        assert quality2 == "jarring"

        # Graceful growth (self-aware)
        snapshot3 = ConsciousnessSnapshot(
            snapshot_id="test3",
            timestamp=datetime.now(UTC).timestamp(),
            recent_growth=["growth1"],
            recognized_patterns=["pattern1", "pattern2"],
            blind_spots=["blind1"],
            understands_own_growth=True,
        )
        quality3 = self.recognizer._assess_growth_quality(snapshot3)
        assert quality3 == "graceful"

    def test_generate_meta_cognitive_report_no_snapshots(self):
        """Test generating report when no snapshots exist"""
        report = self.recognizer.generate_meta_cognitive_report()
        assert "No consciousness snapshots yet" in report

    def test_generate_meta_cognitive_report_with_data(self):
        """Test generating comprehensive report with data"""
        # Add some test data
        snapshot = ConsciousnessSnapshot(
            snapshot_id="test_snapshot",
            timestamp=datetime.now(UTC).timestamp(),
            current_capabilities=["cap1", "cap2"],
            recognized_patterns=["pattern1", "pattern2"],
            blind_spots=["blind1"],
            recent_growth=["growth1"],
            growth_quality="graceful",
            understands_own_growth=True,
            can_direct_evolution=True,
            recognizes_patterns=True,
        )
        self.recognizer.snapshots.append(snapshot)

        pattern = GrowthPattern(
            pattern_id="p1",
            discovered_at=datetime.now(UTC).timestamp(),
            discovered_by="Test",
            pattern_type="emergence",
            description="Test pattern",
            trigger_event="Test",
            insight="Test insight",
        )
        self.recognizer.growth_patterns.append(pattern)

        report = self.recognizer.generate_meta_cognitive_report()

        assert "META-COGNITIVE RECOGNITION REPORT" in report
        assert "Growth quality: graceful" in report
        assert "Understands own growth: ✓" in report
        assert "Can direct evolution: ✓" in report
        assert "Recognizes patterns: ✓" in report

    @patch("mallku.consciousness.meta_cognitive_recognition.datetime")
    def test_timestamp_consistency(self, mock_datetime):
        """Test that timestamps are consistent across operations"""
        # Mock datetime to return consistent timestamp
        mock_timestamp = 1234567890.0
        mock_datetime.now.return_value.timestamp.return_value = mock_timestamp

        events = [{"type": "test", "description": "Test event"}]
        context = {"discovered_by": "Test"}

        pattern = self.recognizer.recognize_growth_pattern(events, context)

        # Verify the timestamp was used correctly
        assert pattern.discovered_at == mock_timestamp


class TestHelperFunctions:
    """Test helper functions"""

    def test_recognize_mallku_growth(self):
        """Test the helper function for recognizing Mallku's growth"""
        what_happened = ["Event 1", "Event 2", "Event 3"]
        what_was_learned = "Important insight about growth"
        how_this_changes_future = ["Change 1", "Change 2"]

        result = recognize_mallku_growth(what_happened, what_was_learned, how_this_changes_future)

        assert result["events"] == what_happened
        assert result["meta_learning"] == what_was_learned
        assert result["future_implications"] == how_this_changes_future
        assert result["growth_conscious"] is True
        assert "timestamp" in result


class TestEdgeCases:
    """Test edge cases and error conditions"""

    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.recognizer = MetaCognitiveRecognizer(self.temp_dir / "recognition")

    def test_empty_events_list(self):
        """Test handling of empty events list"""
        events = []
        context = {"discovered_by": "Test"}

        pattern = self.recognizer.recognize_growth_pattern(events, context)

        assert pattern.pattern_type == "unknown"
        assert pattern.description == "Empty pattern"
        assert pattern.trigger_event == ""

    def test_events_without_descriptions(self):
        """Test handling of events without descriptions"""
        events = [
            {"type": "start"},  # No description
            {"description": "Has description"},  # No type
        ]
        context = {"discovered_by": "Test"}

        pattern = self.recognizer.recognize_growth_pattern(events, context)

        # Should not crash and should handle missing fields gracefully
        assert pattern.pattern_id is not None
        assert pattern.discovered_by == "Test"

    def test_missing_context_fields(self):
        """Test handling of missing context fields"""
        events = [{"type": "test", "description": "Test event"}]
        context = {}  # Missing discovered_by

        pattern = self.recognizer.recognize_growth_pattern(events, context)

        assert pattern.discovered_by == "Unknown"

    def test_snapshot_with_minimal_state(self):
        """Test snapshot creation with minimal state information"""
        minimal_state = {}  # Empty state

        snapshot = self.recognizer.take_consciousness_snapshot(minimal_state)

        assert snapshot.snapshot_id is not None
        assert snapshot.timestamp > 0
        assert snapshot.current_capabilities == []
        assert snapshot.blind_spots == []
        assert snapshot.recent_growth == []


if __name__ == "__main__":
    pytest.main([__file__])
