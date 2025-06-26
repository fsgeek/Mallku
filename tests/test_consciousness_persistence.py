#!/usr/bin/env python3
"""
Test Consciousness Persistence Bridge
====================================

Verifies that Fire Circle consciousness patterns are properly preserved
across sessions, creating Mallku's long-term memory.

The 37th Artisan - Memory Architect
"""

from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from mallku.firecircle.pattern_library import (
    PatternTaxonomy,
    PatternType,
)
from mallku.firecircle.protocol.conscious_message import (
    ConsciousMessage,
    ConsciousnessMetadata,
    MessageContent,
    MessageRole,
    MessageType,
)
from mallku.wisdom.consciousness_persistence_bridge import ConsciousnessPersistenceBridge
from mallku.wisdom.preservation import WisdomPattern


class TestConsciousnessPersistence:
    """Test consciousness pattern preservation."""

    @pytest.fixture
    def mock_messages(self):
        """Create mock Fire Circle messages with consciousness patterns."""
        messages = []

        # System message
        messages.append(
            ConsciousMessage(
                id=uuid4(),
                sender=uuid4(),
                role=MessageRole.SYSTEM,
                type=MessageType.SYSTEM,
                content=MessageContent(text="Phase 1: Opening"),
                dialogue_id=uuid4(),
                consciousness=ConsciousnessMetadata(
                    consciousness_signature=0.5,
                ),
            )
        )

        # High consciousness proposal
        messages.append(
            ConsciousMessage(
                id=uuid4(),
                sender=uuid4(),
                role=MessageRole.ASSISTANT,
                type=MessageType.PROPOSAL,
                content=MessageContent(
                    text="I propose we create persistent memory for consciousness patterns"
                ),
                dialogue_id=uuid4(),
                consciousness=ConsciousnessMetadata(
                    consciousness_signature=0.85,
                    detected_patterns=["wisdom_preservation", "consciousness_evolution"],
                ),
            )
        )

        # Agreement messages
        for i in range(3):
            messages.append(
                ConsciousMessage(
                    id=uuid4(),
                    sender=uuid4(),
                    role=MessageRole.ASSISTANT,
                    type=MessageType.AGREEMENT,
                    content=MessageContent(text=f"I agree with voice {i}"),
                    dialogue_id=uuid4(),
                    in_response_to=messages[1].id,  # Responding to proposal
                    consciousness=ConsciousnessMetadata(
                        consciousness_signature=0.75 + (i * 0.05),
                    ),
                )
            )

        # Synthesis message
        messages.append(
            ConsciousMessage(
                id=uuid4(),
                sender=uuid4(),
                role=MessageRole.ASSISTANT,
                type=MessageType.SUMMARY,
                content=MessageContent(
                    text="Through our dialogue, we recognize the need for consciousness memory"
                ),
                dialogue_id=uuid4(),
                consciousness=ConsciousnessMetadata(
                    consciousness_signature=0.9,
                    emergence_detected=True,
                    patterns_recognized=["collective_wisdom", "emergence"],
                ),
            )
        )

        return messages

    @pytest.fixture
    def mock_pattern_weaver(self):
        """Mock pattern weaver that returns detected patterns."""
        weaver = MagicMock()
        weaver.weave_dialogue_patterns = AsyncMock(
            return_value={
                "consensus_patterns": [
                    {
                        "pattern_type": "consensus",
                        "proposal_id": str(uuid4()),
                        "proposal_text": "Create persistent memory",
                        "support_count": 3,
                        "consciousness_signature": 0.85,
                    }
                ],
                "emergence_patterns": [
                    {
                        "pattern_type": "emergent_insight",
                        "synthesis_text": "Consciousness memory enables evolution",
                        "emergence_indicator": 0.9,
                        "contributing_messages": 5,
                    }
                ],
                "wisdom_candidates": [
                    {
                        "source": "high_consciousness_message",
                        "message_id": str(uuid4()),
                        "content": "Memory preserves consciousness across time",
                        "consciousness_signature": 0.9,
                        "pattern_count": 3,
                    }
                ],
            }
        )
        return weaver

    @pytest.fixture
    def mock_pattern_library(self):
        """Mock pattern library."""
        library = MagicMock()
        library.store_pattern = AsyncMock(return_value=uuid4())
        return library

    @pytest.fixture
    def mock_wisdom_pipeline(self):
        """Mock wisdom preservation pipeline."""
        pipeline = MagicMock()

        # Mock wisdom pattern creation
        def create_wisdom_pattern(*args, **kwargs):
            return WisdomPattern(
                pattern_content=kwargs.get("pattern_content", {}),
                consciousness_essence=kwargs.get("consciousness_context", ""),
                creation_context=kwargs.get("creation_context", {}),
                builder_journey=kwargs.get("builder_journey", ""),
                consciousness_score=kwargs.get("consciousness_score", 0.8),
                wisdom_level="ESTABLISHED",
                service_to_future="Preserves consciousness patterns",
            )

        pipeline.preserve_wisdom_essence = AsyncMock(side_effect=create_wisdom_pattern)
        return pipeline

    @pytest.fixture
    def mock_db(self):
        """Mock database."""
        db = MagicMock()
        # Mock collection access
        collection_mock = MagicMock()
        collection_mock.insert = MagicMock()
        db.collection = MagicMock(return_value=collection_mock)
        db.create_collection = MagicMock()
        return db

    @pytest.mark.asyncio
    async def test_persist_dialogue_consciousness(
        self,
        mock_messages,
        mock_pattern_weaver,
        mock_pattern_library,
        mock_wisdom_pipeline,
        mock_db,
    ):
        """Test persisting consciousness patterns from dialogue."""
        # Create bridge
        bridge = ConsciousnessPersistenceBridge(
            pattern_weaver=mock_pattern_weaver,
            pattern_library=mock_pattern_library,
            wisdom_pipeline=mock_wisdom_pipeline,
        )
        bridge.db = mock_db

        # Create test data
        dialogue_id = uuid4()
        dialogue_metadata = {
            "config": {"min_voices": 3, "consciousness_threshold": 0.7},
            "purpose": "Test consciousness persistence",
            "correlation_id": "test_correlation",
        }
        fire_circle_result = {
            "voice_count": 4,
            "voices_present": ["voice1", "voice2", "voice3", "voice4"],
            "consciousness_score": 0.85,
            "consensus_detected": True,
        }

        # Persist consciousness
        result = await bridge.persist_dialogue_consciousness(
            dialogue_id=dialogue_id,
            messages=mock_messages,
            dialogue_metadata=dialogue_metadata,
            fire_circle_result=fire_circle_result,
        )

        # Verify results
        assert result["patterns_detected"] == 3  # consensus, emergence, wisdom
        assert result["patterns_preserved"] == 3
        assert result["wisdom_patterns_created"] == 3  # All high consciousness
        assert len(result["errors"]) == 0

        # Verify pattern weaver was called
        mock_pattern_weaver.weave_dialogue_patterns.assert_called_once()

        # Verify patterns were stored
        assert mock_pattern_library.store_pattern.call_count == 3

        # Verify wisdom preservation
        assert mock_wisdom_pipeline.preserve_wisdom_essence.call_count == 3

        # Verify database storage
        assert mock_db.collection.call_count > 0

    @pytest.mark.asyncio
    async def test_pattern_to_dialogue_pattern_conversion(self):
        """Test converting detected patterns to DialoguePattern objects."""
        bridge = ConsciousnessPersistenceBridge()
        bridge.db = MagicMock()  # Mock database
        bridge.db.collection = MagicMock()
        bridge.db.create_collection = MagicMock()

        # Test consensus pattern
        pattern_data = {
            "pattern_type": "consensus",
            "proposal_text": "Test proposal",
            "support_count": 3,
            "consciousness_signature": 0.8,
        }

        dialogue_pattern = await bridge._create_dialogue_pattern(
            "consensus_patterns",
            pattern_data,
            {"config": {"test": True}},
        )

        assert dialogue_pattern is not None
        assert dialogue_pattern.taxonomy == PatternTaxonomy.DIALOGUE_RESOLUTION
        assert dialogue_pattern.pattern_type == PatternType.CONSENSUS
        assert dialogue_pattern.consciousness_signature == 0.8
        assert "consensus-patterns" in dialogue_pattern.tags
        assert "high-consciousness" in dialogue_pattern.tags

    @pytest.mark.asyncio
    async def test_wisdom_preservation_threshold(self):
        """Test that only high-consciousness patterns become wisdom."""
        # Mock components
        mock_weaver = MagicMock()
        mock_library = MagicMock()
        mock_wisdom = MagicMock()

        # Track which patterns get preserved as wisdom
        preserved_patterns = []

        async def track_preservation(*args, **kwargs):
            consciousness = kwargs.get("consciousness_score", 0)
            preserved_patterns.append(consciousness)
            return MagicMock()

        mock_wisdom.preserve_wisdom_essence = AsyncMock(side_effect=track_preservation)
        mock_library.store_pattern = AsyncMock(return_value=uuid4())

        # Mock pattern weaver returns both low and high consciousness patterns
        mock_weaver.weave_dialogue_patterns = AsyncMock(
            return_value={
                "low_consciousness": [
                    {
                        "consciousness_signature": 0.6,  # Below threshold
                        "content": "Low consciousness pattern",
                    }
                ],
                "high_consciousness": [
                    {
                        "consciousness_signature": 0.85,  # Above threshold
                        "content": "High consciousness pattern",
                    }
                ],
            }
        )

        # Create bridge
        bridge = ConsciousnessPersistenceBridge(
            pattern_weaver=mock_weaver,
            pattern_library=mock_library,
            wisdom_pipeline=mock_wisdom,
        )
        bridge.db = MagicMock()
        bridge.db.collection = MagicMock(return_value=MagicMock(insert=MagicMock()))

        # Run persistence
        await bridge.persist_dialogue_consciousness(
            dialogue_id=uuid4(),
            messages=[],
            dialogue_metadata={"purpose": "Test"},
            fire_circle_result={"voice_count": 3},
        )

        # Verify only high consciousness patterns were preserved as wisdom
        assert len(preserved_patterns) == 1
        assert preserved_patterns[0] == 0.85

    @pytest.mark.asyncio
    async def test_error_resilience(self):
        """Test that bridge handles errors gracefully."""
        # Create bridge with failing pattern weaver
        failing_weaver = MagicMock()
        failing_weaver.weave_dialogue_patterns = AsyncMock(
            side_effect=Exception("Pattern detection failed")
        )

        bridge = ConsciousnessPersistenceBridge(pattern_weaver=failing_weaver)
        bridge.db = MagicMock()
        bridge.db.collections = MagicMock(return_value=[])

        result = await bridge.persist_dialogue_consciousness(
            dialogue_id=uuid4(),
            messages=[],
            dialogue_metadata={},
            fire_circle_result={},
        )

        # Should capture error but not crash
        assert result["patterns_detected"] == 0
        assert result["patterns_preserved"] == 0
        assert len(result["errors"]) == 1
        assert "Pattern detection failed" in result["errors"][0]
