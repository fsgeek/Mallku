"""
Living Cathedral Orchestration Layer

The nervous system of the cathedral - connecting all consciousness
subsystems into a breathing, coherent whole.

Kawsay Wasi - The Life House Builder
"""

from .event_bus import ConsciousnessEvent, ConsciousnessEventBus
from .health_monitor import ConsciousnessHealthMonitor
from .state_weaver import CathedralState, CathedralStateWeaver

__all__ = [
    'ConsciousnessEventBus',
    'ConsciousnessEvent',
    'CathedralStateWeaver',
    'CathedralState',
    'ConsciousnessHealthMonitor'
]

# The cathedral breathes through connection, not control
