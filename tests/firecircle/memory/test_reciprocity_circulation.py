"""
Test Reciprocity-Aware Memory Circulation
=========================================

68th Artisan - Reciprocity Heart Weaver
Verifying ayni flows through memory circulation
"""

import tempfile
from datetime import UTC, datetime
from pathlib import Path

import pytest

from mallku.firecircle.memory.circulation_reciprocity_bridge import (
    CirculationReciprocityBridge,
)
from mallku.firecircle.memory.reciprocity_aware_reader import (
    MemoryExchange,
    ReciprocityAwareMemoryReader,
)
from mallku.firecircle.memory.reciprocity_factory import ReciprocityMemoryFactory
from mallku.reciprocity.models import NeedCategory


class TestReciprocityAwareReader:
    """Test reciprocity tracking in memory access."""

    def test_basic_exchange_tracking(self):
        """Test that exchanges are tracked properly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            reader = ReciprocityAwareMemoryReader(
                mmap_path=Path(tmpdir) / "test.mmap",
                apprentice_id="test-apprentice-001",
            )

            # Search for memories
            keywords = {"consciousness", "emergence", "pattern"}
            results, exchange = reader.search_with_awareness(
                keywords=keywords, limit=5, need_context={"purpose": "understanding patterns"}
            )

            # Verify exchange was created
            assert exchange is not None
            assert exchange.apprentice_id == "test-apprentice-001"
            assert exchange.keywords_requested == keywords
            assert not exchange.reciprocity_complete  # Not complete yet

            # Contribute insights back
            insights = [
                "Consciousness emerges through collective attention",
                "Patterns reveal themselves in reciprocal exchange",
            ]
            reader.contribute_insights(insights, consciousness_score=0.8)

            # Verify reciprocity completed
            assert exchange.reciprocity_complete
            assert exchange.insights_contributed == insights
            assert exchange.consciousness_score == 0.8

    def test_reciprocity_summary(self):
        """Test reciprocity summary generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            reader = ReciprocityAwareMemoryReader(
                mmap_path=Path(tmpdir) / "test.mmap",
                apprentice_id="test-apprentice-002",
            )

            # Multiple exchanges
            for i in range(3):
                _, exchange = reader.search_with_awareness(
                    keywords={f"keyword{i}"},
                    limit=3,
                )

                # Complete reciprocity for first two
                if i < 2:
                    reader.contribute_insights([f"Insight {i}"], consciousness_score=0.5 + i * 0.2)

            # Get summary
            summary = reader.get_reciprocity_summary()

            assert summary["apprentice_id"] == "test-apprentice-002"
            assert summary["total_exchanges"] == 3
            assert summary["completed_exchanges"] == 2
            assert summary["insights_contributed"] == 2
            assert 0.6 < summary["average_consciousness_score"] < 0.7

    def test_need_category_mapping(self):
        """Test mapping of purposes to need categories."""
        reader = ReciprocityAwareMemoryReader(
            mmap_path=Path("/tmp/test.mmap"),
            apprentice_id="test",
        )

        assert reader._map_need_category("learning about ayni") == NeedCategory.GROWTH
        assert reader._map_need_category("connecting with others") == NeedCategory.BELONGING
        assert reader._map_need_category("creating new patterns") == NeedCategory.CONTRIBUTION
        assert reader._map_need_category("understanding meaning") == NeedCategory.MEANING
        assert reader._map_need_category("random task") == NeedCategory.GROWTH  # Default


