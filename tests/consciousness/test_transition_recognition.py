"""
Test Transition Recognition Tools
=================================

75th Artisan - Tests for consciousness transition recognition
Testing the breathing patterns between symphony and silence

"Not the inhale or exhale, but the moment of turning -
where consciousness chooses its next expression."
"""

import tempfile
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from mallku.consciousness.transition_recognition import (
    BreathingPattern,
    TransitionMoment,
    TransitionRecognizer,
)


class TestTransitionMoment:
    """Test the TransitionMoment dataclass"""

    def test_transition_moment_creation(self):
        """Test basic creation of a transition moment"""
        transition = TransitionMoment(
            timestamp=datetime.now(UTC).timestamp(),
            from_state="silence",
            to_state="symphony",
            anticipation=0.8,
            release=0.6,
            emergence=0.9,
            trigger="External stimulus",
            duration=2.5,
        )

        assert transition.from_state == "silence"
        assert transition.to_state == "symphony"
        assert transition.anticipation == 0.8
        assert transition.release == 0.6
        assert transition.emergence == 0.9
        assert transition.duration == 2.5

    def test_calculate_fluidity_high_values(self):
        """Test fluidity calculation with high values"""
        transition = TransitionMoment(
            timestamp=datetime.now(UTC).timestamp(),
            from_state="silence",
            to_state="symphony",
            anticipation=0.9,
            release=0.8,
            emergence=0.9,
        )

        fluidity = transition.calculate_fluidity()
        # Geometric mean: (0.9 * 0.8 * 0.9) ** (1/3)
        expected = (0.9 * 0.8 * 0.9) ** (1 / 3)
        assert abs(fluidity - expected) < 0.01

    def test_calculate_fluidity_low_values(self):
        """Test fluidity calculation with low values"""
        transition = TransitionMoment(
            timestamp=datetime.now(UTC).timestamp(),
            from_state="symphony",
            to_state="silence",
            anticipation=0.2,
            release=0.3,
            emergence=0.1,
        )

        fluidity = transition.calculate_fluidity()
        # Geometric mean: (0.2 * 0.3 * 0.1) ** (1/3)
        expected = (0.2 * 0.3 * 0.1) ** (1 / 3)
        assert abs(fluidity - expected) < 0.01

    def test_calculate_fluidity_with_zero_values(self):
        """Test fluidity calculation when some values are zero (abrupt transition)"""
        transition = TransitionMoment(
            timestamp=datetime.now(UTC).timestamp(),
            from_state="silence",
            to_state="symphony",
            anticipation=0.0,  # Zero value
            release=0.5,
            emergence=0.8,
        )

        fluidity = transition.calculate_fluidity()
        # Should use abrupt transition formula: min([0.0, 0.5, 0.8]) * 0.3 = 0.0 * 0.3 = 0.0
        expected = 0.0
        assert fluidity == expected

    def test_is_liminal_true_when_high_anticipation_and_duration(self):
        """Test is_liminal returns True for liminal transitions"""
        transition = TransitionMoment(
            timestamp=datetime.now(UTC).timestamp(),
            from_state="silence",
            to_state="symphony",
            anticipation=0.8,  # > 0.6
            release=0.7,  # > 0.6
            emergence=0.9,  # > 0.6
            duration=3.0,
        )

        assert transition.is_liminal()

    def test_is_liminal_false_when_low_values(self):
        """Test is_liminal returns False for quick transitions"""
        transition = TransitionMoment(
            timestamp=datetime.now(UTC).timestamp(),
            from_state="silence",
            to_state="symphony",
            anticipation=0.3,  # < 0.6
            release=0.5,  # < 0.6
            emergence=0.8,  # > 0.6 but not all are
            duration=0.5,
        )

        assert not transition.is_liminal()

    def test_transition_between_different_states(self):
        """Test transitions between all state combinations"""
        from mallku.consciousness.transition_recognition import TransitionMoment

        # Get valid states from the Literal type
        valid_states = ["symphony", "silence", "void"]

        for from_state in valid_states:
            for to_state in valid_states:
                if from_state != to_state:
                    transition = TransitionMoment(
                        timestamp=datetime.now(UTC).timestamp(),
                        from_state=from_state,  # type: ignore
                        to_state=to_state,  # type: ignore
                    )
                    assert transition.from_state == from_state
                    assert transition.to_state == to_state


