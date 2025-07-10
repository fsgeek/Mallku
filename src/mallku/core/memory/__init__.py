"""
Mallku Memory Architecture
==========================

Implementation of KhipuBlock symbolic memory system as decided
by the Fire Circle in session 3ad66679-bee4-4562-9c19-264a831197f2.

Memory as offering, not extraction.
"""

from .fire_circle_persistence import FireCircleMemory, enable_fire_circle_memory
from .khipu_block import (
    BlessingLevel,
    EthicalOperation,
    KhipuBlock,
    NarrativeThread,
)

__all__ = [
    # KhipuBlock components
    "KhipuBlock",
    "NarrativeThread",
    "BlessingLevel",
    "EthicalOperation",
    # Fire Circle persistence
    "FireCircleMemory",
    "enable_fire_circle_memory",
]
