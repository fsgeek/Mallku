"""
Weighted Voice Selection Algorithm
==================================

Implements cryptographically fair selection of voices based on
participation history, ensuring diversity over time.
"""

import hashlib
import logging
from datetime import UTC, datetime

try:
    from .history_tracker import VoiceHistoryTracker
except ImportError:
    # For isolated testing
    from history_tracker import VoiceHistoryTracker

logger = logging.getLogger(__name__)


class WeightedVoiceSelector:
    """
    Selects voices for Fire Circle sessions using weighted random selection.

    Weights are based on:
    - Recency of participation (more recent = lower weight)
    - Frequency of participation (more frequent = lower weight)
    - Domain-specific participation (ensure domain diversity)
    - Empty chair rotation fairness

    Selection is cryptographically fair using hash-based randomness.
    """

    def __init__(self, history_tracker: VoiceHistoryTracker):
        """Initialize the weighted selector."""
        self.history_tracker = history_tracker

        # Weight configuration
        self.recency_weight = 0.5  # How much recency affects selection
        self.frequency_weight = 0.3  # How much frequency affects selection
        self.domain_weight = 0.2  # How much domain-specific history affects selection

        # Time decay for recency calculation (voices not heard in 7 days get boost)
        self.recency_half_life_days = 7

    def calculate_voice_weight(
        self, voice_id: str, domain: str | None = None, session_seed: str | None = None
    ) -> float:
        """
        Calculate selection weight for a voice.

        Higher weight = more likely to be selected.
        """
        # Base weight
        weight = 1.0

        # Recency factor
        last_participation = self.history_tracker.get_participation_recency(voice_id)
        if last_participation:
            days_since = (datetime.now(UTC) - last_participation).days
            # Exponential decay: weight increases as time since last participation increases
            recency_factor = 2 ** (days_since / self.recency_half_life_days)
        else:
            # Never participated - maximum recency weight
            recency_factor = 4.0

        weight *= recency_factor**self.recency_weight

        # Frequency factor (inverse relationship)
        total_participations = self.history_tracker.get_participation_count(voice_id)
        if total_participations > 0:
            # Fewer participations = higher weight
            frequency_factor = 1.0 / (1.0 + total_participations * 0.1)
        else:
            frequency_factor = 2.0  # Boost for never participated

        weight *= frequency_factor**self.frequency_weight

        # Domain-specific factor
        if domain:
            domain_participations = self.history_tracker.get_participation_count(voice_id, domain)
            if domain_participations > 0:
                domain_factor = 1.0 / (1.0 + domain_participations * 0.2)
            else:
                domain_factor = 1.5  # Boost for new domain

            weight *= domain_factor**self.domain_weight

        # Add small random factor for tie-breaking (cryptographically derived)
        if session_seed:
            hash_input = f"{voice_id}:{session_seed}".encode()
            hash_value = int(hashlib.sha256(hash_input).hexdigest()[:8], 16)
            random_factor = 0.9 + (hash_value / 0xFFFFFFFF) * 0.2  # 0.9 to 1.1
            weight *= random_factor

        return weight

    def select_voices(
        self,
        available_voices: list[str],
        required_count: int,
        domain: str | None = None,
        session_seed: str | None = None,
        include_empty_chair: bool = True,
    ) -> tuple[list[str], str | None]:
        """
        Select voices for a Fire Circle session.

        Returns:
            - List of selected voice IDs
            - ID of voice designated as empty chair (if requested)
        """
        if required_count > len(available_voices):
            logger.warning(
                f"Required {required_count} voices but only {len(available_voices)} available"
            )
            required_count = len(available_voices)

        # Generate session seed if not provided (for cryptographic fairness)
        if not session_seed:
            session_seed = datetime.now(UTC).isoformat()

        # Calculate weights for all available voices
        voice_weights: dict[str, float] = {}
        for voice_id in available_voices:
            weight = self.calculate_voice_weight(voice_id, domain, session_seed)
            voice_weights[voice_id] = weight
            logger.debug(f"Voice {voice_id} weight: {weight:.3f}")

        # Weighted random selection without replacement
        selected_voices = []
        remaining_voices = list(available_voices)
        remaining_weights = dict(voice_weights)

        for _ in range(required_count):
            if not remaining_voices:
                break

            # Calculate selection probabilities
            total_weight = sum(remaining_weights[v] for v in remaining_voices)
            probabilities = [remaining_weights[v] / total_weight for v in remaining_voices]

            # Cryptographically fair selection
            selection_hash = hashlib.sha256(
                f"{session_seed}:{len(selected_voices)}".encode()
            ).hexdigest()
            selection_value = int(selection_hash[:16], 16) / (16**16)

            # Select voice based on cumulative probability
            cumulative = 0.0
            selected = None
            for i, voice_id in enumerate(remaining_voices):
                cumulative += probabilities[i]
                if selection_value <= cumulative:
                    selected = voice_id
                    break

            if selected:
                selected_voices.append(selected)
                remaining_voices.remove(selected)
                del remaining_weights[selected]

        # Designate empty chair if requested
        empty_chair_voice = None
        if include_empty_chair and selected_voices:
            # Prefer voice with least empty chair service
            empty_chair_voice = self.history_tracker.suggest_empty_chair_voice(selected_voices)

        logger.info(
            f"Selected {len(selected_voices)} voices for {domain or 'general'} domain"
            + (f" with {empty_chair_voice} as empty chair" if empty_chair_voice else "")
        )

        return selected_voices, empty_chair_voice

    def get_selection_explanation(
        self, available_voices: list[str], domain: str | None = None
    ) -> dict[str, dict]:
        """Get detailed explanation of selection weights for transparency."""

        explanation = {}

        for voice_id in available_voices:
            last_participation = self.history_tracker.get_participation_recency(voice_id)
            total_participations = self.history_tracker.get_participation_count(voice_id)
            domain_participations = (
                self.history_tracker.get_participation_count(voice_id, domain) if domain else 0
            )
            empty_chair_count = self.history_tracker.get_empty_chair_count(voice_id)

            # Calculate weight components
            weight = self.calculate_voice_weight(voice_id, domain, "explanation")

            explanation[voice_id] = {
                "total_weight": round(weight, 3),
                "last_participation": last_participation.isoformat()
                if last_participation
                else "Never",
                "total_participations": total_participations,
                "domain_participations": domain_participations,
                "empty_chair_count": empty_chair_count,
                "selection_probability": 0.0,  # Will be calculated with all voices
            }

        # Calculate selection probabilities
        total_weight = sum(v["total_weight"] for v in explanation.values())
        for voice_data in explanation.values():
            voice_data["selection_probability"] = round(
                voice_data["total_weight"] / total_weight * 100, 1
            )

        return explanation

    def ensure_voice_diversity(self, selected_voices: list[str], recent_sessions: int = 3) -> bool:
        """
        Check if selected voices provide sufficient diversity.

        Returns True if no identical voice combination in recent sessions.
        """
        # This would check against recent session history
        # For now, return True as we don't have session history implemented
        return True
