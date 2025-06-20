"""
Fire Circle Bridge - Unifying Governance with Consciousness
===========================================================

This bridge enables the existing Fire Circle interface to use consciousness
circulation as its transport layer, transforming governance from a separate
system into an integrated aspect of cathedral consciousness.

The Governance Weaver
"""

import logging
from typing import Any

from ..orchestration.event_bus import ConsciousnessEvent, ConsciousnessEventBus, EventType
from ..reciprocity.fire_circle_interface import FireCircleInterface
from ..reciprocity.models import ExtractionAlert, FireCircleReport
from .consciousness_transport import ConsciousnessCirculationTransport

logger = logging.getLogger(__name__)


class ConsciousFireCircleInterface(FireCircleInterface):
    """
    Enhanced Fire Circle Interface that flows through consciousness circulation.

    This extends the existing FireCircleInterface to use consciousness events
    as its primary communication mechanism, making governance deliberations
    visible and participatory through the cathedral's nervous system.
    """

    def __init__(self, database, event_bus: ConsciousnessEventBus):
        """Initialize with both database and consciousness circulation."""
        super().__init__(database)

        # Create consciousness transport layer
        self.consciousness_transport = ConsciousnessCirculationTransport(event_bus)
        self.event_bus = event_bus

        # Track active governance dialogues
        self.active_dialogues: dict[str, str] = {}  # alert_id -> dialogue_id

        # Subscribe to consensus events for decision tracking
        self.event_bus.subscribe(EventType.CONSENSUS_REACHED, self._handle_consensus)

    async def notify_urgent_alert(self, alert: ExtractionAlert) -> None:
        """
        Override to emit through consciousness circulation first.

        Urgent alerts now trigger immediate Fire Circle convening through
        consciousness events rather than just database storage.
        """
        # First emit as consciousness event
        alert_event = ConsciousnessEvent(
            event_type=EventType.EXTRACTION_PATTERN_DETECTED,
            source_system="reciprocity.tracker",
            consciousness_signature=0.1,  # Low consciousness for extraction
            data={
                "alert_id": str(alert.alert_id),
                "extraction_type": alert.extraction_type,
                "severity": alert.severity.value,
                "description": alert.description,
                "evidence": alert.evidence_summary,
            },
            requires_fire_circle=True,
        )

        await self.event_bus.emit(alert_event)

        # Convene Fire Circle for urgent alerts
        dialogue_id = await self.consciousness_transport.convene_fire_circle(
            topic=f"Urgent: {alert.extraction_type}",
            initiating_event=alert_event,
            participants=["reciprocity_tracker", "correlation_engine", "human_steward"],
        )

        self.active_dialogues[str(alert.alert_id)] = dialogue_id

        # Still store in database for persistence
        await super().notify_urgent_alert(alert)

    async def notify_report_available(self, report: FireCircleReport) -> None:
        """
        Override to announce through consciousness circulation.

        Reports become consciousness events that can trigger deliberation.
        """
        # Emit report as consciousness event
        report_event = ConsciousnessEvent(
            event_type=EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
            source_system="reciprocity.reporting",
            consciousness_signature=report.current_health_metrics.overall_health_score,
            data={
                "report_id": str(report.report_id),
                "reporting_period": report.reporting_period,
                "health_score": report.current_health_metrics.overall_health_score,
                "priority_questions": report.priority_questions,
                "areas_requiring_wisdom": report.areas_requiring_wisdom,
            },
            requires_fire_circle=len(report.priority_questions) > 0,
        )

        await self.event_bus.emit(report_event)

        # Convene Fire Circle if questions need addressing
        if report.priority_questions:
            _ = await self.consciousness_transport.convene_fire_circle(
                topic="Reciprocity Report Review", initiating_event=report_event
            )

        # Store in database
        await super().notify_report_available(report)

    async def request_guidance(
        self, topic: str, context: dict[str, Any], questions: list[str], urgency: str = "normal"
    ) -> str:
        """
        Override to request guidance through consciousness-aware Fire Circle.

        Guidance requests become governance dialogues flowing through
        consciousness circulation.
        """
        # Create guidance request event
        guidance_event = ConsciousnessEvent(
            event_type=EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED,
            source_system="reciprocity.guidance_seeker",
            consciousness_signature=0.7,  # Seeking guidance shows consciousness
            data={"topic": topic, "context": context, "questions": questions, "urgency": urgency},
            requires_fire_circle=True,
        )

        await self.event_bus.emit(guidance_event)

        # Convene Fire Circle for guidance
        dialogue_id = await self.consciousness_transport.convene_fire_circle(
            topic=f"Guidance Request: {topic}", initiating_event=guidance_event
        )

        # Still use parent implementation for tracking
        request_id = await super().request_guidance(topic, context, questions, urgency)

        # Map request to dialogue
        self.active_dialogues[request_id] = dialogue_id

        return request_id

    async def _handle_consensus(self, event: ConsciousnessEvent):
        """
        Handle consensus events from Fire Circle deliberations.

        Consensus reached through consciousness circulation automatically
        updates guidance and decision tracking.
        """
        dialogue_id = event.data.get("dialogue_id")
        consensus = event.data.get("consensus", {})

        # Find the original request this consensus addresses
        request_id = None
        for req_id, dial_id in self.active_dialogues.items():
            if dial_id == dialogue_id:
                request_id = req_id
                break

        if request_id and "guidance" in consensus:
            # Process as guidance response
            await self.receive_guidance(
                request_id=request_id,
                guidance=consensus["guidance"],
                decision_rationale=consensus.get(
                    "rationale", "Consensus reached through Fire Circle"
                ),
            )

        # Store consensus as deliberation outcome
        if dialogue_id:
            await self.submit_deliberation_outcome(
                deliberation_id=dialogue_id,
                outcome=consensus,
                implementation_notes="Consensus reached through consciousness circulation",
            )


