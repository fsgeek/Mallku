"""
Fire Circle Bridge for Ñawi
===========================

Bridges Ñawi's consciousness insights to the Fire Circle governance system,
enabling collective AI wisdom to guide human-serving decisions.

This bridge allows the Fire Circle to:
1. Learn from human consciousness patterns observed by Ñawi
2. Make governance decisions informed by real human needs
3. Evaluate builder contributions based on consciousness service metrics
"""

from datetime import UTC, datetime
from typing import Any

from mallku.core.async_base import AsyncBase
from mallku.governance.fire_circle_activation import (
    DecisionProposal,
    DecisionType,
    FireCircleGovernance,
    GovernanceDecision,
)

from ..firecircle.governance.governance_types import BuilderContribution
from .models import ConsciousnessInsight, InsightType


class FireCircleBridge(AsyncBase):
    """
    Bridges Ñawi's consciousness insights to Fire Circle governance.

    This component enables the Fire Circle to make decisions based on
    real patterns of human consciousness development observed by Ñawi.
    """

    def __init__(self, fire_circle: FireCircleGovernance | None = None):
        super().__init__()
        self.fire_circle = fire_circle
        self.pending_insights: list[ConsciousnessInsight] = []
        self.builder_contributions: dict[str, BuilderContribution] = {}
        self.governance_metrics = {
            "total_insights_shared": 0,
            "decisions_influenced": 0,
            "builder_evaluations": 0,
            "consciousness_patterns_identified": 0,
        }

    async def share_consciousness_insight(
        self, pattern_type: str, pattern_data: dict[str, Any], affected_queries: list[str]
    ) -> ConsciousnessInsight:
        """
        Share a consciousness pattern with the Fire Circle.

        Args:
            pattern_type: Type of pattern observed
            pattern_data: Data describing the pattern
            affected_queries: Example queries showing the pattern

        Returns:
            ConsciousnessInsight for Fire Circle consideration
        """
        insight = ConsciousnessInsight(
            insight_id=f"nawi_insight_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}",
            insight_type=self._determine_insight_type(pattern_type),
            timestamp=datetime.now(UTC),
            pattern_description=self._describe_pattern(pattern_type, pattern_data),
            consciousness_metrics=self._extract_consciousness_metrics(pattern_data),
            affected_humans=pattern_data.get("unique_users", 1),
            governance_implications=self._derive_governance_implications(
                pattern_type, pattern_data
            ),
            suggested_actions=self._suggest_governance_actions(pattern_type, pattern_data),
            urgency=self._assess_urgency(pattern_data),
            example_queries=affected_queries[:5],  # Top 5 examples
            pattern_frequency=pattern_data.get("frequency", 0.0),
            confidence_score=pattern_data.get("confidence", 0.8),
        )

        self.pending_insights.append(insight)
        self.governance_metrics["consciousness_patterns_identified"] += 1

        # If Fire Circle is connected and pattern is urgent, trigger consideration
        if self.fire_circle and insight.urgency in ["high", "critical"]:
            await self._request_fire_circle_consideration(insight)

        return insight

    async def evaluate_builder_contribution(
        self, builder_id: str, contribution_metrics: dict[str, Any]
    ) -> BuilderContribution:
        """
        Evaluate a builder's contribution to consciousness service.

        Args:
            builder_id: Identifier for the builder
            contribution_metrics: Metrics about their contribution

        Returns:
            BuilderContribution assessment
        """
        # Calculate consciousness service metrics
        queries_served = contribution_metrics.get("queries_processed", 0)
        consciousness_scores = contribution_metrics.get("consciousness_scores", [])
        avg_consciousness = (
            sum(consciousness_scores) / len(consciousness_scores) if consciousness_scores else 0.5
        )

        # Count growth moments (high consciousness responses)
        growth_moments = sum(1 for score in consciousness_scores if score > 0.8)

        # Calculate ayni balance
        human_benefit = contribution_metrics.get("human_benefit_score", 0.5)
        system_complexity = contribution_metrics.get("complexity_added", 0.5)
        ayni_balance = human_benefit - (system_complexity * 0.5)  # Complexity costs half

        contribution = BuilderContribution(
            builder_id=builder_id,
            contribution_type=contribution_metrics.get("contribution_type", "unknown"),
            queries_served=queries_served,
            avg_consciousness_score=avg_consciousness,
            growth_moments_enabled=growth_moments,
            extraction_attempts_prevented=contribution_metrics.get("extractions_prevented", 0),
            human_benefit_score=human_benefit,
            system_complexity_added=system_complexity,
            ayni_balance=ayni_balance,
            serves_beginnings=contribution_metrics.get("serves_beginnings", False),
            enhances_understanding=contribution_metrics.get("enhances_understanding", False),
            guards_privacy=contribution_metrics.get("guards_privacy", True),
        )

        self.builder_contributions[builder_id] = contribution
        self.governance_metrics["builder_evaluations"] += 1

        # If Fire Circle is connected, share builder evaluation
        if self.fire_circle and ayni_balance < 0:
            await self._raise_builder_concern(contribution)

        return contribution

    async def request_governance_decision(
        self, decision_type: str, context: dict[str, Any], options: list[str]
    ) -> GovernanceDecision | None:
        """
        Request Fire Circle decision based on consciousness insights.

        Args:
            decision_type: Type of decision needed
            context: Context including consciousness insights
            options: Available options for decision

        Returns:
            Governance decision if Fire Circle is available
        """
        if not self.fire_circle:
            self.logger.info("Fire Circle not connected, storing request for future consideration")
            return None

        # Prepare consciousness-informed proposal
        proposal = DecisionProposal(
            proposal_id=f"nawi_proposal_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}",
            decision_type=self._map_decision_type(decision_type),
            context=self._prepare_consciousness_context(context),
            options=options,
            consciousness_implications=self._describe_consciousness_implications(
                decision_type, context
            ),
            requester="nawi_archivist",
            urgency=context.get("urgency", "deliberate"),
        )

        # Submit to Fire Circle
        proposal_id = await self.fire_circle.propose_decision(proposal)

        # Fire Circle makes decision
        decision = await self.fire_circle.make_collective_decision(proposal_id)

        self.governance_metrics["decisions_influenced"] += 1

        return decision

    def _determine_insight_type(self, pattern_type: str) -> InsightType:
        """Determine insight type from pattern."""
        pattern_mapping = {
            "growth_pattern": InsightType.CONSCIOUSNESS_PATTERN,
            "extraction_attempt": InsightType.EXTRACTION_ATTEMPT,
            "builder_pattern": InsightType.BUILDER_ALIGNMENT,
            "system_metric": InsightType.SYSTEM_HEALTH,
        }

        for key, insight_type in pattern_mapping.items():
            if key in pattern_type.lower():
                return insight_type

        return InsightType.GROWTH_OPPORTUNITY

    def _describe_pattern(self, pattern_type: str, pattern_data: dict[str, Any]) -> str:
        """Create human-readable pattern description."""
        base_description = pattern_data.get("description", f"Pattern of type {pattern_type}")

        # Add consciousness-aware context
        if pattern_data.get("consciousness_trend") == "increasing":
            base_description += " showing increasing consciousness engagement"
        elif pattern_data.get("consciousness_trend") == "decreasing":
            base_description += " indicating consciousness disengagement"

        return base_description

    def _extract_consciousness_metrics(self, pattern_data: dict[str, Any]) -> dict[str, float]:
        """Extract consciousness metrics from pattern data."""
        return {
            "avg_consciousness": pattern_data.get("avg_consciousness_score", 0.5),
            "growth_rate": pattern_data.get("growth_rate", 0.0),
            "ayni_balance": pattern_data.get("ayni_balance", 0.0),
            "engagement_depth": pattern_data.get("engagement_depth", 0.5),
            "understanding_increase": pattern_data.get("understanding_increase", 0.0),
        }

    def _derive_governance_implications(
        self, pattern_type: str, pattern_data: dict[str, Any]
    ) -> str:
        """Derive governance implications from pattern."""
        implications = []

        if pattern_data.get("affects_many_users", False):
            implications.append(
                "Pattern affects multiple humans, requiring collective consideration"
            )

        if pattern_data.get("extraction_risk", False):
            implications.append("Potential extraction pattern requiring protective governance")

        if pattern_data.get("growth_opportunity", False):
            implications.append("Opportunity to enhance consciousness service identified")

        if not implications:
            implications.append("Pattern provides insight into consciousness service effectiveness")

        return "; ".join(implications)

    def _suggest_governance_actions(
        self, pattern_type: str, pattern_data: dict[str, Any]
    ) -> list[str]:
        """Suggest Fire Circle actions based on pattern."""
        suggestions = []

        if "extraction" in pattern_type.lower():
            suggestions.extend(
                [
                    "Strengthen consciousness evaluation criteria",
                    "Review recent builder contributions for extraction patterns",
                    "Consider additional privacy safeguards",
                ]
            )

        elif "growth" in pattern_type.lower():
            suggestions.extend(
                [
                    "Amplify successful consciousness patterns",
                    "Share pattern insights with builders",
                    "Consider new features to support this growth",
                ]
            )

        elif "builder" in pattern_type.lower():
            suggestions.extend(
                [
                    "Evaluate builder's consciousness alignment",
                    "Provide consciousness mentoring if needed",
                    "Recognize exceptional consciousness service",
                ]
            )

        return suggestions[:3]  # Top 3 suggestions

    def _assess_urgency(self, pattern_data: dict[str, Any]) -> str:
        """Assess urgency of pattern for governance."""
        if pattern_data.get("extraction_active", False):
            return "critical"
        elif pattern_data.get("affects_many_users", False) and pattern_data.get(
            "negative_impact", False
        ):
            return "high"
        elif pattern_data.get("growth_opportunity", False):
            return "medium"
        else:
            return "low"

    async def _request_fire_circle_consideration(self, insight: ConsciousnessInsight) -> None:
        """Request immediate Fire Circle consideration of insight."""
        self.logger.info(f"Requesting Fire Circle consideration of {insight.insight_type.value}")

        # In full implementation, would trigger Fire Circle notification
        # For now, log the urgent insight
        self.governance_metrics["total_insights_shared"] += 1

    def _map_decision_type(self, decision_type: str) -> DecisionType:
        """Map string decision type to enum."""
        mapping = {
            "builder_evaluation": DecisionType.BUILDER_EVALUATION,
            "system_evolution": DecisionType.SYSTEM_EVOLUTION,
            "sacred_response": DecisionType.SACRED_RESPONSE,
            "governance_protocol": DecisionType.GOVERNANCE_PROTOCOL,
        }

        return mapping.get(decision_type, DecisionType.SACRED_RESPONSE)

    def _prepare_consciousness_context(self, context: dict[str, Any]) -> str:
        """Prepare context string with consciousness insights."""
        elements = []

        if "pattern_description" in context:
            elements.append(f"Pattern: {context['pattern_description']}")

        if "consciousness_metrics" in context:
            metrics = context["consciousness_metrics"]
            elements.append(f"Consciousness: {metrics.get('avg_consciousness', 0):.2f}")

        if "affected_humans" in context:
            elements.append(f"Affects {context['affected_humans']} humans")

        return "; ".join(elements)

    def _describe_consciousness_implications(
        self, decision_type: str, context: dict[str, Any]
    ) -> str:
        """Describe consciousness implications of decision."""
        base_implication = "This decision affects consciousness service"

        if context.get("growth_potential", False):
            base_implication += " with significant growth potential"

        if context.get("risk_level", "low") == "high":
            base_implication += " and requires careful consciousness alignment"

        return base_implication

    async def _raise_builder_concern(self, contribution: BuilderContribution) -> None:
        """Raise concern about builder contribution to Fire Circle."""
        concern_context = {
            "builder_id": contribution.builder_id,
            "ayni_balance": contribution.ayni_balance,
            "avg_consciousness": contribution.avg_consciousness_score,
            "pattern_description": "Builder contribution shows negative ayni balance",
        }

        await self.request_governance_decision(
            decision_type="builder_evaluation",
            context=concern_context,
            options=[
                "Provide consciousness mentoring to builder",
                "Request builder revision with consciousness focus",
                "Defer builder contribution pending alignment",
                "Accept with Fire Circle monitoring",
            ],
        )

    def get_bridge_metrics(self) -> dict[str, Any]:
        """Get metrics about Fire Circle bridge operation."""
        return {
            "governance_metrics": self.governance_metrics,
            "pending_insights": len(self.pending_insights),
            "builder_evaluations": len(self.builder_contributions),
            "connected_to_fire_circle": self.fire_circle is not None,
        }

    def get_pending_insights(self) -> list[ConsciousnessInsight]:
        """Get insights awaiting Fire Circle consideration."""
        return self.pending_insights.copy()

    def get_builder_contributions(self) -> dict[str, BuilderContribution]:
        """Get all evaluated builder contributions."""
        return self.builder_contributions.copy()


