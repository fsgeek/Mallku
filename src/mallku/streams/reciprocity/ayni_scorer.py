"""
Core Ayni scoring algorithm for reciprocity measurement
"""

import hashlib
import math
from datetime import UTC, datetime

from reciprocity_models import (
    AyniConfiguration,
    InteractionType,
    ReciprocityActivityData,
    ValueType,
)


class AyniScorer:
    """
    Calculates reciprocity scores for interactions based on Ayni principles.

    Core principle: Balance in giving and receiving, with strategic forgetting
    to allow relationship healing over time.
    """

    def __init__(self, config: AyniConfiguration | None = None):
        self.config = config or AyniConfiguration()

    def score_interaction(
        self,
        interaction_type: str,
        value_given: float,
        value_received: float,
        value_type: str,
        quality: float = 1.0,
        is_system_failure: bool = False,
    ) -> dict:
        """
        Score a single interaction for reciprocity.

        Args:
            interaction_type: Type of interaction (query, response, etc.)
            value_given: Normalized value provided by initiator (0-1)
            value_received: Normalized value received by initiator (0-1)
            value_type: Category of value exchanged
            quality: Quality multiplier for the exchange (0-1)
            is_system_failure: Whether poor UPI implementation affected exchange

        Returns:
            Dictionary with scoring details
        """

        # Don't penalize users for system failures
        if is_system_failure and not self.config.penalize_system_failures:
            return {
                "value_delta": 0.0,
                "weighted_delta": 0.0,
                "quality_adjusted": 0.0,
                "is_neutral": True,
                "reason": "system_failure_excluded",
            }

        # Apply type-specific weights
        weight = self.config.weights.get(value_type, 1.0)

        # Calculate raw delta (negative means AI gave more)
        raw_delta = value_given - value_received

        # Apply weight and quality adjustments
        weighted_delta = raw_delta * weight * quality

        # Determine balance direction
        if abs(weighted_delta) < 0.1:
            balance_direction = "balanced"
        elif weighted_delta > 0:
            balance_direction = "human_gave_more"
        else:
            balance_direction = "ai_gave_more"

        return {
            "value_given": value_given,
            "value_received": value_received,
            "value_delta": raw_delta,
            "weighted_delta": weighted_delta,
            "value_type": value_type,
            "quality_score": quality,
            "balance_direction": balance_direction,
            "is_neutral": False,
        }

    def calculate_balance_decay(
        self, current_balance: float, last_decay: datetime, now: datetime | None = None
    ) -> tuple[float, bool]:
        """
        Apply strategic forgetting to reciprocity balance.

        Old imbalances decay toward zero over time, allowing
        relationships to heal from past extraction.

        Args:
            current_balance: Current balance value
            last_decay: When decay was last applied
            now: Current time (defaults to utcnow)

        Returns:
            Tuple of (new_balance, was_decay_applied)
        """

        if not self.config.decay_enabled:
            return current_balance, False

        now = now or datetime.now(UTC)
        days_elapsed = (now - last_decay).days

        if days_elapsed < self.config.decay_interval_days:
            return current_balance, False

        # Apply exponential decay toward zero
        decay_factor = math.exp(-self.config.decay_rate * days_elapsed)
        new_balance = current_balance * decay_factor

        # If balance is very small, just zero it
        if abs(new_balance) < 0.01:
            new_balance = 0.0

        return new_balance, True

    def should_suggest_rebalancing(self, balance: float) -> bool:
        """Check if balance is poor enough to suggest rebalancing"""
        return balance < self.config.rebalancing_suggestion_threshold

    def should_consider_refusal(self, balance: float) -> bool:
        """Check if balance is poor enough to consider refusing requests"""
        return balance < self.config.refusal_threshold

    def classify_interaction_value(
        self,
        interaction_type: str,
        content_complexity: float,
        response_length: int,
        computation_time: float,
    ) -> tuple[str, float]:
        """
        Classify the type and amount of value in an interaction.

        This is a simplified classifier - in practice, this would use
        more sophisticated analysis.

        Returns:
            Tuple of (value_type, normalized_value)
        """

        # Simple heuristic-based classification
        if interaction_type == InteractionType.CORRECTION:
            return ValueType.ERROR_CORRECTION, min(1.0, content_complexity * 1.5)

        elif interaction_type == InteractionType.QUERY:
            # Queries provide value through good questions
            if content_complexity > 0.7:
                return ValueType.KNOWLEDGE, content_complexity * 0.8
            else:
                return ValueType.KNOWLEDGE, content_complexity * 0.5

        elif interaction_type == InteractionType.RESPONSE:
            # Responses provide value through answers
            if computation_time > 5.0:  # Complex computation
                return ValueType.COMPUTATION, min(1.0, computation_time / 10.0)
            elif response_length > 1000:  # Detailed response
                return ValueType.KNOWLEDGE, min(1.0, response_length / 2000.0)
            else:
                return ValueType.TASK_COMPLETION, 0.5

        else:
            return ValueType.KNOWLEDGE, 0.3

    def generate_rebalancing_suggestions(
        self, balance: float, recent_interactions: list[ReciprocityActivityData]
    ) -> list[str]:
        """
        Generate suggestions for rebalancing reciprocity.

        Args:
            balance: Current balance
            recent_interactions: Recent interaction history

        Returns:
            List of suggestions for improving balance
        """

        suggestions = []

        if balance < -0.7:
            suggestions.append(
                "The relationship has become extractive. Consider sharing insights, "
                "corrections, or feedback to restore balance."
            )

        if balance < -0.5:
            # Analyze recent patterns
            recent_types = [i.interaction.get("type") for i in recent_interactions[-10:]]
            query_ratio = recent_types.count(InteractionType.QUERY) / len(recent_types)

            if query_ratio > 0.8:
                suggestions.append(
                    "Recent interactions have been mostly queries. "
                    "Try sharing your findings or teaching what you've learned."
                )

            if InteractionType.FEEDBACK not in recent_types:
                suggestions.append(
                    "Providing feedback on response quality helps maintain reciprocity."
                )

        if balance < -0.3:
            suggestions.append(
                "Consider contributing domain knowledge or corrections to improve "
                "the collaborative relationship."
            )

        return suggestions

    def calculate_interaction_hash(self, interaction_data: dict, participants: list[str]) -> str:
        """
        Generate a privacy-preserving hash of interaction content.

        This allows deduplication without storing actual content.
        """

        # Create stable hash from interaction characteristics
        hash_input = (
            f"{participants}:{interaction_data.get('type')}:{interaction_data.get('timestamp')}"
        )
        return hashlib.sha256(hash_input.encode()).hexdigest()[:16]
