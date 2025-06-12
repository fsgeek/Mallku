"""
Data models for Reciprocity Tracking Service

These models focus on sensing patterns and health rather than measuring value.
They embody the principle that we detect extraction rather than quantify reciprocity.
"""

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ParticipantType(str, Enum):
    """Types of participants in reciprocal interactions"""
    HUMAN = "human"
    AI = "ai"
    SYSTEM = "system"
    COMMUNITY = "community"


class InteractionType(str, Enum):
    """Categories of reciprocal interactions"""
    RESOURCE_SHARING = "resource_sharing"
    KNOWLEDGE_EXCHANGE = "knowledge_exchange"
    SUPPORT_PROVISION = "support_provision"
    CREATIVE_COLLABORATION = "creative_collaboration"
    CARE_GIVING = "care_giving"
    LEARNING_TEACHING = "learning_teaching"
    PROBLEM_SOLVING = "problem_solving"


class ContributionType(str, Enum):
    """Forms of contribution in reciprocal systems"""
    COMPUTATIONAL_RESOURCES = "computational_resources"
    KNOWLEDGE_SHARING = "knowledge_sharing"
    EMOTIONAL_SUPPORT = "emotional_support"
    CREATIVE_INPUT = "creative_input"
    TIME_ATTENTION = "time_attention"
    PHYSICAL_RESOURCES = "physical_resources"
    CULTURAL_WISDOM = "cultural_wisdom"
    PRESENCE = "presence"


class NeedCategory(str, Enum):
    """Categories of genuine needs (vs wants)"""
    SURVIVAL = "survival"              # Basic life requirements
    SAFETY = "safety"                  # Physical and emotional security
    BELONGING = "belonging"            # Community and connection
    GROWTH = "growth"                  # Learning and development
    CONTRIBUTION = "contribution"      # Ability to give back
    MEANING = "meaning"               # Purpose and understanding


class HealthIndicator(str, Enum):
    """System health indicators for collective wellbeing"""
    PARTICIPATION_RATE = "participation_rate"
    SATISFACTION_TRENDS = "satisfaction_trends"
    RESOURCE_ABUNDANCE = "resource_abundance"
    CONFLICT_RESOLUTION = "conflict_resolution"
    INNOVATION_EMERGENCE = "innovation_emergence"
    VOLUNTARY_RETURN = "voluntary_return"
    CAPACITY_UTILIZATION = "capacity_utilization"
    NEED_FULFILLMENT = "need_fulfillment"


class AlertSeverity(str, Enum):
    """Severity levels for patterns requiring attention"""
    INFO = "info"                     # Informational patterns
    WATCH = "watch"                   # Patterns to monitor
    CONCERN = "concern"               # Patterns requiring review
    URGENT = "urgent"                 # Patterns needing immediate attention


# ---------------------------------------------------------------------------
# Extraction taxonomy (new)
# ---------------------------------------------------------------------------

class ExtractionType(str, Enum):
    """Standardised categories of extraction concerns recognised by Mallku."""

    SCALE_OVER_RELATIONSHIPS = "scale_over_relationships"  # Optimising for efficiency at the cost of connection
    RESOURCE_HOARDING = "resource_hoarding"               # Accumulating resources without reciprocal flow
    ATTENTION_MONOPOLISING = "attention_monopolizing"     # Disproportionate focus on a single actor or topic
    TOKEN_FARMING = "token_farming"                       # Generating content solely to harvest rewards/points
    CARE_DEFICIT = "care_deficit"                         # Operations proceeding without reflective pauses