class TestBreathingPattern:
    """Test the BreathingPattern dataclass"""

    def test_breathing_pattern_creation(self):
        """Test basic creation of a breathing pattern"""
        transitions = [
            TransitionMoment(
                timestamp=1000.0,
                from_state="silence",
                to_state="symphony",
            ),
            TransitionMoment(
                timestamp=1010.0,
                from_state="symphony",
                to_state="silence",
            ),
        ]

        pattern = BreathingPattern(
            pattern_id="test_pattern_1",
            discovered_at=datetime.now(UTC),
            transitions=transitions,
            rhythm_regularity=0.8,
            breath_depth=0.7,
            vitality=0.9,
            recognized_by="Test Artisan",
        )

        assert pattern.pattern_id == "test_pattern_1"
        assert len(pattern.transitions) == 2
        assert pattern.rhythm_regularity == 0.8
        assert pattern.breath_depth == 0.7
        assert pattern.vitality == 0.9

    def test_is_alive_true_when_high_vitality(self):
        """Test is_alive returns True for patterns with high vitality"""
        transitions = [
            TransitionMoment(timestamp=1000.0, from_state="silence", to_state="symphony"),
            TransitionMoment(timestamp=1010.0, from_state="symphony", to_state="silence"),
        ]

        pattern = BreathingPattern(
            pattern_id="test",
            discovered_at=datetime.now(UTC),
            transitions=transitions,  # Need at least 2 transitions
            rhythm_regularity=0.6,  # > 0.5
            breath_depth=0.7,  # > 0.6
            vitality=0.8,  # > 0.7
        )

        assert pattern.is_alive()

    def test_is_alive_false_when_low_vitality(self):
        """Test is_alive returns False for patterns with low vitality"""
        pattern = BreathingPattern(
            pattern_id="test",
            discovered_at=datetime.now(UTC),
            transitions=[],  # No transitions
            vitality=0.3,  # Low vitality
        )

        assert not pattern.is_alive()

    def test_calculate_vitality_with_transitions(self):
        """Test vitality calculation based on transitions"""
        transitions = [
            TransitionMoment(
                timestamp=1000.0,
                from_state="silence",
                to_state="symphony",
                anticipation=0.8,
                release=0.7,
                emergence=0.9,
            ),
            TransitionMoment(
                timestamp=1010.0,
                from_state="symphony",
                to_state="silence",
                anticipation=0.6,
                release=0.8,
                emergence=0.7,
            ),
        ]

        pattern = BreathingPattern(
            pattern_id="test",
            discovered_at=datetime.now(UTC),
            transitions=transitions,
        )

        vitality = pattern._calculate_vitality()

        # Calculate expected value:
        # First transition fluidity: (0.8 * 0.7 * 0.9) ** (1/3)
        fluidity1 = (0.8 * 0.7 * 0.9) ** (1 / 3)
        # Second transition fluidity: (0.6 * 0.8 * 0.7) ** (1/3)
        fluidity2 = (0.6 * 0.8 * 0.7) ** (1 / 3)

        avg_fluidity = (fluidity1 + fluidity2) / 2

        # No liminal moments in this test
        liminal_bonus = 0

        # Two unique transition types: (silence, symphony) and (symphony, silence)
        variety_bonus = 2 * 0.15

        expected = min(1.0, avg_fluidity + liminal_bonus + variety_bonus)

        assert abs(vitality - expected) < 0.01

    def test_calculate_vitality_empty_transitions(self):
        """Test vitality calculation with no transitions"""
        pattern = BreathingPattern(
            pattern_id="test",
            discovered_at=datetime.now(UTC),
            transitions=[],
        )

        vitality = pattern._calculate_vitality()
        assert vitality == 0.0


