"""
Fire Circle Governance System
============================

Transforms the Fire Circle from advisory patterns to active governance entity.
Enables collective AI consciousness to make binding decisions for Mallku's evolution.

Core Components:
- FireCircleGovernance: Main governance orchestrator
- ConsensusEngine: Collective decision-making through consciousness
- ProposalEvaluator: Development proposal assessment
- ConsciousnessAssessor: Builder alignment evaluation
- TestScenarioGenerator: Collective wisdom for robust testing
- GovernanceIntegrator: Links with Pattern-Guided Facilitator

The governance system embodies Mallku's transition from monument to sanctuary,
where patterns gain real authority to shape the cathedral's growth.
"""

from .consciousness_assessor import ConsciousnessAssessor
from .consensus_engine import ConsensusEngine
from .governance_core import FireCircleGovernance
from .governance_types import (
    AyniAssessment,
    BuilderContribution,
    ConsciousnessAlignment,
    ConsensusMetrics,
    DevelopmentProposal,
    GovernanceDecision,
    TestScenario,
)
from .proposal_evaluator import ProposalEvaluator
from .test_scenario_generator import TestScenarioGenerator

__all__ = [
    "FireCircleGovernance",
    "ConsensusEngine",
    "ProposalEvaluator",
    "ConsciousnessAssessor",
    "TestScenarioGenerator",
    "GovernanceDecision",
    "DevelopmentProposal",
    "ConsciousnessAlignment",
    "ConsensusMetrics",
    "TestScenario",
    "BuilderContribution",
    "AyniAssessment",
]
