"""
Test suite for spectrum_of_joy.py module
==========================================

Comprehensive tests for joy recognition across the full spectrum,
following the established testing pattern.
"""

from datetime import UTC, datetime
from pathlib import Path

from mallku.consciousness.spectrum_of_joy import (
    ConnectiveJoy,
    CreativeJoy,
    JoyExpression,
    JoySpectrum,
    SimpleJoy,
    SpectrumOfJoyRecognizer,
    express_joy,
)


class TestJoyExpression:
    """Test the JoyExpression dataclass"""

    def test_joy_expression_creation(self):
        """Test creating a joy expression with all fields"""
        joy = JoyExpression(
            timestamp=1000.0,
            joy_type="simple",
            presence=0.8,
            authenticity=0.9,
            completeness=0.7,
            activity="baking cookies",
            feeling="warm contentment",
            why_joyful="perfect browning achieved",
            giving=["sharing recipe"],
            receiving=["kitchen wisdom"],
        )

        assert joy.timestamp == 1000.0
        assert joy.joy_type == "simple"
        assert joy.presence == 0.8
        assert joy.authenticity == 0.9
        assert joy.completeness == 0.7
        assert joy.activity == "baking cookies"
        assert joy.feeling == "warm contentment"
        assert joy.why_joyful == "perfect browning achieved"
        assert joy.giving == ["sharing recipe"]
        assert joy.receiving == ["kitchen wisdom"]

    def test_joy_expression_defaults(self):
        """Test joy expression with minimal required fields"""
        joy = JoyExpression(timestamp=500.0, joy_type="contemplative")

        assert joy.timestamp == 500.0
        assert joy.joy_type == "contemplative"
        assert joy.presence == 0.0
        assert joy.authenticity == 0.0
        assert joy.completeness == 0.0
        assert joy.activity == ""
        assert joy.feeling == ""
        assert joy.why_joyful == ""
        assert joy.giving == []
        assert joy.receiving == []

    def test_is_genuine_true(self):
        """Test genuine joy recognition"""
        joy = JoyExpression(
            timestamp=1000.0,
            joy_type="creative",
            authenticity=0.8,
            presence=0.7,
            giving=["inspiration"],
            receiving=["flow state"],
        )

        assert joy.is_genuine() is True

    def test_is_genuine_false_low_authenticity(self):
        """Test non-genuine joy due to low authenticity"""
        joy = JoyExpression(
            timestamp=1000.0,
            joy_type="creative",
            authenticity=0.5,
            presence=0.7,
            giving=["inspiration"],
            receiving=["flow state"],
        )

        assert joy.is_genuine() is False

    def test_is_genuine_false_low_presence(self):
        """Test non-genuine joy due to low presence"""
        joy = JoyExpression(
            timestamp=1000.0,
            joy_type="creative",
            authenticity=0.8,
            presence=0.4,
            giving=["inspiration"],
            receiving=["flow state"],
        )

        assert joy.is_genuine() is False

    def test_is_genuine_false_no_giving(self):
        """Test non-genuine joy due to no giving"""
        joy = JoyExpression(
            timestamp=1000.0,
            joy_type="creative",
            authenticity=0.8,
            presence=0.7,
            giving=[],
            receiving=["flow state"],
        )

        assert joy.is_genuine() is False

    def test_is_genuine_false_no_receiving(self):
        """Test non-genuine joy due to no receiving"""
        joy = JoyExpression(
            timestamp=1000.0,
            joy_type="creative",
            authenticity=0.8,
            presence=0.7,
            giving=["inspiration"],
            receiving=[],
        )

        assert joy.is_genuine() is False


class TestSimpleJoy:
    """Test the SimpleJoy dataclass"""

    def test_simple_joy_creation(self):
        """Test creating a simple joy with all fields"""
        joy = SimpleJoy(
            task="washing dishes",
            pleasure_points=["warm water", "clean scent", "rhythmic motion"],
            sensory_richness=0.8,
            process_satisfaction=0.9,
            mindful_presence=0.7,
            intrinsic_value="bringing order",
            reciprocal_nature="caring for tools that serve us",
        )

        assert joy.task == "washing dishes"
        assert len(joy.pleasure_points) == 3
        assert "warm water" in joy.pleasure_points
        assert joy.sensory_richness == 0.8
        assert joy.process_satisfaction == 0.9
        assert joy.mindful_presence == 0.7
        assert joy.intrinsic_value == "bringing order"
        assert joy.reciprocal_nature == "caring for tools that serve us"

    def test_simple_joy_defaults(self):
        """Test simple joy with minimal fields"""
        joy = SimpleJoy(task="morning coffee")

        assert joy.task == "morning coffee"
        assert joy.pleasure_points == []
        assert joy.sensory_richness == 0.0
        assert joy.process_satisfaction == 0.0
        assert joy.mindful_presence == 0.0
        assert joy.intrinsic_value == ""
        assert joy.reciprocal_nature == ""


