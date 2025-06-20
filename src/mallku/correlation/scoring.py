"""
Confidence scoring system for temporal correlations.

This module implements the multi-factor confidence assessment that transforms
raw pattern detection into wisdom about which correlations are truly meaningful.
The scoring system weighs temporal consistency, frequency strength, context coherence,
causal plausibility, and user validation to produce nuanced confidence estimates.
"""

import math
import statistics
from datetime import UTC, datetime, timedelta
from typing import Any

from .models import CorrelationFeedback, Event, TemporalCorrelation


class ConfidenceScorer:
    """
    Multi-factor confidence assessment for temporal correlations.

    This scorer implements the architect's vision of sophisticated confidence
    evaluation that goes beyond simple correlation counting to understand
    the deeper meaning and reliability of detected patterns.
    """

    def __init__(self):
        """Initialize with default factor weights from architectural design."""
        self.factor_weights = {
            "temporal_consistency": 0.3,
            "frequency_strength": 0.25,
            "context_coherence": 0.2,
            "causal_plausibility": 0.15,
            "user_validation": 0.1,
        }

        # Learning parameters for adaptive scoring
        self.learning_rate = 0.1
        self.feedback_history: list[CorrelationFeedback] = []

    def calculate_correlation_confidence(self, correlation: TemporalCorrelation) -> float:
        """
        Calculate comprehensive confidence score for a temporal correlation.

        This is the heart of the confidence assessment system - it weighs
        multiple factors to determine how confident we should be that a
        detected correlation represents meaningful relationship.

        Args:
            correlation: The temporal correlation to assess

        Returns:
            Confidence score between 0.0 and 1.0
        """
        factors = {
            "temporal_consistency": self.assess_timing_stability(correlation),
            "frequency_strength": self.normalize_occurrence_count(correlation.occurrence_frequency),
            "context_coherence": self.analyze_environmental_similarity(correlation),
            "causal_plausibility": self.estimate_causal_likelihood(correlation),
            "user_validation": self.incorporate_feedback_history(correlation),
        }

        # Calculate weighted combination
        confidence = sum(
            factor_value * self.factor_weights[factor_name]
            for factor_name, factor_value in factors.items()
        )

        # Store individual factor scores for transparency
        correlation.confidence_factors.update(factors)

        return max(0.0, min(1.0, confidence))  # Clamp to [0,1]

    def assess_timing_stability(self, correlation: TemporalCorrelation) -> float:
        """
        Assess how consistent the timing is across correlation instances.

        Temporal consistency is about reliability - do events consistently
        occur at similar intervals, or is the timing chaotic? Higher
        consistency suggests stronger underlying causal relationship.

        Args:
            correlation: Correlation to assess

        Returns:
            Stability score between 0.0 and 1.0
        """
        # If we only have gap variance from the pattern detector
        if hasattr(correlation, "gap_variance") and correlation.gap_variance is not None:
            avg_gap_seconds = correlation.temporal_gap.total_seconds()

            if avg_gap_seconds <= 0:
                return 0.0

            # Calculate coefficient of variation
            std_dev = math.sqrt(correlation.gap_variance)
            cv = std_dev / avg_gap_seconds

            # Convert to stability score (inverse relationship)
            stability = 1.0 / (1.0 + cv)
            return stability

        # Fallback: use pattern stability if available
        if hasattr(correlation, "pattern_stability"):
            return correlation.pattern_stability

        # Default for patterns without timing variance data
        return 0.5

    def normalize_occurrence_count(self, frequency: int) -> float:
        """
        Convert raw occurrence frequency to normalized strength score.

        Frequency matters, but with diminishing returns - the difference
        between 1 and 5 occurrences is more significant than between
        50 and 54 occurrences.

        Args:
            frequency: Number of times pattern has occurred

        Returns:
            Normalized frequency strength between 0.0 and 1.0
        """
        if frequency <= 0:
            return 0.0

        # Logarithmic scaling with diminishing returns
        # 3 occurrences = ~0.5, 10 occurrences = ~0.7, 30+ occurrences = ~0.9+
        max_score = 1.0
        scaling_factor = 10.0

        score = max_score * (1.0 - math.exp(-frequency / scaling_factor))
        return min(score, max_score)

    def analyze_environmental_similarity(self, correlation: TemporalCorrelation) -> float:
        """
        Analyze context coherence across correlated events.

        Context coherence asks: do these events happen in similar
        circumstances? Similar locations, times of day, applications,
        or other environmental factors strengthen correlation confidence.

        Args:
            correlation: Correlation to analyze

        Returns:
            Context coherence score between 0.0 and 1.0
        """
        all_events = [correlation.primary_event] + correlation.correlated_events

        if len(all_events) < 2:
            return 0.5  # Neutral score for insufficient data

        # Extract contexts that exist
        contexts = [event.context for event in all_events if event.context]

        if not contexts:
            return 0.3  # Lower score for events without context

        # Calculate context similarity metrics
        similarity_scores = []

        # 1. Shared context keys
        key_similarity = self._calculate_key_similarity(contexts)
        similarity_scores.append(key_similarity)

        # 2. Shared context values for common keys
        value_similarity = self._calculate_value_similarity(contexts)
        similarity_scores.append(value_similarity)

        # 3. Temporal context patterns (time of day, day of week)
        temporal_similarity = self._calculate_temporal_context_similarity(all_events)
        similarity_scores.append(temporal_similarity)

        # 4. Event type consistency
        type_similarity = self._calculate_event_type_similarity(all_events)
        similarity_scores.append(type_similarity)

        # Overall coherence is average of similarity metrics
        return statistics.mean(similarity_scores)

    def _calculate_key_similarity(self, contexts: list[dict[str, Any]]) -> float:
        """Calculate similarity based on shared context keys."""
        if not contexts:
            return 0.0

        # Find intersection and union of context keys
        all_keys = [set(context.keys()) for context in contexts]
        intersection = set.intersection(*all_keys) if all_keys else set()
        union = set.union(*all_keys) if all_keys else set()

        if not union:
            return 0.5  # Neutral score for no context keys

        # Jaccard similarity
        return len(intersection) / len(union)

    def _calculate_value_similarity(self, contexts: list[dict[str, Any]]) -> float:
        """Calculate similarity based on shared context values."""
        if len(contexts) < 2:
            return 1.0

        # Find common keys across all contexts
        common_keys = set(contexts[0].keys())
        for context in contexts[1:]:
            common_keys &= set(context.keys())

        if not common_keys:
            return 0.5  # No common keys to compare

        # Calculate value agreement for common keys
        agreements = []
        for key in common_keys:
            values = [context[key] for context in contexts]
            unique_values = set(str(v) for v in values)  # Convert to string for comparison

            # Agreement is inverse of value diversity
            agreement = 1.0 / len(unique_values) if unique_values else 0.0
            agreements.append(agreement)

        return statistics.mean(agreements) if agreements else 0.5

    def _calculate_temporal_context_similarity(self, events: list[Event]) -> float:
        """Calculate similarity in temporal context (time patterns)."""
        if len(events) < 2:
            return 1.0

        similarities = []

        # Time of day similarity
        hours = [event.timestamp.hour for event in events]
        hour_variance = statistics.variance(hours) if len(hours) > 1 else 0
        hour_similarity = 1.0 / (1.0 + hour_variance / 12.0)  # Normalize by 12-hour span
        similarities.append(hour_similarity)

        # Day of week similarity
        weekdays = [event.timestamp.weekday() for event in events]
        weekday_variance = statistics.variance(weekdays) if len(weekdays) > 1 else 0
        weekday_similarity = 1.0 / (1.0 + weekday_variance / 3.5)  # Normalize by ~half-week
        similarities.append(weekday_similarity)

        return statistics.mean(similarities)

    def _calculate_event_type_similarity(self, events: list[Event]) -> float:
        """Calculate similarity in event types and streams."""
        if len(events) < 2:
            return 1.0

        # Event type consistency
        types = [event.event_type for event in events]
        unique_types = set(types)
        type_consistency = 1.0 / len(unique_types)

        # Stream consistency
        streams = [event.stream_id for event in events]
        unique_streams = set(streams)
        stream_consistency = 1.0 / len(unique_streams)

        return (type_consistency + stream_consistency) / 2.0

    def estimate_causal_likelihood(self, correlation: TemporalCorrelation) -> float:
        """
        Estimate the plausibility of causal relationship.

        Causal plausibility goes beyond correlation to ask: could there
        be a reasonable causal mechanism? This is where domain knowledge
        and heuristics help distinguish meaningful patterns from noise.

        Args:
            correlation: Correlation to assess

        Returns:
            Causal plausibility score between 0.0 and 1.0
        """
        plausibility_factors = []

        # 1. Temporal ordering consistency (for sequential patterns)
        if correlation.pattern_type == "sequential":
            ordering_score = self._assess_temporal_ordering(correlation)
            plausibility_factors.append(ordering_score)

        # 2. Reasonable time gap
        gap_score = self._assess_reasonable_gap(correlation.temporal_gap)
        plausibility_factors.append(gap_score)

        # 3. Event type compatibility
        compatibility_score = self._assess_event_compatibility(correlation)
        plausibility_factors.append(compatibility_score)

        # 4. Context logical consistency
        logic_score = self._assess_logical_consistency(correlation)
        plausibility_factors.append(logic_score)

        return statistics.mean(plausibility_factors) if plausibility_factors else 0.5

    def _assess_temporal_ordering(self, correlation: TemporalCorrelation) -> float:
        """Assess whether temporal ordering makes causal sense."""
        # For sequential patterns, consistent ordering is important
        if correlation.pattern_type != "sequential":
            return 1.0  # Not applicable for non-sequential patterns

        # Check if primary event consistently precedes correlated events
        # This would require access to the original event sequences
        # For now, return neutral score
        return 0.7  # Assume reasonable ordering for detected sequential patterns

    def _assess_reasonable_gap(self, gap: timedelta) -> float:
        """Assess whether time gap is reasonable for causal relationship."""
        gap_seconds = gap.total_seconds()

        # Very short gaps (< 1 minute) might be too immediate
        if gap_seconds < 60:
            return 0.6

        # Reasonable gaps (1 minute to 4 hours) are plausible
        elif gap_seconds < 14400:  # 4 hours
            return 1.0

        # Long gaps (4 hours to 1 day) are possible but less likely
        elif gap_seconds < 86400:  # 1 day
            return 0.7

        # Very long gaps (> 1 day) are less plausible for most patterns
        else:
            return 0.4

    def _assess_event_compatibility(self, correlation: TemporalCorrelation) -> float:
        """Assess whether event types are compatible for causal relationship."""
        all_events = [correlation.primary_event] + correlation.correlated_events

        # Look for logical event type combinations
        types = [event.event_type.value for event in all_events]

        # Heuristic compatibility matrix
        compatibility_matrix = {
            ("communication", "storage"): 0.9,  # Email -> document creation
            ("activity", "storage"): 0.8,  # User activity -> file operation
            ("environmental", "activity"): 0.7,  # Location change -> activity change
            ("communication", "activity"): 0.8,  # Message -> response activity
        }

        # Calculate compatibility for event type pairs
        compatibilities = []
        for i in range(len(types)):
            for j in range(i + 1, len(types)):
                type_pair = tuple(sorted([types[i], types[j]]))
                compatibility = compatibility_matrix.get(type_pair, 0.5)  # Default neutral
                compatibilities.append(compatibility)

        return statistics.mean(compatibilities) if compatibilities else 0.5

    def _assess_logical_consistency(self, correlation: TemporalCorrelation) -> float:
        """Assess logical consistency of context and content."""
        # This is a placeholder for more sophisticated logical reasoning
        # In the future, this could incorporate:
        # - Domain-specific knowledge about event relationships
        # - Natural language processing of event content
        # - Machine learning models trained on causal relationships

        # For now, return a moderate score based on pattern stability
        return min(0.8, 0.4 + correlation.pattern_stability)

    def incorporate_feedback_history(self, correlation: TemporalCorrelation) -> float:
        """
        Incorporate user validation feedback into confidence assessment.

        User feedback is the gold standard - when humans confirm or reject
        correlations, this provides ground truth about meaningfulness that
        we can use to calibrate our confidence estimates.

        Args:
            correlation: Correlation to assess

        Returns:
            User validation score between 0.0 and 1.0
        """
        if not self.feedback_history:
            return 0.5  # Neutral score when no feedback available

        # Look for feedback on similar correlations
        similar_feedback = self._find_similar_feedback(correlation)

        if not similar_feedback:
            return 0.5  # No similar feedback available

        # Calculate weighted average of feedback
        total_weight = 0.0
        weighted_score = 0.0

        for feedback in similar_feedback:
            # Weight recent feedback more heavily
            age_days = (datetime.now(UTC) - feedback.feedback_timestamp).days
            weight = math.exp(-age_days / 30.0)  # Exponential decay over 30 days

            # Convert feedback to score
            if feedback.is_meaningful:
                score = feedback.confidence_rating
            else:
                score = 1.0 - feedback.confidence_rating

            weighted_score += weight * score
            total_weight += weight

        if total_weight > 0:
            return weighted_score / total_weight
        else:
            return 0.5

    def _find_similar_feedback(self, correlation: TemporalCorrelation) -> list[CorrelationFeedback]:
        """Find feedback on correlations similar to the given one."""
        similar = []

        for feedback in self.feedback_history:
            # This is a simplified similarity check
            # In practice, would need more sophisticated matching
            # based on pattern type, event types, context similarity, etc.
            similar.append(feedback)

        return similar[:10]  # Limit to recent feedback

    def update_weights_from_feedback(self, feedback_batch: list[CorrelationFeedback]):
        """
        Update factor weights based on user feedback.

        This implements adaptive learning where the confidence scorer
        adjusts its weighting of different factors based on which
        combinations tend to predict user satisfaction.

        Args:
            feedback_batch: Recent user feedback to learn from
        """
        if len(feedback_batch) < 10:
            return  # Need sufficient feedback for learning

        # Store feedback for future use
        self.feedback_history.extend(feedback_batch)

        # Simple learning algorithm: adjust weights based on correlation
        # between factor scores and user satisfaction

        # This is a placeholder for more sophisticated learning
        # In practice, would use regression or gradient descent
        # to optimize factor weights based on prediction accuracy

        print(f"Learning from {len(feedback_batch)} feedback instances...")
        # TODO: Implement actual weight optimization

    def get_confidence_explanation(self, correlation: TemporalCorrelation) -> dict[str, Any]:
        """
        Generate human-readable explanation of confidence assessment.

        Provides transparency into why the system assigned a particular
        confidence score, helping users understand and trust the correlation
        detection process.

        Args:
            correlation: Correlation to explain

        Returns:
            Dictionary with explanation details
        """
        factors = correlation.confidence_factors

        explanation = {
            "overall_confidence": correlation.confidence_score,
            "factor_breakdown": {
                "temporal_consistency": {
                    "score": factors.get("temporal_consistency", 0.0),
                    "weight": self.factor_weights["temporal_consistency"],
                    "interpretation": self._interpret_temporal_consistency(
                        factors.get("temporal_consistency", 0.0)
                    ),
                },
                "frequency_strength": {
                    "score": factors.get("frequency_strength", 0.0),
                    "weight": self.factor_weights["frequency_strength"],
                    "interpretation": self._interpret_frequency_strength(
                        correlation.occurrence_frequency
                    ),
                },
                "context_coherence": {
                    "score": factors.get("context_coherence", 0.0),
                    "weight": self.factor_weights["context_coherence"],
                    "interpretation": self._interpret_context_coherence(
                        factors.get("context_coherence", 0.0)
                    ),
                },
                "causal_plausibility": {
                    "score": factors.get("causal_plausibility", 0.0),
                    "weight": self.factor_weights["causal_plausibility"],
                    "interpretation": self._interpret_causal_plausibility(
                        factors.get("causal_plausibility", 0.0)
                    ),
                },
                "user_validation": {
                    "score": factors.get("user_validation", 0.0),
                    "weight": self.factor_weights["user_validation"],
                    "interpretation": self._interpret_user_validation(
                        factors.get("user_validation", 0.0)
                    ),
                },
            },
            "pattern_details": {
                "type": correlation.pattern_type,
                "frequency": correlation.occurrence_frequency,
                "temporal_gap": str(correlation.temporal_gap),
                "stability": correlation.pattern_stability,
            },
        }

        return explanation

    def _interpret_temporal_consistency(self, score: float) -> str:
        """Provide human-readable interpretation of temporal consistency score."""
        if score >= 0.8:
            return "Very consistent timing - events occur at predictable intervals"
        elif score >= 0.6:
            return "Moderately consistent timing - some variation in intervals"
        elif score >= 0.4:
            return "Somewhat inconsistent timing - noticeable variation"
        else:
            return "Inconsistent timing - high variation in intervals"

    def _interpret_frequency_strength(self, frequency: int) -> str:
        """Provide human-readable interpretation of frequency strength."""
        if frequency >= 20:
            return f"Very frequent pattern - observed {frequency} times"
        elif frequency >= 10:
            return f"Frequent pattern - observed {frequency} times"
        elif frequency >= 5:
            return f"Moderate frequency - observed {frequency} times"
        else:
            return f"Low frequency - observed {frequency} times"

    def _interpret_context_coherence(self, score: float) -> str:
        """Provide human-readable interpretation of context coherence score."""
        if score >= 0.8:
            return "Very similar context across occurrences"
        elif score >= 0.6:
            return "Moderately similar context"
        elif score >= 0.4:
            return "Somewhat similar context"
        else:
            return "Varied context across occurrences"

    def _interpret_causal_plausibility(self, score: float) -> str:
        """Provide human-readable interpretation of causal plausibility score."""
        if score >= 0.8:
            return "Highly plausible causal relationship"
        elif score >= 0.6:
            return "Plausible causal relationship"
        elif score >= 0.4:
            return "Possible causal relationship"
        else:
            return "Unclear causal relationship"

    def _interpret_user_validation(self, score: float) -> str:
        """Provide human-readable interpretation of user validation score."""
        if score >= 0.8:
            return "Strong positive feedback from users"
        elif score >= 0.6:
            return "Moderate positive feedback"
        elif score >= 0.4:
            return "Mixed user feedback"
        elif score > 0.1:
            return "Some negative feedback"
        else:
            return "No user feedback available"
