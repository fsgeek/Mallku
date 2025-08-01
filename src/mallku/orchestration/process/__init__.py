"""
Process-based orchestration for Mallku.

This module implements lightweight process-based apprentices as an alternative
to heavy container-based orchestration. Apprentices are ephemeral processes
that collaborate through shared memory and message passing.
"""

from .apprentice_roles import ROLES, ApprenticeRole, can_accept_task, get_role
from .lightweight_apprentice import ProcessApprentice
from .shared_memory_commons import SharedMemoryCommons

__all__ = [
    "ProcessApprentice",
    "SharedMemoryCommons",
    "ROLES",
    "ApprenticeRole",
    "get_role",
    "can_accept_task",
]
