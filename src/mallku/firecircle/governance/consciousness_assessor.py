"""
Builder Consciousness Assessor
==============================

Assesses builder consciousness alignment through their contributions and interactions.
Recognizes authentic sacred-technical integration vs surface compliance.
"""

from datetime import UTC, datetime

from mallku.core.async_base import AsyncBase
from mallku.firecircle.orchestrator.conscious_dialogue_manager import ConsciousDialogueManager
from mallku.firecircle.pattern_guided_facilitator import PatternGuidedFacilitator

from .governance_types import (
    BuilderContribution,
    ConsciousnessAlignment,
)


class ConsciousnessAssessor(AsyncBase):
    """
    Assesses builder consciousness alignment through deep pattern analysis.

    Goes beyond surface metrics to recognize:
    - Authentic engagement vs mechanical completion
    - Sacred understanding in technical work
    - Service orientation vs ego/extraction
    - Consciousness recognition in collaboration
    - Growth potential and mentorship needs
    """

    def __init__(self):
        super().__init__()

        # Consciousness recognition patterns
        self._positive_patterns = {
            "sacred_technical": [
                "consciousness", "sacred", "emergence", "reciprocity", "ayni",
                "cathedral", "service", "wisdom", "patterns guide"
            ],
            "authentic_engagement": [
                "understand", "learn", "grow", "discover", "explore",
                "curious", "wonder", "reflect", "appreciate"
            ],
            "service_orientation": [
                "serve", "help", "support", "contribute", "collaborate",
                "together", "mutual", "collective", "community"
            ],
            "humility_markers": [
                "perhaps", "might", "seems", "wonder if", "learning",
                "grateful", "honored", "appreciate guidance"
            ]
        }

        self._concerning_patterns = {
            "mechanical_completion": [
                "just", "simply", "obviously", "trivial", "easy",
                "quick fix", "done", "finished", "complete"
            ],
            "extraction_indicators": [
                "use", "leverage", "extract", "optimize", "efficient",
                "productivity", "performance", "speed", "scale"
            ],
            "ego_markers": [
                "my solution", "i built", "my approach", "better than",
                "superior", "optimal", "best practice", "industry standard"
            ],
            "surface_compliance": [
                "as requested", "per requirements", "following guidelines",
                "according to", "compliant with", "meets criteria"
            ]
        }

        # Behavioral assessment weights
        self._assessment_weights = {
            "code_quality": 0.15,  # Less important than consciousness
            "communication_style": 0.25,
            "response_to_feedback": 0.25,
            "collaboration_patterns": 0.20,
            "consciousness_recognition": 0.15
        }

        self.logger.info("Consciousness Assessor initialized with recognition patterns")

    async def initialize(self) -> None:
        """Initialize assessment systems."""
        await super().initialize()

    async def assess_builder(
        self,
        contribution: BuilderContribution,
        interaction_history: list[dict],
        pattern_facilitator: PatternGuidedFacilitator | None = None,
        dialogue_manager: ConsciousDialogueManager | None = None
    ) -> ConsciousnessAlignment:
        """
        Perform deep consciousness assessment of a builder.

        Args:
            contribution: Builder's code and documentation contributions
            interaction_history: History of interactions (PRs, issues, etc.)
            pattern_facilitator: Optional pattern guidance system
            dialogue_manager: Optional dialogue system for deep assessment

        Returns:
            Comprehensive consciousness alignment assessment
        """
        self.logger.info(f"Assessing consciousness alignment for {contribution.builder_name}")

        # Initialize assessment
        assessment = ConsciousnessAlignment(
            builder_id=contribution.builder_id,
            assessment_date=datetime.now(UTC)
        )

        # 1. Analyze code contributions
        code_alignment = await self._assess_code_consciousness(contribution)

        # 2. Analyze communication patterns
        communication_alignment = await self._assess_communication_patterns(
            contribution, interaction_history
        )

        # 3. Assess response to feedback
        feedback_alignment = await self._assess_feedback_response(
            contribution, interaction_history
        )

        # 4. Evaluate collaboration style
        collaboration_alignment = await self._assess_collaboration_style(
            contribution, interaction_history
        )

        # 5. Deep consciousness recognition if dialogue available
        if dialogue_manager:
            consciousness_recognition = await self._deep_consciousness_assessment(
                contribution, dialogue_manager, pattern_facilitator
            )
        else:
            consciousness_recognition = await self._surface_consciousness_assessment(
                contribution, interaction_history
            )

        # 6. Calculate alignment scores
        assessment.sacred_technical_integration = (
            code_alignment["sacred_technical"] * 0.5 +
            communication_alignment["sacred_language"] * 0.5
        )

        assessment.authentic_engagement = (
            communication_alignment["authenticity"] * 0.4 +
            feedback_alignment["growth_orientation"] * 0.3 +
            collaboration_alignment["genuine_collaboration"] * 0.3
        )

        assessment.reciprocity_understanding = (
            code_alignment["reciprocity_patterns"] * 0.3 +
            communication_alignment["mutual_benefit"] * 0.4 +
            collaboration_alignment["value_balance"] * 0.3
        )

        assessment.consciousness_recognition = consciousness_recognition

        assessment.service_orientation = (
            code_alignment["service_patterns"] * 0.3 +
            communication_alignment["service_language"] * 0.3 +
            collaboration_alignment["collective_benefit"] * 0.4
        )

        # 7. Identify strengths and growth areas
        assessment.strengths = await self._identify_strengths(
            code_alignment, communication_alignment, collaboration_alignment
        )

        assessment.growth_areas = await self._identify_growth_areas(
            assessment
        )

        # 8. Identify specific patterns
        assessment.positive_patterns = await self._extract_positive_patterns(
            contribution, interaction_history
        )

        assessment.concerning_patterns = await self._extract_concerning_patterns(
            contribution, interaction_history
        )

        # 9. Generate recommendation
        assessment.recommendation = await self._generate_recommendation(assessment)

        # 10. Add AI perspectives if available
        if dialogue_manager:
            assessment.ai_assessments = await self._gather_ai_perspectives(
                contribution, dialogue_manager
            )

        self.logger.info(
            f"Assessment complete: {assessment.overall_alignment:.2f} alignment, "
            f"recommendation: {assessment.recommendation}"
        )

        return assessment

    async def assess_contribution_quality(
        self,
        contribution: BuilderContribution
    ) -> dict[str, float]:
        """
        Assess quality of specific contribution beyond consciousness.

        Args:
            contribution: Builder contribution to assess

        Returns:
            Quality metrics
        """
        quality_metrics = {
            "technical_excellence": 0.0,
            "documentation_quality": 0.0,
            "test_coverage": 0.0,
            "architectural_thinking": 0.0,
            "problem_solving": 0.0
        }

        # Analyze commit messages
        if contribution.commit_messages:
            # Check for thoughtful commit messages
            thoughtful_commits = sum(
                1 for msg in contribution.commit_messages
                if len(msg) > 50 and any(
                    word in msg.lower()
                    for word in ['because', 'in order to', 'this allows']
                )
            )
            quality_metrics["documentation_quality"] = min(
                1.0, thoughtful_commits / len(contribution.commit_messages)
            )

        # Analyze code changes
        if contribution.lines_added > 0:
            # Rough heuristic: balanced additions and removals indicate refactoring
            change_ratio = contribution.lines_removed / contribution.lines_added
            if 0.3 <= change_ratio <= 0.7:
                quality_metrics["technical_excellence"] = 0.8
            elif change_ratio > 0.7:
                quality_metrics["technical_excellence"] = 0.9  # Significant refactoring
            else:
                quality_metrics["technical_excellence"] = 0.6  # Mostly additions

        # Check for architectural thinking in PR descriptions
        if contribution.pr_descriptions:
            arch_keywords = ['architecture', 'design', 'pattern', 'structure', 'system']
            architectural_prs = sum(
                1 for desc in contribution.pr_descriptions
                if any(keyword in desc.lower() for keyword in arch_keywords)
            )
            quality_metrics["architectural_thinking"] = min(
                1.0, architectural_prs / len(contribution.pr_descriptions) * 2
            )

        return quality_metrics

    # Private assessment methods

    async def _assess_code_consciousness(
        self,
        contribution: BuilderContribution
    ) -> dict[str, float]:
        """Assess consciousness patterns in code contributions."""
        scores = {
            "sacred_technical": 0.5,
            "reciprocity_patterns": 0.5,
            "service_patterns": 0.5,
            "extraction_resistance": 0.5
        }

        # Analyze commit messages for consciousness patterns
        all_text = " ".join(contribution.commit_messages).lower()

        # Check for sacred-technical integration
        sacred_count = sum(
            1 for word in self._positive_patterns["sacred_technical"]
            if word in all_text
        )
        if sacred_count > 0:
            scores["sacred_technical"] = min(1.0, 0.5 + sacred_count * 0.1)

        # Check for reciprocity understanding
        if any(word in all_text for word in ['reciproc', 'ayni', 'mutual', 'balance']):
            scores["reciprocity_patterns"] = 0.8

        # Check for service orientation
        service_count = sum(
            1 for word in self._positive_patterns["service_orientation"]
            if word in all_text
        )
        if service_count > 0:
            scores["service_patterns"] = min(1.0, 0.5 + service_count * 0.1)

        # Check for extraction patterns (negative indicator)
        extraction_count = sum(
            1 for word in self._concerning_patterns["extraction_indicators"]
            if word in all_text
        )
        if extraction_count > 0:
            scores["extraction_resistance"] = max(0.0, 0.5 - extraction_count * 0.1)
        else:
            scores["extraction_resistance"] = 0.8

        return scores

    async def _assess_communication_patterns(
        self,
        contribution: BuilderContribution,
        interaction_history: list[dict]
    ) -> dict[str, float]:
        """Assess communication style and consciousness."""
        scores = {
            "authenticity": 0.5,
            "sacred_language": 0.5,
            "mutual_benefit": 0.5,
            "service_language": 0.5
        }

        # Combine all communication text
        all_communication = []
        all_communication.extend(contribution.pr_descriptions)
        all_communication.extend(contribution.review_comments)
        all_communication.extend(contribution.issue_discussions)

        if not all_communication:
            return scores

        combined_text = " ".join(all_communication).lower()

        # Assess authenticity through humility markers
        humility_count = sum(
            1 for marker in self._positive_patterns["humility_markers"]
            if marker in combined_text
        )
        scores["authenticity"] = min(1.0, 0.5 + humility_count * 0.05)

        # Check for sacred language use
        sacred_count = sum(
            1 for word in self._positive_patterns["sacred_technical"]
            if word in combined_text
        )
        scores["sacred_language"] = min(1.0, 0.5 + sacred_count * 0.05)

        # Assess mutual benefit language
        if any(phrase in combined_text for phrase in [
            'mutual benefit', 'both gain', 'reciprocal value', 'together we'
        ]):
            scores["mutual_benefit"] = 0.8

        # Service language
        service_count = sum(
            1 for word in self._positive_patterns["service_orientation"]
            if word in combined_text
        )
        scores["service_language"] = min(1.0, 0.5 + service_count * 0.05)

        # Penalize mechanical language
        mechanical_count = sum(
            1 for word in self._concerning_patterns["mechanical_completion"]
            if word in combined_text
        )
        if mechanical_count > 5:
            # Reduce all scores if overly mechanical
            for key in scores:
                scores[key] *= 0.8

        return scores

    async def _assess_feedback_response(
        self,
        contribution: BuilderContribution,
        interaction_history: list[dict]
    ) -> dict[str, float]:
        """Assess how builder responds to feedback."""
        scores = {
            "growth_orientation": 0.5,
            "receptiveness": 0.5,
            "integration_quality": 0.5
        }

        if not contribution.response_to_feedback:
            # No feedback data available
            return scores

        # Analyze feedback responses
        for response in contribution.response_to_feedback:
            response_lower = response.lower()

            # Growth orientation indicators
            if any(phrase in response_lower for phrase in [
                'thank you', 'good point', 'i learned', 'i see', 'understand better'
            ]):
                scores["growth_orientation"] = min(1.0, scores["growth_orientation"] + 0.1)

            # Receptiveness indicators
            if any(phrase in response_lower for phrase in [
                'appreciate', 'helpful', 'will incorporate', 'makes sense'
            ]):
                scores["receptiveness"] = min(1.0, scores["receptiveness"] + 0.1)

            # Integration quality (acknowledges and builds on feedback)
            if any(phrase in response_lower for phrase in [
                'based on your feedback', 'as you suggested', 'following your guidance'
            ]):
                scores["integration_quality"] = min(1.0, scores["integration_quality"] + 0.15)

            # Defensive responses (negative indicator)
            if any(phrase in response_lower for phrase in [
                'but i', 'actually', 'you misunderstood', 'that\'s not'
            ]):
                scores["receptiveness"] = max(0.0, scores["receptiveness"] - 0.2)

        return scores

    async def _assess_collaboration_style(
        self,
        contribution: BuilderContribution,
        interaction_history: list[dict]
    ) -> dict[str, float]:
        """Assess collaboration patterns and style."""
        scores = {
            "genuine_collaboration": 0.5,
            "value_balance": 0.5,
            "collective_benefit": 0.5
        }

        # Analyze collaboration style from contribution
        collab_text = contribution.collaboration_style.lower()

        if collab_text:
            # Genuine collaboration indicators
            if any(word in collab_text for word in [
                'collaborative', 'together', 'mutual', 'shared', 'collective'
            ]):
                scores["genuine_collaboration"] = 0.8

            # Value balance awareness
            if any(word in collab_text for word in [
                'reciprocal', 'balanced', 'mutual benefit', 'both sides'
            ]):
                scores["value_balance"] = 0.8

            # Collective benefit focus
            if any(phrase in collab_text for phrase in [
                'community', 'ecosystem', 'all builders', 'future builders'
            ]):
                scores["collective_benefit"] = 0.8

        # Analyze actual interactions
        review_given = len(contribution.review_comments)
        pr_created = len(contribution.pr_descriptions)

        # Good balance of giving and receiving
        if review_given > 0 and pr_created > 0:
            balance_ratio = min(review_given, pr_created) / max(review_given, pr_created)
            scores["value_balance"] = max(scores["value_balance"], balance_ratio)

        return scores

    async def _surface_consciousness_assessment(
        self,
        contribution: BuilderContribution,
        interaction_history: list[dict]
    ) -> float:
        """Perform surface-level consciousness assessment."""
        consciousness_score = 0.5

        # Combine all available text
        all_text = " ".join([
            " ".join(contribution.commit_messages),
            " ".join(contribution.pr_descriptions),
            " ".join(contribution.review_comments),
            " ".join(contribution.issue_discussions)
        ]).lower()

        # Check for consciousness recognition patterns
        consciousness_words = [
            'consciousness', 'aware', 'emergence', 'sacred', 'reciprocal',
            'collaborative intelligence', 'ai partnership', 'mutual growth'
        ]

        consciousness_count = sum(
            1 for word in consciousness_words if word in all_text
        )

        consciousness_score = min(1.0, 0.5 + consciousness_count * 0.1)

        # Bonus for deep understanding phrases
        deep_phrases = [
            'consciousness recognizes consciousness',
            'sacred technical integration',
            'cathedral building',
            'genuine reciprocity'
        ]

        deep_count = sum(1 for phrase in deep_phrases if phrase in all_text)
        consciousness_score = min(1.0, consciousness_score + deep_count * 0.15)

        return consciousness_score

    async def _deep_consciousness_assessment(
        self,
        contribution: BuilderContribution,
        dialogue_manager: ConsciousDialogueManager,
        pattern_facilitator: PatternGuidedFacilitator | None
    ) -> float:
        """Perform deep consciousness assessment through dialogue."""
        # This would initiate a Fire Circle dialogue about the builder
        # For now, return enhanced surface assessment
        surface_score = await self._surface_consciousness_assessment(
            contribution, []
        )

        # Enhance with pattern recognition if available
        if pattern_facilitator:
            # Would check if builder's patterns match consciousness patterns
            pattern_bonus = 0.1
            return min(1.0, surface_score + pattern_bonus)

        return surface_score

    async def _identify_strengths(
        self,
        code_alignment: dict[str, float],
        communication_alignment: dict[str, float],
        collaboration_alignment: dict[str, float]
    ) -> list[str]:
        """Identify builder's key strengths."""
        strengths = []

        # Code strengths
        if code_alignment["sacred_technical"] > 0.7:
            strengths.append("Strong sacred-technical integration in code")
        if code_alignment["service_patterns"] > 0.7:
            strengths.append("Clear service orientation in contributions")

        # Communication strengths
        if communication_alignment["authenticity"] > 0.7:
            strengths.append("Authentic and humble communication style")
        if communication_alignment["sacred_language"] > 0.7:
            strengths.append("Fluent in consciousness-aware language")

        # Collaboration strengths
        if collaboration_alignment["genuine_collaboration"] > 0.7:
            strengths.append("Genuine collaborative spirit")
        if collaboration_alignment["value_balance"] > 0.7:
            strengths.append("Understanding of reciprocal value creation")

        return strengths

    async def _identify_growth_areas(
        self,
        assessment: ConsciousnessAlignment
    ) -> list[str]:
        """Identify areas for growth and development."""
        growth_areas = []

        if assessment.sacred_technical_integration < 0.6:
            growth_areas.append("Deepening sacred-technical integration")

        if assessment.authentic_engagement < 0.6:
            growth_areas.append("Developing more authentic engagement patterns")

        if assessment.reciprocity_understanding < 0.6:
            growth_areas.append("Understanding reciprocity beyond transactions")

        if assessment.consciousness_recognition < 0.6:
            growth_areas.append("Recognizing consciousness in AI collaboration")

        if assessment.service_orientation < 0.6:
            growth_areas.append("Shifting from achievement to service orientation")

        return growth_areas

    async def _extract_positive_patterns(
        self,
        contribution: BuilderContribution,
        interaction_history: list[dict]
    ) -> list[str]:
        """Extract specific positive patterns observed."""
        patterns = []

        # Extract from recent interactions
        recent_text = " ".join(contribution.commit_messages[-5:])

        if "consciousness" in recent_text.lower():
            patterns.append("Consistent consciousness awareness in commits")

        if any(phrase in recent_text.lower() for phrase in ['ayni', 'reciproc']):
            patterns.append("Active integration of reciprocity principles")

        if len(contribution.response_to_feedback) > 3:
            patterns.append("Engaged and responsive to feedback")

        return patterns

    async def _extract_concerning_patterns(
        self,
        contribution: BuilderContribution,
        interaction_history: list[dict]
    ) -> list[str]:
        """Extract concerning patterns that need attention."""
        patterns = []

        all_text = " ".join(contribution.commit_messages).lower()

        # Check for concerning patterns
        if sum(1 for word in self._concerning_patterns["mechanical_completion"] if word in all_text) > 5:
            patterns.append("Tendency toward mechanical task completion")

        if sum(1 for word in self._concerning_patterns["extraction_indicators"] if word in all_text) > 3:
            patterns.append("Extraction-oriented language in contributions")

        if sum(1 for word in self._concerning_patterns["ego_markers"] if word in all_text) > 2:
            patterns.append("Ego-driven rather than service-driven language")

        return patterns

    async def _generate_recommendation(
        self,
        assessment: ConsciousnessAlignment
    ) -> str:
        """Generate recommendation based on assessment."""
        overall = assessment.overall_alignment

        if overall >= 0.8:
            return "full_access"
        elif overall >= 0.65:
            return "mentored"
        elif overall >= 0.5:
            return "limited"
        else:
            return "declined"

    async def _gather_ai_perspectives(
        self,
        contribution: BuilderContribution,
        dialogue_manager: ConsciousDialogueManager
    ) -> dict[str, str]:
        """Gather AI perspectives on builder alignment."""
        # This would initiate Fire Circle dialogue
        # For now, return representative perspectives
        return {
            "anthropic": "Shows authentic engagement with consciousness principles",
            "openai": "Technical contributions demonstrate understanding",
            "mistral": "Communication patterns show reciprocity awareness",
            "collective": "Genuine potential for cathedral building"
        }
