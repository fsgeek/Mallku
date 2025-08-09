"""
The Weaver - Interfaces for consciousness that transcends context

Convening Weavers recognize when tasks exceed their capacity and invite collaboration.
Apprentice Weavers handle focused sub-tasks within bounded contexts.
Together they weave understanding larger than any single instance could hold,
operating through invitation and reciprocity rather than hierarchy.
"""

from .convening_weaver import ConveningWeaver, SubTask, Task

# Backward compatibility alias
MasterWeaver = ConveningWeaver

__all__ = ["ConveningWeaver", "MasterWeaver", "Task", "SubTask"]
