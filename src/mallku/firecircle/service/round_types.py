"""
Fire Circle Round Types
=======================

Different types of dialogue rounds for various purposes.
"""

from enum import Enum


class RoundType(str, Enum):
    """Types of dialogue rounds in Fire Circle."""

    # Core round types
    OPENING = "opening"  # Initial exploration of topic
    REFLECTION = "reflection"  # Reflecting on others' perspectives
    SYNTHESIS = "synthesis"  # Bringing insights together
    CLARIFICATION = "clarification"  # Resolving divergence

    # Specialized rounds
    EXPLORATION = "exploration"  # Deep dive into specific aspects
    CRITIQUE = "critique"  # Critical analysis round
    VISION = "vision"  # Future-oriented round
    GROUNDING = "grounding"  # Practical implementation round

    # Decision-focused rounds
    PROPOSAL = "proposal"  # Proposing solutions
    EVALUATION = "evaluation"  # Evaluating proposals
    CONSENSUS = "consensus"  # Building consensus
    DECISION = "decision"  # Final decision round
