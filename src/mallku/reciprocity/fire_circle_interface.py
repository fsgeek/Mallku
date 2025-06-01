"""
Fire Circle Interface - Collective Governance Integration

Provides interface between reciprocity sensing algorithms and Fire Circle
collective governance processes. Embodies cultural humility by serving
rather than replacing human wisdom and collective discernment.
"""

import asyncio
import logging
from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID

from .models import ExtractionAlert, FireCircleReport, ReciprocityPattern


def convert_datetime_for_storage(data: Any) -> Any:
    """Convert datetime objects to string for storage."""
    if isinstance(data, dict):
        return {key: convert_datetime_for_storage(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_datetime_for_storage(item) for item in data]
    elif isinstance(data, datetime):
        return data.isoformat()
    elif isinstance(data, UUID):
        return str(data)
    else:
        return data

logger = logging.getLogger(__name__)


class FireCircleInterface:
    """
    Interface between technical sensing and collective governance wisdom.

    Philosophy:
    - Serves Fire Circle deliberation rather than replacing it
    - Provides information, not decisions
    - Enables cultural adaptation of technical frameworks
    - Maintains transparency and accountability
    - Supports dynamic equilibrium through adaptive governance
    """

    def __init__(self, database):
        """Initialize Fire Circle interface with database connection."""
        self.db = database

        # Notification callbacks (registered by Fire Circle participants)
        self.notification_callbacks = {
            'urgent_alert': [],
            'report_available': [],
            'pattern_detected': [],
            'health_change': []
        }

        # Governance state tracking
        self.pending_deliberations = {}
        self.governance_decisions = {}
        self.cultural_guidance = {}

        # Communication channels
        self.communication_channels = {
            'alerts': [],  # Real-time alerts
            'reports': [], # Periodic reports
            'patterns': [], # Pattern notifications
            'requests': [] # Requests for guidance
        }

        # Decision tracking for algorithmic adaptation
        self.decision_history = []
        self.guidance_effectiveness = {}

    async def initialize(self) -> None:
        """Initialize Fire Circle interface infrastructure."""
        try:
            # Ensure governance collections exist
            collections = [
                'fire_circle_deliberations',
                'governance_decisions',
                'cultural_guidance',
                'deliberation_requests'
            ]

            for collection_name in collections:
                if not self.db.has_collection(collection_name):
                    self.db.create_collection(collection_name)

            # Load existing governance decisions
            await self._load_governance_decisions()

            # Load cultural guidance
            await self._load_cultural_guidance()

            logger.info("Fire Circle interface initialized")

        except Exception as e:
            logger.error(f"Failed to initialize Fire Circle interface: {e}")
            raise

    async def notify_urgent_alert(self, alert: ExtractionAlert) -> None:
        """
        Notify Fire Circle of urgent extraction alert requiring immediate attention.
        """
        try:
            # Create deliberation request
            request = {
                'type': 'urgent_alert',
                'alert_id': str(alert.alert_id),
                'severity': alert.severity.value,
                'extraction_type': alert.extraction_type,
                'description': alert.description,
                'evidence': alert.evidence_summary,
                'suggested_investigations': alert.suggested_investigation_areas,
                'urgency_factors': alert.urgency_factors,
                'timestamp': datetime.now(UTC),
                'status': 'pending_review'
            }

            # Store request for Fire Circle review
            await self._store_deliberation_request(convert_datetime_for_storage(request))

            # Notify registered callbacks
            await self._trigger_callbacks('urgent_alert', alert)

            logger.warning(f"Urgent alert sent to Fire Circle: {alert.extraction_type}")

        except Exception as e:
            logger.error(f"Failed to notify urgent alert: {e}")

    async def notify_report_available(self, report: FireCircleReport) -> None:
        """
        Notify Fire Circle that new comprehensive report is available for review.
        """
        try:
            # Create report notification
            notification = {
                'type': 'report_available',
                'report_id': str(report.report_id),
                'reporting_period': report.reporting_period,
                'health_score': report.current_health_metrics.overall_health_score,
                'priority_questions': report.priority_questions,
                'areas_requiring_wisdom': report.areas_requiring_wisdom,
                'timestamp': datetime.now(UTC),
                'status': 'available_for_review'
            }

            # Store notification
            await self._store_report_notification(convert_datetime_for_storage(notification))

            # Notify registered callbacks
            await self._trigger_callbacks('report_available', report)

            logger.info(f"Fire Circle report notification sent: {report.report_id}")

        except Exception as e:
            logger.error(f"Failed to notify report available: {e}")

    async def notify_pattern_detected(
        self,
        pattern: ReciprocityPattern,
        requires_deliberation: bool = False
    ) -> None:
        """
        Notify Fire Circle of detected pattern that may require attention.
        """
        try:
            notification = {
                'type': 'pattern_detected',
                'pattern_id': str(pattern.pattern_id),
                'pattern_type': pattern.pattern_type,
                'confidence_level': pattern.confidence_level,
                'description': pattern.pattern_description,
                'questions_for_deliberation': pattern.questions_for_deliberation,
                'requires_deliberation': requires_deliberation,
                'timestamp': datetime.now(UTC),
                'status': 'informational' if not requires_deliberation else 'requires_review'
            }

            await self._store_pattern_notification(convert_datetime_for_storage(notification))

            # Only trigger callbacks for patterns requiring attention
            if requires_deliberation or pattern.confidence_level > 0.8:
                await self._trigger_callbacks('pattern_detected', pattern)

            logger.info(f"Pattern notification: {pattern.pattern_type}")

        except Exception as e:
            logger.error(f"Failed to notify pattern detected: {e}")

    async def request_guidance(
        self,
        topic: str,
        context: dict[str, Any],
        questions: list[str],
        urgency: str = "normal"
    ) -> str:
        """
        Request Fire Circle guidance on specific reciprocity question.

        Returns request ID for tracking response.
        """
        try:
            request_id = f"guidance_{int(datetime.now(UTC).timestamp())}"

            guidance_request = {
                'request_id': request_id,
                'topic': topic,
                'context': context,
                'questions': questions,
                'urgency': urgency,
                'requested_timestamp': datetime.now(UTC),
                'status': 'pending_deliberation',
                'requester': 'reciprocity_tracker'
            }

            # Store request
            await self._store_guidance_request(convert_datetime_for_storage(guidance_request))

            # Notify Fire Circle
            await self._trigger_callbacks('guidance_request', guidance_request)

            logger.info(f"Guidance request submitted: {topic}")
            return request_id

        except Exception as e:
            logger.error(f"Failed to request guidance: {e}")
            raise

    async def receive_guidance(
        self,
        request_id: str,
        guidance: dict[str, Any],
        decision_rationale: str
    ) -> None:
        """
        Receive guidance from Fire Circle deliberation.

        This is the primary mechanism for Fire Circle to adapt algorithmic behavior.
        """
        try:
            guidance_response = {
                'request_id': request_id,
                'guidance': guidance,
                'decision_rationale': decision_rationale,
                'deliberation_timestamp': datetime.now(UTC),
                'status': 'guidance_provided'
            }

            # Store guidance
            await self._store_guidance_response(guidance_response)

            # Apply guidance to sensing systems
            await self._apply_guidance(guidance)

            # Track guidance effectiveness
            await self._track_guidance_effectiveness(request_id, guidance)

            logger.info(f"Guidance received and applied: {request_id}")

        except Exception as e:
            logger.error(f"Failed to receive guidance: {e}")
            raise

    async def submit_deliberation_outcome(
        self,
        deliberation_id: str,
        outcome: dict[str, Any],
        implementation_notes: str
    ) -> None:
        """
        Receive outcome from Fire Circle deliberation for tracking and learning.
        """
        try:
            outcome_record = {
                'deliberation_id': deliberation_id,
                'outcome': outcome,
                'implementation_notes': implementation_notes,
                'timestamp': datetime.now(UTC),
                'participants': outcome.get('participants', []),
                'consensus_level': outcome.get('consensus_level', 'unknown')
            }

            # Store outcome
            await self._store_deliberation_outcome(outcome_record)

            # Learn from outcome for future sensing
            await self._learn_from_outcome(outcome_record)

            logger.info(f"Deliberation outcome recorded: {deliberation_id}")

        except Exception as e:
            logger.error(f"Failed to submit deliberation outcome: {e}")

    async def register_callback(
        self,
        event_type: str,
        callback: Callable
    ) -> None:
        """
        Register callback function for Fire Circle notifications.

        Allows Fire Circle participants to receive real-time notifications.
        """
        try:
            if event_type in self.notification_callbacks:
                self.notification_callbacks[event_type].append(callback)
                logger.info(f"Registered callback for {event_type}")
            else:
                raise ValueError(f"Unknown event type: {event_type}")

        except Exception as e:
            logger.error(f"Failed to register callback: {e}")
            raise

    async def get_pending_deliberations(self) -> list[dict[str, Any]]:
        """
        Get list of deliberations pending Fire Circle attention.
        """
        try:
            # Query pending deliberations from database
            pending = await self._query_pending_deliberations()

            # Sort by urgency and timestamp
            sorted_pending = sorted(
                pending,
                key=lambda x: (
                    x.get('urgency', 'normal') == 'urgent',
                    x.get('timestamp', datetime.min.replace(tzinfo=UTC))
                ),
                reverse=True
            )

            return sorted_pending

        except Exception as e:
            logger.error(f"Failed to get pending deliberations: {e}")
            return []

    async def get_guidance_history(
        self,
        topic: str | None = None,
        days_back: int = 30
    ) -> list[dict[str, Any]]:
        """
        Get history of Fire Circle guidance for learning and reference.
        """
        try:
            end_time = datetime.now(UTC)
            start_time = end_time - timedelta(days=days_back)

            guidance_history = await self._query_guidance_history(topic, start_time, end_time)

            return guidance_history

        except Exception as e:
            logger.error(f"Failed to get guidance history: {e}")
            return []

    async def evaluate_guidance_effectiveness(self, guidance_id: str) -> dict[str, Any]:
        """
        Evaluate effectiveness of previous Fire Circle guidance.
        """
        try:
            effectiveness = await self._evaluate_guidance_impact(guidance_id)

            return {
                'guidance_id': guidance_id,
                'effectiveness_score': effectiveness.get('score', 0.5),
                'impact_indicators': effectiveness.get('indicators', {}),
                'lessons_learned': effectiveness.get('lessons', []),
                'recommendations': effectiveness.get('recommendations', [])
            }

        except Exception as e:
            logger.error(f"Failed to evaluate guidance effectiveness: {e}")
            return {'error': str(e)}

    # Private implementation methods

    async def _trigger_callbacks(self, event_type: str, data: Any) -> None:
        """Trigger registered callbacks for event type."""
        try:
            callbacks = self.notification_callbacks.get(event_type, [])

            # Execute callbacks asynchronously
            tasks = []
            for callback in callbacks:
                if asyncio.iscoroutinefunction(callback):
                    tasks.append(callback(data))
                else:
                    tasks.append(asyncio.create_task(asyncio.to_thread(callback, data)))

            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)

        except Exception as e:
            logger.error(f"Error triggering callbacks for {event_type}: {e}")

    async def _store_deliberation_request(self, request: dict[str, Any]) -> None:
        """Store deliberation request in database."""
        try:
            collection = self.db.collection('deliberation_requests')
            collection.insert(request)

        except Exception as e:
            logger.error(f"Failed to store deliberation request: {e}")

    async def _store_report_notification(self, notification: dict[str, Any]) -> None:
        """Store report notification in database."""
        try:
            collection = self.db.collection('fire_circle_notifications')
            collection.insert(notification)

        except Exception as e:
            logger.error(f"Failed to store report notification: {e}")

    async def _store_pattern_notification(self, notification: dict[str, Any]) -> None:
        """Store pattern notification in database."""
        try:
            collection = self.db.collection('fire_circle_notifications')
            collection.insert(notification)

        except Exception as e:
            logger.error(f"Failed to store pattern notification: {e}")

    async def _store_guidance_request(self, request: dict[str, Any]) -> None:
        """Store guidance request in database."""
        try:
            collection = self.db.collection('guidance_requests')
            collection.insert(request)

        except Exception as e:
            logger.error(f"Failed to store guidance request: {e}")

    async def _store_guidance_response(self, response: dict[str, Any]) -> None:
        """Store guidance response in database."""
        try:
            collection = self.db.collection('guidance_responses')
            collection.insert(response)

        except Exception as e:
            logger.error(f"Failed to store guidance response: {e}")

    async def _store_deliberation_outcome(self, outcome: dict[str, Any]) -> None:
        """Store deliberation outcome in database."""
        try:
            collection = self.db.collection('deliberation_outcomes')
            collection.insert(outcome)

        except Exception as e:
            logger.error(f"Failed to store deliberation outcome: {e}")

    async def _load_governance_decisions(self) -> None:
        """Load existing governance decisions from database."""
        try:
            # Implementation would load decisions and apply them
            self.governance_decisions = {}

        except Exception as e:
            logger.error(f"Failed to load governance decisions: {e}")

    async def _load_cultural_guidance(self) -> None:
        """Load existing cultural guidance from database."""
        try:
            # Implementation would load cultural frameworks
            self.cultural_guidance = {}

        except Exception as e:
            logger.error(f"Failed to load cultural guidance: {e}")

    async def _apply_guidance(self, guidance: dict[str, Any]) -> None:
        """Apply Fire Circle guidance to sensing algorithms."""
        try:
            # This would update detection thresholds, pattern definitions, etc.
            # based on Fire Circle decisions
            pass

        except Exception as e:
            logger.error(f"Failed to apply guidance: {e}")

    async def _track_guidance_effectiveness(
        self,
        request_id: str,
        guidance: dict[str, Any]
    ) -> None:
        """Track effectiveness of applied guidance."""
        try:
            # Implementation would monitor how guidance affects system behavior
            pass

        except Exception as e:
            logger.error(f"Failed to track guidance effectiveness: {e}")

    async def _learn_from_outcome(self, outcome: dict[str, Any]) -> None:
        """Learn from deliberation outcome to improve future sensing."""
        try:
            # Implementation would adjust algorithms based on Fire Circle decisions
            pass

        except Exception as e:
            logger.error(f"Failed to learn from outcome: {e}")

    async def _query_pending_deliberations(self) -> list[dict[str, Any]]:
        """Query pending deliberations from database."""
        try:
            # Implementation would query database for pending items
            return []

        except Exception as e:
            logger.error(f"Failed to query pending deliberations: {e}")
            return []

    async def _query_guidance_history(
        self,
        topic: str | None,
        start_time: datetime,
        end_time: datetime
    ) -> list[dict[str, Any]]:
        """Query guidance history from database."""
        try:
            # Implementation would query guidance history
            return []

        except Exception as e:
            logger.error(f"Failed to query guidance history: {e}")
            return []

    async def _evaluate_guidance_impact(self, guidance_id: str) -> dict[str, Any]:
        """Evaluate impact of specific guidance."""
        try:
            # Implementation would analyze guidance effectiveness
            return {}

        except Exception as e:
            logger.error(f"Failed to evaluate guidance impact: {e}")
            return {}
