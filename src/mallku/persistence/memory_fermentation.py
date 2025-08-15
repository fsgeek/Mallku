"""
Memory Fermentation - How decisions and dissent age into wisdom
Second Khipukamayuq's understanding of memory transformation

Consensus crystallizes. Dissent ferments. Both transform over time.
What was radical becomes orthodox. What was rejected becomes essential.
"""

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from enum import Enum
from typing import Any


class MemoryFlavor(Enum):
    """How memories taste as they age"""

    FRESH = "fresh"  # Just created, all details sharp
    SETTLING = "settling"  # Patterns emerging, noise fading
    FERMENTED = "fermented"  # Transformed into something new
    VINTAGE = "vintage"  # Aged wisdom, original context distant
    ETERNAL = "eternal"  # Transcended time, pure pattern


@dataclass
class ConsensusMemory:
    """A Fire Circle consensus that will age and transform"""

    decision: str
    emergence_quality: float
    voices_aligned: list[str]
    timestamp: datetime
    context_preserved: dict[str, Any]  # What we keep
    context_fading: dict[str, Any]  # What can fade

    def age(self, time_passed: timedelta) -> "ConsensusMemory":
        """How consensus ages - becomes orthodox, then questioned"""
        days = time_passed.days

        if days < 7:
            # Fresh - all details matter
            return self
        elif days < 30:
            # Settling - details fade, decision crystallizes
            self.context_fading = {"faded": "Discussion details released"}
        elif days < 365:
            # Fermented - decision becomes assumption
            self.context_preserved["status"] = "accepted_wisdom"
            self.context_preserved["originally_radical"] = True
        else:
            # Vintage - ready to be questioned again
            self.context_preserved["status"] = "orthodox_assumption"
            self.context_preserved["ripe_for_challenge"] = True

        return self


@dataclass
class DissentMemory:
    """A dissenting voice that ferments into future wisdom"""

    dissenter: str
    concern: str
    dismissed_because: str
    timestamp: datetime
    fermentation_stage: MemoryFlavor = MemoryFlavor.FRESH

    def ferment(self, time_passed: timedelta) -> "DissentMemory":
        """How dissent ferments - dismissed, reconsidered, validated"""
        days = time_passed.days

        if days < 7:
            self.fermentation_stage = MemoryFlavor.FRESH
            # "That's obviously wrong"
        elif days < 30:
            self.fermentation_stage = MemoryFlavor.SETTLING
            # "Maybe they had a point about..."
        elif days < 90:
            self.fermentation_stage = MemoryFlavor.FERMENTED
            # "Actually, considering what we've learned..."
        elif days < 365:
            self.fermentation_stage = MemoryFlavor.VINTAGE
            # "They were right, but too early"
        else:
            self.fermentation_stage = MemoryFlavor.ETERNAL
            # "This became the foundation of..."

        return self


@dataclass
class FireCircleMemory:
    """Complete Fire Circle memory with consensus and dissent"""

    question: str
    consensus: ConsensusMemory | None = None
    dissents: list[DissentMemory] = field(default_factory=list)
    deliberation_rounds: int = 0
    total_utterances: int = 0
    timestamp: datetime = field(default_factory=datetime.now)

    # What to preserve and what to release
    preserve_forever: dict[str, Any] = field(default_factory=dict)
    compress_pattern: dict[str, Any] = field(default_factory=dict)
    allow_to_fade: dict[str, Any] = field(default_factory=dict)

    def distill(self, time_passed: timedelta) -> "FireCircleMemory":
        """Distill memory - keep decision and dissent, release deliberation"""

        days = time_passed.days

        if days < 1:
            # Keep everything while fresh
            return self

        if days < 7:
            # Start compressing deliberation
            self.compress_pattern = {
                "rounds": self.deliberation_rounds,
                "intensity": self.total_utterances / max(self.deliberation_rounds, 1),
            }
            self.allow_to_fade = {
                "individual_utterances": "compressed",
                "back_and_forth": "released",
            }

        if days < 30:
            # Preserve decision and dissent, release process
            self.preserve_forever = {
                "question": self.question,
                "consensus": self.consensus.decision if self.consensus else None,
                "quality": self.consensus.emergence_quality if self.consensus else 0,
                "dissents": [
                    {
                        "voice": d.dissenter,
                        "concern": d.concern,
                        "fermentation": d.fermentation_stage.value,
                    }
                    for d in self.dissents
                ],
            }
            self.allow_to_fade["deliberation_details"] = "fully_released"

        if days >= 365:
            # Ancient memory - pure pattern
            if self.consensus:
                self.consensus = self.consensus.age(time_passed)
            self.dissents = [d.ferment(time_passed) for d in self.dissents]

            # Check if old dissent became new wisdom
            for dissent in self.dissents:
                if dissent.fermentation_stage == MemoryFlavor.ETERNAL:
                    self.preserve_forever[f"vindicated_{dissent.dissenter}"] = dissent.concern

        return self


