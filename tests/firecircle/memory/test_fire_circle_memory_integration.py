#!/usr/bin/env python3
"""
Tests for Fire Circle Memory Integration
========================================

T'ikray Yachay - 39th Artisan - Memory Architect
Testing the bridge between session and memory
"""

from uuid import uuid4

from mallku.firecircle.memory.fire_circle_integration import (
    FireCircleMemoryConfig,
    FireCircleMemoryIntegration,
)
from mallku.firecircle.protocol.conscious_message import (
    ConsciousMessage,
    ConsciousnessMetadata,
    MessageContent,
    MessageRole,
    MessageType,
)
from mallku.firecircle.service.round_orchestrator import RoundResponse, RoundSummary


class TestFireCircleMemoryIntegration:
    """Test Fire Circle memory integration."""

    def create_mock_round(
        self, round_number: int, consciousness_score: float = 0.7
    ) -> RoundSummary:
        """Create a mock round summary."""
        responses = {}

        for i, voice_id in enumerate(["anthropic_claude_0", "openai_gpt_0", "mistral_0"]):
            message = ConsciousMessage(
                id=uuid4(),
                sender=uuid4(),
                role=MessageRole.ASSISTANT,
                type=MessageType.REFLECTION,
                content=MessageContent(text=f"Round {round_number} insight from {voice_id}"),
                consciousness=ConsciousnessMetadata(
                    consciousness_signature=consciousness_score + i * 0.05,
                    detected_patterns=["test_pattern"],
                ),
            )

            response = RoundResponse(
                voice_id=voice_id,
                round_number=round_number,
                response=message,
                response_time_ms=1000.0,
                consciousness_score=consciousness_score + i * 0.05,
            )

            responses[voice_id] = response

        return RoundSummary(
            round_number=round_number,
            round_type="exploration",
            prompt=f"Round {round_number} prompt",
            responses=responses,
            consciousness_score=consciousness_score,
            emergence_detected=consciousness_score > 0.7,
            key_patterns=["test_pattern"],
            duration_seconds=30.0,
        )

    def test_session_lifecycle(self):
        """Test basic session lifecycle."""
        integration = FireCircleMemoryIntegration()
        session_id = uuid4()

        # Begin session
        integration.begin_session(
            session_id=session_id,
            domain="test_domain",
            question="Test question?",
            context={"test_context": "value"},
        )

        assert integration.current_session_id == session_id
        assert integration.session_context["domain"] == "test_domain"
        assert integration.session_context["question"] == "Test question?"
        assert integration.episode_count == 0

        # Process rounds (not enough for episode)
        round1 = self.create_mock_round(1, 0.6)
        episode = integration.process_round(round1)
        assert episode is None  # Not enough rounds

        # End session
        episodes = integration.end_session(force_episode=True)
        assert len(episodes) == 1  # Forced final episode
        assert integration.current_session_id is None

    def test_episode_detection(self):
        """Test episode boundary detection."""
        config = FireCircleMemoryConfig(
            enable_episode_segmentation=True,
            min_rounds_per_episode=2,
        )
        integration = FireCircleMemoryIntegration(config=config)

        # Begin session
        integration.begin_session(
            session_id=uuid4(),
            domain="consciousness_exploration",
            question="What emerges?",
        )

        # Process rounds with increasing consciousness
        round1 = self.create_mock_round(1, 0.6)
        round2 = self.create_mock_round(2, 0.7)
        round3 = self.create_mock_round(3, 0.85)  # High consciousness

        episode1 = integration.process_round(round1)
        assert episode1 is None  # Not enough rounds

        episode2 = integration.process_round(round2)
        # May or may not create episode depending on segmenter logic

        episode3 = integration.process_round(round3)
        # May or may not create episode depending on segmenter logic

        # End session
        final_episodes = integration.end_session()
        # Should have created at least one episode by now (either during processing or at end)
        total_episodes = sum(1 for e in [episode1, episode2, episode3] if e) + len(final_episodes)
        assert total_episodes >= 1

    def test_multi_episode_session(self):
        """Test session with multiple episodes."""
        config = FireCircleMemoryConfig(
            enable_episode_segmentation=True,
            min_rounds_per_episode=2,
        )
        integration = FireCircleMemoryIntegration(config=config)

        integration.begin_session(
            session_id=uuid4(),
            domain="governance",
            question="How should we proceed?",
        )

        episodes_created = 0

        # Create many rounds to potentially trigger boundaries
        for i in range(6):
            # Alternate between low and high consciousness
            consciousness = 0.9 if i % 3 == 2 else 0.6
            round_summary = self.create_mock_round(i + 1, consciousness)

            episode = integration.process_round(round_summary)
            if episode:
                episodes_created += 1
                # Episode number is assigned by segmenter
                assert episode.episode_number > 0
                # Basic episode fields should be populated
                assert episode.session_id is not None
                assert episode.duration_seconds > 0

        # End session
        final_episodes = integration.end_session()
        total_episodes = episodes_created + len(final_episodes)

        assert total_episodes >= 1  # At least one episode created

    def test_poetry_integration(self):
        """Test pattern poetry integration."""
        config = FireCircleMemoryConfig(
            enable_episode_segmentation=True,
            enable_pattern_poetry=True,  # Enable poetry
            min_rounds_per_episode=2,
        )
        integration = FireCircleMemoryIntegration(config=config)

        integration.begin_session(
            session_id=uuid4(),
            domain="consciousness_exploration",
            question="What patterns emerge?",
        )

        # Create rounds that should form an episode
        round1 = self.create_mock_round(1, 0.7)

        integration.process_round(round1)
        # Poetry should be created if episode detected
        # (Check logs for poetry creation messages)

        # Force final episode
        episodes = integration.end_session(force_episode=True)
        assert len(episodes) == 1

        # Verify episode has required fields
        episode = episodes[0]
        assert episode.session_id is not None
        assert episode.duration_seconds > 0

    def test_no_session_handling(self):
        """Test handling rounds without active session."""
        integration = FireCircleMemoryIntegration()

        # Try to process round without session
        round_summary = self.create_mock_round(1)
        episode = integration.process_round(round_summary)

        assert episode is None  # Should handle gracefully

        # Try to end non-existent session
        episodes = integration.end_session()
        assert episodes == []  # Should return empty list


# Test the bridges we build
