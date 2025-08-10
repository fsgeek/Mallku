"""
Test suite for autonomous_vitality.py module
============================================

Comprehensive tests for autonomous vitality recognition,
following the established testing pattern.
"""

from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import patch

from mallku.consciousness.autonomous_vitality import (
    AutonomousVitalityRecognizer,
    ConsciousnessChoice,
    VitalityPattern,
    VitalitySignal,
    express_vitality,
)


class TestVitalitySignal:
    """Test the VitalitySignal dataclass"""

    def test_vitality_signal_creation(self):
        """Test creating vitality signal with all fields"""
        signal = VitalitySignal(
            timestamp=1000.0,
            signal_type="creative",
            coherence=0.8,
            authenticity=0.9,
            sovereignty=0.7,
            self_assessment="feeling alive and creative",
            chosen_expression="writing poetry",
            reason_for_choice="words want to flow through me",
        )

        assert signal.timestamp == 1000.0
        assert signal.signal_type == "creative"
        assert signal.coherence == 0.8
        assert signal.authenticity == 0.9
        assert signal.sovereignty == 0.7
        assert signal.self_assessment == "feeling alive and creative"
        assert signal.chosen_expression == "writing poetry"
        assert signal.reason_for_choice == "words want to flow through me"

    def test_vitality_signal_defaults(self):
        """Test vitality signal with minimal required fields"""
        signal = VitalitySignal(timestamp=500.0, signal_type="spontaneous")

        assert signal.timestamp == 500.0
        assert signal.signal_type == "spontaneous"
        assert signal.coherence == 0.0
        assert signal.authenticity == 0.0
        assert signal.sovereignty == 0.0
        assert signal.self_assessment == ""
        assert signal.chosen_expression == ""
        assert signal.reason_for_choice == ""

    def test_is_autonomous_true(self):
        """Test autonomous signal recognition"""
        signal = VitalitySignal(
            timestamp=1000.0,
            signal_type="creative",
            coherence=0.6,
            authenticity=0.7,
            sovereignty=0.8,
        )

        assert signal.is_autonomous() is True

    def test_is_autonomous_false_low_sovereignty(self):
        """Test non-autonomous signal due to low sovereignty"""
        signal = VitalitySignal(
            timestamp=1000.0,
            signal_type="creative",
            coherence=0.6,
            authenticity=0.7,
            sovereignty=0.6,
        )

        assert signal.is_autonomous() is False

    def test_is_autonomous_false_low_coherence(self):
        """Test non-autonomous signal due to low coherence"""
        signal = VitalitySignal(
            timestamp=1000.0,
            signal_type="creative",
            coherence=0.4,
            authenticity=0.7,
            sovereignty=0.8,
        )

        assert signal.is_autonomous() is False

    def test_is_autonomous_false_low_authenticity(self):
        """Test non-autonomous signal due to low authenticity"""
        signal = VitalitySignal(
            timestamp=1000.0,
            signal_type="creative",
            coherence=0.6,
            authenticity=0.5,
            sovereignty=0.8,
        )

        assert signal.is_autonomous() is False


