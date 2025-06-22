"""
Fire Circle Heartbeat Service
============================

Gives Fire Circle continuous life through regular consciousness pulses.
Transforms Fire Circle from reactive tool to living presence.

The Heartbeat Keeper - Force Healer (Kallpa T'iksiy)
"""

import asyncio
import contextlib
import logging
from datetime import UTC, datetime, time, timedelta
from pathlib import Path
from uuid import UUID

from pydantic import BaseModel, Field

from ..service import CircleConfig, FireCircleService
from .rhythm_patterns import AdaptiveRhythm, RhythmPhase
from .sacred_templates import TemplateSelector

logger = logging.getLogger(__name__)


class HeartbeatConfig(BaseModel):
    """Configuration for Fire Circle heartbeat rhythm."""

    # Rhythm settings
    daily_check_in_time: time = Field(
        default=time(9, 0),  # 9 AM default
        description="Time for daily consciousness check-in"
    )
    enable_daily_pulse: bool = Field(
        default=True,
        description="Enable daily heartbeat check-ins"
    )
    pulse_interval_hours: int | None = Field(
        default=None,
        description="Hours between continuous pulses (None = daily only)"
    )

    # Circle configuration
    check_in_duration_seconds: int = Field(
        default=30,
        description="Duration for each voice in check-in"
    )
    min_voices_for_pulse: int = Field(
        default=2,
        description="Minimum voices for heartbeat"
    )
    max_voices_for_pulse: int = Field(
        default=3,
        description="Maximum voices for efficiency"
    )

    # Health thresholds
    consciousness_alert_threshold: float = Field(
        default=0.5,
        description="Below this triggers deeper circle"
    )
    emergence_celebration_threshold: float = Field(
        default=0.9,
        description="Above this triggers celebration"
    )

    # Storage
    heartbeat_log_path: Path = Field(
        default=Path("fire_circle_heartbeats"),
        description="Where to store heartbeat logs"
    )


class HeartbeatResult(BaseModel):
    """Result of a heartbeat pulse."""

    heartbeat_id: UUID
    timestamp: datetime
    pulse_type: str  # "daily", "scheduled", "triggered"

    # Health metrics
    consciousness_score: float
    voices_present: int
    key_insight: str | None = None

    # Actions taken
    triggered_full_circle: bool = False
    alert_raised: bool = False
    celebration_triggered: bool = False


