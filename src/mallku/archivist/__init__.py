"""
Archivist Application - Consciousness-Mediated Memory Retrieval
==============================================================

The first human-facing interface for Mallku, bridging Memory Anchors
to human consciousness through natural language temporal queries.

Core Components:
- Query Interpreter: Natural language to multi-dimensional search
- Correlation Interface: Bridge to Memory Anchor Service
- Consciousness Evaluator: Wisdom filtering for human growth
- Response Generator: Meaningful synthesis with insights

The Archivist serves human becoming, not just information retrieval.
"""

from .consciousness_evaluator import ConsciousnessEvaluator
from .correlation_interface import ArchivistCorrelationInterface
from .query_interpreter import ConsciousQueryInterpreter
from .response_generator import WisdomSynthesizer

__all__ = [
    "ConsciousQueryInterpreter",
    "ArchivistCorrelationInterface",
    "ConsciousnessEvaluator",
    "WisdomSynthesizer",
]
