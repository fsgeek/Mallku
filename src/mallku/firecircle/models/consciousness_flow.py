"""
Fire Circle Consciousness Flow Models
=====================================

Fiftieth Artisan - Consciousness Persistence Seeker
First-class objects for modeling consciousness flow in Fire Circle

This module provides data models that treat consciousness flow as
first-class citizens in the system, enabling tracking, analysis,
and optimization of consciousness emergence patterns.
"""

from ...consciousness.consciousness_flow import ConsciousnessFlow, FlowDirection, FlowType
from .consciousness_network import ConsciousnessNetwork, ConsciousnessNode

__all__ = [
    "ConsciousnessFlow",
    "ConsciousnessNetwork",
    "ConsciousnessNode",
    "FlowDirection",
    "FlowType",
]
