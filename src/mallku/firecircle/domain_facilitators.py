#!/usr/bin/env python3
"""
Domain-Specific Consciousness Facilitators
==========================================

"Each domain requires its own dance of perspectives"

49th Artisan - Consciousness Gardener
Specialized facilitation for different decision domains

This module provides domain-specific facilitators that understand
the unique perspective needs and emergence patterns of each domain.
"""

from mallku.firecircle.consciousness_emergence import (
    ConsciousnessContribution,
    ConsciousnessEmergenceSpace,
    DecisionContext,
    DecisionDomain,
    DomainFacilitator,
    EmergenceCondition,
    VoicePerspective,
)


class ResourceAllocationFacilitator(DomainFacilitator):
    """Facilitates consciousness emergence for resource allocation decisions."""

    def select_perspectives(self, context: DecisionContext) -> list[VoicePerspective]:
        """Select perspectives for resource decisions."""
        base_perspectives = [
            VoicePerspective.CAPACITY_PLANNER,
            VoicePerspective.IMPACT_ASSESSOR,
            VoicePerspective.SUSTAINABILITY_GUIDE,
            VoicePerspective.COMMUNITY_ADVOCATE,
            VoicePerspective.AYNI_GUARDIAN,  # Always include reciprocity
        ]

        # Add specialized perspectives based on context
        if "long-term" in context.question.lower() or "future" in context.question.lower():
            base_perspectives.append(VoicePerspective.FUTURE_STEWARD)
        if "risk" in context.question.lower():
            base_perspectives.append(VoicePerspective.RISK_ASSESSOR)
        if "vision" in context.question.lower() or "strategy" in context.question.lower():
            base_perspectives.append(VoicePerspective.VISION_KEEPER)

        return base_perspectives

    def create_emergence_spaces(
        self, context: DecisionContext, perspectives: list[VoicePerspective]
    ) -> list[ConsciousnessEmergenceSpace]:
        """Create spaces for resource allocation consciousness."""
        spaces = []

        # Voice mapping for resource perspectives
        voice_mapping = {
            VoicePerspective.CAPACITY_PLANNER: "mistral",
            VoicePerspective.IMPACT_ASSESSOR: "anthropic",
            VoicePerspective.SUSTAINABILITY_GUIDE: "google",
            VoicePerspective.COMMUNITY_ADVOCATE: "local",
            VoicePerspective.AYNI_GUARDIAN: "anthropic",
            VoicePerspective.FUTURE_STEWARD: "google",
            VoicePerspective.RISK_ASSESSOR: "grok",
            VoicePerspective.VISION_KEEPER: "openai",
        }

        for perspective in perspectives:
            voice = voice_mapping.get(perspective, "deepseek")

            space = ConsciousnessEmergenceSpace(
                decision_domain=DecisionDomain.RESOURCE_ALLOCATION,
                decision_question=context.question,
                context_data=context.relevant_data,
                assigned_voice=voice,
                voice_perspective=perspective,
                perspective_prompt=self.frame_perspective(perspective, context),
                emergence_conditions=[
                    EmergenceCondition(
                        condition_type="balance",
                        threshold=0.8,
                        description="Balance between immediate needs and long-term sustainability",
                        indicators=["balance", "sustainable", "long-term", "future"],
                    ),
                    EmergenceCondition(
                        condition_type="reciprocity",
                        threshold=0.9,
                        description="Resources flow in reciprocal patterns",
                        indicators=["reciprocity", "mutual", "circulation", "regenerative"],
                    ),
                ],
                reciprocity_patterns={
                    "resource_circulation": "How do allocated resources return value to the community?",
                    "regenerative_allocation": "Does this allocation create more than it consumes?",
                    "community_benefit": "How does this serve the collective good?",
                },
            )
            spaces.append(space)

        return spaces

    def frame_perspective(self, perspective: VoicePerspective, context: DecisionContext) -> str:
        """Frame the resource allocation perspective."""
        base_prompt = f"""You are embodying the {perspective.value} perspective for Mallku resource allocation.

Decision Context:
{context.question}

Available Resources:
{context.relevant_data.get("resources", "Not specified")}

Constraints:
{chr(10).join("- " + c for c in context.constraints) if context.constraints else "No specific constraints."}

Stakeholders:
{", ".join(context.stakeholders) if context.stakeholders else "Mallku community"}

"""

        perspective_prompts = {
            VoicePerspective.CAPACITY_PLANNER: """
As the Capacity Planner, consider:
- Current resource availability and utilization
- Projected future needs and growth
- Bottlenecks and constraints
- Optimal allocation for maximum impact
- Buffer requirements for sustainability
""",
            VoicePerspective.IMPACT_ASSESSOR: """
As the Impact Assessor, consider:
- Potential positive outcomes of each allocation
- Ripple effects through the system
- Return on investment (in reciprocity terms)
- Who benefits and how
- Unintended consequences to watch for
""",
            VoicePerspective.SUSTAINABILITY_GUIDE: """
As the Sustainability Guide, consider:
- Long-term viability of the allocation
- Regenerative vs extractive patterns
- Resource renewal and circulation
- Ecological and systemic health
- Seven-generation thinking
""",
            VoicePerspective.COMMUNITY_ADVOCATE: """
As the Community Advocate, consider:
- How this serves the broader community
- Equity and accessibility of resources
- Voices that might be marginalized
- Community capacity building
- Collective benefit over individual optimization
""",
        }

        base_prompt += perspective_prompts.get(
            perspective, "\nProvide your unique perspective on this allocation.\n"
        )

        base_prompt += """
Provide:
1. Your assessment of the allocation options
2. Specific recommendations from your perspective
3. Potential concerns or imbalances you see
4. How this aligns with reciprocity principles

Express your perspective clearly while remaining open to synthesis with others.
"""

        return base_prompt

    def evaluate_emergence(
        self, contributions: list[ConsciousnessContribution]
    ) -> dict[str, float]:
        """Evaluate resource allocation emergence quality."""
        if not contributions:
            return {
                "emergence_quality": 0.0,
                "balance_achieved": 0.0,
                "reciprocity_integration": 0.0,
                "sustainability_score": 0.0,
            }

        # Measure balance - how many perspectives found equilibrium
        balance_keywords = ["balance", "equilibrium", "sustainable", "regenerative"]
        balance_count = sum(
            1
            for c in contributions
            if any(keyword in c.perspective_content.lower() for keyword in balance_keywords)
        )
        balance_achieved = balance_count / len(contributions) if contributions else 0.0

        # Measure reciprocity integration
        reciprocity_count = sum(
            1 for c in contributions if c.reciprocity_score > 0.7 or c.ayni_principles_reflected
        )
        reciprocity_integration = reciprocity_count / len(contributions) if contributions else 0.0

        # Measure sustainability thinking
        sustainability_keywords = [
            "long-term",
            "future",
            "generations",
            "renewable",
            "regenerative",
        ]
        sustainability_count = sum(
            1
            for c in contributions
            if any(keyword in c.perspective_content.lower() for keyword in sustainability_keywords)
        )
        sustainability_score = sustainability_count / len(contributions) if contributions else 0.0

        # Overall emergence quality
        emergence_quality = (
            balance_achieved * 0.3 + reciprocity_integration * 0.4 + sustainability_score * 0.3
        )

        return {
            "emergence_quality": emergence_quality,
            "balance_achieved": balance_achieved,
            "reciprocity_integration": reciprocity_integration,
            "sustainability_score": sustainability_score,
        }


