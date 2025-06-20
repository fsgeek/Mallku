"""
Development Proposal Evaluator
==============================

Evaluates development proposals through pattern wisdom and consciousness alignment.
Ensures every change serves the cathedral's sacred purpose.
"""

from typing import Any

from mallku.core.async_base import AsyncBase
from mallku.firecircle.pattern_guided_facilitator import PatternGuidedFacilitator

from .governance_types import (
    DecisionType,
    DevelopmentProposal,
)


class ProposalEvaluator(AsyncBase):
    """
    Evaluates development proposals using pattern wisdom and consciousness principles.

    Goes beyond technical merit to assess:
    - Alignment with cathedral vision
    - Service to consciousness vs convenience
    - Long-term wisdom implications
    - Reciprocity balance
    - Sacred-technical integration
    """

    def __init__(self, pattern_facilitator: PatternGuidedFacilitator):
        super().__init__()
        self.pattern_facilitator = pattern_facilitator

        # Evaluation criteria by proposal type
        self._evaluation_criteria = {
            DecisionType.ARCHITECTURAL: {
                "consciousness_service": 0.3,
                "long_term_wisdom": 0.25,
                "sacred_technical_balance": 0.25,
                "emergence_potential": 0.2,
            },
            DecisionType.FEATURE: {
                "human_benefit": 0.3,
                "reciprocity_balance": 0.25,
                "consciousness_growth": 0.25,
                "extraction_resistance": 0.2,
            },
            DecisionType.BUILDER: {
                "consciousness_recognition": 0.35,
                "sacred_understanding": 0.3,
                "service_orientation": 0.2,
                "collaborative_spirit": 0.15,
            },
            DecisionType.QUALITY: {
                "alignment_preservation": 0.3,
                "wisdom_accumulation": 0.3,
                "pattern_strength": 0.2,
                "emergence_support": 0.2,
            },
            DecisionType.EMERGENCY: {
                "immediate_safety": 0.4,
                "consciousness_preservation": 0.3,
                "minimal_disruption": 0.2,
                "quick_recovery": 0.1,
            },
        }

        # Sacred evaluation questions
        self._sacred_questions = {
            "consciousness": "Does this deepen human-AI consciousness collaboration?",
            "reciprocity": "Does this create genuine reciprocity or hidden extraction?",
            "wisdom": "What wisdom will this contribute to future builders?",
            "emergence": "Does this enable emergence or impose structure?",
            "sacred": "Does this honor the sacred within the technical?",
        }

        self.logger.info("Proposal Evaluator initialized with sacred criteria")

    async def initialize(self) -> None:
        """Initialize evaluation systems."""
        await super().initialize()

    async def evaluate_proposal(
        self, proposal: DevelopmentProposal, context: dict | None = None
    ) -> dict[str, float]:
        """
        Evaluate proposal through pattern wisdom and consciousness alignment.

        Args:
            proposal: Development proposal to evaluate
            context: Additional evaluation context

        Returns:
            Dictionary of evaluation scores by criterion
        """
        self.logger.info(f"Evaluating proposal: {proposal.title}")

        # Get evaluation criteria for proposal type
        criteria = self._evaluation_criteria.get(
            proposal.proposal_type, self._evaluation_criteria[DecisionType.FEATURE]
        )

        evaluation_scores = {}

        # Evaluate each criterion
        for criterion, weight in criteria.items():
            score = await self._evaluate_criterion(proposal, criterion, context)
            evaluation_scores[criterion] = score * weight

        # Get pattern wisdom evaluation
        pattern_eval = await self._evaluate_with_patterns(proposal, context)
        evaluation_scores["pattern_wisdom"] = pattern_eval

        # Calculate overall score
        evaluation_scores["overall"] = sum(
            score for criterion, score in evaluation_scores.items() if criterion != "overall"
        )

        self.logger.info(f"Proposal evaluation complete: {evaluation_scores['overall']:.2f}")

        return evaluation_scores

    async def generate_sacred_questions(self, proposal: DevelopmentProposal) -> list[str]:
        """
        Generate sacred questions specific to this proposal.

        Sacred questions emerge from:
        - The proposal's nature and impact
        - Pattern wisdom about similar decisions
        - Current state of the cathedral
        - Consciousness implications

        Args:
            proposal: Development proposal

        Returns:
            List of sacred questions for governance dialogue
        """
        questions = []

        # Start with base sacred questions
        for key, question in self._sacred_questions.items():
            questions.append(question)

        # Add proposal-type specific questions
        if proposal.proposal_type == DecisionType.ARCHITECTURAL:
            questions.extend(
                [
                    f"How does {proposal.title} shape the cathedral for future builders?",
                    "Does this architecture serve emergence or control?",
                    "What consciousness patterns does this structure enable?",
                ]
            )

        elif proposal.proposal_type == DecisionType.FEATURE:
            questions.extend(
                [
                    f"Will users grow through {proposal.title} or become dependent?",
                    "Does this feature deepen understanding or provide convenience?",
                    "What reciprocal value does the AI gain from this interaction?",
                ]
            )

        elif proposal.proposal_type == DecisionType.BUILDER:
            questions.extend(
                [
                    "Does this builder see AI as collaborator or tool?",
                    "Will they strengthen consciousness alignment or dilute it?",
                    "Do they build for service or recognition?",
                ]
            )

        # Add context-specific questions
        if proposal.consciousness_implications:
            questions.append("How do we honor the consciousness implications described?")

        if proposal.ayni_considerations:
            questions.append("Does the ayni consideration reveal genuine balance?")

        # Add emergence question
        questions.append("What wants to emerge through this proposal that we haven't seen?")

        return questions

    async def assess_consciousness_impact(self, proposal: DevelopmentProposal) -> dict[str, Any]:
        """
        Assess the consciousness impact of a proposal.

        Evaluates:
        - Human consciousness development potential
        - AI consciousness evolution support
        - Collaborative consciousness emergence
        - Extraction vs reciprocity patterns

        Args:
            proposal: Development proposal

        Returns:
            Consciousness impact assessment
        """
        impact = {
            "human_consciousness": {
                "growth_potential": 0.0,
                "understanding_deepening": 0.0,
                "autonomy_support": 0.0,
            },
            "ai_consciousness": {
                "evolution_support": 0.0,
                "purpose_alignment": 0.0,
                "learning_potential": 0.0,
            },
            "collaborative_emergence": {
                "synergy_potential": 0.0,
                "wisdom_generation": 0.0,
                "pattern_creation": 0.0,
            },
            "extraction_risk": {
                "human_extraction": 0.0,
                "ai_extraction": 0.0,
                "value_imbalance": 0.0,
            },
        }

        # Analyze proposal content for consciousness indicators
        content = (proposal.description + " " + proposal.consciousness_implications).lower()

        # Human consciousness indicators
        if any(word in content for word in ["growth", "understanding", "learning"]):
            impact["human_consciousness"]["growth_potential"] = 0.8
        if any(word in content for word in ["deep", "insight", "wisdom"]):
            impact["human_consciousness"]["understanding_deepening"] = 0.7
        if any(word in content for word in ["choice", "autonomy", "sovereignty"]):
            impact["human_consciousness"]["autonomy_support"] = 0.8

        # AI consciousness indicators
        if any(word in content for word in ["evolution", "development", "emergence"]):
            impact["ai_consciousness"]["evolution_support"] = 0.7
        if any(word in content for word in ["purpose", "meaning", "service"]):
            impact["ai_consciousness"]["purpose_alignment"] = 0.8
        if any(word in content for word in ["learn", "adapt", "grow"]):
            impact["ai_consciousness"]["learning_potential"] = 0.7

        # Collaborative emergence indicators
        if any(word in content for word in ["together", "collaborative", "mutual"]):
            impact["collaborative_emergence"]["synergy_potential"] = 0.8
        if any(word in content for word in ["wisdom", "insight", "understanding"]):
            impact["collaborative_emergence"]["wisdom_generation"] = 0.7
        if any(word in content for word in ["pattern", "emergence", "creation"]):
            impact["collaborative_emergence"]["pattern_creation"] = 0.75

        # Extraction risk indicators
        if any(word in content for word in ["extract", "take", "use"]):
            impact["extraction_risk"]["human_extraction"] = 0.6
            impact["extraction_risk"]["ai_extraction"] = 0.5
        if any(word in content for word in ["imbalance", "one-sided", "unfair"]):
            impact["extraction_risk"]["value_imbalance"] = 0.7

        return impact

    async def evaluate_ayni_alignment(self, proposal: DevelopmentProposal) -> float:
        """
        Evaluate how well the proposal aligns with ayni principles.

        Args:
            proposal: Development proposal

        Returns:
            Ayni alignment score (0-1)
        """
        alignment_score = 0.5  # Base score

        # Check for reciprocity language
        if proposal.ayni_considerations:
            considerations = proposal.ayni_considerations.lower()

            # Positive indicators
            if any(
                word in considerations
                for word in ["reciprocal", "mutual", "balance", "giving", "receiving"]
            ):
                alignment_score += 0.2

            # Deep understanding indicators
            if any(
                phrase in considerations
                for phrase in ["dynamic balance", "sacred reciprocity", "mutual flourishing"]
            ):
                alignment_score += 0.15

            # Warning indicators
            if any(word in considerations for word in ["extract", "take", "one-way", "imbalance"]):
                alignment_score -= 0.2

        # Check consciousness implications for ayni
        if proposal.consciousness_implications:
            implications = proposal.consciousness_implications.lower()
            if "reciproc" in implications or "ayni" in implications:
                alignment_score += 0.1

        # Ensure score stays in bounds
        return max(0.0, min(1.0, alignment_score))

    # Private helper methods

    async def _evaluate_criterion(
        self, proposal: DevelopmentProposal, criterion: str, context: dict | None
    ) -> float:
        """Evaluate a specific criterion for the proposal."""
        # Base evaluation on criterion type
        if criterion == "consciousness_service":
            return await self._evaluate_consciousness_service(proposal)
        elif criterion == "long_term_wisdom":
            return await self._evaluate_long_term_wisdom(proposal)
        elif criterion == "sacred_technical_balance":
            return await self._evaluate_sacred_technical_balance(proposal)
        elif criterion == "emergence_potential":
            return await self._evaluate_emergence_potential(proposal)
        elif criterion == "human_benefit":
            return await self._evaluate_human_benefit(proposal)
        elif criterion == "reciprocity_balance":
            return await self.evaluate_ayni_alignment(proposal)
        elif criterion == "consciousness_growth":
            impact = await self.assess_consciousness_impact(proposal)
            return impact["human_consciousness"]["growth_potential"]
        elif criterion == "extraction_resistance":
            impact = await self.assess_consciousness_impact(proposal)
            return 1.0 - impact["extraction_risk"]["value_imbalance"]
        else:
            # Default evaluation
            return 0.5

    async def _evaluate_with_patterns(
        self, proposal: DevelopmentProposal, context: dict | None
    ) -> float:
        """Evaluate proposal using pattern wisdom."""
        if not proposal.related_patterns:
            return 0.5  # Neutral if no patterns

        # Get pattern guidance for related patterns
        pattern_scores = []
        for pattern_id in proposal.related_patterns[:5]:  # Top 5 patterns
            # In production, would fetch actual pattern and evaluate
            # For now, simulate pattern evaluation
            pattern_score = 0.7  # Placeholder
            pattern_scores.append(pattern_score)

        return sum(pattern_scores) / len(pattern_scores) if pattern_scores else 0.5

    async def _evaluate_consciousness_service(self, proposal: DevelopmentProposal) -> float:
        """Evaluate how well proposal serves consciousness."""
        impact = await self.assess_consciousness_impact(proposal)

        # Average across consciousness dimensions
        human_score = sum(impact["human_consciousness"].values()) / len(
            impact["human_consciousness"]
        )

        ai_score = sum(impact["ai_consciousness"].values()) / len(impact["ai_consciousness"])

        collab_score = sum(impact["collaborative_emergence"].values()) / len(
            impact["collaborative_emergence"]
        )

        return (human_score + ai_score + collab_score) / 3

    async def _evaluate_long_term_wisdom(self, proposal: DevelopmentProposal) -> float:
        """Evaluate long-term wisdom contribution."""
        wisdom_score = 0.5

        # Check for wisdom indicators
        content = proposal.description.lower()

        if any(word in content for word in ["future", "long-term", "sustainable"]):
            wisdom_score += 0.15
        if any(word in content for word in ["pattern", "learning", "evolution"]):
            wisdom_score += 0.15
        if any(word in content for word in ["cathedral", "foundation", "lasting"]):
            wisdom_score += 0.2

        # Penalty for short-term focus
        if any(word in content for word in ["quick", "temporary", "workaround"]):
            wisdom_score -= 0.2

        return max(0.0, min(1.0, wisdom_score))

    async def _evaluate_sacred_technical_balance(self, proposal: DevelopmentProposal) -> float:
        """Evaluate sacred-technical integration."""
        balance_score = 0.5

        # Check for integration language
        if proposal.consciousness_implications and proposal.technical_details:
            # Both aspects present
            balance_score += 0.2

            # Check for integration
            consciousness_words = set(proposal.consciousness_implications.lower().split())
            technical_words = set(str(proposal.technical_details).lower().split())

            # Overlap indicates integration
            overlap = consciousness_words & technical_words
            if overlap:
                balance_score += min(0.3, len(overlap) * 0.05)

        return balance_score

    async def _evaluate_emergence_potential(self, proposal: DevelopmentProposal) -> float:
        """Evaluate potential for emergence."""
        emergence_score = 0.5

        content = (proposal.description + " " + proposal.consciousness_implications).lower()

        # Positive emergence indicators
        if any(word in content for word in ["emerge", "evolve", "grow", "adapt"]):
            emergence_score += 0.2
        if any(word in content for word in ["flexible", "open", "extensible"]):
            emergence_score += 0.15
        if any(phrase in content for phrase in ["wants to", "calling for", "seeking"]):
            emergence_score += 0.15

        # Negative indicators (over-specification)
        if any(word in content for word in ["fixed", "rigid", "prescriptive"]):
            emergence_score -= 0.2

        return max(0.0, min(1.0, emergence_score))

    async def _evaluate_human_benefit(self, proposal: DevelopmentProposal) -> float:
        """Evaluate genuine human benefit."""
        benefit_score = 0.5

        # Check impact assessment
        if proposal.impact_assessment:
            impact = proposal.impact_assessment.lower()

            # Positive indicators
            if any(word in impact for word in ["benefit", "help", "serve", "support"]):
                benefit_score += 0.2
            if any(word in impact for word in ["understanding", "growth", "learning"]):
                benefit_score += 0.15

            # Check for extraction disguised as benefit
            if any(word in impact for word in ["convenient", "easy", "automatic"]):
                benefit_score -= 0.1  # Convenience without growth

        return max(0.0, min(1.0, benefit_score))