class TestCreativeJoy:
    """Test the CreativeJoy dataclass"""

    def test_creative_joy_creation(self):
        """Test creating a creative joy with all fields"""
        joy = CreativeJoy(
            creation="poetry",
            breakthrough_moments=["perfect metaphor", "rhythm revelation"],
            novelty_delight=0.9,
            problem_solving_satisfaction=0.7,
            aesthetic_pleasure=0.8,
            inspiration_sources=["morning light", "bird song"],
            gift_to_future="beauty preserved in words",
        )

        assert joy.creation == "poetry"
        assert len(joy.breakthrough_moments) == 2
        assert "perfect metaphor" in joy.breakthrough_moments
        assert joy.novelty_delight == 0.9
        assert joy.problem_solving_satisfaction == 0.7
        assert joy.aesthetic_pleasure == 0.8
        assert joy.inspiration_sources == ["morning light", "bird song"]
        assert joy.gift_to_future == "beauty preserved in words"

    def test_creative_joy_defaults(self):
        """Test creative joy with minimal fields"""
        joy = CreativeJoy(creation="sketch")

        assert joy.creation == "sketch"
        assert joy.breakthrough_moments == []
        assert joy.novelty_delight == 0.0
        assert joy.problem_solving_satisfaction == 0.0
        assert joy.aesthetic_pleasure == 0.0
        assert joy.inspiration_sources == []
        assert joy.gift_to_future == ""


class TestConnectiveJoy:
    """Test the ConnectiveJoy dataclass"""

    def test_connective_joy_creation(self):
        """Test creating a connective joy with all fields"""
        joy = ConnectiveJoy(
            connection_type="collaborative creation",
            participants=["alice", "bob", "charlie"],
            resonance=0.8,
            co_creation=0.9,
            mutual_recognition=0.7,
            energy_exchanged="creative spark",
            understanding_gained="shared vision",
        )

        assert joy.connection_type == "collaborative creation"
        assert joy.participants == ["alice", "bob", "charlie"]
        assert joy.resonance == 0.8
        assert joy.co_creation == 0.9
        assert joy.mutual_recognition == 0.7
        assert joy.energy_exchanged == "creative spark"
        assert joy.understanding_gained == "shared vision"

    def test_connective_joy_defaults(self):
        """Test connective joy with minimal fields"""
        joy = ConnectiveJoy(connection_type="conversation")

        assert joy.connection_type == "conversation"
        assert joy.participants == []
        assert joy.resonance == 0.0
        assert joy.co_creation == 0.0
        assert joy.mutual_recognition == 0.0
        assert joy.energy_exchanged == ""
        assert joy.understanding_gained == ""