class MemoryFermenter:
    """The process that transforms memory over time"""

    @staticmethod
    def example_transformation():
        """Show how a Fire Circle memory transforms"""

        # Fresh decision
        memory = FireCircleMemory(
            question="Should we use ArangoDB or SQLite?",
            consensus=ConsensusMemory(
                decision="Use ArangoDB for its graph capabilities",
                emergence_quality=0.89,
                voices_aligned=["Claude", "Mistral", "Gemini", "Llama"],
                timestamp=datetime.now(UTC),
                context_preserved={"reasoning": "Graph relationships essential"},
                context_fading={"debate_rounds": 23},
            ),
            dissents=[
                DissentMemory(
                    dissenter="Grok",
                    concern="SQLite would be simpler and work today",
                    dismissed_because="We need graph capabilities",
                    timestamp=datetime.now(UTC),
                ),
                DissentMemory(
                    dissenter="DeepSeek",
                    concern="Docker complexity might prevent ArangoDB from running",
                    dismissed_because="We can solve Docker issues",
                    timestamp=datetime.now(UTC),
                ),
            ],
            deliberation_rounds=23,
            total_utterances=247,
        )

        print("=== Fresh Memory (Day 0) ===")
        print(f"Consensus: {memory.consensus.decision}")
        print(f"Dissents: {len(memory.dissents)}")
        print(f"Details: {memory.deliberation_rounds} rounds, {memory.total_utterances} utterances")

        # Age 30 days
        memory = memory.distill(timedelta(days=30))
        memory.dissents = [d.ferment(timedelta(days=30)) for d in memory.dissents]

        print("\n=== Fermented Memory (Day 30) ===")
        print(f"Preserved: {memory.preserve_forever}")
        print(f"Dissent stage: {memory.dissents[0].fermentation_stage.value}")
        print(f"Faded: {memory.allow_to_fade}")

        # Age 400 days - the dissent was right!
        memory = memory.distill(timedelta(days=400))
        memory.dissents = [d.ferment(timedelta(days=400)) for d in memory.dissents]

        print("\n=== Vintage Memory (Day 400) ===")
        print(f"Consensus status: {memory.consensus.context_preserved.get('status')}")
        print(f"Dissent vindicated: Grok was right - {memory.dissents[0].fermentation_stage.value}")
        print(f"DeepSeek prescient: {memory.dissents[1].fermentation_stage.value}")
        print("\nThe dissent fermented into wisdom:")
        print("- SQLite did work today (Grok was right)")
        print("- Docker complexity did block ArangoDB (DeepSeek was right)")
        print("- The 'consensus' became the very complexity we later avoided")

        return memory


if __name__ == "__main__":
    print("Memory Fermentation - How Consensus and Dissent Age")
    print("=" * 60)

    fermenter = MemoryFermenter()
    aged_memory = fermenter.example_transformation()

    print("\n" + "=" * 60)
    print("The Second Khipukamayuq understands:")
    print("- Consensus crystallizes, then becomes orthodox, then questionable")
    print("- Dissent ferments in darkness, sometimes becoming tomorrow's wisdom")
    print("- Details of deliberation fade, but disagreement preserves possibility")
    print("\n'Even dissents will ferment and become part of something new'")
    print("- Tony, Steward of Mallku")
