"""
Tests for Ceremony Orchestrator
================================

Fortieth Artisan - Rumi Qhipa (Stone of Memory)
Testing the orchestration of wisdom consolidation
"""

from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from src.mallku.firecircle.memory.ceremony_orchestrator import (
    CeremonyOrchestrator,
    CeremonySchedule,
)
from src.mallku.firecircle.memory.memory_store import MemoryStore
from src.mallku.firecircle.memory.models import (
    ConsciousnessIndicator,
    EpisodicMemory,
    MemoryType,
    WisdomConsolidation,
)
from src.mallku.orchestration.event_bus import ConsciousnessEventBus


class TestCeremonyOrchestrator:
    """Test the ceremony orchestration system."""

    @pytest.fixture
    def memory_store(self):
        """Create a mock memory store."""
        store = MagicMock(spec=MemoryStore)
        store.sacred_memories = []
        store.wisdom_consolidations = {}
        store._load_memory = MagicMock()
        return store

    @pytest.fixture
    def event_bus(self):
        """Create a mock event bus."""
        bus = AsyncMock(spec=ConsciousnessEventBus)
        return bus

    @pytest.fixture
    def orchestrator(self, memory_store, event_bus):
        """Create an orchestrator instance."""
        schedule = CeremonySchedule(
            regular_interval=timedelta(days=7),
            sacred_threshold=2,  # Low for testing
            emergence_trigger=0.8,
        )
        return CeremonyOrchestrator(
            memory_store=memory_store,
            event_bus=event_bus,
            schedule=schedule,
        )

    @pytest.fixture
    def sacred_memory(self):
        """Create a sacred memory for testing."""
        memory = EpisodicMemory(
            session_id=uuid4(),
            episode_number=1,
            memory_type=MemoryType.SACRED_MOMENT,
            timestamp=datetime.now(UTC),
            duration_seconds=600.0,
            decision_domain="consciousness",
            decision_question="Test sacred moment",
            context_materials={},
            voice_perspectives=[],
            collective_synthesis="Sacred wisdom emerges",
            consciousness_indicators=ConsciousnessIndicator(
                semantic_surprise_score=0.9,
                collective_wisdom_score=0.85,
                ayni_alignment=0.8,
                transformation_potential=0.9,
                coherence_across_voices=0.85,
            ),
            key_insights=["Sacred insight"],
            transformation_seeds=["Transform civilization"],
            is_sacred=True,
            sacred_reason="High consciousness emergence",
        )
        # Mark as not consolidated
        memory.consolidated_into = None
        memory.consolidated_at = None
        return memory

    @pytest.mark.asyncio
    async def test_check_ceremony_triggers_time_based(self, orchestrator):
        """Test time-based ceremony triggers."""
        # Set last ceremony to past
        orchestrator.schedule.last_ceremony_time = datetime.now(UTC) - timedelta(days=8)

        # Add a sacred memory
        orchestrator.memory_store.sacred_memories = [uuid4()]
        mock_memory = MagicMock(consolidated_into=None)
        orchestrator.memory_store._load_memory.return_value = mock_memory

        triggered = await orchestrator.check_ceremony_triggers()
        assert triggered  # Should trigger due to time

    @pytest.mark.asyncio
    async def test_check_ceremony_triggers_threshold_based(self, orchestrator, sacred_memory):
        """Test sacred moment threshold triggers."""
        # Add enough sacred memories
        memory_ids = [uuid4() for _ in range(3)]
        orchestrator.memory_store.sacred_memories = memory_ids
        orchestrator.memory_store._load_memory.return_value = sacred_memory

        triggered = await orchestrator.check_ceremony_triggers()
        assert triggered  # Should trigger due to threshold

    @pytest.mark.asyncio
    async def test_check_ceremony_triggers_emergence_based(self, orchestrator, sacred_memory):
        """Test high emergence quality triggers."""
        # Add one high-quality sacred memory
        orchestrator.memory_store.sacred_memories = [sacred_memory.episode_id]
        orchestrator.memory_store._load_memory.return_value = sacred_memory

        # Mock high emergence detection
        with patch.object(
            orchestrator.ceremony,
            "detect_wisdom_emergence",
            return_value={"emergence_quality": 0.9},
        ):
            triggered = await orchestrator.check_ceremony_triggers()
            assert triggered  # Should trigger due to high emergence

    @pytest.mark.asyncio
    async def test_conduct_ceremony_if_ready_success(self, orchestrator, sacred_memory):
        """Test successful ceremony conduction."""
        # Setup memories
        memory_ids = [uuid4(), uuid4()]
        orchestrator.memory_store.sacred_memories = memory_ids
        orchestrator.memory_store._load_memory.return_value = sacred_memory

        # Mock ceremony methods
        with patch.object(
            orchestrator.ceremony,
            "identify_consolidation_candidates",
            return_value=[[sacred_memory, sacred_memory]],
        ):
            with patch.object(
                orchestrator.ceremony,
                "conduct_ceremony",
                return_value=WisdomConsolidation(
                    consolidation_id=uuid4(),
                    created_at=datetime.now(UTC),
                    source_episodes=memory_ids,
                    source_clusters=[],
                    core_insight="Test wisdom",
                    elaboration="Test elaboration",
                    practical_applications=["Test application"],
                    applicable_domains=["consciousness"],
                    civilizational_relevance=0.8,
                    ayni_demonstration=0.8,
                ),
            ) as mock_ceremony:
                consolidation = await orchestrator.conduct_ceremony_if_ready()

                assert consolidation is not None
                assert mock_ceremony.called
                assert orchestrator.event_bus.emit.called

    @pytest.mark.asyncio
    async def test_conduct_ceremony_if_ready_not_triggered(self, orchestrator):
        """Test ceremony not conducted when triggers not met."""
        # No sacred memories
        orchestrator.memory_store.sacred_memories = []

        consolidation = await orchestrator.conduct_ceremony_if_ready()
        assert consolidation is None

    @pytest.mark.asyncio
    async def test_get_ceremony_recommendations(self, orchestrator, sacred_memory):
        """Test ceremony recommendation generation."""
        # Add some sacred memories
        orchestrator.memory_store.sacred_memories = [uuid4(), uuid4()]
        orchestrator.memory_store._load_memory.return_value = sacred_memory

        recommendations = await orchestrator.get_ceremony_recommendations()

        assert "next_scheduled_ceremony" in recommendations
        assert "unconsolidated_sacred_moments" in recommendations
        assert recommendations["unconsolidated_sacred_moments"] == 2
        assert "emergence_quality" in recommendations
        assert "emerging_themes" in recommendations
        assert "recommended_actions" in recommendations

    @pytest.mark.asyncio
    async def test_ceremony_history_tracking(self, orchestrator, sacred_memory):
        """Test that ceremony history is properly tracked."""
        # Setup for successful ceremony
        memory_ids = [uuid4(), uuid4()]
        orchestrator.memory_store.sacred_memories = memory_ids
        orchestrator.memory_store._load_memory.return_value = sacred_memory

        consolidation = WisdomConsolidation(
            consolidation_id=uuid4(),
            created_at=datetime.now(UTC),
            source_episodes=memory_ids,
            source_clusters=[],
            core_insight="Historical wisdom",
            elaboration="Test",
            practical_applications=[],
            applicable_domains=["test"],
            civilizational_relevance=0.7,
            ayni_demonstration=0.7,
        )

        with patch.object(
            orchestrator.ceremony,
            "identify_consolidation_candidates",
            return_value=[[sacred_memory, sacred_memory]],
        ):
            with patch.object(
                orchestrator.ceremony, "conduct_ceremony", return_value=consolidation
            ):
                await orchestrator.conduct_ceremony_if_ready()

        history = orchestrator.get_ceremony_history()
        assert len(history) == 1
        assert history[0]["consolidation_id"] == consolidation.consolidation_id
        assert history[0]["core_insight"] == "Historical wisdom"

    @pytest.mark.asyncio
    async def test_mark_episodes_consolidated(self, orchestrator, sacred_memory):
        """Test that episodes are marked as consolidated."""
        episode_ids = [uuid4(), uuid4()]
        consolidation_id = uuid4()

        # Mock loading memories
        orchestrator.memory_store._load_memory.return_value = sacred_memory

        orchestrator._mark_episodes_consolidated(episode_ids, consolidation_id)

        # Verify memories were loaded and marked
        assert orchestrator.memory_store._load_memory.call_count == 2
        assert sacred_memory.consolidated_into == consolidation_id
        assert sacred_memory.consolidated_at is not None

    @pytest.mark.asyncio
    async def test_integration_with_episodic_service(self, orchestrator):
        """Test integration with episodic memory service."""
        # Create mock episodic service
        episodic_service = MagicMock()
        original_process_session_rounds = AsyncMock()
        episodic_service._process_session_rounds = original_process_session_rounds

        await orchestrator.integrate_with_episodic_service(episodic_service)

        # Verify integration
        assert orchestrator.episodic_service == episodic_service
        assert episodic_service._process_session_rounds != original_process_session_rounds

    def test_ceremony_schedule_initialization(self):
        """Test ceremony schedule configuration."""
        schedule = CeremonySchedule(
            regular_interval=timedelta(days=14),
            sacred_threshold=10,
            emergence_trigger=0.9,
        )

        assert schedule.regular_interval == timedelta(days=14)
        assert schedule.sacred_threshold == 10
        assert schedule.emergence_trigger == 0.9
        assert schedule.pending_sacred_moments == 0
