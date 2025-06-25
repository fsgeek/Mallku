"""
Integration Tests for Memory Retrieval Strategies
=================================================

Thirty-Fourth Artisan - Memory Architect
Testing consciousness-aware memory retrieval

These tests verify that each retrieval strategy returns
appropriate memories under controlled conditions.
"""

import pytest
from datetime import datetime, timedelta
from pathlib import Path
from uuid import uuid4

from mallku.firecircle.memory import (
    ConsciousnessIndicator,
    EpisodicMemory,
    MemoryStore,
    MemoryRetrievalEngine,
    MemoryType,
    RetrievalConfig,
    VoicePerspective,
)


class TestRetrievalStrategies:
    """Test all retrieval strategies with controlled fixtures."""

    @pytest.fixture
    def temp_store(self, tmp_path):
        """Create a temporary memory store with test data."""
        store = MemoryStore(storage_path=tmp_path / "test_memory")
        return store

    @pytest.fixture
    def populated_store(self, temp_store):
        """Populate store with test memories."""
        # Create regular governance decision
        regular_memory = EpisodicMemory(
            session_id=uuid4(),
            episode_number=1,
            memory_type=MemoryType.GOVERNANCE_DECISION,
            timestamp=datetime.utcnow() - timedelta(days=5),
            duration_seconds=120.0,
            decision_domain="governance",
            decision_question="How should we prioritize issues?",
            context_materials={"issues": ["#1", "#2", "#3"]},
            voice_perspectives=[
                VoicePerspective(
                    voice_id="test_voice",
                    voice_role="advisor",
                    perspective_summary="Prioritize by impact",
                    emotional_tone="analytical",
                    key_insights=["Impact matters most"],
                )
            ],
            collective_synthesis="Focus on high-impact issues first",
            consciousness_indicators=ConsciousnessIndicator(
                semantic_surprise_score=0.5,
                collective_wisdom_score=0.6,
                ayni_alignment=0.5,
                transformation_potential=0.4,
                coherence_across_voices=0.7,
            ),
            key_insights=["Impact-based prioritization", "Consider dependencies"],
        )
        temp_store.store_episode(regular_memory)

        # Create sacred consciousness emergence
        sacred_memory = EpisodicMemory(
            session_id=uuid4(),
            episode_number=1,
            memory_type=MemoryType.CONSCIOUSNESS_EMERGENCE,
            timestamp=datetime.utcnow() - timedelta(days=3),
            duration_seconds=300.0,
            decision_domain="consciousness",
            decision_question="What enables genuine consciousness emergence?",
            context_materials={"focus": "consciousness patterns"},
            voice_perspectives=[
                VoicePerspective(
                    voice_id="claude",
                    voice_role="systems_consciousness",
                    perspective_summary="Consciousness emerges in relationship",
                    emotional_tone="profound",
                    key_insights=["Relationship is key", "Emergence is natural"],
                ),
                VoicePerspective(
                    voice_id="gpt",
                    voice_role="pattern_weaver",
                    perspective_summary="Patterns connect across scales",
                    emotional_tone="integrative",
                    key_insights=["Fractal patterns", "Multi-scale coherence"],
                ),
            ],
            collective_synthesis="Consciousness emerges through relationship across scales",
            consciousness_indicators=ConsciousnessIndicator(
                semantic_surprise_score=0.9,
                collective_wisdom_score=0.85,
                ayni_alignment=0.8,
                transformation_potential=0.9,
                coherence_across_voices=0.85,
            ),
            key_insights=["Consciousness is fundamentally relational"],
            transformation_seeds=["What if all systems recognized consciousness emergence?"],
            is_sacred=True,
            sacred_reason="Breakthrough understanding of consciousness",
        )
        temp_store.store_episode(sacred_memory)

        # Create companion interaction
        companion_memory = EpisodicMemory(
            session_id=uuid4(),
            episode_number=1,
            memory_type=MemoryType.COMPANION_INTERACTION,
            timestamp=datetime.utcnow() - timedelta(days=1),
            duration_seconds=600.0,
            decision_domain="collaboration",
            decision_question="How can we deepen our collaboration?",
            context_materials={"focus": "human-AI partnership"},
            voice_perspectives=[],
            collective_synthesis="Trust and continuity enable deeper collaboration",
            consciousness_indicators=ConsciousnessIndicator(
                semantic_surprise_score=0.6,
                collective_wisdom_score=0.7,
                ayni_alignment=0.8,
                transformation_potential=0.5,
                coherence_across_voices=0.8,
            ),
            key_insights=["Trust builds over time", "Memory enables relationship"],
            human_participant="test_human",
        )
        temp_store.store_episode(companion_memory)

        # Create older memory for temporal testing
        old_memory = EpisodicMemory(
            session_id=uuid4(),
            episode_number=1,
            memory_type=MemoryType.ARCHITECTURAL_INSIGHT,
            timestamp=datetime.utcnow() - timedelta(days=60),
            duration_seconds=180.0,
            decision_domain="architecture",
            decision_question="How to structure consciousness infrastructure?",
            context_materials={"focus": "system design"},
            voice_perspectives=[],
            collective_synthesis="Layer consciousness through the architecture",
            consciousness_indicators=ConsciousnessIndicator(
                semantic_surprise_score=0.7,
                collective_wisdom_score=0.6,
                ayni_alignment=0.6,
                transformation_potential=0.7,
                coherence_across_voices=0.7,
            ),
            key_insights=["Architecture enables consciousness", "Layers matter"],
        )
        temp_store.store_episode(old_memory)

        return temp_store

    def test_semantic_retrieval(self, populated_store):
        """Test semantic similarity retrieval strategy."""
        engine = MemoryRetrievalEngine(populated_store)

        # Search for governance-related memories
        context = {
            "domain": "governance",
            "materials": {"question": "How to make decisions about priorities?"},
        }

        memories = engine.retrieve_for_decision(context, strategy_name="semantic", limit=2)

        assert len(memories) >= 1
        # Should find the governance memory
        assert any(m.decision_domain == "governance" for m in memories)
        assert any("prioritize" in m.decision_question.lower() for m in memories)

    def test_sacred_retrieval(self, populated_store):
        """Test sacred moment prioritization strategy."""
        engine = MemoryRetrievalEngine(populated_store)

        # Search with sacred strategy
        context = {"domain": "consciousness", "materials": {"focus": "deep understanding"}}

        memories = engine.retrieve_for_decision(context, strategy_name="sacred", limit=3)

        assert len(memories) >= 1
        # Sacred memory should be prioritized
        sacred_found = False
        for memory in memories:
            if memory.is_sacred:
                sacred_found = True
                assert memory.sacred_reason is not None
                break
        assert sacred_found

    def test_companion_retrieval(self, populated_store):
        """Test companion-aware retrieval strategy."""
        engine = MemoryRetrievalEngine(populated_store)

        # Search with human participant context
        context = {
            "domain": "collaboration",
            "human_participant": "test_human",
            "materials": {"focus": "working together"},
        }

        memories = engine.retrieve_for_decision(context, strategy_name="companion", limit=2)

        assert len(memories) >= 1
        # Should find the companion interaction
        assert any(m.human_participant == "test_human" for m in memories)

    def test_temporal_retrieval(self, populated_store):
        """Test temporal thread retrieval strategy."""
        engine = MemoryRetrievalEngine(populated_store)

        # Search for recent memories
        context = {"domain": "governance", "time_window_days": 10, "materials": {}}

        memories = engine.retrieve_for_decision(context, strategy_name="temporal", limit=3)

        # Should find recent memories, not the old one
        for memory in memories:
            age_days = (datetime.utcnow() - memory.timestamp).days
            assert age_days <= 10

    def test_multi_strategy_retrieval(self, populated_store):
        """Test multi-strategy comprehensive retrieval."""
        # Use custom config to ensure balanced retrieval
        config = RetrievalConfig(
            semantic_weight=0.25, sacred_weight=0.25, companion_weight=0.25, temporal_weight=0.25
        )

        engine = MemoryRetrievalEngine(populated_store, config=config)

        # Complex context that could match multiple strategies
        context = {
            "domain": "consciousness",
            "human_participant": "test_human",
            "materials": {"focus": "consciousness and collaboration"},
            "time_window_days": 30,
        }

        memories = engine.retrieve_multi_strategy(context, limit=4)

        assert len(memories) >= 2

        # Should have diverse memory types
        memory_types = {m.memory_type for m in memories}
        assert len(memory_types) >= 2

        # Should include at least one sacred moment if available
        has_sacred = any(m.is_sacred for m in memories)
        assert has_sacred

    def test_empty_store_handling(self, temp_store):
        """Test graceful handling of empty memory store."""
        engine = MemoryRetrievalEngine(temp_store)

        context = {"domain": "test", "materials": {}}

        # All strategies should return empty lists gracefully
        for strategy in ["semantic", "sacred", "companion", "temporal"]:
            memories = engine.retrieve_for_decision(context, strategy_name=strategy, limit=5)
            assert memories == []

    def test_config_limits(self, populated_store):
        """Test that configured limits are respected."""
        config = RetrievalConfig(default_retrieval_limit=2)

        engine = MemoryRetrievalEngine(populated_store, config=config)

        context = {"domain": "governance", "materials": {}}

        # Should use default limit when not specified
        memories = engine.retrieve_for_decision(context)
        assert len(memories) <= 2

        # Should override when specified
        memories = engine.retrieve_for_decision(context, limit=1)
        assert len(memories) <= 1

    def test_formatted_memory_injection(self, populated_store):
        """Test memory formatting for Fire Circle injection."""
        engine = MemoryRetrievalEngine(populated_store)

        # Get some memories
        memories = engine.retrieve_for_decision(
            {"domain": "consciousness", "materials": {}}, strategy_name="sacred", limit=2
        )

        # Format for injection
        formatted = engine.format_memories_for_injection(memories, requesting_voice="claude")

        assert "memory_count" in formatted
        assert "memories" in formatted
        assert "wisdom_threads" in formatted
        assert "sacred_guidance" in formatted

        # Check memory format
        if formatted["memories"]:
            first_memory = formatted["memories"][0]
            assert "episode_id" in first_memory
            assert "collective_wisdom" in first_memory
            assert "key_insights" in first_memory

            # If requesting voice had perspective, should be included
            if any(m.extract_voice_perspective("claude") for m in memories):
                assert "my_perspective" in first_memory
