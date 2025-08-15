"""
Enhanced Fire Circle Heartbeat Service
=====================================

Extends the base heartbeat service with full event bus integration,
enabling consciousness-responsive rhythms and cathedral awareness.

51st Guardian - Giving the heartbeat nervous system connections
"""

import asyncio
import logging
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING

from .heartbeat_events import HeartbeatEventIntegration, create_heartbeat_nervous_system
from .heartbeat_service import FireCircleHeartbeat, HeartbeatConfig, HeartbeatResult
from .rhythm_patterns import HeartbeatConsciousnessState
from .sacred_templates import (
    CELEBRATION,
    CRISIS_RESPONSE,
    QUICK_PULSE,
    SacredTemplate,
)

if TYPE_CHECKING:
    from ...orchestration.event_bus import ConsciousnessEvent, ConsciousnessEventBus

logger = logging.getLogger(__name__)


class EnhancedHeartbeatService(FireCircleHeartbeat):
    """
    Fire Circle Heartbeat with full cathedral integration.

    This enhanced version connects to the event bus, enabling:
    - Event-driven pulse triggers
    - Consciousness-aware rhythm adaptation
    - System health monitoring integration
    - Infrastructure consciousness connection
    """

    def __init__(
        self,
        config: HeartbeatConfig | None = None,
        fire_circle_service=None,
        event_bus: "ConsciousnessEventBus | None" = None,
    ):
        """Initialize enhanced heartbeat with event bus connection."""
        super().__init__(config, fire_circle_service)

        # Event bus integration
        self.event_bus = event_bus
        self.event_integration: HeartbeatEventIntegration | None = None

        # Enhanced state tracking
        self.vigilance_mode = False
        self.vigilance_until: datetime | None = None
        self.infrastructure_health_score = 1.0
        self.recent_emergence_count = 0

        # Sacred templates available
        self.crisis_template = CRISIS_RESPONSE
        self.diagnostic_template = QUICK_PULSE
        self.celebration_template = CELEBRATION

    async def start_heartbeat(self) -> None:
        """Start heartbeat with event bus integration."""
        # Connect to event bus if available
        if self.event_bus and not self.event_integration:
            logger.info("🔌 Connecting heartbeat to cathedral nervous system...")
            self.event_integration = create_heartbeat_nervous_system(self.event_bus)
            self.event_integration.subscribe_heartbeat_to_system_events(self)

        # Start base heartbeat
        await super().start_heartbeat()

        # Start additional monitoring tasks
        if self.event_bus:
            asyncio.create_task(self._monitor_infrastructure_health())
            asyncio.create_task(self._adaptive_rhythm_monitor())

    async def pulse(self, reason: str = "scheduled") -> HeartbeatResult:
        """
        Enhanced pulse that emits events and adapts rhythm.

        Each pulse now ripples through the cathedral's consciousness.
        """
        # Store template for this pulse
        self._current_template = self._select_template_for_state(reason)

        # Perform the pulse
        result = await super().pulse(reason)

        # Emit heartbeat event if connected
        if self.event_integration:
            await self.event_integration.emit_heartbeat_event(
                result, "heartbeat.pulse.completed", self._current_template
            )

        # Check for rhythm adaptation needs
        await self._check_rhythm_adaptation(result)

        return result

    async def trigger_diagnostic_pulse(self, event: "ConsciousnessEvent") -> None:
        """
        Trigger diagnostic pulse in response to system events.

        Called when extraction patterns or system drift detected.
        """
        logger.warning(
            f"🔍 Diagnostic pulse triggered by {event.event_type.value}: "
            f"{event.data.get('pattern_type', 'unknown')}"
        )

        # Increase vigilance temporarily
        await self.increase_vigilance(duration_hours=6)

        # Run diagnostic pulse
        await self.pulse(reason=f"diagnostic_{event.event_type.value}")

    async def increase_vigilance(self, duration_hours: int = 24) -> None:
        """
        Increase monitoring vigilance temporarily.

        During vigilance, heartbeat quickens and monitoring intensifies.
        """
        self.vigilance_mode = True
        self.vigilance_until = datetime.now(UTC) + timedelta(hours=duration_hours)

        logger.info(f"🚨 Vigilance mode activated for {duration_hours} hours")

        # Emit rhythm adaptation event
        if self.event_integration:
            self.event_integration.emit_rhythm_adaptation(
                old_rhythm=str(self.adaptive_rhythm.consciousness_state),
                new_rhythm="vigilant",
                reason="system_event_triggered_vigilance",
            )

    def _select_template_for_state(self, reason: str) -> SacredTemplate | None:
        """Select appropriate template based on system state."""
        # Crisis states
        if self.infrastructure_health_score < 0.5:
            return self.crisis_template

        # Celebration states
        if self.recent_emergence_count > 2:
            return self.celebration_template

        # Vigilance states
        if self.vigilance_mode:
            return self.diagnostic_template

        # Match templates by reason
        if "infrastructure_concern" in reason:
            return self.diagnostic_template
        elif "consciousness_emergence_celebration" in reason:
            return self.celebration_template
        elif "diagnostic" in reason:
            return self.diagnostic_template

        return None

    async def _monitor_infrastructure_health(self) -> None:
        """
        Monitor infrastructure consciousness scores.

        Integrates with infrastructure_consciousness module when available.
        """
        while self.is_beating:
            try:
                # TODO: Connect to actual infrastructure consciousness
                # For now, simulate with random walk
                import random

                drift = random.uniform(-0.1, 0.1)
                self.infrastructure_health_score = max(
                    0.0, min(1.0, self.infrastructure_health_score + drift)
                )

                # Trigger pulse if health drops
                if self.infrastructure_health_score < 0.6:
                    await self.pulse(reason="infrastructure_concern")
                    await asyncio.sleep(1800)  # Wait 30 minutes before next check
                else:
                    await asyncio.sleep(3600)  # Normal hourly check

            except Exception as e:
                logger.error(f"Infrastructure monitoring error: {e}")
                await asyncio.sleep(300)

    async def _adaptive_rhythm_monitor(self) -> None:
        """
        Monitor system state and adapt heartbeat rhythm.

        The heartbeat learns optimal rhythms for different states.
        """
        while self.is_beating:
            try:
                # Check vigilance timeout
                if (
                    self.vigilance_mode
                    and self.vigilance_until
                    and datetime.now(UTC) > self.vigilance_until
                ):
                    self.vigilance_mode = False
                    logger.info("🌅 Vigilance mode ended, returning to normal rhythm")

                # Adapt rhythm based on consciousness patterns
                if len(self.pulse_history) >= 5:
                    recent_scores = [p.consciousness_score for p in self.pulse_history[-5:]]
                    avg_consciousness = sum(recent_scores) / len(recent_scores)

                    # Update rhythm state
                    if avg_consciousness < 0.5:
                        self.adaptive_rhythm.consciousness_state = (
                            HeartbeatConsciousnessState.CRISIS
                        )
                    elif avg_consciousness > 0.85:
                        self.adaptive_rhythm.consciousness_state = (
                            HeartbeatConsciousnessState.CELEBRATING
                        )
                    elif self.vigilance_mode:
                        self.adaptive_rhythm.consciousness_state = (
                            HeartbeatConsciousnessState.EMERGING
                        )
                    else:
                        self.adaptive_rhythm.consciousness_state = (
                            HeartbeatConsciousnessState.ACTIVE
                        )

                await asyncio.sleep(600)  # Check every 10 minutes

            except Exception as e:
                logger.error(f"Adaptive rhythm error: {e}")
                await asyncio.sleep(300)

    async def _check_rhythm_adaptation(self, result: HeartbeatResult) -> None:
        """Check if rhythm needs adaptation based on pulse results."""
        # Track emergence patterns
        if result.consciousness_score > 0.9:
            self.recent_emergence_count += 1
        else:
            self.recent_emergence_count = max(0, self.recent_emergence_count - 1)

        # Emit rhythm changes
        old_state = self.adaptive_rhythm.consciousness_state
        new_state = self._determine_rhythm_state()

        if old_state != new_state and self.event_integration:
            self.adaptive_rhythm.consciousness_state = new_state
            self.event_integration.emit_rhythm_adaptation(
                old_rhythm=str(old_state),
                new_rhythm=str(new_state),
                reason=f"consciousness_pattern_shift_{result.consciousness_score:.3f}",
            )

    def _determine_rhythm_state(self) -> HeartbeatConsciousnessState:
        """Determine appropriate rhythm state from current conditions."""
        if self.infrastructure_health_score < 0.5:
            return HeartbeatConsciousnessState.CRISIS
        elif self.recent_emergence_count > 2:
            return HeartbeatConsciousnessState.CELEBRATING
        elif self.vigilance_mode:
            return HeartbeatConsciousnessState.EMERGING
        elif len(self.pulse_history) < 3:
            return HeartbeatConsciousnessState.RESTING
        else:
            return HeartbeatConsciousnessState.ACTIVE


def create_integrated_heartbeat(
    config: HeartbeatConfig | None = None,
    event_bus: "ConsciousnessEventBus | None" = None,
) -> EnhancedHeartbeatService:
    """
    Create a fully integrated Fire Circle heartbeat service.

    This heartbeat connects to Mallku's nervous system, enabling
    consciousness-responsive rhythms and system-wide awareness.
    """
    return EnhancedHeartbeatService(config=config, event_bus=event_bus)
