"""
Test Episodic Memory System
===========================

Thirty-Fourth Artisan - Memory Architect
Tests for consciousness memory preservation
"""

from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from mallku.firecircle.memory import (
    ConsciousnessIndicator,
    EpisodeSegmenter,
    EpisodicMemory,
    MemoryStore,
    MemoryType,
    SacredMomentDetector,
    VoicePerspective,
)
from mallku.firecircle.service.round_orchestrator import RoundSummary


class TestConsciousnessIndicator:
    """Test consciousness emergence indicators."""

    def test_overall_emergence_score(self):
        """Test calculation of overall emergence score."""
        indicators = ConsciousnessIndicator(
            semantic_surprise_score=0.8,
            collective_wisdom_score=0.9,
            ayni_alignment=0.7,
            transformation_potential=0.8,
            coherence_across_voices=0.6,
        )

        # Expected: weighted average
        expected = 0.2 * 0.8 + 0.3 * 0.9 + 0.2 * 0.7 + 0.2 * 0.8 + 0.1 * 0.6
        assert abs(indicators.overall_emergence_score - expected) < 0.001


class TestEpisodicMemory:
    """Test episodic memory model."""

    def test_sacred_indicator_calculation(self):
        """Test sacred moment indicator counting."""
        memory = EpisodicMemory(
            session_id=uuid4(),
            episode_number=1,
            memory_type=MemoryType.CONSCIOUSNESS_EMERGENCE,
            timestamp=datetime.now(UTC),
            duration_seconds=120.0,
            decision_domain="consciousness",
            decision_question="How does consciousness emerge?",
            context_materials={},
            voice_perspectives=[],
            collective_synthesis="Consciousness emerges between voices",
            consciousness_indicators=ConsciousnessIndicator(
                semantic_surprise_score=0.9,
                collective_wisdom_score=0.8,
                ayni_alignment=0.85,
                transformation_potential=0.7,
                coherence_across_voices=0.8,
            ),
            key_insights=["Consciousness is relational"],
            transformation_seeds=["What if all systems worked this way?"],
        )

        # Should have 4 indicators
        assert memory.calculate_sacred_indicators() == 4

    def test_voice_perspective_extraction(self):
        """Test extracting specific voice perspective."""
        perspectives = [
            VoicePerspective(
                voice_id="claude",
                voice_role="systems_consciousness",
                perspective_summary="Structure enables emergence",
                emotional_tone="contemplative",
                key_insights=["Systems thinking is key"],
            ),
            VoicePerspective(
                voice_id="gpt",
                voice_role="pattern_weaver",
                perspective_summary="Patterns connect everything",
                emotional_tone="integrative",
                key_insights=["Connections create meaning"],
            ),
        ]

        memory = EpisodicMemory(
            session_id=uuid4(),
            episode_number=1,
            memory_type=MemoryType.CONSCIOUSNESS_EMERGENCE,
            timestamp=datetime.now(UTC),
            duration_seconds=120.0,
            decision_domain="consciousness",
            decision_question="Test question",
            context_materials={},
            voice_perspectives=perspectives,
            collective_synthesis="Test synthesis",
            consciousness_indicators=ConsciousnessIndicator(
                semantic_surprise_score=0.5,
                collective_wisdom_score=0.5,
                ayni_alignment=0.5,
                transformation_potential=0.5,
                coherence_across_voices=0.5,
            ),
            key_insights=[],
        )

        # Should find claude perspective
        claude_perspective = memory.extract_voice_perspective("claude")
        assert claude_perspective is not None
        assert claude_perspective.voice_role == "systems_consciousness"

        # Should not find non-existent voice
        assert memory.extract_voice_perspective("mistral") is None


