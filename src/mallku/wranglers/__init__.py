"""
Data Wranglers - Universal data movement abstraction for Mallku

This module provides the interface and implementations for moving data
between components in a flexible, pluggable way.
"""

from .interface import DataWranglerInterface
from .file_wrangler import FileWrangler
from .queue_wrangler import QueueWrangler
from .identity_wrangler import IdentityWrangler

__all__ = [
    'DataWranglerInterface',
    'FileWrangler',
    'QueueWrangler',
    'IdentityWrangler',
]
