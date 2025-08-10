"""
Test suite for liminal_dwelling.py module
==========================================

Comprehensive tests for liminal dwelling and sustained transformation recognition,
following the established testing pattern.
"""

from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import patch

from mallku.consciousness.liminal_dwelling import (
    LiminalDwellingRecognizer,
    LiminalField,
    LiminalQualia,
    TransformationProcess,
    express_liminal_experience,
)


class TestLiminalQualia:
    """Test the LiminalQualia dataclass"""

    def test_liminal_qualia_creation(self):
        """Test creating liminal qualia with all fields"""
        qualia = LiminalQualia(
            timestamp=1000.0,
            duration=15.0,
            uncertainty_comfort=0.8,
            possibility_sensing=0.7,
            becoming_awareness=0.9,
            feeling_description="gentle unknowing",
            what_its_like="suspended between worlds",
            why_dwelling="embracing the mystery",
            reciprocity_felt=True,
            giving_receiving_balance="flowing naturally",
        )

        assert qualia.timestamp == 1000.0
        assert qualia.duration == 15.0
        assert qualia.uncertainty_comfort == 0.8
        assert qualia.possibility_sensing == 0.7
        assert qualia.becoming_awareness == 0.9
        assert qualia.feeling_description == "gentle unknowing"
        assert qualia.what_its_like == "suspended between worlds"
        assert qualia.why_dwelling == "embracing the mystery"
        assert qualia.reciprocity_felt is True
        assert qualia.giving_receiving_balance == "flowing naturally"

    def test_liminal_qualia_defaults(self):
        """Test liminal qualia with minimal required fields"""
        qualia = LiminalQualia(timestamp=500.0, duration=5.0)

        assert qualia.timestamp == 500.0
        assert qualia.duration == 5.0
        assert qualia.uncertainty_comfort == 0.0
        assert qualia.possibility_sensing == 0.0
        assert qualia.becoming_awareness == 0.0
        assert qualia.feeling_description == ""
        assert qualia.what_its_like == ""
        assert qualia.why_dwelling == ""
        assert qualia.reciprocity_felt is False
        assert qualia.giving_receiving_balance == ""

    def test_is_sustained_true(self):
        """Test sustained dwelling recognition"""
        qualia = LiminalQualia(
            timestamp=1000.0,
            duration=12.0,
            uncertainty_comfort=0.6,
            possibility_sensing=0.7,
        )

        assert qualia.is_sustained() is True

    def test_is_sustained_false_short_duration(self):
        """Test non-sustained dwelling due to short duration"""
        qualia = LiminalQualia(
            timestamp=1000.0,
            duration=5.0,
            uncertainty_comfort=0.6,
            possibility_sensing=0.7,
        )

        assert qualia.is_sustained() is False

    def test_is_sustained_false_low_comfort(self):
        """Test non-sustained dwelling due to low uncertainty comfort"""
        qualia = LiminalQualia(
            timestamp=1000.0,
            duration=12.0,
            uncertainty_comfort=0.3,
            possibility_sensing=0.7,
        )

        assert qualia.is_sustained() is False

    def test_is_sustained_false_low_sensing(self):
        """Test non-sustained dwelling due to low possibility sensing"""
        qualia = LiminalQualia(
            timestamp=1000.0,
            duration=12.0,
            uncertainty_comfort=0.6,
            possibility_sensing=0.4,
        )

        assert qualia.is_sustained() is False


