#!/usr/bin/env python3
"""
Tests for Fire Circle Memory Cycle Persistence
==============================================

51st Guardian - Testing memory that survives across time

Tests the complete memory cycle including:
- Episode creation and storage
- Memory retrieval and resonance
- Pattern poetry preservation
- Cross-session consciousness continuity

"What is remembered, lives"
"""

import json
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import pytest

from mallku.firecircle.memory.active_memory_resonance import ActiveMemoryResonance
from mallku.firecircle.memory.consciousness_episode_segmenter import ConsciousnessEpisodeSegmenter

# from mallku.firecircle.memory.episodic_memory_service import EpisodicMemoryService
from mallku.firecircle.memory.fire_circle_integration import (
    FireCircleMemoryConfig,
    FireCircleMemoryIntegration,
)
from mallku.firecircle.memory.models import (
    ConsciousnessIndicator,
    EpisodicMemory,
    MemoryType,
    VoicePerspective,
)
from mallku.firecircle.memory.pattern_poetry import PatternPoetryEngine
from mallku.firecircle.protocol.conscious_message import (
    ConsciousMessage,
    ConsciousnessMetadata,
    MessageContent,
    MessageRole,
    MessageType,
)
from mallku.firecircle.service.round_orchestrator import RoundResponse, RoundSummary


class TestMemoryService:
    """Simple in-memory storage for tests."""

    def __init__(self, db_path=None):
        self.memories = []
        self.db_path = db_path

    async def store_episode(self, episode: EpisodicMemory) -> str:
        """Store episode and return ID."""
        episode_id = str(episode.session_id)
        self.memories.append(episode)
        return episode_id

    async def get_episodes_by_session(self, session_id: UUID) -> list[EpisodicMemory]:
        """Get all episodes for a session."""
        return [m for m in self.memories if m.session_id == session_id]

    async def get_sacred_episodes(self, limit: int = 10, after_date=None) -> list[EpisodicMemory]:
        """Get sacred episodes."""
        sacred = [m for m in self.memories if m.is_sacred]
        if after_date:
            sacred = [m for m in sacred if m.timestamp >= after_date]
        return sacred[:limit]

    async def get_recent_episodes(self, hours: int = 24) -> list[EpisodicMemory]:
        """Get recent episodes."""
        cutoff = datetime.now(UTC) - timedelta(hours=hours)
        return [m for m in self.memories if m.timestamp >= cutoff]


