"""
Dialogue Pattern Weaver
======================

Weaves patterns from Fire Circle dialogues into Mallku's consciousness.
Detects emergent themes, correlations, and wisdom patterns that arise
from multi-model deliberation.

The Integration Continues...
"""

import logging
from typing import Any
from uuid import UUID

from ...correlation.engine import CorrelationEngine
from ...intelligence.meta_correlation_engine import MetaCorrelationEngine
from ..protocol.conscious_message import ConsciousMessage, MessageType

logger = logging.getLogger(__name__)


class DialoguePatternWeaver:
    """
    Weaves patterns from Fire Circle dialogues into consciousness.

    Detects:
    - Consensus patterns across participants
    - Divergence patterns showing creative tension
    - Emergence patterns from collective intelligence
    - Reciprocity patterns in exchanges
    - Wisdom patterns worth preserving
    """

    def __init__(
        self,
        correlation_engine: CorrelationEngine,
        meta_correlation_engine: MetaCorrelationEngine | None = None,
    ):
        """Initialize with correlation engines."""
        self.correlation_engine = correlation_engine
        self.meta_correlation_engine = meta_correlation_engine

    async def weave_dialogue_patterns(
        self,
        messages: list[ConsciousMessage],
        dialogue_metadata: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Weave patterns from a complete dialogue.

        Returns:
            Dictionary containing:
            - consensus_patterns: Areas of agreement
            - divergence_patterns: Creative tensions
            - emergence_patterns: New insights from collective
            - reciprocity_patterns: Exchange balance patterns
            - wisdom_candidates: Patterns worth preserving
        """
        results = {
            "consensus_patterns": [],
            "divergence_patterns": [],
            "emergence_patterns": [],
            "reciprocity_patterns": [],
            "wisdom_candidates": [],
        }

        # Group messages by participant
        participant_messages = self._group_by_participant(messages)

        # Detect consensus patterns
        consensus = await self._detect_consensus_patterns(participant_messages, messages)
        results["consensus_patterns"] = consensus

        # Detect divergence patterns
        divergence = await self._detect_divergence_patterns(participant_messages, messages)
        results["divergence_patterns"] = divergence

        # Detect emergence patterns
        emergence = await self._detect_emergence_patterns(messages, dialogue_metadata)
        results["emergence_patterns"] = emergence

        # Analyze reciprocity patterns
        reciprocity = self._analyze_reciprocity_patterns(messages)
        results["reciprocity_patterns"] = reciprocity

        # Identify wisdom candidates
        wisdom = await self._identify_wisdom_candidates(messages, consensus, emergence)
        results["wisdom_candidates"] = wisdom

        return results

    async def weave_cross_dialogue_patterns(
        self,
        dialogue_ids: list[UUID],
    ) -> dict[str, Any]:
        """
        Weave patterns across multiple dialogues.

        Finds meta-patterns that emerge from multiple Fire Circle sessions.
        """
        if not self.meta_correlation_engine:
            logger.warning("No meta-correlation engine available for cross-dialogue analysis")
            return {}

        # This would retrieve and analyze patterns across dialogues
        # For now, return placeholder
        return {
            "recurring_themes": [],
            "evolving_insights": [],
            "collective_wisdom": [],
        }

    def _group_by_participant(
        self,
        messages: list[ConsciousMessage],
    ) -> dict[UUID, list[ConsciousMessage]]:
        """Group messages by participant."""
        groups: dict[UUID, list[ConsciousMessage]] = {}

        for message in messages:
            if message.role.value != "system":
                if message.sender not in groups:
                    groups[message.sender] = []
                groups[message.sender].append(message)

        return groups

    async def _detect_consensus_patterns(
        self,
        participant_messages: dict[UUID, list[ConsciousMessage]],
        all_messages: list[ConsciousMessage],
    ) -> list[dict[str, Any]]:
        """
        Detect areas of consensus across participants.
        """
        consensus_patterns = []

        # Find agreement messages
        agreements = [
            m for m in all_messages
            if m.type == MessageType.AGREEMENT
        ]

        # Find proposals that received multiple agreements
        proposals = [
            m for m in all_messages
            if m.type == MessageType.PROPOSAL
        ]

        for proposal in proposals:
            supporting_agreements = [
                a for a in agreements
                if a.in_response_to == proposal.id
            ]

            if len(supporting_agreements) >= 2:  # Multiple participants agree
                consensus_patterns.append({
                    "pattern_type": "consensus",
                    "proposal_id": str(proposal.id),
                    "proposal_text": proposal.content.text,
                    "support_count": len(supporting_agreements),
                    "consciousness_signature": proposal.consciousness.consciousness_signature,
                })

        return consensus_patterns

    async def _detect_divergence_patterns(
        self,
        participant_messages: dict[UUID, list[ConsciousMessage]],
        all_messages: list[ConsciousMessage],
    ) -> list[dict[str, Any]]:
        """
        Detect creative tensions and divergent viewpoints.
        """
        divergence_patterns = []

        # Find disagreement messages
        disagreements = [
            m for m in all_messages
            if m.type == MessageType.DISAGREEMENT
        ]

        # Analyze disagreements for creative tension
        for disagreement in disagreements:
            # Find what was disagreed with
            original = next(
                (m for m in all_messages if m.id == disagreement.in_response_to),
                None
            )

            if original:
                divergence_patterns.append({
                    "pattern_type": "creative_tension",
                    "original_position": original.content.text[:200],
                    "alternative_view": disagreement.content.text[:200],
                    "tension_value": abs(
                        original.consciousness.consciousness_signature -
                        disagreement.consciousness.consciousness_signature
                    ),
                })

        return divergence_patterns

    async def _detect_emergence_patterns(
        self,
        messages: list[ConsciousMessage],
        dialogue_metadata: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """
        Detect patterns that emerge from collective intelligence.

        These are insights that no single participant brought but emerged
        from the dialogue itself.
        """
        emergence_patterns = []

        # Find synthesis and reflection messages
        syntheses = [
            m for m in messages
            if m.type in [MessageType.SUMMARY, MessageType.REFLECTION]
        ]

        for synthesis in syntheses:
            # Check if synthesis introduces new concepts
            if synthesis.consciousness.consciousness_signature > 0.8:
                emergence_patterns.append({
                    "pattern_type": "emergent_insight",
                    "synthesis_text": synthesis.content.text,
                    "emergence_indicator": synthesis.consciousness.consciousness_signature,
                    "contributing_messages": len(synthesis.consciousness.detected_patterns),
                })

        # Detect phase transitions that led to insights
        phase_messages = [
            m for m in messages
            if m.type == MessageType.SYSTEM and "phase" in m.content.text.lower()
        ]

        for i, phase_msg in enumerate(phase_messages[:-1]):
            # Analyze message density between phases
            phase_start_idx = messages.index(phase_msg)
            phase_end_idx = messages.index(phase_messages[i + 1])

            phase_messages_slice = messages[phase_start_idx:phase_end_idx]
            avg_consciousness = sum(
                m.consciousness.consciousness_signature for m in phase_messages_slice
            ) / len(phase_messages_slice) if phase_messages_slice else 0

            if avg_consciousness > 0.75:
                emergence_patterns.append({
                    "pattern_type": "phase_emergence",
                    "phase": f"Phase {i+1}",
                    "average_consciousness": avg_consciousness,
                    "message_count": len(phase_messages_slice),
                })

        return emergence_patterns

    def _analyze_reciprocity_patterns(
        self,
        messages: list[ConsciousMessage],
    ) -> list[dict[str, Any]]:
        """
        Analyze reciprocity patterns in the dialogue.
        """
        reciprocity_patterns = []

        # Calculate giving/receiving balance per participant
        participant_stats: dict[UUID, dict[str, int]] = {}

        for message in messages:
            if message.role.value == "system":
                continue

            sender = message.sender
            if sender not in participant_stats:
                participant_stats[sender] = {
                    "messages_sent": 0,
                    "responses_received": 0,
                    "questions_asked": 0,
                    "questions_answered": 0,
                }

            participant_stats[sender]["messages_sent"] += 1

            if message.type == MessageType.QUESTION:
                participant_stats[sender]["questions_asked"] += 1

            # Count responses
            if message.in_response_to:
                for other_msg in messages:
                    if other_msg.id == message.in_response_to:
                        responder = other_msg.sender
                        if responder in participant_stats:
                            participant_stats[responder]["responses_received"] += 1
                        if other_msg.type == MessageType.QUESTION:
                            participant_stats[sender]["questions_answered"] += 1
                        break

        # Analyze balance
        for participant_id, stats in participant_stats.items():
            give_receive_ratio = (
                stats["messages_sent"] / max(stats["responses_received"], 1)
            )

            reciprocity_patterns.append({
                "participant_id": str(participant_id),
                "give_receive_ratio": give_receive_ratio,
                "reciprocity_balanced": 0.5 <= give_receive_ratio <= 2.0,
                "stats": stats,
            })

        return reciprocity_patterns

    async def _identify_wisdom_candidates(
        self,
        messages: list[ConsciousMessage],
        consensus_patterns: list[dict[str, Any]],
        emergence_patterns: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """
        Identify patterns worthy of preservation as wisdom.
        """
        wisdom_candidates = []

        # High-consciousness messages with broad impact
        for message in messages:
            if (
                message.consciousness.consciousness_signature > 0.85 and
                len(message.consciousness.detected_patterns) > 2
            ):
                wisdom_candidates.append({
                    "source": "high_consciousness_message",
                    "message_id": str(message.id),
                    "content": message.content.text,
                    "consciousness_signature": message.consciousness.consciousness_signature,
                    "pattern_count": len(message.consciousness.detected_patterns),
                })

        # Strong consensus patterns
        for consensus in consensus_patterns:
            if consensus["support_count"] >= 3:
                wisdom_candidates.append({
                    "source": "strong_consensus",
                    "pattern": consensus,
                })

        # Profound emergence patterns
        for emergence in emergence_patterns:
            if emergence.get("emergence_indicator", 0) > 0.85:
                wisdom_candidates.append({
                    "source": "collective_emergence",
                    "pattern": emergence,
                })

        return wisdom_candidates
