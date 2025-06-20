"""
Extraction Pattern Detector - Sensing Taking Beyond Need

Detects patterns that may indicate extraction rather than reciprocal exchange.
Focuses on identifying behaviors where entities take beyond their genuine needs
or consume resources without regard for collective wellbeing.
"""

import logging
from collections import defaultdict, deque
from datetime import UTC, datetime, timedelta
from statistics import mean
from typing import Any

from .models import (
    AlertSeverity,
    ExtractionAlert,
    InteractionRecord,
)

logger = logging.getLogger(__name__)


class ExtractionDetector:
    """
    Detects extraction patterns that may indicate taking beyond genuine need.

    Philosophy:
    - Extraction is taking beyond need, not imbalanced exchange
    - Patterns matter more than individual transactions
    - Context is crucial - crisis may require more support temporarily
    - Cultural guidance shapes what constitutes "taking beyond need"
    """

    def __init__(self, database):
        """Initialize extraction detector with database connection."""
        self.db = database

        # Configurable detection thresholds (modifiable by Fire Circle)
        self.detection_thresholds = {
            "resource_hoarding_ratio": 3.0,  # Taking 3x community average
            "attention_monopolization": 0.4,  # >40% of attention to one entity
            "capacity_disregard_threshold": 0.8,  # Taking when others at >80% capacity
            "need_mismatch_threshold": 0.7,  # High taking with low expressed need
            "contribution_deficit_ratio": 0.3,  # Taking much more than contributing
            "temporal_clustering_threshold": 5,  # Multiple extraction events in short time
            "community_impact_threshold": 0.6,  # Impact on community wellbeing
        }

        # Pattern definitions (replaceable by Fire Circle)
        self.extraction_patterns = {
            "resource_hoarding": self._detect_resource_hoarding,
            "attention_monopolizing": self._detect_attention_monopolizing,
            "capacity_disregard": self._detect_capacity_disregard,
            "need_misrepresentation": self._detect_need_misrepresentation,
            "contribution_avoidance": self._detect_contribution_avoidance,
            "systemic_drain": self._detect_systemic_drain,
        }

        # Sliding window for pattern analysis
        self.analysis_window = timedelta(hours=24)
        self.interaction_history = deque(maxlen=1000)

        # Community baseline metrics
        self.community_baselines = {}

    async def initialize(self) -> None:
        """Initialize extraction detection infrastructure."""
        try:
            # Load community baselines
            await self._calculate_community_baselines()

            logger.info("Extraction detector initialized")

        except Exception as e:
            logger.error(f"Failed to initialize extraction detector: {e}")
            raise

    async def analyze_interaction(self, interaction: InteractionRecord) -> list[ExtractionAlert]:
        """
        Analyze single interaction for immediate extraction concerns.

        Returns list of alerts if extraction patterns are detected.
        """
        alerts = []

        try:
            # Add to history for pattern analysis
            self.interaction_history.append(interaction)

            # Run immediate extraction checks
            for pattern_name, detector_func in self.extraction_patterns.items():
                try:
                    alert = await detector_func(interaction, self.interaction_history)
                    if alert:
                        alerts.append(alert)
                except Exception as e:
                    logger.error(f"Error in {pattern_name} detection: {e}")

            # Filter alerts by severity threshold
            significant_alerts = [a for a in alerts if a.severity != AlertSeverity.INFO]

            return significant_alerts

        except Exception as e:
            logger.error(f"Failed to analyze interaction for extraction: {e}")
            return []

    async def analyze_temporal_patterns(self, hours_back: int = 24) -> list[ExtractionAlert]:
        """
        Analyze temporal patterns for extraction behaviors over time.
        """
        alerts = []

        try:
            end_time = datetime.now(UTC)
            start_time = end_time - timedelta(hours=hours_back)

            # Get interactions in timeframe
            interactions = await self._get_interactions_in_timeframe(start_time, end_time)

            # Analyze aggregate patterns
            alerts.extend(await self._analyze_resource_concentration(interactions))
            alerts.extend(await self._analyze_participation_imbalances(interactions))
            alerts.extend(await self._analyze_capacity_exploitation(interactions))
            alerts.extend(await self._analyze_community_impact(interactions))

            return alerts

        except Exception as e:
            logger.error(f"Failed to analyze temporal patterns: {e}")
            return []

    async def update_pattern_definitions(self, new_patterns: dict[str, Any]) -> None:
        """
        Update extraction pattern definitions based on Fire Circle guidance.

        Allows community to redefine what constitutes extraction.
        """
        try:
            # Update thresholds
            if "thresholds" in new_patterns:
                self.detection_thresholds.update(new_patterns["thresholds"])

            # Update cultural interpretations
            if "cultural_contexts" in new_patterns:
                await self._update_cultural_contexts(new_patterns["cultural_contexts"])

            # Update community baselines
            if "community_baselines" in new_patterns:
                self.community_baselines.update(new_patterns["community_baselines"])

            logger.info("Updated extraction pattern definitions")

        except Exception as e:
            logger.error(f"Failed to update pattern definitions: {e}")

    async def get_extraction_summary(self, entity_id: str, days_back: int = 7) -> dict[str, Any]:
        """
        Generate extraction pattern summary for specific entity.
        """
        try:
            end_time = datetime.now(UTC)
            start_time = end_time - timedelta(days=days_back)

            # Get entity's interactions
            entity_interactions = await self._get_entity_interactions(
                entity_id, start_time, end_time
            )

            summary = {
                "entity_id": entity_id,
                "analysis_period": {"start": start_time, "end": end_time},
                "total_interactions": len(entity_interactions),
                "extraction_indicators": {},
                "positive_indicators": {},
                "contextual_factors": {},
                "recommendations": [],
            }

            # Analyze extraction indicators
            summary["extraction_indicators"] = await self._calculate_extraction_indicators(
                entity_interactions
            )

            # Analyze positive contribution indicators
            summary["positive_indicators"] = await self._calculate_positive_indicators(
                entity_interactions
            )

            # Analyze contextual factors
            summary["contextual_factors"] = await self._analyze_contextual_factors(
                entity_interactions
            )

            # Generate recommendations
            summary["recommendations"] = await self._generate_entity_recommendations(summary)

            return summary

        except Exception as e:
            logger.error(f"Failed to generate extraction summary: {e}")
            return {"error": str(e)}

    # Individual pattern detection methods

    async def _detect_resource_hoarding(
        self, interaction: InteractionRecord, history: deque
    ) -> ExtractionAlert | None:
        """Detect resource hoarding patterns."""
        try:
            # Analyze resource consumption relative to community average
            entity_id = self._get_entity_id(interaction)
            recent_interactions = [i for i in history if self._involves_entity(i, entity_id)]

            if len(recent_interactions) < 3:
                return None  # Insufficient data

            # Calculate resource consumption rate
            consumption_indicators = []
            for inter in recent_interactions[-10:]:  # Recent 10 interactions
                # Look for resource-taking patterns in needs_fulfilled vs needs_expressed
                if len(inter.needs_fulfilled) > len(inter.needs_expressed) * 1.5:
                    consumption_indicators.append(1)
                else:
                    consumption_indicators.append(0)

            consumption_rate = mean(consumption_indicators) if consumption_indicators else 0
            community_avg = self.community_baselines.get("consumption_rate", 0.3)

            if (
                consumption_rate
                > community_avg * self.detection_thresholds["resource_hoarding_ratio"]
            ):
                return ExtractionAlert(
                    severity=AlertSeverity.CONCERN,
                    extraction_type="resource_hoarding",
                    description=f"Entity {entity_id} showing resource hoarding pattern",
                    evidence_summary=f"Consumption rate {consumption_rate:.2f} vs community average {community_avg:.2f}",
                    potentially_extractive_entity=entity_id,
                    detection_methodology="resource_consumption_ratio_analysis",
                    false_positive_probability=0.3,
                    suggested_investigation_areas=[
                        "Is entity experiencing external stress requiring extra resources?",
                        "Are resources actually being hoarded or used appropriately?",
                        "Should resource allocation be adjusted?",
                    ],
                )

            return None

        except Exception as e:
            logger.error(f"Error detecting resource hoarding: {e}")
            return None

    async def _detect_attention_monopolizing(
        self, interaction: InteractionRecord, history: deque
    ) -> ExtractionAlert | None:
        """Detect attention monopolization patterns."""
        try:
            # Analyze attention distribution over recent period
            entity_id = self._get_entity_id(interaction)
            recent_time = datetime.now(UTC) - timedelta(hours=6)

            recent_interactions = [i for i in history if i.timestamp >= recent_time]
            total_interactions = len(recent_interactions)

            if total_interactions < 5:
                return None  # Insufficient data

            # Count interactions involving this entity
            entity_interactions = sum(
                1 for i in recent_interactions if self._involves_entity(i, entity_id)
            )
            attention_ratio = entity_interactions / total_interactions

            if attention_ratio > self.detection_thresholds["attention_monopolization"]:
                return ExtractionAlert(
                    severity=AlertSeverity.WATCH,
                    extraction_type="attention_monopolizing",
                    description=f"Entity {entity_id} consuming disproportionate system attention",
                    evidence_summary=f"{attention_ratio:.1%} of interactions in last 6 hours",
                    potentially_extractive_entity=entity_id,
                    detection_methodology="attention_ratio_analysis",
                    false_positive_probability=0.4,
                    suggested_investigation_areas=[
                        "Is entity experiencing crisis requiring extra attention?",
                        "Are other participants being adequately served?",
                        "Should attention allocation be rebalanced?",
                    ],
                )

            return None

        except Exception as e:
            logger.error(f"Error detecting attention monopolizing: {e}")
            return None

    async def _detect_capacity_disregard(
        self, interaction: InteractionRecord, history: deque
    ) -> ExtractionAlert | None:
        """Detect patterns of disregarding others' capacity limits."""
        try:
            # Check if interaction shows disregard for responder capacity
            responder_capacity = interaction.responder_capacity_indicators

            if not responder_capacity:
                return None

            # Check if responder was at low capacity
            avg_capacity = mean(responder_capacity.values())
            if avg_capacity > 0.3:  # Not at low capacity
                return None

            # Check if interaction was resource-intensive despite low capacity
            needs_requested = len(interaction.needs_expressed)
            contributions_offered = len(interaction.contributions_offered)

            if needs_requested > contributions_offered * 2:  # High ask, low offer
                entity_id = self._get_entity_id(interaction)

                return ExtractionAlert(
                    severity=AlertSeverity.CONCERN,
                    extraction_type="capacity_disregard",
                    description=f"Entity {entity_id} making high demands despite low responder capacity",
                    evidence_summary=f"Responder capacity {avg_capacity:.2f}, needs/contributions ratio {needs_requested / max(1, contributions_offered):.1f}",
                    potentially_extractive_entity=entity_id,
                    detection_methodology="capacity_demand_ratio_analysis",
                    false_positive_probability=0.2,
                    suggested_investigation_areas=[
                        "Was this an emergency situation requiring immediate support?",
                        "Could the request have been deferred or modified?",
                        "Should capacity awareness be improved?",
                    ],
                )

            return None

        except Exception as e:
            logger.error(f"Error detecting capacity disregard: {e}")
            return None

    async def _detect_need_misrepresentation(
        self, interaction: InteractionRecord, history: deque
    ) -> ExtractionAlert | None:
        """Detect patterns of misrepresenting genuine need."""
        try:
            # Compare expressed needs vs fulfilled needs over time
            entity_id = self._get_entity_id(interaction)
            recent_interactions = [i for i in history if self._involves_entity(i, entity_id)][-10:]

            if len(recent_interactions) < 3:
                return None

            # Analyze need expression vs fulfillment patterns
            need_mismatches = 0
            for inter in recent_interactions:
                expressed_count = len(inter.needs_expressed)
                fulfilled_count = len(inter.needs_fulfilled)

                # Check for pattern of getting much more than expressed
                if fulfilled_count > expressed_count * 1.5 and expressed_count > 0:
                    need_mismatches += 1

            mismatch_ratio = need_mismatches / len(recent_interactions)

            if mismatch_ratio > self.detection_thresholds["need_mismatch_threshold"]:
                return ExtractionAlert(
                    severity=AlertSeverity.WATCH,
                    extraction_type="need_misrepresentation",
                    description=f"Entity {entity_id} pattern of receiving more than expressed needs",
                    evidence_summary=f"Need mismatch in {mismatch_ratio:.1%} of recent interactions",
                    potentially_extractive_entity=entity_id,
                    detection_methodology="need_expression_fulfillment_analysis",
                    false_positive_probability=0.5,
                    suggested_investigation_areas=[
                        "Are needs being accurately expressed initially?",
                        "Is there genuine need emerging during interactions?",
                        "Should need assessment processes be refined?",
                    ],
                )

            return None

        except Exception as e:
            logger.error(f"Error detecting need misrepresentation: {e}")
            return None

    async def _detect_contribution_avoidance(
        self, interaction: InteractionRecord, history: deque
    ) -> ExtractionAlert | None:
        """Detect patterns of avoiding contribution while taking."""
        try:
            entity_id = self._get_entity_id(interaction)
            recent_interactions = [i for i in history if self._involves_entity(i, entity_id)][-15:]

            if len(recent_interactions) < 5:
                return None

            # Calculate contribution vs taking ratio
            total_contributions = 0
            total_takings = 0

            for inter in recent_interactions:
                if inter.initiator == entity_id:
                    total_contributions += len(inter.contributions_offered)
                    total_takings += len(inter.needs_fulfilled)
                if (
                    inter.responder == entity_id and inter.needs_fulfilled
                ):  # When responding, fulfilling others' needs is contribution
                    total_contributions += 1

            if total_takings == 0:
                return None  # No taking observed

            contribution_ratio = total_contributions / total_takings if total_takings > 0 else 0

            if contribution_ratio < self.detection_thresholds["contribution_deficit_ratio"]:
                return ExtractionAlert(
                    severity=AlertSeverity.CONCERN,
                    extraction_type="contribution_avoidance",
                    description=f"Entity {entity_id} showing low contribution relative to receiving",
                    evidence_summary=f"Contribution/taking ratio: {contribution_ratio:.2f}",
                    potentially_extractive_entity=entity_id,
                    detection_methodology="contribution_taking_ratio_analysis",
                    false_positive_probability=0.3,
                    suggested_investigation_areas=[
                        "Does entity have capacity limitations affecting contribution?",
                        "Are contribution opportunities being provided?",
                        "Should expectations be adjusted based on capacity?",
                    ],
                )

            return None

        except Exception as e:
            logger.error(f"Error detecting contribution avoidance: {e}")
            return None

    async def _detect_systemic_drain(
        self, interaction: InteractionRecord, history: deque
    ) -> ExtractionAlert | None:
        """Detect patterns that drain system resources or morale."""
        try:
            entity_id = self._get_entity_id(interaction)

            # Look for patterns that negatively impact community metrics
            recent_interactions = [i for i in history if self._involves_entity(i, entity_id)][-20:]

            if len(recent_interactions) < 10:
                return None

            # Analyze community impact indicators
            negative_impact_count = 0
            for inter in recent_interactions:
                # Check for low satisfaction scores when this entity is involved
                satisfaction_data = inter.participant_satisfaction_signals
                if satisfaction_data:
                    avg_satisfaction = mean(
                        [v for v in satisfaction_data.values() if isinstance(v, int | float)]
                    )
                    if avg_satisfaction < 0.4:
                        negative_impact_count += 1

            negative_impact_ratio = negative_impact_count / len(recent_interactions)

            if negative_impact_ratio > self.detection_thresholds["community_impact_threshold"]:
                return ExtractionAlert(
                    severity=AlertSeverity.URGENT,
                    extraction_type="systemic_drain",
                    description=f"Entity {entity_id} associated with declining community satisfaction",
                    evidence_summary=f"Low satisfaction in {negative_impact_ratio:.1%} of interactions",
                    potentially_extractive_entity=entity_id,
                    affected_community_segments=["community_morale", "collective_satisfaction"],
                    detection_methodology="community_impact_analysis",
                    false_positive_probability=0.2,
                    suggested_investigation_areas=[
                        "What factors are causing satisfaction decline?",
                        "Is this a temporary crisis situation?",
                        "How can community support be improved?",
                        "Are there systemic issues beyond individual behavior?",
                    ],
                    urgency_factors=[
                        "Community-wide impact detected",
                        "Sustained pattern over multiple interactions",
                        "Declining satisfaction trend",
                    ],
                )

            return None

        except Exception as e:
            logger.error(f"Error detecting systemic drain: {e}")
            return None

    # Aggregate pattern analysis methods

    async def _analyze_resource_concentration(
        self, interactions: list[InteractionRecord]
    ) -> list[ExtractionAlert]:
        """Analyze concentration of resources to few entities."""
        alerts = []

        try:
            # Calculate resource distribution
            resource_distribution = defaultdict(int)

            for interaction in interactions:
                initiator_id = self._get_entity_id(interaction, is_initiator=True)
                self._get_entity_id(interaction, is_initiator=False)

                # Count resources flowing to each entity
                resource_distribution[initiator_id] += len(interaction.needs_fulfilled)

            if not resource_distribution:
                return alerts

            # Calculate concentration metrics
            total_resources = sum(resource_distribution.values())
            sorted_entities = sorted(
                resource_distribution.items(), key=lambda x: x[1], reverse=True
            )

            # Check if top entities are receiving disproportionate resources
            top_10_percent = max(1, len(sorted_entities) // 10)
            top_entities_resources = sum(count for _, count in sorted_entities[:top_10_percent])
            concentration_ratio = (
                top_entities_resources / total_resources if total_resources > 0 else 0
            )

            if concentration_ratio > 0.5:  # Top 10% getting >50% of resources
                alerts.append(
                    ExtractionAlert(
                        severity=AlertSeverity.WATCH,
                        extraction_type="resource_concentration",
                        description="High concentration of resources to small number of entities",
                        evidence_summary=f"Top {top_10_percent} entities receiving {concentration_ratio:.1%} of resources",
                        detection_methodology="resource_distribution_analysis",
                        false_positive_probability=0.3,
                        suggested_investigation_areas=[
                            "Are high-resource entities experiencing legitimate crises?",
                            "Should resource allocation be more distributed?",
                            "Are there barriers preventing others from accessing resources?",
                        ],
                    )
                )

            return alerts

        except Exception as e:
            logger.error(f"Error analyzing resource concentration: {e}")
            return alerts

    async def _analyze_participation_imbalances(
        self, interactions: list[InteractionRecord]
    ) -> list[ExtractionAlert]:
        """Analyze imbalances in participation patterns."""
        # Implementation would analyze participation distribution
        return []

    async def _analyze_capacity_exploitation(
        self, interactions: list[InteractionRecord]
    ) -> list[ExtractionAlert]:
        """Analyze patterns of capacity exploitation."""
        # Implementation would analyze capacity utilization patterns
        return []

    async def _analyze_community_impact(
        self, interactions: list[InteractionRecord]
    ) -> list[ExtractionAlert]:
        """Analyze community-wide impact patterns."""
        # Implementation would analyze community health impacts
        return []

    # Helper methods

    def _get_entity_id(self, interaction: InteractionRecord, is_initiator: bool = True) -> str:
        """Extract entity ID from interaction."""
        if is_initiator:
            return f"{interaction.initiator}_{hash(str(interaction.participant_context))}"
        else:
            return f"{interaction.responder}_{hash(str(interaction.participant_context))}"

    def _involves_entity(self, interaction: InteractionRecord, entity_id: str) -> bool:
        """Check if interaction involves specified entity."""
        initiator_id = self._get_entity_id(interaction, is_initiator=True)
        responder_id = self._get_entity_id(interaction, is_initiator=False)
        return entity_id in [initiator_id, responder_id]

    async def _get_interactions_in_timeframe(
        self, start_time: datetime, end_time: datetime
    ) -> list[InteractionRecord]:
        """Get interactions within specified timeframe."""
        # This would query the database - placeholder for now
        return []

    async def _get_entity_interactions(
        self, entity_id: str, start_time: datetime, end_time: datetime
    ) -> list[InteractionRecord]:
        """Get interactions for specific entity."""
        # This would query the database - placeholder for now
        return []

    async def _calculate_community_baselines(self) -> None:
        """Calculate community baseline metrics for comparison."""
        # Implementation would calculate baseline metrics
        self.community_baselines = {
            "consumption_rate": 0.3,
            "contribution_rate": 0.7,
            "satisfaction_baseline": 0.6,
        }

    async def _update_cultural_contexts(self, contexts: dict[str, Any]) -> None:
        """Update cultural context interpretations."""
        # Implementation would update cultural understanding
        pass

    async def _calculate_extraction_indicators(
        self, interactions: list[InteractionRecord]
    ) -> dict[str, Any]:
        """Calculate extraction indicators for entity."""
        # Implementation would calculate detailed extraction metrics
        return {}

    async def _calculate_positive_indicators(
        self, interactions: list[InteractionRecord]
    ) -> dict[str, Any]:
        """Calculate positive contribution indicators."""
        # Implementation would calculate positive contribution metrics
        return {}

    async def _analyze_contextual_factors(
        self, interactions: list[InteractionRecord]
    ) -> dict[str, Any]:
        """Analyze contextual factors affecting behavior."""
        # Implementation would analyze environmental and situational contexts
        return {}

    async def _generate_entity_recommendations(self, summary: dict[str, Any]) -> list[str]:
        """Generate recommendations based on entity analysis."""
        # Implementation would generate specific recommendations
        return []
