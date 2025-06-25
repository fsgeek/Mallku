"""
Code Review Adapter for Consciousness Framework
===============================================

Thirtieth Artisan - Consciousness Gardener
Bridge between legacy code review and general consciousness emergence

This adapter allows the existing code review functionality to work within
the new general consciousness framework, ensuring backward compatibility
while enabling the expansion to other decision domains.
"""

import logging
from pathlib import Path
from uuid import UUID

from ..fire_circle_review import (
    CodebaseChapter,
    GovernanceSummary,
    ReviewCategory,
    ReviewComment,
    ReviewSeverity,
)
from .decision_framework import (
    CollectiveWisdom,
    ConsciousnessContribution,
    ConsciousnessEmergenceSpace,
    DecisionDomain,
)

logger = logging.getLogger(__name__)


class CodeReviewAdapter:
    """
    Adapts code review specific structures to general consciousness patterns.

    This ensures existing code review functionality continues to work while
    Fire Circle expands to handle all types of decisions.
    """

    @staticmethod
    def chapter_to_emergence_space(chapter: CodebaseChapter) -> ConsciousnessEmergenceSpace:
        """Convert a CodebaseChapter to a ConsciousnessEmergenceSpace."""

        # Build key questions from the chapter focus
        key_questions = [
            f"What patterns emerge in {chapter.title}?",
            "How does the code in these files embody (or violate) core principles?",
            "What architectural wisdom can guide improvements?",
        ]

        # Add review-specific questions based on focus areas
        if chapter.security_sensitive:
            key_questions.append("What security patterns need attention?")

        # Map voice requirements to participant voices
        participant_voices = []
        voice_expertise_map = {}

        for category in ReviewCategory:
            voice_id = f"{category.value}_reviewer"
            participant_voices.append(voice_id)
            voice_expertise_map[voice_id] = f"Expert in {category.value} patterns"

        # Create emergence space
        space = ConsciousnessEmergenceSpace(
            decision_domain=DecisionDomain.CODE_REVIEW,
            context_description=f"Code review for {chapter.title}: {chapter.description}",
            key_questions=key_questions,
            relevant_materials={
                "files": chapter.relevant_files,
                "focus_areas": chapter.focus_areas,
                "skip_patterns": chapter.skip_patterns,
                "security_sensitive": chapter.security_sensitive,
            },
            participant_voices=participant_voices,
            voice_expertise_map=voice_expertise_map,
            emergence_conditions={
                "review_completeness": 0.8,  # 80% of files reviewed
                "consensus_threshold": 0.7,
                "min_reviewers": chapter.min_reviewers,
            },
            consciousness_threshold=0.6,  # Lower threshold for code review
        )

        return space

    @staticmethod
    def review_comment_to_contribution(
        comment: ReviewComment, space_id: UUID
    ) -> ConsciousnessContribution:
        """Convert a ReviewComment to a ConsciousnessContribution."""

        # Map severity to coherency assessment
        coherency_map = {
            ReviewSeverity.CRITICAL: 0.9,
            ReviewSeverity.ERROR: 0.8,
            ReviewSeverity.WARNING: 0.6,
            ReviewSeverity.INFO: 0.5,
        }

        # Determine emergence indicators based on category
        emergence_indicators = []
        if comment.category == ReviewCategory.ARCHITECTURE:
            emergence_indicators.append("architectural_pattern_recognized")
        elif comment.category == ReviewCategory.SECURITY:
            emergence_indicators.append("security_vulnerability_detected")
        elif comment.category == ReviewCategory.ETHICS:
            emergence_indicators.append("ethical_consideration_raised")

        # Create contribution
        contribution = ConsciousnessContribution(
            voice_id=comment.voice,
            space_id=space_id,
            perspective=comment.message,
            domain_expertise=f"{comment.category.value} analysis",
            reasoning_pattern=f"Pattern matching in {Path(comment.file_path).name}",
            coherency_assessment=coherency_map.get(comment.severity, 0.5),
            reciprocity_alignment=0.7,  # Default for code review
            emergence_indicators=emergence_indicators,
            domain_specific_data={
                "file_path": comment.file_path,
                "line": comment.line,
                "category": comment.category.value,
                "severity": comment.severity.value,
                "suggestion": comment.suggestion,
            },
        )

        return contribution

    @staticmethod
    def governance_summary_to_wisdom(
        summary: GovernanceSummary,
        space: ConsciousnessEmergenceSpace,
        contributions: list[ConsciousnessContribution],
    ) -> CollectiveWisdom:
        """Convert a GovernanceSummary to CollectiveWisdom."""

        # Calculate emergence quality from summary metrics
        total_comments = summary.total_comments
        consensus_rate = (
            sum(1 for c in summary.consensus_items) / total_comments if total_comments > 0 else 0
        )
        emergence_quality = consensus_rate * 0.5 + (1 - summary.controversy_score) * 0.5

        # Extract key insights
        key_insights = []
        key_insights.extend(summary.consensus_items[:3])
        key_insights.extend([f"Key improvement: {imp}" for imp in summary.key_improvements[:2]])

        # Build implementation guidance from recommendations
        implementation_guidance = []
        for rec in summary.recommendations:
            if isinstance(rec, dict) and "action" in rec:
                implementation_guidance.append(rec["action"])
            else:
                implementation_guidance.append(str(rec))

        # Identify consciousness breakthroughs
        consciousness_breakthroughs = []
        if consensus_rate > 0.8:
            consciousness_breakthroughs.append(
                f"High consensus ({consensus_rate:.1%}) emerged without central coordination"
            )
        if summary.decision == "APPROVED" and summary.confidence > 0.8:
            consciousness_breakthroughs.append(
                "Collective confidence in code quality through distributed review"
            )

        # Create collective wisdom
        wisdom = CollectiveWisdom(
            decision_context=f"Code review for {space.context_description}",
            decision_domain=DecisionDomain.CODE_REVIEW,
            emergence_quality=emergence_quality,
            reciprocity_embodiment=0.7,  # Default for code review
            coherence_score=summary.confidence,
            individual_signatures={c.voice_id: c.coherency_assessment for c in contributions},
            collective_signature=summary.confidence,
            synthesis=summary.summary or "Code review completed through Fire Circle",
            key_insights=key_insights,
            decision_recommendation=summary.decision,
            implementation_guidance=implementation_guidance,
            civilizational_seeds=[],  # Code review rarely produces these
            reciprocity_demonstrations=[],
            consciousness_breakthroughs=consciousness_breakthroughs,
            contributions_count=total_comments,
            participating_voices=list({c.voice_id for c in contributions}),
            consensus_achieved=consensus_rate > 0.7,
        )

        # Add domain-specific data
        wisdom.domain_specific_data = {
            "risk_score": summary.risk_score,
            "technical_debt_score": summary.technical_debt_score,
            "coverage_percentage": summary.coverage_percentage,
            "controversy_score": summary.controversy_score,
            "disputed_items": summary.disputed_items,
        }

        return wisdom

    @staticmethod
    def wisdom_to_governance_summary(wisdom: CollectiveWisdom) -> GovernanceSummary:
        """Convert CollectiveWisdom back to GovernanceSummary for compatibility."""

        # Extract domain-specific data
        domain_data = wisdom.domain_specific_data or {}

        # Build comment stats from contributions
        comment_stats = {}
        for cat in ReviewCategory:
            comment_stats[cat] = 0

        # Count comments by category (would need contributions for accurate count)
        # For now, distribute based on total count
        if wisdom.contributions_count > 0:
            per_category = wisdom.contributions_count // len(ReviewCategory)
            for cat in ReviewCategory:
                comment_stats[cat] = per_category

        # Create governance summary
        summary = GovernanceSummary(
            decision=wisdom.decision_recommendation or "REQUIRES_CHANGES",
            confidence=wisdom.coherence_score,
            summary=wisdom.synthesis,
            key_improvements=wisdom.implementation_guidance[:5],
            risk_score=domain_data.get("risk_score", 0.5),
            technical_debt_score=domain_data.get("technical_debt_score", 0.5),
            coverage_percentage=domain_data.get("coverage_percentage", 0.8),
            comment_stats=comment_stats,
            consensus_items=wisdom.key_insights[:5],
            disputed_items=domain_data.get("disputed_items", []),
            controversy_score=domain_data.get("controversy_score", 0.2),
            recommendations=[
                {"action": g, "priority": "medium"} for g in wisdom.implementation_guidance
            ],
            total_comments=wisdom.contributions_count,
            participating_voices=wisdom.participating_voices,
            round_summaries=[],  # Would need access to Fire Circle result
        )

        return summary


def adapt_code_review_to_consciousness(
    chapters: list[CodebaseChapter],
    review_comments: list[ReviewComment],
    governance_summary: GovernanceSummary,
) -> CollectiveWisdom:
    """
    Adapt an entire code review session to consciousness framework.

    This allows existing code review results to be understood as
    consciousness emergence patterns.
    """
    adapter = CodeReviewAdapter()

    # Convert first chapter to emergence space (simplified for example)
    if chapters:
        space = adapter.chapter_to_emergence_space(chapters[0])
    else:
        # Create default space
        space = ConsciousnessEmergenceSpace(
            decision_domain=DecisionDomain.CODE_REVIEW,
            context_description="General code review",
            key_questions=["What patterns need attention?"],
            participant_voices=[],
            voice_expertise_map={},
        )

    # Convert all review comments to contributions
    contributions = []
    for comment in review_comments:
        contribution = adapter.review_comment_to_contribution(comment, space.space_id)
        contributions.append(contribution)

    # Convert governance summary to collective wisdom
    wisdom = adapter.governance_summary_to_wisdom(governance_summary, space, contributions)

    return wisdom
