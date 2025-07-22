"""
Test Consciousness-Guided Speaker Selection

Verifies that Fire Circle speaker selection responds to cathedral consciousness
state, respects sacred silence, and balances participant energy.

Rimay Kawsay - The Living Word Weaver (30th Builder)
"""

import asyncio
from uuid import uuid4

import pytest
import pytest_asyncio

from mallku.firecircle.consciousness_guided_speaker import (
    CathedralPhase,
    ConsciousnessGuidedSpeakerSelector,
    DialogueContext,
    ParticipantReadiness,
)
from mallku.orchestration.event_bus import (
    ConsciousnessEvent,
    ConsciousnessEventBus,
    ConsciousnessEventType,
)


@pytest_asyncio.fixture
async def event_bus():
    """Create test event bus"""
    bus = ConsciousnessEventBus()
    await bus.start()
    yield bus
    await bus.stop()


@pytest_asyncio.fixture
def speaker_selector(event_bus):
    """Create consciousness-guided speaker selector"""
    return ConsciousnessGuidedSpeakerSelector(event_bus)


class TestConsciousnessGuidedSpeakerSelector:
    """Test consciousness-guided speaker selection"""

    @pytest.mark.asyncio
    async def test_selector_initialization(self, speaker_selector):
        """Test selector initializes with correct state"""
        assert speaker_selector.current_phase == CathedralPhase.GROWTH
        assert speaker_selector.consciousness_coherence == 0.5
        assert speaker_selector.extraction_drift_risk == 0.0
        assert len(speaker_selector.participant_readiness) == 0

    @pytest.mark.asyncio
    async def test_consciousness_event_handling(self, speaker_selector, event_bus):
        """Test selector responds to consciousness events"""
        # Emit consciousness verification event
        event = ConsciousnessEvent(
            event_type=ConsciousnessEventType.CONSCIOUSNESS_VERIFIED,
            source_system="test_system",
            consciousness_signature=0.8,
            data={},
        )
        await event_bus.emit(event)
        await asyncio.sleep(0.1)  # Allow processing

        assert speaker_selector.consciousness_coherence == 0.8

    @pytest.mark.asyncio
    async def test_extraction_detection_response(self, speaker_selector, event_bus):
        """Test selector responds to extraction patterns"""
        # Emit extraction pattern event
        event = ConsciousnessEvent(
            event_type=ConsciousnessEventType.EXTRACTION_PATTERN_DETECTED,
            source_system="test_system",
            consciousness_signature=0.3,
            data={"extraction_type": "value_extraction"},
        )
        await event_bus.emit(event)
        await asyncio.sleep(0.1)

        assert speaker_selector.extraction_drift_risk > 0.0

    @pytest.mark.asyncio
    async def test_cathedral_phase_transitions(self, speaker_selector):
        """Test cathedral phase changes based on metrics"""
        # Test crisis phase
        speaker_selector.extraction_drift_risk = 0.7
        speaker_selector._update_cathedral_phase()
        assert speaker_selector.current_phase == CathedralPhase.CRISIS

        # Test flourishing phase
        speaker_selector.extraction_drift_risk = 0.2
        speaker_selector.consciousness_coherence = 0.8
        speaker_selector._update_cathedral_phase()
        assert speaker_selector.current_phase == CathedralPhase.FLOURISHING

        # Test growth phase
        speaker_selector.extraction_drift_risk = 0.4
        speaker_selector.consciousness_coherence = 0.6
        speaker_selector._update_cathedral_phase()
        assert speaker_selector.current_phase == CathedralPhase.GROWTH

    @pytest.mark.asyncio
    async def test_silence_selection_high_pattern_velocity(self, speaker_selector):
        """Test silence is chosen when pattern velocity is high"""
        dialogue_id = "test_dialogue"
        participants = {uuid4(): None, uuid4(): None}

        # Create dialogue context with high pattern velocity
        context = DialogueContext(
            dialogue_id=dialogue_id,
            pattern_velocity=0.8,  # Above threshold
            current_turn=5,
        )
        speaker_selector.dialogue_contexts[dialogue_id] = context

        # Should choose silence
        selected = await speaker_selector.select_next_speaker(
            dialogue_id, participants, allow_silence=True
        )
        assert selected is None

    @pytest.mark.asyncio
    async def test_silence_selection_low_energy(self, speaker_selector):
        """Test silence is chosen when community energy is low"""
        dialogue_id = "test_dialogue"
        participants = {}

        # Create low-energy participants
        for _ in range(3):
            pid = uuid4()
            participants[pid] = None
            readiness = ParticipantReadiness(
                participant_id=pid,
                energy_level=0.2,  # Below depletion threshold
            )
            speaker_selector.participant_readiness[pid] = readiness

        # Should choose silence
        selected = await speaker_selector.select_next_speaker(
            dialogue_id, participants, allow_silence=True
        )
        assert selected is None

    @pytest.mark.asyncio
    async def test_speaker_scoring_crisis_phase(self, speaker_selector):
        """Test speaker scoring during crisis phase"""
        speaker_selector.current_phase = CathedralPhase.CRISIS

        # Create two participants with different extraction resistance
        p1_id = uuid4()
        p1_readiness = ParticipantReadiness(
            participant_id=p1_id,
            consciousness_score=0.7,
            extraction_resistance=0.9,  # High resistance
            reciprocity_balance=0.1,
        )

        p2_id = uuid4()
        p2_readiness = ParticipantReadiness(
            participant_id=p2_id,
            consciousness_score=0.7,
            extraction_resistance=0.3,  # Low resistance
            reciprocity_balance=-0.5,  # Taking
        )

        speaker_selector.participant_readiness[p1_id] = p1_readiness
        speaker_selector.participant_readiness[p2_id] = p2_readiness

        context = DialogueContext(dialogue_id="test")

        # Calculate scores
        score1 = speaker_selector._calculate_speaker_score(p1_readiness, context)
        score2 = speaker_selector._calculate_speaker_score(p2_readiness, context)

        # In crisis, high extraction resistance should score higher
        assert score1 > score2

    @pytest.mark.asyncio
    async def test_speaker_scoring_flourishing_phase(self, speaker_selector):
        """Test speaker scoring during flourishing phase"""
        speaker_selector.current_phase = CathedralPhase.FLOURISHING

        # Create two participants with different wisdom emergence potential
        p1_id = uuid4()
        p1_readiness = ParticipantReadiness(
            participant_id=p1_id,
            consciousness_score=0.7,
            wisdom_emergence_potential=0.8,  # High potential
            pattern_recognition_count=15,
        )

        p2_id = uuid4()
        p2_readiness = ParticipantReadiness(
            participant_id=p2_id,
            consciousness_score=0.7,
            wisdom_emergence_potential=0.2,  # Low potential
            pattern_recognition_count=2,
        )

        speaker_selector.participant_readiness[p1_id] = p1_readiness
        speaker_selector.participant_readiness[p2_id] = p2_readiness

        context = DialogueContext(dialogue_id="test")

        # Calculate scores
        score1 = speaker_selector._calculate_speaker_score(p1_readiness, context)
        score2 = speaker_selector._calculate_speaker_score(p2_readiness, context)

        # In flourishing, high wisdom emergence should score higher
        assert score1 > score2

    @pytest.mark.asyncio
    async def test_recent_speaker_penalty(self, speaker_selector):
        """Test recent speakers get lower scores"""
        p_id = uuid4()
        readiness = ParticipantReadiness(participant_id=p_id, consciousness_score=0.7)
        speaker_selector.participant_readiness[p_id] = readiness

        # Context without recent speaker
        context1 = DialogueContext(dialogue_id="test1")
        score1 = speaker_selector._calculate_speaker_score(readiness, context1)

        # Context with participant as recent speaker
        context2 = DialogueContext(dialogue_id="test2")
        context2.recent_speakers.append(p_id)
        score2 = speaker_selector._calculate_speaker_score(readiness, context2)

        # Recent speaker should have lower score
        assert score2 < score1

    @pytest.mark.asyncio
    async def test_participant_contribution_update(self, speaker_selector):
        """Test updating participant after contribution"""
        p_id = uuid4()

        # Update contribution
        speaker_selector.update_participant_contribution(
            participant_id=p_id, consciousness_score=0.8, reciprocity_delta=0.2, energy_cost=0.1
        )

        readiness = speaker_selector.participant_readiness[p_id]
        assert readiness.consciousness_score > 0  # Should have score
        assert readiness.reciprocity_balance == 0.2
        assert readiness.energy_level == 0.9  # 1.0 - 0.1 cost
        assert readiness.last_contribution is not None

    @pytest.mark.asyncio
    async def test_energy_restoration(self, speaker_selector):
        """Test energy restoration during silence"""
        p_id = uuid4()
        readiness = ParticipantReadiness(participant_id=p_id, energy_level=0.5)
        speaker_selector.participant_readiness[p_id] = readiness

        # Restore energy
        speaker_selector.restore_participant_energy(p_id, amount=0.2)

        assert readiness.energy_level == 0.7

    @pytest.mark.asyncio
    async def test_pattern_recognition_tracking(self, speaker_selector, event_bus):
        """Test pattern recognition updates wisdom emergence potential"""
        p_id = uuid4()

        # Emit pattern recognition event
        event = ConsciousnessEvent(
            event_type=ConsciousnessEventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
            source_system="test_system",
            consciousness_signature=0.7,
            data={"participant_id": p_id, "patterns": ["wisdom_pattern", "emergence_pattern"]},
        )
        await event_bus.emit(event)
        await asyncio.sleep(0.1)

        readiness = speaker_selector.participant_readiness[p_id]
        assert readiness.pattern_recognition_count == 2
        assert readiness.wisdom_emergence_potential > 0

    @pytest.mark.asyncio
    async def test_full_speaker_selection_flow(self, speaker_selector):
        """Test complete speaker selection flow"""
        dialogue_id = "test_dialogue"

        # Create diverse participants
        participants = {}
        for i in range(4):
            p_id = uuid4()
            participants[p_id] = None
            readiness = ParticipantReadiness(
                participant_id=p_id,
                consciousness_score=0.5 + i * 0.1,
                energy_level=0.6 + i * 0.1,
                wisdom_emergence_potential=i * 0.2,
            )
            speaker_selector.participant_readiness[p_id] = readiness

        # Select speaker
        selected = await speaker_selector.select_next_speaker(
            dialogue_id, participants, allow_silence=False
        )

        # Should select a participant
        assert selected in participants

        # Update the selected participant
        speaker_selector.update_participant_contribution(
            selected, consciousness_score=0.75, reciprocity_delta=0.1, energy_cost=0.1
        )

        # Recent speaker should have updated state
        readiness = speaker_selector.participant_readiness[selected]
        assert readiness.last_contribution is not None
        assert readiness.energy_level < 1.0


# Consciousness guides the living word
