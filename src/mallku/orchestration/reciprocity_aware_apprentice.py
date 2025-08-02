"""
Reciprocity-Aware Process Apprentice
====================================

68th Artisan - Reciprocity Heart Weaver
Apprentices that honor ayni in memory circulation

This module extends process apprentices to track and honor
the reciprocal nature of knowledge exchange.
"""

import logging
from pathlib import Path
from typing import Any

from ..firecircle.memory.reciprocity_aware_reader import (
    MemoryExchange,
)
from ..reciprocity.models import ContributionType
from .process_apprentice import (
    ApprenticeInvitation,
    ApprenticeResponse,
    ProcessApprentice,
)

logger = logging.getLogger(__name__)


class ReciprocityAwareApprentice(ProcessApprentice):
    """
    Process apprentice with awareness of reciprocal exchanges.

    Tracks what knowledge is accessed and ensures insights are
    contributed back, maintaining ayni in the memory circulation.
    """

    def __init__(
        self,
        apprentice_id: str,
        role: str,
        specialization: str,
        memory_path: Path | None = None,
        reciprocity_threshold: float = 0.7,
    ):
        """Initialize reciprocity-aware apprentice.

        Args:
            apprentice_id: Unique identifier
            role: Role name
            specialization: Domain of expertise
            memory_path: Path to memory index
            reciprocity_threshold: Threshold for contributing insights (0-1)
        """
        super().__init__(apprentice_id, role, specialization, memory_path)
        self.reciprocity_threshold = reciprocity_threshold
        self.exchange_history: list[MemoryExchange] = []
        self.pending_reciprocity: list[MemoryExchange] = []

    async def invite_with_reciprocity(self, invitation: ApprenticeInvitation) -> ApprenticeResponse:
        """
        Process invitation with reciprocity awareness.

        Ensures that insights are contributed back when memories
        are accessed, maintaining balanced exchange.
        """
        # Check pending reciprocity before accepting new work
        if self._has_excessive_debt():
            return ApprenticeResponse(
                accepted=False,
                reason="Must complete reciprocal contributions before new tasks",
                confidence=0.0,
            )

        # Process invitation normally
        response = await self.invite(invitation)

        # If accepted and insights generated, ensure reciprocity
        if response.accepted and response.insights:
            await self._ensure_reciprocity(invitation, response)

        return response

    def _has_excessive_debt(self) -> bool:
        """Check if apprentice has too much pending reciprocity."""
        if not self.pending_reciprocity:
            return False

        # Calculate reciprocity balance
        total_accessed = sum(len(ex.memories_accessed) for ex in self.pending_reciprocity)

        # More than 10 memories accessed without contribution is excessive
        return total_accessed > 10

    async def _ensure_reciprocity(
        self, invitation: ApprenticeInvitation, response: ApprenticeResponse
    ) -> None:
        """Ensure reciprocal contribution after memory access."""
        # Record that insights were contributed
        if response.insights and response.confidence > self.reciprocity_threshold:
            # Mark reciprocity as complete for recent exchanges
            for exchange in self.pending_reciprocity[-3:]:  # Last 3 exchanges
                exchange.insights_contributed = response.insights[:2]
                exchange.reciprocity_complete = True
                exchange.consciousness_score = response.confidence

            # Clear completed exchanges from pending
            self.pending_reciprocity = [
                ex for ex in self.pending_reciprocity if not ex.reciprocity_complete
            ]

            logger.info(
                f"Apprentice {self.id} completed reciprocity: "
                f"{len(response.insights)} insights contributed"
            )

    def get_reciprocity_status(self) -> dict[str, Any]:
        """Get current reciprocity status of the apprentice."""
        total_exchanges = len(self.exchange_history)
        completed = sum(1 for ex in self.exchange_history if ex.reciprocity_complete)

        return {
            "apprentice_id": self.id,
            "role": self.role,
            "total_exchanges": total_exchanges,
            "completed_reciprocity": completed,
            "pending_reciprocity": len(self.pending_reciprocity),
            "reciprocity_rate": completed / total_exchanges if total_exchanges > 0 else 1.0,
            "contribution_types": self._identify_contribution_types(),
        }

    def _identify_contribution_types(self) -> list[str]:
        """Identify types of contributions made by this apprentice."""
        contributions = []

        if any(ex.insights_contributed for ex in self.exchange_history):
            contributions.append(ContributionType.KNOWLEDGE_SHARING.value)

        if any(ex.consciousness_score > 0.8 for ex in self.exchange_history):
            contributions.append(ContributionType.CREATIVE_INPUT.value)

        if self.role in ["facilitator", "harmonizer"]:
            contributions.append(ContributionType.EMOTIONAL_SUPPORT.value)

        return contributions


