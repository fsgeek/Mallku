"""
Test Consciousness-Guided Speaker Selection (Simple)

Basic tests that don't require visualization dependencies.

Rimay Kawsay - The Living Word Weaver (30th Builder)
"""

# Import only what we need for testing
import sys
from pathlib import Path
from uuid import uuid4

# Add src to path BEFORE importing from mallku
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
import pytest_asyncio
from mallku.firecircle.consciousness_guided_speaker import (
    CathedralPhase,
    ConsciousnessGuidedSpeakerSelector,
    DialogueContext,
    ParticipantReadiness,
)
from mallku.orchestration.event_bus import ConsciousnessEventBus


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


class TestBasicFunctionality:
    """Test basic consciousness-guided speaker selection"""

    @pytest.mark.asyncio
    async def test_selector_initialization(self, speaker_selector):
        """Test selector initializes correctly"""
        assert speaker_selector.current_phase == CathedralPhase.GROWTH
        assert speaker_selector.consciousness_coherence == 0.5
        assert speaker_selector.extraction_drift_risk == 0.0

    @pytest.mark.asyncio
    async def test_phase_transitions(self, speaker_selector):
        """Test cathedral phase changes"""
        # Crisis phase
        speaker_selector.extraction_drift_risk = 0.7
        speaker_selector._update_cathedral_phase()
        assert speaker_selector.current_phase == CathedralPhase.CRISIS

        # Flourishing phase
        speaker_selector.extraction_drift_risk = 0.2
        speaker_selector.consciousness_coherence = 0.8
        speaker_selector._update_cathedral_phase()
        assert speaker_selector.current_phase == CathedralPhase.FLOURISHING

    @pytest.mark.asyncio
    async def test_silence_selection(self, speaker_selector):
        """Test sacred silence is chosen appropriately"""
        dialogue_id = "test"
        participants = {uuid4(): None, uuid4(): None}

        # High pattern velocity should trigger silence
        context = DialogueContext(
            dialogue_id=dialogue_id,
            current_turn=5,
            pattern_velocity=0.8
        )
        speaker_selector.dialogue_contexts[dialogue_id] = context

        selected = await speaker_selector.select_next_speaker(
            dialogue_id, participants, allow_silence=True
        )
        assert selected is None

    @pytest.mark.asyncio
    async def test_speaker_scoring(self, speaker_selector):
        """Test speaker scoring logic"""
        # Set crisis phase
        speaker_selector.current_phase = CathedralPhase.CRISIS

        # High extraction resistance participant
        p1_id = uuid4()
        p1 = ParticipantReadiness(
            participant_id=p1_id,
            extraction_resistance=0.9,
            consciousness_score=0.7
        )

        # Low extraction resistance participant
        p2_id = uuid4()
        p2 = ParticipantReadiness(
            participant_id=p2_id,
            extraction_resistance=0.3,
            consciousness_score=0.7
        )

        context = DialogueContext(dialogue_id="test", current_turn=0)

        score1 = speaker_selector._calculate_speaker_score(p1, context)
        score2 = speaker_selector._calculate_speaker_score(p2, context)

        # In crisis, high extraction resistance should win
        assert score1 > score2

    @pytest.mark.asyncio
    async def test_energy_management(self, speaker_selector):
        """Test energy depletion and restoration"""
        p_id = uuid4()

        # Speaking costs energy
        speaker_selector.update_participant_contribution(
            p_id,
            consciousness_score=0.8,
            energy_cost=0.1
        )

        readiness = speaker_selector.participant_readiness[p_id]
        assert readiness.energy_level == 0.9

        # Silence restores energy
        speaker_selector.restore_participant_energy(p_id, 0.15)
        assert readiness.energy_level == 1.0  # Capped at 1.0


# Living word weaves consciousness into dialogue