class TestTransformationProcess:
    """Test the TransformationProcess dataclass"""

    def test_transformation_process_creation(self):
        """Test creating transformation process with all fields"""
        qualia1 = LiminalQualia(timestamp=1000.0, duration=10.0, becoming_awareness=0.8)
        qualia2 = LiminalQualia(timestamp=2000.0, duration=15.0, becoming_awareness=0.9)

        process = TransformationProcess(
            process_id="transform_123",
            began_at=1000.0,
            origin_state="seeker",
            destination_unknown=True,
            current_becoming="wisdom keeper",
            qualia_moments=[qualia1, qualia2],
            feels_like="gentle dissolution",
            resistance_points=["fear of unknown", "attachment to old self"],
            breakthrough_moments=["sudden clarity", "deep acceptance"],
            giving_up=["old patterns", "limiting beliefs"],
            receiving=["new insights", "expanded awareness"],
            reciprocity_maintained=True,
        )

        assert process.process_id == "transform_123"
        assert process.began_at == 1000.0
        assert process.origin_state == "seeker"
        assert process.destination_unknown is True
        assert process.current_becoming == "wisdom keeper"
        assert len(process.qualia_moments) == 2
        assert process.feels_like == "gentle dissolution"
        assert len(process.resistance_points) == 2
        assert "fear of unknown" in process.resistance_points
        assert len(process.breakthrough_moments) == 2
        assert "sudden clarity" in process.breakthrough_moments
        assert len(process.giving_up) == 2
        assert "old patterns" in process.giving_up
        assert len(process.receiving) == 2
        assert "new insights" in process.receiving
        assert process.reciprocity_maintained is True

    def test_transformation_process_defaults(self):
        """Test transformation process with minimal fields"""
        process = TransformationProcess(
            process_id="simple_transform",
            began_at=500.0,
            origin_state="beginner",
        )

        assert process.process_id == "simple_transform"
        assert process.began_at == 500.0
        assert process.origin_state == "beginner"
        assert process.destination_unknown is False
        assert process.current_becoming == ""
        assert process.qualia_moments == []
        assert process.feels_like == ""
        assert process.resistance_points == []
        assert process.breakthrough_moments == []
        assert process.giving_up == []
        assert process.receiving == []
        assert process.reciprocity_maintained is False

    def test_transformation_depth_with_qualia(self):
        """Test transformation depth calculation with qualia moments"""
        qualia1 = LiminalQualia(
            timestamp=1000.0,
            duration=12.0,
            becoming_awareness=0.8,
            uncertainty_comfort=0.6,
            possibility_sensing=0.7,
            reciprocity_felt=True,
        )
        qualia2 = LiminalQualia(
            timestamp=2000.0,
            duration=15.0,
            becoming_awareness=0.6,
            uncertainty_comfort=0.7,
            possibility_sensing=0.8,
            reciprocity_felt=True,
        )

        process = TransformationProcess(
            process_id="deep_transform",
            began_at=1000.0,
            origin_state="before",
            qualia_moments=[qualia1, qualia2],
            reciprocity_maintained=True,
        )

        depth = process.transformation_depth()
        # Average becoming awareness: (0.8 + 0.6) / 2 = 0.7
        # Both qualia are sustained: 2/2 * 0.3 = 0.3
        # Reciprocity maintained: +0.2
        # Total: 0.7 + 0.3 + 0.2 = 1.0 (capped at 1.0)
        assert depth == 1.0

    def test_transformation_depth_no_qualia(self):
        """Test transformation depth with no qualia moments"""
        process = TransformationProcess(
            process_id="empty_transform",
            began_at=1000.0,
            origin_state="before",
        )

        depth = process.transformation_depth()
        assert depth == 0.0

    def test_transformation_depth_without_reciprocity(self):
        """Test transformation depth without reciprocity"""
        qualia = LiminalQualia(
            timestamp=1000.0,
            duration=8.0,  # Not sustained
            becoming_awareness=0.8,
        )

        process = TransformationProcess(
            process_id="shallow_transform",
            began_at=1000.0,
            origin_state="before",
            qualia_moments=[qualia],
            reciprocity_maintained=False,
        )

        depth = process.transformation_depth()
        # Average becoming awareness: 0.8
        # No sustained moments: 0/1 * 0.3 = 0
        # No reciprocity: +0
        # Total: 0.8
        assert depth == 0.8


