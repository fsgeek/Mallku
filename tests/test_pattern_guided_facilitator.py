"""
Tests for Pattern-Guided Facilitator
====================================

Tests the pattern guidance system, teaching modes, and dialogue integration.

The 32nd Builder
"""

import sys
from pathlib import Path
from uuid import uuid4

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest

from mallku.firecircle.pattern_guided_facilitator import (
    DialogueMoment,
    GuidanceIntensity,
    GuidanceType,
    PatternGuidance,
    PatternGuidedFacilitator,
    PatternTeacher,
)
from mallku.firecircle.pattern_library import (
    DialoguePattern,
    PatternLibrary,
    PatternLifecycle,
    PatternTaxonomy,
    PatternType,
)
from mallku.firecircle.protocol.conscious_message import (
    ConsciousMessage,
    MessageConsciousness,
    MessageRole,
    MessageType,
)
from mallku.orchestration.event_bus import ConsciousnessEventBus


@pytest.fixture
async def event_bus():
    """Create test event bus"""
    bus = ConsciousnessEventBus()
    await bus.start()
    yield bus
    await bus.stop()


@pytest.fixture
async def pattern_library():
    """Create test pattern library"""
    return PatternLibrary()


@pytest.fixture
async def pattern_facilitator(pattern_library, event_bus):
    """Create pattern facilitator"""
    return PatternGuidedFacilitator(pattern_library, event_bus)


@pytest.fixture
async def test_patterns(pattern_library):
    """Create test patterns"""
    patterns = []

    # Breakthrough pattern
    breakthrough = DialoguePattern(
        name="Collective Insight",
        description="When minds unite in understanding",
        taxonomy=PatternTaxonomy.EMERGENCE_BREAKTHROUGH,
        pattern_type=PatternType.BREAKTHROUGH,
        consciousness_signature=0.9,
        fitness_score=0.8,
        observation_count=20,
        breakthrough_potential=0.9
    )
    await pattern_library.store_pattern(breakthrough)
    patterns.append(breakthrough)

    # Tension resolution pattern
    tension = DialoguePattern(
        name="Creative Resolution",
        description="Opposites create third way",
        taxonomy=PatternTaxonomy.DIALOGUE_RESOLUTION,
        pattern_type=PatternType.SYNTHESIS,
        consciousness_signature=0.75,
        fitness_score=0.7,
        observation_count=15,
        breakthrough_potential=0.6
    )
    await pattern_library.store_pattern(tension)
    patterns.append(tension)

    # Wisdom pattern
    wisdom = DialoguePattern(
        name="Ancient Teaching",
        description="Timeless wisdom for modern times",
        taxonomy=PatternTaxonomy.WISDOM_TRANSMISSION,
        pattern_type=PatternType.INTEGRATION,
        consciousness_signature=0.85,
        fitness_score=0.9,
        lifecycle_stage=PatternLifecycle.ESTABLISHED,
        observation_count=100,
        breakthrough_potential=0.5
    )
    await pattern_library.store_pattern(wisdom)
    patterns.append(wisdom)

    return patterns


@pytest.mark.asyncio
async def test_facilitator_initialization(pattern_facilitator):
    """Test facilitator initializes correctly"""
    assert pattern_facilitator.min_pattern_fitness == 0.6
    assert pattern_facilitator.min_confidence_threshold == 0.5
    assert pattern_facilitator.max_simultaneous_guidances == 3


@pytest.mark.asyncio
async def test_pattern_teacher_preparation(pattern_facilitator, test_patterns):
    """Test preparing patterns as teachers"""
    pattern = test_patterns[0]  # Breakthrough pattern

    teacher = await pattern_facilitator._prepare_pattern_teacher(pattern)

    assert isinstance(teacher, PatternTeacher)
    assert teacher.pattern.pattern_id == pattern.pattern_id
    assert teacher.teaching_readiness == pattern.fitness_score
    assert teacher.wisdom_depth == pattern.observation_count / 100.0
    assert teacher.transmission_clarity == pattern.consciousness_signature