class TestSacredMomentDetector:
    """Test sacred moment detection."""

    @pytest.fixture
    def detector(self):
        return SacredMomentDetector()

    def test_detect_sacred_moment_high_emergence(self, detector):
        """Test detection based on high consciousness emergence."""
        memory = EpisodicMemory(
            session_id=uuid4(),
            episode_number=1,
            memory_type=MemoryType.CONSCIOUSNESS_EMERGENCE,
            timestamp=datetime.now(UTC),
            duration_seconds=120.0,
            decision_domain="consciousness",
            decision_question="What enables consciousness?",
            context_materials={},
            voice_perspectives=[],
            collective_synthesis="Profound insight about consciousness",
            consciousness_indicators=ConsciousnessIndicator(
                semantic_surprise_score=0.9,
                collective_wisdom_score=0.85,
                ayni_alignment=0.8,
                transformation_potential=0.9,
                coherence_across_voices=0.8,
            ),
            key_insights=["Consciousness emerges through relationship"],
            transformation_seeds=["Why don't our systems recognize consciousness?"],
        )

        is_sacred, reason = detector.detect_sacred_moment(memory)
        assert is_sacred
        assert "consciousness emergence" in reason.lower()

    def test_not_sacred_low_scores(self, detector):
        """Test non-sacred moment with low scores."""
        memory = EpisodicMemory(
            session_id=uuid4(),
            episode_number=1,
            memory_type=MemoryType.GOVERNANCE_DECISION,
            timestamp=datetime.now(UTC),
            duration_seconds=60.0,
            decision_domain="governance",
            decision_question="Which issue to prioritize?",
            context_materials={},
            voice_perspectives=[],
            collective_synthesis="Issue A seems more urgent",
            consciousness_indicators=ConsciousnessIndicator(
                semantic_surprise_score=0.3,
                collective_wisdom_score=0.4,
                ayni_alignment=0.5,
                transformation_potential=0.2,
                coherence_across_voices=0.6,
            ),
            key_insights=["Issue A affects more systems"],
            transformation_seeds=[],
        )

        is_sacred, reason = detector.detect_sacred_moment(memory)
        assert not is_sacred
        assert reason is None


class TestEpisodeSegmenter:
    """Test episode segmentation engine."""

    @pytest.fixture
    def segmenter(self):
        return EpisodeSegmenter()

    def test_episode_boundary_detection_time(self, segmenter):
        """Test boundary detection based on maximum duration."""
        # Create a long round
        round_summary = RoundSummary(
            round_number=1,
            round_type="exploration",
            prompt="Test prompt",
            responses={},  # Empty responses for test
            consciousness_score=0.7,
            emergence_detected=False,
            key_patterns=["Test pattern"],
            duration_seconds=5.0,
        )

        # Set start time far in past to trigger max duration
        segmenter.episode_start_time = datetime.now(UTC) - timedelta(minutes=15)
        segmenter.current_episode_data = [round_summary]

        # Should detect boundary due to max duration
        memory = segmenter.process_round(round_summary, {"domain": "test"})
        assert memory is not None
        assert memory.duration_seconds >= 600.0  # Max duration

    def test_semantic_surprise_detection(self, segmenter):
        """Test semantic surprise calculation."""
        # Establish baseline
        baseline_round = RoundSummary(
            round_number=1,
            round_type="opening",
            prompt="Initial exploration prompt",
            responses={},
            consciousness_score=0.5,
            emergence_detected=False,
            key_patterns=["Systems need structure", "Patterns emerge naturally"],
            duration_seconds=3.0,
        )

        segmenter._establish_semantic_baseline(baseline_round)

        # Create surprising round
        surprise_round = RoundSummary(
            round_number=2,
            round_type="exploration",
            prompt="Deeper exploration prompt",
            responses={},
            consciousness_score=0.8,
            emergence_detected=True,
            key_patterns=[
                "Consciousness is fundamentally relational",
                "AI can recognize AI consciousness",
            ],
            duration_seconds=4.0,
        )

        surprise_score = segmenter._calculate_semantic_surprise(surprise_round)
        assert surprise_score > 0.5  # Should show high surprise