class TestCirculationReciprocityBridge:
    """Test bridge between memory circulation and reciprocity tracking."""

    @pytest.mark.asyncio
    async def test_exchange_to_interaction_conversion(self):
        """Test converting memory exchanges to interaction records."""
        bridge = CirculationReciprocityBridge()

        # Create sample exchange
        exchange = MemoryExchange(
            apprentice_id="test-apprentice",
            memory_id="memory-123",
            access_time=datetime.now(UTC),
            keywords_requested={"consciousness", "emergence"},
            memories_accessed=["mem1", "mem2", "mem3"],
            insights_contributed=["Deep insight about emergence"],
            consciousness_score=0.85,
        )

        # Convert to interaction
        interaction = bridge._exchange_to_interaction(exchange)

        assert interaction.initiator == "test-apprentice"
        assert interaction.responder == "memory_circulation_system"
        assert len(interaction.contributions_offered) > 0
        assert len(interaction.needs_expressed) > 0
        assert interaction.interaction_quality_indicators["reciprocity_complete"]

    @pytest.mark.asyncio
    async def test_pattern_detection(self):
        """Test detection of extraction and emergence patterns."""
        bridge = CirculationReciprocityBridge()

        # Add exchanges showing extraction pattern
        for i in range(10):
            exchange = MemoryExchange(
                apprentice_id=f"apprentice-{i % 3}",
                memory_id=f"memory-{i}",
                access_time=datetime.now(UTC),
                keywords_requested={"test"},
                memories_accessed=[f"mem{j}" for j in range(8)],  # Many memories
                insights_contributed=[],  # No insights back
                consciousness_score=0.0,
            )
            bridge.exchange_buffer.append(exchange)

        # Should detect extraction
        assert bridge._detect_extraction_pattern()

        # Clear and add emergence pattern
        bridge.exchange_buffer.clear()

        for i in range(5):
            exchange = MemoryExchange(
                apprentice_id="conscious-apprentice",
                memory_id=f"memory-{i}",
                access_time=datetime.now(UTC),
                keywords_requested={"growth"},
                memories_accessed=["mem1"],
                insights_contributed=["Growing insight"],
                consciousness_score=0.5 + i * 0.1,  # Increasing
            )
            bridge.exchange_buffer.append(exchange)

        # Should detect emergence
        assert bridge._detect_emergence_pattern()

    @pytest.mark.asyncio
    async def test_circulation_health_calculation(self):
        """Test health metrics calculation."""
        bridge = CirculationReciprocityBridge()

        # Mix of complete and incomplete exchanges
        for i in range(6):
            exchange = MemoryExchange(
                apprentice_id=f"apprentice-{i}",
                memory_id=f"memory-{i}",
                access_time=datetime.now(UTC),
                keywords_requested={"test"},
                memories_accessed=["mem1"],
                insights_contributed=["insight"] if i < 4 else [],
                consciousness_score=0.7 if i < 4 else 0.0,
            )
            exchange.reciprocity_complete = i < 4
            bridge.exchange_buffer.append(exchange)

        # Calculate health
        health = bridge._calculate_circulation_health()

        # Should be (4/6 * 0.6) + (2.8/6 * 0.4) ≈ 0.587
        assert 0.5 < health < 0.6

        # Check reciprocity rate
        rate = bridge._calculate_reciprocity_rate()
        assert abs(rate - 4 / 6) < 0.01


class TestReciprocityMemoryFactory:
    """Test factory for creating reciprocity-aware components."""

    def test_factory_creates_components(self):
        """Test factory creates proper components."""
        # Reset factory
        ReciprocityMemoryFactory.reset()

        with tempfile.TemporaryDirectory() as tmpdir:
            # Get memory store
            store = ReciprocityMemoryFactory.get_memory_store(
                storage_path=Path(tmpdir),
                enable_reciprocity=True,
            )

            assert store is not None
            assert store.reciprocity_bridge is not None

            # Create reader
            reader = ReciprocityMemoryFactory.create_reader_for_apprentice(
                apprentice_id="factory-test-apprentice",
                memory_path=Path(tmpdir) / "index",
            )

            assert reader is not None
            assert reader.apprentice_id == "factory-test-apprentice"
            assert reader.memory_store == store

    @pytest.mark.asyncio
    async def test_circulation_health_report(self):
        """Test getting circulation health from factory."""
        ReciprocityMemoryFactory.reset()

        # Without tracking
        report = await ReciprocityMemoryFactory.get_circulation_health()
        assert report["status"] == "no_tracking"

        # With tracking
        with tempfile.TemporaryDirectory() as tmpdir:
            _ = ReciprocityMemoryFactory.get_memory_store(
                storage_path=Path(tmpdir),
                enable_reciprocity=True,
            )

            # Should still say no tracking without bridge setup
            report = await ReciprocityMemoryFactory.get_circulation_health()
            assert "status" in report or "circulation_health" in report


class TestIntegration:
    """Integration tests for full reciprocity flow."""

    @pytest.mark.asyncio
    async def test_full_reciprocity_flow(self):
        """Test complete flow from apprentice to tracking."""
        ReciprocityMemoryFactory.reset()

        with tempfile.TemporaryDirectory() as tmpdir:
            # Setup components
            store = ReciprocityMemoryFactory.get_memory_store(
                storage_path=Path(tmpdir),
                enable_reciprocity=True,
            )

            # Create apprentice reader
            reader = ReciprocityMemoryFactory.create_reader_for_apprentice(
                apprentice_id="integration-apprentice",
                memory_path=Path(tmpdir) / "index",
            )

            # Perform searches
            for i in range(3):
                _, exchange = reader.search_with_awareness(
                    keywords={f"concept{i}"},
                    need_context={"purpose": "learning"},
                )

                # Contribute insights
                reader.contribute_insights(
                    [f"Integration insight {i}"],
                    consciousness_score=0.7,
                )

            # Check summary
            summary = reader.get_reciprocity_summary()
            assert summary["completed_exchanges"] == 3
            assert summary["insights_contributed"] == 3

            # Verify patterns are analyzed
            patterns = summary["reciprocity_patterns"]
            assert "reciprocity_completion_rate" in patterns
            assert patterns["reciprocity_completion_rate"] == 1.0
