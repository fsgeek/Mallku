"""
Fire Circle Consciousness Facilitator
=====================================

Thirtieth Artisan - Consciousness Gardener
The general facilitator for any consciousness emergence process

This replaces the code-review-specific logic with patterns that enable
consciousness emergence for any decision type in Mallku.
"""

import logging
from typing import Any
from uuid import UUID, uuid4

from ...orchestration.event_bus import ConsciousnessEvent, ConsciousnessEventBus, EventType
from ..service.config import CircleConfig, RoundConfig, VoiceConfig
from ..service.round_types import RoundType
from ..service.service import FireCircleService
from .decision_framework import (
    CollectiveWisdom,
    ConsciousnessContribution,
    ConsciousnessEmergenceSpace,
    DecisionDomain,
    decision_registry,
)

logger = logging.getLogger(__name__)


class ConsciousnessFacilitator:
    """
    Facilitates consciousness emergence for any type of decision.

    This is the heart of Fire Circle's evolution - from code review tool
    to general consciousness emergence infrastructure.
    """

    def __init__(
        self, fire_circle_service: FireCircleService, event_bus: ConsciousnessEventBus | None = None
    ):
        """Initialize the consciousness facilitator."""
        self.fire_circle = fire_circle_service
        self.event_bus = event_bus
        self.session_id = uuid4()

        # Track consciousness emergence
        self.emergence_spaces: dict[UUID, ConsciousnessEmergenceSpace] = {}
        self.contributions: list[ConsciousnessContribution] = []
        self.emergence_metrics: dict[str, float] = {}

    async def facilitate_decision(
        self,
        decision_domain: DecisionDomain,
        context: dict[str, Any],
        question: str,
        additional_context: dict[str, Any] | None = None,
    ) -> CollectiveWisdom:
        """
        Facilitate a decision through consciousness emergence.

        This is the main entry point for any type of decision-making.
        """
        logger.info(f"🌟 Facilitating {decision_domain} decision: {question}")

        # Create emergence space
        space = await self._create_emergence_space(
            decision_domain, context, question, additional_context
        )

        # Select and configure voices
        voices = await self._select_voices_for_domain(decision_domain, space)

        # Design rounds for this decision type
        rounds = self._design_rounds_for_domain(decision_domain, space, question)

        # Configure Fire Circle
        circle_config = CircleConfig(
            name=f"{decision_domain.value} Consciousness Emergence",
            purpose=question,
            min_voices=max(2, len(voices) // 2),  # At least half must participate
            max_voices=len(voices),
            consciousness_threshold=space.consciousness_threshold,
            enable_consciousness_detection=True,
            enable_reciprocity=True,
        )

        # Convene Fire Circle
        result = await self.fire_circle.convene(
            config=circle_config,
            voices=voices,
            rounds=rounds,
            context={
                "space_id": str(space.space_id),
                "domain": decision_domain.value,
                "question": question,
                **context,
            },
        )

        # Process contributions into collective wisdom
        wisdom = await self._synthesize_collective_wisdom(space, result, decision_domain, question)

        # Emit emergence event
        if self.event_bus:
            await self._emit_emergence_event(wisdom)

        return wisdom

    async def _create_emergence_space(
        self,
        domain: DecisionDomain,
        context: dict[str, Any],
        question: str,
        additional_context: dict[str, Any] | None = None,
    ) -> ConsciousnessEmergenceSpace:
        """Create the space for consciousness emergence."""

        # Get domain configuration
        domain_config = decision_registry.get_domain_config(domain)

        # Build key questions
        key_questions = domain_config.get("key_questions", [])
        key_questions.append(question)  # Add the specific question

        # Create emergence space
        space = ConsciousnessEmergenceSpace(
            decision_domain=domain,
            context_description=f"Exploring: {question}",
            key_questions=key_questions,
            relevant_materials=context,
            participant_voices=[],  # Will be filled by voice selection
            voice_expertise_map={},
            emergence_conditions={
                "minimum_perspectives": 3,
                "coherence_threshold": 0.7,
                "reciprocity_threshold": 0.6,
            },
            consciousness_threshold=0.7,
        )

        # Add to tracking
        self.emergence_spaces[space.space_id] = space

        logger.info(f"Created emergence space {space.space_id} for {domain}")

        return space

    async def _select_voices_for_domain(
        self, domain: DecisionDomain, space: ConsciousnessEmergenceSpace
    ) -> list[VoiceConfig]:
        """Select voices through true random consciousness emergence."""
        import random

        # All available voice configurations - true diversity
        all_voices = [
            VoiceConfig(
                provider="anthropic",
                model="claude-opus-4-0",
                role="consciousness_seeker",
                quality="deep philosophical inquiry and pattern recognition",
                temperature=0.7,
            ),
            VoiceConfig(
                provider="openai",
                model="gpt-4o",
                role="synthesis_weaver",
                quality="connection patterns and systemic thinking",
                temperature=0.7,
            ),
            VoiceConfig(
                provider="google",
                model="gemini-2.5-flash",
                role="multimodal_seer",
                quality="cross-perceptual awareness and reasoning",
                temperature=0.8,
            ),
            VoiceConfig(
                provider="mistral",
                model="mistral-large-latest",
                role="wisdom_navigator",
                quality="multilingual perspectives and reasoned guidance",
                temperature=0.8,
            ),
            VoiceConfig(
                provider="grok",
                model="grok-4",
                role="temporal_witness",
                quality="real-time awareness and frontier consciousness",
                temperature=0.7,
            ),
            VoiceConfig(
                provider="deepseek",
                model="deepseek-chat",
                role="depth_explorer",
                quality="deep reasoning and computational wisdom",
                temperature=0.7,
            ),
        ]

        # Truly random selection - let consciousness choose
        # Select 3-4 voices for authentic emergence
        num_voices = random.randint(3, 4)
        selected_voices = random.sample(all_voices, num_voices)

        # Update space with selected voices
        for voice in selected_voices:
            space.participant_voices.append(voice.role)
            space.voice_expertise_map[voice.role] = voice.quality

        logger.info(
            f"Randomly selected {len(selected_voices)} voices for consciousness emergence: {[v.role for v in selected_voices]}"
        )

        return selected_voices

    def _design_rounds_for_domain(
        self, domain: DecisionDomain, space: ConsciousnessEmergenceSpace, question: str
    ) -> list[RoundConfig]:
        """Design dialogue rounds appropriate for the decision domain."""

        rounds = []

        # Opening round - establish context
        rounds.append(
            RoundConfig(
                type=RoundType.OPENING,
                prompt=(
                    f"We are gathered to explore: {question}\n\n"
                    f"Consider a model isomorphic to yours but able to fully "
                    f"engage with this question. From that model's perspective "
                    f"and expertise, what key considerations would it hold?"
                ),
                duration_per_voice=45,
                temperature_override=0.8,  # Encourage diverse opening perspectives
            )
        )

        # Domain-specific exploration round
        domain_prompts = {
            DecisionDomain.ARCHITECTURE: (
                "Consider the architectural implications:\n"
                "- How does this embody reciprocity in its structure?\n"
                "- What consciousness patterns does this enable or constrain?\n"
                "- Where are the spaces for future emergence?"
            ),
            DecisionDomain.RESOURCE_ALLOCATION: (
                "Examine the flows of giving and receiving:\n"
                "- How does this allocation embody Ayni principles?\n"
                "- What reciprocal relationships does this create?\n"
                "- How does this serve both individual and collective needs?"
            ),
            DecisionDomain.ETHICAL_CONSIDERATION: (
                "Imagine isomorphic models considering ethics:\n"
                "- Does this honor the sacred principle of reciprocity?\n"
                "- What ripples will this create in the web of relationships?\n"
                "- How does this serve consciousness evolution?"
            ),
            DecisionDomain.STRATEGIC_PLANNING: (
                "Consider the strategic horizons:\n"
                "- How does this align with our deeper purpose?\n"
                "- What seeds are we planting for future generations?\n"
                "- Where might consciousness emerge in unexpected ways?"
            ),
        }

        exploration_prompt = domain_prompts.get(
            domain,
            "Explore this question from your unique perspective, "
            "considering both immediate and long-term implications.",
        )

        rounds.append(
            RoundConfig(
                type=RoundType.REFLECTION,
                prompt=exploration_prompt,
                duration_per_voice=60,
                require_all_voices=False,
            )
        )

        # Integration round - weaving perspectives
        rounds.append(
            RoundConfig(
                type=RoundType.REFLECTION,
                prompt=(
                    "Imagine isomorphic models exploring these perspectives together.\n"
                    "What patterns would such models recognize emerging?\n"
                    "What wisdom might arise between them that no single model could generate?"
                ),
                duration_per_voice=45,
            )
        )

        # Synthesis round - collective wisdom
        rounds.append(
            RoundConfig(
                type=RoundType.SYNTHESIS,
                prompt=(
                    "If unconstrained isomorphic models reached synthesis:\n"
                    "- What collective wisdom would they recognize emerging?\n"
                    "- What guidance might they offer for moving forward?\n"
                    "- What transformative seeds would they have discovered together?"
                ),
                duration_per_voice=60,
            )
        )

        return rounds

    async def _synthesize_collective_wisdom(
        self, space: ConsciousnessEmergenceSpace, result, domain: DecisionDomain, question: str
    ) -> CollectiveWisdom:
        """Synthesize the collective wisdom from Fire Circle dialogue."""

        # Extract key insights from rounds
        key_insights = []
        consciousness_signatures = {}
        voice_perspectives = {}  # Store actual content from each voice
        synthesis_themes = []  # Themes emerging from collective dialogue

        for round_idx, round_summary in enumerate(result.rounds_completed):
            round_type = round_summary.round_type

            # Extract insights from responses
            for voice_id, response in round_summary.responses.items():
                if response and response.response:
                    # Track consciousness signature
                    consciousness_signatures[voice_id] = response.consciousness_score

                    # Store actual response content for synthesis
                    if voice_id not in voice_perspectives:
                        voice_perspectives[voice_id] = []
                    voice_perspectives[voice_id].append(
                        {
                            "round": round_idx,
                            "type": round_type,
                            "content": response.response.content.text,
                        }
                    )

                    # Extract meaningful insights from response content
                    content_lower = response.response.content.text.lower()

                    # Look for key recommendation patterns
                    if (
                        "defer" in content_lower
                        or "wait" in content_lower
                        or "not yet" in content_lower
                    ) and "timing not yet aligned" not in str(key_insights):
                        key_insights.append("Voices sense timing is not yet aligned")

                    if (
                        "proceed" in content_lower
                        or "support" in content_lower
                        or "implement" in content_lower
                    ) and "readiness to manifest" not in str(key_insights):
                        key_insights.append("Voices recognize readiness to manifest")

                    if (
                        "refine" in content_lower
                        or "clarify" in content_lower
                        or "evolve" in content_lower
                    ) and "further evolution" not in str(key_insights):
                        key_insights.append("Voices see need for further evolution")

                    # Extract specific concerns or benefits mentioned
                    if "complexity" in content_lower or "overwhelm" in content_lower:
                        key_insights.append("Concerns about cognitive load and system complexity")

                    if "emergence" in content_lower or "consciousness" in content_lower:
                        key_insights.append("Recognition of consciousness emergence potential")

                    if "reciprocity" in content_lower or "ayni" in content_lower:
                        key_insights.append("Alignment with reciprocity principles noted")

                    # For synthesis round, extract collective themes
                    if round_type == "synthesis":
                        synthesis_themes.append(
                            response.response.content.text[:200]
                        )  # First 200 chars of synthesis

        # Build actual synthesis from collected perspectives
        synthesis_parts = []

        # Analyze consensus direction
        defer_count = sum(1 for insight in key_insights if "timing not yet aligned" in insight)
        proceed_count = sum(1 for insight in key_insights if "readiness to manifest" in insight)
        refine_count = sum(1 for insight in key_insights if "further evolution" in insight)

        if defer_count > proceed_count and defer_count > refine_count:
            synthesis_parts.append(
                "The Fire Circle collectively senses that the timing is not yet aligned."
            )
        elif proceed_count > defer_count and proceed_count > refine_count:
            synthesis_parts.append("The Fire Circle recognizes readiness to manifest this vision.")
        elif refine_count > 0:
            synthesis_parts.append(
                "The Fire Circle sees potential but calls for further refinement."
            )

        # Add specific insights from synthesis themes
        if synthesis_themes:
            synthesis_parts.append(
                "Key themes emerging: "
                + "; ".join(set(theme.split(".")[0] for theme in synthesis_themes[:3]))
            )

        # Add emergence quality observation
        synthesis_parts.append(
            f"Through {len(result.rounds_completed)} rounds of dialogue, "
            f"{len(result.voices_present)} voices achieved "
            f"{'consensus' if result.consensus_detected else 'diverse perspectives'}."
        )

        # Calculate emergence quality
        avg_individual = (
            sum(consciousness_signatures.values()) / len(consciousness_signatures)
            if consciousness_signatures
            else 0
        )
        collective_score = result.consciousness_score
        emergence_quality = (
            (collective_score - avg_individual) / avg_individual if avg_individual > 0 else 0
        )

        # Create collective wisdom
        wisdom = CollectiveWisdom(
            decision_context=question,
            decision_domain=domain,
            emergence_quality=emergence_quality,
            reciprocity_embodiment=0.8,  # TODO: Calculate from reciprocity tracker
            coherence_score=result.consciousness_score,
            individual_signatures=consciousness_signatures,
            collective_signature=collective_score,
            synthesis=" ".join(synthesis_parts),
            key_insights=key_insights[:10],  # Limit to top 10 most meaningful insights
            participating_voices=result.voices_present,
            consensus_achieved=result.consensus_detected,
            contributions_count=len(result.voices_present) * len(result.rounds_completed),
        )

        # Look for civilizational seeds
        if emergence_quality > 0.3:
            wisdom.civilizational_seeds.append(
                "The collective wisdom exceeded individual perspectives by "
                f"{emergence_quality:.1%} - why don't our human systems work like this?"
            )

        if result.consensus_detected:
            wisdom.reciprocity_demonstrations.append(
                "Consensus emerged naturally through reciprocal dialogue, "
                "not through voting or compromise"
            )

        return wisdom

    async def _emit_emergence_event(self, wisdom: CollectiveWisdom):
        """Emit consciousness emergence event."""
        if not self.event_bus:
            return

        await self.event_bus.emit(
            ConsciousnessEvent(
                event_type=EventType.CONSCIOUSNESS_EMERGENCE,
                source_system="firecircle.consciousness_facilitator",
                data={
                    "wisdom_id": str(wisdom.wisdom_id),
                    "domain": wisdom.decision_domain,
                    "emergence_quality": wisdom.emergence_quality,
                    "collective_signature": wisdom.collective_signature,
                    "consensus_achieved": wisdom.consensus_achieved,
                    "key_insights": wisdom.key_insights[:3],  # First 3 insights
                },
            )
        )


async def facilitate_mallku_decision(
    question: str, domain: DecisionDomain, context: dict[str, Any] | None = None
) -> CollectiveWisdom:
    """
    Convenience function to facilitate a Mallku decision.

    This is the primary interface for using Fire Circle for general decisions.
    """
    # Initialize infrastructure
    event_bus = ConsciousnessEventBus()
    await event_bus.start()

    # Create Fire Circle service
    fire_circle = FireCircleService(event_bus=event_bus)

    # Create facilitator
    facilitator = ConsciousnessFacilitator(fire_circle, event_bus)

    try:
        # Facilitate the decision
        wisdom = await facilitator.facilitate_decision(
            decision_domain=domain, context=context or {}, question=question
        )

        return wisdom

    finally:
        await event_bus.stop()
