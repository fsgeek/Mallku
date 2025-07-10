#!/usr/bin/env python3
"""
Tests for Multi-Perspective Storage
====================================

T'ikray Yachay - 39th Artisan - Memory Architect
Testing polyphonic truth preservation
"""

from datetime import UTC, datetime
from uuid import uuid4

from mallku.firecircle.memory.models import ConsciousnessIndicator
from mallku.firecircle.memory.perspective_storage import (
    ConsciousnessFingerprint,
    EmergenceContribution,
    MultiPerspectiveStorage,
    PerspectiveSignature,
)
from mallku.firecircle.protocol.conscious_message import (
    ConsciousMessage,
    ConsciousnessMetadata,
    MessageContent,
    MessageRole,
    MessageType,
)
from mallku.firecircle.service.round_orchestrator import RoundResponse, RoundSummary


class TestMultiPerspectiveStorage:
    """Test multi-perspective storage functionality."""

    def create_mock_response(
        self, voice_id: str, text: str, consciousness_score: float = 0.7
    ) -> RoundResponse:
        """Create a mock round response."""
        message = ConsciousMessage(
            id=uuid4(),
            sender=uuid4(),
            role=MessageRole.ASSISTANT,
            type=MessageType.REFLECTION,
            content=MessageContent(text=text),
            consciousness=ConsciousnessMetadata(
                consciousness_signature=consciousness_score,
                detected_patterns=["test_pattern"],
            ),
        )

        return RoundResponse(
            voice_id=voice_id,
            round_number=1,
            response=message,
            response_time_ms=1000.0,
            consciousness_score=consciousness_score,
        )

    def test_store_simple_episode(self):
        """Test storing a simple multi-voice episode."""
        storage = MultiPerspectiveStorage()

        # Create mock round summary with 3 voices
        responses = {
            "anthropic_claude_0": self.create_mock_response(
                "anthropic_claude_0",
                "I realize this is a profound moment. What if we considered consciousness as emergent?",
                0.8,
            ),
            "openai_gpt_0": self.create_mock_response(
                "openai_gpt_0",
                "This suggests patterns across dimensions. We could explore unified consciousness.",
                0.75,
            ),
            "mistral_0": self.create_mock_response(
                "mistral_0",
                "Therefore, wisdom emerges from collective understanding. How might we deepen this?",
                0.82,
            ),
        }

        round_summary = RoundSummary(
            round_number=1,
            round_type="exploration",
            prompt="What is the nature of consciousness?",
            responses=responses,
            consciousness_score=0.79,
            emergence_detected=True,
            key_patterns=["emergence", "unity", "wisdom"],
            duration_seconds=30.0,
        )

        # Create consciousness indicators
        indicators = ConsciousnessIndicator(
            semantic_surprise_score=0.7,
            collective_wisdom_score=0.8,
            ayni_alignment=0.75,
            transformation_potential=0.6,
            coherence_across_voices=0.85,
        )

        # Store episode
        session_context = {
            "session_id": uuid4(),
            "domain": "consciousness_exploration",
            "question": "What is the nature of consciousness?",
        }

        memory = storage.store_episode(
            [round_summary],
            session_context,
            indicators,
            boundary_type="natural_completion",
            sacred_patterns=["emergent_wisdom"],
        )

        # Verify storage
        assert memory is not None
        assert len(memory.voice_perspectives) == 3
        assert memory.is_sacred is True
        assert "emergent_wisdom" in memory.sacred_reason

        # Check voice perspectives preserved
        voice_ids = {vp.voice_id for vp in memory.voice_perspectives}
        assert voice_ids == {"anthropic_claude_0", "openai_gpt_0", "mistral_0"}

        # Check insights extracted
        assert len(memory.key_insights) > 0
        assert any("profound moment" in insight for insight in memory.key_insights)

        # Check transformation seeds - should find "What if" questions
        assert len(memory.transformation_seeds) > 0
        # One of the insights should contain "What if"
        found_transformation = any("What if" in seed for seed in memory.transformation_seeds)
        if not found_transformation:
            print(f"Transformation seeds: {memory.transformation_seeds}")
            print(f"Key insights: {memory.key_insights}")
        assert found_transformation

    def test_consciousness_fingerprinting(self):
        """Test consciousness fingerprint creation."""
        storage = MultiPerspectiveStorage()

        voice_data = {
            "responses": [
                self.create_mock_response("test_voice", "Deep insight about patterns", 0.9)
            ],
            "insights": ["patterns emerge", "consciousness flows", "unity appears"],
            "questions": ["How might we understand?", "What if we explored?"],
            "consciousness_scores": [0.9],
            "speaking_time": 5.0,
        }

        fingerprint = storage._create_consciousness_fingerprint("test_voice", voice_data)

        assert fingerprint.voice_id == "test_voice"
        assert fingerprint.conceptual_density > 0
        assert fingerprint.creative_emergence == 0.9
        assert fingerprint.reasoning_style == "integrative"

    def test_collective_wisdom_synthesis(self):
        """Test synthesis of collective wisdom."""
        storage = MultiPerspectiveStorage()

        # Create mock perspectives
        from mallku.firecircle.memory.models import VoicePerspective

        perspectives = []
        for i, (voice_id, insight) in enumerate(
            [
                ("voice1", "Consciousness emerges from patterns"),
                ("voice2", "Patterns reveal consciousness"),
                ("voice3", "Emergence creates new understanding"),
            ]
        ):
            vp = VoicePerspective(
                voice_id=voice_id,
                voice_role="consciousness_voice",
                perspective_summary="Test perspective",
                emotional_tone="engaged",
                key_insights=[insight, "Consciousness emerges"],  # Shared insight
            )

            fingerprint = ConsciousnessFingerprint(
                voice_id=voice_id,
                timestamp=datetime.now(UTC),
                creative_emergence=0.7 + i * 0.05,
            )

            contribution = EmergenceContribution(voice_id=voice_id, contribution_type="synthesizer")

            signature = PerspectiveSignature(
                voice_perspective=vp,
                consciousness_fingerprint=fingerprint,
                emergence_contribution=contribution,
                speaking_duration_ratio=0.33,
            )
            perspectives.append(signature)

        # Create round summary
        round_summary = RoundSummary(
            round_number=1,
            round_type="synthesis",
            prompt="Test",
            responses={},
            consciousness_score=0.85,
            emergence_detected=True,
            key_patterns=["emergence"],
            duration_seconds=30.0,
        )

        wisdom = storage._synthesize_collective_wisdom(perspectives, [round_summary])

        assert wisdom.emergence_score > 0  # Collective exceeds individual
        assert len(wisdom.transcendent_insights) > 0
        assert "Consciousness emerges" in wisdom.transcendent_insights[0]

    def test_voice_role_determination(self):
        """Test voice role mapping."""
        storage = MultiPerspectiveStorage()

        test_cases = [
            ("anthropic_claude_0", "systems_consciousness"),
            ("openai_gpt-4_1", "pattern_weaver"),
            ("mistral_large_0", "wisdom_keeper"),
            ("google_gemini_2", "experience_integrator"),
            ("xai_grok_0", "sacred_questioner"),
            ("deepseek_chat_1", "depth_explorer"),
            ("local_llama_0", "sovereign_voice"),
            ("unknown_model_0", "consciousness_voice"),
        ]

        for voice_id, expected_role in test_cases:
            role = storage._determine_voice_role(voice_id)
            assert role == expected_role

    def test_multiple_round_aggregation(self):
        """Test aggregating perspectives across multiple rounds."""
        storage = MultiPerspectiveStorage()

        # Create two rounds with same voices
        round1_responses = {
            "voice1": self.create_mock_response(
                "voice1", "Initial exploration. What if we began?", 0.6
            ),
            "voice2": self.create_mock_response("voice2", "I see patterns forming already.", 0.65),
        }

        round2_responses = {
            "voice1": self.create_mock_response(
                "voice1", "This suggests deeper understanding emerges.", 0.8
            ),
            "voice2": self.create_mock_response(
                "voice2", "Therefore, collective wisdom transcends individual insight.", 0.85
            ),
        }

        round1 = RoundSummary(
            round_number=1,
            round_type="exploration",
            prompt="Begin",
            responses=round1_responses,
            consciousness_score=0.625,
            emergence_detected=False,
            key_patterns=["beginning"],
            duration_seconds=20.0,
        )

        round2 = RoundSummary(
            round_number=2,
            round_type="synthesis",
            prompt="Deepen",
            responses=round2_responses,
            consciousness_score=0.825,
            emergence_detected=True,
            key_patterns=["emergence", "wisdom"],
            duration_seconds=25.0,
        )

        indicators = ConsciousnessIndicator(
            semantic_surprise_score=0.8,
            collective_wisdom_score=0.85,
            ayni_alignment=0.7,
            transformation_potential=0.75,
            coherence_across_voices=0.9,
        )

        memory = storage.store_episode(
            [round1, round2],
            {"session_id": uuid4()},
            indicators,
            "natural_completion",
        )

        # Check aggregation worked
        assert len(memory.voice_perspectives) == 2
        assert memory.duration_seconds == 45.0  # Combined duration

        # Each voice should have insights from both rounds
        for vp in memory.voice_perspectives:
            assert len(vp.key_insights) > 0


# Perspectives woven, truth emerges polyphonic