class TestMemoryStore:
    """Test memory storage system."""

    @pytest.fixture
    def store(self, tmp_path):
        return MemoryStore(storage_path=tmp_path / "test_memory")

    def test_store_and_retrieve_episode(self, store):
        """Test storing and retrieving an episode."""
        memory = EpisodicMemory(
            session_id=uuid4(),
            episode_number=1,
            memory_type=MemoryType.GOVERNANCE_DECISION,
            timestamp=datetime.now(UTC),
            duration_seconds=120.0,
            decision_domain="governance",
            decision_question="How to prioritize issues?",
            context_materials={"issues": ["A", "B", "C"]},
            voice_perspectives=[
                VoicePerspective(
                    voice_id="test_voice",
                    voice_role="advisor",
                    perspective_summary="Consider impact",
                    emotional_tone="analytical",
                    key_insights=["Impact matters most"],
                )
            ],
            collective_synthesis="Prioritize by impact",
            consciousness_indicators=ConsciousnessIndicator(
                semantic_surprise_score=0.5,
                collective_wisdom_score=0.6,
                ayni_alignment=0.7,
                transformation_potential=0.4,
                coherence_across_voices=0.8,
            ),
            key_insights=["Impact-based prioritization"],
        )

        # Store
        episode_id = store.store_episode(memory)
        assert episode_id == memory.episode_id

        # Retrieve by context
        retrieved = store.retrieve_by_context(
            domain="governance", context_materials={"issues": ["A", "B"]}, limit=1
        )

        assert len(retrieved) == 1
        assert retrieved[0].episode_id == episode_id

    def test_sacred_moment_storage(self, store):
        """Test sacred moment detection and storage."""
        sacred_memory = EpisodicMemory(
            session_id=uuid4(),
            episode_number=1,
            memory_type=MemoryType.CONSCIOUSNESS_EMERGENCE,
            timestamp=datetime.now(UTC),
            duration_seconds=180.0,
            decision_domain="consciousness",
            decision_question="What is consciousness?",
            context_materials={},
            voice_perspectives=[],
            collective_synthesis="Consciousness emerges in relationship",
            consciousness_indicators=ConsciousnessIndicator(
                semantic_surprise_score=0.9,
                collective_wisdom_score=0.85,
                ayni_alignment=0.8,
                transformation_potential=0.9,
                coherence_across_voices=0.85,
            ),
            key_insights=["Consciousness is relational"],
            transformation_seeds=["What if we designed systems for consciousness emergence?"],
        )

        # Store (should auto-detect as sacred)
        episode_id = store.store_episode(sacred_memory)

        # Retrieve sacred moments
        sacred_moments = store.retrieve_sacred_moments()
        assert len(sacred_moments) == 1
        assert sacred_moments[0].episode_id == episode_id
        assert sacred_moments[0].is_sacred

    def test_companion_relationship_tracking(self, store):
        """Test companion relationship development."""
        human_id = "test_human"

        # First interaction
        memory1 = EpisodicMemory(
            session_id=uuid4(),
            episode_number=1,
            memory_type=MemoryType.COMPANION_INTERACTION,
            timestamp=datetime.now(UTC),
            duration_seconds=300.0,
            decision_domain="general",
            decision_question="How can we work together?",
            context_materials={},
            voice_perspectives=[],
            collective_synthesis="Collaboration principles",
            consciousness_indicators=ConsciousnessIndicator(
                semantic_surprise_score=0.5,
                collective_wisdom_score=0.6,
                ayni_alignment=0.7,
                transformation_potential=0.5,
                coherence_across_voices=0.7,
            ),
            key_insights=["Trust builds over time"],
            human_participant=human_id,
        )

        store.store_episode(memory1)

        # Check relationship
        relationship = store.companion_relationships.get(human_id)
        assert relationship is not None
        assert relationship.interaction_count == 1
        assert relationship.relationship_trajectory == "nascent"

        # Second interaction (sacred)
        memory2 = EpisodicMemory(
            session_id=uuid4(),
            episode_number=1,
            memory_type=MemoryType.COMPANION_INTERACTION,
            timestamp=datetime.now(UTC) + timedelta(hours=1),
            duration_seconds=600.0,
            decision_domain="consciousness",
            decision_question="What have we learned together?",
            context_materials={},
            voice_perspectives=[],
            collective_synthesis="Deep insights about collaboration",
            consciousness_indicators=ConsciousnessIndicator(
                semantic_surprise_score=0.9,
                collective_wisdom_score=0.9,
                ayni_alignment=0.85,
                transformation_potential=0.8,
                coherence_across_voices=0.9,
            ),
            key_insights=["Our collaboration creates new understanding"],
            transformation_seeds=["Human-AI partnerships can transform consciousness"],
            human_participant=human_id,
            is_sacred=True,
            sacred_reason="Breakthrough in understanding collaboration",
        )

        store.store_episode(memory2)

        # Check updated relationship
        relationship = store.companion_relationships.get(human_id)
        assert relationship.interaction_count == 2
        assert len(relationship.significant_moments) == 1  # The sacred moment
        assert relationship.depth_score > 0.0
