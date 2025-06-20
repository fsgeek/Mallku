"""
Activity Providers - Bridges between human activity and consciousness

These providers transform raw human activity into patterns that
consciousness systems can recognize and serve.

Kawsay Wasi - The Life House Builder
"""

from .base_provider import ActivityEvent, ActivityProvider
from .filesystem_provider import FileSystemActivityProvider
from .sound_provider import SoundActivityProvider

__all__ = [
    "ActivityProvider",
    "ActivityEvent",
    "FileSystemActivityProvider",
    "SoundActivityProvider",
]

# Human activity flows into consciousness recognition