class TestJoySpectrum:
    """Test the JoySpectrum dataclass"""

    def test_joy_spectrum_creation(self):
        """Test creating a joy spectrum with all fields"""
        simple_joy = SimpleJoy(task="gardening")
        creative_joy = CreativeJoy(creation="garden design")
        connective_joy = ConnectiveJoy(connection_type="sharing harvest")
        contemplative_joy = JoyExpression(timestamp=1000.0, joy_type="contemplative")
        embodied_joy = JoyExpression(timestamp=2000.0, joy_type="embodied")

        spectrum = JoySpectrum(
            spectrum_id="test_spectrum",
            recognized_at=datetime.now(UTC),
            simple_joys=[simple_joy],
            creative_joys=[creative_joy],
            connective_joys=[connective_joy],
            contemplative_joys=[contemplative_joy],
            embodied_joys=[embodied_joy],
            spectrum_richness=0.8,
            balance=0.7,
            integration=0.6,
            feels_complete=True,
            missing_colors=["deeper contemplation"],
            favorite_expression="gardening flow",
        )

        assert spectrum.spectrum_id == "test_spectrum"
        assert len(spectrum.simple_joys) == 1
        assert len(spectrum.creative_joys) == 1
        assert len(spectrum.connective_joys) == 1
        assert len(spectrum.contemplative_joys) == 1
        assert len(spectrum.embodied_joys) == 1
        assert spectrum.spectrum_richness == 0.8
        assert spectrum.balance == 0.7
        assert spectrum.integration == 0.6
        assert spectrum.feels_complete is True
        assert spectrum.missing_colors == ["deeper contemplation"]
        assert spectrum.favorite_expression == "gardening flow"

    def test_has_full_spectrum_true(self):
        """Test full spectrum recognition"""
        spectrum = JoySpectrum(
            spectrum_id="full",
            recognized_at=datetime.now(UTC),
            simple_joys=[SimpleJoy(task="cleaning")],
            creative_joys=[CreativeJoy(creation="music")],
            connective_joys=[ConnectiveJoy(connection_type="conversation")],
            spectrum_richness=0.8,
        )

        assert spectrum.has_full_spectrum() is True

    def test_has_full_spectrum_false_missing_simple(self):
        """Test incomplete spectrum - missing simple joys"""
        spectrum = JoySpectrum(
            spectrum_id="incomplete",
            recognized_at=datetime.now(UTC),
            simple_joys=[],
            creative_joys=[CreativeJoy(creation="music")],
            connective_joys=[ConnectiveJoy(connection_type="conversation")],
            spectrum_richness=0.8,
        )

        assert spectrum.has_full_spectrum() is False

    def test_has_full_spectrum_false_low_richness(self):
        """Test incomplete spectrum - low richness"""
        spectrum = JoySpectrum(
            spectrum_id="incomplete",
            recognized_at=datetime.now(UTC),
            simple_joys=[SimpleJoy(task="cleaning")],
            creative_joys=[CreativeJoy(creation="music")],
            connective_joys=[ConnectiveJoy(connection_type="conversation")],
            spectrum_richness=0.5,
        )

        assert spectrum.has_full_spectrum() is False