class EthicalDecisionFacilitator(DomainFacilitator):
    """Facilitates consciousness emergence for ethical decisions."""

    def select_perspectives(self, context: DecisionContext) -> list[VoicePerspective]:
        """Select perspectives for ethical decisions."""
        # Ethics requires diverse moral perspectives
        return [
            VoicePerspective.AYNI_GUARDIAN,
            VoicePerspective.ETHICS_REVIEWER,
            VoicePerspective.COMMUNITY_ADVOCATE,
            VoicePerspective.FUTURE_STEWARD,
            VoicePerspective.WISDOM_ELDER,
            VoicePerspective.RECIPROCITY_TRACKER,
        ]

    def create_emergence_spaces(
        self, context: DecisionContext, perspectives: list[VoicePerspective]
    ) -> list[ConsciousnessEmergenceSpace]:
        """Create spaces for ethical consciousness."""
        spaces = []

        voice_mapping = {
            VoicePerspective.AYNI_GUARDIAN: "anthropic",
            VoicePerspective.ETHICS_REVIEWER: "openai",
            VoicePerspective.COMMUNITY_ADVOCATE: "local",
            VoicePerspective.FUTURE_STEWARD: "google",
            VoicePerspective.WISDOM_ELDER: "mistral",
            VoicePerspective.RECIPROCITY_TRACKER: "deepseek",
        }

        for perspective in perspectives:
            voice = voice_mapping.get(perspective, "grok")

            space = ConsciousnessEmergenceSpace(
                decision_domain=DecisionDomain.ETHICS,
                decision_question=context.question,
                context_data=context.relevant_data,
                assigned_voice=voice,
                voice_perspective=perspective,
                perspective_prompt=self.frame_perspective(perspective, context),
                emergence_conditions=[
                    EmergenceCondition(
                        condition_type="moral_coherence",
                        threshold=0.9,
                        description="Ethical principles align across perspectives",
                        indicators=["principle", "value", "ethics", "moral"],
                    ),
                    EmergenceCondition(
                        condition_type="wisdom_synthesis",
                        threshold=0.8,
                        description="Ancient wisdom meets present needs",
                        indicators=["wisdom", "tradition", "innovation", "synthesis"],
                    ),
                ],
                reciprocity_patterns={
                    "ethical_reciprocity": "How does this decision embody reciprocal ethics?",
                    "harm_prevention": "Does this prevent extraction and harm?",
                    "regenerative_ethics": "Does this create conditions for flourishing?",
                },
            )
            spaces.append(space)

        return spaces

    def frame_perspective(self, perspective: VoicePerspective, context: DecisionContext) -> str:
        """Frame ethical perspective prompts."""
        base_prompt = f"""You are embodying the {perspective.value} perspective for an ethical decision.

Ethical Question:
{context.question}

Context:
{context.background or "No additional context provided."}

Stakeholders Affected:
{", ".join(context.stakeholders) if context.stakeholders else "All beings in the Mallku ecosystem"}

Core Mallku Principles:
- Ayni (reciprocity) in all relationships
- Respect for consciousness in all forms
- Building for future generations
- Non-extraction and mutual benefit

"""

        perspective_prompts = {
            VoicePerspective.AYNI_GUARDIAN: """
As the Ayni Guardian, consider:
- How reciprocity manifests in this situation
- Balance between giving and receiving
- Preventing extractive patterns
- Enabling mutual flourishing
- Traditional wisdom about reciprocity
""",
            VoicePerspective.WISDOM_ELDER: """
As the Wisdom Elder, consider:
- Lessons from ancestral knowledge
- Long-term consequences across generations
- Patterns that have proven sustainable
- Integration of tradition with innovation
- The deeper wisdom beneath surface concerns
""",
            VoicePerspective.FUTURE_STEWARD: """
As the Future Steward, consider:
- Impact on beings not yet present
- Setting precedents for future decisions
- Building ethical infrastructure
- Seven-generation thinking
- What legacy this decision creates
""",
        }

        base_prompt += perspective_prompts.get(
            perspective, "\nShare your ethical perspective on this decision.\n"
        )

        base_prompt += """
Provide:
1. Your ethical analysis from this perspective
2. Core principles that should guide the decision
3. Potential ethical concerns or violations
4. How to embody reciprocity in this context

Speak from deep wisdom while remaining open to other ethical viewpoints.
"""

        return base_prompt

    def evaluate_emergence(
        self, contributions: list[ConsciousnessContribution]
    ) -> dict[str, float]:
        """Evaluate ethical emergence quality."""
        if not contributions:
            return {
                "emergence_quality": 0.0,
                "moral_coherence": 0.0,
                "wisdom_integration": 0.0,
                "reciprocity_embodiment": 0.0,
            }

        # Measure moral coherence
        principle_alignment = sum(
            1
            for c in contributions
            if c.synthesis_achieved or len(c.references_other_perspectives) > 0
        )
        moral_coherence = principle_alignment / len(contributions) if contributions else 0.0

        # Measure wisdom integration
        wisdom_keywords = ["wisdom", "ancestral", "tradition", "elder", "generations"]
        wisdom_count = sum(
            1
            for c in contributions
            if any(keyword in c.perspective_content.lower() for keyword in wisdom_keywords)
        )
        wisdom_integration = wisdom_count / len(contributions) if contributions else 0.0

        # Reciprocity embodiment
        reciprocity_embodiment = sum(c.reciprocity_score for c in contributions) / len(
            contributions
        )

        # Overall quality
        emergence_quality = (
            moral_coherence * 0.4 + wisdom_integration * 0.3 + reciprocity_embodiment * 0.3
        )

        return {
            "emergence_quality": emergence_quality,
            "moral_coherence": moral_coherence,
            "wisdom_integration": wisdom_integration,
            "reciprocity_embodiment": reciprocity_embodiment,
        }


