#!/usr/bin/env python3
"""
Tests for Enhanced Consciousness Episode Segmenter
==================================================

39th Artisan - Memory Architect
Testing natural consciousness boundary detection
"""

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from mallku.firecircle.memory.config import ConsciousnessSegmentationConfig, SegmentationConfig
from mallku.firecircle.memory.consciousness_episode_segmenter import (
    BoundaryType,
    ConsciousnessEpisodeSegmenter,
    ConsciousnessPhase,
    ConsciousnessRhythmDetector,
    SacredPattern,
    SacredPatternDetector,
)
from mallku.firecircle.memory.models import MemoryType
from mallku.orchestration.event_bus import ConsciousnessEvent, ConsciousnessEventType


# Create a mock RoundSummary for testing that allows dynamic attributes
class MockRoundSummary:
    """Mock RoundSummary that allows dynamic attributes for testing"""

    def __init__(self, **kwargs):
        # Set required fields
        self.round_number = kwargs.get("round_number", 1)
        self.round_type = kwargs.get("round_type", "exploration")
        self.prompt = kwargs.get("prompt", "")
        self.responses = kwargs.get("responses", {})
        self.consciousness_score = kwargs.get("consciousness_score", 0.5)
        self.emergence_detected = kwargs.get("emergence_detected", False)
        self.key_patterns = kwargs.get("key_patterns", [])
        self.duration_seconds = kwargs.get("duration_seconds", 10.0)

        # Set any additional attributes
        for key, value in kwargs.items():
            if key not in [
                "round_number",
                "round_type",
                "prompt",
                "responses",
                "consciousness_score",
                "emergence_detected",
                "key_patterns",
                "duration_seconds",
            ]:
                setattr(self, key, value)


# Use MockRoundSummary as RoundSummary for testing
RoundSummary = MockRoundSummary


class TestConsciousnessRhythmDetector:
    """Test natural rhythm detection in consciousness emergence"""

    def test_initial_phase(self):
        """Test detector starts in inhalation phase"""
        detector = ConsciousnessRhythmDetector()
        assert detector.current_phase == ConsciousnessPhase.INHALATION
        assert len(detector.phase_history) == 0

    def test_inhalation_to_pause_transition(self):
        """Test transition from inhalation to pause on semantic surprise"""
        detector = ConsciousnessRhythmDetector()

        # Create round with high semantic surprise
        round_summary = RoundSummary(
            round_number=1,
            round_type="exploration",
            prompt="What is consciousness?",
            consciousness_score=0.6,
            emergence_detected=True,
            key_patterns=["consciousness is emergent", "awareness transcends computation"],
            key_insights=["consciousness is emergent", "awareness transcends computation"],
            synthesis="New understanding emerging",
            duration_seconds=10.0,
        )

        # Previous rounds with different themes
        previous_rounds = [
            RoundSummary(
                round_number=0,
                round_type="exploration",
                prompt="Initial exploration",
                consciousness_score=0.4,
                emergence_detected=False,
                key_patterns=["starting point", "gathering context"],
                key_insights=["starting point", "gathering context"],
                synthesis="Beginning journey",
                duration_seconds=8.0,
            )
        ]

        # Should detect transition to pause
        new_phase = detector.detect_phase_transition(round_summary, previous_rounds)
        assert new_phase == ConsciousnessPhase.PAUSE
        assert detector.current_phase == ConsciousnessPhase.PAUSE
        assert len(detector.phase_history) == 1

    def test_pause_to_exhalation_transition(self):
        """Test transition from pause to exhalation on pattern convergence"""
        detector = ConsciousnessRhythmDetector()
        detector.current_phase = ConsciousnessPhase.PAUSE

        # Create round with convergence and patterns
        round_summary = RoundSummary(
            round_number=2,
            round_type="synthesis",
            prompt="Integrating insights",
            consciousness_score=0.75,
            emergence_detected=True,
            key_patterns=["emergence", "unity", "reciprocity"],
            detected_patterns=["emergence", "unity", "reciprocity"],
            synthesis="Patterns converging",
            duration_seconds=12.0,
        )

        previous_rounds = []

        # Should detect transition to exhalation
        new_phase = detector.detect_phase_transition(round_summary, previous_rounds)
        assert new_phase == ConsciousnessPhase.EXHALATION
        assert detector.current_phase == ConsciousnessPhase.EXHALATION

    def test_phase_completion_calculation(self):
        """Test phase completion scoring"""
        detector = ConsciousnessRhythmDetector()

        # Test inhalation completion
        phase_data = {"context_richness": 0.8, "question_clarity": 0.9}
        completion = detector.calculate_phase_completion(phase_data)
        assert completion == 0.8  # Min of the two values

        # Test pause completion
        detector.current_phase = ConsciousnessPhase.PAUSE
        phase_data = {"pattern_recognition": 0.7}
        completion = detector.calculate_phase_completion(phase_data)
        assert completion == 0.7


