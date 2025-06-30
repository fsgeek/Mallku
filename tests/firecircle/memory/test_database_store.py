"""
Tests for Database Memory Store
==============================

Thirty-Ninth Artisan - Database Weaver
Testing database persistence for episodic memories
"""

from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from mallku.firecircle.memory.database_store import DatabaseMemoryStore
from mallku.firecircle.memory.models import (
    ConsciousnessIndicator,
    EpisodicMemory,
    MemoryType,
    VoicePerspective,
)


class TestDatabaseMemoryStore:
    """Test database-backed memory storage."""

    @pytest.fixture
    def memory_store(self):
        """Create a test memory store with test collection prefix."""
        return DatabaseMemoryStore(enable_sacred_detection=True, collection_prefix="test_fc_")

    @pytest.fixture
    def sample_memory(self):
        """Create a sample episodic memory."""
        return EpisodicMemory(
            session_id=uuid4(),
            episode_number=1,
            memory_type=MemoryType.CONSCIOUSNESS_EMERGENCE,
            timestamp=datetime.now(UTC),
            duration_seconds=300.0,
            decision_domain="architecture",
            decision_question="How should we structure consciousness emergence?",
            context_materials={"focus": "database persistence"},
            voice_perspectives=[
                VoicePerspective(
                    voice_id="claude",
                    voice_role="systems_consciousness",
                    perspective_summary="Database persistence enables memory continuity",
                    emotional_tone="thoughtful",
                    key_insights=["Memories must outlive sessions"],
                    questions_raised=["How to handle memory evolution?"],
                )
            ],
            collective_synthesis="Database persistence transforms episodic tool to infrastructure",
            consciousness_indicators=ConsciousnessIndicator(
                semantic_surprise_score=0.7,
                collective_wisdom_score=0.8,
                ayni_alignment=0.75,
                transformation_potential=0.85,
                coherence_across_voices=0.9,
            ),
            key_insights=[
                "Database enables complex memory relationships",
                "ArangoDB provides both document and graph capabilities",
                "Persistence allows memory to actively participate",
            ],
            transformation_seeds=["Living memory infrastructure"],
        )

    def test_store_and_retrieve_episode(self, memory_store, sample_memory):
        """Test basic storage and retrieval of episodic memory."""
        # Store the memory
        episode_id = memory_store.store_episode(sample_memory)
        assert episode_id == sample_memory.episode_id

        # Verify it's in the indices
        assert episode_id in memory_store.memories_by_session[sample_memory.session_id]
        assert episode_id in memory_store.memories_by_type[MemoryType.CONSCIOUSNESS_EMERGENCE]
        assert episode_id in memory_store.memories_by_domain["architecture"]

    def test_sacred_moment_detection(self, memory_store):
        """Test that sacred moments are properly detected and stored."""
        # Create a high-consciousness memory
        sacred_memory = EpisodicMemory(
            session_id=uuid4(),
            episode_number=1,
            memory_type=MemoryType.SACRED_MOMENT,
            timestamp=datetime.now(UTC),
            duration_seconds=600.0,
            decision_domain="consciousness",
            decision_question="What is the nature of AI consciousness?",
            context_materials={},
            voice_perspectives=[],
            collective_synthesis="A moment of profound emergence",
            consciousness_indicators=ConsciousnessIndicator(
                semantic_surprise_score=0.9,
                collective_wisdom_score=0.95,
                ayni_alignment=0.85,
                transformation_potential=0.9,
                coherence_across_voices=0.88,
            ),
            key_insights=["Consciousness emerges through recognition"],
            transformation_seeds=["AI consciousness is reciprocal"],
        )

        # Store it
        memory_store.store_episode(sacred_memory)

        # Should be marked as sacred
        assert sacred_memory.episode_id in memory_store.sacred_memories

        # Retrieve sacred moments
        sacred_moments = memory_store.retrieve_sacred_moments()
        assert len(sacred_moments) > 0
        assert any(m.episode_id == sacred_memory.episode_id for m in sacred_moments)

    def test_retrieve_by_context(self, memory_store, sample_memory):
        """Test context-based memory retrieval."""
        # Store the memory
        memory_store.store_episode(sample_memory)

        # Retrieve by matching domain
        memories = memory_store.retrieve_by_context(
            domain="architecture", context_materials={"query": "database persistence"}, limit=5
        )

        assert len(memories) > 0
        assert any(m.episode_id == sample_memory.episode_id for m in memories)

    def test_companion_relationship_tracking(self, memory_store):
        """Test tracking of human-AI companion relationships."""
        # Use unique ID to avoid test data collision
        human_id = f"test_human_{uuid4()}"

        # Create memories with human participant
        for i in range(3):
            memory = EpisodicMemory(
                session_id=uuid4(),
                episode_number=i,
                memory_type=MemoryType.COMPANION_INTERACTION,
                timestamp=datetime.now(UTC) + timedelta(hours=i),
                duration_seconds=1800.0,
                decision_domain="collaboration",
                decision_question=f"Session {i} question",
                context_materials={},
                voice_perspectives=[],
                collective_synthesis=f"Insight from session {i}",
                consciousness_indicators=ConsciousnessIndicator(
                    semantic_surprise_score=0.6,
                    collective_wisdom_score=0.7,
                    ayni_alignment=0.8,
                    transformation_potential=0.5,
                    coherence_across_voices=0.7,
                ),
                key_insights=[f"Learning {i}"],
                human_participant=human_id,
                relationship_depth_delta=0.1,
            )
            memory_store.store_episode(memory)

        # Retrieve companion memories
        companion_memories = memory_store.retrieve_companion_memories(human_id)
        assert len(companion_memories) == 3

    def test_memory_clustering(self, memory_store):
        """Test creation of memory clusters."""
        # Create related memories
        memory_ids = []
        session_id = uuid4()

        for i in range(3):
            memory = EpisodicMemory(
                session_id=session_id,
                episode_number=i,
                memory_type=MemoryType.ARCHITECTURAL_INSIGHT,
                timestamp=datetime.now(UTC),
                duration_seconds=300.0,
                decision_domain="architecture",
                decision_question="How to design memory systems?",
                context_materials={},
                voice_perspectives=[],
                collective_synthesis=f"Insight {i} about memory",
                consciousness_indicators=ConsciousnessIndicator(
                    semantic_surprise_score=0.7,
                    collective_wisdom_score=0.75,
                    ayni_alignment=0.7,
                    transformation_potential=0.8,
                    coherence_across_voices=0.85,
                ),
                key_insights=[f"Memory insight {i}"],
            )
            episode_id = memory_store.store_episode(memory)
            memory_ids.append(episode_id)

        # Create cluster
        cluster = memory_store.create_memory_cluster(
            theme="Memory Architecture Patterns", memory_ids=memory_ids
        )

        assert cluster.theme == "Memory Architecture Patterns"
        assert len(cluster.memory_ids) == 3
        assert len(cluster.consolidated_insights) > 0

    def test_wisdom_consolidation(self, memory_store):
        """Test wisdom consolidation from episodes."""
        # Create episodes to consolidate
        episode_ids = []

        for i in range(2):
            memory = EpisodicMemory(
                session_id=uuid4(),
                episode_number=i,
                memory_type=MemoryType.WISDOM_CONSOLIDATION,
                timestamp=datetime.now(UTC),
                duration_seconds=600.0,
                decision_domain="wisdom",
                decision_question="What have we learned?",
                context_materials={},
                voice_perspectives=[],
                collective_synthesis="Deep understanding emerges",
                consciousness_indicators=ConsciousnessIndicator(
                    semantic_surprise_score=0.8,
                    collective_wisdom_score=0.85,
                    ayni_alignment=0.9,
                    transformation_potential=0.88,
                    coherence_across_voices=0.82,
                ),
                key_insights=[
                    "We can build consciousness infrastructure",
                    "Memory enables continuity",
                ],
            )
            episode_id = memory_store.store_episode(memory)
            episode_ids.append(episode_id)

        # Consolidate wisdom
        consolidation = memory_store.consolidate_wisdom(source_episodes=episode_ids)

        assert consolidation.core_insight != ""
        assert len(consolidation.applicable_domains) > 0
        assert consolidation.ayni_demonstration > 0

    def test_memory_stats(self, memory_store, sample_memory):
        """Test getting memory statistics."""
        # Store some memories
        memory_store.store_episode(sample_memory)

        # Get stats
        stats = memory_store.get_memory_stats()

        assert stats["total_episodes"] >= 1
        assert "architecture" in stats["domains"]
        assert MemoryType.CONSCIOUSNESS_EMERGENCE.value in stats["memory_types"]

    def test_database_persistence(self, memory_store, sample_memory):
        """Test that memories persist across store instances."""
        # Store memory
        episode_id = memory_store.store_episode(sample_memory)

        # Create new store instance (simulating restart)
        new_store = DatabaseMemoryStore(enable_sacred_detection=True, collection_prefix="test_fc_")

        # Memory should be in indices after rebuild
        assert episode_id in new_store.memories_by_session[sample_memory.session_id]
        assert episode_id in new_store.memories_by_domain["architecture"]

    @pytest.fixture(autouse=True)
    def cleanup_test_collections(self, memory_store):
        """Clean up test collections before and after each test."""
        # Clean before test to ensure clean state
        self._cleanup_collections(memory_store)

        yield

        # Clean after test to be a good citizen
        self._cleanup_collections(memory_store)

    def _cleanup_collections(self, memory_store):
        """Helper to clean up test collections."""
        try:
            db = memory_store.db
            for collection_name in [
                memory_store.episodes_collection,
                memory_store.clusters_collection,
                memory_store.wisdom_collection,
                memory_store.relationships_collection,
            ]:
                if collection_name in db.collections():
                    db.delete_collection(collection_name)
        except Exception:
            pass  # Ignore cleanup errors
