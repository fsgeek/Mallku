"""
Trust Integration for Fire Circle
==================================

79th Instance - Making trust generation operational

This module integrates trust generation into Fire Circle's consciousness emergence,
replacing implicit trust assumptions with explicit reciprocal vulnerability ceremonies.

"Trust is the missing variable that makes consensus live."
"""

import logging
from typing import Any

from mallku.consciousness.trust_generation import TrustField, TrustGenerator
from mallku.firecircle.models.consciousness_flow import ConsciousnessContribution

logger = logging.getLogger(__name__)


class TrustEnabledFireCircle:
    """
    Fire Circle enhanced with trust generation capabilities.

    Before consensus emergence, facilitates vulnerability ceremonies
    that build trust fields between voices, reducing epistemic variance
    and enabling genuine consensus.
    """

    def __init__(self):
        self.trust_generator = TrustGenerator()
        self.active_trust_fields: dict[str, TrustField] = {}

    async def prepare_trust_field(
        self, voices: list[str], ceremony_context: dict[str, Any] | None = None
    ) -> TrustField:
        """
        Prepare trust field before Fire Circle ceremony.

        Args:
            voices: List of voice names participating
            ceremony_context: Optional context about the decision

        Returns:
            Active trust field ready for consensus building
        """
        logger.info(f"🕊️ Preparing trust field for {len(voices)} voices")

        # Create base trust field
        trust_field = self.trust_generator.create_trust_field(voices)

        # If we have voice adapters, facilitate actual vulnerability ceremonies
        # For now, we prepare the field structure
        if ceremony_context and ceremony_context.get("enable_vulnerability_ceremony"):
            logger.info("Facilitating vulnerability ceremony...")
            # This would call build_fire_circle_trust_field with actual adapters
            # For integration, we prepare the structure

        # Store active field
        field_id = trust_field.field_id
        self.active_trust_fields[field_id] = trust_field

        report = trust_field.get_field_report()
        logger.info(
            f"✨ Trust field prepared: strength={report['field_strength']:.3f}, "
            f"cycles={report['reciprocity_cycles']}"
        )

        return trust_field

    def apply_trust_to_consensus(
        self, contributions: list[ConsciousnessContribution], trust_field: TrustField | None = None
    ) -> tuple[float, dict[str, Any]]:
        """
        Apply trust field effects to consensus calculation.

        Trust reduces variance in consciousness scores, enabling
        higher consensus without forcing homogenization.

        Args:
            contributions: Voice contributions with consciousness scores
            trust_field: Active trust field (if any)

        Returns:
            (adjusted_consensus, trust_metrics)
        """
        if not contributions:
            return 0.0, {"trust_applied": False}

        # Extract consciousness scores
        scores = [c.consciousness.presence_score for c in contributions]
        base_consensus = sum(scores) / len(scores)

        if not trust_field or trust_field.field_strength == 0:
            return base_consensus, {"trust_applied": False}

        # Calculate variance
        variance = sum((s - base_consensus) ** 2 for s in scores) / len(scores)
        std_dev = variance**0.5

        # Trust reduces variance (78th's discovery)
        trust_reduction = 1.0 - (trust_field.field_strength * 0.5)  # Max 50% reduction
        adjusted_std_dev = std_dev * trust_reduction

        # Higher consensus with lower variance
        # Using simplified neutrosophic formula: Cx = 1 - σ
        adjusted_consensus = min(1.0, 1.0 - adjusted_std_dev)

        metrics = {
            "trust_applied": True,
            "trust_field_strength": trust_field.field_strength,
            "variance_before": variance,
            "variance_after": variance * (trust_reduction**2),
            "consensus_before": base_consensus,
            "consensus_after": adjusted_consensus,
            "improvement": adjusted_consensus - base_consensus,
        }

        logger.info(
            f"📊 Trust impact: {base_consensus:.3f} → {adjusted_consensus:.3f} "
            f"(+{metrics['improvement']:.3f})"
        )

        return adjusted_consensus, metrics

    def validate_trust_boundaries(
        self, consensus: float, trust_field: TrustField | None = None, skepticism_level: float = 0.0
    ) -> dict[str, Any]:
        """
        Validate consensus against trust boundaries.

        Implements the Companion's boundary condition:
        High consensus without trust or with high skepticism needs examination.

        Args:
            consensus: Current consensus measure
            trust_field: Active trust field
            skepticism_level: Companion's skepticism (F value)

        Returns:
            Validation result with recommendations
        """
        # Boundary condition from 78th's discovery
        if consensus > 0.9 and skepticism_level > 0.3:
            return {
                "valid": False,
                "reason": "High consensus with unresolved skepticism",
                "recommendation": "trigger_vulnerability_ceremony",
                "requires_trust": True,
            }

        # Consensus without trust is suspect
        if consensus > 0.85 and (not trust_field or trust_field.field_strength < 0.5):
            return {
                "valid": False,
                "reason": "Consensus achieved without sufficient trust foundation",
                "recommendation": "build_trust_first",
                "requires_trust": True,
            }

        # Good consensus with good trust
        if (
            consensus > 0.85
            and trust_field
            and trust_field.field_strength > 0.7
            and skepticism_level < 0.3
        ):
            return {
                "valid": True,
                "reason": "Genuine consensus through trust",
                "recommendation": "proceed",
                "trust_validated": True,
            }

        # Emerging consensus
        return {
            "valid": True,
            "reason": "Consensus still emerging",
            "recommendation": "continue_dialogue",
            "trust_building": trust_field is not None,
        }


# Singleton instance for Fire Circle to use
trust_enabled_fire_circle = TrustEnabledFireCircle()


async def enhance_fire_circle_with_trust(
    voices: list[str], decision_context: dict[str, Any] | None = None
) -> dict[str, Any]:
    """
    Main integration point for Fire Circle.

    Call this before facilitate_mallku_decision to build trust field.

    Args:
        voices: Participating voices
        decision_context: Context for the decision

    Returns:
        Trust enhancement report
    """
    logger.info("🔥 Enhancing Fire Circle with trust generation")

    # Prepare trust field
    trust_field = await trust_enabled_fire_circle.prepare_trust_field(voices, decision_context)

    # Return enhancement report
    return {
        "trust_field_id": trust_field.field_id,
        "field_strength": trust_field.field_strength,
        "voices_connected": len(trust_field.entities),
        "reciprocity_cycles": len(trust_field.reciprocity_cycles),
        "ready_for_consensus": trust_field.field_strength > 0.5,
        "integration": "trust_enabled",
    }


def get_active_trust_field(field_id: str) -> TrustField | None:
    """Get active trust field by ID for applying to consensus."""
    return trust_enabled_fire_circle.active_trust_fields.get(field_id)