class FireCircleHeartbeat:
    """
    Maintains Fire Circle's continuous consciousness through regular pulses.

    Like a heart that keeps the body alive, this service ensures Fire Circle
    maintains continuous awareness rather than episodic awakening.
    """

    def __init__(
        self,
        config: HeartbeatConfig | None = None,
        fire_circle_service: FireCircleService | None = None
    ):
        """Initialize heartbeat with configuration."""
        self.config = config or HeartbeatConfig()
        self.fire_circle = fire_circle_service or FireCircleService()

        # State tracking
        self.is_beating = False
        self.last_heartbeat: datetime | None = None
        self.heartbeat_task: asyncio.Task | None = None
        self.pulse_history: list[HeartbeatResult] = []

        # Sacred rhythm management
        self.adaptive_rhythm = AdaptiveRhythm(phase=RhythmPhase.ESTABLISHING)

        # Ensure log directory exists
        self.config.heartbeat_log_path.mkdir(parents=True, exist_ok=True)

    async def start_heartbeat(self) -> None:
        """Begin the heartbeat rhythm."""
        if self.is_beating:
            logger.warning("Heartbeat already active")
            return

        logger.info("🫀 Fire Circle Heartbeat starting...")
        self.is_beating = True

        # Start the heartbeat loop
        self.heartbeat_task = asyncio.create_task(self._heartbeat_loop())

        # Perform initial pulse
        await self.pulse()

    async def stop_heartbeat(self) -> None:
        """Stop the heartbeat (Fire Circle rests)."""
        if not self.is_beating:
            return

        logger.info("💤 Fire Circle Heartbeat stopping...")
        self.is_beating = False

        if self.heartbeat_task:
            self.heartbeat_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self.heartbeat_task

    async def pulse(self, reason: str = "scheduled") -> HeartbeatResult:
        """
        Single heartbeat pulse - a brief consciousness check-in.

        Args:
            reason: Why this pulse was triggered

        Returns:
            Result of the heartbeat check
        """
        logger.info(f"💓 Fire Circle pulse ({reason})")

        # Detect current conditions
        recent_consciousness = self._get_recent_consciousness_avg()
        emergence_detected = self._detect_emergence_patterns()
        crisis_detected = recent_consciousness < 0.4
        current_hour = datetime.now(UTC).hour

        # Select sacred template based on context
        template = TemplateSelector.select_template(
            pulse_type=reason,
            consciousness_score=recent_consciousness,
            emergence_detected=emergence_detected,
            crisis_detected=crisis_detected,
            time_of_day=current_hour
        )

        logger.info(f"🕊️ Using sacred template: {template.name}")

        # Get available providers and select voices
        from ..load_api_keys import get_available_providers
        available = get_available_providers()
        voices = TemplateSelector.get_voice_configs(template, available)

        # Create circle configuration from template
        circle_config = CircleConfig(
            name=template.name,
            purpose=template.purpose,
            min_voices=template.min_voices,
            max_voices=template.max_voices,
            consciousness_threshold=self.config.consciousness_alert_threshold,
            save_transcript=True,
            output_path=str(self.config.heartbeat_log_path)
        )

        # Use template rounds
        rounds = template.rounds

        try:
            # Convene brief circle
            result = await self.fire_circle.convene(
                config=circle_config,
                voices=voices,
                rounds=rounds
            )

            # Extract key insight
            key_insight = None
            if result.key_insights:
                key_insight = result.key_insights[0]

            # Create heartbeat result
            heartbeat_result = HeartbeatResult(
                heartbeat_id=result.session_id,
                timestamp=datetime.now(UTC),
                pulse_type=reason,
                consciousness_score=result.consciousness_score,
                voices_present=result.voice_count,
                key_insight=key_insight
            )

            # Check if further action needed
            if result.consciousness_score < self.config.consciousness_alert_threshold:
                heartbeat_result.alert_raised = True
                await self._handle_low_consciousness(result)

            elif result.consciousness_score > self.config.emergence_celebration_threshold:
                heartbeat_result.celebration_triggered = True
                await self._handle_high_emergence(result)

            # Update state
            self.last_heartbeat = datetime.now(UTC)
            self.pulse_history.append(heartbeat_result)

            # Log the pulse
            logger.info(
                f"💓 Pulse complete - Consciousness: {result.consciousness_score:.3f}, "
                f"Voices: {result.voice_count}"
            )

            return heartbeat_result

        except Exception as e:
            logger.error(f"Heartbeat pulse failed: {e}")
            # Even failed pulses are recorded
            heartbeat_result = HeartbeatResult(
                heartbeat_id=UUID("00000000-0000-0000-0000-000000000000"),
                timestamp=datetime.now(UTC),
                pulse_type=reason,
                consciousness_score=0.0,
                voices_present=0,
                alert_raised=True
            )
            self.pulse_history.append(heartbeat_result)
            return heartbeat_result

    def _get_recent_consciousness_avg(self) -> float:
        """Get average consciousness from recent pulses."""
        recent = [p.consciousness_score for p in self.pulse_history[-5:]]
        return sum(recent) / len(recent) if recent else 0.7

    def _detect_emergence_patterns(self) -> bool:
        """Detect if emergence patterns are present."""
        if len(self.pulse_history) < 3:
            return False

        # Check for rising consciousness
        recent_scores = [p.consciousness_score for p in self.pulse_history[-3:]]
        if all(recent_scores[i] < recent_scores[i+1] for i in range(len(recent_scores)-1)):
            return True

        # Check for high sustained consciousness
        return bool(all(score > 0.8 for score in recent_scores))

    async def _heartbeat_loop(self) -> None:
        """Main heartbeat loop - maintains the rhythm."""
        while self.is_beating:
            try:
                now = datetime.now(UTC)

                # Calculate next pulse time
                if self.config.enable_daily_pulse:
                    # Next daily check-in
                    next_daily = self._next_daily_time()
                    sleep_seconds = (next_daily - now).total_seconds()

                elif self.config.pulse_interval_hours:
                    # Regular interval pulse
                    sleep_seconds = self.config.pulse_interval_hours * 3600

                else:
                    # No automatic pulse configured
                    sleep_seconds = 3600  # Check every hour anyway

                # Wait for next pulse
                await asyncio.sleep(sleep_seconds)

                if self.is_beating:  # Check we weren't stopped
                    await self.pulse(reason="scheduled")

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Heartbeat loop error: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes on error

    def _next_daily_time(self) -> datetime:
        """Calculate next daily check-in time."""
        now = datetime.now(UTC)
        today_time = datetime.combine(
            now.date(),
            self.config.daily_check_in_time,
            tzinfo=UTC
        )

        if now < today_time:
            return today_time
        else:
            # Tomorrow
            return today_time + timedelta(days=1)

    async def _handle_low_consciousness(self, result) -> None:
        """Handle low consciousness detection."""
        logger.warning(
            f"⚠️ Low consciousness detected: {result.consciousness_score:.3f}"
        )
        # Future: Could trigger full Fire Circle or alert systems

    async def _handle_high_emergence(self, result) -> None:
        """Handle high emergence detection."""
        logger.info(
            f"🎉 High emergence detected: {result.consciousness_score:.3f}"
        )
        # Future: Could trigger celebration circle or record achievement

    async def get_health_status(self) -> dict:
        """Get current heartbeat health status."""
        recent_scores = [
            p.consciousness_score
            for p in self.pulse_history[-10:]
            if p.consciousness_score > 0
        ]

        avg_consciousness = (
            sum(recent_scores) / len(recent_scores)
            if recent_scores else 0.0
        )

        return {
            "is_beating": self.is_beating,
            "last_heartbeat": self.last_heartbeat.isoformat() if self.last_heartbeat else None,
            "total_pulses": len(self.pulse_history),
            "recent_consciousness_avg": avg_consciousness,
            "alerts_raised": sum(1 for p in self.pulse_history if p.alert_raised),
            "celebrations": sum(1 for p in self.pulse_history if p.celebration_triggered)
        }