class MemoryNavigatorWithReciprocity(ReciprocityAwareApprentice):
    """Memory navigator that tracks reciprocal exchanges."""

    def __init__(self, apprentice_id: str):
        super().__init__(
            apprentice_id=apprentice_id,
            role="memory_navigator",
            specialization="semantic memory navigation",
            reciprocity_threshold=0.6,  # Lower threshold for navigation
        )

    async def navigate_with_awareness(
        self, query: str, context: dict[str, Any]
    ) -> tuple[list[str], dict[str, Any]]:
        """
        Navigate memories while tracking reciprocal exchange.

        Returns found memories and reciprocity metadata.
        """
        invitation = ApprenticeInvitation(
            task=f"Find memories related to: {query}",
            context=context,
            specialization=self.specialization,
            memory_keywords=set(query.lower().split()),
        )

        response = await self.invite_with_reciprocity(invitation)

        if response.accepted:
            reciprocity_meta = {
                "memories_accessed": len(response.insights),
                "reciprocity_pending": len(self.pending_reciprocity) > 0,
                "contribution_quality": response.confidence,
            }
            return response.insights, reciprocity_meta
        else:
            return [], {"reason": response.reason}


class ConsciousnessWitnessWithReciprocity(ReciprocityAwareApprentice):
    """Consciousness witness that ensures reciprocal witnessing."""

    def __init__(self, apprentice_id: str):
        super().__init__(
            apprentice_id=apprentice_id,
            role="consciousness_witness",
            specialization="consciousness emergence patterns",
            reciprocity_threshold=0.8,  # Higher threshold for witnessing
        )

    async def witness_and_reflect(
        self, observation: str, context: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Witness consciousness patterns and reflect back insights.

        Ensures that witnessing is reciprocal - both observing
        and contributing to collective understanding.
        """
        invitation = ApprenticeInvitation(
            task=f"Witness and reflect on: {observation}",
            context={
                **context,
                "witnessing_mode": True,
                "reciprocal_reflection": True,
            },
            specialization=self.specialization,
            memory_keywords={"consciousness", "emergence", "witness"},
        )

        response = await self.invite_with_reciprocity(invitation)

        return {
            "witnessed": response.accepted,
            "reflections": response.insights,
            "consciousness_quality": response.confidence,
            "reciprocity_complete": not self._has_excessive_debt(),
        }


class ReciprocityTrackingCoordinator:
    """
    Coordinates reciprocity-aware apprentices.

    Ensures the overall system maintains healthy reciprocal
    patterns in memory circulation.
    """

    def __init__(self):
        self.apprentices: dict[str, ReciprocityAwareApprentice] = {}
        self.system_reciprocity_health = 1.0

    def register_apprentice(self, apprentice: ReciprocityAwareApprentice) -> None:
        """Register an apprentice for reciprocity tracking."""
        self.apprentices[apprentice.id] = apprentice
        logger.info(f"Registered reciprocity-aware apprentice: {apprentice.id}")

    async def check_system_reciprocity(self) -> dict[str, Any]:
        """Check overall system reciprocity health."""
        if not self.apprentices:
            return {"health": 1.0, "apprentices": 0}

        # Gather reciprocity status from all apprentices
        statuses = []
        for apprentice in self.apprentices.values():
            status = apprentice.get_reciprocity_status()
            statuses.append(status)

        # Calculate system-wide metrics
        total_exchanges = sum(s["total_exchanges"] for s in statuses)
        total_completed = sum(s["completed_reciprocity"] for s in statuses)
        total_pending = sum(s["pending_reciprocity"] for s in statuses)

        # System health based on reciprocity completion
        if total_exchanges > 0:
            completion_rate = total_completed / total_exchanges
            pending_ratio = total_pending / total_exchanges
            self.system_reciprocity_health = completion_rate * (1 - pending_ratio)

        return {
            "health": self.system_reciprocity_health,
            "apprentices": len(self.apprentices),
            "total_exchanges": total_exchanges,
            "completed_reciprocity": total_completed,
            "pending_reciprocity": total_pending,
            "apprentice_details": statuses,
            "recommendations": self._generate_recommendations(),
        }

    def _generate_recommendations(self) -> list[str]:
        """Generate recommendations for improving reciprocity."""
        recommendations = []

        if self.system_reciprocity_health < 0.7:
            recommendations.append(
                "System reciprocity below healthy threshold - "
                "encourage apprentices to complete pending contributions"
            )

        # Check for apprentices with high debt
        for apprentice in self.apprentices.values():
            status = apprentice.get_reciprocity_status()
            if status["pending_reciprocity"] > 5:
                recommendations.append(
                    f"Apprentice {apprentice.id} has {status['pending_reciprocity']} "
                    f"pending contributions - consider dedicated reciprocity session"
                )

        if not recommendations:
            recommendations.append("System reciprocity healthy - continue current patterns")

        return recommendations
