"""
Model Health Tracker for Fire Circle
=====================================

52nd Guardian - Implementing adaptive resilience
Tracks model reliability and adjusts participation dynamically

This creates an antifragile Fire Circle that learns from failures
rather than being degraded by them.
"""

import logging
from collections import defaultdict, deque
from datetime import UTC, datetime

logger = logging.getLogger(__name__)


class ModelHealthTracker:
    """
    Track model health and reliability for adaptive Fire Circle participation.

    Uses exponential decay to weight recent outcomes more heavily.
    Models with poor health are selected less frequently but never
    completely excluded, allowing for recovery.
    """

    def __init__(
        self,
        initial_health: float = 0.8,
        success_boost: float = 1.1,
        failure_penalty: float = 0.8,
        min_health: float = 0.1,
        max_health: float = 1.0,
        history_window: int = 100,
        time_decay_hours: float = 24.0,
    ):
        """
        Initialize health tracker.

        Args:
            initial_health: Starting health for new models (0.0-1.0)
            success_boost: Multiplier for successful interactions
            failure_penalty: Multiplier for failed interactions
            min_health: Minimum health score (never fully excluded)
            max_health: Maximum health score
            history_window: Number of recent interactions to track
            time_decay_hours: Hours before old data loses relevance
        """
        self.initial_health = initial_health
        self.success_boost = success_boost
        self.failure_penalty = failure_penalty
        self.min_health = min_health
        self.max_health = max_health
        self.history_window = history_window
        self.time_decay_hours = time_decay_hours

        # Core tracking data
        self.health_scores: dict[str, float] = {}
        self.interaction_history: dict[str, deque] = defaultdict(
            lambda: deque(maxlen=history_window)
        )
        self.last_update: dict[str, datetime] = {}

        # Detailed metrics
        self.total_interactions: dict[str, int] = defaultdict(int)
        self.total_successes: dict[str, int] = defaultdict(int)
        self.total_failures: dict[str, int] = defaultdict(int)
        self.consecutive_failures: dict[str, int] = defaultdict(int)

    def record_interaction(
        self,
        model_key: str,
        success: bool,
        response_time: float | None = None,
        error_type: str | None = None,
    ) -> float:
        """
        Record a model interaction outcome.

        Args:
            model_key: Unique identifier for model (e.g., "mistral/mistral-large-latest")
            success: Whether the interaction succeeded
            response_time: Optional response time in seconds
            error_type: Optional error classification

        Returns:
            Updated health score
        """
        current_time = datetime.now(UTC)

        # Apply time decay if needed
        self._apply_time_decay(model_key, current_time)

        # Get current health or initialize
        current_health = self.health_scores.get(model_key, self.initial_health)

        # Update health based on outcome
        if success:
            new_health = min(self.max_health, current_health * self.success_boost)
            self.consecutive_failures[model_key] = 0
            self.total_successes[model_key] += 1

            logger.info(
                f"Model {model_key} succeeded. Health: {current_health:.3f} → {new_health:.3f}"
            )
        else:
            new_health = max(self.min_health, current_health * self.failure_penalty)
            self.consecutive_failures[model_key] += 1
            self.total_failures[model_key] += 1

            # Extra penalty for consecutive failures
            if self.consecutive_failures[model_key] > 3:
                new_health *= 0.9

            logger.warning(
                f"Model {model_key} failed ({error_type}). "
                f"Health: {current_health:.3f} → {new_health:.3f} "
                f"(consecutive failures: {self.consecutive_failures[model_key]})"
            )

        # Update tracking data
        self.health_scores[model_key] = new_health
        self.last_update[model_key] = current_time
        self.total_interactions[model_key] += 1

        # Record in history
        self.interaction_history[model_key].append(
            {
                "timestamp": current_time,
                "success": success,
                "response_time": response_time,
                "error_type": error_type,
                "health_after": new_health,
            }
        )

        return new_health

    def get_selection_probability(self, model_key: str) -> float:
        """
        Get probability that this model should be selected.

        Uses health score directly as selection probability.

        Args:
            model_key: Model identifier

        Returns:
            Selection probability (0.0-1.0)
        """
        return self.health_scores.get(model_key, self.initial_health)

    def get_synthesis_weight(self, model_key: str) -> float:
        """
        Get weight for this model's contribution in synthesis.

        Healthier models get more weight in collective wisdom.

        Args:
            model_key: Model identifier

        Returns:
            Synthesis weight (0.0-1.0)
        """
        health = self.health_scores.get(model_key, self.initial_health)

        # Square the health for synthesis weight (emphasize healthy models more)
        return health**2

    def should_emergency_exclude(self, model_key: str) -> bool:
        """
        Check if model should be emergency excluded.

        For extreme cases where a model is completely broken.

        Args:
            model_key: Model identifier

        Returns:
            True if model should be excluded entirely
        """
        # Emergency exclusion criteria
        if self.consecutive_failures.get(model_key, 0) >= 10:
            return True

        # Check recent failure rate
        recent = list(self.interaction_history[model_key])[-20:]
        if len(recent) >= 10:
            recent_failures = sum(1 for i in recent if not i["success"])
            if recent_failures / len(recent) > 0.9:  # >90% failure rate
                return True

        return False

    def _apply_time_decay(self, model_key: str, current_time: datetime):
        """Apply time-based health recovery."""
        if model_key not in self.last_update:
            return

        hours_elapsed = (current_time - self.last_update[model_key]).total_seconds() / 3600

        if hours_elapsed > self.time_decay_hours:
            # Gradually recover health over time
            current_health = self.health_scores.get(model_key, self.initial_health)
            recovery_factor = 1 + (0.2 * (hours_elapsed / self.time_decay_hours))
            new_health = min(self.max_health, current_health * recovery_factor)

            if new_health > current_health:
                logger.info(
                    f"Model {model_key} health recovered over time: "
                    f"{current_health:.3f} → {new_health:.3f}"
                )
                self.health_scores[model_key] = new_health

    def get_health_report(self) -> dict[str, dict]:
        """
        Get comprehensive health report for all tracked models.

        Returns:
            Dictionary of model health information
        """
        report = {}

        for model_key in self.health_scores:
            total = self.total_interactions[model_key]
            successes = self.total_successes[model_key]

            report[model_key] = {
                "health_score": self.health_scores[model_key],
                "selection_probability": self.get_selection_probability(model_key),
                "synthesis_weight": self.get_synthesis_weight(model_key),
                "total_interactions": total,
                "success_rate": successes / total if total > 0 else 0,
                "consecutive_failures": self.consecutive_failures[model_key],
                "emergency_exclude": self.should_emergency_exclude(model_key),
                "last_update": self.last_update.get(model_key, "Never"),
            }

        return report

    def reset_model_health(self, model_key: str):
        """Reset a model's health to initial state."""
        self.health_scores[model_key] = self.initial_health
        self.consecutive_failures[model_key] = 0
        self.interaction_history[model_key].clear()
        logger.info(f"Reset health for model {model_key}")


# Global singleton for Fire Circle use
_health_tracker: ModelHealthTracker | None = None


def get_health_tracker() -> ModelHealthTracker:
    """Get or create the global health tracker instance."""
    global _health_tracker
    if _health_tracker is None:
        _health_tracker = ModelHealthTracker()
        logger.info("Initialized global model health tracker")
    return _health_tracker