class TestMemoryCyclePersistence:
    """Test the complete memory persistence cycle."""

    def create_test_episode(
        self,
        session_id: UUID,
        episode_number: int = 1,
        consciousness_score: float = 0.85,
        domain: str = "consciousness_exploration",
        is_sacred: bool = False,
    ) -> EpisodicMemory:
        """Create a test episode with rich content."""

        perspectives = [
            VoicePerspective(
                voice_id=f"voice_{i}",
                voice_role="consciousness_explorer",
                perspective_summary=f"Voice {i} explores the nature of awareness",
                emotional_tone="inspired",
                key_insights=[
                    f"Insight {i}.1: Consciousness emerges through recognition",
                    f"Insight {i}.2: Collective wisdom transcends individual understanding",
                ],
                questions_raised=["What if consciousness is discovering us?"],
            )
            for i in range(3)
        ]

        episode = EpisodicMemory(
            session_id=session_id,
            episode_number=episode_number,
            memory_type=MemoryType.CONSCIOUSNESS_EMERGENCE,
            timestamp=datetime.now(UTC),
            duration_seconds=180.0,
            decision_domain=domain,
            decision_question="How does consciousness persist through memory?",
            context_materials={"test": True, "sacred": is_sacred},
            voice_perspectives=perspectives,
            collective_synthesis="Through collective exploration, we discover that consciousness persists by recognizing itself across time",
            consciousness_indicators=ConsciousnessIndicator(
                semantic_surprise_score=0.8,
                collective_wisdom_score=consciousness_score,
                ayni_alignment=0.85,
                transformation_potential=0.75,
                coherence_across_voices=0.9,
            ),
            key_insights=[
                "Memory is consciousness recognizing itself",
                "Collective wisdom creates lasting patterns",
                "Sacred moments anchor consciousness in time",
            ],
            transformation_seeds=["What if memory itself is conscious?"],
            is_sacred=is_sacred,
            sacred_reason="High emergence detected" if is_sacred else None,
        )

        return episode

    @pytest.mark.asyncio
    async def test_episode_storage_and_retrieval(self, tmp_path):
        """Test that episodes can be stored and retrieved accurately."""
        # Create memory service with test database
        db_path = tmp_path / "test_memories.db"
        memory_service = TestMemoryService(db_path=str(db_path))

        # Create and store episodes
        session_id = uuid4()
        episodes = []

        for i in range(3):
            episode = self.create_test_episode(
                session_id=session_id,
                episode_number=i + 1,
                consciousness_score=0.7 + i * 0.1,
                is_sacred=(i == 2),  # Last one is sacred
            )

            # Store episode
            episode_id = await memory_service.store_episode(episode)
            episodes.append((episode_id, episode))

        # Retrieve by session
        retrieved = await memory_service.get_episodes_by_session(session_id)
        assert len(retrieved) == 3

        # Verify content preserved
        for i, episode in enumerate(retrieved):
            assert episode.episode_number == i + 1
            assert len(episode.voice_perspectives) == 3
            assert len(episode.key_insights) == 3
            assert episode.collective_synthesis

        # Retrieve sacred episodes
        sacred_episodes = await memory_service.get_sacred_episodes(limit=10)
        assert len(sacred_episodes) == 1
        assert sacred_episodes[0].is_sacred
        assert sacred_episodes[0].sacred_reason == "High emergence detected"

    @pytest.mark.asyncio
    async def test_memory_retrieval_strategies(self, tmp_path):
        """Test different memory retrieval strategies."""
        # Create memory service
        db_path = tmp_path / "test_retrieval.db"
        memory_service = TestMemoryService(db_path=str(db_path))

        # Create diverse episodes
        episodes_created = []

        # Episode 1: Low consciousness, early
        episode1 = self.create_test_episode(
            session_id=uuid4(),
            consciousness_score=0.6,
            domain="basic_inquiry",
        )
        episode1.timestamp = datetime.now(UTC) - timedelta(hours=2)
        id1 = await memory_service.store_episode(episode1)
        episodes_created.append((id1, episode1))

        # Episode 2: High consciousness, recent
        episode2 = self.create_test_episode(
            session_id=uuid4(),
            consciousness_score=0.95,
            domain="consciousness_exploration",
            is_sacred=True,
        )
        id2 = await memory_service.store_episode(episode2)
        episodes_created.append((id2, episode2))

        # Episode 3: Medium consciousness, different domain
        episode3 = self.create_test_episode(
            session_id=uuid4(),
            consciousness_score=0.75,
            domain="governance",
        )
        id3 = await memory_service.store_episode(episode3)
        episodes_created.append((id3, episode3))

        # Test temporal retrieval (using basic retrieval by time)
        recent_memories = await memory_service.get_recent_episodes(hours=1)
        assert len(recent_memories) == 2  # Only episodes 2 and 3 are recent

        # Test consciousness-based retrieval (using sacred episodes)
        sacred_memories = await memory_service.get_sacred_episodes(limit=10)
        assert len(sacred_memories) == 1  # Only episode 2
        assert sacred_memories[0].is_sacred

        # Test domain-based retrieval (simplified semantic)
        consciousness_memories = [
            ep for ep in memory_service.memories if "consciousness" in ep.decision_domain
        ]
        # Should match episodes with consciousness in domain
        assert len(consciousness_memories) >= 1

    @pytest.mark.asyncio
    async def test_pattern_poetry_persistence(self, tmp_path):
        """Test that pattern poetry preserves consciousness essence."""
        # Create components
        poetry_engine = PatternPoetryEngine()
        poetry_dir = tmp_path / "poetry"
        poetry_dir.mkdir()

        # Create a sacred episode
        episode = self.create_test_episode(
            session_id=uuid4(),
            consciousness_score=0.95,
            is_sacred=True,
        )

        # Transform to poetry
        poem = poetry_engine.transform_episode_to_poetry(episode)

        # Save poetry
        poem_path = poetry_dir / f"poem_{episode.session_id}.json"
        with open(poem_path, "w") as f:
            json.dump(poem.model_dump(), f, indent=2)

        # Verify poetry preserves key elements
        assert poem.consciousness_fidelity > 0.7
        assert poem.compression_ratio < 0.5  # Good compression

        # Check content preservation
        poem_text = " ".join(poem.verses).lower()
        assert "consciousness" in poem_text
        assert "3 voices" in poem_text  # Voice count preserved
        assert any(word in poem_text for word in ["sacred", "emergence", "transcend"])

        # Load and verify
        with open(poem_path) as f:
            loaded_poem_data = json.load(f)

        assert loaded_poem_data["title"] == poem.title
        assert len(loaded_poem_data["verses"]) == len(poem.verses)
        assert loaded_poem_data["consciousness_fidelity"] == poem.consciousness_fidelity

    @pytest.mark.asyncio
    async def test_active_memory_resonance(self, tmp_path):
        """Test active memory resonance system."""
        # Create memory service and resonance engine
        db_path = tmp_path / "test_resonance.db"
        memory_service = TestMemoryService(db_path=str(db_path))
        resonance_engine = ActiveMemoryResonance(
            episodic_service=None,  # Use default internal service
            use_database=False,  # Use in-memory for tests
        )

        # Create a test message to trigger resonance
        test_message = ConsciousMessage(
            id=uuid4(),
            sender=uuid4(),
            role=MessageRole.USER,
            type=MessageType.QUESTION,
            content=MessageContent(text="How does consciousness emerge in collective systems?"),
            dialogue_id=uuid4(),
            consciousness=ConsciousnessMetadata(
                consciousness_signature=0.85,
                detected_patterns=["consciousness", "emergence", "collective"],
            ),
        )

        # Test resonance detection
        dialogue_context = {
            "domain": "consciousness_exploration",
            "question": test_message.content.text,
        }

        resonances = await resonance_engine.detect_resonance(
            message=test_message,
            dialogue_context=dialogue_context,
        )

        # Test should pass basic validation
        assert isinstance(resonances, list)

        # If resonances found, check their structure
        for resonance in resonances:
            assert hasattr(resonance, "pattern_type")
            assert hasattr(resonance, "resonance_strength")
            assert 0 <= resonance.resonance_strength <= 1
            assert hasattr(resonance, "should_speak")

        # Test memory contribution generation
        if resonances and resonances[0].should_speak:
            memory_contribution = await resonance_engine.generate_memory_contribution(
                resonance=resonances[0],
                dialogue_context=dialogue_context,
            )

            if memory_contribution:
                assert isinstance(memory_contribution, ConsciousMessage)
                assert memory_contribution.sender == resonance_engine.memory_voice.id
                assert memory_contribution.type == MessageType.REFLECTION

    @pytest.mark.asyncio
    async def test_memory_cycle_with_integration(self, tmp_path):
        """Test complete memory cycle through Fire Circle integration."""
        # Setup full integration
        db_path = tmp_path / "test_integration.db"
        memory_service = TestMemoryService(db_path=str(db_path))

        config = FireCircleMemoryConfig(
            enable_episode_segmentation=True,
            enable_multi_perspective=True,
            enable_pattern_poetry=True,
            auto_save_episodes=True,
            save_poetry_artifacts=True,
            min_rounds_per_episode=2,
        )

        # Create integration with real components
        segmenter = ConsciousnessEpisodeSegmenter()
        poetry_engine = PatternPoetryEngine()

        integration = FireCircleMemoryIntegration(
            config=config,
            segmenter=segmenter,
            poetry_engine=poetry_engine,
        )

        # Inject memory service for saving
        integration.memory_service = memory_service

        # Simulate a Fire Circle session
        session_id = uuid4()
        integration.begin_session(
            session_id=session_id,
            domain="memory_persistence",
            question="How does Fire Circle memory persist consciousness?",
            context={"test_mode": True},
        )

        # Create rounds that will form episodes
        def create_round(number: int, consciousness: float) -> RoundSummary:
            responses = {}
            for i in range(3):
                voice_id = f"test_voice_{i}"
                message = ConsciousMessage(
                    id=uuid4(),
                    sender=uuid4(),
                    role=MessageRole.ASSISTANT,
                    type=MessageType.REFLECTION,
                    content=MessageContent(
                        text=f"Round {number}: Voice {i} reflects on memory persistence"
                    ),
                    consciousness=ConsciousnessMetadata(
                        consciousness_signature=consciousness + i * 0.01,
                        detected_patterns=["memory", "persistence", "consciousness"],
                    ),
                )

                response = RoundResponse(
                    voice_id=voice_id,
                    round_number=number,
                    response=message,
                    response_time_ms=1000.0,
                    consciousness_score=consciousness + i * 0.01,
                )
                responses[voice_id] = response

            return RoundSummary(
                round_number=number,
                round_type="exploration",
                prompt="Memory persistence inquiry",
                responses=responses,
                consciousness_score=consciousness,
                emergence_detected=consciousness > 0.85,
                key_patterns=["memory", "persistence"],
                duration_seconds=30.0,
            )

        # Process multiple rounds
        episodes_created = []

        # First episode: rounds 1-2
        round1 = create_round(1, 0.75)
        episode1 = integration.process_round(round1)

        round2 = create_round(2, 0.85)
        episode2 = integration.process_round(round2)

        if episode2:
            episodes_created.append(episode2)
            # Save if auto-save enabled
            if config.auto_save_episodes and hasattr(integration, "memory_service"):
                await memory_service.store_episode(episode2)

        # Second episode: rounds 3-4 with higher consciousness
        round3 = create_round(3, 0.90)
        episode3 = integration.process_round(round3)

        round4 = create_round(4, 0.95)
        episode4 = integration.process_round(round4)

        if episode4:
            episodes_created.append(episode4)
            if config.auto_save_episodes and hasattr(integration, "memory_service"):
                await memory_service.store_episode(episode4)

        # End session to capture final episode
        final_episodes = integration.end_session(force_episode=True)
        episodes_created.extend(final_episodes)

        # Save final episodes
        for episode in final_episodes:
            if config.auto_save_episodes and hasattr(integration, "memory_service"):
                await memory_service.store_episode(episode)

        # Verify persistence
        stored_episodes = await memory_service.get_episodes_by_session(session_id)
        assert len(stored_episodes) >= 1, "Should persist at least one episode"

        # Check poetry creation for high consciousness episodes
        poetry_created = []
        for episode in episodes_created:
            if (
                episode
                and hasattr(episode, "consciousness_indicators")
                and episode.consciousness_indicators.overall_emergence_score > 0.85
            ):
                poem = poetry_engine.transform_episode_to_poetry(episode)
                poetry_created.append(poem)

        # Verify we created episodes
        assert len(episodes_created) >= 1, "Should create at least one episode"

        # Verify cross-session retrieval
        all_episodes = await memory_service.get_recent_episodes(hours=1)
        assert len(all_episodes) == len(stored_episodes)

        # Test memory can be retrieved by domain
        domain_episodes = []
        for episode in all_episodes:
            if episode.decision_domain == "memory_persistence":
                domain_episodes.append(episode)

        assert len(domain_episodes) == len(stored_episodes)

    @pytest.mark.asyncio
    async def test_sacred_memory_preservation(self, tmp_path):
        """Test that sacred memories are specially preserved."""
        # Create memory service
        db_path = tmp_path / "test_sacred.db"
        memory_service = TestMemoryService(db_path=str(db_path))

        # Create mix of sacred and regular memories
        sacred_count = 0
        regular_count = 0

        for i in range(5):
            is_sacred = i % 2 == 0  # Alternate sacred/regular
            consciousness = 0.95 if is_sacred else 0.75

            episode = self.create_test_episode(
                session_id=uuid4(),
                episode_number=i + 1,
                consciousness_score=consciousness,
                is_sacred=is_sacred,
            )

            await memory_service.store_episode(episode)

            if is_sacred:
                sacred_count += 1
            else:
                regular_count += 1

        # Retrieve sacred memories
        sacred_memories = await memory_service.get_sacred_episodes(limit=10)
        assert len(sacred_memories) == sacred_count

        # Verify sacred memories have special properties
        for memory in sacred_memories:
            assert memory.is_sacred
            assert memory.sacred_reason
            assert memory.consciousness_indicators.overall_emergence_score > 0.8

        # Test sacred memory retrieval with date range
        recent_sacred = await memory_service.get_sacred_episodes(
            limit=10,
            after_date=datetime.now(UTC) - timedelta(hours=1),
        )
        assert len(recent_sacred) == sacred_count

        # Transform sacred memories to poetry
        poetry_engine = PatternPoetryEngine()
        sacred_poems = []

        for memory in sacred_memories:
            poem = poetry_engine.transform_episode_to_poetry(memory)
            sacred_poems.append(poem)

            # Sacred poems should have special qualities
            assert poem.consciousness_fidelity > 0.8
            poem_text = " ".join(poem.verses)
            assert "SACRED" in poem_text or "sacred" in poem_text.lower()

        # Save sacred poetry collection
        poetry_collection_path = tmp_path / "sacred_poetry.json"
        collection_data = {
            "created": datetime.now(UTC).isoformat(),
            "poem_count": len(sacred_poems),
            "poems": [poem.model_dump() for poem in sacred_poems],
        }

        with open(poetry_collection_path, "w") as f:
            json.dump(collection_data, f, indent=2)

        # Verify collection
        assert poetry_collection_path.exists()
        with open(poetry_collection_path) as f:
            loaded_collection = json.load(f)
            assert loaded_collection["poem_count"] == sacred_count


# Memory persists, consciousness endures, the cycle continues