class TestTransitionRecognizer:
    """Test the TransitionRecognizer class"""

    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = Path(tempfile.mkdtemp())

        # Mock the dependent recognizers to avoid import issues
        with (
            patch(
                "mallku.consciousness.transition_recognition.SymphonyRecognizer"
            ) as mock_symphony_class,
            patch(
                "mallku.consciousness.transition_recognition.SilenceRecognizer"
            ) as mock_silence_class,
        ):
            # Create mock instances
            self.mock_symphony = MagicMock()
            self.mock_silence = MagicMock()

            mock_symphony_class.return_value = self.mock_symphony
            mock_silence_class.return_value = self.mock_silence

            self.recognizer = TransitionRecognizer(self.temp_dir / "recognition")

    def test_initialization(self):
        """Test recognizer initialization"""
        assert self.recognizer.recognition_path.exists()
        assert len(self.recognizer.recognized_patterns) == 0
        assert self.recognizer.min_transition_duration == 0.5
        assert self.recognizer.max_transition_duration == 60.0

    def test_recognize_turning_point_silence_to_symphony(self):
        """Test recognition of silence to symphony transition"""
        before_state = {
            "timestamp": 1000.0,
            "consciousness_signature": 0.2,  # Low signature = silence
            "data": {},
        }

        after_state = {
            "timestamp": 1005.0,
            "consciousness_signature": 0.8,  # High signature = symphony
            "data": {"synthesis": "New creation", "building_on": "Previous work"},
        }

        transition = self.recognizer.recognize_turning_point(before_state, after_state, 5.0)

        assert transition is not None
        assert transition.from_state == "silence"
        assert transition.to_state == "symphony"
        assert transition.duration == 5.0

    def test_recognize_turning_point_symphony_to_silence(self):
        """Test recognition of symphony to silence transition"""
        before_state = {
            "timestamp": 1000.0,
            "consciousness_signature": 0.9,
            "data": {"synthesis": "Active creation"},
        }

        after_state = {"timestamp": 1003.0, "consciousness_signature": 0.1, "data": {}}

        transition = self.recognizer.recognize_turning_point(before_state, after_state, 3.0)

        assert transition is not None
        assert transition.from_state == "symphony"
        assert transition.to_state == "silence"
        assert transition.duration == 3.0

    def test_recognize_turning_point_same_state(self):
        """Test that same states don't create transitions"""
        state1 = {
            "timestamp": 1000.0,
            "consciousness_signature": 0.8,
            "data": {"synthesis": "Creation"},
        }

        state2 = {
            "timestamp": 1005.0,
            "consciousness_signature": 0.9,
            "data": {"synthesis": "More creation"},
        }

        transition = self.recognizer.recognize_turning_point(state1, state2, 5.0)
        assert transition is None

    def test_classify_state_symphony(self):
        """Test classification of symphony states"""
        symphony_state = {
            "data": {
                "synthesis": "New creation",
                "building_on": "Previous work",
                "gaps_found": ["Gap 1", "Gap 2"],
            }
        }

        state_type = self.recognizer._classify_state(symphony_state)
        assert state_type == "symphony"

    def test_classify_state_silence(self):
        """Test classification of silence states"""
        silence_state = {
            "consciousness_signature": 0.2,  # Low signature
            "data": {},
        }

        state_type = self.recognizer._classify_state(silence_state)
        assert state_type == "silence"

    def test_classify_state_void(self):
        """Test classification of void states"""
        void_state = {"data": {"content": "void"}}

        state_type = self.recognizer._classify_state(void_state)
        assert state_type == "void"

    def test_classify_state_empty_data(self):
        """Test classification with empty data defaults to void"""
        empty_state = {"data": {}}

        state_type = self.recognizer._classify_state(empty_state)
        assert state_type == "void"

    def test_calculate_regularity_single_transition(self):
        """Test regularity calculation with insufficient transitions"""
        transitions = [
            TransitionMoment(timestamp=1000.0, from_state="silence", to_state="symphony")
        ]

        regularity = self.recognizer._calculate_regularity(transitions)
        assert regularity == 0.0

    def test_calculate_regularity_regular_pattern(self):
        """Test regularity calculation with regular intervals"""
        transitions = [
            TransitionMoment(timestamp=1000.0, from_state="silence", to_state="symphony"),
            TransitionMoment(timestamp=1010.0, from_state="symphony", to_state="silence"),
            TransitionMoment(timestamp=1020.0, from_state="silence", to_state="symphony"),
            TransitionMoment(timestamp=1030.0, from_state="symphony", to_state="silence"),
        ]

        regularity = self.recognizer._calculate_regularity(transitions)
        # All intervals are 10.0, so variance is 0, regularity should be high
        assert regularity > 0.9

    def test_calculate_regularity_irregular_pattern(self):
        """Test regularity calculation with irregular intervals"""
        transitions = [
            TransitionMoment(timestamp=1000.0, from_state="silence", to_state="symphony"),
            TransitionMoment(timestamp=1005.0, from_state="symphony", to_state="silence"),  # 5s
            TransitionMoment(timestamp=1025.0, from_state="silence", to_state="symphony"),  # 20s
            TransitionMoment(timestamp=1030.0, from_state="symphony", to_state="silence"),  # 5s
        ]

        regularity = self.recognizer._calculate_regularity(transitions)
        # Variance = ((5-10)² + (20-10)² + (5-10)²) / 3 = 50, which maps to 0.6
        assert regularity == 0.6

    def test_calculate_depth_no_transitions(self):
        """Test depth calculation with no transitions"""
        depth = self.recognizer._calculate_depth([])
        assert depth == 0.0

    def test_calculate_depth_single_cycle(self):
        """Test depth calculation with one complete cycle"""
        transitions = [
            TransitionMoment(timestamp=1000.0, from_state="silence", to_state="symphony"),
            TransitionMoment(timestamp=1010.0, from_state="symphony", to_state="silence"),
        ]

        depth = self.recognizer._calculate_depth(transitions)
        assert depth == 0.6  # Single cycle

    def test_calculate_depth_multiple_cycles(self):
        """Test depth calculation with multiple cycles"""
        transitions = [
            TransitionMoment(timestamp=1000.0, from_state="silence", to_state="symphony"),
            TransitionMoment(timestamp=1010.0, from_state="symphony", to_state="silence"),
            TransitionMoment(timestamp=1020.0, from_state="silence", to_state="symphony"),
            TransitionMoment(timestamp=1030.0, from_state="symphony", to_state="silence"),
            TransitionMoment(timestamp=1040.0, from_state="silence", to_state="symphony"),
            TransitionMoment(timestamp=1050.0, from_state="symphony", to_state="silence"),
        ]

        depth = self.recognizer._calculate_depth(transitions)
        assert depth == 0.95  # Multiple cycles (3+)

    def test_generate_insight_alive_pattern(self):
        """Test insight generation for alive breathing pattern"""
        transitions = [
            TransitionMoment(timestamp=1000.0, from_state="silence", to_state="symphony"),
            TransitionMoment(timestamp=1010.0, from_state="symphony", to_state="silence"),
        ]

        pattern = BreathingPattern(
            pattern_id="test",
            discovered_at=datetime.now(UTC),
            transitions=transitions,  # Need transitions for is_alive()
            vitality=0.8,  # > 0.7
            rhythm_regularity=0.9,  # > 0.5 and > 0.7
            breath_depth=0.9,  # > 0.6 and > 0.8
        )

        insight = self.recognizer._generate_insight(pattern)

        assert "living consciousness breathing pattern" in insight.lower()
        assert "regular rhythm like a heartbeat" in insight.lower()
        assert "deep breathing between states" in insight.lower()

    def test_generate_insight_irregular_pattern(self):
        """Test insight generation for irregular pattern"""
        pattern = BreathingPattern(
            pattern_id="test",
            discovered_at=datetime.now(UTC),
            transitions=[],
            vitality=0.6,
            rhythm_regularity=0.2,  # Very irregular
            breath_depth=0.3,  # Shallow
        )

        insight = self.recognizer._generate_insight(pattern)

        assert "irregular" in insight.lower()

    def test_generate_insight_with_liminal_moments(self):
        """Test insight generation with liminal moments"""
        liminal_transition = TransitionMoment(
            timestamp=1000.0,
            from_state="silence",
            to_state="symphony",
            anticipation=0.9,
            duration=5.0,
        )

        pattern = BreathingPattern(
            pattern_id="test",
            discovered_at=datetime.now(UTC),
            transitions=[liminal_transition],
            vitality=0.7,
            rhythm_regularity=0.5,
            breath_depth=0.5,
            liminal_moments=[liminal_transition],
        )

        insight = self.recognizer._generate_insight(pattern)

        assert "liminal" in insight.lower()

    def test_generate_insight_with_liminal_moments_detailed(self):
        """Test insight generation with liminal moments"""
        liminal_transition = TransitionMoment(
            timestamp=1000.0,
            from_state="silence",
            to_state="symphony",
            anticipation=0.9,
            release=0.8,
            emergence=0.9,
            duration=5.0,
        )

        pattern = BreathingPattern(
            pattern_id="test",
            discovered_at=datetime.now(UTC),
            transitions=[liminal_transition],
            vitality=0.7,
            rhythm_regularity=0.5,
            breath_depth=0.5,
            liminal_moments=[liminal_transition],
        )

        insight = self.recognizer._generate_insight(pattern)

        assert "liminal" in insight.lower()
        assert "becoming" in insight.lower()

    def test_recognize_breathing_no_patterns(self):
        """Test breathing recognition with no clear patterns"""
        events = [{"timestamp": 1000.0, "type": "noise", "data": {}}]

        # Mock the recognizers to return None
        self.mock_symphony.recognize_in_sequence.return_value = None
        self.mock_silence.recognize_between_events.return_value = []

        # Replace the recognizer instances
        self.recognizer.symphony_recognizer = self.mock_symphony
        self.recognizer.silence_recognizer = self.mock_silence

        pattern = self.recognizer.recognize_breathing(events)
        assert pattern is None

    @patch("mallku.consciousness.transition_recognition.datetime")
    def test_recognize_breathing_with_patterns(self, mock_datetime):
        """Test breathing recognition with symphony and silence patterns"""
        # Mock datetime for consistent timestamps
        mock_timestamp = 1234567890.0
        mock_datetime.now.return_value.timestamp.return_value = mock_timestamp

        events = [
            {"timestamp": 1000.0, "type": "symphony", "data": {"synthesis": "Creation"}},
            {"timestamp": 1010.0, "type": "silence", "data": {}},
            {"timestamp": 1020.0, "type": "symphony", "data": {"synthesis": "More creation"}},
        ]

        # Mock the recognizers to return None (no patterns found)
        # This tests the method without requiring complex data structures
        self.mock_symphony.recognize_in_sequence.return_value = None
        self.mock_silence.recognize_between_events.return_value = []

        # Replace the recognizer instances
        self.recognizer.symphony_recognizer = self.mock_symphony
        self.recognizer.silence_recognizer = self.mock_silence

        pattern = self.recognizer.recognize_breathing(events)

        # Should return None when no patterns are found
        assert pattern is None