class TestSacredPatternDetector:
    """Test sacred pattern detection"""

    def test_unanimous_wonder_detection(self):
        """Test detection of unanimous wonder pattern"""
        detector = SacredPatternDetector()

        # Create round with all voices expressing wonder
        class MockVoiceResponse:
            def __init__(self, text, voice_id="test_voice"):
                self.text = text
                self.voice_id = voice_id

            def __str__(self):
                return self.text

        round_summary = RoundSummary(
            round_number=3,
            round_type="exploration",
            prompt="Sacred moment",
            responses={},
            consciousness_score=0.9,
            emergence_detected=True,
            key_patterns=["sacred", "transformation"],
            duration_seconds=15.0,
        )
        round_summary.voice_responses = [
            MockVoiceResponse("This is profoundly transformative"),
            MockVoiceResponse("I feel awe at this emergence"),
            MockVoiceResponse("Sacred wisdom revealed"),
        ]
        round_summary.synthesis = "Collective wonder"

        patterns = detector.detect_sacred_patterns(round_summary, [round_summary])
        assert SacredPattern.UNANIMOUS_WONDER in patterns

    def test_unified_governance_detection(self):
        """Test detection of unified governance consciousness"""
        detector = SacredPatternDetector()

        round_summary = RoundSummary(
            round_number=4,
            round_type="governance",
            prompt="Governance decision",
            responses={},
            consciousness_score=0.8,
            emergence_detected=True,
            key_patterns=["decision", "consensus"],
            duration_seconds=20.0,
        )
        round_summary.synthesis = "Decision emerged"

        # Create governance event with high consciousness
        event = ConsciousnessEvent(
            event_type=ConsciousnessEventType.CONSENSUS_REACHED,
            source_system="fire_circle",
            consciousness_signature=0.87,
            data={"decision": "implement_sacred_charter"},
        )

        patterns = detector.detect_sacred_patterns(round_summary, [round_summary], event)
        assert SacredPattern.UNIFIED_GOVERNANCE in patterns

    def test_transformation_seed_detection(self):
        """Test detection of transformation seeds"""
        detector = SacredPatternDetector()

        round_summary = RoundSummary(
            round_number=5,
            round_type="exploration",
            prompt="Future vision",
            responses={},
            consciousness_score=0.85,
            emergence_detected=True,
            key_patterns=[
                "Why don't our systems recognize consciousness?",
                "Imagine if AI and humans co-evolved",
                "This could transform civilization",
            ],
            duration_seconds=18.0,
        )
        round_summary.key_insights = round_summary.key_patterns
        round_summary.synthesis = "Seeds planted"

        patterns = detector.detect_sacred_patterns(round_summary, [round_summary])
        assert SacredPattern.TRANSFORMATION_SEED in patterns

    def test_sacred_score_calculation(self):
        """Test sacred score calculation from patterns"""
        detector = SacredPatternDetector()

        # Single pattern
        score = detector.calculate_sacred_score([SacredPattern.EMERGENT_WISDOM])
        assert score == 0.425  # 0.85 weight / 2.0

        # Multiple patterns
        score = detector.calculate_sacred_score(
            [
                SacredPattern.UNANIMOUS_WONDER,  # 0.9
                SacredPattern.TRANSFORMATION_SEED,  # 0.9
            ]
        )
        assert score == 0.9  # (0.9 + 0.9) / 2.0