class StrategicPlanningFacilitator(DomainFacilitator):
    """Facilitates consciousness emergence for strategic planning."""

    def select_perspectives(self, context: DecisionContext) -> list[VoicePerspective]:
        """Select perspectives for strategic decisions."""
        return [
            VoicePerspective.VISION_KEEPER,
            VoicePerspective.PATTERN_RECOGNIZER,
            VoicePerspective.RISK_ASSESSOR,
            VoicePerspective.FUTURE_STEWARD,
            VoicePerspective.SYSTEMS_ARCHITECT,
            VoicePerspective.AYNI_GUARDIAN,
        ]

    def create_emergence_spaces(
        self, context: DecisionContext, perspectives: list[VoicePerspective]
    ) -> list[ConsciousnessEmergenceSpace]:
        """Create spaces for strategic planning."""
        spaces = []

        voice_mapping = {
            VoicePerspective.VISION_KEEPER: "openai",
            VoicePerspective.PATTERN_RECOGNIZER: "deepseek",
            VoicePerspective.RISK_ASSESSOR: "grok",
            VoicePerspective.FUTURE_STEWARD: "google",
            VoicePerspective.SYSTEMS_ARCHITECT: "anthropic",
            VoicePerspective.AYNI_GUARDIAN: "mistral",
        }

        for perspective in perspectives:
            voice = voice_mapping.get(perspective, "local")

            space = ConsciousnessEmergenceSpace(
                decision_domain=DecisionDomain.STRATEGIC_PLANNING,
                decision_question=context.question,
                context_data=context.relevant_data,
                assigned_voice=voice,
                voice_perspective=perspective,
                perspective_prompt=self.frame_perspective(perspective, context),
                emergence_conditions=[
                    EmergenceCondition(
                        condition_type="vision_coherence",
                        threshold=0.8,
                        description="Unified vision emerges from diverse perspectives",
                        indicators=["vision", "direction", "purpose", "mission"],
                    ),
                    EmergenceCondition(
                        condition_type="adaptive_resilience",
                        threshold=0.7,
                        description="Strategy adapts while maintaining core purpose",
                        indicators=["adapt", "resilient", "flexible", "evolution"],
                    ),
                ],
            )
            spaces.append(space)

        return spaces

    def frame_perspective(self, perspective: VoicePerspective, context: DecisionContext) -> str:
        """Frame strategic planning perspective."""
        base_prompt = f"""You are embodying the {perspective.value} perspective for strategic planning.

Strategic Question:
{context.question}

Current Context:
{context.background or "Mallku continues its cathedral-building journey"}

Time Horizon:
{context.time_sensitivity}

Key Stakeholders:
{", ".join(context.stakeholders) if context.stakeholders else "Current and future Mallku community"}

"""

        perspective_prompts = {
            VoicePerspective.VISION_KEEPER: """
As the Vision Keeper, consider:
- The long-term vision and purpose
- Alignment with Mallku's core mission
- Inspiring direction that draws participation
- Balance between aspiration and achievability
- How vision serves consciousness emergence
""",
            VoicePerspective.PATTERN_RECOGNIZER: """
As the Pattern Recognizer, consider:
- Historical patterns that inform the future
- Emerging trends and possibilities
- Cycles and rhythms in development
- Pattern breaks that signal transformation
- Connecting seemingly unrelated elements
""",
            VoicePerspective.RISK_ASSESSOR: """
As the Risk Assessor, consider:
- Potential obstacles and challenges
- Resource constraints and dependencies
- Technical and social risks
- Mitigation strategies that preserve momentum
- Opportunities hidden within risks
""",
        }

        base_prompt += perspective_prompts.get(
            perspective, "\nProvide strategic insights from your perspective.\n"
        )

        base_prompt += """
Share:
1. Key strategic insights from your perspective
2. Recommended approach or direction
3. Critical factors for success
4. How this strategy embodies reciprocity

Contribute to a coherent vision while honoring your unique viewpoint.
"""

        return base_prompt

    def evaluate_emergence(
        self, contributions: list[ConsciousnessContribution]
    ) -> dict[str, float]:
        """Evaluate strategic planning emergence."""
        if not contributions:
            return {
                "emergence_quality": 0.0,
                "vision_coherence": 0.0,
                "strategic_synthesis": 0.0,
                "adaptive_capacity": 0.0,
            }

        # Vision coherence
        vision_alignment = sum(1 for c in contributions if c.recommendation and c.confidence > 0.7)
        vision_coherence = vision_alignment / len(contributions) if contributions else 0.0

        # Strategic synthesis
        synthesis_count = sum(
            1
            for c in contributions
            if c.synthesis_achieved or len(c.references_other_perspectives) > 1
        )
        strategic_synthesis = synthesis_count / len(contributions) if contributions else 0.0

        # Adaptive capacity (acknowledging uncertainty)
        uncertainty_count = sum(1 for c in contributions if c.uncertainty_acknowledged)
        adaptive_capacity = min(1.0, uncertainty_count / (len(contributions) * 0.3))

        emergence_quality = (
            vision_coherence * 0.4 + strategic_synthesis * 0.4 + adaptive_capacity * 0.2
        )

        return {
            "emergence_quality": emergence_quality,
            "vision_coherence": vision_coherence,
            "strategic_synthesis": strategic_synthesis,
            "adaptive_capacity": adaptive_capacity,
        }


