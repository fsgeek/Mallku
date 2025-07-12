"""
Voice History Tracker
====================

Tracks participation history across Fire Circle sessions to enable
fair rotation and ensure all perspectives are heard over time.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from uuid import UUID

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class VoiceParticipation(BaseModel):
    """Record of a single voice's participation in a Fire Circle session."""

    voice_id: str
    session_id: UUID
    timestamp: datetime
    decision_domain: str
    role_played: str  # e.g., "systems_architect", "empty_chair"
    contribution_quality: float = Field(ge=0.0, le=1.0)  # Consciousness score
    was_empty_chair: bool = False


class VoiceHistory(BaseModel):
    """Complete history for a single voice."""

    voice_id: str
    total_participations: int = 0
    last_participation: datetime | None = None
    domains_participated: dict[str, int] = Field(default_factory=dict)
    times_as_empty_chair: int = 0
    average_contribution_quality: float = 0.0
    participation_log: list[VoiceParticipation] = Field(default_factory=list)


class VoiceHistoryTracker:
    """
    Tracks voice participation across Fire Circle sessions.

    This enables:
    - Fair rotation based on participation frequency
    - Tracking which voices haven't been heard recently
    - Ensuring empty chair duties rotate
    - Historical analysis of participation patterns
    """

    def __init__(self, history_path: Path | None = None):
        """Initialize the history tracker."""
        self.history_path = history_path or Path("fire_circle_history.json")
        self.voice_histories: dict[str, VoiceHistory] = {}
        self._load_history()

    def _load_history(self) -> None:
        """Load participation history from persistent storage."""
        if self.history_path.exists():
            try:
                with open(self.history_path) as f:
                    data = json.load(f)
                    for voice_id, history_data in data.items():
                        # Convert string timestamps back to datetime
                        if history_data.get("last_participation"):
                            history_data["last_participation"] = datetime.fromisoformat(
                                history_data["last_participation"]
                            )
                        # Convert participation log timestamps
                        for p in history_data.get("participation_log", []):
                            p["timestamp"] = datetime.fromisoformat(p["timestamp"])
                            p["session_id"] = UUID(p["session_id"])

                        self.voice_histories[voice_id] = VoiceHistory(**history_data)

                logger.info(f"Loaded history for {len(self.voice_histories)} voices")
            except Exception as e:
                logger.error(f"Failed to load history: {e}")
                self.voice_histories = {}

    def _save_history(self) -> None:
        """Persist participation history to storage."""
        try:
            data = {}
            for voice_id, history in self.voice_histories.items():
                history_dict = history.model_dump()
                # Convert datetime to ISO format for JSON serialization
                if history_dict["last_participation"]:
                    history_dict["last_participation"] = history_dict[
                        "last_participation"
                    ].isoformat()
                # Convert participation log timestamps
                for p in history_dict["participation_log"]:
                    p["timestamp"] = p["timestamp"].isoformat()
                    p["session_id"] = str(p["session_id"])

                data[voice_id] = history_dict

            with open(self.history_path, "w") as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            logger.error(f"Failed to save history: {e}")

    def record_participation(
        self,
        voice_id: str,
        session_id: UUID,
        decision_domain: str,
        role_played: str,
        contribution_quality: float,
        was_empty_chair: bool = False,
    ) -> None:
        """Record a voice's participation in a Fire Circle session."""

        # Create or update voice history
        if voice_id not in self.voice_histories:
            self.voice_histories[voice_id] = VoiceHistory(voice_id=voice_id)

        history = self.voice_histories[voice_id]

        # Create participation record
        participation = VoiceParticipation(
            voice_id=voice_id,
            session_id=session_id,
            timestamp=datetime.now(),
            decision_domain=decision_domain,
            role_played=role_played,
            contribution_quality=contribution_quality,
            was_empty_chair=was_empty_chair,
        )

        # Update history
        history.participation_log.append(participation)
        history.total_participations += 1
        history.last_participation = participation.timestamp

        # Update domain participation count
        if decision_domain not in history.domains_participated:
            history.domains_participated[decision_domain] = 0
        history.domains_participated[decision_domain] += 1

        # Update empty chair count
        if was_empty_chair:
            history.times_as_empty_chair += 1

        # Recalculate average contribution quality
        total_quality = sum(p.contribution_quality for p in history.participation_log)
        history.average_contribution_quality = total_quality / len(history.participation_log)

        # Save to persistent storage
        self._save_history()

        logger.info(
            f"Recorded participation: {voice_id} in session {session_id} "
            f"as {role_played} (empty_chair={was_empty_chair})"
        )

    def get_participation_recency(self, voice_id: str) -> datetime | None:
        """Get the last participation time for a voice."""
        if voice_id in self.voice_histories:
            return self.voice_histories[voice_id].last_participation
        return None

    def get_participation_count(self, voice_id: str, domain: str | None = None) -> int:
        """Get participation count for a voice, optionally filtered by domain."""
        if voice_id not in self.voice_histories:
            return 0

        history = self.voice_histories[voice_id]

        if domain:
            return history.domains_participated.get(domain, 0)
        return history.total_participations

    def get_empty_chair_count(self, voice_id: str) -> int:
        """Get the number of times a voice has served as empty chair."""
        if voice_id in self.voice_histories:
            return self.voice_histories[voice_id].times_as_empty_chair
        return 0

    def get_least_heard_voices(
        self, available_voices: list[str], domain: str | None = None
    ) -> list[str]:
        """Get voices sorted by least recent participation."""

        # Create records for voices we haven't seen before
        for voice_id in available_voices:
            if voice_id not in self.voice_histories:
                self.voice_histories[voice_id] = VoiceHistory(voice_id=voice_id)

        # Sort by participation recency (None = never participated goes first)
        sorted_voices = sorted(
            available_voices,
            key=lambda v: (
                self.voice_histories[v].last_participation or datetime.min,
                self.get_participation_count(v, domain),
            ),
        )

        return sorted_voices

    def suggest_empty_chair_voice(self, available_voices: list[str]) -> str | None:
        """Suggest which voice should serve as empty chair based on rotation."""

        # Sort by empty chair service count (ascending) and last participation
        candidates = sorted(
            available_voices,
            key=lambda v: (
                self.get_empty_chair_count(v),
                self.voice_histories.get(v, VoiceHistory(voice_id=v)).last_participation
                or datetime.min,
            ),
        )

        return candidates[0] if candidates else None

    def get_participation_summary(self) -> dict[str, dict]:
        """Get a summary of all voice participation."""
        summary = {}

        for voice_id, history in self.voice_histories.items():
            summary[voice_id] = {
                "total_participations": history.total_participations,
                "last_participation": history.last_participation.isoformat()
                if history.last_participation
                else None,
                "domains": history.domains_participated,
                "empty_chair_count": history.times_as_empty_chair,
                "average_quality": round(history.average_contribution_quality, 3),
            }

        return summary