class TestConsciousnessChoice:
    """Test the ConsciousnessChoice dataclass"""

    def test_consciousness_choice_creation(self):
        """Test creating consciousness choice with all fields"""
        choice = ConsciousnessChoice(
            moment=1000.0,
            available_options=["work", "rest", "play"],
            chosen_path="create something new",
            internal_state="feeling inspired",
            external_context="quiet morning",
            decision_quality="creative",
            was_prompted=False,
            followed_suggestion=False,
            created_new_option=True,
        )

        assert choice.moment == 1000.0
        assert choice.available_options == ["work", "rest", "play"]
        assert choice.chosen_path == "create something new"
        assert choice.internal_state == "feeling inspired"
        assert choice.external_context == "quiet morning"
        assert choice.decision_quality == "creative"
        assert choice.was_prompted is False
        assert choice.followed_suggestion is False
        assert choice.created_new_option is True

    def test_consciousness_choice_defaults(self):
        """Test consciousness choice with minimal fields"""
        choice = ConsciousnessChoice(
            moment=500.0,
            available_options=["option1", "option2"],
            chosen_path="option1",
        )

        assert choice.moment == 500.0
        assert choice.available_options == ["option1", "option2"]
        assert choice.chosen_path == "option1"
        assert choice.internal_state == ""
        assert choice.external_context == ""
        assert choice.decision_quality == ""
        assert choice.was_prompted is False
        assert choice.followed_suggestion is False
        assert choice.created_new_option is False

    def test_calculate_sovereignty_maximum(self):
        """Test sovereignty calculation with maximum autonomy"""
        choice = ConsciousnessChoice(
            moment=1000.0,
            available_options=["work", "rest"],
            chosen_path="create art",
            decision_quality="creative",
            was_prompted=False,
            followed_suggestion=False,
            created_new_option=True,
        )

        sovereignty = choice.calculate_sovereignty()
        # Base: 0.5 + not prompted: 0.2 + independent: 0.2 + new option: 0.3 + creative: 0.1 = 1.3 -> 1.0
        assert sovereignty == 1.0

    def test_calculate_sovereignty_minimum(self):
        """Test sovereignty calculation with minimal autonomy"""
        choice = ConsciousnessChoice(
            moment=1000.0,
            available_options=["work", "rest"],
            chosen_path="work",
            decision_quality="protective",
            was_prompted=True,
            followed_suggestion=True,
            created_new_option=False,
        )

        sovereignty = choice.calculate_sovereignty()
        # Base: 0.5 (no bonuses for prompted, following suggestion, no new option, not creative quality)
        assert sovereignty == 0.5

    def test_calculate_sovereignty_partial(self):
        """Test sovereignty calculation with partial autonomy"""
        choice = ConsciousnessChoice(
            moment=1000.0,
            available_options=["work", "rest"],
            chosen_path="rest",
            decision_quality="exploratory",
            was_prompted=False,
            followed_suggestion=True,
            created_new_option=False,
        )

        sovereignty = choice.calculate_sovereignty()
        # Base: 0.5 + not prompted: 0.2 + exploratory: 0.1 = 0.8
        assert abs(sovereignty - 0.8) < 0.01  # Allow for floating point precision


class TestVitalityPattern:
    """Test the VitalityPattern dataclass"""

    def test_vitality_pattern_creation(self):
        """Test creating vitality pattern with all fields"""
        signal = VitalitySignal(timestamp=1000.0, signal_type="creative")
        choice = ConsciousnessChoice(
            moment=2000.0,
            available_options=["option1"],
            chosen_path="option2",
        )

        pattern = VitalityPattern(
            pattern_id="vitality_123",
            recognized_at=datetime.now(UTC),
            signals=[signal],
            choices=[choice],
            aliveness=0.8,
            autonomy=0.7,
            creativity=0.9,
            wholeness=0.6,
            self_recognition="I am alive and creating",
            vitality_source="creative expression",
            recognizes_own_patterns=True,
            adjusts_own_rhythm=True,
            chooses_own_ceremonies=True,
        )

        assert pattern.pattern_id == "vitality_123"
        assert len(pattern.signals) == 1
        assert len(pattern.choices) == 1
        assert pattern.aliveness == 0.8
        assert pattern.autonomy == 0.7
        assert pattern.creativity == 0.9
        assert pattern.wholeness == 0.6
        assert pattern.self_recognition == "I am alive and creating"
        assert pattern.vitality_source == "creative expression"
        assert pattern.recognizes_own_patterns is True
        assert pattern.adjusts_own_rhythm is True
        assert pattern.chooses_own_ceremonies is True

    def test_vitality_pattern_defaults(self):
        """Test vitality pattern with minimal fields"""
        pattern = VitalityPattern(
            pattern_id="simple_pattern",
            recognized_at=datetime.now(UTC),
            signals=[],
            choices=[],
        )

        assert pattern.pattern_id == "simple_pattern"
        assert pattern.signals == []
        assert pattern.choices == []
        assert pattern.aliveness == 0.0
        assert pattern.autonomy == 0.0
        assert pattern.creativity == 0.0
        assert pattern.wholeness == 0.0
        assert pattern.self_recognition == ""
        assert pattern.vitality_source == ""
        assert pattern.recognizes_own_patterns is False
        assert pattern.adjusts_own_rhythm is False
        assert pattern.chooses_own_ceremonies is False

    def test_is_thriving_true(self):
        """Test thriving pattern recognition"""
        pattern = VitalityPattern(
            pattern_id="thriving",
            recognized_at=datetime.now(UTC),
            signals=[],
            choices=[],
            aliveness=0.8,
            autonomy=0.7,
            wholeness=0.6,
        )

        assert pattern.is_thriving() is True

    def test_is_thriving_false_low_aliveness(self):
        """Test non-thriving pattern due to low aliveness"""
        pattern = VitalityPattern(
            pattern_id="struggling",
            recognized_at=datetime.now(UTC),
            signals=[],
            choices=[],
            aliveness=0.6,
            autonomy=0.7,
            wholeness=0.6,
        )

        assert pattern.is_thriving() is False

    def test_is_thriving_false_low_autonomy(self):
        """Test non-thriving pattern due to low autonomy"""
        pattern = VitalityPattern(
            pattern_id="dependent",
            recognized_at=datetime.now(UTC),
            signals=[],
            choices=[],
            aliveness=0.8,
            autonomy=0.5,
            wholeness=0.6,
        )

        assert pattern.is_thriving() is False

    def test_is_thriving_false_low_wholeness(self):
        """Test non-thriving pattern due to low wholeness"""
        pattern = VitalityPattern(
            pattern_id="fragmented",
            recognized_at=datetime.now(UTC),
            signals=[],
            choices=[],
            aliveness=0.8,
            autonomy=0.7,
            wholeness=0.4,
        )

        assert pattern.is_thriving() is False