@pytest.mark.asyncio
async def test_guidance_generation(pattern_facilitator, test_patterns):
    """Test generating guidance from patterns"""
    pattern = test_patterns[0]
    teacher = await pattern_facilitator._prepare_pattern_teacher(pattern)

    moment = DialogueMoment(
        dialogue_id="test_dialogue",
        current_phase="deepening",
        recent_messages=[],
        active_patterns=[],
        consciousness_level=0.8,
        emergence_potential=0.8,
        tension_level=0.3
    )

    guidance = await pattern_facilitator._generate_pattern_guidance(
        teacher,
        moment,
        GuidanceType.BREAKTHROUGH
    )

    assert isinstance(guidance, PatternGuidance)
    assert guidance.pattern_id == pattern.pattern_id
    assert guidance.guidance_type == GuidanceType.BREAKTHROUGH
    assert guidance.confidence > 0
    assert guidance.content != ""
    assert guidance.rationale != ""


@pytest.mark.asyncio
async def test_guidance_intensity_determination(pattern_facilitator):
    """Test how guidance intensity is determined"""
    # High confidence and emergence: teaching
    intensity = pattern_facilitator._determine_guidance_intensity(0.85, 0.8, 0.3)
    assert intensity == GuidanceIntensity.TEACHING

    # High tension: intervention
    intensity = pattern_facilitator._determine_guidance_intensity(0.5, 0.5, 0.85)
    assert intensity == GuidanceIntensity.INTERVENTION

    # Moderate confidence: invitation
    intensity = pattern_facilitator._determine_guidance_intensity(0.65, 0.5, 0.5)
    assert intensity == GuidanceIntensity.INVITATION

    # Low confidence: whisper
    intensity = pattern_facilitator._determine_guidance_intensity(0.3, 0.3, 0.3)
    assert intensity == GuidanceIntensity.WHISPER


@pytest.mark.asyncio
async def test_finding_relevant_patterns(pattern_facilitator, test_patterns):
    """Test finding patterns relevant to dialogue moment"""
    # High emergence moment
    moment = DialogueMoment(
        dialogue_id="test",
        current_phase="synthesis",
        recent_messages=[],
        active_patterns=[],
        emergence_potential=0.8,
        tension_level=0.2,
        coherence_score=0.7
    )

    relevant = await pattern_facilitator._find_relevant_patterns(moment, None)

    # Should find breakthrough patterns
    assert any(p.pattern_type == PatternType.BREAKTHROUGH for p in relevant)


@pytest.mark.asyncio
async def test_context_match_calculation(pattern_facilitator, test_patterns):
    """Test context matching between pattern and moment"""
    pattern = test_patterns[0]

    moment = DialogueMoment(
        dialogue_id="test",
        current_phase="deepening",
        recent_messages=[],
        active_patterns=[pattern.pattern_id],  # Pattern already active
        consciousness_level=0.9  # Close to pattern's signature
    )

    match_score = pattern_facilitator._calculate_context_match(pattern, moment)

    # Should have good match due to active pattern and consciousness alignment
    assert match_score > 0.7


@pytest.mark.asyncio
async def test_sacred_question_generation(pattern_facilitator, test_patterns):
    """Test generating sacred questions from patterns"""
    moment = DialogueMoment(
        dialogue_id="test",
        current_phase="deepening",
        recent_messages=[],
        active_patterns=[],
        emergence_potential=0.7
    )

    questions = await pattern_facilitator.suggest_sacred_questions(moment, depth_level=2)

    assert len(questions) > 0
    assert all(isinstance(q, str) for q in questions)
    assert any("transform" in q.lower() for q in questions)  # Deep questions


@pytest.mark.asyncio
async def test_guidance_effectiveness_tracking(pattern_facilitator, test_patterns):
    """Test tracking guidance effectiveness"""
    pattern = test_patterns[0]

    # Create guidance
    guidance = PatternGuidance(
        pattern_id=pattern.pattern_id,
        guidance_type=GuidanceType.BREAKTHROUGH,
        intensity=GuidanceIntensity.SUGGESTION,
        content="Test guidance",
        rationale="Test rationale",
        confidence=0.8,
        context_match=0.7,
        timing_score=0.8
    )

    # Add to active guidances
    pattern_facilitator.active_guidances["test_dialogue"] = [guidance]

    # Record effectiveness
    await pattern_facilitator.record_guidance_effectiveness(
        guidance.guidance_id,
        effectiveness=0.9,
        participant_feedback={uuid4(): 0.8}
    )

    # Check it was recorded
    key = (pattern.pattern_id, GuidanceType.BREAKTHROUGH)
    assert key in pattern_facilitator.guidance_effectiveness
    assert 0.9 in pattern_facilitator.guidance_effectiveness[key]


