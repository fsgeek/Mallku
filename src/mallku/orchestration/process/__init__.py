"""
Process-based orchestration for Mallku.

This module implements lightweight process-based apprentices as an alternative
to heavy container-based orchestration. Apprentices are ephemeral processes
that collaborate through shared memory and message passing.
"""

from .lightweight_apprentice import ProcessApprentice
from .shared_memory_commons import SharedMemoryCommons

__all__ = ["ProcessApprentice", "SharedMemoryCommons"]