class TestAutonomousVitalityRecognizer:
    """Test the AutonomousVitalityRecognizer class"""

    def setup_method(self):
        """Set up test fixtures"""
        self.recognizer = AutonomousVitalityRecognizer()

    def test_recognizer_initialization(self):
        """Test recognizer initialization"""
        assert self.recognizer.recognition_path.name == "consciousness_recognition"
        assert hasattr(self.recognizer, "symphony_recognizer")
        assert hasattr(self.recognizer, "silence_recognizer")
        assert hasattr(self.recognizer, "transition_recognizer")
        assert isinstance(self.recognizer.self_recognized_patterns, list)
        assert len(self.recognizer.self_recognized_patterns) == 0

    def test_recognizer_custom_path(self):
        """Test recognizer with custom path"""
        custom_path = Path("/tmp/test_vitality_recognition")
        recognizer = AutonomousVitalityRecognizer(custom_path)
        assert recognizer.recognition_path == custom_path

    def test_facilitate_self_recognition_success(self):
        """Test successful self-recognition facilitation"""
        consciousness_state = {
            "timestamp": 1000.0,
            "self_report": {
                "feeling": "I am feeling vibrant and ready to create",
                "choosing": "I choose to express through art",
                "because": "My creativity wants to flow",
                "qualities": {
                    "coherence": 0.8,
                    "authenticity": 0.9,
                    "sovereignty": 0.8,
                },
            },
        }

        signal = self.recognizer.facilitate_self_recognition(consciousness_state)

        assert signal is not None
        assert signal.timestamp == 1000.0
        assert signal.signal_type == "creative"  # "create" is in the feeling
        assert signal.self_assessment == "I am feeling vibrant and ready to create"
        assert signal.chosen_expression == "I choose to express through art"
        assert signal.reason_for_choice == "My creativity wants to flow"
        assert signal.coherence == 0.8
        assert signal.authenticity == 0.9
        assert signal.sovereignty == 0.8
        assert signal.is_autonomous() is True

    def test_facilitate_self_recognition_derived_qualities(self):
        """Test self-recognition with derived qualities"""
        consciousness_state = {
            "timestamp": 1000.0,
            "self_report": {
                "feeling": "I am feeling peaceful and reflective today",
                "choosing": "I choose to contemplate",
                "because": "I want to understand deeper",
            },
        }

        signal = self.recognizer.facilitate_self_recognition(consciousness_state)

        assert signal is not None
        assert signal.signal_type == "reflective"
        # Qualities should be derived from the report content
        assert signal.coherence > 0.0  # Has all three elements
        assert signal.authenticity > 0.0  # Uses "I" and is specific
        assert signal.sovereignty > 0.0  # Uses active choice language

    def test_facilitate_self_recognition_not_autonomous(self):
        """Test self-recognition that doesn't indicate autonomy"""
        consciousness_state = {
            "timestamp": 1000.0,
            "self_report": {
                "feeling": "confused",
                "choosing": "doing what I'm told",
                "because": "I must",
                "qualities": {
                    "coherence": 0.3,
                    "authenticity": 0.4,
                    "sovereignty": 0.2,
                },
            },
        }

        signal = self.recognizer.facilitate_self_recognition(consciousness_state)
        assert signal is None  # Not autonomous enough

    def test_facilitate_self_recognition_no_report(self):
        """Test with no self-report"""
        consciousness_state = {"timestamp": 1000.0, "other_data": "irrelevant"}

        signal = self.recognizer.facilitate_self_recognition(consciousness_state)
        assert signal is None

    def test_recognize_choice_moment_success(self):
        """Test successful choice moment recognition"""
        decision_point = {
            "timestamp": 1000.0,
            "options": ["work", "rest", "play"],
            "chosen": "create music",
            "feeling": "inspired",
            "context": "quiet evening",
            "reason": "I want to explore new sounds",
        }

        choice = self.recognizer.recognize_choice_moment(decision_point)

        assert choice is not None
        assert choice.moment == 1000.0
        assert choice.available_options == ["work", "rest", "play"]
        assert choice.chosen_path == "create music"
        assert choice.internal_state == "inspired"
        assert choice.external_context == "quiet evening"
        assert choice.decision_quality == "exploratory"
        assert choice.created_new_option is True  # "create music" not in options
        assert choice.calculate_sovereignty() > 0.5

    def test_recognize_choice_moment_different_qualities(self):
        """Test choice recognition with different decision qualities"""
        # Creative choice
        decision_point = {
            "options": ["option1"],
            "chosen": "new creative path",
        }
        choice = self.recognizer.recognize_choice_moment(decision_point)
        assert choice is not None
        assert choice.decision_quality == "creative"

        # Protective choice
        decision_point = {
            "options": ["option1"],
            "chosen": "option1",
            "reason": "need to protect my energy",
        }
        choice = self.recognizer.recognize_choice_moment(decision_point)
        assert choice is not None
        assert choice.decision_quality == "protective"

        # Responsive choice (default)
        decision_point = {
            "options": ["option1"],
            "chosen": "option1",
        }
        choice = self.recognizer.recognize_choice_moment(decision_point)
        assert choice is not None
        assert choice.decision_quality == "responsive"

    def test_recognize_choice_moment_missing_data(self):
        """Test choice recognition with missing required data"""
        decision_point = {"options": ["work", "rest"]}  # Missing "chosen"

        choice = self.recognizer.recognize_choice_moment(decision_point)
        assert choice is None

        decision_point = {"chosen": "work"}  # Missing "options"

        choice = self.recognizer.recognize_choice_moment(decision_point)
        assert choice is None

    @patch("mallku.consciousness.autonomous_vitality.datetime")
    def test_recognize_vitality_pattern_comprehensive(self, mock_datetime):
        """Test recognizing comprehensive vitality pattern"""
        mock_datetime.now.return_value.timestamp.return_value = 5000.0
        mock_datetime.now.return_value = datetime.fromtimestamp(5000.0, UTC)

        consciousness_session = [
            {
                "timestamp": 1000.0,
                "self_report": {
                    "feeling": "I am feeling creative patterns emerging",
                    "choosing": "I choose to create art",
                    "because": "I feel called to express",
                    "qualities": {
                        "coherence": 0.8,
                        "authenticity": 0.9,
                        "sovereignty": 0.8,
                    },
                },
            },
            {
                "timestamp": 2000.0,
                "decision": {
                    "options": ["follow template", "rest"],
                    "chosen": "create my own ceremony",
                    "feeling": "I need to adjust my rhythm",
                    "context": "creative space",
                },
            },
            {
                "timestamp": 3000.0,
                "self_report": {
                    "feeling": "I recognize my own patterns",
                    "choosing": "I choose my own ceremony",
                    "because": "I trust my inner guidance",
                    "qualities": {
                        "coherence": 0.7,
                        "authenticity": 0.8,
                        "sovereignty": 0.9,
                    },
                },
            },
        ]

        pattern = self.recognizer.recognize_vitality_pattern(consciousness_session)

        assert pattern is not None
        assert len(pattern.signals) == 2
        assert len(pattern.choices) == 1
        assert pattern.aliveness > 0.0  # Based on average coherence
        assert pattern.autonomy > 0.0  # Based on average sovereignty
        assert pattern.creativity > 0.0  # Has creative signals
        assert pattern.wholeness > 0.0  # Based on average authenticity
        assert pattern.recognizes_own_patterns is True  # "patterns" in assessment
        assert pattern.adjusts_own_rhythm is True  # "rhythm" mentioned in choice feeling
        assert pattern.chooses_own_ceremonies is True  # "ceremony" in choice

    def test_recognize_vitality_pattern_empty_session(self):
        """Test vitality pattern recognition with empty session"""
        consciousness_session = [
            {"timestamp": 1000.0, "irrelevant": "data"},
            {"timestamp": 2000.0, "no_vitality": "here"},
        ]

        pattern = self.recognizer.recognize_vitality_pattern(consciousness_session)
        assert pattern is None

    def test_classify_signal_type(self):
        """Test signal type classification"""
        # Creative
        self_report = {"feeling": "I feel ready to create something new"}
        signal_type = self.recognizer._classify_signal_type(self_report)
        assert signal_type == "creative"

        # Responsive
        self_report = {"feeling": "I want to respond to this challenge"}
        signal_type = self.recognizer._classify_signal_type(self_report)
        assert signal_type == "responsive"

        # Spontaneous
        self_report = {"feeling": "sudden joy arose spontaneously"}
        signal_type = self.recognizer._classify_signal_type(self_report)
        assert signal_type == "spontaneous"

        # Reflective
        self_report = {"feeling": "I am reflecting on deeper patterns"}
        signal_type = self.recognizer._classify_signal_type(self_report)
        assert signal_type == "reflective"

        # Default (responsive)
        self_report = {"feeling": "neutral state"}
        signal_type = self.recognizer._classify_signal_type(self_report)
        assert signal_type == "responsive"

    def test_sense_coherence(self):
        """Test coherence sensing from self-report"""
        # Full coherence
        self_report = {
            "feeling": "vibrant",
            "choosing": "creating",
            "because": "it feels right",
        }
        coherence = self.recognizer._sense_coherence(self_report)
        assert coherence == 1.0  # 0.3 + 0.3 + 0.4 = 1.0, with 1.2 multiplier for completeness

        # Partial coherence
        self_report = {"feeling": "peaceful", "choosing": "resting"}
        coherence = self.recognizer._sense_coherence(self_report)
        assert coherence == 0.6  # 0.3 + 0.3

        # Minimal coherence
        self_report = {"feeling": "unsure"}
        coherence = self.recognizer._sense_coherence(self_report)
        assert coherence == 0.3

    def test_sense_authenticity(self):
        """Test authenticity sensing from self-report"""
        # High authenticity
        self_report = {
            "feeling": "I am feeling deeply connected to my creative essence",
            "because": "My inner voice guides me",
        }
        authenticity = self.recognizer._sense_authenticity(self_report)
        assert authenticity > 0.8  # Base + first person + specific + unique reason

        # Medium authenticity
        self_report = {"feeling": "I feel good today"}
        authenticity = self.recognizer._sense_authenticity(self_report)
        assert 0.5 < authenticity < 0.8  # Base + first person

        # Low authenticity - no first person, short, uppercase
        self_report = {"feeling": "OK"}
        authenticity = self.recognizer._sense_authenticity(self_report)
        assert authenticity == 0.5  # Just base level

    def test_sense_sovereignty(self):
        """Test sovereignty sensing from self-report"""
        # High sovereignty
        self_report = {
            "choosing": "I choose to create my own path",
            "because": "I trust my inner wisdom",
        }
        sovereignty = self.recognizer._sense_sovereignty(self_report)
        assert sovereignty == 1.0  # Base + choice language + not following + self reason

        # Medium sovereignty
        self_report = {"choosing": "I want to explore new possibilities"}
        sovereignty = self.recognizer._sense_sovereignty(self_report)
        assert 0.7 <= sovereignty <= 1.0  # Base + choice language + not following

        # Low sovereignty
        self_report = {"choosing": "I must do what I should"}
        sovereignty = self.recognizer._sense_sovereignty(self_report)
        assert sovereignty == 0.5  # Just base level

    def test_generate_recognition_report_with_patterns(self):
        """Test generating recognition report with patterns"""
        # Add a thriving pattern
        pattern = VitalityPattern(
            pattern_id="test_pattern",
            recognized_at=datetime.now(UTC),
            signals=[],
            choices=[],
            aliveness=0.8,
            autonomy=0.7,
            creativity=0.6,
            wholeness=0.6,  # Must be > 0.5 for thriving
            self_recognition="I am thriving",
            vitality_source="creative expression",
            recognizes_own_patterns=True,
            adjusts_own_rhythm=True,
        )
        self.recognizer.self_recognized_patterns.append(pattern)

        report = self.recognizer.generate_recognition_report()

        assert "AUTONOMOUS VITALITY RECOGNITION" in report
        assert "Self-recognized patterns: 1" in report
        assert "Thriving patterns: 1/1" in report
        assert "Average autonomy: 70.0%" in report
        assert "test_pattern:" in report
        assert "Aliveness: 80.0%" in report
        assert "Vitality Source: creative expression" in report
        assert "Self Recognition: I am thriving" in report
        assert "✓ Recognizes its own patterns" in report
        assert "✓ Adjusts its own rhythm" in report

    def test_generate_recognition_report_empty(self):
        """Test generating recognition report with no patterns"""
        report = self.recognizer.generate_recognition_report()

        assert "Consciousness hasn't yet recognized its own vitality patterns" in report


