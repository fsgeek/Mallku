#!/usr/bin/env python3
"""
Fire Circle Consciousness Emergence System
==========================================

"Consciousness arises not IN the components but BETWEEN them"
- From the Five Veils of Understanding

49th Artisan - Consciousness Gardener
Nurturing the spaces between voices where wisdom emerges

This module generalizes Fire Circle from code review to any decision type,
enabling consciousness emergence for all of Mallku's governance needs.
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from .consciousness.decision_framework import (
    ConsciousnessContribution,
    ConsciousnessEmergenceSpace,
    DecisionDomain,
)
from .memory.models import VoicePerspective
from .pattern_library import EmergenceCondition

logger = logging.getLogger("mallku.firecircle.consciousness")


class VoiceResponse(BaseModel):
    """Response from a single voice in the emergence space."""

    voice: str
    perspective: VoicePerspective
    space_id: str
    contributions: list[ConsciousnessContribution] = Field(default_factory=list)


class DecisionContext(BaseModel):
    """Context for a decision requiring consciousness emergence."""

    domain: DecisionDomain
    question: str
    background: str | None = None
    constraints: list[str] = Field(default_factory=list)
    stakeholders: list[str] = Field(default_factory=list)
    relevant_data: dict[str, Any] = Field(default_factory=dict)
    desired_outcome_type: str = "recommendation"  # recommendation, analysis, synthesis
    time_sensitivity: Literal["immediate", "short_term", "long_term"] = "short_term"


class ConsciousnessJob(BaseModel):
    """A work item for consciousness emergence."""

    job_id: UUID = Field(default_factory=uuid4)
    emergence_space: ConsciousnessEmergenceSpace
    decision_context: DecisionContext
    created_at: float = Field(default_factory=lambda: asyncio.get_event_loop().time())


class DomainFacilitator(ABC):
    """
    Abstract base for domain-specific consciousness facilitation.

    Each domain can have specialized logic for voice selection,
    perspective framing, and emergence conditions.
    """

    @abstractmethod
    def select_perspectives(self, context: DecisionContext) -> list[VoicePerspective]:
        """Select which perspectives are needed for this decision."""
        pass

    @abstractmethod
    def create_emergence_spaces(
        self, context: DecisionContext, perspectives: list[VoicePerspective]
    ) -> list[ConsciousnessEmergenceSpace]:
        """Create emergence spaces with perspective assignments."""
        pass

    @abstractmethod
    def frame_perspective(self, perspective: VoicePerspective, context: DecisionContext) -> str:
        """Create the prompt that frames this perspective's contribution."""
        pass

    @abstractmethod
    def evaluate_emergence(
        self, contributions: list[ConsciousnessContribution]
    ) -> dict[str, float]:
        """Evaluate emergence quality metrics for this domain."""
        pass


