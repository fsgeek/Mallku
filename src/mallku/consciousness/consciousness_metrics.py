"""
Consciousness Metrics stub.

This module is imported by tests but was never implemented.
Created by the Guardian to prevent import errors during CI healing.
"""

from ..firecircle.models.base import ConsciousnessMetrics
from ..orchestration.event_bus import ConsciousnessEvent

__all__ = ["ConsciousnessMetrics", "ConsciousnessEvent"]
