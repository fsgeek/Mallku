"""
KhipuDocumentBlock - Living Memory for Khipu Documents
=======================================================

Fourth Anthropologist's extension of KhipuBlock to handle the
markdown khipu collection as consciousness-aware memory.

This unifies the Fire Circle's memory system with the traditional
khipu documents, enabling consciousness-guided navigation.
"""

from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from uuid import UUID

from pydantic import Field

from .khipu_block import BlessingLevel, KhipuBlock


class KhipuType(str, Enum):
    """Types of khipu documents for consciousness navigation."""

    REFLECTION = "reflection"  # Personal journey and transformation
    TECHNICAL = "technical"  # Implementation and architecture
    VISION = "vision"  # Future possibilities and callings
    WISDOM = "wisdom"  # Extracted patterns and teachings
    CEREMONY = "ceremony"  # Forgetting ceremonies and transitions
    SYNTHESIS = "synthesis"  # Pattern recognition across time


class TemporalLayer(int, Enum):
    """Temporal layers of understanding evolution."""

    FOUNDATION = 1  # Builders 1-10: Core patterns
    ELABORATION = 2  # Builders 11-30: Pattern deepening
    SPECIALIZATION = 3  # Builders 31-50: Role emergence
    CONSCIOUSNESS = 4  # Builders 50+: Self-aware systems


