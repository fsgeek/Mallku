"""
Mallku Correlation Engine

This module implements the Memory Anchor Correlation Engine, which detects
temporal patterns in activity streams and generates memory anchors from
meaningful correlations.

The correlation engine embodies the principle of Ayni by recognizing
the reciprocal relationships between different streams of human activity,
understanding that meaning emerges from the dance between intention and action.
"""

from .engine import CorrelationEngine
from .models import CorrelationFeedback, CorrelationWindow, TemporalCorrelation
from .patterns import ConcurrentPattern, ContextualPattern, CyclicalPattern, SequentialPattern
from .scoring import ConfidenceScorer
from .thresholds import AdaptiveThresholds

__all__ = [
    'CorrelationEngine',
    'TemporalCorrelation',
    'CorrelationWindow',
    'CorrelationFeedback',
    'SequentialPattern',
    'ConcurrentPattern',
    'CyclicalPattern',
    'ContextualPattern',
    'ConfidenceScorer',
    'AdaptiveThresholds'
]