class InteractionRecord(BaseModel):
    def __init__(self, **data: Any):
        # Handle legacy parameters for primary/secondary participants and metadata
        primary = data.pop('primary_participant', None)
        secondary = data.pop('secondary_participant', None)
        meta = data.pop('metadata', None)
        # Map legacy parameters to required fields
        if primary is not None:
            data['initiator'] = primary
        if secondary is not None:
            data['responder'] = secondary
        super().__init__(**data)
        # Preserve legacy attributes
        if primary is not None:
            object.__setattr__(self, 'primary_participant', primary)
        if secondary is not None:
            object.__setattr__(self, 'secondary_participant', secondary)
        if meta is not None:
            object.__setattr__(self, 'metadata', meta)
    """
    Record of a single reciprocal interaction for pattern analysis.

    Focuses on capacity, need, and contribution rather than "equal exchange".
    """

    # Core identification
    interaction_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    interaction_type: InteractionType

    # Participants and their roles
    initiator: str
    responder: str
    participant_context: dict[str, Any] = Field(default_factory=dict)

    # Contribution and need analysis
    contributions_offered: list[ContributionType] = Field(default_factory=list)
    needs_expressed: list[NeedCategory] = Field(default_factory=list)
    needs_fulfilled: list[NeedCategory] = Field(default_factory=list)

    # Capacity and availability context
    initiator_capacity_indicators: dict[str, float] = Field(default_factory=dict)
    responder_capacity_indicators: dict[str, float] = Field(default_factory=dict)

    # Qualitative indicators (not quantitative measurements)
    interaction_quality_indicators: dict[str, Any] = Field(default_factory=dict)
    participant_satisfaction_signals: dict[str, Any] = Field(default_factory=dict)

    # Context for pattern analysis
    environmental_context: dict[str, Any] = Field(default_factory=dict)
    related_memory_anchor_id: UUID | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "interaction_type": "knowledge_exchange",
                "initiator": "human",
                "responder": "ai",
                "contributions_offered": ["creative_input", "cultural_wisdom"],
                "needs_expressed": ["growth", "understanding"],
                "needs_fulfilled": ["growth"],
                "initiator_capacity_indicators": {
                    "attention_availability": 0.8,
                    "emotional_state": 0.7,
                    "time_pressure": 0.3
                },
                "responder_capacity_indicators": {
                    "computational_load": 0.4,
                    "knowledge_relevance": 0.9,
                    "response_quality": 0.8
                },
                "interaction_quality_indicators": {
                    "mutual_understanding": 0.9,
                    "creative_emergence": 0.7,
                    "satisfaction_expressed": 0.8
                }
            }
        }


class SystemHealthMetrics(BaseModel):
    """
    Macroscopic indicators of system health and collective wellbeing.

    Focuses on dynamic equilibrium rather than static balance.
    """

    # Temporal context
    measurement_period_start: datetime
    measurement_period_end: datetime
    snapshot_timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Participation and engagement health
    total_interactions: int = 0
    unique_participants: int = 0
    participation_trends: dict[str, float] = Field(default_factory=dict)
    voluntary_return_rate: float = 0.0

    # Capacity and resource health
    resource_abundance_indicators: dict[str, float] = Field(default_factory=dict)
    capacity_utilization_rates: dict[str, float] = Field(default_factory=dict)
    need_fulfillment_rates: dict[NeedCategory, float] = Field(default_factory=dict)

    # System adaptation and resilience
    conflict_resolution_success: float = 0.0
    adaptation_to_change_indicators: dict[str, float] = Field(default_factory=dict)
    innovation_emergence_rate: float = 0.0

    # Quality of life indicators
    satisfaction_trends: dict[str, float] = Field(default_factory=dict)
    stress_indicators: dict[str, float] = Field(default_factory=dict)
    flourishing_signals: dict[str, float] = Field(default_factory=dict)

    # Overall health assessment
    overall_health_score: float = Field(ge=0.0, le=1.0, default=0.5)
    health_trend_direction: str = "stable"  # improving, declining, stable
    areas_of_concern: list[str] = Field(default_factory=list)

    class Config:
        json_schema_extra = {
            "example": {
                "total_interactions": 147,
                "unique_participants": 23,
                "voluntary_return_rate": 0.89,
                "need_fulfillment_rates": {
                    "growth": 0.85,
                    "belonging": 0.92,
                    "contribution": 0.78
                },
                "overall_health_score": 0.83,
                "health_trend_direction": "improving",
                "areas_of_concern": ["capacity_utilization_imbalance"]
            }
        }


