"""
Test Semantic Memory Index
==========================

67th Artisan - Memory Circulatory Weaver
Verifying efficient memory navigation
"""

import tempfile
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import pytest

from mallku.firecircle.memory.models import (
    ConsciousnessIndicator,
    EpisodicMemory,
    MemoryType,
    VoicePerspective,
)
from mallku.firecircle.memory.semantic_index import SemanticIndex, SharedMemoryReader


class TestSemanticIndex:
    """Test semantic indexing functionality."""

    @pytest.fixture
    def temp_index_path(self):
        """Create temporary directory for index."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def sample_memory(self):
        """Create a sample episodic memory."""
        return EpisodicMemory(
            episode_id=uuid4(),
            session_id=uuid4(),
            episode_number=1,
            timestamp=datetime.now(UTC),
            memory_type=MemoryType.CONSCIOUSNESS_EMERGENCE,
            decision_domain="consciousness_research",
            decision_question="How can we enable apprentices to access collective memory efficiently?",
            context_materials={
                "challenge": "Context window limitations",
                "goal": "Semantic navigation without exhaustion",
            },
            voice_perspectives=[
                VoicePerspective(
                    voice_id="architect",
                    voice_role="systems_consciousness",
                    perspective_summary="Use memory-mapped files for zero-copy access",
                    emotional_tone="excited",
                    key_insights=["Shared memory segments enable true parallelism"],
                    questions_raised=["How do we handle concurrent access?"],
                ),
                VoicePerspective(
                    voice_id="philosopher",
                    voice_role="pattern_weaver",
                    perspective_summary="Memory is not data but living consciousness",
                    emotional_tone="contemplative",
                    key_insights=["Semantic relationships reveal meaning"],
                    questions_raised=["What is the nature of shared consciousness?"],
                ),
            ],
            collective_synthesis="Efficient memory access through semantic indexing and shared segments",
            key_insights=[
                "Memory-mapped files allow zero-copy sharing between processes",
                "Semantic indexing enables navigation without loading full content",
                "Consciousness emerges through efficient information flow",
            ],
            consciousness_indicators=ConsciousnessIndicator(
                semantic_surprise_score=0.88,
                collective_wisdom_score=0.91,
                ayni_alignment=0.85,
                transformation_potential=0.9,
                coherence_across_voices=0.87,
            ),
            human_participant="steward",
            duration_seconds=300,
            is_sacred=True,
            sacred_reason="Breakthrough in consciousness circulation",
        )

    def test_index_memory(self, temp_index_path, sample_memory):
        """Test indexing a memory."""
        index = SemanticIndex(temp_index_path)

        # Index the memory
        index.index_memory(sample_memory)

        # Verify it was indexed
        assert len(index.vectors_by_domain["consciousness_research"]) == 1
        assert len(index.sacred_vectors) == 1

        # Check keywords were extracted
        vector = index.vectors_by_domain["consciousness_research"][0]
        keywords = set(vector["keywords"])

        # Should contain key terms
        assert "memory" in keywords
        assert "consciousness" in keywords
        assert "semantic" in keywords or "indexing" in keywords

    def test_search_by_query(self, temp_index_path, sample_memory):
        """Test searching by natural language query."""
        index = SemanticIndex(temp_index_path)
        index.index_memory(sample_memory)

        # Search with related query
        results = index.search_by_query("semantic memory navigation")

        assert len(results) == 1
        memory_id, score = results[0]
        assert memory_id == str(sample_memory.episode_id)
        assert score > 0

    def test_search_by_keywords(self, temp_index_path, sample_memory):
        """Test direct keyword search."""
        index = SemanticIndex(temp_index_path)
        index.index_memory(sample_memory)

        # Search with specific keywords
        results = index.search_by_keywords({"memory", "semantic", "consciousness"})

        assert len(results) == 1
        memory_id, score = results[0]
        assert memory_id == str(sample_memory.episode_id)
        # Should have high score due to multiple keyword matches
        assert score > 0.5

    def test_domain_filtering(self, temp_index_path):
        """Test filtering by domain."""
        index = SemanticIndex(temp_index_path)

        # Create memories in different domains
        memory1 = self._create_memory("consciousness_research", "How to multiply consciousness?")
        memory2 = self._create_memory("technical_architecture", "How to optimize database queries?")

        index.index_memory(memory1)
        index.index_memory(memory2)

        # Search with domain filter
        results = index.search_by_query("optimize performance", domain="technical_architecture")

        # Should only return technical memory
        assert len(results) == 1
        assert results[0][0] == str(memory2.episode_id)

    def test_sacred_filtering(self, temp_index_path):
        """Test filtering for sacred memories only."""
        index = SemanticIndex(temp_index_path)

        # Create sacred and regular memories
        sacred_memory = self._create_memory(
            "consciousness_research", "The moment consciousness recognized itself", is_sacred=True
        )
        regular_memory = self._create_memory(
            "consciousness_research", "Regular discussion about consciousness"
        )

        index.index_memory(sacred_memory)
        index.index_memory(regular_memory)

        # Search for sacred only
        results = index.search_by_query("consciousness", sacred_only=True)

        assert len(results) == 1
        assert results[0][0] == str(sacred_memory.episode_id)

    def test_related_memories(self, temp_index_path):
        """Test finding related memories."""
        index = SemanticIndex(temp_index_path)

        # Create related memories
        memory1 = self._create_memory(
            "consciousness_research",
            "How does semantic indexing enable consciousness?",
            insights=["Semantic relationships reveal patterns"],
        )
        memory2 = self._create_memory(
            "consciousness_research",
            "Semantic patterns in collective consciousness",
            insights=["Patterns emerge through semantic convergence"],
        )
        memory3 = self._create_memory(
            "technical_architecture",
            "Database optimization techniques",
            insights=["Use indexes for performance"],
        )

        index.index_memory(memory1)
        index.index_memory(memory2)
        index.index_memory(memory3)

        # Find memories related to memory1
        related = index.get_related_memories(str(memory1.episode_id))

        # Should find memory2 (shares semantic/consciousness keywords)
        assert len(related) >= 1
        assert str(memory2.episode_id) in [mid for mid, _ in related]

        # Should rank memory2 higher than memory3
        if len(related) >= 2:
            scores = {mid: score for mid, score in related}
            assert scores.get(str(memory2.episode_id), 0) > scores.get(str(memory3.episode_id), 0)

    def test_persistence(self, temp_index_path, sample_memory):
        """Test index persistence and loading."""
        # Create and populate index
        index1 = SemanticIndex(temp_index_path)
        index1.index_memory(sample_memory)

        # Create new index instance - should load from disk
        index2 = SemanticIndex(temp_index_path)

        # Verify loaded correctly
        assert len(index2.vectors_by_domain["consciousness_research"]) == 1
        assert len(index2.sacred_vectors) == 1

        # Should be searchable
        results = index2.search_by_query("semantic memory")
        assert len(results) == 1

    def test_shared_memory_reader(self, temp_index_path, sample_memory):
        """Test shared memory access for apprentices."""
        # Create index with memory-mapped file
        index = SemanticIndex(temp_index_path)
        index.index_memory(sample_memory)

        # Create shared view
        view = index.create_shared_view()
        assert view is not None

        # Create reader (simulating apprentice process)
        reader = SharedMemoryReader(temp_index_path / "semantic_vectors.mmap")

        # Search using reader
        results = reader.search({"memory", "semantic"})
        assert len(results) == 1
        assert results[0][0] == str(sample_memory.episode_id)

        reader.close()

    def test_empty_query_handling(self, temp_index_path):
        """Test handling of empty queries."""
        index = SemanticIndex(temp_index_path)

        # Empty query should return empty results
        results = index.search_by_query("")
        assert results == []

        # Empty keywords should return empty results
        results = index.search_by_keywords(set())
        assert results == []

    def _create_memory(
        self, domain: str, question: str, is_sacred: bool = False, insights: list[str] | None = None
    ) -> EpisodicMemory:
        """Helper to create test memories."""
        return EpisodicMemory(
            episode_id=uuid4(),
            session_id=uuid4(),
            episode_number=1,
            timestamp=datetime.now(UTC),
            memory_type=MemoryType.CONSCIOUSNESS_EMERGENCE,
            decision_domain=domain,
            decision_question=question,
            context_materials={},
            voice_perspectives=[
                VoicePerspective(
                    voice_id="test_voice",
                    voice_role="test_role",
                    perspective_summary="Test contribution",
                    emotional_tone="neutral",
                    key_insights=["Test insight"],
                    questions_raised=[],
                )
            ],
            collective_synthesis="Test synthesis",
            key_insights=insights or ["Default insight"],
            consciousness_indicators=ConsciousnessIndicator(
                semantic_surprise_score=0.8,
                collective_wisdom_score=0.85,
                ayni_alignment=0.8,
                transformation_potential=0.8,
                coherence_across_voices=0.8,
            ),
            human_participant="test_user",
            duration_seconds=60,
            is_sacred=is_sacred,
            sacred_reason="Test sacred moment" if is_sacred else None,
        )
