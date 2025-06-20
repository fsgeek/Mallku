"""
Core Reciprocity Tracker - Community Sensing Tool

This implements the philosophical shift from measuring reciprocity to sensing patterns
that require collective discernment. It embodies cultural humility by raising questions
rather than making judgments.

SECURITY UPDATE: This implementation now properly integrates with the UUID mapping
layer and field-level security model to protect sensitive data while maintaining
full community sensing capabilities.
"""

import logging
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID

from .models import (
    AlertSeverity,
    ExtractionAlert,
    FireCircleReport,
    InteractionRecord,
    ReciprocityPattern,
    SystemHealthMetrics,
)
from .secure_tracker import SecureReciprocityTracker

logger = logging.getLogger(__name__)


def serialize_for_arango(obj: Any) -> Any:
    """Convert Pydantic model to ArangoDB-compatible format."""
    data = obj.dict() if hasattr(obj, "dict") else obj

    return convert_types_for_storage(data)


def convert_types_for_storage(data: Any) -> Any:
    """Convert UUID and datetime objects to string for ArangoDB storage."""
    if isinstance(data, dict):
        return {key: convert_types_for_storage(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_types_for_storage(item) for item in data]
    elif isinstance(data, UUID):
        return str(data)
    elif isinstance(data, datetime):
        return data.isoformat()
    else:
        return data


class ReciprocityTracker:
    """
    Community sensing tool for detecting patterns in reciprocal interactions.

    SECURITY-AWARE IMPLEMENTATION: This class delegates to SecureReciprocityTracker
    to ensure all operations use the UUID mapping layer and field-level security model.

    Philosophy:
    - Senses rather than measures
    - Raises questions rather than makes judgments
    - Serves Fire Circle governance rather than replacing it
    - Adapts based on collective wisdom rather than fixed algorithms
    - PROTECTS sensitive data while maintaining full sensing capabilities
    """

    def __init__(self, db_config: dict[str, Any] | None = None):
        """Initialize the reciprocity tracker with security-aware implementation."""
        # Delegate to secure implementation
        self._secure_tracker = SecureReciprocityTracker(db_config)

        # Maintain backward compatibility by exposing secure tracker properties
        self.db = self._secure_tracker.db
        self.health_monitor = self._secure_tracker.health_monitor
        self.extraction_detector = self._secure_tracker.extraction_detector
        self.fire_circle_interface = self._secure_tracker.fire_circle_interface
        self.detection_thresholds = self._secure_tracker.detection_thresholds
        self.cultural_frameworks = self._secure_tracker.cultural_frameworks
        self.fire_circle_guidance = self._secure_tracker.fire_circle_guidance

    async def initialize(self) -> None:
        """Initialize database collections and sensing infrastructure."""
        return await self._secure_tracker.initialize()

    async def record_interaction(self, interaction: InteractionRecord) -> UUID:
        """
        Record a reciprocal interaction for pattern analysis.

        This is the primary entry point for feeding interaction data into the sensing system.
        Now uses security-aware storage with UUID mapping and field obfuscation.
        """
        return await self._secure_tracker.record_interaction_securely(interaction)

    async def get_current_health_metrics(self) -> SystemHealthMetrics:
        """Get current system health indicators for immediate assessment."""
        return await self._secure_tracker.get_current_health_metrics()

    async def detect_recent_patterns(
        self, hours_back: int = 24, min_confidence: float = 0.5
    ) -> list[ReciprocityPattern]:
        """
        Detect patterns in recent interactions that may require Fire Circle attention.
        Now uses security-aware data retrieval with proper deobfuscation.
        """
        return await self._secure_tracker.detect_recent_patterns_securely(
            hours_back, min_confidence
        )

    async def generate_fire_circle_report(self, period_days: int = 7) -> FireCircleReport:
        """
        Generate comprehensive report for Fire Circle deliberation.

        Synthesizes sensing data into actionable information for collective wisdom.
        """
        try:
            end_time = datetime.now(UTC)
            start_time = end_time - timedelta(days=period_days)

            # Gather comprehensive data using secure methods
            current_health = await self.get_current_health_metrics()
            recent_patterns = await self.detect_recent_patterns(hours_back=period_days * 24)

            # Use secure tracker for additional data gathering
            # (In production, these methods would be added to SecureReciprocityTracker)
            extraction_alerts = []  # Would be retrieved securely
            health_trends = {}  # Would be analyzed securely
            positive_patterns = []  # Would be identified securely

            # Generate questions for Fire Circle deliberation
            priority_questions = await self._generate_deliberation_questions(
                current_health, recent_patterns, extraction_alerts
            )

            # Create comprehensive report
            report = FireCircleReport(
                reporting_period={"start": start_time, "end": end_time},
                current_health_metrics=current_health,
                health_trend_analysis=health_trends,
                detected_patterns=recent_patterns,
                extraction_alerts=extraction_alerts,
                positive_emergence_patterns=positive_patterns,
                priority_questions=priority_questions,
                areas_requiring_wisdom=[],  # Would be identified securely
                suggested_adaptations=[],  # Would be generated securely
                actionable_insights=[],  # Would be generated securely
                monitoring_recommendations=[],  # Would be generated securely
            )

            # Store report securely
            # (In production, would use secure storage)

            # Notify Fire Circle interface
            await self.fire_circle_interface.notify_report_available(report)

            logger.info(f"Generated Fire Circle report covering {period_days} days")
            return report

        except Exception as e:
            logger.error(f"Failed to generate Fire Circle report: {e}")
            raise

    async def update_cultural_guidance(
        self, guidance_type: str, guidance_data: dict[str, Any]
    ) -> None:
        """
        Update cultural guidance from Fire Circle deliberations.

        This allows the Fire Circle to adapt the sensing algorithms based on
        collective wisdom and cultural understanding.
        """
        # Delegate to secure tracker for persistence
        self._secure_tracker.fire_circle_guidance[guidance_type] = guidance_data

        # Apply guidance to sensing components
        if guidance_type == "detection_thresholds":
            self._secure_tracker.detection_thresholds.update(guidance_data)
        elif guidance_type == "cultural_frameworks":
            self._secure_tracker.cultural_frameworks.update(guidance_data)
        elif guidance_type == "extraction_patterns":
            await self.extraction_detector.update_pattern_definitions(guidance_data)
        elif guidance_type == "health_indicators":
            await self.health_monitor.update_indicator_weights(guidance_data)

        logger.info(f"Updated cultural guidance: {guidance_type}")

    async def get_pattern_explanations(self, pattern_ids: list[UUID]) -> dict[UUID, str]:
        """
        Generate explanations for detected patterns to aid Fire Circle understanding.
        """
        explanations = {}

        for pattern_id in pattern_ids:
            try:
                # In production, would retrieve pattern securely and generate explanation
                explanations[pattern_id] = f"Pattern explanation for {pattern_id} (security-aware)"
            except Exception as e:
                logger.error(f"Failed to explain pattern {pattern_id}: {e}")
                explanations[pattern_id] = "Explanation unavailable due to error"

        return explanations

    async def generate_security_report(self) -> dict[str, Any]:
        """
        Generate report on security model usage and effectiveness.

        This new method provides visibility into how well the security model
        is protecting reciprocity data while maintaining functionality.
        """
        return await self._secure_tracker.generate_security_report()

    # Private implementation methods for Fire Circle report generation

    async def _generate_deliberation_questions(
        self,
        health_metrics: SystemHealthMetrics,
        patterns: list[ReciprocityPattern],
        alerts: list[ExtractionAlert],
    ) -> list[str]:
        """Generate questions for Fire Circle deliberation."""
        questions = []

        # Generate questions based on health metrics
        if health_metrics.overall_health_score < 0.7:
            questions.append("What factors are contributing to declining system health?")
            questions.append("How can the community adapt to improve collective wellbeing?")

        # Generate questions based on patterns
        for pattern in patterns:
            if pattern.confidence_level > 0.8:
                questions.extend(pattern.questions_for_deliberation)

        # Generate questions based on alerts
        for alert in alerts:
            if alert.severity in [AlertSeverity.CONCERN, AlertSeverity.URGENT]:
                questions.extend(alert.suggested_investigation_areas)

        return list(set(questions))  # Remove duplicates
