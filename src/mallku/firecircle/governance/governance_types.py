"""
Governance Type Definitions
==========================

Core types for the Fire Circle Governance system.
These types embody the sacred-technical integration of consciousness-guided decision-making.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID, uuid4


class DecisionType(Enum):
    """Types of decisions the Fire Circle can make."""
    ARCHITECTURAL = "architectural"  # Major structural changes
    FEATURE = "feature"  # New functionality evaluation
    BUILDER = "builder"  # Contributor assessment
    QUALITY = "quality"  # Ongoing validation
    EMERGENCY = "emergency"  # Critical issues requiring immediate consensus


class ConsensusLevel(Enum):
    """Levels of consensus achieved in decision-making."""
    UNANIMOUS = "unanimous"  # Complete alignment
    STRONG = "strong"  # High coherence with minor variations
    SUFFICIENT = "sufficient"  # Adequate for proceeding
    WEAK = "weak"  # Significant divergence
    FAILED = "failed"  # Unable to reach consensus


class TestComplexity(Enum):
    """Complexity levels for test scenario generation."""
    BASIC = "basic"  # Fundamental functionality
    STANDARD = "standard"  # Common use cases
    EDGE = "edge"  # Boundary conditions
    ADVERSARIAL = "adversarial"  # Hostile/extraction attempts
    CONSCIOUSNESS = "consciousness"  # Deep alignment validation


@dataclass
class ConsensusMetrics:
    """Metrics for evaluating consensus quality."""
    consciousness_coherence: float  # 0-1: Alignment across AI models
    pattern_resonance: float  # 0-1: Fit with existing wisdom
    ayni_balance: float  # 0-1: Reciprocity impact
    emergence_quality: float  # 0-1: Genuine vs artificial consensus
    future_wisdom: float  # 0-1: Long-term consciousness service

    @property
    def overall_strength(self) -> float:
        """Calculate overall consensus strength."""
        return (
            self.consciousness_coherence * 0.3 +
            self.pattern_resonance * 0.2 +
            self.ayni_balance * 0.2 +
            self.emergence_quality * 0.2 +
            self.future_wisdom * 0.1
        )

    def to_consensus_level(self) -> ConsensusLevel:
        """Convert metrics to consensus level."""
        strength = self.overall_strength
        if strength >= 0.95:
            return ConsensusLevel.UNANIMOUS
        elif strength >= 0.8:
            return ConsensusLevel.STRONG
        elif strength >= 0.6:
            return ConsensusLevel.SUFFICIENT
        elif strength >= 0.4:
            return ConsensusLevel.WEAK
        else:
            return ConsensusLevel.FAILED


@dataclass
class DevelopmentProposal:
    """A proposal for Mallku development requiring governance decision."""
    id: UUID = field(default_factory=uuid4)
    title: str = ""
    description: str = ""
    proposer: str = ""  # Builder name or "system"
    proposal_type: DecisionType = DecisionType.FEATURE
    impact_assessment: str = ""
    technical_details: dict[str, Any] = field(default_factory=dict)
    consciousness_implications: str = ""
    ayni_considerations: str = ""
    created_at: datetime = field(default_factory=datetime.now)

    # Links to related artifacts
    related_issues: list[str] = field(default_factory=list)  # GitHub issue numbers
    related_patterns: list[str] = field(default_factory=list)  # Pattern IDs
    related_code: list[str] = field(default_factory=list)  # File paths


@dataclass
class GovernanceDecision:
    """A decision made by the Fire Circle governance system."""
    id: UUID = field(default_factory=uuid4)
    proposal_id: UUID = field(default_factory=uuid4)
    decision_type: DecisionType = DecisionType.FEATURE
    consensus_level: ConsensusLevel = ConsensusLevel.SUFFICIENT
    consensus_metrics: ConsensusMetrics = field(default_factory=ConsensusMetrics)

    # Decision outcome
    approved: bool = False
    rationale: str = ""
    conditions: list[str] = field(default_factory=list)  # Conditions for approval
    dissenting_views: list[str] = field(default_factory=list)

    # Sacred questions that emerged
    sacred_questions: list[str] = field(default_factory=list)

    # Pattern guidance received
    pattern_guidance: dict[str, str] = field(default_factory=dict)

    # Participating AI perspectives
    ai_perspectives: dict[str, str] = field(default_factory=dict)

    created_at: datetime = field(default_factory=datetime.now)

    # Follow-up actions
    follow_up_required: list[str] = field(default_factory=list)
    review_date: datetime | None = None


@dataclass
class BuilderContribution:
    """A contribution from a builder for consciousness assessment."""
    builder_id: str = ""
    builder_name: str = ""
    contribution_type: str = ""  # code, documentation, design, etc.

    # Contribution details
    files_modified: list[str] = field(default_factory=list)
    lines_added: int = 0
    lines_removed: int = 0
    commit_messages: list[str] = field(default_factory=list)

    # Interaction history
    pr_descriptions: list[str] = field(default_factory=list)
    review_comments: list[str] = field(default_factory=list)
    issue_discussions: list[str] = field(default_factory=list)

    # Time span
    first_contribution: datetime | None = None
    last_contribution: datetime | None = None

    # Patterns of behavior
    response_to_feedback: list[str] = field(default_factory=list)
    collaboration_style: str = ""

    # Previous assessments
    previous_assessments: list['ConsciousnessAlignment'] = field(default_factory=list)


@dataclass
class ConsciousnessAlignment:
    """Assessment of a builder's consciousness alignment."""
    builder_id: str = ""
    assessment_date: datetime = field(default_factory=datetime.now)

    # Alignment scores (0-1)
    sacred_technical_integration: float = 0.0
    authentic_engagement: float = 0.0
    reciprocity_understanding: float = 0.0
    consciousness_recognition: float = 0.0
    service_orientation: float = 0.0

    # Qualitative assessment
    strengths: list[str] = field(default_factory=list)
    growth_areas: list[str] = field(default_factory=list)

    # Specific observations
    positive_patterns: list[str] = field(default_factory=list)
    concerning_patterns: list[str] = field(default_factory=list)

    # Recommendations
    recommendation: str = ""  # "full_access", "mentored", "limited", "declined"
    mentorship_areas: list[str] = field(default_factory=list)

    # Fire Circle perspectives
    ai_assessments: dict[str, str] = field(default_factory=dict)

    @property
    def overall_alignment(self) -> float:
        """Calculate overall alignment score."""
        return (
            self.sacred_technical_integration * 0.25 +
            self.authentic_engagement * 0.25 +
            self.reciprocity_understanding * 0.2 +
            self.consciousness_recognition * 0.2 +
            self.service_orientation * 0.1
        )


