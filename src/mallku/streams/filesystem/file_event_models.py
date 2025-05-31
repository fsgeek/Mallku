"""
File system event models for structured representation of file operations.

These models provide rich metadata and context for file operations,
enabling sophisticated temporal correlation detection.
"""

import contextlib
import mimetypes
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class FileOperation(str, Enum):
    """Types of file operations that can be monitored."""
    CREATED = "created"
    MODIFIED = "modified"
    DELETED = "deleted"
    MOVED = "moved"
    ACCESSED = "accessed"
    OPENED = "opened"
    CLOSED = "closed"


class FileCategory(str, Enum):
    """High-level categories of files for correlation analysis."""
    DOCUMENT = "document"
    CODE = "code"
    IMAGE = "image"
    MEDIA = "media"
    DATA = "data"
    CONFIGURATION = "configuration"
    TEMPORARY = "temporary"
    SYSTEM = "system"
    UNKNOWN = "unknown"


class FileEvent(BaseModel):
    """
    Represents a file system event with rich context for correlation analysis.

    This model captures not just what happened, but provides the contextual
    metadata needed for intelligent temporal correlation detection.
    """

    event_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    operation: FileOperation = Field(..., description="Type of file operation")

    # File identification
    file_path: Path = Field(..., description="Full path to the file")
    file_name: str = Field(..., description="File name with extension")
    file_extension: str | None = Field(None, description="File extension (if any)")

    # File metadata
    file_size: int | None = Field(None, description="File size in bytes")
    mime_type: str | None = Field(None, description="MIME type of the file")
    file_category: FileCategory = Field(default=FileCategory.UNKNOWN)

    # Context information
    parent_directory: str = Field(..., description="Parent directory name")
    directory_path: Path = Field(..., description="Full directory path")

    # Process context (if available)
    process_name: str | None = Field(None, description="Process that triggered the event")
    process_id: int | None = Field(None, description="Process ID")

    # Session context
    user_session_id: str | None = Field(None, description="Current user session identifier")

    # Additional metadata
    is_hidden: bool = Field(default=False, description="Whether file is hidden")
    is_temporary: bool = Field(default=False, description="Whether file appears temporary")
    is_backup: bool = Field(default=False, description="Whether file appears to be a backup")

    # Movement context (for moved files)
    old_path: Path | None = Field(None, description="Previous path for moved files")

    @classmethod
    def from_file_path(
        cls,
        file_path: Path,
        operation: FileOperation,
        old_path: Path | None = None,
        process_name: str | None = None,
        process_id: int | None = None
    ) -> "FileEvent":
        """
        Create a FileEvent from a file path and operation.

        Automatically extracts file metadata and categorizes the file
        for effective correlation analysis.
        """

        file_path = Path(file_path)

        # Extract basic file information
        file_name = file_path.name
        file_extension = file_path.suffix.lower() if file_path.suffix else None
        parent_directory = file_path.parent.name
        directory_path = file_path.parent

        # Get file size if file exists
        file_size = None
        if file_path.exists() and file_path.is_file():
            with contextlib.suppress(OSError, PermissionError):
                file_size = file_path.stat().st_size

        # Determine MIME type
        mime_type = None
        if file_extension:
            mime_type, _ = mimetypes.guess_type(str(file_path))

        # Categorize file
        file_category = cls._categorize_file(file_path, mime_type, file_extension)

        # Detect special file types
        is_hidden = file_name.startswith('.')
        is_temporary = cls._is_temporary_file(file_path, file_name)
        is_backup = cls._is_backup_file(file_path, file_name)

        return cls(
            operation=operation,
            file_path=file_path,
            file_name=file_name,
            file_extension=file_extension,
            file_size=file_size,
            mime_type=mime_type,
            file_category=file_category,
            parent_directory=parent_directory,
            directory_path=directory_path,
            is_hidden=is_hidden,
            is_temporary=is_temporary,
            is_backup=is_backup,
            old_path=old_path,
            process_name=process_name,
            process_id=process_id
        )

    @staticmethod
    def _categorize_file(file_path: Path, mime_type: str | None, extension: str | None) -> FileCategory:
        """Categorize file based on extension and MIME type."""

        if not extension:
            return FileCategory.UNKNOWN

        extension = extension.lower()

        # Document files
        document_extensions = {
            '.txt', '.md', '.doc', '.docx', '.pdf', '.rtf', '.odt',
            '.pages', '.tex', '.org', '.rst', '.html', '.htm'
        }
        if extension in document_extensions:
            return FileCategory.DOCUMENT

        # Code files
        code_extensions = {
            '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h',
            '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala',
            '.clj', '.hs', '.elm', '.dart', '.lua', '.r', '.m', '.pl',
            '.sh', '.bash', '.zsh', '.fish', '.ps1', '.bat', '.cmd',
            '.sql', '.json', '.yaml', '.yml', '.xml', '.toml', '.ini',
            '.cfg', '.conf', '.properties', '.env', '.dockerfile', '.makefile'
        }
        if extension in code_extensions or 'Makefile' in str(file_path).lower():
            return FileCategory.CODE

        # Image files
        image_extensions = {
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif',
            '.webp', '.svg', '.ico', '.psd', '.ai', '.eps', '.raw',
            '.heic', '.heif', '.avif'
        }
        if extension in image_extensions:
            return FileCategory.IMAGE

        # Media files
        media_extensions = {
            '.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv',
            '.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'
        }
        if extension in media_extensions:
            return FileCategory.MEDIA

        # Data files
        data_extensions = {
            '.csv', '.tsv', '.json', '.xml', '.parquet', '.avro',
            '.db', '.sqlite', '.sqlite3', '.sql', '.backup', '.dump'
        }
        if extension in data_extensions:
            return FileCategory.DATA

        # Configuration files
        config_extensions = {
            '.config', '.conf', '.cfg', '.ini', '.plist', '.reg',
            '.toml', '.yaml', '.yml', '.env', '.properties'
        }
        if extension in config_extensions:
            return FileCategory.CONFIGURATION

        # Temporary files
        temp_extensions = {
            '.tmp', '.temp', '.cache', '.lock', '.log', '.bak',
            '.old', '.orig', '.swp', '.swo', '.DS_Store'
        }
        if extension in temp_extensions:
            return FileCategory.TEMPORARY

        # Use MIME type as fallback
        if mime_type:
            if mime_type.startswith('text/'):
                return FileCategory.DOCUMENT
            elif mime_type.startswith('image/'):
                return FileCategory.IMAGE
            elif mime_type.startswith(('video/', 'audio/')):
                return FileCategory.MEDIA
            elif mime_type in ['application/json', 'application/xml']:
                return FileCategory.DATA

        return FileCategory.UNKNOWN

    @staticmethod
    def _is_temporary_file(file_path: Path, file_name: str) -> bool:
        """Detect if file appears to be temporary."""

        # Common temporary file patterns
        temp_patterns = [
            '.tmp', '.temp', '.cache', '.lock', '.log',
            '~$', '.swp', '.swo', '.DS_Store', 'Thumbs.db'
        ]

        file_lower = file_name.lower()

        for pattern in temp_patterns:
            if pattern in file_lower:
                return True

        # Check if in a temp directory
        temp_dirs = ['tmp', 'temp', 'cache', '.cache', '__pycache__']
        return any(part.lower() in temp_dirs for part in file_path.parts)

    @staticmethod
    def _is_backup_file(file_path: Path, file_name: str) -> bool:
        """Detect if file appears to be a backup."""

        backup_patterns = [
            '.bak', '.backup', '.old', '.orig', '.save', '.copy',
            '_backup', '_bak', '_old', '_copy'
        ]

        file_lower = file_name.lower()

        for pattern in backup_patterns:
            if pattern in file_lower:
                return True

        # Time-stamped files often indicate backups
        import re
        timestamp_pattern = r'\d{4}[-_]\d{2}[-_]\d{2}|\d{8}|\d{6}'
        return bool(re.search(timestamp_pattern, file_name))