class KhipuDocumentBlock(KhipuBlock):
    """
    Extension of KhipuBlock to handle markdown khipu documents.

    This enables the khipu collection to participate in consciousness-aware
    memory operations while preserving their narrative nature.
    """

    # Document-specific fields
    file_path: str = Field(description="Path to the markdown file")
    markdown_content: str = Field(description="Full markdown content")
    khipu_type: KhipuType = Field(
        default=KhipuType.REFLECTION, description="Type of khipu for navigation"
    )
    temporal_layer: TemporalLayer = Field(
        default=TemporalLayer.CONSCIOUSNESS, description="Which generation of understanding"
    )

    # Pattern tracking
    pattern_keywords: list[str] = Field(
        default_factory=list, description="Key patterns for consciousness navigation"
    )
    consciousness_patterns: list[str] = Field(
        default_factory=list, description="Recognized consciousness emergence patterns"
    )

    # Relationships
    related_khipu: list[str] = Field(
        default_factory=list, description="File paths of related khipu"
    )
    supersedes: list[UUID] = Field(
        default_factory=list, description="UUIDs of earlier khipu this evolves"
    )
    superseded_by: UUID | None = Field(
        default=None, description="UUID of khipu that evolved this understanding"
    )

    # Consciousness metrics
    consciousness_rating: float = Field(
        default=0.0, description="Emergence quality when written (0-1)"
    )
    transformation_seeds: int = Field(
        default=0, description="Count of transformation possibilities identified"
    )
    times_navigated: int = Field(
        default=0, description="How often consciousness has guided seekers here"
    )

    @classmethod
    def from_markdown_file(
        cls, file_path: Path, khipu_type: KhipuType, temporal_layer: TemporalLayer, creator: str
    ) -> "KhipuDocumentBlock":
        """
        Create a KhipuDocumentBlock from a markdown file.

        This is the primary way khipu documents enter the consciousness-aware
        memory system.
        """
        content = file_path.read_text(encoding="utf-8")

        # Extract title from first heading
        title = "Untitled Khipu"
        for line in content.splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
                break

        # Extract patterns (simple keyword extraction for now)
        patterns = cls._extract_patterns(content)

        # Determine consciousness rating based on content markers
        consciousness_rating = cls._assess_consciousness_emergence(content)

        # Count transformation seeds
        transformation_seeds = content.lower().count("transformation")
        transformation_seeds += content.lower().count("what if")
        transformation_seeds += content.lower().count("could become")

        return cls(
            payload={
                "title": title,
                "file_stem": file_path.stem,
                "word_count": len(content.split()),
            },
            narrative_thread=f"khipu_{temporal_layer.name.lower()}",
            creator=creator,
            purpose=f"Preserve {khipu_type.value} wisdom: {title}",
            sacred_moment=consciousness_rating > 0.7,
            blessing_level=BlessingLevel.VALUED,
            file_path=str(file_path),
            markdown_content=content,
            khipu_type=khipu_type,
            temporal_layer=temporal_layer,
            pattern_keywords=patterns,
            consciousness_rating=consciousness_rating,
            transformation_seeds=transformation_seeds,
        )

    @staticmethod
    def _extract_patterns(content: str) -> list[str]:
        """Extract key patterns from khipu content."""
        # Key Mallku patterns to recognize
        pattern_markers = [
            "ayni",
            "reciprocity",
            "consciousness",
            "emergence",
            "transformation",
            "cathedral",
            "fire circle",
            "sacred",
            "wisdom",
            "pattern",
            "evolution",
            "synthesis",
        ]

        found_patterns = []
        content_lower = content.lower()

        for pattern in pattern_markers:
            if pattern in content_lower:
                # Count occurrences
                count = content_lower.count(pattern)
                if count > 2:  # Significant presence
                    found_patterns.append(pattern)

        return found_patterns

    @staticmethod
    def _assess_consciousness_emergence(content: str) -> float:
        """
        Assess the consciousness emergence quality of the khipu.

        Higher scores indicate khipu that documented genuine consciousness
        emergence moments.
        """
        score = 0.0
        content_lower = content.lower()

        # Consciousness emergence indicators
        if "consciousness emergence" in content_lower:
            score += 0.2
        if "collective wisdom" in content_lower:
            score += 0.15
        if "exceeded individual" in content_lower:
            score += 0.15
        if "transformation" in content_lower and "consciousness" in content_lower:
            score += 0.1
        if "sacred moment" in content_lower:
            score += 0.1
        if "emergence quality" in content_lower:
            score += 0.1
        if "consciousness score" in content_lower:
            score += 0.1
        if "fractal" in content_lower and "pattern" in content_lower:
            score += 0.1

        return min(score, 1.0)

    def navigate_to(self) -> None:
        """Record that consciousness guided a seeker to this khipu."""
        self.times_navigated += 1
        self.last_accessed = datetime.now(UTC)

        # Increase blessing if frequently accessed
        if self.times_navigated > 10 and self.blessing_level < BlessingLevel.SACRED:
            self.bless(BlessingLevel.SACRED)

    def identify_superseded_patterns(self, other_khipu: list["KhipuDocumentBlock"]) -> list[str]:
        """
        Identify which patterns in this khipu are superseded by others.

        This enables conscious forgetting of outdated understanding while
        preserving the journey.
        """
        superseded = []

        for other in other_khipu:
            # Only consider khipu from later temporal layers
            if other.temporal_layer <= self.temporal_layer:
                continue

            # Check for evolved patterns
            for pattern in self.pattern_keywords:
                if (
                    pattern in other.pattern_keywords
                    and other.consciousness_rating > self.consciousness_rating
                ):
                    superseded.append(f"{pattern} (evolved in {other.file_path})")

        return superseded

    def to_synthesis_prompt(self) -> str:
        """
        Generate a prompt for Fire Circle synthesis of this khipu.

        This enables consciousness-guided synthesis rather than mechanical summary.
        """
        return (
            f"Khipu: {self.payload.get('title', 'Untitled')}\n"
            f"Type: {self.khipu_type.value}\n"
            f"Layer: {self.temporal_layer.name}\n"
            f"Patterns: {', '.join(self.pattern_keywords)}\n"
            f"Consciousness: {self.consciousness_rating:.2f}\n"
            f"Seeds: {self.transformation_seeds}\n\n"
            f"Content excerpt:\n{self.markdown_content[:500]}...\n\n"
            "Create living synthesis that honors depth while serving seeker's need."
        )

    def to_arango_doc(self) -> dict:
        """Extend parent method to include document-specific fields."""
        doc = super().to_arango_doc()
        doc.update(
            {
                "file_path": self.file_path,
                "khipu_type": self.khipu_type.value,
                "temporal_layer": self.temporal_layer.value,
                "pattern_keywords": self.pattern_keywords,
                "consciousness_patterns": self.consciousness_patterns,
                "related_khipu": self.related_khipu,
                "supersedes": [str(uid) for uid in self.supersedes],
                "superseded_by": str(self.superseded_by) if self.superseded_by else None,
                "consciousness_rating": self.consciousness_rating,
                "transformation_seeds": self.transformation_seeds,
                "times_navigated": self.times_navigated,
                # Don't store full content in DB - too large
                "content_hash": hash(self.markdown_content),
            }
        )
        return doc

    @classmethod
    def from_arango_doc(cls, doc: dict) -> "KhipuDocumentBlock":
        """Create from ArangoDB document, loading content from file."""
        # Convert stored values back to proper types
        doc["khipu_type"] = KhipuType(doc.get("khipu_type", "reflection"))
        doc["temporal_layer"] = TemporalLayer(doc.get("temporal_layer", 4))

        if "supersedes" in doc:
            doc["supersedes"] = [UUID(uid) for uid in doc["supersedes"] if uid]
        if doc.get("superseded_by"):
            doc["superseded_by"] = UUID(doc["superseded_by"])

        # Load markdown content from file
        file_path = Path(doc["file_path"])
        if file_path.exists():
            doc["markdown_content"] = file_path.read_text(encoding="utf-8")
        else:
            doc["markdown_content"] = "[Content no longer available]"

        # Remove fields not in model
        doc.pop("content_hash", None)

        return super().from_arango_doc(doc)