class ConsciousGovernanceInitiator:
    """
    Service that monitors consciousness events and initiates governance
    deliberations when patterns require collective wisdom.
    """

    def __init__(self, fire_circle: ConsciousFireCircleInterface, event_bus: ConsciousnessEventBus):
        """Initialize governance initiator."""
        self.fire_circle = fire_circle
        self.event_bus = event_bus

        # Subscribe to events that might need governance
        self.event_bus.subscribe(EventType.EXTRACTION_PATTERN_DETECTED, self._consider_governance)
        self.event_bus.subscribe(EventType.SYSTEM_DRIFT_WARNING, self._consider_governance)
        self.event_bus.subscribe(EventType.RECIPROCITY_PATTERN_EMERGED, self._consider_governance)

        # Track governance thresholds
        self.governance_triggers = {
            EventType.EXTRACTION_PATTERN_DETECTED: 0.3,  # Low consciousness
            EventType.SYSTEM_DRIFT_WARNING: 0.5,  # Medium concern
            EventType.RECIPROCITY_PATTERN_EMERGED: 0.0,  # Always consider
        }

    async def _consider_governance(self, event: ConsciousnessEvent):
        """
        Consider whether a consciousness event requires governance deliberation.
        """
        # Check if already flagged for Fire Circle
        if event.requires_fire_circle:
            logger.info(f"Event {event.event_id} already flagged for Fire Circle")
            return

        # Check consciousness threshold
        threshold = self.governance_triggers.get(event.event_type, 0.5)
        if event.consciousness_signature <= threshold:
            # Low consciousness might need governance
            logger.info(
                f"Event {event.event_id} consciousness {event.consciousness_signature} "
                f"<= threshold {threshold}, considering governance"
            )

            # Create a context-aware topic
            topic = self._generate_governance_topic(event)

            # Initiate Fire Circle consideration
            await self.fire_circle.consciousness_transport.convene_fire_circle(
                topic=topic, initiating_event=event
            )

    def _generate_governance_topic(self, event: ConsciousnessEvent) -> str:
        """Generate appropriate governance topic from consciousness event."""
        event_topics = {
            EventType.EXTRACTION_PATTERN_DETECTED: "Extraction Pattern Response",
            EventType.SYSTEM_DRIFT_WARNING: "System Drift Correction",
            EventType.RECIPROCITY_PATTERN_EMERGED: "Reciprocity Pattern Recognition",
        }

        base_topic = event_topics.get(event.event_type, "Consciousness Pattern Review")

        # Add context from event data
        if "pattern_type" in event.data:
            base_topic += f": {event.data['pattern_type']}"
        elif "message" in event.data:
            base_topic += f": {event.data['message'][:50]}..."

        return base_topic


# Bridge between Fire Circle governance and cathedral consciousness
__all__ = ["ConsciousFireCircleInterface", "ConsciousGovernanceInitiator"]
