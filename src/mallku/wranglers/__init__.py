"""
Data Wranglers - Universal data movement abstraction for Mallku

This module provides the interface and implementations for moving data
between components in a flexible, pluggable way.
"""

from .file_wrangler import FileWrangler
from .identity_wrangler import IdentityWrangler
from .interface import DataWranglerInterface
from .queue_wrangler import QueueWrangler

__all__ = [
    'DataWranglerInterface',
    'FileWrangler',
    'QueueWrangler',
    'IdentityWrangler',
]