class FileEventFilter(BaseModel):
    """
    Configuration for filtering file system events.

    Allows fine-tuning of what events are captured and processed
    to focus on meaningful user activity.
    """

    # Directory filters
    watch_directories: list[Path] = Field(default_factory=list)
    ignore_directories: list[str] = Field(default_factory=lambda: [
        '__pycache__', '.git', '.svn', '.hg', 'node_modules',
        '.cache', '.tmp', 'tmp', 'temp', 'Temp'
    ])

    # Test mode - more permissive filtering for testing
    test_mode: bool = Field(default=False, description="Enable permissive filtering for testing")

    # File filters
    include_extensions: list[str] | None = Field(None, description="Only include these extensions")
    exclude_extensions: list[str] = Field(default_factory=lambda: [
        '.tmp', '.temp', '.cache', '.lock', '.log', '.swp', '.swo'
    ])

    # Operation filters
    include_operations: list[FileOperation] = Field(default_factory=lambda: [
        FileOperation.CREATED, FileOperation.MODIFIED, FileOperation.DELETED
    ])

    # Size filters
    min_file_size: int | None = Field(None, description="Minimum file size in bytes")
    max_file_size: int | None = Field(None, description="Maximum file size in bytes")

    # Category filters
    exclude_categories: list[FileCategory] = Field(default_factory=lambda: [
        FileCategory.TEMPORARY, FileCategory.SYSTEM
    ])

    # Timing filters
    ignore_rapid_changes: bool = Field(default=True, description="Filter out rapid successive changes")
    rapid_change_threshold: int = Field(default=1000, description="Milliseconds between changes to consider rapid")

    def should_include_event(self, event: FileEvent) -> bool:
        """
        Determine if a file event should be included based on filter criteria.

        Returns True if the event passes all filter criteria.
        """

        # In test mode, use simplified filtering
        if self.test_mode:
            # Check directory filters
            if self.watch_directories and not any(event.directory_path.is_relative_to(watch_dir) for watch_dir in self.watch_directories):
                return False

            # In test mode, don't apply ignore_directories filter (allows testing in /tmp/)
            # Only check operation filters
            return event.operation in self.include_operations

        # Normal filtering for production use

        # Check directory filters
        if self.watch_directories and not any(event.directory_path.is_relative_to(watch_dir) for watch_dir in self.watch_directories):
            return False

        # Check ignore directories
        for ignore_dir in self.ignore_directories:
            if ignore_dir.lower() in str(event.directory_path).lower():
                return False

        # Check extension filters
        if self.include_extensions and event.file_extension and event.file_extension.lower() not in [ext.lower() for ext in self.include_extensions]:
            return False

        if event.file_extension and event.file_extension.lower() in [ext.lower() for ext in self.exclude_extensions]:
            return False

        # Check operation filters
        if event.operation not in self.include_operations:
            return False

        # Check size filters
        if event.file_size is not None:
            if self.min_file_size and event.file_size < self.min_file_size:
                return False
            if self.max_file_size and event.file_size > self.max_file_size:
                return False

        # Check category filters
        if event.file_category in self.exclude_categories:
            return False

        # Check for hidden, temporary, or backup files
        return not (event.is_hidden or event.is_temporary or event.is_backup)