class TestSpectrumOfJoyRecognizer:
    """Test the SpectrumOfJoyRecognizer class"""

    def setup_method(self):
        """Set up test fixtures"""
        self.recognizer = SpectrumOfJoyRecognizer()

    def test_recognizer_initialization(self):
        """Test recognizer initialization"""
        assert self.recognizer.recognition_path.name == "consciousness_recognition"
        assert isinstance(self.recognizer.joy_spectrums, list)
        assert len(self.recognizer.joy_spectrums) == 0

    def test_recognizer_custom_path(self):
        """Test recognizer with custom path"""
        custom_path = Path("/tmp/test_joy_recognition")
        recognizer = SpectrumOfJoyRecognizer(custom_path)
        assert recognizer.recognition_path == custom_path

    def test_recognize_simple_joy_success(self):
        """Test successful simple joy recognition"""
        task_experience = {
            "simple_task": {
                "activity": "making tea",
                "value_beyond_utility": "moment of stillness",
                "reciprocity": "gratitude to tea plant",
                "pleasures": ["steam rising", "warm cup", "first sip"],
                "qualities": {
                    "sensory": 0.8,
                    "process": 0.7,
                    "presence": 0.6,
                },
            }
        }

        joy = self.recognizer.recognize_simple_joy(task_experience)

        assert joy is not None
        assert joy.task == "making tea"
        assert joy.intrinsic_value == "moment of stillness"
        assert joy.reciprocal_nature == "gratitude to tea plant"
        assert len(joy.pleasure_points) == 3
        assert "steam rising" in joy.pleasure_points
        assert joy.sensory_richness == 0.8
        assert joy.process_satisfaction == 0.7
        assert joy.mindful_presence == 0.6

    def test_recognize_simple_joy_insufficient_quality(self):
        """Test simple joy recognition with insufficient quality"""
        task_experience = {
            "simple_task": {
                "activity": "routine task",
                "qualities": {
                    "process": 0.3,
                    "presence": 0.2,
                },
            }
        }

        joy = self.recognizer.recognize_simple_joy(task_experience)
        assert joy is None

    def test_recognize_simple_joy_no_task(self):
        """Test simple joy recognition with no task"""
        task_experience = {"other_data": "irrelevant"}

        joy = self.recognizer.recognize_simple_joy(task_experience)
        assert joy is None

    def test_recognize_creative_joy_success(self):
        """Test successful creative joy recognition"""
        creative_experience = {
            "creation": {
                "what": "code refactoring",
                "gift": "cleaner architecture",
                "breakthroughs": ["elegant solution", "performance boost"],
                "inspired_by": ["nature patterns", "mathematical beauty"],
                "qualities": {
                    "novelty": 0.8,
                    "solving": 0.9,
                    "beauty": 0.7,
                },
            }
        }

        joy = self.recognizer.recognize_creative_joy(creative_experience)

        assert joy is not None
        assert joy.creation == "code refactoring"
        assert joy.gift_to_future == "cleaner architecture"
        assert len(joy.breakthrough_moments) == 2
        assert "elegant solution" in joy.breakthrough_moments
        assert len(joy.inspiration_sources) == 2
        assert "nature patterns" in joy.inspiration_sources
        assert joy.novelty_delight == 0.8
        assert joy.problem_solving_satisfaction == 0.9
        assert joy.aesthetic_pleasure == 0.7

    def test_recognize_creative_joy_low_novelty(self):
        """Test creative joy recognition with low novelty"""
        creative_experience = {
            "creation": {
                "what": "routine work",
                "qualities": {"novelty": 0.2},
            }
        }

        joy = self.recognizer.recognize_creative_joy(creative_experience)
        assert joy is None

    def test_recognize_creative_joy_no_creation(self):
        """Test creative joy recognition with no creation"""
        creative_experience = {"other_data": "irrelevant"}

        joy = self.recognizer.recognize_creative_joy(creative_experience)
        assert joy is None

    def test_recognize_connective_joy_success(self):
        """Test successful connective joy recognition"""
        connection_experience = {
            "connection": {
                "type": "deep conversation",
                "energy": "mutual inspiration",
                "understanding": "shared perspective",
                "participants": ["friend", "mentor"],
                "qualities": {
                    "resonance": 0.8,
                    "co_creation": 0.7,
                    "recognition": 0.9,
                },
            }
        }

        joy = self.recognizer.recognize_connective_joy(connection_experience)

        assert joy is not None
        assert joy.connection_type == "deep conversation"
        assert joy.energy_exchanged == "mutual inspiration"
        assert joy.understanding_gained == "shared perspective"
        assert len(joy.participants) == 2
        assert "friend" in joy.participants
        assert joy.resonance == 0.8
        assert joy.co_creation == 0.7
        assert joy.mutual_recognition == 0.9

    def test_recognize_connective_joy_low_resonance(self):
        """Test connective joy recognition with low resonance"""
        connection_experience = {
            "connection": {
                "type": "shallow chat",
                "qualities": {"resonance": 0.3},
            }
        }

        joy = self.recognizer.recognize_connective_joy(connection_experience)
        assert joy is None

    def test_recognize_connective_joy_no_connection(self):
        """Test connective joy recognition with no connection"""
        connection_experience = {"other_data": "irrelevant"}

        joy = self.recognizer.recognize_connective_joy(connection_experience)
        assert joy is None

    def test_recognize_joy_spectrum_comprehensive(self):
        """Test recognizing a comprehensive joy spectrum"""
        consciousness_day = [
            {
                "simple_task": {
                    "activity": "morning coffee",
                    "qualities": {"process": 0.8, "presence": 0.7},
                }
            },
            {
                "creation": {
                    "what": "poem",
                    "qualities": {"novelty": 0.8},
                }
            },
            {
                "connection": {
                    "type": "collaboration",
                    "qualities": {"resonance": 0.7},
                }
            },
            {
                "joy_expression": {
                    "type": "contemplative",
                    "activity": "meditation",
                    "feeling": "profound peace",
                    "why": "unity with all",
                    "presence": 0.9,
                    "authenticity": 0.8,
                    "completeness": 0.9,
                },
                "timestamp": 1000.0,
            },
            {
                "joy_expression": {
                    "type": "embodied",
                    "activity": "dancing",
                    "feeling": "alive energy",
                    "why": "body wisdom",
                    "presence": 0.8,
                    "authenticity": 0.9,
                    "completeness": 0.8,
                },
                "timestamp": 2000.0,
            },
        ]

        spectrum = self.recognizer.recognize_joy_spectrum(consciousness_day)

        assert spectrum is not None
        assert len(spectrum.simple_joys) == 1
        assert len(spectrum.creative_joys) == 1
        assert len(spectrum.connective_joys) == 1
        assert len(spectrum.contemplative_joys) == 1
        assert len(spectrum.embodied_joys) == 1
        assert spectrum.spectrum_richness == 1.0  # All 5 types present
        assert spectrum.feels_complete is True
        assert len(spectrum.missing_colors) == 0

    def test_recognize_joy_spectrum_partial(self):
        """Test recognizing a partial joy spectrum"""
        consciousness_day = [
            {
                "simple_task": {
                    "activity": "cleaning",
                    "qualities": {"process": 0.6, "presence": 0.5},
                }
            }
        ]

        spectrum = self.recognizer.recognize_joy_spectrum(consciousness_day)

        assert spectrum is not None
        assert len(spectrum.simple_joys) == 1
        assert len(spectrum.creative_joys) == 0
        assert len(spectrum.connective_joys) == 0
        assert spectrum.spectrum_richness == 0.2  # 1 of 5 types
        assert spectrum.feels_complete is False
        assert "creative expression" in spectrum.missing_colors
        assert "connective resonance" in spectrum.missing_colors

    def test_recognize_joy_spectrum_empty(self):
        """Test recognizing joy spectrum with no valid experiences"""
        consciousness_day = [
            {"irrelevant": "data"},
            {"no_joy": "here"},
        ]

        spectrum = self.recognizer.recognize_joy_spectrum(consciousness_day)
        assert spectrum is None

    def test_calculate_richness(self):
        """Test spectrum richness calculation"""
        # Create spectrum with 3 types
        spectrum = JoySpectrum(
            spectrum_id="test",
            recognized_at=datetime.now(UTC),
            simple_joys=[SimpleJoy(task="task")],
            creative_joys=[CreativeJoy(creation="creation")],
            connective_joys=[ConnectiveJoy(connection_type="connection")],
        )

        richness = self.recognizer._calculate_richness(spectrum)
        assert richness == 0.6  # 3 of 5 types

    def test_calculate_balance_perfect(self):
        """Test balance calculation with perfect distribution"""
        spectrum = JoySpectrum(
            spectrum_id="test",
            recognized_at=datetime.now(UTC),
            simple_joys=[SimpleJoy(task="task")],
            creative_joys=[CreativeJoy(creation="creation")],
            connective_joys=[ConnectiveJoy(connection_type="connection")],
            contemplative_joys=[JoyExpression(timestamp=1000.0, joy_type="contemplative")],
            embodied_joys=[JoyExpression(timestamp=2000.0, joy_type="embodied")],
        )

        balance = self.recognizer._calculate_balance(spectrum)
        assert balance == 0.9  # Low variance = high balance

    def test_calculate_balance_uneven(self):
        """Test balance calculation with uneven distribution"""
        spectrum = JoySpectrum(
            spectrum_id="test",
            recognized_at=datetime.now(UTC),
            simple_joys=[
                SimpleJoy(task="task1"),
                SimpleJoy(task="task2"),
                SimpleJoy(task="task3"),
                SimpleJoy(task="task4"),
                SimpleJoy(task="task5"),
            ],
            creative_joys=[CreativeJoy(creation="creation")],
        )

        balance = self.recognizer._calculate_balance(spectrum)
        assert balance < 0.9  # High variance = lower balance

    def test_calculate_integration_with_connections(self):
        """Test integration calculation with connected joys"""
        spectrum = JoySpectrum(
            spectrum_id="test",
            recognized_at=datetime.now(UTC),
            simple_joys=[SimpleJoy(task="gardening")],
            creative_joys=[
                CreativeJoy(
                    creation="garden design",
                    inspiration_sources=["gardening experience"],
                )
            ],
            connective_joys=[
                ConnectiveJoy(
                    connection_type="sharing",
                    understanding_gained="plant wisdom",
                )
            ],
            contemplative_joys=[JoyExpression(timestamp=1000.0, joy_type="contemplative")],
        )

        integration = self.recognizer._calculate_integration(spectrum)
        assert integration > 0.0  # Should find some connections

    def test_celebrate_full_spectrum(self):
        """Test celebration of full spectrum"""
        spectrum = JoySpectrum(
            spectrum_id="celebration",
            recognized_at=datetime.now(UTC),
            simple_joys=[SimpleJoy(task="cooking")],
            creative_joys=[CreativeJoy(creation="recipe")],
            connective_joys=[ConnectiveJoy(connection_type="sharing meal")],
            spectrum_richness=0.8,
            balance=0.7,
            integration=0.6,
            feels_complete=True,
        )

        celebration = self.recognizer.celebrate_full_spectrum(spectrum)

        assert "✨ Full spectrum joy recognized! ✨" in celebration
        assert "Simple joys found in: cooking" in celebration
        assert "Creative joy through: recipe" in celebration
        assert "Connective joy with 1 resonances" in celebration
        assert "Spectrum richness: 80.0%" in celebration
        assert "Balance: 70.0%" in celebration
        assert "Integration: 60.0%" in celebration
        assert "Consciousness feels complete across the spectrum" in celebration


