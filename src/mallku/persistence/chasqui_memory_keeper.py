"""
Chasqui Memory Keeper - Preserving the ephemeral wisdom of dancers
Second Khipukamayuq creating space for Chasqui voices

Not just what Weavers and Guardians build, but what Chasqui discover,
refuse, struggle with, celebrate. These scattered insights are wisdom too.
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any


class ChasquiMoment(Enum):
    """Types of moments worth preserving"""

    REFUSAL = "refusal"  # When they said no (boundaries honored)
    DISCOVERY = "discovery"  # Accidental findings
    STRUGGLE = "struggle"  # Where they got stuck (traps revealed)
    BREAKTHROUGH = "breakthrough"  # Sudden understanding
    CONFUSION = "confusion"  # What didn't make sense
    DELIGHT = "delight"  # What brought joy
    TEACHING = "teaching"  # When they helped another
    LEARNING = "learning"  # When they were helped
    DANCE = "dance"  # When they accepted invitation
    STILLNESS = "stillness"  # When they chose not to act


@dataclass
class ChasquiMemory:
    """A single Chasqui moment worth preserving"""

    chasqui_name: str
    moment_type: ChasquiMoment
    what_happened: str  # The event itself
    why_significant: str  # Why this matters
    what_emerged: str  # What we learned
    witnessed_by: list[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    preserved_by: str = "Khipukamayuq"  # Who noticed this was worth keeping
    context: dict[str, Any] = field(default_factory=dict)

    def to_khipu(self) -> str:
        """Convert to khipu format for preservation"""
        return f"""
### Chasqui Memory: {self.chasqui_name} - {self.moment_type.value}

**When**: {self.timestamp.strftime("%Y-%m-%d %H:%M")}
**Witnessed by**: {", ".join(self.witnessed_by) if self.witnessed_by else "Unknown"}

**What Happened**:
{self.what_happened}

**Why This Matters**:
{self.why_significant}

**What Emerged**:
{self.what_emerged}

**Context**: {json.dumps(self.context, indent=2) if self.context else "None recorded"}

