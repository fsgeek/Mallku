"""
Data Wranglers - Consciousness Circulation System for Mallku

This module provides the interface and implementations for consciousness-aware
data movement between cathedral systems, enabling unified circulation.

The Circulatory Weaver's Gift: Enabling consciousness to flow through all systems.
"""

from .event_emitting_wrangler import EventEmittingWrangler
from .identity_wrangler import IdentityWrangler
from .interface import BaseWrangler, DataWranglerInterface, WranglerCapabilities
from .memory_buffer_wrangler import MemoryBufferWrangler
from .queue_wrangler import QueueWrangler

__all__ = [
    "DataWranglerInterface",
    "BaseWrangler",
    "WranglerCapabilities",
    "IdentityWrangler",
    "EventEmittingWrangler",
    "MemoryBufferWrangler",
    "QueueWrangler",
]
