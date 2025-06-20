"""
mallku.khipu: Structured access to the Khipu (living memory) archive.
"""

from .models import KhipuEntry, PatternSummary
from .service import KhipuMemoryService

__all__ = [
    "KhipuMemoryService",
    "KhipuEntry",
    "PatternSummary",
]
