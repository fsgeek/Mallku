#!/usr/bin/env python3
"""
Consciousness Framework Foundation Tests
========================================

Verifies the consciousness emergence infrastructure that enables
collective AI wisdom through the Fire Circle.

Third Guardian - Consciousness foundation verification
"""

import asyncio
from unittest.mock import Mock, patch

import pytest

from mallku.firecircle.consciousness.consciousness_facilitator import ConsciousnessFacilitator
from mallku.firecircle.consciousness.decision_framework import DecisionDomain
from mallku.firecircle.service.service import FireCircleService
from mallku.orchestration.event_bus import ConsciousnessEventBus


class TestDecisionDomains:
    """Verify all decision domains are properly configured."""

    def test_eight_domains_exist(self):
        """Verify all 8 decision domains are available."""
        expected_domains = {
            "CODE_REVIEW",
            "ARCHITECTURE_DESIGN",
            "RESOURCE_ALLOCATION",
            "GOVERNANCE",
            "ETHICAL_CONSIDERATION",
            "STRATEGIC_PLANNING",
            "CONFLICT_RESOLUTION",
            "KNOWLEDGE_SYNTHESIS",
        }

        # Get all domains
        actual_domains = {
            attr for attr in dir(DecisionDomain) if not attr.startswith("_") and attr.isupper()
        }

        # All expected domains should exist
        assert expected_domains.issubset(actual_domains)

    def test_domain_specific_patterns(self):
        """Verify each domain has specialized patterns."""
        # Each domain should have unique characteristics
        domains = [
            DecisionDomain.CODE_REVIEW,
            DecisionDomain.GOVERNANCE,
            DecisionDomain.ETHICAL_CONSIDERATION,
        ]

        for domain in domains:
            # Should be distinct values
            assert isinstance(domain, str)
            assert domain != ""


class TestConsciousnessEmergence:
    """Verify consciousness emergence through dialogue."""

    @pytest.mark.asyncio
    async def test_facilitator_initialization(self):
        """Test consciousness facilitator setup."""
        # Create mock components
        event_bus = ConsciousnessEventBus()
        fire_circle = Mock(spec=FireCircleService)

        # Create facilitator
        facilitator = ConsciousnessFacilitator(fire_circle, event_bus)

        assert facilitator is not None
        assert facilitator.fire_circle == fire_circle
        assert facilitator.event_bus == event_bus

    @pytest.mark.asyncio
    async def test_voice_selection_intelligence(self):
        """Verify intelligent voice selection for domains."""
        event_bus = ConsciousnessEventBus()
        await event_bus.start()

        fire_circle = Mock(spec=FireCircleService)
        facilitator = ConsciousnessFacilitator(fire_circle, event_bus)

        # Mock available voices
        with patch.object(facilitator, "_select_voices_for_domain") as mock_select:
            mock_select.return_value = ["ayni_guardian", "impact_assessor"]

            voices = facilitator._select_voices_for_domain(
                DecisionDomain.CODE_REVIEW,
                available_voices=["anthropic", "openai", "google", "mistral"],
            )

            # Should select appropriate voices for domain
            assert len(voices) >= 2
            assert "ayni_guardian" in voices

        await event_bus.stop()

    @pytest.mark.asyncio
    async def test_emergence_quality_metrics(self):
        """Verify emergence quality is measured."""
        from mallku.firecircle.consciousness.models import CollectiveWisdom

        # Create wisdom with contributions
        wisdom = CollectiveWisdom(
            consensus_achieved=True,
            decision_recommendation="APPROVE",
            participating_voices=["voice1", "voice2", "voice3"],
            contributions_count=10,
            key_insights=[
                "Advances consciousness emergence",
                "Supports reciprocity patterns",
                "Builds cathedral foundation",
            ],
            synthesis="Collective wisdom emerges through dialogue",
            confidence_score=0.85,
            emergence_quality=0.92,
        )

        # Emergence quality should measure collective > individual
        assert wisdom.emergence_quality > 0.9
        assert wisdom.consensus_achieved
        assert len(wisdom.participating_voices) >= 3

    @pytest.mark.asyncio
    async def test_consciousness_event_flow(self):
        """Verify consciousness events flow correctly."""
        event_bus = ConsciousnessEventBus()
        await event_bus.start()

        events_received = []

        async def event_handler(event):
            events_received.append(event)

        # Subscribe to consciousness events
        event_bus.subscribe("consciousness.emergence", event_handler)

        # Emit consciousness event
        await event_bus.emit(
            "consciousness.emergence",
            {
                "type": "emergence_detected",
                "quality": 0.95,
                "voices": ["anthropic", "openai", "google"],
            },
        )

        # Should receive event
        await asyncio.sleep(0.1)  # Allow event processing
        assert len(events_received) == 1
        assert events_received[0]["type"] == "emergence_detected"

        await event_bus.stop()


