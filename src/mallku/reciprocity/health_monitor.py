"""
System Health Monitor - Macroscopic Wellbeing Sensing

Tracks system-wide indicators of collective health and dynamic equilibrium
rather than individual transaction measurements. Focuses on the overall
ecosystem's ability to sustain reciprocal relationships.
"""

import logging
from datetime import UTC, datetime, timedelta
from statistics import mean, stdev
from typing import Any

from .models import (
    HealthIndicator,
    InteractionRecord,
    NeedCategory,
    SystemHealthMetrics,
)

logger = logging.getLogger(__name__)


class SystemHealthMonitor:
    """
    Monitors macroscopic indicators of system health and collective wellbeing.

    Philosophy:
    - Health is measured at the ecosystem level, not individual transaction level
    - Dynamic equilibrium is healthy; static balance may indicate stagnation
    - Looks for signs of flourishing vs. signs of stress or extraction
    - Adapts health indicators based on Fire Circle guidance
    """

    def __init__(self, database):
        """Initialize health monitor with database connection."""
        self.db = database

        # Health indicator weights (modifiable by Fire Circle)
        self.indicator_weights = {
            HealthIndicator.PARTICIPATION_RATE: 0.15,
            HealthIndicator.SATISFACTION_TRENDS: 0.20,
            HealthIndicator.RESOURCE_ABUNDANCE: 0.15,
            HealthIndicator.CONFLICT_RESOLUTION: 0.10,
            HealthIndicator.INNOVATION_EMERGENCE: 0.10,
            HealthIndicator.VOLUNTARY_RETURN: 0.15,
            HealthIndicator.CAPACITY_UTILIZATION: 0.10,
            HealthIndicator.NEED_FULFILLMENT: 0.05
        }

        # Baseline metrics for comparison
        self.baseline_metrics = {}

        # Real-time metric cache
        self.metric_cache = {}
        self.cache_update_interval = timedelta(minutes=15)
        self.last_cache_update = datetime.min.replace(tzinfo=UTC)

    async def initialize(self) -> None:
        """Initialize health monitoring infrastructure."""
        try:
            # Ensure health snapshots collection exists
            if not self.db.has_collection('system_health_snapshots'):
                self.db.create_collection('system_health_snapshots')

            # Load or establish baseline metrics
            await self._establish_baseline_metrics()

            logger.info("System health monitor initialized")

        except Exception as e:
            logger.error(f"Failed to initialize health monitor: {e}")
            raise

    async def get_current_metrics(self) -> SystemHealthMetrics:
        """
        Get current system health metrics with real-time calculation.
        """
        try:
            # Check if cache needs updating
            if self._should_update_cache():
                await self._update_metric_cache()

            end_time = datetime.now(UTC)
            start_time = end_time - timedelta(days=7)  # Week-long measurement period

            # Calculate comprehensive health metrics
            metrics = SystemHealthMetrics(
                measurement_period_start=start_time,
                measurement_period_end=end_time,
                snapshot_timestamp=end_time
            )

            # Populate participation and engagement metrics
            await self._calculate_participation_metrics(metrics, start_time, end_time)

            # Populate capacity and resource metrics
            await self._calculate_capacity_metrics(metrics, start_time, end_time)

            # Populate adaptation and resilience metrics
            await self._calculate_adaptation_metrics(metrics, start_time, end_time)

            # Populate quality of life metrics
            await self._calculate_quality_metrics(metrics, start_time, end_time)

            # Calculate overall health score
            metrics.overall_health_score = await self._calculate_overall_health_score(metrics)

            # Determine health trend direction
            metrics.health_trend_direction = await self._determine_health_trend(metrics)

            # Identify areas of concern
            metrics.areas_of_concern = await self._identify_areas_of_concern(metrics)

            # Store snapshot for historical analysis
            await self._store_health_snapshot(metrics)

            return metrics

        except Exception as e:
            logger.error(f"Failed to get current health metrics: {e}")
            # Return minimal metrics on error
            return SystemHealthMetrics(
                measurement_period_start=datetime.now(UTC) - timedelta(days=7),
                measurement_period_end=datetime.now(UTC),
                overall_health_score=0.5  # Neutral score on error
            )

    async def update_interaction_metrics(self, interaction: InteractionRecord) -> None:
        """
        Update real-time health indicators based on new interaction.

        This provides immediate feedback on system health changes.
        """
        try:
            # Update participation tracking
            await self._update_participation_tracking(interaction)

            # Update satisfaction indicators
            await self._update_satisfaction_indicators(interaction)

            # Update capacity utilization
            await self._update_capacity_utilization(interaction)

            # Update need fulfillment tracking
            await self._update_need_fulfillment(interaction)

            # Clear cache to force recalculation
            self.metric_cache.clear()

        except Exception as e:
            logger.error(f"Failed to update interaction metrics: {e}")

    async def update_indicator_weights(self, new_weights: dict[str, float]) -> None:
        """
        Update health indicator weights based on Fire Circle guidance.

        Allows the community to adapt what aspects of health are prioritized.
        """
        try:
            # Validate weights sum to approximately 1.0
            total_weight = sum(new_weights.values())
            if abs(total_weight - 1.0) > 0.1:
                logger.warning(f"Health indicator weights sum to {total_weight}, not 1.0")

            # Update weights
            for indicator_str, weight in new_weights.items():
                if hasattr(HealthIndicator, indicator_str.upper()):
                    indicator = HealthIndicator(indicator_str.lower())
                    self.indicator_weights[indicator] = weight

            logger.info(f"Updated health indicator weights: {len(new_weights)} indicators")

        except Exception as e:
            logger.error(f"Failed to update indicator weights: {e}")

    async def get_health_trend_analysis(self, days_back: int = 30) -> dict[str, Any]:
        """
        Analyze health trends over specified time period.
        """
        try:
            end_time = datetime.now(UTC)
            start_time = end_time - timedelta(days=days_back)

            # Get historical health snapshots
            snapshots = await self._get_health_snapshots_in_timeframe(start_time, end_time)

            if len(snapshots) < 2:
                return {'insufficient_data': True}

            # Analyze trends in key metrics
            trends = {}

            # Overall health score trend
            health_scores = [s.overall_health_score for s in snapshots]
            trends['overall_health'] = {
                'current': health_scores[-1],
                'average': mean(health_scores),
                'trend': 'improving' if health_scores[-1] > health_scores[0] else 'declining',
                'volatility': stdev(health_scores) if len(health_scores) > 1 else 0
            }

            # Participation trends
            participation_rates = [s.voluntary_return_rate for s in snapshots]
            trends['participation'] = {
                'current': participation_rates[-1],
                'average': mean(participation_rates),
                'trend': 'increasing' if participation_rates[-1] > participation_rates[0] else 'decreasing'
            }

            # Resource abundance trends
            abundance_indicators = []
            for snapshot in snapshots:
                if snapshot.resource_abundance_indicators:
                    avg_abundance = mean(snapshot.resource_abundance_indicators.values())
                    abundance_indicators.append(avg_abundance)

            if abundance_indicators:
                trends['resource_abundance'] = {
                    'current': abundance_indicators[-1],
                    'average': mean(abundance_indicators),
                    'trend': 'increasing' if abundance_indicators[-1] > abundance_indicators[0] else 'decreasing'
                }

            return trends

        except Exception as e:
            logger.error(f"Failed to analyze health trends: {e}")
            return {'error': str(e)}

    # Private implementation methods

    def _should_update_cache(self) -> bool:
        """Check if metric cache needs updating."""
        return (datetime.now(UTC) - self.last_cache_update) >= self.cache_update_interval

    async def _update_metric_cache(self) -> None:
        """Update cached metrics for performance."""
        try:
            # Cache frequently used metrics
            self.metric_cache['participant_count'] = await self._get_unique_participant_count()
            self.metric_cache['recent_interactions'] = await self._get_recent_interaction_count()
            self.metric_cache['satisfaction_trends'] = await self._get_satisfaction_trend_data()

            self.last_cache_update = datetime.now(UTC)

        except Exception as e:
            logger.error(f"Failed to update metric cache: {e}")

    async def _calculate_participation_metrics(
        self,
        metrics: SystemHealthMetrics,
        start_time: datetime,
        end_time: datetime
    ) -> None:
        """Calculate participation and engagement health metrics."""
        try:
            # Get interactions in timeframe
            interactions = await self._get_interactions_in_timeframe(start_time, end_time)

            # Basic counts
            metrics.total_interactions = len(interactions)

            # Unique participants
            participants = set()
            for interaction in interactions:
                participants.add(f"{interaction.initiator}_{hash(str(interaction.participant_context))}")
                participants.add(f"{interaction.responder}_{hash(str(interaction.participant_context))}")
            metrics.unique_participants = len(participants)

            # Participation trends (compare to previous period)
            prev_start = start_time - (end_time - start_time)
            prev_interactions = await self._get_interactions_in_timeframe(prev_start, start_time)

            if prev_interactions:
                participation_change = (len(interactions) - len(prev_interactions)) / len(prev_interactions)
                metrics.participation_trends['interaction_change'] = participation_change

            # Voluntary return rate (estimate based on repeat participation)
            returning_participants = await self._calculate_return_rate(interactions, start_time)
            metrics.voluntary_return_rate = returning_participants

        except Exception as e:
            logger.error(f"Failed to calculate participation metrics: {e}")

    async def _calculate_capacity_metrics(
        self,
        metrics: SystemHealthMetrics,
        start_time: datetime,
        end_time: datetime
    ) -> None:
        """Calculate capacity and resource health metrics."""
        try:
            interactions = await self._get_interactions_in_timeframe(start_time, end_time)

            # Resource abundance indicators
            resource_stress_count = 0
            resource_abundance_count = 0

            for interaction in interactions:
                # Analyze capacity indicators
                initiator_capacity = interaction.initiator_capacity_indicators
                responder_capacity = interaction.responder_capacity_indicators

                # Check for resource stress signals
                if any(cap < 0.3 for cap in initiator_capacity.values()):
                    resource_stress_count += 1
                if any(cap < 0.3 for cap in responder_capacity.values()):
                    resource_stress_count += 1

                # Check for resource abundance signals
                if any(cap > 0.8 for cap in initiator_capacity.values()):
                    resource_abundance_count += 1
                if any(cap > 0.8 for cap in responder_capacity.values()):
                    resource_abundance_count += 1

            # Calculate abundance ratio
            total_capacity_signals = resource_stress_count + resource_abundance_count
            if total_capacity_signals > 0:
                abundance_ratio = resource_abundance_count / total_capacity_signals
                metrics.resource_abundance_indicators['capacity_abundance_ratio'] = abundance_ratio

            # Capacity utilization rates
            utilization_rates = []
            for interaction in interactions:
                all_capacities = list(interaction.initiator_capacity_indicators.values()) + \
                               list(interaction.responder_capacity_indicators.values())
                if all_capacities:
                    avg_utilization = mean(all_capacities)
                    utilization_rates.append(avg_utilization)

            if utilization_rates:
                metrics.capacity_utilization_rates['average'] = mean(utilization_rates)
                metrics.capacity_utilization_rates['variance'] = stdev(utilization_rates) if len(utilization_rates) > 1 else 0

            # Need fulfillment rates
            need_fulfillment = {}
            for need_category in NeedCategory:
                fulfilled = sum(1 for i in interactions if need_category in i.needs_fulfilled)
                expressed = sum(1 for i in interactions if need_category in i.needs_expressed)
                if expressed > 0:
                    need_fulfillment[need_category] = fulfilled / expressed

            metrics.need_fulfillment_rates = need_fulfillment

        except Exception as e:
            logger.error(f"Failed to calculate capacity metrics: {e}")

    async def _calculate_adaptation_metrics(
        self,
        metrics: SystemHealthMetrics,
        start_time: datetime,
        end_time: datetime
    ) -> None:
        """Calculate system adaptation and resilience metrics."""
        try:
            # Conflict resolution success (placeholder - would need conflict data)
            metrics.conflict_resolution_success = 0.8  # Default estimate

            # Innovation emergence rate (new interaction patterns)
            innovation_signals = await self._detect_innovation_signals(start_time, end_time)
            metrics.innovation_emergence_rate = len(innovation_signals) / max(1, metrics.total_interactions) * 100

            # Adaptation indicators (changes in response to challenges)
            adaptation_indicators = await self._calculate_adaptation_indicators(start_time, end_time)
            metrics.adaptation_to_change_indicators = adaptation_indicators

        except Exception as e:
            logger.error(f"Failed to calculate adaptation metrics: {e}")

    async def _calculate_quality_metrics(
        self,
        metrics: SystemHealthMetrics,
        start_time: datetime,
        end_time: datetime
    ) -> None:
        """Calculate quality of life and satisfaction metrics."""
        try:
            interactions = await self._get_interactions_in_timeframe(start_time, end_time)

            # Satisfaction trends
            satisfaction_scores = []
            stress_indicators = []
            flourishing_signals = []

            for interaction in interactions:
                # Extract satisfaction signals
                satisfaction_data = interaction.participant_satisfaction_signals
                quality_data = interaction.interaction_quality_indicators

                if satisfaction_data:
                    # Aggregate satisfaction scores
                    satisfaction_values = [v for v in satisfaction_data.values() if isinstance(v, int | float)]
                    if satisfaction_values:
                        satisfaction_scores.extend(satisfaction_values)

                if quality_data:
                    # Look for stress indicators (low quality scores)
                    quality_values = [v for v in quality_data.values() if isinstance(v, int | float)]
                    stress_indicators.extend([v for v in quality_values if v < 0.4])

                    # Look for flourishing signals (high quality + emergence)
                    if any(v > 0.8 for v in quality_values):
                        flourishing_signals.append(1)

            # Calculate aggregated metrics
            if satisfaction_scores:
                metrics.satisfaction_trends['average_satisfaction'] = mean(satisfaction_scores)
                metrics.satisfaction_trends['satisfaction_variance'] = stdev(satisfaction_scores) if len(satisfaction_scores) > 1 else 0

            if interactions:
                metrics.stress_indicators['stress_incident_rate'] = len(stress_indicators) / len(interactions)
                metrics.flourishing_signals['flourishing_rate'] = len(flourishing_signals) / len(interactions)

        except Exception as e:
            logger.error(f"Failed to calculate quality metrics: {e}")

    async def _calculate_overall_health_score(self, metrics: SystemHealthMetrics) -> float:
        """Calculate weighted overall health score."""
        try:
            score_components = {}

            # Participation health component
            participation_score = min(1.0, metrics.voluntary_return_rate)
            score_components[HealthIndicator.PARTICIPATION_RATE] = participation_score

            # Satisfaction health component
            satisfaction_avg = metrics.satisfaction_trends.get('average_satisfaction', 0.5)
            score_components[HealthIndicator.SATISFACTION_TRENDS] = satisfaction_avg

            # Resource abundance component
            abundance_avg = mean(metrics.resource_abundance_indicators.values()) if metrics.resource_abundance_indicators else 0.5
            score_components[HealthIndicator.RESOURCE_ABUNDANCE] = abundance_avg

            # Conflict resolution component
            score_components[HealthIndicator.CONFLICT_RESOLUTION] = metrics.conflict_resolution_success

            # Innovation emergence component
            innovation_normalized = min(1.0, metrics.innovation_emergence_rate / 10.0)  # Normalize to 0-1
            score_components[HealthIndicator.INNOVATION_EMERGENCE] = innovation_normalized

            # Voluntary return component
            score_components[HealthIndicator.VOLUNTARY_RETURN] = metrics.voluntary_return_rate

            # Capacity utilization component
            capacity_avg = metrics.capacity_utilization_rates.get('average', 0.5)
            score_components[HealthIndicator.CAPACITY_UTILIZATION] = capacity_avg

            # Need fulfillment component
            need_fulfillment_avg = mean(metrics.need_fulfillment_rates.values()) if metrics.need_fulfillment_rates else 0.5
            score_components[HealthIndicator.NEED_FULFILLMENT] = need_fulfillment_avg

            # Calculate weighted score
            overall_score = 0.0
            for indicator, score in score_components.items():
                weight = self.indicator_weights.get(indicator, 0.0)
                overall_score += score * weight

            return max(0.0, min(1.0, overall_score))

        except Exception as e:
            logger.error(f"Failed to calculate overall health score: {e}")
            return 0.5  # Neutral score on error

    async def _determine_health_trend(self, current_metrics: SystemHealthMetrics) -> str:
        """Determine if health is improving, declining, or stable."""
        try:
            # Get previous health snapshot for comparison
            previous_snapshot = await self._get_previous_health_snapshot()

            if not previous_snapshot:
                return "stable"  # No baseline for comparison

            score_change = current_metrics.overall_health_score - previous_snapshot.overall_health_score

            if score_change > 0.05:
                return "improving"
            elif score_change < -0.05:
                return "declining"
            else:
                return "stable"

        except Exception as e:
            logger.error(f"Failed to determine health trend: {e}")
            return "stable"

    async def _identify_areas_of_concern(self, metrics: SystemHealthMetrics) -> list[str]:
        """Identify specific areas requiring attention."""
        concerns = []

        try:
            # Check participation concerns
            if metrics.voluntary_return_rate < 0.6:
                concerns.append("low_voluntary_return_rate")

            # Check satisfaction concerns
            avg_satisfaction = metrics.satisfaction_trends.get('average_satisfaction', 0.5)
            if avg_satisfaction < 0.6:
                concerns.append("declining_satisfaction")

            # Check resource concerns
            abundance_avg = mean(metrics.resource_abundance_indicators.values()) if metrics.resource_abundance_indicators else 0.5
            if abundance_avg < 0.4:
                concerns.append("resource_scarcity")

            # Check capacity concerns
            capacity_avg = metrics.capacity_utilization_rates.get('average', 0.5)
            if capacity_avg > 0.9:
                concerns.append("capacity_overutilization")
            elif capacity_avg < 0.3:
                concerns.append("capacity_underutilization")

            # Check need fulfillment concerns
            for need_category, fulfillment_rate in metrics.need_fulfillment_rates.items():
                if fulfillment_rate < 0.5:
                    concerns.append(f"unfulfilled_{need_category.value}_needs")

            return concerns

        except Exception as e:
            logger.error(f"Failed to identify areas of concern: {e}")
            return concerns

    # Database interaction methods

    async def _get_interactions_in_timeframe(
        self,
        start_time: datetime,
        end_time: datetime
    ) -> list[InteractionRecord]:
        """Get interactions within specified timeframe."""
        # This would query the reciprocity_interactions collection
        # For now, return empty list as placeholder
        return []

    async def _store_health_snapshot(self, metrics: SystemHealthMetrics) -> None:
        """Store health snapshot for historical analysis."""
        try:
            # Convert to dict and handle datetime/UUID serialization
            snapshot_doc = metrics.dict()
            # Convert datetime objects to ISO format strings
            for key, value in snapshot_doc.items():
                if isinstance(value, datetime):
                    snapshot_doc[key] = value.isoformat()

            snapshot_doc['_key'] = f"snapshot_{int(metrics.snapshot_timestamp.timestamp())}"

            collection = self.db.collection('system_health_snapshots')
            collection.insert(snapshot_doc)

        except Exception as e:
            logger.error(f"Failed to store health snapshot: {e}")

    async def _get_health_snapshots_in_timeframe(
        self,
        start_time: datetime,
        end_time: datetime
    ) -> list[SystemHealthMetrics]:
        """Get historical health snapshots."""
        # Implementation would query health snapshots collection
        return []

    async def _establish_baseline_metrics(self) -> None:
        """Establish baseline metrics for comparison."""
        # Implementation would calculate or load baseline metrics
        pass

    async def _get_previous_health_snapshot(self) -> SystemHealthMetrics | None:
        """Get the most recent previous health snapshot."""
        # Implementation would query for most recent snapshot
        return None

    async def _update_participation_tracking(self, interaction: InteractionRecord) -> None:
        """Update real-time participation tracking."""
        # Implementation would update participation counters
        pass

    async def _update_satisfaction_indicators(self, interaction: InteractionRecord) -> None:
        """Update real-time satisfaction indicators."""
        # Implementation would update satisfaction metrics
        pass

    async def _update_capacity_utilization(self, interaction: InteractionRecord) -> None:
        """Update real-time capacity utilization."""
        # Implementation would update capacity metrics
        pass

    async def _update_need_fulfillment(self, interaction: InteractionRecord) -> None:
        """Update real-time need fulfillment tracking."""
        # Implementation would update need fulfillment counters
        pass

    async def _get_unique_participant_count(self) -> int:
        """Get count of unique participants."""
        # Implementation would count unique participants
        return 0

    async def _get_recent_interaction_count(self) -> int:
        """Get count of recent interactions."""
        # Implementation would count recent interactions
        return 0

    async def _get_satisfaction_trend_data(self) -> dict[str, Any]:
        """Get satisfaction trend data."""
        # Implementation would calculate satisfaction trends
        return {}

    async def _calculate_return_rate(
        self,
        interactions: list[InteractionRecord],
        start_time: datetime
    ) -> float:
        """Calculate participant return rate."""
        # Implementation would analyze repeat participation
        return 0.8  # Placeholder

    async def _detect_innovation_signals(
        self,
        start_time: datetime,
        end_time: datetime
    ) -> list[dict[str, Any]]:
        """Detect innovation and emergence signals."""
        # Implementation would identify new patterns or behaviors
        return []

    async def _calculate_adaptation_indicators(
        self,
        start_time: datetime,
        end_time: datetime
    ) -> dict[str, float]:
        """Calculate adaptation indicators."""
        # Implementation would measure system adaptation
        return {}
