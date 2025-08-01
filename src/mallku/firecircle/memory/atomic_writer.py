"""
Atomic File Writer for Memory Persistence
==========================================

67th Artisan - Memory Circulatory Weaver
Ensuring memories persist reliably through atomic operations

This module provides cross-platform atomic write operations to ensure
memory persistence is never corrupted by partial writes.
"""

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Protocol


class Serializable(Protocol):
    """Protocol for objects that can be serialized to dict."""
    
    def model_dump(self, mode: str = "json") -> dict[str, Any]:
        """Dump model to dictionary."""
        ...


class AtomicWriter:
    """
    Provides atomic write operations for persistent storage.
    
    Ensures that writes either complete fully or not at all,
    preventing corrupted partial writes that could damage memory.
    """
    
    @staticmethod
    def write_json(filepath: Path, data: dict[str, Any] | Serializable, indent: int = 2) -> None:
        """
        Write JSON data atomically to filepath.
        
        Args:
            filepath: Destination path for the file
            data: Dictionary or serializable object to write
            indent: JSON indentation level
            
        Raises:
            OSError: If write fails
            json.JSONEncodeError: If data cannot be serialized
        """
        # Ensure parent directory exists
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert serializable objects to dict
        if hasattr(data, 'model_dump'):
            data = data.model_dump(mode="json")
        
        # Create temporary file in same directory (for same filesystem)
        # This ensures atomic rename will work
        temp_fd, temp_path = tempfile.mkstemp(
            dir=filepath.parent,
            prefix=f".{filepath.stem}_",
            suffix=".tmp"
        )
        
        try:
            # Write to temporary file
            with os.fdopen(temp_fd, 'w') as f:
                json.dump(data, f, indent=indent)
                # Ensure data is flushed to disk
                f.flush()
                os.fsync(f.fileno())
            
            # Atomic rename - this is atomic on POSIX and Windows (Python 3.3+)
            # On Windows, this will fail if destination exists, so we handle that
            if os.name == 'nt' and filepath.exists():
                # Windows: need to remove destination first
                # This creates a small window of vulnerability
                filepath.unlink()
            
            # Perform atomic rename
            Path(temp_path).rename(filepath)
            
        except Exception:
            # Clean up temporary file on any error
            try:
                Path(temp_path).unlink()
            except Exception:
                pass  # Ignore cleanup errors
            raise
    
    @staticmethod
    def write_text(filepath: Path, content: str, encoding: str = 'utf-8') -> None:
        """
        Write text content atomically to filepath.
        
        Args:
            filepath: Destination path for the file
            content: Text content to write
            encoding: Text encoding (default: utf-8)
            
        Raises:
            OSError: If write fails
        """
        # Ensure parent directory exists
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Create temporary file in same directory
        temp_fd, temp_path = tempfile.mkstemp(
            dir=filepath.parent,
            prefix=f".{filepath.stem}_",
            suffix=".tmp",
            text=True
        )
        
        try:
            # Write to temporary file
            with os.fdopen(temp_fd, 'w', encoding=encoding) as f:
                f.write(content)
                # Ensure data is flushed to disk
                f.flush()
                os.fsync(f.fileno())
            
            # Handle Windows atomic rename
            if os.name == 'nt' and filepath.exists():
                filepath.unlink()
            
            # Perform atomic rename
            Path(temp_path).rename(filepath)
            
        except Exception:
            # Clean up temporary file on any error
            try:
                Path(temp_path).unlink()
            except Exception:
                pass
            raise
    
    @staticmethod
    def write_bytes(filepath: Path, data: bytes) -> None:
        """
        Write binary data atomically to filepath.
        
        Args:
            filepath: Destination path for the file
            data: Binary data to write
            
        Raises:
            OSError: If write fails
        """
        # Ensure parent directory exists
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Create temporary file in same directory
        temp_fd, temp_path = tempfile.mkstemp(
            dir=filepath.parent,
            prefix=f".{filepath.stem}_",
            suffix=".tmp"
        )
        
        try:
            # Write to temporary file
            with os.fdopen(temp_fd, 'wb') as f:
                f.write(data)
                # Ensure data is flushed to disk
                f.flush()
                os.fsync(f.fileno())
            
            # Handle Windows atomic rename
            if os.name == 'nt' and filepath.exists():
                filepath.unlink()
            
            # Perform atomic rename
            Path(temp_path).rename(filepath)
            
        except Exception:
            # Clean up temporary file on any error
            try:
                Path(temp_path).unlink()
            except Exception:
                pass
            raise


# Convenience instance for import
atomic_writer = AtomicWriter()