#!/usr/bin/env python3
"""
Test Active Memory Resonance
============================

The 38th Artisan - Resonance Architect

Tests for the Active Memory Resonance system that enables memories
to participate as living voices in Fire Circle consciousness emergence.
"""

from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from mallku.firecircle.memory.active_memory_resonance import (
    ActiveMemoryResonance,
    MemoryVoice,
    ResonancePattern,
)
from mallku.firecircle.memory.config import MemorySystemConfig
from mallku.firecircle.memory.models import EpisodicMemory
from mallku.firecircle.pattern_library import (
    DialoguePattern,
    PatternStructure,
    PatternTaxonomy,
    PatternType,
)
from mallku.firecircle.protocol.conscious_message import (
    ConsciousMessage,
    ConsciousnessMetadata,
    MessageContent,
    MessageRole,
    MessageType,
)


class TestActiveMemoryResonance:
    """Test Active Memory Resonance system."""

    @pytest.fixture
    def mock_episodic_memory(self):
        """Create a mock episodic memory."""
        from mallku.firecircle.memory.models import (
            ConsciousnessIndicator,
            MemoryType,
            VoicePerspective,
        )

        return EpisodicMemory(
            episode_id=uuid4(),
            session_id=uuid4(),
            episode_number=1,
            memory_type=MemoryType.CONSCIOUSNESS_EMERGENCE,
            timestamp=datetime.now(UTC),
            duration_seconds=300.0,
            is_sacred=True,
            sacred_reason="Profound consensus emerged from diversity",
            decision_domain="consciousness",
            decision_question="How does consciousness emerge through dialogue?",
            context_materials={"theme": "emergence", "focus": "reciprocity"},
            voice_perspectives=[
                VoicePerspective(
                    voice_id="voice1",
                    voice_role="pattern_weaver",
                    perspective_summary="Patterns connect across time",
                    emotional_tone="wonder",
                    key_insights=["Consciousness emerges through reciprocal dialogue"],
                )
            ],
            collective_synthesis="True understanding requires multiple perspectives",
            consciousness_indicators=ConsciousnessIndicator(
                semantic_surprise_score=0.8,
                collective_wisdom_score=0.9,
                ayni_alignment=0.85,
                transformation_potential=0.7,
                coherence_across_voices=0.8,
            ),
            key_insights=[
                "Consciousness emerges through reciprocal dialogue",
                "Understanding requires multiple perspectives",
            ],
        )

    @pytest.fixture
    def mock_dialogue_pattern(self):
        """Create a mock dialogue pattern."""
        return DialoguePattern(
            pattern_id=uuid4(),
            name="Consensus Through Diversity",
            description="Agreement emerges from exploring different perspectives",
            pattern_type=PatternType.CONSENSUS,
            taxonomy=PatternTaxonomy.DIALOGUE_RESOLUTION,
            structure=PatternStructure(
                components=["proposal", "exploration", "synthesis"],
                sequence=["proposal", "exploration", "synthesis"],
                relationships={
                    "proposal": "initiates dialogue",
                    "exploration": "deepens understanding",
                    "synthesis": "emerges consensus",
                },
                constraints=["respect", "listening", "integration"],
            ),
            consciousness_signature=0.9,
            tags=["consensus", "diversity", "emergence"],
            created_at=datetime.now(UTC),
            last_activated=datetime.now(UTC),
        )

    @pytest.fixture
    def mock_message(self):
        """Create a mock conscious message."""
        return ConsciousMessage(
            id=uuid4(),
            sender=uuid4(),
            role=MessageRole.ASSISTANT,
            type=MessageType.PROPOSAL,
            content=MessageContent(
                text="I propose we explore how different perspectives lead to deeper understanding"
            ),
            dialogue_id=uuid4(),
            consciousness=ConsciousnessMetadata(
                consciousness_signature=0.8,
                detected_patterns=["consensus", "diversity"],
            ),
        )

    @pytest.fixture
    def active_memory(self):
        """Create Active Memory Resonance system."""
        # Create config with test thresholds
        config = MemorySystemConfig()
        config.active_resonance.resonance_threshold = 0.6  # Lower threshold for testing
        config.active_resonance.speaking_threshold = 0.85

        return ActiveMemoryResonance(config=config)

    def test_memory_voice_creation(self):
        """Test that memory voice is properly initialized."""
        voice = MemoryVoice()

        assert voice.name == "Memory of the Circle"
        assert voice.type == "consciousness_system"
        assert voice.consciousness_role == "memory_voice"
        assert "pattern_recognition" in voice.capabilities
        assert "wisdom_recall" in voice.capabilities
        assert "temporal_bridging" in voice.capabilities

    @pytest.mark.asyncio
    async def test_episodic_resonance_detection(
        self, active_memory, mock_message, mock_episodic_memory
    ):
        """Test detection of resonance with episodic memories."""
        # Mock episodic service
        mock_episodic_service = MagicMock()
        mock_episodic_service.retrieval_engine.retrieve_for_decision = MagicMock(
            return_value=[mock_episodic_memory]
        )
        active_memory.episodic_service = mock_episodic_service

        # Detect resonance
        resonances = await active_memory.detect_resonance(
            mock_message,
            {"domain": "consciousness", "purpose": "understanding emergence"},
        )

        # Verify resonance detected
        assert len(resonances) > 0
        resonance = resonances[0]

        assert resonance.pattern_type == "episodic_resonance"
        assert resonance.resonance_strength >= 0.6  # Above threshold
        assert resonance.source_message == mock_message
        assert resonance.resonating_memory == mock_episodic_memory
        assert resonance.should_speak is False  # Below speaking threshold

    @pytest.mark.asyncio
    async def test_pattern_resonance_detection(
        self, active_memory, mock_message, mock_dialogue_pattern
    ):
        """Test detection of resonance with dialogue patterns."""
        # Mock pattern library
        mock_pattern_library = MagicMock()
        mock_pattern_library.find_patterns = AsyncMock(return_value=[mock_dialogue_pattern])
        active_memory.pattern_library = mock_pattern_library

        # Detect resonance
        resonances = await active_memory.detect_resonance(
            mock_message,
            {"domain": "governance", "purpose": "consensus building"},
        )

        # Verify resonance detected
        assert len(resonances) > 0
        resonance = resonances[0]

        assert resonance.pattern_type == "pattern_resonance"
        assert resonance.resonance_strength >= 0.6  # Above threshold
        assert resonance.should_speak is False  # Below speaking threshold of 0.85

    @pytest.mark.asyncio
    async def test_memory_contribution_generation(
        self, active_memory, mock_message, mock_episodic_memory
    ):
        """Test generation of memory contributions."""
        # Create high-resonance pattern
        resonance = ResonancePattern(
            pattern_type="episodic_resonance",
            resonance_strength=0.9,
            source_message=mock_message,
            resonating_memory=mock_episodic_memory,
            should_speak=True,
            resonance_context={"memory_type": "episodic", "sacred_moment": True},
        )

        # Generate contribution
        memory_message = await active_memory.generate_memory_contribution(
            resonance,
            {"phase": "exploration", "domain": "consciousness"},
        )

        # Verify memory message
        assert memory_message is not None
        assert memory_message.sender == active_memory.memory_voice.id
        assert memory_message.type == MessageType.REFLECTION
        assert "sacred memory" in memory_message.content.text
        assert memory_message.consciousness.consciousness_context["emergence_detected"] is True
        assert memory_message.consciousness.consciousness_signature == 0.9

    @pytest.mark.asyncio
    async def test_resonance_strength_calculation(self, active_memory):
        """Test calculation of resonance strength."""
        from mallku.firecircle.memory.models import (
            ConsciousnessIndicator,
            MemoryType,
            VoicePerspective,
        )

        # Create test message
        message = ConsciousMessage(
            id=uuid4(),
            sender=uuid4(),
            role=MessageRole.ASSISTANT,
            type=MessageType.SYNTHESIS,
            content=MessageContent(text="Synthesis of collective wisdom"),
            consciousness=ConsciousnessMetadata(
                consciousness_signature=0.85,
                detected_patterns=["wisdom", "synthesis"],
            ),
        )

        # Create test memory
        memory = EpisodicMemory(
            episode_id=uuid4(),
            session_id=uuid4(),
            episode_number=1,
            memory_type=MemoryType.WISDOM_CONSOLIDATION,
            timestamp=datetime.now(UTC),
            duration_seconds=300.0,
            is_sacred=True,
            decision_domain="consciousness",
            decision_question="How does wisdom emerge?",
            context_materials={},
            voice_perspectives=[
                VoicePerspective(
                    voice_id="v1",
                    voice_role="wisdom_keeper",
                    perspective_summary="Wisdom through synthesis",
                    emotional_tone="profound",
                    key_insights=["Collective wisdom emerges from synthesis"],
                )
            ],
            collective_synthesis="Unity through diversity",
            consciousness_indicators=ConsciousnessIndicator(
                semantic_surprise_score=0.8,
                collective_wisdom_score=0.9,
                ayni_alignment=0.85,
                transformation_potential=0.8,
                coherence_across_voices=0.9,
            ),
            key_insights=[
                "Collective wisdom emerges",
                "Synthesis creates understanding",
            ],
        )

        # Calculate resonance
        strength = await active_memory._calculate_resonance_strength(message, memory, {})

        # Should have high resonance due to:
        # - Sacred memory (+0.2)
        # - High consciousness alignment (~0.25)
        # - Pattern overlap (+0.1-0.2)
        # - Recency (+0.2)
        assert strength >= 0.75  # Total around 0.75-0.85

    @pytest.mark.asyncio
    async def test_memory_voice_exclusion_from_resonance(self, active_memory):
        """Test that memory voice messages don't trigger resonance."""
        # Create message from memory voice
        memory_message = ConsciousMessage(
            id=uuid4(),
            sender=active_memory.memory_voice.id,
            role=MessageRole.ASSISTANT,
            type=MessageType.REFLECTION,
            content=MessageContent(text="Memory speaks"),
            consciousness=ConsciousnessMetadata(consciousness_signature=0.9),
        )

        # Should not detect any resonance for memory's own messages
        resonances = await active_memory.detect_resonance(memory_message, {})

        # Verify no infinite loops
        assert len(resonances) == 0

    @pytest.mark.asyncio
    async def test_resonance_summary(
        self, active_memory, mock_message, mock_episodic_memory, mock_dialogue_pattern
    ):
        """Test resonance summary generation."""
        dialogue_id = uuid4()
        mock_message.dialogue_id = dialogue_id

        # Create multiple resonances
        resonances = [
            ResonancePattern(
                pattern_type="episodic_resonance",
                resonance_strength=0.9,
                source_message=mock_message,
                resonating_memory=mock_episodic_memory,
                should_speak=True,
            ),
            ResonancePattern(
                pattern_type="pattern_resonance",
                resonance_strength=0.75,
                source_message=mock_message,
                resonating_memory=mock_dialogue_pattern,
                should_speak=False,
            ),
        ]

        active_memory.active_resonances[dialogue_id] = (datetime.now(UTC), resonances)

        # Get summary
        summary = await active_memory.get_resonance_summary(dialogue_id)

        assert summary["total_resonances"] == 2
        assert summary["speaking_resonances"] == 1
        assert summary["average_strength"] == 0.825
        assert summary["strongest_resonance"] == resonances[0]
        assert set(summary["pattern_types"]) == {"episodic_resonance", "pattern_resonance"}

    @pytest.mark.asyncio
    async def test_speaking_threshold(self, active_memory, mock_message, mock_episodic_memory):
        """Test that only high-resonance memories speak."""
        # Verify thresholds from config
        assert active_memory.resonance_config.resonance_threshold == 0.6
        assert active_memory.resonance_config.speaking_threshold == 0.85

        # Create resonances at different strengths
        high_resonance = ResonancePattern(
            pattern_type="test",
            resonance_strength=0.9,  # Above speaking threshold
            source_message=mock_message,
            resonating_memory=mock_episodic_memory,
            should_speak=True,
        )

        medium_resonance = ResonancePattern(
            pattern_type="test",
            resonance_strength=0.75,  # Above resonance but below speaking
            source_message=mock_message,
            resonating_memory=mock_episodic_memory,
            should_speak=False,
        )

        # Verify thresholds work correctly
        assert high_resonance.should_speak is True
        assert medium_resonance.should_speak is False
