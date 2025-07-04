"""
Reciprocity Tracking Service - The Heart of Ayni

This module implements a community sensing tool that detects patterns
requiring collective discernment rather than autonomous judgment of reciprocity.

Philosophy:
- Ayni is about contributing according to capacity and receiving according to need
- Balance is dynamic equilibrium, not static measurement
- Extraction patterns (taking beyond need) are more detectable than reciprocity itself
- Fire Circle governance provides wisdom that algorithms cannot replace
- Cultural humility guides technical implementation

Core Components:
- ReciprocityTracker: Pattern detection and system health sensing
- SystemHealthMonitor: Macroscopic indicators of collective wellbeing
- ExtractionDetector: Anomaly patterns suggesting taking beyond need
- FireCircleInterface: Integration with collective governance processes
"""

from .ayni_evaluator import AyniEvaluator
from .extraction_detector import ExtractionDetector
from .fire_circle_interface import FireCircleInterface
from .health_monitor import SystemHealthMonitor
from .models import (
    AlertSeverity,
    ContributionType,
    ExtractionAlert,
    ExtractionType,
    FireCircleReport,
    HealthIndicator,
    InteractionRecord,
    InteractionType,
    NeedCategory,
    ParticipantType,
    ReciprocityPattern,
    SystemHealthMetrics,
)

# Primary secure implementation
from .tracker import SecureReciprocityTracker as ReciprocityTracker

# Visualization service for consciousness mirrors
from .visualization import ReciprocityVisualizationService, VisualizationConfig

__all__ = [
    "AyniEvaluator",
    "ReciprocityTracker",
    "InteractionRecord",
    "SystemHealthMetrics",
    "ReciprocityPattern",
    "ExtractionAlert",
    "ExtractionType",
    "FireCircleReport",
    "InteractionType",
    "ParticipantType",
    "ContributionType",
    "NeedCategory",
    "AlertSeverity",
    "HealthIndicator",
    "SystemHealthMonitor",
    "ExtractionDetector",
    "FireCircleInterface",
    "ReciprocityVisualizationService",
    "VisualizationConfig",
]