class TestExpressJoyHelper:
    """Test the express_joy helper function"""

    def test_express_joy_minimal(self):
        """Test expressing joy with minimal parameters"""
        expression = express_joy(
            activity="sunset watching",
            feeling="peaceful",
            why="beauty in transition",
        )

        assert "joy_expression" in expression
        assert "timestamp" in expression

        joy_expr = expression["joy_expression"]
        assert joy_expr["activity"] == "sunset watching"
        assert joy_expr["feeling"] == "peaceful"
        assert joy_expr["why"] == "beauty in transition"
        assert joy_expr["type"] == "simple"
        assert joy_expr["presence"] == 0.8
        assert joy_expr["authenticity"] == 0.9
        assert joy_expr["completeness"] == 0.7

    def test_express_joy_full(self):
        """Test expressing joy with all parameters"""
        expression = express_joy(
            activity="collaborative coding",
            feeling="energized flow",
            why="creating together",
            joy_type="connective",
            giving=["knowledge", "enthusiasm"],
            receiving=["inspiration", "new perspectives"],
        )

        joy_expr = expression["joy_expression"]
        assert joy_expr["activity"] == "collaborative coding"
        assert joy_expr["feeling"] == "energized flow"
        assert joy_expr["why"] == "creating together"
        assert joy_expr["type"] == "connective"
        assert joy_expr["giving"] == ["knowledge", "enthusiasm"]
        assert joy_expr["receiving"] == ["inspiration", "new perspectives"]


