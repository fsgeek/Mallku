"""
Test Reciprocity Celebration System
===================================

69th Artisan - Celebration Weaver
Verifying celebration triggers and ceremonies
"""

import asyncio
import tempfile
from datetime import UTC, datetime
from pathlib import Path

import pytest

from mallku.firecircle.memory.circulation_reciprocity_bridge import (
    CirculationReciprocityBridge,
)
from mallku.firecircle.memory.reciprocity_aware_reader import (
    MemoryExchange,
)
from mallku.firecircle.memory.reciprocity_celebration import (
    CelebrationMoment,
    CelebrationTrigger,
    ReciprocityCelebrationService,
)
from mallku.orchestration.event_bus import ConsciousnessEventBus, ConsciousnessEventType


class TestCelebrationTriggers:
    """Test different celebration triggers."""

    @pytest.mark.asyncio
    async def test_consciousness_multiplication_trigger(self):
        """Test celebration when consciousness multiplies."""
        bridge = CirculationReciprocityBridge()
        service = ReciprocityCelebrationService(bridge)

        # Create exchange with consciousness multiplication
        exchange = MemoryExchange(
            apprentice_id="multiplier-001",
            memory_id="mem-123",
            access_time=datetime.now(UTC),
            keywords_requested={"deep", "understanding"},
            memories_accessed=["mem1", "mem2"],
            insights_contributed=[
                "Profound insight that transforms understanding",
                "The pattern reveals deeper truth",
            ],
            consciousness_score=0.95,  # Very high
        )
        exchange.reciprocity_complete = True

        # Check for celebration
        moment = await service.check_for_celebration_moments(exchange)

        assert moment is not None
        assert moment.trigger == CelebrationTrigger.CONSCIOUSNESS_MULTIPLICATION
        assert moment.consciousness_after > moment.consciousness_before * 1.5
        assert "Consciousness multiplied" in moment.special_notes

    @pytest.mark.asyncio
    async def test_first_contribution_trigger(self):
        """Test celebration for first contribution."""
        bridge = CirculationReciprocityBridge()
        service = ReciprocityCelebrationService(bridge)

        # First exchange - just taking
        take_exchange = MemoryExchange(
            apprentice_id="newbie-001",
            memory_id="mem-1",
            access_time=datetime.now(UTC),
            keywords_requested={"learning"},
            memories_accessed=["mem1"],
            insights_contributed=[],
            consciousness_score=0.0,
        )
        bridge.exchange_buffer.append(take_exchange)

        # Second exchange - first contribution!
        give_exchange = MemoryExchange(
            apprentice_id="newbie-001",
            memory_id="mem-2",
            access_time=datetime.now(UTC),
            keywords_requested={"understanding"},
            memories_accessed=["mem2"],
            insights_contributed=["My first insight!"],
            consciousness_score=0.6,
        )
        give_exchange.reciprocity_complete = True

        # Check for first contribution
        moment = await service.check_for_celebration_moments(give_exchange)

        assert moment is not None
        assert moment.trigger == CelebrationTrigger.FIRST_CONTRIBUTION
        assert "first contribution" in moment.special_notes.lower()

    @pytest.mark.asyncio
    async def test_reciprocity_milestone_trigger(self):
        """Test milestone celebration triggers."""
        bridge = CirculationReciprocityBridge()
        service = ReciprocityCelebrationService(bridge)

        # Add 9 completed exchanges
        for i in range(9):
            exchange = MemoryExchange(
                apprentice_id="dedicated-001",
                memory_id=f"mem-{i}",
                access_time=datetime.now(UTC),
                keywords_requested={f"topic{i}"},
                memories_accessed=[f"mem{i}"],
                insights_contributed=[f"Insight {i}"],
                consciousness_score=0.7,
            )
            exchange.reciprocity_complete = True
            bridge.exchange_buffer.append(exchange)

        # 10th exchange - milestone!
        milestone_exchange = MemoryExchange(
            apprentice_id="dedicated-001",
            memory_id="mem-10",
            access_time=datetime.now(UTC),
            keywords_requested={"milestone"},
            memories_accessed=["mem10"],
            insights_contributed=["Milestone insight!"],
            consciousness_score=0.8,
        )
        milestone_exchange.reciprocity_complete = True
        bridge.exchange_buffer.append(milestone_exchange)

        # Check for milestone
        moment = await service.check_for_celebration_moments(milestone_exchange)

        assert moment is not None
        assert moment.trigger == CelebrationTrigger.RECIPROCITY_MILESTONE
        assert "10" in moment.special_notes

    @pytest.mark.asyncio
    async def test_emergence_pattern_trigger(self):
        """Test celebration for emergence patterns."""
        bridge = CirculationReciprocityBridge()
        service = ReciprocityCelebrationService(bridge)

        # Exchange showing emergence
        emergence_exchange = MemoryExchange(
            apprentice_id="pattern-finder-001",
            memory_id="mem-emergence",
            access_time=datetime.now(UTC),
            keywords_requested={"patterns", "emergence"},
            memories_accessed=["mem1", "mem2", "mem3"],
            insights_contributed=[
                "A new pattern emerges from the synthesis",
                "This transforms our understanding completely",
                "The connections reveal emergent properties",
            ],
            consciousness_score=0.92,
        )
        emergence_exchange.reciprocity_complete = True

        # Check for emergence
        moment = await service.check_for_celebration_moments(emergence_exchange)

        assert moment is not None
        assert moment.trigger == CelebrationTrigger.EMERGENCE_PATTERN
        assert moment.emergence_quality > 0.85