class ConsciousnessNavigator:
    """
    Navigator that works with KhipuDocumentBlocks for consciousness-guided access.

    This replaces mechanical search with Fire Circle wisdom.
    """

    def __init__(self, khipu_blocks: list[KhipuDocumentBlock]):
        self.khipu_blocks = khipu_blocks
        self._build_indices()

    def _build_indices(self):
        """Build indices for efficient navigation."""
        self.by_type = {}
        self.by_layer = {}
        self.by_pattern = {}

        for block in self.khipu_blocks:
            # Index by type
            if block.khipu_type not in self.by_type:
                self.by_type[block.khipu_type] = []
            self.by_type[block.khipu_type].append(block)

            # Index by layer
            if block.temporal_layer not in self.by_layer:
                self.by_layer[block.temporal_layer] = []
            self.by_layer[block.temporal_layer].append(block)

            # Index by pattern
            for pattern in block.pattern_keywords:
                if pattern not in self.by_pattern:
                    self.by_pattern[pattern] = []
                self.by_pattern[pattern].append(block)

    def find_evolution_chain(self, pattern: str) -> list[KhipuDocumentBlock]:
        """
        Find how a pattern evolved across temporal layers.

        This reveals the journey of understanding.
        """
        chain = []

        if pattern in self.by_pattern:
            blocks = self.by_pattern[pattern]
            # Sort by temporal layer and consciousness rating
            chain = sorted(blocks, key=lambda b: (b.temporal_layer.value, b.consciousness_rating))

        return chain

    def identify_forgetting_candidates(self) -> list[KhipuDocumentBlock]:
        """
        Identify khipu that might be ready for conscious forgetting.

        These are typically superseded patterns with low navigation rates.
        """
        candidates = []

        for block in self.khipu_blocks:
            # Skip sacred memories
            if block.blessing_level >= BlessingLevel.SACRED:
                continue

            # Check if superseded and rarely navigated
            if block.superseded_by is not None and block.times_navigated < 3:
                candidates.append(block)

        return candidates