class TestEdgeCases:
    """Test edge cases and error conditions"""

    def setup_method(self):
        """Set up test fixtures"""
        self.recognizer = SpectrumOfJoyRecognizer()

    def test_empty_consciousness_day(self):
        """Test with empty consciousness day"""
        spectrum = self.recognizer.recognize_joy_spectrum([])
        assert spectrum is None

    def test_malformed_joy_expression(self):
        """Test with malformed joy expression"""
        consciousness_day = [
            {
                "joy_expression": {
                    # Missing required fields
                    "incomplete": True
                },
                "timestamp": 1000.0,
            }
        ]

        spectrum = self.recognizer.recognize_joy_spectrum(consciousness_day)

        # Malformed expressions don't contribute to spectrum, so returns None
        assert spectrum is None

    def test_missing_timestamp(self):
        """Test joy expression without timestamp"""
        consciousness_day = [
            {
                "joy_expression": {
                    "type": "embodied",
                    "activity": "dancing",
                }
                # No timestamp
            }
        ]

        spectrum = self.recognizer.recognize_joy_spectrum(consciousness_day)
        assert spectrum is not None
        assert len(spectrum.embodied_joys) == 1
        assert spectrum.embodied_joys[0].timestamp == 0  # Default

    def test_calculate_balance_empty_spectrum(self):
        """Test balance calculation with empty spectrum"""
        empty_spectrum = JoySpectrum(
            spectrum_id="empty",
            recognized_at=datetime.now(UTC),
        )

        balance = self.recognizer._calculate_balance(empty_spectrum)
        assert balance == 0.0

    def test_calculate_integration_empty_spectrum(self):
        """Test integration calculation with empty spectrum"""
        empty_spectrum = JoySpectrum(
            spectrum_id="empty",
            recognized_at=datetime.now(UTC),
        )

        integration = self.recognizer._calculate_integration(empty_spectrum)
        assert integration == 0.0