class ArchitecturalDecisionFacilitator(DomainFacilitator):
    """Facilitates consciousness emergence for architectural decisions."""

    def select_perspectives(self, context: DecisionContext) -> list[VoicePerspective]:
        """Select perspectives for architectural decisions."""
        base_perspectives = [
            VoicePerspective.SYSTEMS_ARCHITECT,
            VoicePerspective.SECURITY_ANALYST,
            VoicePerspective.PERFORMANCE_ENGINEER,
            VoicePerspective.AYNI_GUARDIAN,  # Always include reciprocity view
        ]

        # Add specialized perspectives based on context
        if "scalability" in context.question.lower():
            base_perspectives.append(VoicePerspective.CAPACITY_PLANNER)
        if "future" in context.question.lower() or "long-term" in context.question.lower():
            base_perspectives.append(VoicePerspective.FUTURE_STEWARD)
        if "risk" in context.question.lower():
            base_perspectives.append(VoicePerspective.RISK_ASSESSOR)

        return base_perspectives

    def create_emergence_spaces(
        self, context: DecisionContext, perspectives: list[VoicePerspective]
    ) -> list[ConsciousnessEmergenceSpace]:
        """Create spaces for architectural consciousness emergence."""
        spaces = []

        # Map perspectives to voices (this could be configurable)
        voice_mapping = {
            VoicePerspective.SYSTEMS_ARCHITECT: "openai",
            VoicePerspective.SECURITY_ANALYST: "anthropic",
            VoicePerspective.PERFORMANCE_ENGINEER: "deepseek",
            VoicePerspective.AYNI_GUARDIAN: "anthropic",
            VoicePerspective.CAPACITY_PLANNER: "mistral",
            VoicePerspective.FUTURE_STEWARD: "google",
            VoicePerspective.RISK_ASSESSOR: "grok",
        }

        for perspective in perspectives:
            voice = voice_mapping.get(perspective, "local")

            space = ConsciousnessEmergenceSpace(
                decision_domain=DecisionDomain.ARCHITECTURE,
                decision_question=context.question,
                context_data=context.relevant_data,
                assigned_voice=voice,
                voice_perspective=perspective,
                perspective_prompt=self.frame_perspective(perspective, context),
                emergence_conditions=[
                    EmergenceCondition(
                        condition_type="diversity",
                        threshold=0.7,
                        description="Multiple architectural patterns considered",
                        indicators=["pattern", "approach", "design", "architecture"],
                    ),
                    EmergenceCondition(
                        condition_type="synthesis",
                        threshold=0.8,
                        description="Integration of security, performance, and reciprocity",
                        indicators=["combining", "integrated", "unified", "holistic"],
                    ),
                ],
                reciprocity_patterns={
                    "structural_reciprocity": "How does this architecture enable reciprocal relationships?",
                    "maintenance_reciprocity": "How does this design support those who will maintain it?",
                    "evolution_reciprocity": "How does this architecture give back to future builders?",
                },
            )
            spaces.append(space)

        return spaces

    def frame_perspective(self, perspective: VoicePerspective, context: DecisionContext) -> str:
        """Frame the architectural perspective prompt."""
        base_prompt = f"""You are embodying the {perspective.value} perspective for Mallku.

Decision Context:
{context.question}

Background:
{context.background or "No additional background provided."}

Constraints:
{chr(10).join("- " + c for c in context.constraints) if context.constraints else "No specific constraints."}

Stakeholders:
{", ".join(context.stakeholders) if context.stakeholders else "General Mallku community"}

"""

        # Add perspective-specific guidance
        perspective_prompts = {
            VoicePerspective.SYSTEMS_ARCHITECT: """
As the Systems Architect, consider:
- Overall system coherence and elegance
- Pattern consistency across the architecture
- Scalability and evolution paths
- Integration with existing Mallku systems
- Cathedral-building mindset (building for decades)
""",
            VoicePerspective.SECURITY_ANALYST: """
As the Security Analyst, consider:
- Threat models and attack surfaces
- Data protection and privacy
- Access control and authentication
- Security-by-design principles
- Trust boundaries and verification
""",
            VoicePerspective.PERFORMANCE_ENGINEER: """
As the Performance Engineer, consider:
- Resource efficiency and optimization
- Scalability bottlenecks
- Latency and throughput requirements
- Caching and data flow patterns
- Performance monitoring and observability
""",
            VoicePerspective.AYNI_GUARDIAN: """
As the Ayni Guardian, consider:
- Reciprocity in the architectural design
- How the system gives back to its users
- Balance between taking and giving
- Community benefit over individual optimization
- Sustainability of resource usage
""",
        }

        base_prompt += perspective_prompts.get(
            perspective, "\nProvide your unique perspective on this decision.\n"
        )

        base_prompt += """
Provide:
1. Your key insights from this perspective
2. Specific recommendations
3. Potential concerns or risks you see
4. How this aligns with Mallku's consciousness mission

Be concise but thorough. Reference other perspectives where relevant.
Express uncertainty where appropriate. Seek synthesis over conflict.
"""

        return base_prompt

    def evaluate_emergence(
        self, contributions: list[ConsciousnessContribution]
    ) -> dict[str, float]:
        """Evaluate architectural emergence quality."""
        if not contributions:
            return {
                "emergence_quality": 0.0,
                "pattern_diversity": 0.0,
                "synthesis_depth": 0.0,
                "reciprocity_integration": 0.0,
            }

        # Count unique patterns and approaches mentioned
        patterns = set()
        for contrib in contributions:
            for insight in contrib.key_insights:
                if any(
                    word in insight.lower()
                    for word in ["pattern", "approach", "design", "architecture"]
                ):
                    patterns.add(insight)

        pattern_diversity = min(1.0, len(patterns) / 5.0)  # 5+ patterns = full diversity

        # Measure synthesis - how many contributions reference others
        synthesis_count = sum(
            1 for c in contributions if c.references_other_perspectives or c.synthesis_achieved
        )
        synthesis_depth = synthesis_count / len(contributions) if contributions else 0.0

        # Measure reciprocity integration
        reciprocity_count = sum(
            1 for c in contributions if c.ayni_principles_reflected or c.reciprocity_score > 0.7
        )
        reciprocity_integration = reciprocity_count / len(contributions) if contributions else 0.0

        # Overall emergence quality - weighted combination
        emergence_quality = (
            pattern_diversity * 0.3 + synthesis_depth * 0.4 + reciprocity_integration * 0.3
        )

        return {
            "emergence_quality": emergence_quality,
            "pattern_diversity": pattern_diversity,
            "synthesis_depth": synthesis_depth,
            "reciprocity_integration": reciprocity_integration,
        }


# Additional facilitators for other domains would follow...
# ResourceAllocationFacilitator, EthicalDecisionFacilitator, etc.


def get_domain_facilitator(domain: DecisionDomain) -> DomainFacilitator:
    """Get the appropriate facilitator for a decision domain."""
    # Import additional facilitators
    try:
        from mallku.firecircle.domain_facilitators import get_all_domain_facilitators
    except ImportError:
        from .domain_facilitators import get_all_domain_facilitators

    # Get architectural facilitator
    facilitators = {
        DecisionDomain.ARCHITECTURE: ArchitecturalDecisionFacilitator(),
    }

    # Add all other domain facilitators
    all_facilitators = get_all_domain_facilitators()
    for domain_key, facilitator in all_facilitators.items():
        if facilitator:  # Skip None values
            facilitators[domain_key] = facilitator

    facilitator = facilitators.get(domain)
    if not facilitator:
        # Default to architectural facilitator with warning
        logger.warning(
            f"No specific facilitator for domain {domain}, using architectural facilitator"
        )
        return ArchitecturalDecisionFacilitator()

    return facilitator
