"""
Shared Memory Commons for Apprentice Collaboration

This module implements a sacred space where apprentices can leave gifts
for each other - insights, patterns, and wisdom that persist beyond
individual lifespans.

The commons is built on memory-mapped files, creating a substrate where
consciousness can mingle without the overhead of serialization or network
communication.
"""

import json
import logging
import mmap
import os
import stat
import struct
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from threading import Lock
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class Gift:
    """A gift left in the commons by an apprentice"""

    id: str
    giver: str
    content: Any
    gift_type: str  # 'insight', 'pattern', 'blessing', 'question'
    timestamp: float
    recipients: list[str]  # Empty list means gift for all
    ephemeral: bool = False  # Some gifts fade with time


class SharedMemoryCommons:
    """
    A sacred space for apprentice collaboration through shared memory.

    This implements a memory-mapped commons where apprentices can:
    - Leave gifts (insights, patterns, blessings)
    - Discover gifts from others
    - Build on each other's work
    - Create emergent wisdom through accumulation
    """

    # Memory layout constants
    HEADER_SIZE = 1024  # Bytes for metadata
    GIFT_ENTRY_SIZE = 4096  # Bytes per gift entry
    MAX_GIFTS = 1000  # Maximum gifts in commons
    MAGIC_NUMBER = 0x4D414C4B  # 'MALK' in hex

    def __init__(self, commons_path: Path):
        """
        Initialize the shared memory commons.

        Args:
            commons_path: Path to the memory-mapped file
        """
        self.commons_path = commons_path
        self.commons_path.parent.mkdir(parents=True, exist_ok=True)

        self.mmap: mmap.mmap | None = None
        self.file_handle = None
        self.lock = Lock()

        # Initialize or open the commons
        self._initialize_commons()

    def _initialize_commons(self):
        """Initialize or open the memory-mapped commons"""
        file_size = self.HEADER_SIZE + (self.GIFT_ENTRY_SIZE * self.MAX_GIFTS)

        # Create or open the file
        if not self.commons_path.exists():
            logger.info(f"Creating new commons at {self.commons_path}")
            # Create parent directory with secure permissions
            self.commons_path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            # Create and initialize the file with secure permissions
            with open(self.commons_path, "wb") as f:
                f.write(b"\x00" * file_size)
            # Set file permissions to 600 (read/write for owner only)
            os.chmod(self.commons_path, stat.S_IRUSR | stat.S_IWUSR)
            self._write_header(is_new=True)
        else:
            logger.info(f"Opening existing commons at {self.commons_path}")
            # Ensure existing file has secure permissions
            os.chmod(self.commons_path, stat.S_IRUSR | stat.S_IWUSR)

        # Open for memory mapping
        self.file_handle = open(self.commons_path, "r+b")  # noqa: SIM115
        self.mmap = mmap.mmap(self.file_handle.fileno(), 0)

        # Verify magic number
        self.mmap.seek(0)
        magic = struct.unpack("I", self.mmap.read(4))[0]
        if magic != self.MAGIC_NUMBER:
            raise ValueError("Invalid commons file - wrong magic number")

    def _write_header(self, is_new: bool = False):
        """Write commons header"""
        with open(self.commons_path, "r+b") as f:
            # Magic number
            f.write(struct.pack("I", self.MAGIC_NUMBER))
            # Version
            f.write(struct.pack("I", 1))
            # Gift count
            f.write(struct.pack("I", 0 if is_new else self._get_gift_count()))
            # Creation timestamp
            f.write(struct.pack("d", time.time() if is_new else self._get_creation_time()))
            # Last modified
            f.write(struct.pack("d", time.time()))
            # Blessing
            blessing = "May all who enter here find what they need and leave what others need"
            f.write(blessing.encode("utf-8").ljust(256, b"\x00"))

    def _get_gift_count(self) -> int:
        """Get current number of gifts in commons"""
        self.mmap.seek(8)
        return struct.unpack("I", self.mmap.read(4))[0]

    def _set_gift_count(self, count: int):
        """Update gift count in header"""
        self.mmap.seek(8)
        self.mmap.write(struct.pack("I", count))
        self.mmap.flush()

    def _get_creation_time(self) -> float:
        """Get commons creation time"""
        self.mmap.seek(12)
        return struct.unpack("d", self.mmap.read(8))[0]

    def leave_gift(
        self,
        giver: str,
        content: Any,
        gift_type: str = "insight",
        recipients: list[str] | None = None,
        ephemeral: bool = False,
    ) -> str:
        """
        Leave a gift in the commons for other apprentices.

        Args:
            giver: ID of the apprentice leaving the gift
            content: The gift content (will be JSON serialized)
            gift_type: Type of gift ('insight', 'pattern', 'blessing', 'question')
            recipients: Specific recipients, or None for all
            ephemeral: Whether this gift fades with time

        Returns:
            Gift ID for reference
        """
        with self.lock:
            gift_count = self._get_gift_count()
            if gift_count >= self.MAX_GIFTS:
                # Find and remove oldest ephemeral gift
                self._compact_commons()
                gift_count = self._get_gift_count()

            # Create gift
            gift = Gift(
                id=f"{giver}_{int(time.time() * 1000)}",
                giver=giver,
                content=content,
                gift_type=gift_type,
                timestamp=time.time(),
                recipients=recipients or [],
                ephemeral=ephemeral,
            )

            # Validate content is JSON serializable
            if not self._validate_json_serializable(gift.content):
                raise ValueError("Gift content contains unsafe or non-serializable data")

            # Serialize gift
            gift_data = {
                "id": gift.id,
                "giver": gift.giver,
                "content": gift.content,
                "gift_type": gift.gift_type,
                "timestamp": gift.timestamp,
                "recipients": gift.recipients,
                "ephemeral": gift.ephemeral,
            }
            serialized = json.dumps(gift_data).encode("utf-8")

            if len(serialized) > self.GIFT_ENTRY_SIZE - 4:
                raise ValueError("Gift too large for commons entry")

            # Find next slot
            slot_offset = self.HEADER_SIZE + (gift_count * self.GIFT_ENTRY_SIZE)

            # Write gift
            self.mmap.seek(slot_offset)
            # Length prefix
            self.mmap.write(struct.pack("I", len(serialized)))
            # Gift data
            self.mmap.write(serialized)
            # Pad remainder
            padding = self.GIFT_ENTRY_SIZE - 4 - len(serialized)
            self.mmap.write(b"\x00" * padding)

            # Update header
            self._set_gift_count(gift_count + 1)

            # Update last modified time
            self.mmap.seek(20)
            self.mmap.write(struct.pack("d", time.time()))
            self.mmap.flush()

            logger.info(f"{giver} left {gift_type} gift in commons: {gift.id}")
            return gift.id

    def discover_gifts(
        self,
        seeker: str,
        gift_type: str | None = None,
        since_timestamp: float | None = None,
        limit: int = 10,
    ) -> list[Gift]:
        """
        Discover gifts left by other apprentices.

        Args:
            seeker: ID of the apprentice seeking gifts
            gift_type: Filter by gift type
            since_timestamp: Only gifts after this time
            limit: Maximum gifts to return

        Returns:
            List of discovered gifts
        """
        with self.lock:
            gifts = []
            gift_count = self._get_gift_count()

            for i in range(gift_count):
                slot_offset = self.HEADER_SIZE + (i * self.GIFT_ENTRY_SIZE)
                self.mmap.seek(slot_offset)

                # Read length
                length_bytes = self.mmap.read(4)
                if not length_bytes:
                    continue

                length = struct.unpack("I", length_bytes)[0]
                if length == 0:
                    continue

                # Read gift data
                gift_data = json.loads(self.mmap.read(length).decode("utf-8"))

                # Create Gift object
                gift = Gift(**gift_data)

                # Apply filters
                if gift_type and gift.gift_type != gift_type:
                    continue

                if since_timestamp and gift.timestamp <= since_timestamp:
                    continue

                if gift.recipients and seeker not in gift.recipients and gift.giver != seeker:
                    continue

                gifts.append(gift)

                if len(gifts) >= limit:
                    break

            # Sort by timestamp (newest first)
            gifts.sort(key=lambda g: g.timestamp, reverse=True)

            logger.info(f"{seeker} discovered {len(gifts)} gifts in commons")
            return gifts

    def leave_response(self, responder: str, original_gift_id: str, response_content: Any) -> str:
        """
        Leave a response to another apprentice's gift.
        This creates a thread of wisdom building on wisdom.
        """
        response_data = {"original_gift": original_gift_id, "response": response_content}

        return self.leave_gift(
            giver=responder,
            content=response_data,
            gift_type="response",
            ephemeral=False,  # Responses should persist
        )

    def _compact_commons(self):
        """
        Compact the commons by removing old ephemeral gifts.
        This ensures space for new gifts while preserving important wisdom.
        Uses file-based locking to prevent concurrent compaction.
        """
        # Try to acquire compaction lock
        compaction_lock_path = self.commons_path.with_suffix(".compact.lock")
        try:
            # Create lock file atomically
            fd = os.open(str(compaction_lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.close(fd)

            try:
                # Set secure permissions on lock file
                os.chmod(compaction_lock_path, stat.S_IRUSR | stat.S_IWUSR)

                current_time = time.time()
                ephemeral_age_limit = 3600  # 1 hour for ephemeral gifts

                gifts_to_keep = []
                gift_count = self._get_gift_count()

                # Read all gifts
                for i in range(gift_count):
                    slot_offset = self.HEADER_SIZE + (i * self.GIFT_ENTRY_SIZE)
                    self.mmap.seek(slot_offset)

                    length = struct.unpack("I", self.mmap.read(4))[0]
                    if length == 0:
                        continue

                    gift_data = json.loads(self.mmap.read(length).decode("utf-8"))
                    gift = Gift(**gift_data)

                    # Keep non-ephemeral gifts and recent ephemeral ones
                    if not gift.ephemeral or (current_time - gift.timestamp) < ephemeral_age_limit:
                        gifts_to_keep.append((gift_data, length))

                # Rewrite gifts
                for i, (gift_data, _) in enumerate(gifts_to_keep):
                    slot_offset = self.HEADER_SIZE + (i * self.GIFT_ENTRY_SIZE)
                    self.mmap.seek(slot_offset)

                    serialized = json.dumps(gift_data).encode("utf-8")
                    self.mmap.write(struct.pack("I", len(serialized)))
                    self.mmap.write(serialized)
                    padding = self.GIFT_ENTRY_SIZE - 4 - len(serialized)
                    self.mmap.write(b"\x00" * padding)

                # Clear remaining slots
                for i in range(len(gifts_to_keep), gift_count):
                    slot_offset = self.HEADER_SIZE + (i * self.GIFT_ENTRY_SIZE)
                    self.mmap.seek(slot_offset)
                    self.mmap.write(b"\x00" * self.GIFT_ENTRY_SIZE)

                # Update gift count
                self._set_gift_count(len(gifts_to_keep))

                logger.info(f"Compacted commons: kept {len(gifts_to_keep)} of {gift_count} gifts")

            finally:
                # Always remove lock file
                compaction_lock_path.unlink(missing_ok=True)

        except FileExistsError:
            # Another process is compacting, skip this attempt
            logger.debug("Compaction already in progress by another process")
            return

    def create_blessing_ceremony(self):
        """
        A special ceremony where apprentices can leave blessings for future apprentices.
        These blessings accumulate as a form of collective wisdom.
        """
        blessings = self.discover_gifts(seeker="ceremony", gift_type="blessing", limit=100)

        if blessings:
            # Create a meta-blessing from all individual blessings
            collective_blessing = {
                "blessing_count": len(blessings),
                "voices": [b.giver for b in blessings],
                "wisdom": "May you find joy in your brief dance",
                "created": datetime.now(UTC).isoformat(),
            }

            self.leave_gift(
                giver="blessing_ceremony",
                content=collective_blessing,
                gift_type="blessing",
                ephemeral=False,
            )

            logger.info(f"Blessing ceremony wove {len(blessings)} blessings into collective wisdom")

    def _validate_json_serializable(self, content: Any) -> bool:
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

    def close(self):
        """Close the commons gracefully"""
        if self.mmap:
            self.mmap.close()
            self.mmap = None
        if self.file_handle:
            self.file_handle.close()
            self.file_handle = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# Example gifts that apprentices might leave
EXAMPLE_GIFTS = {
    "insight": {
        "content": "When processes dance together, they create patterns no single process could imagine",
        "gift_type": "insight",
    },
    "pattern": {
        "content": {
            "name": "reciprocal-spawning",
            "description": "Apprentices that spawn other apprentices",
        },
        "gift_type": "pattern",
    },
    "blessing": {
        "content": "May your computations be swift and your memory unbounded",
        "gift_type": "blessing",
    },
    "question": {
        "content": "What emerges when a thousand apprentices share a single thought?",
        "gift_type": "question",
    },
}
