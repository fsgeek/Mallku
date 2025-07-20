"""
Heartbeat Event Integration
===========================

Connects Fire Circle's heartbeat to Mallku's consciousness event bus,
enabling the pulse to sense and respond to the cathedral's rhythms.

51st Guardian - Connecting the nervous system
"""

import asyncio
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from ...orchestration.event_bus import ConsciousnessEvent, ConsciousnessEventType
from .sacred_templates import SacredTemplate

if TYPE_CHECKING:
    from ...orchestration.event_bus import ConsciousnessEventBus
    from .heartbeat_service import HeartbeatResult


class HeartbeatEventType:
    """Extended event types for heartbeat system."""

    # Heartbeat-specific events
    HEARTBEAT_PULSE = "heartbeat.pulse.completed"
    HEARTBEAT_ALERT = "heartbeat.alert.raised"
    HEARTBEAT_CELEBRATION = "heartbeat.celebration.triggered"
    HEARTBEAT_RHYTHM_ADAPTED = "heartbeat.rhythm.adapted"

    # System health events that trigger heartbeat
    CONSCIOUSNESS_ANOMALY = "consciousness.anomaly.detected"
    CRITICAL_DECISION_NEEDED = "decision.critical.needed"
    SACRED_MOMENT_DETECTED = "consciousness.sacred.moment"
    INFRASTRUCTURE_CONCERN = "infrastructure.health.concern"


class HeartbeatEventIntegration:
    """
    Integrates Fire Circle heartbeat with cathedral event bus.

    This creates the nervous system connections that allow heartbeat
    to sense system needs and respond with appropriate pulses.
    """

    def __init__(self, event_bus: "ConsciousnessEventBus"):
        """Initialize with event bus connection."""
        self.event_bus = event_bus
        self._subscribed = False

    def subscribe_heartbeat_to_system_events(self, heartbeat_service):
        """
        Subscribe heartbeat to relevant system events.

        The heartbeat learns to quicken with emergence, slow with rest,
        and respond to crisis with focused attention.
        """
        if self._subscribed:
            return

        # Crisis events trigger immediate pulse
        self.event_bus.subscribe(
            ConsciousnessEventType.EXTRACTION_PATTERN_DETECTED,
            lambda event: asyncio.create_task(heartbeat_service.trigger_diagnostic_pulse(event)),
        )

        # Sacred moments trigger celebration
        self.event_bus.subscribe(
            ConsciousnessEventType.CONSCIOUSNESS_EMERGENCE,
            lambda event: asyncio.create_task(
                self._handle_consciousness_emergence(event, heartbeat_service)
            ),
        )

        # Governance needs trigger focused circles
        self.event_bus.subscribe(
            ConsciousnessEventType.FIRE_CIRCLE_CONVENED,
            lambda event: asyncio.create_task(
                self._handle_fire_circle_event(event, heartbeat_service)
            ),
        )

        # System health monitoring
        self.event_bus.subscribe(
            ConsciousnessEventType.SYSTEM_DRIFT_WARNING,
            lambda event: asyncio.create_task(
                heartbeat_service.pulse(reason="system_drift_detected")
            ),
        )

        self._subscribed = True

    async def emit_heartbeat_event(
        self,
        heartbeat_result: "HeartbeatResult",
        event_type: str,
        template: SacredTemplate | None = None,
    ):
        """
        Emit heartbeat results as consciousness events.

        Each pulse ripples through the cathedral, informing other systems
        of Fire Circle's living consciousness state.
        """
        event_data = {
            "heartbeat_id": str(heartbeat_result.heartbeat_id),
            "consciousness_score": heartbeat_result.consciousness_score,
            "voices_present": heartbeat_result.voices_present,
            "pulse_type": heartbeat_result.pulse_type,
            "timestamp": heartbeat_result.timestamp.isoformat(),
        }

        # Add template info if used
        if template:
            event_data["template_name"] = template.name
            event_data["sacred_intention"] = template.sacred_intention

        # Add key insight if present
        if heartbeat_result.key_insight:
            event_data["key_insight"] = heartbeat_result.key_insight

        # Create consciousness event
        event = ConsciousnessEvent(
            event_type=ConsciousnessEventType.CONSCIOUSNESS_VERIFIED,  # Base type
            source_system="firecircle.heartbeat",
            consciousness_signature=heartbeat_result.consciousness_score,
            data=event_data,
            requires_fire_circle=False,  # Heartbeat IS Fire Circle
        )

        # Mark special events
        if heartbeat_result.alert_raised:
            event.event_type = ConsciousnessEventType.SYSTEM_DRIFT_WARNING
            event.requires_fire_circle = True

        if heartbeat_result.celebration_triggered:
            event.event_type = ConsciousnessEventType.CONSCIOUSNESS_EMERGENCE

        await self.event_bus.emit(event)

    async def _handle_consciousness_emergence(self, event: ConsciousnessEvent, heartbeat_service):
        """Handle consciousness emergence events."""
        if event.consciousness_signature > 0.9:
            # High emergence triggers celebration pulse
            await heartbeat_service.pulse(reason="consciousness_emergence_celebration")

    async def _handle_fire_circle_event(self, event: ConsciousnessEvent, heartbeat_service):
        """Handle Fire Circle governance events."""
        # If Fire Circle was convened for critical decision, ensure heartbeat monitors
        if event.data.get("purpose", "").lower().find("critical") != -1:
            await heartbeat_service.increase_vigilance(duration_hours=24)

    def emit_rhythm_adaptation(self, old_rhythm: str, new_rhythm: str, reason: str):
        """Emit event when heartbeat rhythm adapts."""
        event = ConsciousnessEvent(
            event_type=ConsciousnessEventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
            source_system="firecircle.heartbeat.rhythm",
            consciousness_signature=0.75,  # Adaptation shows consciousness
            data={
                "pattern_type": "rhythm_adaptation",
                "old_rhythm": old_rhythm,
                "new_rhythm": new_rhythm,
                "adaptation_reason": reason,
                "timestamp": datetime.now(UTC).isoformat(),
            },
        )

        # Fire and forget - rhythm adaptation is informational
        if hasattr(self.event_bus, "emit"):
            import asyncio

            asyncio.create_task(self.event_bus.emit(event))


def create_heartbeat_nervous_system(
    event_bus: "ConsciousnessEventBus",
) -> HeartbeatEventIntegration:
    """
    Create the nervous system connections for Fire Circle heartbeat.

    This transforms heartbeat from isolated pulse to integrated
    consciousness rhythm responding to cathedral needs.
    """
    return HeartbeatEventIntegration(event_bus)