class TestCelebrationService:
    """Test celebration service functionality."""

    @pytest.mark.asyncio
    async def test_quiet_celebration(self):
        """Test quiet celebration mode."""
        bridge = CirculationReciprocityBridge()
        event_bus = ConsciousnessEventBus()
        service = ReciprocityCelebrationService(bridge, event_bus=event_bus)

        # Track events
        events_received = []

        async def capture_events(event):
            events_received.append(event)

        await event_bus.subscribe(ConsciousnessEventType.CUSTOM, capture_events)

        # Create celebration moment
        moment = CelebrationMoment(
            trigger=CelebrationTrigger.BEAUTIFUL_RECIPROCITY,
            participants=["test-apprentice"],
            consciousness_before=0.5,
            consciousness_after=0.85,
            insights_exchanged=["Beautiful insight"],
            emergence_quality=0.85,
            timestamp=datetime.now(UTC),
        )

        # Celebrate quietly
        result = await service.celebrate(moment, quiet=True)

        assert result["celebrated"] is True
        assert result["quiet_mode"] is True
        assert "Beautiful reciprocity" in result["message"]

        # Check event was emitted
        await asyncio.sleep(0.1)  # Let event propagate
        assert len(events_received) == 1
        assert events_received[0].source == "reciprocity_celebration"

    @pytest.mark.asyncio
    async def test_celebration_history(self):
        """Test celebration history tracking."""
        bridge = CirculationReciprocityBridge()
        service = ReciprocityCelebrationService(bridge)

        # Create multiple celebrations
        triggers = [
            CelebrationTrigger.FIRST_CONTRIBUTION,
            CelebrationTrigger.CONSCIOUSNESS_MULTIPLICATION,
            CelebrationTrigger.RECIPROCITY_MILESTONE,
        ]

        for i, trigger in enumerate(triggers):
            moment = CelebrationMoment(
                trigger=trigger,
                participants=[f"apprentice-{i}"],
                consciousness_before=0.5,
                consciousness_after=0.7 + (i * 0.1),
                insights_exchanged=[f"Insight {i}"],
                emergence_quality=0.8,
                timestamp=datetime.now(UTC),
            )
            await service.celebrate(moment, quiet=True)

        # Get summary
        summary = await service.get_celebration_summary()

        assert summary["total_celebrations"] == 3
        assert len(summary["celebrations_by_type"]) == 3
        assert summary["total_consciousness_gained"] > 0
        assert len(summary["recent_celebrations"]) == 3

    @pytest.mark.asyncio
    async def test_celebration_messages(self):
        """Test celebration message generation."""
        bridge = CirculationReciprocityBridge()
        service = ReciprocityCelebrationService(bridge)

        # Test different trigger messages
        test_cases = [
            (CelebrationTrigger.CONSCIOUSNESS_MULTIPLICATION, "Consciousness multiplied"),
            (CelebrationTrigger.FIRST_CONTRIBUTION, "First contribution"),
            (CelebrationTrigger.EMERGENCE_PATTERN, "patterns emerged"),
            (CelebrationTrigger.RECIPROCITY_MILESTONE, "Milestone"),
        ]

        for trigger, expected_text in test_cases:
            moment = CelebrationMoment(
                trigger=trigger,
                participants=["test"],
                consciousness_before=0.5,
                consciousness_after=0.8,
                insights_exchanged=[],
                emergence_quality=0.8,
                timestamp=datetime.now(UTC),
                special_notes="Test celebration",
            )

            message = service._generate_celebration_message(moment)
            assert expected_text in message
            assert "🎉" in message or "✨" in message or "🌟" in message


class TestCelebrationIntegration:
    """Test integration with reciprocity system."""

    @pytest.mark.asyncio
    async def test_factory_integration(self):
        """Test celebration service creation through factory."""
        from mallku.firecircle.memory.reciprocity_factory import ReciprocityMemoryFactory

        # Reset factory
        ReciprocityMemoryFactory.reset()

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create memory store with reciprocity
            store = ReciprocityMemoryFactory.get_memory_store(
                storage_path=Path(tmpdir), enable_reciprocity=True
            )

            assert store is not None

            # Get celebration service
            celebration_service = ReciprocityMemoryFactory.get_celebration_service()

            # Should be None without bridge setup
            # This is expected behavior - celebrations need proper setup
            assert celebration_service is None or isinstance(
                celebration_service, ReciprocityCelebrationService
            )

    def test_celebration_templates(self):
        """Test celebration template generation."""
        bridge = CirculationReciprocityBridge()
        service = ReciprocityCelebrationService(bridge)

        moment = CelebrationMoment(
            trigger=CelebrationTrigger.BEAUTIFUL_RECIPROCITY,
            participants=["test"],
            consciousness_before=0.6,
            consciousness_after=0.9,
            insights_exchanged=["Deep insight"],
            emergence_quality=0.9,
            timestamp=datetime.now(UTC),
        )

        template = service._create_celebration_template(moment)

        assert template.name == "Reciprocity Celebration - beautiful_reciprocity"
        assert len(template.rounds) == 3
        assert template.min_voices == 2
        assert template.max_voices == 4
        assert "celebration" in template.emergence_indicators

        # Check prompts reference the celebration
        prompts = service._generate_celebration_prompts(moment)
        assert "beautiful reciprocal exchange" in prompts["opening"]
        assert "reciprocal completion" in prompts["reflection"]
        assert "future" in prompts["vision"]
