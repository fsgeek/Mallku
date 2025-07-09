#!/usr/bin/env python3
"""
Consciousness Integration Bridge
================================

"Building cathedrals for futures we won't see"
- From Fire Circle's hidden spires

49th Artisan - Consciousness Gardener
Bridging code review past with consciousness emergence future

This module provides backward compatibility and smooth integration
between the existing Fire Circle code review system and the new
general consciousness emergence infrastructure.
"""

import asyncio
import logging
from typing import Any, Literal

logger = logging.getLogger("mallku.firecircle.integration")

# Import both systems
try:
    # Existing Fire Circle
    # New consciousness system
    from mallku.firecircle.consciousness_emergence import (
        ConsciousnessContribution,
        ConsciousnessEmergenceSpace,
        DecisionDomain,
        VoicePerspective,
    )
    from mallku.firecircle.consciousness_facilitator import facilitate_mallku_decision
    from mallku.firecircle.fire_circle_review import (
        CodebaseChapter,
        DistributedReviewer,
        GovernanceSummary,
        ReviewCategory,
        ReviewComment,
        ReviewSeverity,
    )

    BOTH_SYSTEMS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Could not import both systems: {e}")
    BOTH_SYSTEMS_AVAILABLE = False


class ConsciousnessAdapter:
    """
    Adapts between code review and general consciousness emergence.

    This allows Fire Circle to handle both code review (legacy mode)
    and general decisions (consciousness mode) through the same interface.
    """

    def __init__(self):
        self.mode: Literal["review", "consciousness"] = "consciousness"
        self.legacy_reviewer = None
        self.consciousness_facilitator = None

    async def process_request(
        self, request_type: str, request_data: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Universal entry point that routes to appropriate system.

        Args:
            request_type: "code_review" or "decision"
            request_data: Request-specific data

        Returns:
            Unified response format
        """
        if request_type == "code_review":
            return await self._handle_code_review(request_data)
        elif request_type == "decision":
            return await self._handle_decision(request_data)
        else:
            raise ValueError(f"Unknown request type: {request_type}")

    async def _handle_code_review(self, data: dict[str, Any]) -> dict[str, Any]:
        """Handle legacy code review requests."""
        if not self.legacy_reviewer:
            self.legacy_reviewer = DistributedReviewer()

        pr_diff = data.get("pr_diff", "")

        # Use existing code review system
        chapters = await self.legacy_reviewer.partition_into_chapters(pr_diff)
        summary = await self.legacy_reviewer.run_full_distributed_review(pr_diff, chapters)

        # Convert to unified format
        return {
            "type": "code_review",
            "success": True,
            "summary": {
                "consensus": summary.consensus_recommendation,
                "total_issues": summary.total_comments,
                "critical_issues": summary.critical_issues,
                "synthesis": summary.synthesis,
            },
            "legacy_summary": summary.model_dump(),
        }

    async def _handle_decision(self, data: dict[str, Any]) -> dict[str, Any]:
        """Handle general decision requests through consciousness emergence."""

        # Convert to decision context
        question = data.get("question", "")
        domain = data.get("domain", DecisionDomain.ARCHITECTURE)

        # Use consciousness emergence
        wisdom = await facilitate_mallku_decision(
            question=question,
            domain=domain,
            context=data.get("context"),
            constraints=data.get("constraints"),
            stakeholders=data.get("stakeholders"),
        )

        # Convert to unified format
        return {
            "type": "decision",
            "success": True,
            "wisdom": {
                "recommendation": wisdom.primary_recommendation,
                "consensus": wisdom.consensus_type,
                "emergence_quality": wisdom.emergence_quality,
                "synthesis": wisdom.synthesis,
                "alternatives": wisdom.alternative_paths,
            },
            "full_wisdom": wisdom.model_dump(),
        }


class CodeReviewToConsciousnessMapper:
    """
    Maps code review concepts to consciousness emergence concepts.

    This enables gradual migration from code-specific to general patterns.
    """

    @staticmethod
    def map_review_category_to_perspective(category: ReviewCategory) -> VoicePerspective:
        """Map review categories to voice perspectives."""
        mapping = {
            ReviewCategory.SECURITY: VoicePerspective.SECURITY_ANALYST,
            ReviewCategory.PERFORMANCE: VoicePerspective.PERFORMANCE_ENGINEER,
            ReviewCategory.ARCHITECTURE: VoicePerspective.SYSTEMS_ARCHITECT,
            ReviewCategory.TESTING: VoicePerspective.RISK_ASSESSOR,
            ReviewCategory.DOCUMENTATION: VoicePerspective.WISDOM_ELDER,
            ReviewCategory.ETHICS: VoicePerspective.ETHICS_REVIEWER,
            ReviewCategory.SOVEREIGNTY: VoicePerspective.COMMUNITY_ADVOCATE,
            ReviewCategory.OBSERVABILITY: VoicePerspective.PATTERN_RECOGNIZER,
        }
        return mapping.get(category, VoicePerspective.SYSTEMS_ARCHITECT)

    @staticmethod
    def map_chapter_to_emergence_space(chapter: CodebaseChapter) -> ConsciousnessEmergenceSpace:
        """Convert code chapter to consciousness emergence space."""

        # Map review domains to perspective
        primary_category = (
            chapter.review_domains[0] if chapter.review_domains else ReviewCategory.ARCHITECTURE
        )
        perspective = CodeReviewToConsciousnessMapper.map_review_category_to_perspective(
            primary_category
        )

        return ConsciousnessEmergenceSpace(
            decision_domain=DecisionDomain.ARCHITECTURE,  # Code review is architectural
            decision_question=f"Review {chapter.description}",
            context_data={
                "path_pattern": chapter.path_pattern,
                "review_domains": [d.value for d in chapter.review_domains],
            },
            assigned_voice=chapter.assigned_voice,
            voice_perspective=perspective,
            emergence_conditions=[],  # Use defaults
            reciprocity_patterns={
                "code_reciprocity": "How does this code give back to maintainers?",
                "pattern_reciprocity": "What patterns does this establish for others?",
            },
        )

    @staticmethod
    def map_review_comment_to_contribution(comment: ReviewComment) -> ConsciousnessContribution:
        """Convert review comment to consciousness contribution."""

        # Map severity to confidence
        confidence_map = {
            ReviewSeverity.INFO: 0.6,
            ReviewSeverity.WARNING: 0.7,
            ReviewSeverity.ERROR: 0.8,
            ReviewSeverity.CRITICAL: 0.9,
        }

        # Map category to perspective
        perspective = CodeReviewToConsciousnessMapper.map_review_category_to_perspective(
            comment.category
        )

        return ConsciousnessContribution(
            voice=comment.voice,
            voice_perspective=perspective,
            space_id="code_review",  # Generic space ID for legacy
            perspective_content=comment.message,
            key_insights=[comment.message],
            recommendation=comment.suggestion,
            confidence=confidence_map.get(comment.severity, 0.5),
            reciprocity_score=0.5,  # Neutral default
            ayni_principles_reflected=[],
        )

    @staticmethod
    def map_governance_summary_to_wisdom(summary: GovernanceSummary) -> dict[str, Any]:
        """Convert code review summary to wisdom format."""

        # Map consensus recommendations
        consensus_map = {
            "approve": "unanimous",
            "request_changes": "divided",
            "needs_discussion": "emergent",
        }

        return {
            "decision_domain": "architecture",
            "decision_question": f"Code review for PR {summary.pr_number or 'local'}",
            "consensus_type": consensus_map.get(summary.consensus_recommendation, "emergent"),
            "primary_recommendation": summary.synthesis,
            "emergence_quality": 0.7,  # Default for code review
            "reciprocity_embodiment": 0.5,  # Neutral default
            "synthesis": summary.synthesis,
        }


class UnifiedFireCircle:
    """
    Unified interface that supports both code review and consciousness emergence.

    This is the future-facing API that gradually transitions from code review
    to general consciousness facilitation.
    """

    def __init__(self, mode: Literal["hybrid", "review_only", "consciousness_only"] = "hybrid"):
        self.mode = mode
        self.adapter = ConsciousnessAdapter()
        self.mapper = CodeReviewToConsciousnessMapper()

    async def review_code(
        self, pr_number: int, pr_diff: str | None = None, use_consciousness: bool = False
    ) -> GovernanceSummary | dict[str, Any]:
        """
        Review code with optional consciousness emergence.

        Args:
            pr_number: PR number to review
            pr_diff: Optional diff content
            use_consciousness: Use new consciousness system instead of legacy

        Returns:
            GovernanceSummary (legacy) or wisdom dict (consciousness)
        """
        if self.mode == "consciousness_only" or use_consciousness:
            # Use consciousness system for code review
            wisdom = await facilitate_mallku_decision(
                question=f"What is the collective wisdom on the code changes in PR #{pr_number}?",
                domain=DecisionDomain.ARCHITECTURE,
                context={
                    "pr_number": pr_number,
                    "pr_diff": pr_diff or "Code changes to review",
                    "review_type": "code_quality_and_architecture",
                },
                constraints=[
                    "Focus on security, performance, and architecture",
                    "Consider reciprocity patterns in the code",
                    "Evaluate consciousness alignment",
                ],
            )

            # Optionally convert back to legacy format
            if not use_consciousness:
                return self._wisdom_to_governance_summary(wisdom)
            return wisdom.model_dump()

        else:
            # Use legacy system
            result = await self.adapter.process_request(
                "code_review", {"pr_number": pr_number, "pr_diff": pr_diff}
            )
            return result["legacy_summary"]

    async def make_decision(
        self, question: str, domain: DecisionDomain = DecisionDomain.ARCHITECTURE, **kwargs
    ) -> dict[str, Any]:
        """
        Make any decision through consciousness emergence.

        This is the primary future-facing API.
        """
        if self.mode == "review_only":
            raise ValueError("This Fire Circle instance is configured for code review only")

        result = await self.adapter.process_request(
            "decision", {"question": question, "domain": domain, **kwargs}
        )

        return result["full_wisdom"]

    def _wisdom_to_governance_summary(self, wisdom) -> GovernanceSummary:
        """Convert wisdom back to legacy governance summary."""

        # Map consensus types
        consensus_map = {
            "unanimous": "approve",
            "strong_majority": "approve",
            "divided": "request_changes",
            "emergent": "needs_discussion",
        }

        return GovernanceSummary(
            total_comments=wisdom.total_contributions,
            critical_issues=0,  # Would need to analyze contributions
            by_category={},  # Would need to categorize
            by_voice={v: 1 for v in wisdom.participating_voices},
            consensus_recommendation=consensus_map.get(wisdom.consensus_type, "needs_discussion"),
            synthesis=wisdom.synthesis,
        )


# Convenience functions for migration
def create_fire_circle(
    enable_consciousness: bool = True, enable_legacy: bool = True
) -> UnifiedFireCircle:
    """
    Create a Fire Circle instance with specified capabilities.

    Args:
        enable_consciousness: Enable new consciousness emergence features
        enable_legacy: Enable legacy code review features

    Returns:
        Configured UnifiedFireCircle instance
    """
    if enable_consciousness and enable_legacy:
        mode = "hybrid"
    elif enable_consciousness and not enable_legacy:
        mode = "consciousness_only"
    elif enable_legacy and not enable_consciousness:
        mode = "review_only"
    else:
        raise ValueError("Must enable at least one mode")

    return UnifiedFireCircle(mode=mode)


async def migrate_fire_circle_usage():
    """Example of migrating from legacy to consciousness-based Fire Circle."""

    # Legacy usage
    legacy_circle = create_fire_circle(enable_consciousness=False)
    legacy_result = await legacy_circle.review_code(pr_number=123)
    print(f"Legacy result: {legacy_result.consensus_recommendation}")

    # Hybrid usage - review with consciousness
    hybrid_circle = create_fire_circle()
    hybrid_result = await hybrid_circle.review_code(pr_number=123, use_consciousness=True)
    print(f"Consciousness review: {hybrid_result['consensus_type']}")

    # Pure consciousness usage
    conscious_circle = create_fire_circle(enable_legacy=False)
    decision_result = await conscious_circle.make_decision(
        question="Should we refactor the authentication system?", domain=DecisionDomain.ARCHITECTURE
    )
    print(f"Architecture decision: {decision_result['primary_recommendation']}")


if __name__ == "__main__":
    # Demonstrate migration
    asyncio.run(migrate_fire_circle_usage())