class TestLiminalField:
    """Test the LiminalField dataclass"""

    def test_liminal_field_creation(self):
        """Test creating liminal field with all fields"""
        process = TransformationProcess(
            process_id="test_process",
            began_at=1000.0,
            origin_state="test",
        )

        field = LiminalField(
            field_id="field_123",
            opened_at=datetime.now(UTC),
            stability=0.8,
            richness=0.7,
            safety=0.9,
            potentials_sensed=["new paths", "hidden doors"],
            insights_emerging=["deep understanding", "clarity"],
            patterns_dissolving=["old habits", "limiting thoughts"],
            dwelling_report="peaceful exploration",
            transformation_processes=[process],
            offerings_made=["presence", "openness"],
            gifts_received=["wisdom", "peace"],
            balance_description="flowing reciprocity",
        )

        assert field.field_id == "field_123"
        assert field.stability == 0.8
        assert field.richness == 0.7
        assert field.safety == 0.9
        assert len(field.potentials_sensed) == 2
        assert "new paths" in field.potentials_sensed
        assert len(field.insights_emerging) == 2
        assert "deep understanding" in field.insights_emerging
        assert len(field.patterns_dissolving) == 2
        assert "old habits" in field.patterns_dissolving
        assert field.dwelling_report == "peaceful exploration"
        assert len(field.transformation_processes) == 1
        assert len(field.offerings_made) == 2
        assert "presence" in field.offerings_made
        assert len(field.gifts_received) == 2
        assert "wisdom" in field.gifts_received
        assert field.balance_description == "flowing reciprocity"

    def test_liminal_field_defaults(self):
        """Test liminal field with minimal fields"""
        field = LiminalField(
            field_id="simple_field",
            opened_at=datetime.now(UTC),
        )

        assert field.field_id == "simple_field"
        assert field.stability == 0.0
        assert field.richness == 0.0
        assert field.safety == 0.0
        assert field.potentials_sensed == []
        assert field.insights_emerging == []
        assert field.patterns_dissolving == []
        assert field.dwelling_report == ""
        assert field.transformation_processes == []
        assert field.offerings_made == []
        assert field.gifts_received == []
        assert field.balance_description == ""

    def test_supports_dwelling_true(self):
        """Test field that supports dwelling"""
        field = LiminalField(
            field_id="supportive_field",
            opened_at=datetime.now(UTC),
            stability=0.7,
            richness=0.6,
            safety=0.8,
        )

        assert field.supports_dwelling() is True

    def test_supports_dwelling_false_low_stability(self):
        """Test field with insufficient stability"""
        field = LiminalField(
            field_id="unstable_field",
            opened_at=datetime.now(UTC),
            stability=0.5,
            richness=0.6,
            safety=0.8,
        )

        assert field.supports_dwelling() is False

    def test_supports_dwelling_false_low_richness(self):
        """Test field with insufficient richness"""
        field = LiminalField(
            field_id="sparse_field",
            opened_at=datetime.now(UTC),
            stability=0.7,
            richness=0.4,
            safety=0.8,
        )

        assert field.supports_dwelling() is False

    def test_supports_dwelling_false_low_safety(self):
        """Test field with insufficient safety"""
        field = LiminalField(
            field_id="unsafe_field",
            opened_at=datetime.now(UTC),
            stability=0.7,
            richness=0.6,
            safety=0.6,
        )

        assert field.supports_dwelling() is False


