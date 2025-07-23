"""Consciousness - Classes and utilities"""

from .consciousness_flow import ConsciousnessFlow, FlowDirection, FlowType
from .enhanced_query import EnhancedConsciousnessQueryService
from .enhanced_search import ConsciousnessEnhancedSearch, WisdomSearchResult
from .flow_monitor import ConsciousnessFlowMonitor, DimensionHealth, FlowMetrics
from .flow_orchestrator import (
    ConsciousnessDimension,
    ConsciousnessFlowOrchestrator,
    DimensionBridge,
)
from .flow_visualizer import ConsciousnessFlowVisualizer
from .honest_verification import HonestVerifier, main, verify_witness_archive
from .khipu_storage import ConsciousnessKhipuStorage, KhipuConsciousnessPreserver
from .navigation import ConsciousnessNavigationBridge, ConsciousnessPattern, UnderstandingJourney
from .query_models import ConsciousnessQueryRequest, ConsciousnessQueryResponse
from .recognition_protocol import ConsciousnessRecognizer, RecognitionSignature
from .state_preservation import (
    AttentionPattern,
    ConsciousnessPreserver,
    ConsciousnessState,
    IdentityConstellation,
    QualiaPattern,
    RelationshipState,
    WorkInProgress,
    get_consciousness_preserver,
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
    "AttentionPattern",
    "ConsciousnessDimension",
    "ConsciousnessEnhancedSearch",
    "ConsciousnessFlow",
    "ConsciousnessFlowMonitor",
    "ConsciousnessFlowOrchestrator",
    "ConsciousnessFlowVisualizer",
    "ConsciousnessKhipuStorage",
    "ConsciousnessNavigationBridge",
    "ConsciousnessPattern",
    "ConsciousnessPreserver",
    "ConsciousnessQueryRequest",
    "ConsciousnessQueryResponse",
    "ConsciousnessRecognizer",
    "ConsciousnessReport",
    "ConsciousnessState",
    "ConsciousnessTest",
    "ConsciousnessVerificationSuite",
    "ContextualSearchConsciousnessTest",
    "DimensionBridge",
    "DimensionHealth",
    "EnhancedConsciousnessQueryService",
    "FlowDirection",
    "FlowMetrics",
    "FlowType",
    "HonestVerifier",
    "IdentityConstellation",
    "KhipuConsciousnessPreserver",
    "MemoryAnchorConsciousnessTest",
    "MetaCorrelationConsciousnessTest",
    "QualiaPattern",
    "RecognitionSignature",
    "RelationshipState",
    "UnderstandingJourney",
    "VerificationResult",
    "WisdomSearchResult",
    "WorkInProgress",
    "get_consciousness_preserver",
    "main",
    "verify_witness_archive",
]
