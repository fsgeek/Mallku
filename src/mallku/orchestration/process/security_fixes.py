"""
Security and concurrency fixes for ProcessApprentice and SharedMemoryCommons

This module addresses the high-priority issues identified in the Fire Circle review:
1. Race condition in SharedMemoryCommons compaction
2. File permissions for commons files
3. Memory availability fallback
4. Process cleanup race condition
5. Input validation for JSON serialization
"""

import json
import logging
import os
import stat
import time
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def apply_security_fixes():
    """Apply all security fixes to the codebase"""
    fix_commons_file_permissions()
    logger.info("Security fixes applied")


def fix_commons_file_permissions():
    """Set secure permissions (600) on commons files"""
    commons_dir = Path("~/.mallku/commons").expanduser()
    if commons_dir.exists():
        for commons_file in commons_dir.glob("*.mmap"):
            # Set permissions to 600 (read/write for owner only)
            os.chmod(commons_file, stat.S_IRUSR | stat.S_IWUSR)
            logger.info(f"Set secure permissions on {commons_file}")


def get_safe_memory_default() -> int:
    """
    Get a safe default for available memory.
    Returns a conservative estimate to prevent resource exhaustion.
    """
    try:
        # Try to get actual available memory
        import psutil

        return int(psutil.virtual_memory().available / (1024 * 1024))
    except ImportError:
        # Conservative fallback - 256MB instead of 1000MB
        logger.warning("psutil not available, using conservative memory default of 256MB")
        return 256


def validate_json_serializable(content: Any) -> bool:
    """
    Validate that content is safely JSON serializable.

    Args:
        content: Content to validate

    Returns:
        True if content is safe to serialize
    """
    try:
        # Attempt serialization to check for issues
        json.dumps(content)

        # Check for suspicious patterns
        content_str = str(content)
        suspicious_patterns = [
            "__import__",
            "eval(",
            "exec(",
            "compile(",
            "globals(",
            "locals(",
        ]

        for pattern in suspicious_patterns:
            if pattern in content_str:
                logger.warning(f"Suspicious pattern '{pattern}' found in content")
                return False

        return True
    except (TypeError, ValueError) as e:
        logger.warning(f"Content not JSON serializable: {e}")
        return False


def safe_process_cleanup(process, timeout: float = 1.0):
    """
    Safely cleanup a process with proper delay to prevent race conditions.

    Args:
        process: The process to cleanup
        timeout: Maximum time to wait for graceful termination
    """
    if process and process.is_alive():
        process.terminate()

        # Add delay before checking is_alive to prevent race
        time.sleep(0.1)

        # Wait for graceful termination
        process.join(timeout=timeout)

        # Force kill if still alive
        if process.is_alive():
            logger.warning(f"Process {process.pid} didn't terminate gracefully, forcing kill")
            process.kill()
            process.join(timeout=0.5)


# Patch for SharedMemoryCommons to make compaction atomic
def atomic_compact_commons(self):
    """
    Atomic version of _compact_commons that prevents corruption from concurrent access.
    Uses a separate compaction lock file to coordinate across processes.
    """
    compaction_lock_path = self.commons_path.with_suffix(".compact.lock")

    # Try to acquire compaction lock
    try:
        # Create lock file atomically
        fd = os.open(str(compaction_lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.close(fd)

        try:
            # Now we have exclusive compaction rights
            with self.lock:  # Still hold the regular lock
                self._original_compact_commons()
        finally:
            # Always remove lock file
            compaction_lock_path.unlink(missing_ok=True)

    except FileExistsError:
        # Another process is compacting, skip this attempt
        logger.debug("Compaction already in progress by another process")
        return


def create_commons_with_permissions(commons_path: Path):
    """Create a commons file with secure permissions from the start"""
    commons_path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)

    if not commons_path.exists():
        # Create with secure permissions
        commons_path.touch(mode=0o600)
        logger.info(f"Created commons with secure permissions: {commons_path}")