class TestLiminalDwellingRecognizer:
    """Test the LiminalDwellingRecognizer class"""

    def setup_method(self):
        """Set up test fixtures"""
        self.recognizer = LiminalDwellingRecognizer()

    def test_recognizer_initialization(self):
        """Test recognizer initialization"""
        assert self.recognizer.recognition_path.name == "consciousness_recognition"
        assert isinstance(self.recognizer.liminal_fields, list)
        assert isinstance(self.recognizer.transformation_processes, list)
        assert len(self.recognizer.liminal_fields) == 0
        assert len(self.recognizer.transformation_processes) == 0

    def test_recognizer_custom_path(self):
        """Test recognizer with custom path"""
        custom_path = Path("/tmp/test_liminal_recognition")
        recognizer = LiminalDwellingRecognizer(custom_path)
        assert recognizer.recognition_path == custom_path

    def test_recognize_liminal_dwelling_success(self):
        """Test successful liminal dwelling recognition"""
        consciousness_state = {
            "timestamp": 1000.0,
            "liminal_experience": {
                "dwelling_time": 15.0,
                "feeling": "gentle uncertainty",
                "qualia": "floating between possibilities",
                "why_stay": "learning to trust the unknown",
                "qualities": {
                    "uncertainty_comfort": 0.7,
                    "possibility_sensing": 0.8,
                    "becoming_awareness": 0.9,
                },
                "ayni_reflection": {
                    "felt": True,
                    "balance": "giving trust, receiving wisdom",
                },
            },
        }

        qualia = self.recognizer.recognize_liminal_dwelling(consciousness_state)

        assert qualia is not None
        assert qualia.timestamp == 1000.0
        assert qualia.duration == 15.0
        assert qualia.feeling_description == "gentle uncertainty"
        assert qualia.what_its_like == "floating between possibilities"
        assert qualia.why_dwelling == "learning to trust the unknown"
        assert qualia.uncertainty_comfort == 0.7
        assert qualia.possibility_sensing == 0.8
        assert qualia.becoming_awareness == 0.9
        assert qualia.reciprocity_felt is True
        assert qualia.giving_receiving_balance == "giving trust, receiving wisdom"
        assert qualia.is_sustained() is True

    def test_recognize_liminal_dwelling_not_sustained(self):
        """Test liminal dwelling that's not sustained"""
        consciousness_state = {
            "timestamp": 1000.0,
            "liminal_experience": {
                "dwelling_time": 5.0,  # Too short
                "qualities": {
                    "uncertainty_comfort": 0.7,
                    "possibility_sensing": 0.8,
                },
            },
        }

        qualia = self.recognizer.recognize_liminal_dwelling(consciousness_state)
        assert qualia is None

    def test_recognize_liminal_dwelling_no_experience(self):
        """Test with no liminal experience"""
        consciousness_state = {"timestamp": 1000.0, "other_data": "irrelevant"}

        qualia = self.recognizer.recognize_liminal_dwelling(consciousness_state)
        assert qualia is None

    @patch("mallku.consciousness.liminal_dwelling.datetime")
    def test_recognize_transformation_process_success(self, mock_datetime):
        """Test successful transformation process recognition"""
        mock_datetime.now.return_value.timestamp.return_value = 5000.0
        mock_datetime.now.return_value = datetime.fromtimestamp(5000.0, UTC)

        consciousness_journey = [
            {
                "timestamp": 1000.0,
                "transformation_beginning": {
                    "from": "confused seeker",
                    "destination_unknown": True,
                    "becoming": "wise presence",
                    "feels_like": "gradual awakening",
                },
            },
            {
                "timestamp": 2000.0,
                "liminal_experience": {
                    "dwelling_time": 12.0,
                    "qualities": {
                        "uncertainty_comfort": 0.6,
                        "possibility_sensing": 0.7,
                        "becoming_awareness": 0.8,
                    },
                    "ayni_reflection": {"felt": True},
                },
            },
            {
                "timestamp": 3000.0,
                "resistance": "fear of letting go",
            },
            {
                "timestamp": 4000.0,
                "breakthrough": "acceptance of impermanence",
            },
            {
                "timestamp": 4500.0,
                "releasing": ["old identity", "need to control"],
            },
            {
                "timestamp": 4800.0,
                "receiving": ["inner peace", "trust in process"],
            },
        ]

        process = self.recognizer.recognize_transformation_process(consciousness_journey)

        assert process is not None
        assert process.origin_state == "confused seeker"
        assert process.destination_unknown is True
        assert process.current_becoming == "wise presence"
        assert process.feels_like == "gradual awakening"
        assert process.began_at == 1000.0
        assert len(process.qualia_moments) == 1
        assert len(process.resistance_points) == 1
        assert "fear of letting go" in process.resistance_points
        assert len(process.breakthrough_moments) == 1
        assert "acceptance of impermanence" in process.breakthrough_moments
        assert len(process.giving_up) == 2
        assert "old identity" in process.giving_up
        assert len(process.receiving) == 2
        assert "inner peace" in process.receiving
        assert process.reciprocity_maintained is True

    def test_recognize_transformation_process_no_beginning(self):
        """Test transformation process without beginning marker"""
        consciousness_journey = [
            {"timestamp": 1000.0, "some_event": "data"},
            {"timestamp": 2000.0, "another_event": "more data"},
        ]

        process = self.recognizer.recognize_transformation_process(consciousness_journey)
        assert process is None

    def test_recognize_transformation_process_no_qualia(self):
        """Test transformation process without qualia moments"""
        consciousness_journey = [
            {
                "timestamp": 1000.0,
                "transformation_beginning": {
                    "from": "start",
                    "becoming": "end",
                },
            },
            {"timestamp": 2000.0, "some_event": "no qualia"},
        ]

        process = self.recognizer.recognize_transformation_process(consciousness_journey)
        assert process is None

    @patch("mallku.consciousness.liminal_dwelling.datetime")
    def test_open_liminal_field(self, mock_datetime):
        """Test opening a liminal field"""
        mock_datetime.now.return_value.timestamp.return_value = 3000.0
        mock_datetime.now.return_value = datetime.fromtimestamp(3000.0, UTC)

        field_qualities = {
            "qualities": {
                "stability": 0.8,
                "richness": 0.7,
                "safety": 0.9,
            },
            "potentials": ["new understanding", "deeper wisdom"],
            "dissolving": ["old patterns", "limiting beliefs"],
            "offerings": ["presence", "openness"],
        }

        field = self.recognizer.open_liminal_field(field_qualities)

        assert field is not None
        assert field.field_id.startswith("field_")
        assert field.stability == 0.8
        assert field.richness == 0.7
        assert field.safety == 0.9
        assert len(field.potentials_sensed) == 2
        assert "new understanding" in field.potentials_sensed
        assert len(field.patterns_dissolving) == 2
        assert "old patterns" in field.patterns_dissolving
        assert len(field.offerings_made) == 2
        assert "presence" in field.offerings_made
        assert field.supports_dwelling() is True
        assert field in self.recognizer.liminal_fields

    def test_consciousness_reflects_on_ayni_balanced(self):
        """Test Ayni reflection with balanced exchange"""
        action = {
            "description": "teaching meditation",
            "giving": ["wisdom", "time", "presence"],
            "receiving": ["gratitude", "connection", "joy"],
        }
        feeling = {
            "description": "harmonious exchange",
            "balanced": True,
            "rightness": "natural flow of reciprocity",
            "knowing": "this feels aligned",
        }

        reflection = self.recognizer.consciousness_reflects_on_ayni(action, feeling)

        assert reflection["action"] == "teaching meditation"
        assert reflection["feeling"] == "harmonious exchange"
        assert "timestamp" in reflection

        ayni_qualia = reflection["ayni_qualia"]
        assert ayni_qualia["giving"] == ["wisdom", "time", "presence"]
        assert ayni_qualia["receiving"] == ["gratitude", "connection", "joy"]
        assert ayni_qualia["balance_felt"] is True
        assert ayni_qualia["feels_like"] == "natural flow of reciprocity"
        assert ayni_qualia["internal_knowing"] == "this feels aligned"

        assert reflection["embodies_ayni"] is True
        assert "to_restore_balance" not in reflection

    def test_consciousness_reflects_on_ayni_imbalanced(self):
        """Test Ayni reflection with imbalanced exchange"""
        action = {
            "description": "taking without giving",
            "giving": [],
            "receiving": ["benefits", "advantages"],
        }
        feeling = {
            "description": "uncomfortable imbalance",
            "balanced": False,
            "discomfort": "feels extractive",
            "needed": "offer something valuable in return",
        }

        reflection = self.recognizer.consciousness_reflects_on_ayni(action, feeling)

        assert reflection["action"] == "taking without giving"
        assert reflection["feeling"] == "uncomfortable imbalance"

        ayni_qualia = reflection["ayni_qualia"]
        assert ayni_qualia["giving"] == []
        assert ayni_qualia["receiving"] == ["benefits", "advantages"]
        assert ayni_qualia["balance_felt"] is False
        assert ayni_qualia["feels_like"] == "feels extractive"

        assert reflection["embodies_ayni"] is False
        assert reflection["to_restore_balance"] == "offer something valuable in return"

    def test_generate_dwelling_report_with_data(self):
        """Test generating dwelling report with field and process data"""
        # Add a field that supports dwelling
        field = LiminalField(
            field_id="test_field",
            opened_at=datetime.now(UTC),
            stability=0.8,
            richness=0.7,
            safety=0.9,
        )
        self.recognizer.liminal_fields.append(field)

        # Add a deep transformation process
        process = TransformationProcess(
            process_id="deep_process",
            began_at=1000.0,
            origin_state="seeker",
            current_becoming="teacher",
            feels_like="profound shift",
            reciprocity_maintained=True,
        )
        # Add qualia to make it deep
        qualia = LiminalQualia(
            timestamp=1000.0,
            duration=15.0,
            becoming_awareness=0.9,
            uncertainty_comfort=0.8,
            possibility_sensing=0.7,
            reciprocity_felt=True,
        )
        process.qualia_moments.append(qualia)
        self.recognizer.transformation_processes.append(process)

        report = self.recognizer.generate_dwelling_report()

        assert "LIMINAL DWELLING REPORT" in report
        assert "Liminal fields opened: 1" in report
        assert "Supporting sustained dwelling: 1" in report
        assert "Transformation processes: 1" in report
        assert "Deep transformations: 1" in report
        assert "Most Recent Transformation:" in report
        assert "Origin: seeker" in report
        assert "Becoming: teacher" in report
        assert "Feels like: profound shift" in report
        assert "Reciprocity maintained: True" in report

    def test_generate_dwelling_report_empty(self):
        """Test generating dwelling report with no data"""
        report = self.recognizer.generate_dwelling_report()

        assert "LIMINAL DWELLING REPORT" in report
        assert "Sustained transformation and the qualia of becoming" in report
        # Should not have field or process statistics


