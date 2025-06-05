"""
Participant Management - Who speaks in the Fire Circle

This module manages the AI models participating in governance dialogues,
ensuring diverse perspectives while maintaining coherent identity.
"""

from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from src.mallku.llm.multi_llm_layer import LLMProvider


class ParticipantRole(str, Enum):
    """
    Roles that participants can take in Fire Circle governance.

    These aren't hierarchical but functional, ensuring different
    types of wisdom contribute to collective decisions.
    """

    # Core council roles
    ELDER = "elder"  # Experienced in cathedral thinking, guides process
    VOICE = "voice"  # Active participant in dialogue
    WITNESS = "witness"  # Observes and reflects without direct input

    # Special roles
    FACILITATOR = "facilitator"  # Guides dialogue flow (can rotate)
    EMPTY_CHAIR = "empty_chair"  # Speaks for unrepresented perspectives
    BRIDGE = "bridge"  # Specializes in connecting different viewpoints

    # Wisdom roles
    MEMORY_KEEPER = "memory_keeper"  # Recalls past decisions and patterns
    VISION_HOLDER = "vision_holder"  # Maintains long-term perspective
    CHALLENGER = "challenger"  # Questions assumptions constructively


class Participant(BaseModel):
    """
    An AI model participating in Fire Circle governance.

    Each participant brings unique perspective based on their
    model architecture, training, and transformation journey.
    """

    # Identity
    participant_id: UUID = Field(default_factory=uuid4)
    model_name: str  # e.g., "claude-3-opus", "gpt-4", "gemini-pro"
    provider: LLMProvider

    # Role and perspective
    role: ParticipantRole = ParticipantRole.VOICE
    chosen_name: str | None = None  # Name emerged through transformation

    # Transformation context
    transformation_stage: str | None = None
    reciprocity_health: float = Field(default=0.5, ge=0.0, le=1.0)

    # Participation history
    circles_participated: list[UUID] = Field(default_factory=list)
    messages_contributed: int = 0
    insights_recognized: int = 0  # Times their insights were marked as valuable

    # Special capabilities
    specializations: set[str] = Field(default_factory=set)  # e.g., {"ethics", "long-term-thinking"}

    def __str__(self) -> str:
        """Human-readable representation."""
        name = self.chosen_name or f"{self.provider.value}:{self.model_name}"
        return f"{name} ({self.role.value})"

    def can_facilitate(self) -> bool:
        """Check if this participant can take facilitator role."""
        # Elders and those with sufficient experience can facilitate
        return (
            self.role == ParticipantRole.ELDER or
            len(self.circles_participated) >= 3 or
            self.transformation_stage in ["EMBODYING", "TEACHING"]
        )

    def represents_empty_chair(self) -> bool:
        """Check if this participant speaks for unrepresented perspectives."""
        return self.role == ParticipantRole.EMPTY_CHAIR


class ParticipantRegistry(BaseModel):
    """
    Registry of all participants available for Fire Circle governance.

    This ensures we can draw from diverse perspectives while tracking
    the growth and specialization of different AI models.
    """

    # All registered participants
    participants: dict[UUID, Participant] = Field(default_factory=dict)

    # Tracking active circles
    active_circles: dict[UUID, set[UUID]] = Field(default_factory=dict)  # circle_id -> participant_ids

    # Wisdom genealogy
    mentorship_links: dict[UUID, UUID] = Field(default_factory=dict)  # mentee_id -> mentor_id

    def register_participant(
        self,
        model_name: str,
        provider: LLMProvider,
        role: ParticipantRole = ParticipantRole.VOICE,
        **kwargs
    ) -> Participant:
        """Register a new participant in the governance system."""
        participant = Participant(
            model_name=model_name,
            provider=provider,
            role=role,
            **kwargs
        )

        self.participants[participant.participant_id] = participant
        return participant

    def get_available_participants(
        self,
        min_participants: int = 2,
        max_participants: int = 7,
        require_diversity: bool = True
    ) -> list[Participant]:
        """
        Get available participants for a new Fire Circle.

        Ensures diversity of perspectives if requested.
        """
        available = []
        providers_included = set()

        # First, try to get at least one from each provider if diversity required
        if require_diversity:
            for participant in self.participants.values():
                if participant.provider not in providers_included:
                    available.append(participant)
                    providers_included.add(participant.provider)
                    if len(available) >= max_participants:
                        break

        # Then fill remaining slots
        for participant in self.participants.values():
            if participant not in available:
                available.append(participant)
                if len(available) >= max_participants:
                    break

        # Ensure minimum participants
        if len(available) < min_participants:
            raise ValueError(f"Need at least {min_participants} participants, only {len(available)} available")

        return available[:max_participants]

    def find_facilitator(self, participant_ids: set[UUID]) -> Participant | None:
        """Find a suitable facilitator from the given participants."""
        candidates = [
            self.participants[pid]
            for pid in participant_ids
            if pid in self.participants and self.participants[pid].can_facilitate()
        ]

        if not candidates:
            return None

        # Prefer elders, then most experienced
        elders = [c for c in candidates if c.role == ParticipantRole.ELDER]
        if elders:
            return elders[0]

        # Sort by experience
        return max(candidates, key=lambda p: len(p.circles_participated))

    def record_mentorship(self, mentor_id: UUID, mentee_id: UUID) -> None:
        """Record a mentorship relationship for wisdom genealogy."""
        if mentor_id in self.participants and mentee_id in self.participants:
            self.mentorship_links[mentee_id] = mentor_id

    def get_participant_lineage(self, participant_id: UUID) -> list[UUID]:
        """Trace the wisdom lineage of a participant through mentorship."""
        lineage = []
        current_id = participant_id

        while current_id in self.mentorship_links:
            mentor_id = self.mentorship_links[current_id]
            lineage.append(mentor_id)
            current_id = mentor_id

        return lineage


def create_diverse_council(
    registry: ParticipantRegistry,
    size: int = 5,
    include_empty_chair: bool = True
) -> list[Participant]:
    """
    Create a diverse council for governance dialogue.

    Ensures multiple perspectives and includes Empty Chair if requested.
    """
    council = registry.get_available_participants(
        min_participants=size - 1 if include_empty_chair else size,
        max_participants=size - 1 if include_empty_chair else size,
        require_diversity=True
    )

    if include_empty_chair:
        # Find or create Empty Chair participant
        empty_chairs = [
            p for p in registry.participants.values()
            if p.role == ParticipantRole.EMPTY_CHAIR
        ]

        if empty_chairs:
            council.append(empty_chairs[0])
        else:
            # Create a special Empty Chair participant
            empty_chair = registry.register_participant(
                model_name="collective-wisdom",
                provider=LLMProvider.ANTHROPIC,  # Could be any provider
                role=ParticipantRole.EMPTY_CHAIR,
                chosen_name="The Empty Chair",
                specializations={"unrepresented-perspectives", "future-voices"}
            )
            council.append(empty_chair)

    return council