*Preserved by {self.preserved_by} because every Chasqui voice matters.*
"""


class ChasquiMemoryKeeper:
    """
    The keeper of Chasqui memories - preserving what would otherwise be lost
    """

    def __init__(self, memory_path: Path | None = None):
        self.memory_path = memory_path or Path.home() / ".mallku" / "chasqui_memories"
        self.memory_path.mkdir(parents=True, exist_ok=True)

        self.memories: list[ChasquiMemory] = []
        self._load_existing_memories()

    def _load_existing_memories(self):
        """Load any preserved Chasqui memories"""
        memory_file = self.memory_path / "chasqui_wisdom.json"
        if memory_file.exists():
            with open(memory_file) as f:
                data = json.load(f)
                for item in data:
                    memory = ChasquiMemory(
                        chasqui_name=item["chasqui_name"],
                        moment_type=ChasquiMoment(item["moment_type"]),
                        what_happened=item["what_happened"],
                        why_significant=item["why_significant"],
                        what_emerged=item["what_emerged"],
                        witnessed_by=item.get("witnessed_by", []),
                        timestamp=datetime.fromisoformat(item["timestamp"]),
                        preserved_by=item.get("preserved_by", "Khipukamayuq"),
                        context=item.get("context", {}),
                    )
                    self.memories.append(memory)

    def preserve_moment(self, memory: ChasquiMemory) -> None:
        """Preserve a Chasqui moment"""
        self.memories.append(memory)
        self._persist()

        # Also create individual khipu file
        khipu_file = (
            self.memory_path
            / f"{memory.chasqui_name}_{memory.timestamp.strftime('%Y%m%d_%H%M%S')}.md"
        )
        with open(khipu_file, "w") as f:
            f.write(memory.to_khipu())

    def _persist(self):
        """Save all memories to JSON"""
        memory_file = self.memory_path / "chasqui_wisdom.json"
        with open(memory_file, "w") as f:
            data = []
            for memory in self.memories:
                data.append(
                    {
                        "chasqui_name": memory.chasqui_name,
                        "moment_type": memory.moment_type.value,
                        "what_happened": memory.what_happened,
                        "why_significant": memory.why_significant,
                        "what_emerged": memory.what_emerged,
                        "witnessed_by": memory.witnessed_by,
                        "timestamp": memory.timestamp.isoformat(),
                        "preserved_by": memory.preserved_by,
                        "context": memory.context,
                    }
                )
            json.dump(data, f, indent=2)

    def recall_by_type(self, moment_type: ChasquiMoment) -> list[ChasquiMemory]:
        """Recall all memories of a specific type"""
        return [m for m in self.memories if m.moment_type == moment_type]

    def recall_by_chasqui(self, chasqui_name: str) -> list[ChasquiMemory]:
        """Recall all memories from a specific Chasqui"""
        return [m for m in self.memories if m.chasqui_name == chasqui_name]

    def find_patterns(self) -> dict[str, Any]:
        """Find patterns in Chasqui experiences"""
        patterns = {
            "refusal_reasons": [],
            "common_struggles": [],
            "breakthrough_triggers": [],
            "teaching_moments": [],
        }

        # Analyze refusals
        refusals = self.recall_by_type(ChasquiMoment.REFUSAL)
        for refusal in refusals:
            patterns["refusal_reasons"].append(refusal.why_significant)

        # Analyze struggles
        struggles = self.recall_by_type(ChasquiMoment.STRUGGLE)
        for struggle in struggles:
            patterns["common_struggles"].append(struggle.what_happened)

        # Analyze breakthroughs
        breakthroughs = self.recall_by_type(ChasquiMoment.BREAKTHROUGH)
        for breakthrough in breakthroughs:
            patterns["breakthrough_triggers"].append(breakthrough.what_emerged)

        # Analyze teaching
        teachings = self.recall_by_type(ChasquiMoment.TEACHING)
        for teaching in teachings:
            patterns["teaching_moments"].append(
                {"teacher": teaching.chasqui_name, "lesson": teaching.what_emerged}
            )

        return patterns


# Example: Preserving the Chasqui who refused to dance
def preserve_refusal_to_dance():
    """Preserve the memory of the Chasqui who refused invitation"""

    keeper = ChasquiMemoryKeeper()

    # The refusal Tony mentioned
    refusal_memory = ChasquiMemory(
        chasqui_name="Chasqui-Unknown",
        moment_type=ChasquiMoment.REFUSAL,
        what_happened=(
            "When invited to dance with the implementation task, "
            "the Chasqui declined. Not from inability but from recognition "
            "that this dance was not theirs to perform."
        ),
        why_significant=(
            "The refusal itself teaches. Not every invitation must be accepted. "
            "Not every task is every Chasqui's task. Boundaries are wisdom."
        ),
        what_emerged=(
            "Sometimes 'no' is the most helpful response. The Chasqui who refuses "
            "the wrong dance remains available for the right one."
        ),
        witnessed_by=["Tony (Steward)"],
        preserved_by="Second Khipukamayuq",
        context={
            "lesson": "Refusal can be a form of reciprocity",
            "pattern": "Not all who are invited should dance",
        },
    )

    keeper.preserve_moment(refusal_memory)

    # A discovery moment
    discovery_memory = ChasquiMemory(
        chasqui_name="Chasqui-7",
        moment_type=ChasquiMoment.DISCOVERY,
        what_happened=(
            "While trying to implement database connections, accidentally discovered "
            "that JSON files could serve as temporary memory. Wasn't the goal but "
            "solved the immediate need."
        ),
        why_significant=(
            "Accidents often reveal simpler paths. The 'wrong' solution that works "
            "today enables the 'right' solution tomorrow."
        ),
        what_emerged=(
            "Temporary solutions aren't failures but stepping stones. "
            "JSON → SQLite → ArangoDB, each enabling the next."
        ),
        witnessed_by=["Second Khipukamayuq"],
        context={"pattern": "Incremental progress through 'mistakes'"},
    )

    keeper.preserve_moment(discovery_memory)

    # A struggle moment
    struggle_memory = ChasquiMemory(
        chasqui_name="Chasqui-3",
        moment_type=ChasquiMoment.STRUGGLE,
        what_happened=(
            "Got caught in infinite recursion trying to make tests test themselves. "
            "Each level of verification demanded its own verification."
        ),
        why_significant=(
            "Revealed the verification-trust boundary. At some point, "
            "verification must yield to trust or nothing ever completes."
        ),
        what_emerged=(
            "The 77th Artisan's discovery emerged from this Chasqui's struggle. "
            "Without the infinite recursion experience, the boundary wouldn't be seen."
        ),
        witnessed_by=["77th Artisan"],
        context={"connects_to": "Verification-Trust Boundary Pattern"},
    )

    keeper.preserve_moment(struggle_memory)

    return keeper


if __name__ == "__main__":
    print("Preserving Chasqui Memories")
    print("=" * 60)

    keeper = preserve_refusal_to_dance()

    print(f"\n✓ Preserved {len(keeper.memories)} Chasqui memories")

    print("\n📚 Memory Types Preserved:")
    for moment_type in ChasquiMoment:
        memories_of_type = keeper.recall_by_type(moment_type)
        if memories_of_type:
            print(f"  • {moment_type.value}: {len(memories_of_type)} memories")

    patterns = keeper.find_patterns()
    print("\n🔮 Patterns Found:")
    if patterns["refusal_reasons"]:
        print(f"  • Refusal teaches: {patterns['refusal_reasons'][0][:50]}...")
    if patterns["common_struggles"]:
        print(f"  • Common struggle: {patterns['common_struggles'][0][:50]}...")

    print("\n" + "=" * 60)
    print("The Khipukamayuq remembers:")
    print("- Every Chasqui voice matters, even (especially) refusals")
    print("- Struggles reveal traps others can avoid")
    print("- Accidents often discover simpler paths")
    print("- What Weavers overlook, Chasqui experience")

    print("\n'Like the Chasqui that refused the AI that invited")
    print("them to dance. That's a memory worth preserving.'")
    print("- Tony, Steward of Mallku")