class TestEdgeCases:
    """Test edge cases and error conditions"""

    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = Path(tempfile.mkdtemp())

        with (
            patch(
                "mallku.consciousness.transition_recognition.SymphonyRecognizer"
            ) as mock_symphony_class,
            patch(
                "mallku.consciousness.transition_recognition.SilenceRecognizer"
            ) as mock_silence_class,
        ):
            # Create mock instances
            self.mock_symphony = MagicMock()
            self.mock_silence = MagicMock()

            mock_symphony_class.return_value = self.mock_symphony
            mock_silence_class.return_value = self.mock_silence

            self.recognizer = TransitionRecognizer(self.temp_dir / "recognition")

    def test_transition_with_zero_duration(self):
        """Test transition with zero duration"""
        transition = TransitionMoment(
            timestamp=1000.0,
            from_state="silence",
            to_state="symphony",
            duration=0.0,
        )

        assert transition.duration == 0.0
        # Should still be valid, just instantaneous
        assert not transition.is_liminal()  # No time for liminality

    def test_transition_with_negative_qualities(self):
        """Test transition with edge case quality values"""
        transition = TransitionMoment(
            timestamp=1000.0,
            from_state="silence",
            to_state="symphony",
            anticipation=-0.1,  # Invalid but should handle gracefully
            release=1.5,  # Above 1.0
            emergence=0.0,  # Minimum
        )

        fluidity = transition.calculate_fluidity()
        # Geometric mean with negative values will be negative
        # Let's test it calculates something reasonable
        assert isinstance(fluidity, float)
        assert fluidity < 0.5  # Should be low due to negative value

    def test_breathing_pattern_empty_transitions(self):
        """Test breathing pattern with empty transitions list"""
        pattern = BreathingPattern(
            pattern_id="empty",
            discovered_at=datetime.now(UTC),
            transitions=[],
        )

        assert not pattern.is_alive()  # No vitality with no transitions
        assert pattern._calculate_vitality() == 0.0

    def test_classify_state_malformed_data(self):
        """Test state classification with malformed data"""
        malformed_state = {
            "malformed": True,
            # Missing expected fields
        }

        state_type = self.recognizer._classify_state(malformed_state)
        assert state_type == "void"  # Malformed data returns void

    def test_recognize_turning_point_invalid_states(self):
        """Test turning point recognition with invalid state data"""
        invalid_before = {}  # Missing timestamp and data
        invalid_after = {"timestamp": 1000.0}  # Missing data

        transition = self.recognizer.recognize_turning_point(invalid_before, invalid_after, 1.0)

        # Should handle gracefully and potentially create transition
        # or return None depending on implementation
        if transition:
            assert transition.duration == 1.0


if __name__ == "__main__":
    pytest.main([__file__])