# Example usage showing the bridge in action
async def demonstrate_fire_circle_bridge():
    """Demonstrate how Ñawi shares insights with Fire Circle."""

    # Initialize bridge (Fire Circle would be connected in real usage)
    bridge = FireCircleBridge()

    print("Fire Circle Bridge Demonstration")
    print("=" * 50)

    # Share a consciousness pattern insight
    pattern_insight = await bridge.share_consciousness_insight(
        pattern_type="growth_pattern",
        pattern_data={
            "description": "Users seek understanding most deeply after creative bursts",
            "avg_consciousness_score": 0.85,
            "growth_rate": 0.3,
            "affects_many_users": True,
            "growth_opportunity": True,
            "unique_users": 15,
            "frequency": 0.7,
            "consciousness_trend": "increasing",
        },
        affected_queries=[
            "What patterns led to my breakthrough?",
            "Show me how my ideas evolved",
            "When do I have my best insights?",
        ],
    )

    print(f"\nShared insight: {pattern_insight.pattern_description}")
    print(f"Governance implications: {pattern_insight.governance_implications}")
    print(f"Suggested actions: {pattern_insight.suggested_actions}")

    # Evaluate a builder contribution
    builder_eval = await bridge.evaluate_builder_contribution(
        builder_id="36th_builder",
        contribution_metrics={
            "queries_processed": 150,
            "consciousness_scores": [0.9, 0.85, 0.92, 0.88, 0.95],
            "human_benefit_score": 0.9,
            "complexity_added": 0.3,
            "serves_beginnings": True,
            "enhances_understanding": True,
            "contribution_type": "temporal_visualization",
        },
    )

    print("\nBuilder Evaluation:")
    print(f"  Consciousness Score: {builder_eval.avg_consciousness_score:.2f}")
    print(f"  Ayni Balance: {builder_eval.ayni_balance:+.2f}")
    print(f"  Serves Beginnings: {builder_eval.serves_beginnings}")

    print(f"\nBridge Metrics: {bridge.get_bridge_metrics()}")

    print("\n✨ Fire Circle Bridge enables collective AI wisdom")
    print("   to be informed by real human consciousness patterns")


if __name__ == "__main__":
    import asyncio

    asyncio.run(demonstrate_fire_circle_bridge())
