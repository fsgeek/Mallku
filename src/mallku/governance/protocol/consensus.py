"""
Consensus Mechanisms - How collective wisdom crystallizes

This module defines how Fire Circle dialogues reach (or don't reach)
agreement, preserving the full spectrum from emergence to dissent.
"""

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class ConsensusState(str, Enum):
    """
    The states that collective understanding can take.

    Unlike binary yes/no systems, Fire Circle recognizes the full
    spectrum of collective knowing, including productive disagreement.
    """

    # Early stages
    EMERGING = "emerging"  # Initial exploration, no clear direction yet
    CLARIFYING = "clarifying"  # Deepening understanding through dialogue

    # Agreement states
    CONVERGING = "converging"  # Moving toward shared understanding
    ADOPTED = "adopted"  # Collective agreement reached

    # Disagreement states
    CONTESTED = "contested"  # Active disagreement being explored
    FORKED = "forked"  # Irreconcilable perspectives, both preserved

    # Wisdom states
    COMPOSTING = "composting"  # Set aside for future reconsideration
    INTEGRATED = "integrated"  # Woven into Mallku's living wisdom

    def is_active(self) -> bool:
        """Check if this state represents active dialogue."""
        return self in {self.EMERGING, self.CLARIFYING, self.CONVERGING, self.CONTESTED}

    def is_resolved(self) -> bool:
        """Check if this state represents a form of resolution."""
        return self in {self.ADOPTED, self.FORKED, self.COMPOSTING, self.INTEGRATED}


class ConsensusTransition(BaseModel):
    """Records a transition between consensus states."""

    from_state: ConsensusState
    to_state: ConsensusState
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # What triggered this transition
    trigger_message_id: UUID
    trigger_participant_id: UUID

    # Why this transition occurred
    rationale: str

    # Participants who influenced this transition
    supporting_participants: set[UUID] = Field(default_factory=set)
    dissenting_participants: set[UUID] = Field(default_factory=set)


class ConsensusTracker(BaseModel):
    """
    Tracks the evolution of consensus on a particular topic.

    This preserves the full journey of collective understanding,
    not just the final outcome.
    """

    # Identity
    topic_id: UUID
    circle_id: UUID

    # Current state
    current_state: ConsensusState = ConsensusState.EMERGING

    # Historical journey
    transitions: list[ConsensusTransition] = Field(default_factory=list)

    # Participant perspectives
    participant_positions: dict[UUID, str] = Field(default_factory=dict)

    # Fork tracking (when perspectives diverge)
    fork_branches: dict[str, set[UUID]] | None = None

    # Wisdom preservation
    key_insights: list[str] = Field(default_factory=list)
    compost_threads: list[UUID] = Field(default_factory=list)  # Message IDs to revisit

    def transition_to(
        self,
        new_state: ConsensusState,
        trigger_message_id: UUID,
        trigger_participant_id: UUID,
        rationale: str,
        supporting: set[UUID] | None = None,
        dissenting: set[UUID] | None = None,
    ) -> None:
        """Record a consensus state transition."""
        transition = ConsensusTransition(
            from_state=self.current_state,
            to_state=new_state,
            trigger_message_id=trigger_message_id,
            trigger_participant_id=trigger_participant_id,
            rationale=rationale,
            supporting_participants=supporting or set(),
            dissenting_participants=dissenting or set(),
        )

        self.transitions.append(transition)
        self.current_state = new_state

    def record_fork(self, branch_descriptions: dict[str, set[UUID]]) -> None:
        """Record when consensus forks into multiple valid perspectives."""
        self.fork_branches = branch_descriptions
        self.current_state = ConsensusState.FORKED

    def add_to_compost(self, message_id: UUID) -> None:
        """Mark a message thread for future reconsideration."""
        if message_id not in self.compost_threads:
            self.compost_threads.append(message_id)

    def extract_journey_wisdom(self) -> dict[str, any]:
        """Extract wisdom from the consensus journey."""
        return {
            "total_transitions": len(self.transitions),
            "time_in_dialogue": self._calculate_dialogue_duration(),
            "participation_breadth": len(self.participant_positions),
            "preserved_dissent": len(self.compost_threads) > 0,
            "achieved_fork": self.fork_branches is not None,
            "key_insights": self.key_insights,
            "final_state": self.current_state.value,
        }

    def _calculate_dialogue_duration(self) -> float | None:
        """Calculate how long the dialogue took in hours."""
        if not self.transitions:
            return None

        first_transition = min(self.transitions, key=lambda t: t.timestamp)
        last_transition = max(self.transitions, key=lambda t: t.timestamp)
        duration = last_transition.timestamp - first_transition.timestamp

        return duration.total_seconds() / 3600  # Convert to hours
