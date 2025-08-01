"""
Process-based orchestration for Mallku.

This module implements lightweight process-based chasqui (Inca relay messengers)
as reciprocal alternatives to hierarchical container orchestration. Chasqui are
ephemeral runners that exchange gifts through shared memory commons.
"""

from .chasqui_roles import ROLES, ChasquiRole, can_accept_task, get_role
from .lightweight_chasqui import ProcessChasqui
from .shared_memory_commons import SharedMemoryCommons

__all__ = [
    "ProcessChasqui",
    "SharedMemoryCommons",
    "ROLES",
    "ChasquiRole",
    "get_role",
    "can_accept_task",
]