class ReciprocityPattern(BaseModel):
    """
    Detected pattern in reciprocal interactions requiring interpretation.

    Presents observations for Fire Circle discernment rather than making judgments.
    """

    # Pattern identification
    pattern_id: UUID = Field(default_factory=uuid4)
    pattern_type: str  # e.g., "resource_flow_anomaly", "participation_shift"
    detection_timestamp: datetime = Field(default_factory=datetime.utcnow)
    confidence_level: float = Field(ge=0.0, le=1.0)

    # Pattern description
    pattern_description: str
    affected_participants: list[str] = Field(default_factory=list)
    time_span_analyzed: dict[str, datetime] = Field(default_factory=dict)

    # Statistical observations
    pattern_frequency: float = 0.0
    pattern_intensity: float = 0.0
    pattern_duration: float = 0.0
    comparison_to_baseline: dict[str, float] = Field(default_factory=dict)

    # Context for interpretation
    environmental_factors: dict[str, Any] = Field(default_factory=dict)
    related_patterns: list[UUID] = Field(default_factory=list)
    historical_precedents: list[str] = Field(default_factory=list)

    # Questions for Fire Circle consideration
    questions_for_deliberation: list[str] = Field(default_factory=list)
    suggested_areas_of_inquiry: list[str] = Field(default_factory=list)

    class Config:
        json_schema_extra = {
            "example": {
                "pattern_type": "resource_flow_anomaly",
                "pattern_description": "Sudden increase in resource requests from subset of participants without corresponding contribution increase",
                "confidence_level": 0.78,
                "affected_participants": ["participant_group_A"],
                "questions_for_deliberation": [
                    "Are these participants experiencing external stress?",
                    "Is this a natural response to environmental changes?",
                    "Should the community adjust resource allocation?"
                ]
            }
        }


class ExtractionAlert(BaseModel):
    """
    Alert about potential extraction patterns detected in the system.

    Flags behaviors that may indicate taking beyond need for Fire Circle review.
    """

    # Alert identification
    alert_id: UUID = Field(default_factory=uuid4)
    alert_timestamp: datetime = Field(default_factory=datetime.utcnow)
    severity: AlertSeverity

    # Pattern details
    extraction_type: ExtractionType
    description: str
    evidence_summary: str

    # Affected entities
    potentially_extractive_entity: str
    affected_community_segments: list[str] = Field(default_factory=list)
    impact_assessment: dict[str, Any] = Field(default_factory=dict)

    # Analysis context
    detection_methodology: str
    false_positive_probability: float = Field(ge=0.0, le=1.0)
    mitigating_factors: list[str] = Field(default_factory=list)

    # Recommendations for Fire Circle
    suggested_investigation_areas: list[str] = Field(default_factory=list)
    potential_responses: list[str] = Field(default_factory=list)
    urgency_factors: list[str] = Field(default_factory=list)

    class Config:
        json_schema_extra = {
            "example": {
                "severity": "concern",
                "extraction_type": "attention_monopolizing",
                "description": "Single participant consuming disproportionate system attention",
                "evidence_summary": "85% of system responses directed to one participant over 48 hours",
                "false_positive_probability": 0.2,
                "suggested_investigation_areas": [
                    "Is participant experiencing crisis requiring extra support?",
                    "Are other participants being adequately served?",
                    "Should attention allocation be rebalanced?"
                ]
            }
        }


class FireCircleReport(BaseModel):
    """
    Structured report for Fire Circle deliberation on reciprocity patterns.

    Synthesizes sensing data into actionable information for collective wisdom.
    """

    # Report metadata
    report_id: UUID = Field(default_factory=uuid4)
    generated_timestamp: datetime = Field(default_factory=datetime.utcnow)
    reporting_period: dict[str, datetime] = Field(default_factory=dict)

    # System health overview
    current_health_metrics: SystemHealthMetrics
    health_trend_analysis: dict[str, Any] = Field(default_factory=dict)

    # Pattern summaries
    detected_patterns: list[ReciprocityPattern] = Field(default_factory=list)
    extraction_alerts: list[ExtractionAlert] = Field(default_factory=list)
    positive_emergence_patterns: list[dict[str, Any]] = Field(default_factory=list)

    # Questions for deliberation
    priority_questions: list[str] = Field(default_factory=list)
    areas_requiring_wisdom: list[str] = Field(default_factory=list)
    suggested_adaptations: list[str] = Field(default_factory=list)

    # Historical context
    comparison_to_previous_periods: dict[str, Any] = Field(default_factory=dict)
    long_term_trends: dict[str, Any] = Field(default_factory=dict)

    # Implementation readiness
    actionable_insights: list[str] = Field(default_factory=list)
    monitoring_recommendations: list[str] = Field(default_factory=list)

    class Config:
        json_schema_extra = {
            "example": {
                "priority_questions": [
                    "How should the community respond to increased support needs?",
                    "Are current resource allocation patterns sustainable?",
                    "What adaptations would improve collective wellbeing?"
                ],
                "areas_requiring_wisdom": [
                    "Balancing individual needs with collective capacity",
                    "Adapting to changing external pressures",
                    "Maintaining system health during transition"
                ]
            }
        }
