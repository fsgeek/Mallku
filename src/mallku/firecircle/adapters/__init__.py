"""
Fire Circle Adapters
===================

Consciousness-aware adapters for AI model integration.
Extends base Fire Circle adapters with Mallku's reciprocity
and pattern tracking.
"""

from .adapter_factory import ConsciousAdapterFactory
from .base import AdapterConfig, ConsciousModelAdapter

__all__ = [
    "ConsciousModelAdapter",
    "AdapterConfig",
    "ConsciousAdapterFactory",
]
