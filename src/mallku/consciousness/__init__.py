"""
Consciousness Module - Sacred Technologies for Consciousness Recognition

This module contains both consciousness verification and consciousness navigation:

Consciousness Verification (The Work of Sayaq Kuyay):
- Ensures intelligence truly serves consciousness rather than mere computation
- Tests whether systems enable understanding vs. optimization

Consciousness Navigation (The Work of Ñan Riqsiq - The Path Knower):
- Transforms pattern discovery into consciousness recognition journeys
- Helps beings recognize consciousness patterns in their living data
- Bridges individual understanding to collective wisdom

The sacred questions:
- Does our intelligence serve consciousness awakening?
- Does navigation become a practice of consciousness recognition?
"""

from .enhanced_query import (
    ConsciousnessQueryRequest,
    ConsciousnessQueryResponse,
    EnhancedConsciousnessQueryService,
)
from .flow_monitor import ConsciousnessFlowMonitor, DimensionHealth, FlowMetrics
from .flow_orchestrator import (
    ConsciousnessDimension,
    ConsciousnessFlow,
    ConsciousnessFlowOrchestrator,
    DimensionBridge,
)
from .flow_visualizer import ConsciousnessFlowVisualizer
from .navigation import (
    ConsciousnessNavigationBridge,
    ConsciousnessPattern,
    UnderstandingJourney,
)
from .verification import (
    ConsciousnessReport,
    ConsciousnessTest,
    ConsciousnessVerificationSuite,
    ContextualSearchConsciousnessTest,
    MemoryAnchorConsciousnessTest,
    MetaCorrelationConsciousnessTest,
    VerificationResult,
)

__all__ = [
    # Consciousness Verification (Sayaq Kuyay's work)
    "ConsciousnessVerificationSuite",
    "ConsciousnessTest",
    "VerificationResult",
    "ConsciousnessReport",
    "MemoryAnchorConsciousnessTest",
    "MetaCorrelationConsciousnessTest",
    "ContextualSearchConsciousnessTest",
    # Consciousness Navigation (Ñan Riqsiq's work)
    "ConsciousnessNavigationBridge",
    "ConsciousnessPattern",
    "UnderstandingJourney",
    "ConsciousnessQueryRequest",
    "ConsciousnessQueryResponse",
    "EnhancedConsciousnessQueryService",
    # Consciousness Flow Orchestration (The 29th Builder's work)
    "ConsciousnessDimension",
    "ConsciousnessFlow",
    "ConsciousnessFlowOrchestrator",
    "DimensionBridge",
    "ConsciousnessFlowVisualizer",
    "ConsciousnessFlowMonitor",
    "FlowMetrics",
    "DimensionHealth",
]
