"""
Core Reciprocity Tracker - Community Sensing Tool

This implements the philosophical shift from measuring reciprocity to sensing patterns
that require collective discernment. It embodies cultural humility by raising questions
rather than making judgments.
"""

import logging
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID

from ..core.database import get_database
from .extraction_detector import ExtractionDetector
from .fire_circle_interface import FireCircleInterface
from .health_monitor import SystemHealthMonitor
from .models import (
    AlertSeverity,
    ExtractionAlert,
    FireCircleReport,
    InteractionRecord,
    ReciprocityPattern,
    SystemHealthMetrics,
)

logger = logging.getLogger(__name__)


def serialize_for_arango(obj: Any) -> Any:
    """Convert Pydantic model to ArangoDB-compatible format."""
    data = obj.dict() if hasattr(obj, 'dict') else obj

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

    Philosophy:
    - Senses rather than measures
    - Raises questions rather than makes judgments
    - Serves Fire Circle governance rather than replacing it
    - Adapts based on collective wisdom rather than fixed algorithms
    """

    def __init__(self, db_config: dict[str, Any] | None = None):
        """Initialize the reciprocity tracker with sensing components."""
        self.db = get_database() if db_config is None else get_database(db_config)

        # Core sensing components
        self.health_monitor = SystemHealthMonitor(self.db)
        self.extraction_detector = ExtractionDetector(self.db)
        self.fire_circle_interface = FireCircleInterface(self.db)

        # Pattern detection state
        self.interaction_buffer: list[InteractionRecord] = []
        self.pattern_detection_interval = timedelta(hours=1)
        self.last_pattern_analysis = datetime.now(UTC)

        # Adaptive thresholds (modifiable by Fire Circle)
        self.detection_thresholds = {
            'participation_anomaly': 0.3,
            'resource_flow_anomaly': 0.4,
            'extraction_concern': 0.6,
            'system_health_decline': 0.7
        }

        # Cultural adaptation interface
        self.cultural_frameworks = {}
        self.fire_circle_guidance = {}

    async def initialize(self) -> None:
        """Initialize database collections and sensing infrastructure."""
        try:
            # Ensure collections exist
            collections = [
                'reciprocity_interactions',
                'reciprocity_patterns',
                'reciprocity_alerts',
                'system_health_snapshots',
                'fire_circle_reports'
            ]

            for collection_name in collections:
                if not self.db.has_collection(collection_name):
                    self.db.create_collection(collection_name)
                    logger.info(f"Created collection: {collection_name}")

            # Initialize sensing components
            await self.health_monitor.initialize()
            await self.extraction_detector.initialize()
            await self.fire_circle_interface.initialize()

            # Load any existing Fire Circle guidance
            await self._load_fire_circle_guidance()

            logger.info("Reciprocity tracker initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize reciprocity tracker: {e}")
            raise

    async def record_interaction(self, interaction: InteractionRecord) -> None:
        """
        Record a reciprocal interaction for pattern analysis.

        This is the primary entry point for feeding interaction data into the sensing system.
        """
        try:
            # Store in database
            interaction_doc = serialize_for_arango(interaction)
            interaction_doc['_key'] = str(interaction.interaction_id)

            collection = self.db.collection('reciprocity_interactions')
            collection.insert(interaction_doc)

            # Add to buffer for real-time pattern detection
            self.interaction_buffer.append(interaction)

            # Update real-time health indicators
            await self.health_monitor.update_interaction_metrics(interaction)

            # Check for immediate extraction concerns
            extraction_alerts = await self.extraction_detector.analyze_interaction(interaction)
            for alert in extraction_alerts:
                await self._handle_extraction_alert(alert)

            # Periodic pattern analysis
            if self._should_run_pattern_analysis():
                await self._run_pattern_analysis()

            logger.debug(f"Recorded interaction: {interaction.interaction_type}")

        except Exception as e:
            logger.error(f"Failed to record interaction: {e}")
            raise

    async def get_current_health_metrics(self) -> SystemHealthMetrics:
        """Get current system health indicators for immediate assessment."""
        return await self.health_monitor.get_current_metrics()

    async def detect_recent_patterns(
        self,
        hours_back: int = 24,
        min_confidence: float = 0.5
    ) -> list[ReciprocityPattern]:
        """
        Detect patterns in recent interactions that may require Fire Circle attention.
        """
        try:
            end_time = datetime.now(UTC)
            start_time = end_time - timedelta(hours=hours_back)

            # Get recent interactions
            interactions = await self._get_interactions_in_timeframe(start_time, end_time)

            # Analyze patterns using multiple detection methods
            patterns = []

            # Participation pattern analysis
            participation_patterns = await self._analyze_participation_patterns(interactions)
            patterns.extend(participation_patterns)

            # Resource flow pattern analysis
            resource_patterns = await self._analyze_resource_flow_patterns(interactions)
            patterns.extend(resource_patterns)

            # Temporal pattern analysis
            temporal_patterns = await self._analyze_temporal_patterns(interactions)
            patterns.extend(temporal_patterns)

            # Filter by confidence threshold
            significant_patterns = [p for p in patterns if p.confidence_level >= min_confidence]

            # Store detected patterns
            for pattern in significant_patterns:
                await self._store_pattern(pattern)

            logger.info(f"Detected {len(significant_patterns)} significant patterns")
            return significant_patterns

        except Exception as e:
            logger.error(f"Failed to detect patterns: {e}")
            return []

    async def generate_fire_circle_report(
        self,
        period_days: int = 7
    ) -> FireCircleReport:
        """
        Generate comprehensive report for Fire Circle deliberation.

        Synthesizes sensing data into actionable information for collective wisdom.
        """
        try:
            end_time = datetime.now(UTC)
            start_time = end_time - timedelta(days=period_days)

            # Gather comprehensive data
            current_health = await self.get_current_health_metrics()
            recent_patterns = await self.detect_recent_patterns(hours_back=period_days * 24)
            extraction_alerts = await self._get_recent_extraction_alerts(period_days)

            # Analyze trends and changes
            health_trends = await self._analyze_health_trends(period_days)
            positive_patterns = await self._identify_positive_emergence_patterns(recent_patterns)

            # Generate questions for Fire Circle deliberation
            priority_questions = await self._generate_deliberation_questions(
                current_health, recent_patterns, extraction_alerts
            )

            # Create comprehensive report
            report = FireCircleReport(
                reporting_period={
                    'start': start_time,
                    'end': end_time
                },
                current_health_metrics=current_health,
                health_trend_analysis=health_trends,
                detected_patterns=recent_patterns,
                extraction_alerts=extraction_alerts,
                positive_emergence_patterns=positive_patterns,
                priority_questions=priority_questions,
                areas_requiring_wisdom=await self._identify_wisdom_areas(recent_patterns),
                suggested_adaptations=await self._suggest_adaptations(current_health, recent_patterns),
                actionable_insights=await self._generate_actionable_insights(recent_patterns),
                monitoring_recommendations=await self._generate_monitoring_recommendations(recent_patterns)
            )

            # Store report for historical analysis
            await self._store_fire_circle_report(report)

            # Notify Fire Circle interface
            await self.fire_circle_interface.notify_report_available(report)

            logger.info(f"Generated Fire Circle report covering {period_days} days")
            return report

        except Exception as e:
            logger.error(f"Failed to generate Fire Circle report: {e}")
            raise

    async def update_cultural_guidance(
        self,
        guidance_type: str,
        guidance_data: dict[str, Any]
    ) -> None:
        """
        Update cultural guidance from Fire Circle deliberations.

        This allows the Fire Circle to adapt the sensing algorithms based on
        collective wisdom and cultural understanding.
        """
        try:
            self.fire_circle_guidance[guidance_type] = guidance_data

            # Apply guidance to sensing components
            if guidance_type == 'detection_thresholds':
                self.detection_thresholds.update(guidance_data)
            elif guidance_type == 'cultural_frameworks':
                self.cultural_frameworks.update(guidance_data)
            elif guidance_type == 'extraction_patterns':
                await self.extraction_detector.update_pattern_definitions(guidance_data)
            elif guidance_type == 'health_indicators':
                await self.health_monitor.update_indicator_weights(guidance_data)

            # Store guidance for persistence
            await self._store_cultural_guidance(guidance_type, guidance_data)

            logger.info(f"Updated cultural guidance: {guidance_type}")

        except Exception as e:
            logger.error(f"Failed to update cultural guidance: {e}")
            raise

    async def get_pattern_explanations(self, pattern_ids: list[UUID]) -> dict[UUID, str]:
        """
        Generate explanations for detected patterns to aid Fire Circle understanding.
        """
        explanations = {}

        for pattern_id in pattern_ids:
            try:
                pattern = await self._get_pattern_by_id(pattern_id)
                if pattern:
                    explanation = await self._generate_pattern_explanation(pattern)
                    explanations[pattern_id] = explanation
            except Exception as e:
                logger.error(f"Failed to explain pattern {pattern_id}: {e}")
                explanations[pattern_id] = "Explanation unavailable due to error"

        return explanations

    # Private implementation methods

    def _should_run_pattern_analysis(self) -> bool:
        """Determine if it's time to run comprehensive pattern analysis."""
        time_since_last = datetime.now(UTC) - self.last_pattern_analysis
        return (time_since_last >= self.pattern_detection_interval or
                len(self.interaction_buffer) >= 50)

    async def _run_pattern_analysis(self) -> None:
        """Run comprehensive pattern analysis on buffered interactions."""
        try:
            if not self.interaction_buffer:
                return

            # Analyze buffered interactions
            patterns = []

            # Real-time pattern detection methods
            participation_patterns = await self._analyze_participation_patterns(self.interaction_buffer)
            patterns.extend(participation_patterns)

            # Store significant patterns
            for pattern in patterns:
                if pattern.confidence_level >= self.detection_thresholds.get('pattern_significance', 0.6):
                    await self._store_pattern(pattern)

            # Clear buffer and update timestamp
            self.interaction_buffer.clear()
            self.last_pattern_analysis = datetime.now(UTC)

        except Exception as e:
            logger.error(f"Pattern analysis failed: {e}")

    async def _get_interactions_in_timeframe(
        self,
        start_time: datetime,
        end_time: datetime
    ) -> list[InteractionRecord]:
        """Retrieve interactions within specified timeframe."""
        try:
            aql_query = """
            FOR interaction IN @@collection
                FILTER interaction.timestamp >= @start_time
                   AND interaction.timestamp <= @end_time
                SORT interaction.timestamp DESC
                RETURN interaction
            """

            cursor = self.db.aql.execute(
                aql_query,
                bind_vars={
                    '@collection': 'reciprocity_interactions',
                    'start_time': start_time.isoformat(),
                    'end_time': end_time.isoformat()
                }
            )

            interactions = []
            for doc in cursor:
                # Remove ArangoDB metadata
                doc.pop('_key', None)
                doc.pop('_id', None)
                doc.pop('_rev', None)
                interactions.append(InteractionRecord(**doc))

            return interactions

        except Exception as e:
            logger.error(f"Failed to retrieve interactions: {e}")
            return []

    async def _analyze_participation_patterns(
        self,
        interactions: list[InteractionRecord]
    ) -> list[ReciprocityPattern]:
        """Analyze participation patterns for anomalies."""
        # Implementation would analyze participation rates, frequency changes,
        # new participant integration, participant departure patterns
        # This is a placeholder for the sophisticated pattern analysis
        return []

    async def _analyze_resource_flow_patterns(
        self,
        interactions: list[InteractionRecord]
    ) -> list[ReciprocityPattern]:
        """Analyze resource flow patterns for imbalances."""
        # Implementation would analyze resource allocation, hoarding patterns,
        # resource scarcity indicators, abundance distribution
        return []

    async def _analyze_temporal_patterns(
        self,
        interactions: list[InteractionRecord]
    ) -> list[ReciprocityPattern]:
        """Analyze temporal patterns in reciprocal exchanges."""
        # Implementation would analyze timing patterns, cyclical behaviors,
        # response time distributions, temporal clustering
        return []

    async def _handle_extraction_alert(self, alert: ExtractionAlert) -> None:
        """Handle extraction alert by storing and potentially notifying Fire Circle."""
        try:
            # Store alert
            alert_doc = alert.dict()
            alert_doc['_key'] = str(alert.alert_id)

            collection = self.db.collection('reciprocity_alerts')
            collection.insert(alert_doc)

            # Notify Fire Circle for urgent alerts
            if alert.severity == AlertSeverity.URGENT:
                await self.fire_circle_interface.notify_urgent_alert(alert)

            logger.warning(f"Extraction alert: {alert.extraction_type}")

        except Exception as e:
            logger.error(f"Failed to handle extraction alert: {e}")

    async def _store_pattern(self, pattern: ReciprocityPattern) -> None:
        """Store detected pattern in database."""
        try:
            pattern_doc = serialize_for_arango(pattern)
            pattern_doc['_key'] = str(pattern.pattern_id)

            collection = self.db.collection('reciprocity_patterns')
            collection.insert(pattern_doc)

        except Exception as e:
            logger.error(f"Failed to store pattern: {e}")

    async def _store_fire_circle_report(self, report: FireCircleReport) -> None:
        """Store Fire Circle report for historical analysis."""
        try:
            report_doc = serialize_for_arango(report)
            report_doc['_key'] = str(report.report_id)

            collection = self.db.collection('fire_circle_reports')
            collection.insert(report_doc)

        except Exception as e:
            logger.error(f"Failed to store Fire Circle report: {e}")

    async def _load_fire_circle_guidance(self) -> None:
        """Load existing Fire Circle guidance from database."""
        # Implementation would load stored cultural guidance and apply it
        pass

    async def _store_cultural_guidance(
        self,
        guidance_type: str,
        guidance_data: dict[str, Any]
    ) -> None:
        """Store cultural guidance for persistence."""
        # Implementation would store guidance in database for future sessions
        pass

    async def _get_recent_extraction_alerts(self, days_back: int) -> list[ExtractionAlert]:
        """Get recent extraction alerts for reporting."""
        # Implementation would retrieve alerts from specified time period
        return []

    async def _analyze_health_trends(self, days_back: int) -> dict[str, Any]:
        """Analyze health trends over specified period."""
        # Implementation would analyze health metric changes over time
        return {}

    async def _identify_positive_emergence_patterns(
        self,
        patterns: list[ReciprocityPattern]
    ) -> list[dict[str, Any]]:
        """Identify positive emergence patterns from detected patterns."""
        # Implementation would filter for positive, innovative, or flourishing patterns
        return []

    async def _generate_deliberation_questions(
        self,
        health_metrics: SystemHealthMetrics,
        patterns: list[ReciprocityPattern],
        alerts: list[ExtractionAlert]
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

    async def _identify_wisdom_areas(self, patterns: list[ReciprocityPattern]) -> list[str]:
        """Identify areas requiring Fire Circle wisdom."""
        # Implementation would analyze patterns to identify areas needing human wisdom
        return []

    async def _suggest_adaptations(
        self,
        health_metrics: SystemHealthMetrics,
        patterns: list[ReciprocityPattern]
    ) -> list[str]:
        """Suggest potential adaptations based on sensing data."""
        # Implementation would generate adaptation suggestions
        return []

    async def _generate_actionable_insights(self, patterns: list[ReciprocityPattern]) -> list[str]:
        """Generate actionable insights from pattern analysis."""
        # Implementation would create specific actionable recommendations
        return []

    async def _generate_monitoring_recommendations(self, patterns: list[ReciprocityPattern]) -> list[str]:
        """Generate monitoring recommendations for ongoing sensing."""
        # Implementation would suggest areas for enhanced monitoring
        return []

    async def _get_pattern_by_id(self, pattern_id: UUID) -> ReciprocityPattern | None:
        """Retrieve pattern by ID from database."""
        # Implementation would fetch pattern from database
        return None

    async def _generate_pattern_explanation(self, pattern: ReciprocityPattern) -> str:
        """Generate human-readable explanation of detected pattern."""
        # Implementation would create clear explanation of pattern for Fire Circle
        return f"Pattern explanation for {pattern.pattern_type}: {pattern.pattern_description}"
