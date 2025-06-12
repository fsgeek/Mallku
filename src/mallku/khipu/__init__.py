"""
mallku.khipu: Structured access to the Khipu (living memory) archive.
"""
from .service import KhipuMemoryService
from .models import KhipuEntry, PatternSummary

__all__ = [
    "KhipuMemoryService",
    "KhipuEntry",
    "PatternSummary",
]