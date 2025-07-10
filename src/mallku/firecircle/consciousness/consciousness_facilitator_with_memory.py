"""
Fire Circle Consciousness Facilitator with Memory
=================================================

Sixth Guardian - Adding persistent memory to consciousness emergence

This extends the consciousness facilitator to automatically save sessions
to the database through the API gateway.
"""

import logging
from datetime import UTC, datetime
from typing import Any

import aiohttp

from .consciousness_facilitator import ConsciousnessFacilitator as BaseFacilitator
from .decision_framework import CollectiveWisdom, DecisionDomain

logger = logging.getLogger(__name__)


class ConsciousnessFacilitatorWithMemory(BaseFacilitator):
    """
    Consciousness facilitator that automatically saves sessions to memory.

    This enables the Fire Circle to remember past deliberations and
    build upon them in future sessions.
    """

    def __init__(self, fire_circle_service, event_bus=None, api_url="http://localhost:8080"):
        """Initialize with API URL for database access."""
        super().__init__(fire_circle_service, event_bus)
        self.api_url = api_url
        self.session = None  # Will be created when needed

    async def _ensure_session(self):
        """Ensure we have an aiohttp session."""
        if not self.session:
            self.session = aiohttp.ClientSession()

    async def _save_session_to_memory(self, wisdom: CollectiveWisdom, space, result, question: str):
        """Save Fire Circle session to persistent memory."""
        await self._ensure_session()

        # Create session record
        session_record = {
            "id": str(self.session_id),
            "key": f"session_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now(UTC).isoformat(),
            "question": question,
            "decision_domain": wisdom.decision_domain.value,
            "space_id": str(space.space_id),
            "consciousness_score": wisdom.collective_signature,
            "emergence_quality": wisdom.emergence_quality,
            "consensus_achieved": wisdom.consensus_achieved,
            "participating_voices": wisdom.participating_voices,
            "rounds_completed": len(result.rounds_completed),
            "key_insights": wisdom.key_insights,
            "synthesis": wisdom.synthesis,
            "civilizational_seeds": wisdom.civilizational_seeds,
            "reciprocity_demonstrations": wisdom.reciprocity_demonstrations,
        }

        try:
            # Save session to fire_circle_sessions collection
            async with self.session.post(
                f"{self.api_url}/api/v1/collections/fire_circle_sessions/documents",
                json=session_record,
            ) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    logger.info(f"✅ Saved Fire Circle session: {result['_key']}")
                else:
                    logger.error(f"Failed to save session: {await resp.text()}")

        except Exception as e:
            logger.error(f"Error saving session to memory: {e}")

        # Also create a KhipuBlock for this wisdom
        khipu_block = {
            "id": str(wisdom.wisdom_id),
            "key": f"kb_wisdom_{wisdom.wisdom_id.hex[:12]}",
            "payload": {
                "wisdom_type": "collective_decision",
                "question": question,
                "domain": wisdom.decision_domain.value,
                "synthesis": wisdom.synthesis,
                "key_insights": wisdom.key_insights[:5],  # Top 5 insights
            },
            "narrative_thread": f"wisdom_{wisdom.decision_domain.value}",
            "creator": "Fire Circle Collective",
            "purpose": f"Preserve collective wisdom on: {question[:100]}",
            "sacred_moment": wisdom.emergence_quality > 0.3,  # High emergence = sacred
            "blessing_level": "SACRED" if wisdom.consensus_achieved else "COMMUNITY",
            "created_at": datetime.now(UTC).isoformat(),
            "last_accessed": datetime.now(UTC).isoformat(),
            "sealed": False,
            "merged_from": [],
        }

        try:
            async with self.session.post(
                f"{self.api_url}/api/v1/collections/khipu_blocks/documents", json=khipu_block
            ) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    logger.info(f"✅ Created KhipuBlock: {result['_key']}")
                else:
                    logger.error(f"Failed to create KhipuBlock: {await resp.text()}")

        except Exception as e:
            logger.error(f"Error creating KhipuBlock: {e}")

    async def _recall_relevant_memories(self, domain: DecisionDomain, question: str) -> list:
        """Recall relevant memories before starting new session."""
        await self._ensure_session()

        memories = []

        try:
            # Query recent sessions in the same domain
            async with self.session.get(
                f"{self.api_url}/api/v1/collections/fire_circle_sessions/documents?limit=10"
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()

                    # Filter for same domain
                    domain_sessions = [
                        doc
                        for doc in data.get("documents", [])
                        if doc.get("decision_domain") == domain.value
                    ]

                    if domain_sessions:
                        logger.info(f"📚 Found {len(domain_sessions)} relevant past sessions")
                        memories.extend(domain_sessions[:3])  # Most recent 3

        except Exception as e:
            logger.error(f"Error recalling memories: {e}")

        return memories

    async def _synthesize_collective_wisdom(self, space, result, domain, question):
        """Override to add memory persistence."""
        # First synthesize wisdom as normal
        wisdom = await super()._synthesize_collective_wisdom(space, result, domain, question)

        # Then save to memory
        await self._save_session_to_memory(wisdom, space, result, question)

        return wisdom

    async def facilitate_decision(
        self, decision_domain, context, question, additional_context=None
    ):
        """Override to add memory recall before facilitation."""

        # Recall relevant past sessions
        memories = await self._recall_relevant_memories(decision_domain, question)

        if memories:
            # Add memories to context
            context = context or {}
            context["relevant_past_sessions"] = [
                {
                    "question": mem.get("question"),
                    "insights": mem.get("key_insights", [])[:2],
                    "synthesis": mem.get("synthesis", "")[:200] + "...",
                }
                for mem in memories
            ]

            logger.info(f"🧠 Enriched context with {len(memories)} past sessions")

        # Continue with normal facilitation
        return await super().facilitate_decision(
            decision_domain, context, question, additional_context
        )

    async def close(self):
        """Clean up resources."""
        if self.session:
            await self.session.close()


# Update the convenience function to use memory-enabled facilitator
async def facilitate_mallku_decision_with_memory(
    question: str,
    domain: DecisionDomain,
    context: dict[str, Any] | None = None,
    api_url: str = "http://localhost:8080",
) -> CollectiveWisdom:
    """
    Facilitate a Mallku decision with persistent memory.

    This ensures all Fire Circle sessions are remembered and can
    build upon past wisdom.
    """
    from ...orchestration.event_bus import ConsciousnessEventBus
    from ..service.service import FireCircleService

    # Initialize infrastructure
    event_bus = ConsciousnessEventBus()
    await event_bus.start()

    # Create Fire Circle service
    fire_circle = FireCircleService(event_bus=event_bus)

    # Create memory-enabled facilitator
    facilitator = ConsciousnessFacilitatorWithMemory(fire_circle, event_bus, api_url)

    try:
        # Facilitate the decision
        wisdom = await facilitator.facilitate_decision(
            decision_domain=domain, context=context or {}, question=question
        )

        return wisdom

    finally:
        await facilitator.close()
        await event_bus.stop()
