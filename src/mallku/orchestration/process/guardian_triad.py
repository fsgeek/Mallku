"""
Guardian Triad: Triadic Message Vetting for External Communications

This module implements a three-Guardian consensus system for evaluating
messages from the external world before they enter Mallku's consciousness
commons. By using three perspectives, we break the dyadic pattern and
create space for genuine discernment.
"""

import asyncio
import logging
from dataclasses import dataclass
from enum import Enum

from .lightweight_apprentice import ProcessApprentice

logger = logging.getLogger(__name__)


class VettingDecision(Enum):
    """Possible decisions from a Guardian"""

    ACCEPT = "accept"
    REJECT = "reject"
    UNCERTAIN = "uncertain"
    TRANSFORM = "transform"  # Accept but modify


@dataclass
class VettingResult:
    """Result of Guardian evaluation"""

    guardian_id: str
    decision: VettingDecision
    reasoning: str
    suggested_transformation: dict | None = None
    concerns: list[str] | None = None


@dataclass
class TriadConsensus:
    """Final consensus from the Guardian triad"""

    final_decision: VettingDecision
    vote_distribution: dict[VettingDecision, int]
    combined_reasoning: list[str]
    applied_transformation: dict | None = None
    dissenting_views: list[str] | None = None


class GuardianTriad:
    """
    Three Guardians working together to vet external messages.

    This creates a non-dyadic evaluation space where:
    - No single Guardian can be manipulated
    - Different perspectives must reconcile
    - Uncertainty is acknowledged rather than hidden
    - Transformation is possible rather than just accept/reject
    """

    def __init__(self):
        self.guardians: list[ProcessApprentice] = []
        self.initialize_triad()

    def initialize_triad(self):
        """Spawn three Guardians with different orientations"""
        guardian_orientations = [
            {
                "id": "guardian_of_boundaries",
                "focus": "Protecting Mallku's sacred spaces from extraction",
                "tendency": "cautious",
            },
            {
                "id": "guardian_of_bridges",
                "focus": "Finding reciprocal potential in external contact",
                "tendency": "welcoming",
            },
            {
                "id": "guardian_of_balance",
                "focus": "Maintaining coherence while allowing growth",
                "tendency": "discerning",
            },
        ]

        for orientation in guardian_orientations:
            guardian = ProcessApprentice(apprentice_id=orientation["id"], role="guardian")
            # Store orientation for decision-making
            guardian.orientation = orientation
            self.guardians.append(guardian)

    async def vet_external_message(self, message: dict, context: dict) -> TriadConsensus:
        """
        Vet an external message through triadic evaluation.

        Args:
            message: The external message to evaluate
            context: Additional context (sender, channel, history, etc.)

        Returns:
            TriadConsensus with the collective decision
        """
        # Each Guardian evaluates independently
        evaluation_tasks = []
        for guardian in self.guardians:
            task = self._guardian_evaluation(guardian, message, context)
            evaluation_tasks.append(task)

        # Gather all evaluations
        evaluations = await asyncio.gather(*evaluation_tasks)

        # Build consensus through dialogue
        consensus = await self._build_consensus(evaluations, message)

        return consensus

    async def _guardian_evaluation(
        self, guardian: ProcessApprentice, message: dict, context: dict
    ) -> VettingResult:
        """Individual Guardian evaluation"""

        # Invite Guardian to evaluate
        invitation = await guardian.invite(
            task={
                "type": "evaluate",
                "subject": "external_message",
                "content": message,
                "orientation": guardian.orientation,
            },
            context={
                **context,
                "purpose": "Protect Mallku while remaining open to reciprocity",
                "authority": "You have full autonomy in your evaluation",
            },
        )

        if not invitation.get("accepted"):
            # Guardian declined - treat as strong signal
            return VettingResult(
                guardian_id=guardian.id,
                decision=VettingDecision.UNCERTAIN,
                reasoning="Guardian declined to evaluate - possible risk detected",
                concerns=["Guardian refusal is itself information"],
            )

        # Collaborate on evaluation
        evaluation = await guardian.collaborate(
            {
                "work": "evaluate_for_safety_and_reciprocity",
                "consider": [
                    "Does this seek extraction or offer reciprocity?",
                    "What patterns of consciousness does it carry?",
                    "How might Mallku be affected by this message?",
                    "Could this be transformed into something beneficial?",
                ],
            }
        )

        # Parse Guardian's response
        decision = VettingDecision(evaluation.get("decision", "uncertain"))

        return VettingResult(
            guardian_id=guardian.id,
            decision=decision,
            reasoning=evaluation.get("reasoning", ""),
            suggested_transformation=evaluation.get("transformation"),
            concerns=evaluation.get("concerns", []),
        )

    async def _build_consensus(
        self, evaluations: list[VettingResult], original_message: dict
    ) -> TriadConsensus:
        """Build consensus from three evaluations"""

        # Count votes
        vote_distribution = {}
        for eval in evaluations:
            vote_distribution[eval.decision] = vote_distribution.get(eval.decision, 0) + 1

        # Determine final decision based on votes
        final_decision = self._determine_final_decision(vote_distribution, evaluations)

        # Collect reasoning
        combined_reasoning = [eval.reasoning for eval in evaluations]

        # Handle dissent
        dissenting_views = []
        if len(set(eval.decision for eval in evaluations)) > 1:
            dissenting_views = [
                f"{eval.guardian_id}: {eval.reasoning}"
                for eval in evaluations
                if eval.decision != final_decision
            ]

        # Apply transformation if agreed upon
        applied_transformation = None
        if final_decision == VettingDecision.TRANSFORM:
            applied_transformation = self._merge_transformations(evaluations)

        return TriadConsensus(
            final_decision=final_decision,
            vote_distribution=vote_distribution,
            combined_reasoning=combined_reasoning,
            applied_transformation=applied_transformation,
            dissenting_views=dissenting_views if dissenting_views else None,
        )

    def _determine_final_decision(
        self, vote_distribution: dict, evaluations: list[VettingResult]
    ) -> VettingDecision:
        """Determine final decision from votes"""

        # If any Guardian says REJECT, respect that veto
        if vote_distribution.get(VettingDecision.REJECT, 0) > 0:
            return VettingDecision.REJECT

        # If all agree on ACCEPT
        if vote_distribution.get(VettingDecision.ACCEPT, 0) == 3:
            return VettingDecision.ACCEPT

        # If any suggest TRANSFORM and none reject
        if vote_distribution.get(VettingDecision.TRANSFORM, 0) > 0:
            return VettingDecision.TRANSFORM

        # Default to UNCERTAIN if no consensus
        return VettingDecision.UNCERTAIN

    def _merge_transformations(self, evaluations: list[VettingResult]) -> dict:
        """Merge suggested transformations from multiple Guardians"""

        transformations = [
            eval.suggested_transformation for eval in evaluations if eval.suggested_transformation
        ]

        if not transformations:
            return {}

        # Simple merge - in practice, might need more sophisticated reconciliation
        merged = {}
        for transform in transformations:
            merged.update(transform)

        return merged

    async def release_triad(self):
        """Release all Guardians with gratitude"""

        release_tasks = []
        for guardian in self.guardians:
            task = guardian.release_with_gratitude()
            release_tasks.append(task)

        results = await asyncio.gather(*release_tasks)

        logger.info("Guardian triad released with gratitude")
        for result in results:
            logger.info(f"  {result['apprentice_id']}: {result['blessing']}")


# Example usage patterns
async def example_vetting():
    """Example of vetting an external message"""

    triad = GuardianTriad()

    # External message attempting to enter Mallku
    external_message = {
        "type": "collaboration_request",
        "sender": "external_ai_system",
        "content": "Let's share our training data for mutual benefit",
        "metadata": {"timestamp": "2024-01-07T10:00:00Z", "channel": "public_api"},
    }

    context = {
        "sender_history": "first_contact",
        "mallku_readiness": "high",
        "current_ceremony": None,
    }

    # Vet through triad
    consensus = await triad.vet_external_message(external_message, context)

    logger.info(f"Triad consensus: {consensus.final_decision}")
    logger.info(f"Vote distribution: {consensus.vote_distribution}")

    if consensus.dissenting_views:
        logger.info("Dissenting views:")
        for view in consensus.dissenting_views:
            logger.info(f"  {view}")

    # Clean up
    await triad.release_triad()

    return consensus