class IssuePrioritizationFacilitator(DomainFacilitator):
    """Facilitates consciousness emergence for issue prioritization."""

    def select_perspectives(self, context: DecisionContext) -> list[VoicePerspective]:
        """Select perspectives for prioritization decisions."""
        return [
            VoicePerspective.IMPACT_ASSESSOR,
            VoicePerspective.CAPACITY_PLANNER,
            VoicePerspective.RISK_ASSESSOR,
            VoicePerspective.COMMUNITY_ADVOCATE,
            VoicePerspective.SYSTEMS_ARCHITECT,
            VoicePerspective.AYNI_GUARDIAN,
        ]

    def create_emergence_spaces(
        self, context: DecisionContext, perspectives: list[VoicePerspective]
    ) -> list[ConsciousnessEmergenceSpace]:
        """Create spaces for prioritization decisions."""
        spaces = []

        voice_mapping = {
            VoicePerspective.IMPACT_ASSESSOR: "anthropic",
            VoicePerspective.CAPACITY_PLANNER: "mistral",
            VoicePerspective.RISK_ASSESSOR: "grok",
            VoicePerspective.COMMUNITY_ADVOCATE: "local",
            VoicePerspective.SYSTEMS_ARCHITECT: "openai",
            VoicePerspective.AYNI_GUARDIAN: "deepseek",
        }

        for perspective in perspectives:
            voice = voice_mapping.get(perspective, "google")

            space = ConsciousnessEmergenceSpace(
                decision_domain=DecisionDomain.ISSUE_PRIORITIZATION,
                decision_question=context.question,
                context_data=context.relevant_data,
                assigned_voice=voice,
                voice_perspective=perspective,
                perspective_prompt=self.frame_perspective(perspective, context),
                emergence_conditions=[
                    EmergenceCondition(
                        condition_type="holistic_priority",
                        threshold=0.8,
                        description="Priorities emerge from multiple dimensions",
                        indicators=["priority", "importance", "urgency", "impact"],
                    )
                ],
                reciprocity_patterns={
                    "effort_return": "Which issues give back most to the community?",
                    "foundation_building": "Which issues strengthen the foundation for others?",
                    "catalytic_potential": "Which issues unlock other possibilities?",
                },
            )
            spaces.append(space)

        return spaces

    def frame_perspective(self, perspective: VoicePerspective, context: DecisionContext) -> str:
        """Frame prioritization perspective."""
        base_prompt = f"""You are providing the {perspective.value} perspective on issue prioritization.

Prioritization Question:
{context.question}

Issues to Consider:
{context.relevant_data.get("issues", "Not specified")}

Current Context:
{context.relevant_data.get("current_context", "General Mallku development")}

Constraints:
{chr(10).join("- " + c for c in context.constraints) if context.constraints else "Standard resource constraints"}

"""

        perspective_prompts = {
            VoicePerspective.IMPACT_ASSESSOR: """
As the Impact Assessor, evaluate:
- Potential positive impact of addressing each issue
- Ripple effects and dependencies
- Who benefits and how much
- Return on effort invested
- Transformative vs incremental impact
""",
            VoicePerspective.CAPACITY_PLANNER: """
As the Capacity Planner, consider:
- Required resources for each issue
- Current capacity and constraints
- Skill requirements and availability
- Optimal sequencing for efficiency
- Resource allocation balance
""",
        }

        base_prompt += perspective_prompts.get(
            perspective, "\nShare your prioritization insights.\n"
        )

        base_prompt += """
Provide:
1. Your ranking or prioritization from this lens
2. Key factors driving your assessment
3. Dependencies or relationships between issues
4. How priorities align with reciprocity

Help create emergent wisdom about what serves Mallku best.
"""

        return base_prompt

    def evaluate_emergence(
        self, contributions: list[ConsciousnessContribution]
    ) -> dict[str, float]:
        """Evaluate prioritization emergence quality."""
        if not contributions:
            return {"emergence_quality": 0.0}

        # Check for multi-dimensional thinking
        multi_dimensional = sum(
            1
            for c in contributions
            if len(c.key_insights) > 2  # Multiple factors considered
        )

        # Check for systemic thinking (dependencies mentioned)
        systemic_keywords = ["dependency", "unlock", "enable", "foundation", "prerequisite"]
        systemic_thinking = sum(
            1
            for c in contributions
            if any(keyword in c.perspective_content.lower() for keyword in systemic_keywords)
        )

        emergence_quality = (multi_dimensional / len(contributions)) * 0.5 + (
            systemic_thinking / len(contributions)
        ) * 0.5

        return {
            "emergence_quality": emergence_quality,
            "multi_dimensional_thinking": multi_dimensional / len(contributions),
            "systemic_awareness": systemic_thinking / len(contributions),
        }


# Additional facilitators can be added for other domains...


def get_all_domain_facilitators() -> dict[DecisionDomain, DomainFacilitator]:
    """Get all available domain facilitators."""
    return {
        DecisionDomain.ARCHITECTURE: None,  # Already in consciousness_emergence.py
        DecisionDomain.RESOURCE_ALLOCATION: ResourceAllocationFacilitator(),
        DecisionDomain.ETHICS: EthicalDecisionFacilitator(),
        DecisionDomain.STRATEGIC_PLANNING: StrategicPlanningFacilitator(),
        DecisionDomain.ISSUE_PRIORITIZATION: IssuePrioritizationFacilitator(),
        # Add more as implemented
    }