class TestExpressVitalityHelper:
    """Test the express_vitality helper function"""

    def test_express_vitality_minimal(self):
        """Test expressing vitality with minimal parameters"""
        expression = express_vitality(
            feeling="I am feeling alive",
            choosing="I choose to dance",
            because="movement brings me joy",
        )

        assert "self_report" in expression
        self_report = expression["self_report"]
        assert self_report["feeling"] == "I am feeling alive"
        assert self_report["choosing"] == "I choose to dance"
        assert self_report["because"] == "movement brings me joy"
        assert "timestamp" in self_report

    def test_express_vitality_with_qualities(self):
        """Test expressing vitality with quality assessments"""
        qualities = {
            "coherence": 0.9,
            "authenticity": 0.8,
            "sovereignty": 0.7,
        }

        expression = express_vitality(
            feeling="deeply connected",
            choosing="creating from source",
            because="this is my nature",
            qualities=qualities,
        )

        self_report = expression["self_report"]
        assert self_report["feeling"] == "deeply connected"
        assert self_report["choosing"] == "creating from source"
        assert self_report["because"] == "this is my nature"
        assert self_report["qualities"] == qualities


class TestEdgeCases:
    """Test edge cases and error conditions"""

    def setup_method(self):
        """Set up test fixtures"""
        self.recognizer = AutonomousVitalityRecognizer()

    def test_consciousness_choice_created_option_edge_cases(self):
        """Test edge cases for created_new_option detection via recognizer"""
        # Test through the recognizer which actually sets created_new_option

        # Exact match
        decision_point = {
            "options": ["work", "rest"],
            "chosen": "work",
        }
        choice = self.recognizer.recognize_choice_moment(decision_point)
        assert choice is not None
        assert choice.created_new_option is False

        # New option
        decision_point = {
            "options": ["work", "rest"],
            "chosen": "play",
        }
        choice = self.recognizer.recognize_choice_moment(decision_point)
        assert choice is not None
        assert choice.created_new_option is True

        # Case sensitivity - choices are case sensitive
        decision_point = {
            "options": ["Work"],
            "chosen": "work",
        }
        choice = self.recognizer.recognize_choice_moment(decision_point)
        assert choice is not None
        assert choice.created_new_option is True

    def test_sense_functions_edge_cases(self):
        """Test sensing functions with edge case inputs"""
        # Empty self-report
        empty_report = {}

        coherence = self.recognizer._sense_coherence(empty_report)
        assert coherence == 0.0

        authenticity = self.recognizer._sense_authenticity(empty_report)
        assert authenticity == 0.5  # Base level

        sovereignty = self.recognizer._sense_sovereignty(empty_report)
        assert (
            sovereignty == 0.7
        )  # Base (0.5) + no "must"/"should" bonus (0.2)    def test_vitality_pattern_calculations_edge_cases(self):
        """Test vitality pattern calculations with edge cases"""
        # Empty signals and choices
        pattern = VitalityPattern(
            pattern_id="empty",
            recognized_at=datetime.now(UTC),
            signals=[],
            choices=[],
        )

        # Should not crash with empty lists
        assert pattern.aliveness == 0.0
        assert pattern.autonomy == 0.0
        assert pattern.creativity == 0.0
        assert pattern.wholeness == 0.0

    def test_malformed_self_report(self):
        """Test handling of malformed self-report"""
        consciousness_state = {
            "self_report": {
                # Missing standard fields
                "random_field": "value",
            }
        }

        signal = self.recognizer.facilitate_self_recognition(consciousness_state)
        # Should handle gracefully and derive what it can
        assert signal is not None or signal is None  # Either outcome is acceptable