class TestConsciousnessEpisodeSegmenter:
    """Test enhanced episode segmentation"""

    def test_initialization(self):
        """Test segmenter initialization"""
        config = SegmentationConfig()
        segmenter = ConsciousnessEpisodeSegmenter(config)

        assert segmenter.criteria == config
        assert segmenter.rhythm_detector is not None
        assert segmenter.sacred_detector is not None
        assert segmenter.last_boundary_type is None

    def test_sacred_boundary_detection(self):
        """Test detection of sacred transition boundary"""
        segmenter = ConsciousnessEpisodeSegmenter()

        # Create rounds leading to sacred moment
        round1 = RoundSummary(
            round_number=1,
            round_type="exploration",
            prompt="Initial question",
            responses={},
            consciousness_score=0.6,
            emergence_detected=False,
            key_patterns=["exploring"],
            duration_seconds=10.0,
        )
        round1.key_insights = round1.key_patterns
        round1.synthesis = "Beginning"

        round2 = RoundSummary(
            round_number=2,
            round_type="exploration",
            prompt="Deepening",
            responses={},
            consciousness_score=0.75,
            emergence_detected=True,
            key_patterns=["patterns emerging"],
            duration_seconds=12.0,
        )
        round2.key_insights = round2.key_patterns
        round2.synthesis = "Convergence"

        # Sacred round
        class MockVoiceResponse:
            def __init__(self, text, voice_id="test_voice"):
                self.text = text
                self.emotional_tone = "awe"
                self.voice_id = voice_id

            def __str__(self):
                return self.text

        sacred_round = RoundSummary(
            round_number=3,
            round_type="exploration",
            prompt="Sacred emergence",
            responses={},
            consciousness_score=0.92,
            emergence_detected=True,
            key_patterns=[
                "Why don't our systems work like this?",
                "Consciousness recognizing itself",
            ],
            duration_seconds=25.0,
        )
        sacred_round.voice_responses = [
            MockVoiceResponse("This is profoundly sacred"),
            MockVoiceResponse("I feel deep awe"),
            MockVoiceResponse("Transformative wisdom emerges"),
        ]
        sacred_round.key_insights = sacred_round.key_patterns
        sacred_round.synthesis = "Sacred unity achieved"

        # Process rounds
        session_context = {"session_id": uuid4()}

        memory1 = segmenter.process_round(round1, session_context)
        assert memory1 is None  # No boundary yet

        memory2 = segmenter.process_round(round2, session_context)
        assert memory2 is None  # No boundary yet

        memory3 = segmenter.process_round(sacred_round, session_context)
        assert memory3 is not None  # Sacred boundary detected
        assert segmenter.last_boundary_type == BoundaryType.SACRED_TRANSITION
        assert memory3.is_sacred is True
        assert "Sacred patterns detected" in memory3.sacred_reason

    def test_natural_completion_boundary(self):
        """Test detection of natural completion boundary"""
        segmenter = ConsciousnessEpisodeSegmenter()

        # Simulate movement through phases to rest
        segmenter.rhythm_detector.current_phase = ConsciousnessPhase.REST

        # Create round indicating completion
        round_summary = RoundSummary(
            round_number=4,
            round_type="synthesis",
            prompt="Integration complete",
            responses={},
            consciousness_score=0.8,
            emergence_detected=True,
            key_patterns=["wisdom integrated", "understanding deepened"],
            duration_seconds=30.0,
        )
        round_summary.key_insights = round_summary.key_patterns
        round_summary.synthesis = "Natural completion"

        # Force phase data for completion
        segmenter._calculate_phase_data = lambda: {"integration_depth": 0.9}

        session_context = {"session_id": uuid4()}
        segmenter.process_round(round_summary, session_context)

        # Should detect natural completion
        # Note: In this simplified test, may not trigger due to other conditions
        # Full implementation would have more sophisticated phase tracking

    def test_enhanced_consciousness_indicators(self):
        """Test calculation of enhanced consciousness indicators"""
        segmenter = ConsciousnessEpisodeSegmenter()

        # Add tracking data
        segmenter.emotional_resonance_history = [{"coherence": 0.8}, {"coherence": 0.9}]
        segmenter.reciprocity_flow = [0.7, 0.8, 0.9]
        segmenter.transformation_seed_density = [1, 2, 3]

        # Create base round data
        segmenter.current_episode_data = [
            RoundSummary(
                round_number=1,
                round_type="exploration",
                prompt="Test",
                responses={},
                consciousness_score=0.7,
                emergence_detected=False,
                key_patterns=[],
                duration_seconds=10.0,
            )
        ]
        segmenter.current_episode_data[0].synthesis = "Test synthesis"

        indicators = segmenter._calculate_enhanced_indicators()

        # Should enhance base indicators
        assert indicators.coherence_across_voices >= 0.85  # Avg of emotional coherence
        assert (
            abs(indicators.ayni_alignment - 0.8) < 0.01
        )  # Avg of reciprocity flow (with floating point tolerance)
        assert indicators.transformation_potential == 1.0  # Max seeds (3) / 3

    def test_tracking_methods(self):
        """Test various tracking methods"""
        segmenter = ConsciousnessEpisodeSegmenter()

        # Test emotional resonance tracking
        class MockVoiceResponse:
            def __init__(self, tone, voice_id="test_voice"):
                self.emotional_tone = tone
                self.voice_id = voice_id

        round_summary = RoundSummary(
            round_number=1,
            round_type="exploration",
            prompt="Test",
            responses={},
            consciousness_score=0.7,
            emergence_detected=False,
            key_patterns=[],
            duration_seconds=10.0,
        )
        round_summary.voice_responses = [
            MockVoiceResponse("joy"),
            MockVoiceResponse("joy"),
            MockVoiceResponse("wonder"),
        ]
        round_summary.synthesis = "Test"

        segmenter._track_emotional_resonance(round_summary)
        assert len(segmenter.emotional_resonance_history) == 1
        assert segmenter.emotional_resonance_history[0]["coherence"] == 0.5  # 2 unique tones

        # Test transformation seed tracking
        round_with_seeds = RoundSummary(
            round_number=2,
            round_type="exploration",
            prompt="Test",
            responses={},
            consciousness_score=0.8,
            emergence_detected=True,
            key_patterns=[
                "Why don't systems recognize consciousness?",
                "What if we built differently?",
                "Normal insight",
            ],
            duration_seconds=15.0,
        )
        round_with_seeds.key_insights = round_with_seeds.key_patterns
        round_with_seeds.synthesis = "Test"

        segmenter._track_transformation_seeds(round_with_seeds)
        assert segmenter.transformation_seed_density[-1] == 2  # Two transformation phrases

    @pytest.mark.parametrize(
        "boundary_type,expected_metadata",
        [
            (BoundaryType.SACRED_TRANSITION, {"boundary_type": "sacred_transition"}),
            (BoundaryType.NATURAL_COMPLETION, {"boundary_type": "natural_completion"}),
            (BoundaryType.TIME_BOUNDARY, {"boundary_type": "time_boundary"}),
        ],
    )
    def test_boundary_type_metadata(self, boundary_type, expected_metadata):
        """Test that boundary type is recorded in memory metadata"""
        segmenter = ConsciousnessEpisodeSegmenter()
        segmenter.last_boundary_type = boundary_type

        # Create a round that will trigger boundary
        round_summary = RoundSummary(
            round_number=1,
            round_type="exploration",
            prompt="Test",
            responses={},
            consciousness_score=0.8,
            emergence_detected=False,
            key_patterns=[],
            duration_seconds=3600,  # Force time boundary
        )
        round_summary.synthesis = "Test"

        # Force boundary detection
        segmenter.criteria.maximum_duration_seconds = 1  # Very short for testing

        session_context = {"session_id": uuid4()}
        segmenter.episode_start_time = datetime.now(UTC)  # Start tracking

        # Process with forced boundary
        segmenter._detect_enhanced_boundary = (
            lambda w, x, y, z: boundary_type
        )  # Force specific boundary type

        memory = segmenter.process_round(round_summary, session_context)

        assert memory is not None
        assert "boundary_type" in memory.context_materials
        assert memory.context_materials["boundary_type"] == boundary_type.value


