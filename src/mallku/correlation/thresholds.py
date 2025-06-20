"""
Adaptive threshold management for correlation detection.

This module implements self-adjusting correlation detection parameters that
learn from user feedback and performance metrics. The adaptive thresholds
embody the system's developing wisdom about when to trust correlations
and when to remain skeptical.
"""

import json
import statistics
from datetime import UTC, datetime, timedelta
from pathlib import Path

from .models import CorrelationFeedback, TemporalPrecision


class AdaptiveThresholds:
    """
    Self-adjusting correlation detection parameters.

    This class implements the learning mechanism that allows the correlation
    engine to improve its judgment over time, adjusting sensitivity based
    on precision/recall trade-offs and user satisfaction.
    """

    def __init__(self, config_file: str | None = None):
        """
        Initialize adaptive thresholds with defaults from architectural design.

        Args:
            config_file: Optional path to saved threshold configuration
        """
        # Core detection thresholds
        self.confidence_threshold = 0.6
        self.frequency_threshold = 3

        # Temporal windows for different precision levels
        self.temporal_windows = {
            TemporalPrecision.INSTANT: timedelta(seconds=10),
            TemporalPrecision.MINUTE: timedelta(minutes=5),
            TemporalPrecision.SESSION: timedelta(minutes=30),
            TemporalPrecision.DAILY: timedelta(hours=4),
            TemporalPrecision.CYCLICAL: timedelta(days=1),
        }

        # Learning parameters
        self.learning_rate = 0.1
        self.target_precision = 0.8  # Minimize false positives
        self.target_recall = 0.7  # Don't miss too many valid correlations

        # Performance tracking
        self.performance_history: list[dict] = []
        self.feedback_history: list[CorrelationFeedback] = []

        # Threshold bounds (prevent extreme adjustments)
        self.min_confidence_threshold = 0.2
        self.max_confidence_threshold = 0.9
        self.min_frequency_threshold = 2
        self.max_frequency_threshold = 10

        # Configuration persistence
        self.config_file = config_file or "correlation_thresholds.json"

        # Load saved configuration if available
        self._load_configuration()

    def update_from_feedback(self, feedback_batch: list[CorrelationFeedback]) -> dict[str, float]:
        """
        Adjust thresholds based on user feedback and performance metrics.

        This is the core learning mechanism - analyzing feedback patterns
        to optimize the precision/recall balance and user satisfaction.

        Args:
            feedback_batch: Recent user feedback to learn from

        Returns:
            Dictionary with performance metrics and threshold changes
        """
        if len(feedback_batch) < 5:
            return {"message": "Insufficient feedback for learning"}

        # Store feedback for analysis
        self.feedback_history.extend(feedback_batch)

        # Calculate current performance metrics
        metrics = self.calculate_performance_metrics(feedback_batch)

        # Record performance for trend analysis
        self.performance_history.append(
            {
                "timestamp": datetime.now(UTC),
                "precision": metrics["precision"],
                "recall": metrics["recall"],
                "f1_score": metrics["f1_score"],
                "user_satisfaction": metrics["user_satisfaction"],
                "confidence_threshold": self.confidence_threshold,
                "frequency_threshold": self.frequency_threshold,
            }
        )

        # Adjust thresholds based on performance
        threshold_changes = self._adjust_thresholds(metrics)

        # Optimize temporal windows based on successful correlations
        window_changes = self._optimize_temporal_windows(feedback_batch)

        # Save updated configuration
        self._save_configuration()

        return {
            "metrics": metrics,
            "threshold_changes": threshold_changes,
            "window_changes": window_changes,
            "feedback_count": len(feedback_batch),
        }

    def calculate_performance_metrics(
        self, feedback_batch: list[CorrelationFeedback]
    ) -> dict[str, float]:
        """
        Calculate precision, recall, and satisfaction metrics from feedback.

        Args:
            feedback_batch: User feedback to analyze

        Returns:
            Dictionary with performance metrics
        """
        if not feedback_batch:
            return {"precision": 0.0, "recall": 0.0, "f1_score": 0.0, "user_satisfaction": 0.0}

        # Classify feedback as positive (meaningful) or negative
        positive_feedback = [f for f in feedback_batch if f.is_meaningful]
        negative_feedback = [f for f in feedback_batch if not f.is_meaningful]

        # Calculate precision (what fraction of detected correlations are meaningful?)
        total_detections = len(feedback_batch)
        true_positives = len(positive_feedback)
        precision = true_positives / total_detections if total_detections > 0 else 0.0

        # Recall is harder to calculate without knowing missed correlations
        # Use user satisfaction as a proxy for recall
        satisfaction_scores = [f.confidence_rating for f in positive_feedback]
        user_satisfaction = statistics.mean(satisfaction_scores) if satisfaction_scores else 0.0

        # Use satisfaction as proxy for recall (satisfied users suggest we're not missing patterns)
        recall = user_satisfaction

        # F1 score combines precision and recall
        if precision + recall > 0:
            f1_score = 2 * (precision * recall) / (precision + recall)
        else:
            f1_score = 0.0

        return {
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score,
            "user_satisfaction": user_satisfaction,
            "positive_count": len(positive_feedback),
            "negative_count": len(negative_feedback),
        }

    def _adjust_thresholds(self, metrics: dict[str, float]) -> dict[str, float]:
        """
        Adjust confidence and frequency thresholds based on performance metrics.

        Args:
            metrics: Current performance metrics

        Returns:
            Dictionary describing threshold changes
        """
        changes = {}

        # Adjust confidence threshold based on precision/recall balance
        precision = metrics["precision"]
        recall = metrics["recall"]

        old_confidence = self.confidence_threshold

        # If precision is too low (too many false positives), increase threshold
        if precision < self.target_precision:
            adjustment = self.learning_rate * (self.target_precision - precision)
            self.confidence_threshold += adjustment
            changes["confidence_increase"] = adjustment

        # If recall is too low (missing valid correlations), decrease threshold
        elif recall < self.target_recall:
            adjustment = self.learning_rate * (self.target_recall - recall)
            self.confidence_threshold -= adjustment
            changes["confidence_decrease"] = adjustment

        # Clamp to bounds
        self.confidence_threshold = max(
            self.min_confidence_threshold,
            min(self.max_confidence_threshold, self.confidence_threshold),
        )

        if old_confidence != self.confidence_threshold:
            changes["new_confidence_threshold"] = self.confidence_threshold

        # Adjust frequency threshold based on false positive patterns
        old_frequency = self.frequency_threshold

        # If we're getting too many low-frequency false positives, increase threshold
        negative_feedback = [f for f in self.feedback_history[-50:] if not f.is_meaningful]
        if len(negative_feedback) > 5:
            # This is a simplified heuristic - in practice would analyze
            # frequency patterns in false positives
            if precision < 0.6:
                self.frequency_threshold = min(
                    self.max_frequency_threshold, self.frequency_threshold + 1
                )
                changes["frequency_increased"] = True

        # If precision is very high, we might be too conservative on frequency
        elif precision > 0.9 and recall < 0.6:
            self.frequency_threshold = max(
                self.min_frequency_threshold, self.frequency_threshold - 1
            )
            changes["frequency_decreased"] = True

        if old_frequency != self.frequency_threshold:
            changes["new_frequency_threshold"] = self.frequency_threshold

        return changes

    def _optimize_temporal_windows(
        self, feedback_batch: list[CorrelationFeedback]
    ) -> dict[str, str]:
        """
        Optimize temporal windows based on successful correlation patterns.

        Args:
            feedback_batch: Recent feedback to analyze

        Returns:
            Dictionary describing window optimizations
        """
        changes = {}

        # Analyze timing patterns in successful correlations
        positive_feedback = [f for f in feedback_batch if f.is_meaningful]

        if len(positive_feedback) < 3:
            return changes

        # This is a placeholder for temporal window optimization
        # In practice, would analyze the temporal gaps in successful
        # correlations and adjust windows to better capture those patterns

        # For now, implement conservative adjustment
        satisfaction_rate = len(positive_feedback) / len(feedback_batch)

        if satisfaction_rate > 0.8:
            # High satisfaction - windows might be too narrow, try expanding slightly
            for precision in self.temporal_windows:
                old_window = self.temporal_windows[precision]
                new_window = old_window * 1.1  # 10% increase
                self.temporal_windows[precision] = new_window
            changes["window_expansion"] = "Expanded windows by 10% due to high satisfaction"

        elif satisfaction_rate < 0.5:
            # Low satisfaction - windows might be too wide, try contracting
            for precision in self.temporal_windows:
                old_window = self.temporal_windows[precision]
                new_window = old_window * 0.9  # 10% decrease
                self.temporal_windows[precision] = new_window
            changes["window_contraction"] = "Contracted windows by 10% due to low satisfaction"

        return changes

    def get_threshold_for_precision(self, precision: TemporalPrecision) -> timedelta:
        """
        Get the current temporal window threshold for a given precision level.

        Args:
            precision: Temporal precision level

        Returns:
            Current temporal window for that precision
        """
        return self.temporal_windows.get(precision, timedelta(minutes=5))

    def should_accept_correlation(
        self, confidence: float, frequency: int, pattern_type: str
    ) -> bool:
        """
        Determine whether a correlation should be accepted based on current thresholds.

        Args:
            confidence: Correlation confidence score
            frequency: Number of pattern occurrences
            pattern_type: Type of correlation pattern

        Returns:
            True if correlation meets acceptance criteria
        """
        # Basic threshold checks
        if confidence < self.confidence_threshold:
            return False

        if frequency < self.frequency_threshold:
            return False

        # Pattern-specific adjustments
        adjusted_threshold = self._get_pattern_specific_threshold(pattern_type)

        return confidence >= adjusted_threshold

    def _get_pattern_specific_threshold(self, pattern_type: str) -> float:
        """
        Get confidence threshold adjusted for specific pattern types.

        Different pattern types might warrant different confidence requirements
        based on their typical reliability and user value.

        Args:
            pattern_type: Type of correlation pattern

        Returns:
            Adjusted confidence threshold
        """
        # Pattern-specific multipliers based on typical reliability
        pattern_multipliers = {
            "sequential": 1.0,  # Standard threshold
            "concurrent": 1.1,  # Slightly higher (concurrent can be noisy)
            "cyclical": 0.9,  # Slightly lower (cyclical patterns are valuable)
            "contextual": 1.05,  # Slightly higher (context can be subjective)
        }

        multiplier = pattern_multipliers.get(pattern_type, 1.0)
        return self.confidence_threshold * multiplier

    def get_performance_summary(self) -> dict[str, any]:
        """
        Get summary of recent performance and threshold evolution.

        Returns:
            Dictionary with performance trends and current settings
        """
        if not self.performance_history:
            return {
                "status": "No performance history available",
                "current_thresholds": {
                    "confidence": self.confidence_threshold,
                    "frequency": self.frequency_threshold,
                },
            }

        recent_performance = self.performance_history[-10:]  # Last 10 measurements

        # Calculate trends
        precisions = [p["precision"] for p in recent_performance]
        recalls = [p["recall"] for p in recent_performance]
        satisfactions = [p["user_satisfaction"] for p in recent_performance]

        return {
            "performance_trends": {
                "average_precision": statistics.mean(precisions),
                "average_recall": statistics.mean(recalls),
                "average_satisfaction": statistics.mean(satisfactions),
                "precision_trend": self._calculate_trend(precisions),
                "recall_trend": self._calculate_trend(recalls),
                "satisfaction_trend": self._calculate_trend(satisfactions),
            },
            "current_thresholds": {
                "confidence": self.confidence_threshold,
                "frequency": self.frequency_threshold,
                "temporal_windows": {str(k): str(v) for k, v in self.temporal_windows.items()},
            },
            "learning_stats": {
                "total_feedback": len(self.feedback_history),
                "performance_measurements": len(self.performance_history),
                "learning_rate": self.learning_rate,
            },
        }

    def _calculate_trend(self, values: list[float]) -> str:
        """Calculate trend direction for a series of values."""
        if len(values) < 2:
            return "insufficient_data"

        # Simple linear trend
        x = list(range(len(values)))
        slope = sum(
            (x[i] - statistics.mean(x)) * (values[i] - statistics.mean(values))
            for i in range(len(values))
        ) / sum((x[i] - statistics.mean(x)) ** 2 for i in range(len(values)))

        if slope > 0.01:
            return "improving"
        elif slope < -0.01:
            return "declining"
        else:
            return "stable"

    def _save_configuration(self):
        """Save current threshold configuration to file."""
        try:
            config = {
                "confidence_threshold": self.confidence_threshold,
                "frequency_threshold": self.frequency_threshold,
                "temporal_windows": {
                    str(k): v.total_seconds() for k, v in self.temporal_windows.items()
                },
                "learning_rate": self.learning_rate,
                "target_precision": self.target_precision,
                "target_recall": self.target_recall,
                "last_updated": datetime.now(UTC).isoformat(),
            }

            config_path = Path(self.config_file)
            config_path.parent.mkdir(parents=True, exist_ok=True)

            with open(config_path, "w") as f:
                json.dump(config, f, indent=2)

        except Exception as e:
            print(f"Warning: Could not save threshold configuration: {e}")

    def _load_configuration(self):
        """Load threshold configuration from file if it exists."""
        try:
            config_path = Path(self.config_file)

            if not config_path.exists():
                return  # Use defaults

            with open(config_path) as f:
                config = json.load(f)

            # Load thresholds
            self.confidence_threshold = config.get(
                "confidence_threshold", self.confidence_threshold
            )
            self.frequency_threshold = config.get("frequency_threshold", self.frequency_threshold)

            # Load temporal windows
            if "temporal_windows" in config:
                for precision_str, seconds in config["temporal_windows"].items():
                    try:
                        precision = TemporalPrecision(precision_str)
                        self.temporal_windows[precision] = timedelta(seconds=seconds)
                    except ValueError:
                        continue  # Skip invalid precision values

            # Load learning parameters
            self.learning_rate = config.get("learning_rate", self.learning_rate)
            self.target_precision = config.get("target_precision", self.target_precision)
            self.target_recall = config.get("target_recall", self.target_recall)

        except Exception as e:
            print(f"Warning: Could not load threshold configuration: {e}")
            # Continue with defaults

    def reset_to_defaults(self):
        """Reset all thresholds to default values."""
        self.confidence_threshold = 0.6
        self.frequency_threshold = 3

        self.temporal_windows = {
            TemporalPrecision.INSTANT: timedelta(seconds=10),
            TemporalPrecision.MINUTE: timedelta(minutes=5),
            TemporalPrecision.SESSION: timedelta(minutes=30),
            TemporalPrecision.DAILY: timedelta(hours=4),
            TemporalPrecision.CYCLICAL: timedelta(days=1),
        }

        self.performance_history.clear()

        # Save reset configuration
        self._save_configuration()

    def export_learning_data(self) -> dict[str, any]:
        """
        Export learning data for analysis or transfer to other systems.

        Returns:
            Dictionary with complete learning history and configuration
        """
        return {
            "current_thresholds": {
                "confidence_threshold": self.confidence_threshold,
                "frequency_threshold": self.frequency_threshold,
                "temporal_windows": {
                    str(k): v.total_seconds() for k, v in self.temporal_windows.items()
                },
            },
            "learning_parameters": {
                "learning_rate": self.learning_rate,
                "target_precision": self.target_precision,
                "target_recall": self.target_recall,
            },
            "performance_history": [
                {**entry, "timestamp": entry["timestamp"].isoformat()}
                for entry in self.performance_history
            ],
            "feedback_summary": {
                "total_feedback": len(self.feedback_history),
                "positive_feedback": len([f for f in self.feedback_history if f.is_meaningful]),
                "negative_feedback": len([f for f in self.feedback_history if not f.is_meaningful]),
            },
        }
