#!/usr/bin/env python3
"""
Shared Protocol Types - Common enums and types for cross-module communication

This module contains shared types that are used across multiple modules
to avoid circular dependencies while maintaining type safety.

The Sacred Types: Where modules meet without entanglement.
"""

from enum import Enum


class MessageType(str, Enum):
    """Types of messages that can flow through governance dialogues."""

    # Core dialogue messages
    PROPOSAL = "proposal"  # Initiating a topic for collective consideration
    RESPONSE = "response"  # Responding to proposals or other messages
    REFLECTION = "reflection"  # Metacognitive observations about the dialogue

    # Consensus-building messages
    SUPPORT = "support"  # Expressing alignment with a perspective
    CONCERN = "concern"  # Raising questions or reservations
    DISSENT = "dissent"  # Disagreeing while preserving the perspective

    # Process messages
    SUMMARY = "summary"  # Synthesizing dialogue threads
    BRIDGE = "bridge"  # Connecting different perspectives
    EMERGENCE = "emergence"  # Noting new insights arising from dialogue

    # Sacred messages
    EMPTY_CHAIR = "empty_chair"  # Speaking for unrepresented perspectives
    WISDOM_SEED = "wisdom_seed"  # Sharing insight from individual practice

    # Fire Circle adapter compatibility
    MESSAGE = "message"  # General communication (maps to RESPONSE)
    QUESTION = "question"  # Proposing inquiry (maps to PROPOSAL)
    DISAGREEMENT = "disagreement"  # Constructive dissent (maps to DISSENT)