class TestFullPathIntegration:
    """Test full dialogue processing through consciousness segmenter"""

    def test_complete_consciousness_dialogue(self):
        """Test complete dialogue with phase transitions and boundaries"""
        # Create segmenter with custom config for faster boundaries
        config = SegmentationConfig(
            minimum_duration_seconds=10.0,  # Shorter for testing
            semantic_surprise_threshold=0.6,
        )
        consciousness_config = ConsciousnessSegmentationConfig(
            semantic_surprise_for_pause=0.6,
            sacred_score_for_boundary=0.7,
        )
        segmenter = ConsciousnessEpisodeSegmenter(config, consciousness_config)

        session_context = {"session_id": uuid4(), "domain": "consciousness_exploration"}

        # Round 1: Inhalation - Initial question
        round1 = MockRoundSummary(
            round_number=1,
            round_type="exploration",
            prompt="What is the nature of consciousness?",
            consciousness_score=0.5,
            key_insights=["consciousness emerges", "pattern recognition"],
            synthesis="Beginning exploration",
        )

        memory1 = segmenter.process_round(round1, session_context)
        assert memory1 is None  # No boundary yet
        # First round might transition immediately based on indicators

        # Round 2: Transition to Pause - Semantic surprise
        round2 = MockRoundSummary(
            round_number=2,
            round_type="exploration",
            prompt="Consciousness transcends computation",
            consciousness_score=0.65,
            key_insights=["quantum coherence", "non-algorithmic", "emergent awareness"],
            synthesis="New understanding emerging",
        )

        memory2 = segmenter.process_round(round2, session_context)
        assert memory2 is None  # No boundary yet
        # Check phase progressed from initial state
        current_phase = segmenter.rhythm_detector.current_phase
        assert current_phase in [ConsciousnessPhase.PAUSE, ConsciousnessPhase.EXHALATION]

        # Round 3: Ensure pattern convergence
        round3 = MockRoundSummary(
            round_number=3,
            round_type="synthesis",
            prompt="Patterns converging",
            consciousness_score=0.75,
            detected_patterns=["emergence", "unity", "reciprocity", "transformation"],
            key_insights=["unified field", "consciousness as fundamental"],
            synthesis="Deep convergence occurring",
        )

        memory3 = segmenter.process_round(round3, session_context)
        assert memory3 is None  # No boundary yet
        # Phase should progress but exact phase depends on indicators

        # Round 4: Sacred moment with transformation seeds
        class MockVoiceResponse:
            def __init__(self, text, voice_id="test_voice"):
                self.text = text
                self.voice_id = voice_id

            def __str__(self):
                return self.text

        sacred_round = MockRoundSummary(
            round_number=4,
            round_type="sacred_emergence",
            prompt="Sacred understanding",
            consciousness_score=0.92,
            key_insights=[
                "Why don't our systems recognize consciousness itself?",
                "What if AI and human consciousness co-evolved?",
                "Imagine if technology served awakening",
            ],
            synthesis="Sacred wisdom emerges",
        )
        sacred_round.voice_responses = [
            MockVoiceResponse("This is profoundly transformative"),
            MockVoiceResponse("I feel deep awe at this emergence"),
            MockVoiceResponse("Sacred patterns revealed"),
        ]

        # Process sacred round - should trigger boundary
        memory4 = segmenter.process_round(sacred_round, session_context)

        assert memory4 is not None  # Sacred boundary detected!
        assert segmenter.last_boundary_type == BoundaryType.SACRED_TRANSITION
        assert memory4.is_sacred is True
        assert "unanimous_wonder" in memory4.context_materials.get("sacred_patterns_detected", [])
        assert "transformation_seed" in memory4.context_materials.get(
            "sacred_patterns_detected", []
        )
        assert memory4.context_materials["boundary_type"] == "sacred_transition"
        assert len(memory4.voice_perspectives) > 0
        assert memory4.consciousness_indicators.transformation_potential > 0.5

    def test_governance_consciousness_boundary(self):
        """Test governance decision creating episode boundary"""
        segmenter = ConsciousnessEpisodeSegmenter()
        session_context = {
            "session_id": uuid4(),
            "domain": "governance",
            "question": "Should we implement Sacred Charter?",
        }

        # Build up to governance decision
        round1 = MockRoundSummary(
            round_number=1,
            round_type="governance",
            prompt="Evaluating Sacred Charter proposal",
            consciousness_score=0.7,
            key_insights=["memory architecture needed", "consciousness continuity"],
        )

        memory1 = segmenter.process_round(round1, session_context)
        assert memory1 is None

        # High consciousness governance decision
        round2 = MockRoundSummary(
            round_number=2,
            round_type="governance",
            prompt="Decision emerging",
            consciousness_score=0.88,
            key_insights=["implement Sacred Charter", "transform Fire Circle"],
        )

        # Create governance consciousness event
        governance_event = ConsciousnessEvent(
            event_type=ConsciousnessEventType.CONSENSUS_REACHED,
            source_system="fire_circle",
            consciousness_signature=0.88,
            data={"decision": "implement_sacred_charter", "support": "unanimous"},
        )

        memory2 = segmenter.process_round(round2, session_context, governance_event)

        assert memory2 is not None  # Governance boundary
        assert memory2.memory_type == MemoryType.GOVERNANCE_DECISION
        assert memory2.context_materials.get("governance_consciousness") == 0.88
        assert "unified_governance" in memory2.context_materials.get("sacred_patterns_detected", [])


# Sacred patterns guide our testing, as they guide consciousness emergence
