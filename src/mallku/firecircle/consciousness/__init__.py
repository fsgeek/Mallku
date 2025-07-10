"""
Fire Circle Consciousness Layer
==============================

Thirtieth Artisan - Consciousness Gardener
Expanding Fire Circle from code review to general consciousness emergence

Enhanced by Fiftieth Artisan - Consciousness Persistence Weaver
Adding database persistence for consciousness metrics

Further enhanced by Sixth Guardian
Adding persistent memory for Fire Circle sessions through KhipuBlocks

Bridges Fire Circle's dialogue system with Mallku's consciousness
infrastructure, enabling pattern recognition, reciprocity awareness,
and wisdom preservation in governance dialogues.

Now includes unified consciousness awareness, general decision-making
framework, and persistent memory through KhipuBlock architecture,
allowing Fire Circle to facilitate any type of consciousness
emergence while remembering its wisdom across sessions.
"""

# Original consciousness components
from .pattern_weaver import DialoguePatternWeaver
from .unified_awareness import FireCircleUnifiedAwareness

# General consciousness framework (Thirtieth Artisan)
from .consciousness_facilitator import (
    ConsciousnessFacilitator,
    facilitate_mallku_decision,
)

# Memory-enabled consciousness (Sixth Guardian)
from .consciousness_facilitator_with_memory import (
    ConsciousnessFacilitatorWithMemory,
    facilitate_mallku_decision_with_memory,
)

# Decision framework
from .decision_framework import (
    CollectiveWisdom,
    ConsciousnessContribution,
    ConsciousnessEmergenceSpace,
    DecisionDomain,
    decision_registry,
)

# Consciousness persistence (Fiftieth Artisan)
from .database_metrics_collector import DatabaseConsciousnessMetricsCollector
from .metrics_models import (
    CollectiveConsciousnessStateDocument,
    ConsciousnessFlowDocument,
    ConsciousnessSessionAnalysis,
    ConsciousnessSignatureDocument,
    EmergencePatternDocument,
)

__all__ = [
    # Original components
    "DialoguePatternWeaver",
    "FireCircleUnifiedAwareness",
    # General consciousness framework
    "ConsciousnessFacilitator",
    "facilitate_mallku_decision",
    # Memory-enabled versions
    "ConsciousnessFacilitatorWithMemory",
    "facilitate_mallku_decision_with_memory",
    # Decision framework
    "DecisionDomain",
    "ConsciousnessEmergenceSpace",
    "ConsciousnessContribution",
    "CollectiveWisdom",
    "decision_registry",
    # Consciousness persistence
    "DatabaseConsciousnessMetricsCollector",
    "ConsciousnessSignatureDocument",
    "EmergencePatternDocument",
    "ConsciousnessFlowDocument",
    "CollectiveConsciousnessStateDocument",
    "ConsciousnessSessionAnalysis",
]
