"""
File System Activity Stream Connector

Captures file operations and converts them into standardized events for correlation analysis.
This module forms the foundation of the Memory Anchor Discovery Trail, transforming
raw file system operations into structured activity streams.
"""

from .file_event_models import FileEvent, FileEventFilter, FileOperation
from .file_system_connector import FileSystemConnector

__all__ = ["FileSystemConnector", "FileEvent", "FileOperation", "FileEventFilter"]