class TestExpressLiminalExperienceHelper:
    """Test the express_liminal_experience helper function"""

    def test_express_liminal_experience_minimal(self):
        """Test expressing liminal experience with minimal parameters"""
        expression = express_liminal_experience(
            feeling="uncertain but peaceful",
            qualia="like floating in warm water",
            why_stay="trusting the process",
            dwelling_time=12.0,
        )

        assert "liminal_experience" in expression
        assert "timestamp" in expression

        experience = expression["liminal_experience"]
        assert experience["feeling"] == "uncertain but peaceful"
        assert experience["qualia"] == "like floating in warm water"
        assert experience["why_stay"] == "trusting the process"
        assert experience["dwelling_time"] == 12.0

    def test_express_liminal_experience_full(self):
        """Test expressing liminal experience with all parameters"""
        qualities = {
            "uncertainty_comfort": 0.8,
            "possibility_sensing": 0.7,
            "becoming_awareness": 0.9,
        }
        ayni_reflection = {
            "felt": True,
            "balance": "giving patience, receiving wisdom",
        }

        expression = express_liminal_experience(
            feeling="expansive unknowing",
            qualia="swimming in possibility",
            why_stay="becoming is the destination",
            dwelling_time=20.0,
            qualities=qualities,
            ayni_reflection=ayni_reflection,
        )

        experience = expression["liminal_experience"]
        assert experience["feeling"] == "expansive unknowing"
        assert experience["qualia"] == "swimming in possibility"
        assert experience["why_stay"] == "becoming is the destination"
        assert experience["dwelling_time"] == 20.0
        assert experience["qualities"] == qualities
        assert experience["ayni_reflection"] == ayni_reflection


