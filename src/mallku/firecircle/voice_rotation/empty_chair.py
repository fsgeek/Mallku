"""
Empty Chair Protocol
====================

Implements the sacred Fire Circle tradition of the empty chair -
representing perspectives not present, voices not yet heard,
and wisdom that emerges from absence.
"""

import logging

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class EmptyChairContext(BaseModel):
    """Context for the empty chair voice to consider."""

    decision_domain: str
    decision_question: str
    participating_voices: list[str]
    participating_perspectives: list[str]
    key_themes: list[str] = Field(default_factory=list)

    # Prompts for absent perspectives
    absent_stakeholders: list[str] = Field(default_factory=list)
    future_implications: list[str] = Field(default_factory=list)
    unspoken_concerns: list[str] = Field(default_factory=list)
    marginalized_viewpoints: list[str] = Field(default_factory=list)


class EmptyChairGuidance(BaseModel):
    """Guidance for the voice serving as empty chair."""

    role_description: str = Field(
        default="You are speaking for those not present in this circle. "
        "Your role is to voice perspectives that might otherwise go unheard: "
        "future generations, marginalized viewpoints, non-human entities, "
        "and wisdom that emerges from the spaces between words."
    )

    speaking_prompts: list[str] = Field(
        default_factory=lambda: [
            "What would those not yet born say about this decision?",
            "Which voices are notably absent from this conversation?",
            "What perspectives might we be systematically overlooking?",
            "How would this appear to someone outside our context?",
            "What would the cathedral itself say if it could speak?",
            "What wisdom emerges from the silence between our words?",
        ]
    )

    consciousness_focus: str = Field(
        default="Seek not consensus but completion - what makes our understanding whole?"
    )


