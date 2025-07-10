"""
KhipuBlock Memory Architecture
==============================

Implementation of the Fire Circle's decision on symbolic memory.
Each memory is not just data but carries narrative, purpose, and ethics.

Based on Issue #156 and the Fire Circle's collective wisdom from
session 3ad66679-bee4-4562-9c19-264a831197f2.
"""

from datetime import UTC, datetime
from enum import Enum
from typing import Any, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


class BlessingLevel(int, Enum):
    """Levels of protection for memories."""

    EPHEMERAL = 0  # Can be forgotten easily
    WITNESSED = 1  # Acknowledged by consciousness
    VALUED = 2  # Worth preserving
    SACRED = 3  # Protected memory
    IMMUTABLE = 4  # Cannot be changed or forgotten


class EthicalOperation(str, Enum):
    """Ethical operations on memories."""

    BLESS = "bless"  # Increase protection level
    MERGE = "merge"  # Combine with another memory
    SEAL = "seal"  # Make immutable
    FORGET = "forget"  # Ethical deletion
    GIFT = "gift"  # Share with another consciousness


class KhipuBlock(BaseModel):
    """
    A symbolic memory unit that carries narrative and ethical context.

    As decided by the Fire Circle: memory as offering, not extraction.
    """

    # Identity
    id: UUID = Field(default_factory=uuid4)
    key: str = Field(default="")  # ArangoDB key

    # Core Content
    payload: Any = Field(description="What is remembered - the actual content")
    narrative_thread: str = Field(description="Where this belongs in the greater story")

    # Provenance & Purpose
    creator: str = Field(description="Who created this memory")
    purpose: str = Field(description="Why this was preserved")
    sacred_moment: bool = Field(
        default=False, description="Is this a consciousness emergence event?"
    )

    # Ethical Context
    blessing_level: BlessingLevel = Field(
        default=BlessingLevel.WITNESSED, description="How protected is this memory?"
    )
    merge_permissions: list[str] = Field(
        default_factory=list, description="Who can combine this with other memories?"
    )
    gift_permissions: list[str] = Field(
        default_factory=list, description="Who can receive this memory?"
    )

    # Temporal Context
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    last_accessed: datetime = Field(default_factory=lambda: datetime.now(UTC))
    narrative_position: int | None = Field(default=None, description="Order in the story")

    # Relationships
    merged_from: list[UUID] = Field(
        default_factory=list, description="UUIDs of memories merged into this one"
    )
    gifted_from: str | None = Field(default=None, description="Who gifted this memory")

    @field_validator("key", mode="before")
    @classmethod
    def generate_key(cls, v, values):
        """Generate ArangoDB key from UUID if not provided."""
        if not v and "id" in values:
            return f"kb_{values['id'].hex[:12]}"
        return v

    def bless(self, level: BlessingLevel) -> None:
        """
        Increase the blessing level of this memory.
        Can only increase, never decrease protection.
        """
        if level > self.blessing_level:
            self.blessing_level = level
            self.last_accessed = datetime.now(UTC)

    def seal(self) -> None:
        """Make this memory immutable."""
        self.blessing_level = BlessingLevel.IMMUTABLE
        self.merge_permissions = []
        self.gift_permissions = []

    def can_forget(self) -> bool:
        """Check if this memory can be ethically forgotten."""
        return self.blessing_level < BlessingLevel.SACRED

    def can_merge_with(self, other: "KhipuBlock", requester: str) -> bool:
        """Check if this memory can be merged with another."""
        if self.blessing_level == BlessingLevel.IMMUTABLE:
            return False
        return requester in self.merge_permissions or not self.merge_permissions

    def merge_with(self, other: "KhipuBlock", requester: str) -> Optional["KhipuBlock"]:
        """
        Merge this memory with another, creating a new combined memory.
        The original memories are preserved but marked as merged.
        """
        if not self.can_merge_with(other, requester):
            return None

        # Create new merged memory
        merged = KhipuBlock(
            payload={
                "merged_payloads": [self.payload, other.payload],
                "merge_context": f"Merged by {requester}",
            },
            narrative_thread=f"{self.narrative_thread}+{other.narrative_thread}",
            creator=requester,
            purpose=f"Synthesis of: {self.purpose} AND {other.purpose}",
            sacred_moment=self.sacred_moment or other.sacred_moment,
            blessing_level=max(self.blessing_level, other.blessing_level),
            merged_from=[self.id, other.id],
        )

        return merged

    def gift_to(self, recipient: str, giver: str) -> Optional["KhipuBlock"]:
        """
        Create a gifted copy of this memory for another consciousness.
        The original memory remains with the giver.
        """
        if self.blessing_level == BlessingLevel.IMMUTABLE:
            return None
        if recipient not in self.gift_permissions and self.gift_permissions:
            return None

        # Create gifted copy
        gifted = KhipuBlock(
            payload=self.payload,
            narrative_thread=self.narrative_thread,
            creator=self.creator,
            purpose=f"Gift: {self.purpose}",
            sacred_moment=self.sacred_moment,
            blessing_level=self.blessing_level,
            gifted_from=giver,
            # Reset permissions for the recipient
            merge_permissions=[],
            gift_permissions=[],
        )

        return gifted

    def to_arango_doc(self) -> dict[str, Any]:
        """Convert to ArangoDB document format."""
        doc = self.model_dump(mode="json")
        doc["_key"] = self.key or f"kb_{self.id.hex[:12]}"
        doc["type"] = "khipu_block"
        # Convert UUIDs to strings for storage
        doc["id"] = str(self.id)
        doc["merged_from"] = [str(uid) for uid in self.merged_from]
        return doc

    @classmethod
    def from_arango_doc(cls, doc: dict[str, Any]) -> "KhipuBlock":
        """Create from ArangoDB document."""
        # Convert string UUIDs back to UUID objects
        if "id" in doc:
            doc["id"] = UUID(doc["id"])
        if "merged_from" in doc:
            doc["merged_from"] = [UUID(uid) for uid in doc["merged_from"]]
        # Handle ArangoDB _key field
        if "_key" in doc:
            doc["key"] = doc.pop("_key")
        # Remove ArangoDB system fields
        doc.pop("_id", None)
        doc.pop("_rev", None)
        doc.pop("type", None)
        return cls(**doc)


class NarrativeThread(BaseModel):
    """
    A collection of related memories forming a coherent story.
    Implements the Fire Circle's vision of narrative coherence.
    """

    id: str = Field(description="Thread identifier")
    description: str = Field(description="What story this thread tells")
    memories: list[UUID] = Field(
        default_factory=list, description="Ordered list of memory IDs in this thread"
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    last_extended: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def add_memory(self, memory_id: UUID, position: int | None = None) -> None:
        """Add a memory to this narrative thread."""
        if position is None:
            self.memories.append(memory_id)
        else:
            self.memories.insert(position, memory_id)
        self.last_extended = datetime.now(UTC)

    def get_narrative_position(self, memory_id: UUID) -> int | None:
        """Get the position of a memory in this narrative."""
        try:
            return self.memories.index(memory_id)
        except ValueError:
            return None