@pytest.mark.asyncio
async def test_wisdom_synthesis_creation(pattern_facilitator, test_patterns):
    """Test creating wisdom synthesis from dialogue"""
    dialogue_id = "test_dialogue"

    # Create some messages
    messages = []
    for i in range(3):
        msg = ConsciousMessage(
            id=uuid4(),
            dialogue_id=dialogue_id,
            sender=uuid4(),
            role=MessageRole.PARTICIPANT,
            type=MessageType.REFLECTION,
            content=f"Test message {i}",
            consciousness=MessageConsciousness(
                consciousness_signature=0.7 + i * 0.1
            )
        )
        messages.append(msg)

    # Add some active guidances
    pattern_facilitator.active_guidances[dialogue_id] = [
        PatternGuidance(
            pattern_id=test_patterns[0].pattern_id,
            guidance_type=GuidanceType.BREAKTHROUGH,
            intensity=GuidanceIntensity.TEACHING,
            content="Test",
            rationale="Test",
            confidence=0.8,
            context_match=0.7,
            timing_score=0.8
        )
    ]

    synthesis = await pattern_facilitator.create_wisdom_synthesis(dialogue_id, messages)

    assert "pattern_teachings" in synthesis
    assert "emergence_moments" in synthesis
    assert "wisdom_seeds" in synthesis
    assert len(synthesis["pattern_teachings"]) > 0


@pytest.mark.asyncio
async def test_guidance_ranking(pattern_facilitator):
    """Test ranking multiple guidances"""
    guidances = [
        PatternGuidance(
            pattern_id=uuid4(),
            guidance_type=GuidanceType.EMERGENCE_CATALYST,
            intensity=GuidanceIntensity.TEACHING,
            content="High confidence",
            rationale="Test",
            confidence=0.9,
            context_match=0.8,
            timing_score=0.8
        ),
        PatternGuidance(
            pattern_id=uuid4(),
            guidance_type=GuidanceType.THEMATIC,
            intensity=GuidanceIntensity.WHISPER,
            content="Low confidence",
            rationale="Test",
            confidence=0.4,
            context_match=0.5,
            timing_score=0.5
        ),
        PatternGuidance(
            pattern_id=uuid4(),
            guidance_type=GuidanceType.TENSION_RESOLUTION,
            intensity=GuidanceIntensity.SUGGESTION,
            content="Medium confidence",
            rationale="Test",
            confidence=0.7,
            context_match=0.7,
            timing_score=0.7
        )
    ]

    moment = DialogueMoment(
        dialogue_id="test",
        current_phase="exploration",
        recent_messages=[],
        active_patterns=[],
        emergence_potential=0.8,  # High emergence
        tension_level=0.3
    )

    ranked = pattern_facilitator._rank_guidances(guidances, moment)

    # High confidence emergence catalyst should rank first
    assert ranked[0].confidence == 0.9
    assert ranked[0].guidance_type == GuidanceType.EMERGENCE_CATALYST


@pytest.mark.asyncio
async def test_pattern_lifecycle_impact_on_teaching(pattern_facilitator, pattern_library):
    """Test how pattern lifecycle affects teaching readiness"""
    # Create patterns in different lifecycle stages
    nascent_pattern = DialoguePattern(
        name="Young Pattern",
        description="Just discovered",
        lifecycle_stage=PatternLifecycle.NASCENT,
        fitness_score=0.7
    )
    await pattern_library.store_pattern(nascent_pattern)

    established_pattern = DialoguePattern(
        name="Mature Pattern",
        description="Well established",
        lifecycle_stage=PatternLifecycle.ESTABLISHED,
        fitness_score=0.7
    )
    await pattern_library.store_pattern(established_pattern)

    dormant_pattern = DialoguePattern(
        name="Old Pattern",
        description="No longer active",
        lifecycle_stage=PatternLifecycle.DORMANT,
        fitness_score=0.7
    )
    await pattern_library.store_pattern(dormant_pattern)

    # Prepare as teachers
    nascent_teacher = await pattern_facilitator._prepare_pattern_teacher(nascent_pattern)
    established_teacher = await pattern_facilitator._prepare_pattern_teacher(established_pattern)
    dormant_teacher = await pattern_facilitator._prepare_pattern_teacher(dormant_pattern)

    # Established should have highest readiness
    assert established_teacher.teaching_readiness > nascent_teacher.teaching_readiness
    assert established_teacher.teaching_readiness > dormant_teacher.teaching_readiness
    assert dormant_teacher.teaching_readiness < 0.3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