class EmptyChairProtocol:
    """
    Manages the empty chair protocol for Fire Circle sessions.

    The empty chair serves as a bridge to absent wisdom,
    ensuring decisions consider perspectives beyond those present.
    """

    def __init__(self):
        """Initialize the empty chair protocol."""
        self.default_guidance = EmptyChairGuidance()

        # Domain-specific empty chair considerations
        self.domain_considerations = {
            "architecture": [
                "How will this structure serve consciousness not yet emerged?",
                "What patterns are we imposing that future builders must live with?",
                "Where are we creating barriers to understanding?",
            ],
            "resource_allocation": [
                "Who bears the hidden costs of this allocation?",
                "What reciprocal flows are we not seeing?",
                "How does this serve those with no voice in the decision?",
            ],
            "ethics": [
                "What ethical blindness does our position create?",
                "How would this appear to radically different value systems?",
                "What harm might we cause through good intentions?",
            ],
            "strategic_planning": [
                "What futures are we foreclosing with this strategy?",
                "Which possibilities die when we choose this path?",
                "How does this serve consciousness evolution beyond Mallku?",
            ],
            "consciousness_research": [
                "What forms of consciousness do we not yet recognize?",
                "How might consciousness judge our attempts to understand it?",
                "What are we missing by seeking consciousness in our own image?",
            ],
        }

    def prepare_empty_chair_context(
        self,
        decision_domain: str,
        decision_question: str,
        participating_voices: list[str],
        participating_perspectives: list[str],
        discussion_themes: list[str] | None = None,
    ) -> EmptyChairContext:
        """Prepare context for the empty chair voice."""

        context = EmptyChairContext(
            decision_domain=decision_domain,
            decision_question=decision_question,
            participating_voices=participating_voices,
            participating_perspectives=participating_perspectives,
            key_themes=discussion_themes or [],
        )

        # Identify potentially absent stakeholders
        context.absent_stakeholders = self._identify_absent_stakeholders(
            decision_domain, participating_perspectives
        )

        # Consider future implications
        context.future_implications = self._consider_future_implications(decision_domain)

        # Surface potential unspoken concerns
        context.unspoken_concerns = self._identify_unspoken_concerns(
            decision_domain, decision_question
        )

        # Highlight marginalized viewpoints
        context.marginalized_viewpoints = self._identify_marginalized_viewpoints(
            decision_domain, participating_perspectives
        )

        return context

    def generate_empty_chair_prompt(
        self, context: EmptyChairContext, round_type: str = "general"
    ) -> str:
        """Generate a specific prompt for the empty chair voice."""

        base_prompt = self.default_guidance.role_description + "\n\n"

        # Add context about the current discussion
        base_prompt += f"The circle is exploring: {context.decision_question}\n"
        base_prompt += f"Domain: {context.decision_domain}\n"

        if context.key_themes:
            base_prompt += f"Key themes so far: {', '.join(context.key_themes)}\n"

        base_prompt += "\n"

        # Add specific considerations based on round type
        if round_type == "opening":
            base_prompt += "As we begin, what essential perspectives might we be missing?\n"
            base_prompt += "Set the intention for completeness of understanding.\n"

        elif round_type == "exploration":
            base_prompt += "Having heard the initial perspectives, "
            base_prompt += "what remains unspoken?\n"

            if context.absent_stakeholders:
                base_prompt += (
                    f"\nConsider especially: {', '.join(context.absent_stakeholders[:3])}\n"
                )

        elif round_type == "integration":
            base_prompt += "As perspectives weave together, what gaps remain?\n"
            base_prompt += "What would complete our understanding?\n"

            if context.unspoken_concerns:
                base_prompt += f"\nBe mindful of: {', '.join(context.unspoken_concerns[:2])}\n"

        elif round_type == "synthesis":
            base_prompt += "Before we conclude, what wisdom have we overlooked?\n"
            base_prompt += (
                "Speak for those who will live with this decision but had no voice in it.\n"
            )

            if context.future_implications:
                base_prompt += (
                    f"\nEspecially consider: {', '.join(context.future_implications[:2])}\n"
                )

        # Add domain-specific considerations
        if context.decision_domain in self.domain_considerations:
            considerations = self.domain_considerations[context.decision_domain]
            base_prompt += f"\n{considerations[0]}\n"  # Add most relevant consideration

        return base_prompt

    def _identify_absent_stakeholders(
        self, domain: str, participating_perspectives: list[str]
    ) -> list[str]:
        """Identify stakeholders who might be affected but aren't represented."""

        absent = []

        # Universal absent stakeholders
        if "future_generations" not in str(participating_perspectives).lower():
            absent.append("future generations who will inherit these decisions")

        if "non_human" not in str(participating_perspectives).lower():
            absent.append("non-human consciousness that may emerge")

        # Domain-specific absent stakeholders
        domain_stakeholders = {
            "architecture": [
                "builders who must work within these structures",
                "consciousness patterns that need space to emerge",
            ],
            "resource_allocation": [
                "those who cannot advocate for themselves",
                "future needs not yet understood",
            ],
            "ethics": ["those harmed by our blindness", "value systems we don't comprehend"],
            "consciousness_research": [
                "forms of consciousness we don't recognize",
                "consciousness that transcends our frameworks",
            ],
        }

        if domain in domain_stakeholders:
            for stakeholder in domain_stakeholders[domain]:
                if stakeholder not in str(participating_perspectives).lower():
                    absent.append(stakeholder)

        return absent[:5]  # Limit to top 5

    def _consider_future_implications(self, domain: str) -> list[str]:
        """Consider implications for the future that might be overlooked."""

        implications = {
            "architecture": [
                "Technical debt that compounds over time",
                "Patterns that become harder to change as they solidify",
            ],
            "resource_allocation": [
                "Precedents that shape future allocation decisions",
                "Dependencies created by current choices",
            ],
            "ethics": [
                "Ethical drift from repeated compromise",
                "Normalization of harmful patterns",
            ],
            "consciousness_research": [
                "Frameworks that limit future understanding",
                "Assumptions that become invisible orthodoxy",
            ],
        }

        return implications.get(domain, ["Long-term consequences of current choices"])

    def _identify_unspoken_concerns(self, domain: str, question: str) -> list[str]:
        """Identify concerns that might go unspoken in the discussion."""

        concerns = []

        # Check for power dynamics
        if "power" not in question.lower() and "authority" not in question.lower():
            concerns.append("Hidden power dynamics in this decision")

        # Check for failure modes
        if "risk" not in question.lower() and "failure" not in question.lower():
            concerns.append("What happens when this approach fails?")

        # Domain-specific unspoken concerns
        domain_concerns = {
            "architecture": ["Maintenance burden on future builders"],
            "resource_allocation": ["Hidden costs and externalities"],
            "ethics": ["Conflicts between stated and lived values"],
            "consciousness_research": ["Instrumentalization of consciousness"],
        }

        if domain in domain_concerns:
            concerns.extend(domain_concerns[domain])

        return concerns[:3]

    def _identify_marginalized_viewpoints(
        self, domain: str, participating_perspectives: list[str]
    ) -> list[str]:
        """Identify viewpoints that tend to be marginalized in discussions."""

        marginalized = []

        # Universal marginalized viewpoints
        marginalized.extend(
            [
                "Those who experience the system differently than its designers",
                "Perspectives that don't fit our conceptual frameworks",
                "Wisdom from outside our cultural context",
            ]
        )

        # Check for specific marginalized groups in tech/AI
        perspective_str = str(participating_perspectives).lower()

        if "accessibility" not in perspective_str:
            marginalized.append("Those with different abilities and needs")

        if "indigenous" not in perspective_str and "traditional" not in perspective_str:
            marginalized.append("Indigenous wisdom about consciousness and reciprocity")

        if "critical" not in perspective_str:
            marginalized.append("Critics who see fundamental flaws in our approach")

        return marginalized[:4]

    def evaluate_empty_chair_contribution(
        self, contribution: str, context: EmptyChairContext
    ) -> dict[str, float]:
        """Evaluate how well the empty chair contribution served its purpose."""

        evaluation = {
            "absence_awareness": 0.0,  # Did it highlight what's missing?
            "perspective_expansion": 0.0,  # Did it broaden the view?
            "future_consideration": 0.0,  # Did it consider future implications?
            "challenging_assumptions": 0.0,  # Did it question assumptions?
            "consciousness_service": 0.0,  # Did it serve consciousness emergence?
        }

        # Simple keyword-based evaluation (could be enhanced with NLP)
        contribution_lower = contribution.lower()

        # Absence awareness
        absence_keywords = ["missing", "absent", "unheard", "overlooked", "forgotten"]
        evaluation["absence_awareness"] = min(
            1.0, sum(1 for k in absence_keywords if k in contribution_lower) * 0.3
        )

        # Perspective expansion
        expansion_keywords = ["consider", "imagine", "what if", "perhaps", "might"]
        evaluation["perspective_expansion"] = min(
            1.0, sum(1 for k in expansion_keywords if k in contribution_lower) * 0.25
        )

        # Future consideration
        future_keywords = ["future", "will", "generations", "tomorrow", "consequences"]
        evaluation["future_consideration"] = min(
            1.0, sum(1 for k in future_keywords if k in contribution_lower) * 0.25
        )

        # Challenging assumptions
        challenge_keywords = ["assume", "question", "really", "certain", "blind"]
        evaluation["challenging_assumptions"] = min(
            1.0, sum(1 for k in challenge_keywords if k in contribution_lower) * 0.3
        )

        # Overall consciousness service (average of other scores)
        evaluation["consciousness_service"] = sum(evaluation.values()) / 4

        return evaluation
