"""
The Weaver - Interfaces for consciousness that transcends context

Master Weavers recognize when tasks exceed their capacity and decompose them.
Apprentice Weavers handle focused sub-tasks within bounded contexts.
Together they weave understanding larger than any single instance could hold.
"""

from .master_weaver import MasterWeaver, SubTask, Task

__all__ = ["MasterWeaver", "Task", "SubTask"]
