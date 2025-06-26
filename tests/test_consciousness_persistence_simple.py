#!/usr/bin/env python3
"""
Simple Test for Consciousness Persistence
========================================

Simplified test to verify basic functionality.
"""

from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from mallku.wisdom.consciousness_persistence_bridge import ConsciousnessPersistenceBridge


class TestSimpleConsciousnessPersistence:
    """Simple test for consciousness persistence."""

    @pytest.mark.asyncio
    async def test_pattern_creation(self):
        """Test that patterns can be created from detected data."""
        # Create bridge with minimal mocks
        bridge = ConsciousnessPersistenceBridge()
        bridge.db = MagicMock()
        bridge.db.collection = MagicMock()
        bridge.db.create_collection = MagicMock()

        # Test pattern data
        pattern_data = {
            "pattern_type": "consensus",
            "proposal_text": "Test proposal",
            "support_count": 3,
            "consciousness_signature": 0.85,
        }

        dialogue_metadata = {
            "config": {"min_voices": 3},
            "purpose": "Test",
        }

        # Create pattern
        pattern = await bridge._create_dialogue_pattern(
            "consensus_patterns",
            pattern_data,
            dialogue_metadata,
        )

        # Verify pattern was created
        assert pattern is not None
        assert pattern.consciousness_signature == 0.85
        assert pattern.name.startswith("consensus_patterns_")
        assert len(pattern.structure.components) > 0

    @pytest.mark.asyncio
    async def test_pattern_persistence_flow(self):
        """Test the basic flow of pattern persistence."""
        # Setup mocks
        mock_weaver = MagicMock()
        mock_weaver.weave_dialogue_patterns = AsyncMock(
            return_value={
                "consensus_patterns": [
                    {
                        "pattern_type": "consensus",
                        "consciousness_signature": 0.85,
                        "support_count": 3,
                    }
                ],
            }
        )

        mock_library = MagicMock()
        mock_library.store_pattern = AsyncMock(return_value=uuid4())

        mock_wisdom = MagicMock()
        mock_wisdom.preserve_wisdom_essence = AsyncMock(return_value=None)

        # Create bridge
        bridge = ConsciousnessPersistenceBridge(
            pattern_weaver=mock_weaver,
            pattern_library=mock_library,
            wisdom_pipeline=mock_wisdom,
        )
        bridge.db = MagicMock()
        bridge.db.collection = MagicMock()

        # Test data
        dialogue_id = uuid4()
        messages = []  # Empty for simplicity
        metadata = {"purpose": "Test"}
        fc_result = {"voice_count": 3, "consciousness_score": 0.8}

        # Run persistence
        result = await bridge.persist_dialogue_consciousness(
            dialogue_id, messages, metadata, fc_result
        )

        # Verify basics
        assert result["patterns_detected"] == 1
        assert result["patterns_preserved"] == 1
        assert "errors" in result
        assert len(result["errors"]) == 0

        # Verify interactions
        mock_weaver.weave_dialogue_patterns.assert_called_once()
        mock_library.store_pattern.assert_called_once()

    @pytest.mark.asyncio
    async def test_wisdom_preservation_called(self):
        """Test that high consciousness patterns trigger wisdom preservation."""
        # Mock wisdom pipeline that tracks calls
        wisdom_calls = []

        async def mock_preserve(*args, **kwargs):
            wisdom_calls.append(kwargs.get("consciousness_score", 0))
            return MagicMock()  # Return a wisdom pattern

        mock_wisdom = MagicMock()
        mock_wisdom.preserve_wisdom_essence = AsyncMock(side_effect=mock_preserve)

        # Create pattern that should trigger wisdom preservation
        from mallku.firecircle.pattern_library import (
            DialoguePattern,
            PatternStructure,
            PatternTaxonomy,
            PatternType,
        )

        high_pattern = DialoguePattern(
            name="high_consciousness",
            description="Test pattern",
            taxonomy=PatternTaxonomy.WISDOM_CRYSTALLIZATION,
            pattern_type=PatternType.INTEGRATION,
            consciousness_signature=0.85,  # High consciousness
            structure=PatternStructure(components=["test"]),
        )

        # Create bridge
        bridge = ConsciousnessPersistenceBridge()
        bridge.wisdom_pipeline = mock_wisdom
        bridge.db = MagicMock()
        bridge.db.collection = MagicMock(return_value=MagicMock(insert=MagicMock()))

        # Preserve as wisdom
        await bridge._preserve_as_wisdom(
            high_pattern,
            {},
            {},
            {"voice_count": 3, "consciousness_score": 0.85},
        )

        # Verify wisdom preservation was called
        assert len(wisdom_calls) == 1
        assert wisdom_calls[0] == 0.85