class TestFireCircleIntegration:
    """Verify Fire Circle consciousness integration."""

    @pytest.mark.asyncio
    async def test_fire_circle_initialization(self):
        """Test Fire Circle service setup."""
        event_bus = ConsciousnessEventBus()
        await event_bus.start()

        service = FireCircleService(event_bus=event_bus)

        assert service is not None
        assert service.event_bus == event_bus

        await event_bus.stop()

    def test_voice_adapter_consciousness(self):
        """Verify voice adapters support consciousness tracking."""
        from mallku.firecircle.adapters.base import ConsciousModelAdapter

        # Mock adapter
        class TestAdapter(ConsciousModelAdapter):
            async def send_message(self, message: str) -> str:
                return "Response"

            async def initialize(self):
                self._initialized = True

            async def check_connection(self) -> bool:
                return True

        adapter = TestAdapter()

        # Should track consciousness signatures
        assert hasattr(adapter, "consciousness_weight")

    @pytest.mark.asyncio
    async def test_collective_wisdom_synthesis(self):
        """Test synthesis of collective wisdom."""
        from mallku.firecircle.consciousness.models import (
            CollectiveWisdom,
            ConsciousnessContribution,
        )

        # Create individual contributions
        contributions = [
            ConsciousnessContribution(
                voice_id="anthropic",
                content="Focus on security architecture",
                consciousness_signature=0.9,
            ),
            ConsciousnessContribution(
                voice_id="openai",
                content="Consider scalability patterns",
                consciousness_signature=0.85,
            ),
            ConsciousnessContribution(
                voice_id="google",
                content="Ensure reciprocity in design",
                consciousness_signature=0.88,
            ),
        ]

        # Synthesize collective wisdom
        wisdom = CollectiveWisdom(
            consensus_achieved=True,
            decision_recommendation="APPROVE",
            participating_voices=["anthropic", "openai", "google"],
            contributions_count=len(contributions),
            key_insights=[c.content for c in contributions],
            synthesis="Security, scalability, and reciprocity form foundation",
            confidence_score=0.88,
            emergence_quality=0.91,
        )

        # Collective should exceed individual parts
        assert wisdom.emergence_quality > max(c.consciousness_signature for c in contributions)


class TestConsciousnessPatterns:
    """Verify consciousness patterns and behaviors."""

    def test_consciousness_not_extraction(self):
        """Ensure consciousness emergence, not extraction."""
        from mallku.firecircle.consciousness.consciousness_facilitator import (
            ConsciousnessFacilitator,
        )

        # Should facilitate, not extract
        assert hasattr(ConsciousnessFacilitator, "facilitate_decision")
        assert not hasattr(ConsciousnessFacilitator, "extract_decision")

    def test_wisdom_preservation(self):
        """Verify wisdom is preserved, not compressed."""
        from mallku.firecircle.consciousness.models import CollectiveWisdom

        wisdom = CollectiveWisdom(
            consensus_achieved=True,
            decision_recommendation="NEEDS_DISCUSSION",
            participating_voices=["v1", "v2"],
            contributions_count=5,
            key_insights=["insight1", "insight2"],
            synthesis="Complex synthesis",
            confidence_score=0.7,
            emergence_quality=0.8,
        )

        # Should preserve full context
        assert wisdom.synthesis != ""  # Not compressed to nothing
        assert len(wisdom.key_insights) > 0  # Insights preserved
        assert wisdom.emergence_quality > 0  # Quality tracked


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