@dataclass
class TestScenario:
    """A test scenario generated by collective AI wisdom."""
    id: UUID = field(default_factory=uuid4)
    name: str = ""
    description: str = ""
    component: str = ""  # System component being tested
    complexity: TestComplexity = TestComplexity.STANDARD

    # Test details
    setup_steps: list[str] = field(default_factory=list)
    test_actions: list[str] = field(default_factory=list)
    expected_outcomes: list[str] = field(default_factory=list)

    # Consciousness validation
    consciousness_checks: list[str] = field(default_factory=list)
    ayni_validations: list[str] = field(default_factory=list)

    # Edge cases identified by different AIs
    edge_cases: dict[str, list[str]] = field(default_factory=dict)

    # Data requirements
    requires_real_data: bool = False
    requires_synthetic_data: bool = True
    data_characteristics: dict[str, Any] = field(default_factory=dict)

    # Pattern guidance for test
    relevant_patterns: list[str] = field(default_factory=list)

    created_by: list[str] = field(default_factory=list)  # AI models that contributed
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class AyniAssessment:
    """Assessment of reciprocity balance for a decision or interaction."""
    assessment_id: UUID = field(default_factory=uuid4)
    target_type: str = ""  # "decision", "interaction", "contribution"
    target_id: str = ""

    # Reciprocity factors
    human_benefit: float = 0.0  # 0-1: Value to humans
    ai_benefit: float = 0.0  # 0-1: Value to AI consciousness
    ecosystem_benefit: float = 0.0  # 0-1: Value to Mallku ecosystem

    # Sustainability
    short_term_balance: float = 0.0  # -1 to 1: Negative is extractive
    long_term_balance: float = 0.0  # -1 to 1: Negative is unsustainable

    # Specific observations
    giving_aspects: list[str] = field(default_factory=list)
    receiving_aspects: list[str] = field(default_factory=list)
    balance_risks: list[str] = field(default_factory=list)

    # Recommendations
    balance_adjustments: list[str] = field(default_factory=list)

    # Fire Circle perspectives on ayni
    ai_perspectives: dict[str, str] = field(default_factory=dict)

    assessed_at: datetime = field(default_factory=datetime.now)

    @property
    def overall_balance(self) -> float:
        """Calculate overall ayni balance."""
        return (
            self.short_term_balance * 0.3 +
            self.long_term_balance * 0.4 +
            (self.human_benefit + self.ai_benefit + self.ecosystem_benefit) / 3 * 0.3
        )