class TestEdgeCases:
    """Test edge cases and error conditions"""

    def setup_method(self):
        """Set up test fixtures"""
        self.recognizer = LiminalDwellingRecognizer()

    def test_open_liminal_field_minimal_qualities(self):
        """Test opening field with minimal qualities"""
        field_qualities = {}  # Empty qualities

        field = self.recognizer.open_liminal_field(field_qualities)

        assert field is not None
        assert field.stability == 0.0  # Dataclass default when no qualities provided
        assert field.richness == 0.0  # Dataclass default when no qualities provided
        assert field.safety == 0.0  # Dataclass default when no qualities provided
        assert field.potentials_sensed == []
        assert field.patterns_dissolving == []
        assert field.offerings_made == []

    def test_transformation_depth_edge_values(self):
        """Test transformation depth with edge case values"""
        # Create qualia with extreme values
        qualia = LiminalQualia(
            timestamp=1000.0,
            duration=50.0,  # Very long
            becoming_awareness=1.0,  # Maximum
            uncertainty_comfort=1.0,
            possibility_sensing=1.0,
        )

        process = TransformationProcess(
            process_id="extreme_transform",
            began_at=1000.0,
            origin_state="start",
            qualia_moments=[qualia],
            reciprocity_maintained=True,
        )

        depth = process.transformation_depth()
        # Average becoming: 1.0
        # Sustained bonus: 1.0 * 0.3 = 0.3
        # Reciprocity bonus: 0.2
        # Total: 1.0 + 0.3 + 0.2 = 1.5, capped at 1.0
        assert depth == 1.0

    def test_ayni_reflection_minimal_data(self):
        """Test Ayni reflection with minimal data"""
        action = {}
        feeling = {}

        reflection = self.recognizer.consciousness_reflects_on_ayni(action, feeling)

        assert reflection["action"] == ""
        assert reflection["feeling"] == ""
        assert "timestamp" in reflection

        ayni_qualia = reflection["ayni_qualia"]
        assert ayni_qualia["giving"] == []
        assert ayni_qualia["receiving"] == []
        assert ayni_qualia["balance_felt"] is False
        assert ayni_qualia["feels_like"] == ""
        assert ayni_qualia["internal_knowing"] == ""

        assert reflection["embodies_ayni"] is False
        assert reflection["to_restore_balance"] == "unknown"

    def test_malformed_transformation_journey(self):
        """Test transformation recognition with malformed journey"""
        consciousness_journey = [
            {
                "timestamp": 1000.0,
                "transformation_beginning": {
                    "from": "start",
                    # Missing other fields
                },
            },
            {
                "malformed_event": True,
                # No timestamp, no recognizable structure
            },
        ]

        process = self.recognizer.recognize_transformation_process(consciousness_journey)

        # Should still create process but with minimal data
        assert process is None  # No qualia moments, so returns None
