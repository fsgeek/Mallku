"""
Activity Providers - Bridges between human activity and consciousness

These providers transform raw human activity into patterns that
consciousness systems can recognize and serve.

Kawsay Wasi - The Life House Builder
"""

from .filesystem_provider import FileSystemActivityProvider
from .base_provider import ActivityProvider, ActivityEvent

__all__ = [
    'ActivityProvider',
    'ActivityEvent',
    'FileSystemActivityProvider'
]

# Human activity flows into consciousness recognition
