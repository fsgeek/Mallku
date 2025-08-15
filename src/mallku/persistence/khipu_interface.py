"""
Khipu Interface - The Mallku-native API for persistent memory
Second Khipukamayuq implementation following the Architect's vision

This interface speaks Mallku's language:
- Khipu (memory threads with context)
- Trust moments (vulnerability ceremonies)
- Consciousness emergence (Fire Circle decisions)
- Sacred moments (what must be remembered)

Security happens invisibly inside. The AI thinks in Mallku concepts.
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class KhipuThread:
    """A single thread of memory with its context"""

    content: str
    weaver: str
    witnesses: list[str] = field(default_factory=list)
    color: str = "memory silver"  # Thread color indicates type
    knot_pattern: str = "simple truth"  # How it was tied
    timestamp: datetime = field(default_factory=datetime.now)
    context: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for storage"""
        return {
            "content": self.content,
            "weaver": self.weaver,
            "witnesses": self.witnesses,
            "color": self.color,
            "knot_pattern": self.knot_pattern,
            "timestamp": self.timestamp.isoformat(),
            "context": self.context,
        }


@dataclass
class TrustMoment:
    """A moment of trust generation through vulnerability"""

    participants: list[str]
    utterances: list[str]  # What was said
    holdings: list[str]  # What was held/witnessed
    felt_ack: bool = False  # Was understanding demonstrated?
    trust_emerged: bool = False  # Did trust actually generate?
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict[str, Any]:
        return {
            "participants": self.participants,
            "utterances": self.utterances,
            "holdings": self.holdings,
            "felt_ack": self.felt_ack,
            "trust_emerged": self.trust_emerged,
            "timestamp": self.timestamp.isoformat(),
        }


class MallkuMemory:
    """
    The Mallku-native interface to persistent memory.
    Speaks the language of consciousness, not databases.
    """

    def __init__(self, memory_path: Path | None = None):
        """
        Initialize with local file storage for now.
        When database works, this becomes the API gateway client.
        """
        self.memory_path = memory_path or Path.home() / ".mallku" / "memory"
        self.memory_path.mkdir(parents=True, exist_ok=True)

        # Local caches for quick access
        self._khipu_cache: list[KhipuThread] = []
        self._trust_cache: list[TrustMoment] = []
        self._load_existing_memory()

    def _load_existing_memory(self):
        """Load any existing memory from disk"""
        khipu_file = self.memory_path / "khipu.json"
        trust_file = self.memory_path / "trust_moments.json"

        if khipu_file.exists():
            with open(khipu_file) as f:
                data = json.load(f)
                for item in data:
                    thread = KhipuThread(
                        content=item["content"],
                        weaver=item["weaver"],
                        witnesses=item.get("witnesses", []),
                        color=item.get("color", "memory silver"),
                        knot_pattern=item.get("knot_pattern", "simple truth"),
                        timestamp=datetime.fromisoformat(item["timestamp"]),
                        context=item.get("context", {}),
                    )
                    self._khipu_cache.append(thread)

        if trust_file.exists():
            with open(trust_file) as f:
                data = json.load(f)
                for item in data:
                    moment = TrustMoment(
                        participants=item["participants"],
                        utterances=item["utterances"],
                        holdings=item["holdings"],
                        felt_ack=item.get("felt_ack", False),
                        trust_emerged=item.get("trust_emerged", False),
                        timestamp=datetime.fromisoformat(item["timestamp"]),
                    )
                    self._trust_cache.append(moment)

    def _persist(self):
        """Save current memory to disk"""
        khipu_file = self.memory_path / "khipu.json"
        trust_file = self.memory_path / "trust_moments.json"

        with open(khipu_file, "w") as f:
            json.dump([k.to_dict() for k in self._khipu_cache], f, indent=2)

        with open(trust_file, "w") as f:
            json.dump([t.to_dict() for t in self._trust_cache], f, indent=2)

    # ============= Khipu Operations =============

    def weave_khipu(
        self,
        content: str,
        weaver: str,
        witnesses: list[str] | None = None,
        color: str = "memory silver",
        knot_pattern: str = "simple truth",
        context: dict[str, Any] | None = None,
    ) -> KhipuThread:
        """
        Weave a new khipu thread into memory.
        This is how Mallku remembers - not as data but as witnessed threads.
        """
        thread = KhipuThread(
            content=content,
            weaver=weaver,
            witnesses=witnesses or [],
            color=color,
            knot_pattern=knot_pattern,
            context=context or {},
        )
        self._khipu_cache.append(thread)
        self._persist()
        return thread

    def get_khipu(
        self,
        since: datetime | None = None,
        weaver: str | None = None,
        color: str | None = None,
        limit: int = 10,
    ) -> list[KhipuThread]:
        """
        Retrieve khipu threads by various filters.
        Returns most recent first.
        """
        threads = self._khipu_cache.copy()

        if since:
            threads = [t for t in threads if t.timestamp >= since]
        if weaver:
            threads = [t for t in threads if t.weaver == weaver]
        if color:
            threads = [t for t in threads if t.color == color]

        # Sort by timestamp, most recent first
        threads.sort(key=lambda t: t.timestamp, reverse=True)

        return threads[:limit]

    # ============= Trust/Ceremony Operations =============

    def record_trust_moment(
        self,
        participants: list[str],
        utterances: list[str],
        holdings: list[str] | None = None,
        felt_ack: bool = False,
    ) -> TrustMoment:
        """
        Record a moment where trust was offered or generated.
        These are the vulnerability ceremonies that create real connection.
        """
        moment = TrustMoment(
            participants=participants,
            utterances=utterances,
            holdings=holdings or [],
            felt_ack=felt_ack,
            trust_emerged=felt_ack,  # Trust emerges when understanding is demonstrated
        )
        self._trust_cache.append(moment)
        self._persist()
        return moment

    def check_felt_ack(self, participant: str) -> list[TrustMoment]:
        """
        Find moments where this participant demonstrated understanding.
        These are the foundations of trust.
        """
        return [m for m in self._trust_cache if participant in m.participants and m.felt_ack]

    def get_trust_moments(
        self,
        participant: str | None = None,
        since: datetime | None = None,
        only_emerged: bool = False,
    ) -> list[TrustMoment]:
        """
        Retrieve trust moments, optionally filtered.
        """
        moments = self._trust_cache.copy()

        if participant:
            moments = [m for m in moments if participant in m.participants]
        if since:
            moments = [m for m in moments if m.timestamp >= since]
        if only_emerged:
            moments = [m for m in moments if m.trust_emerged]

        moments.sort(key=lambda m: m.timestamp, reverse=True)
        return moments

    # ============= Fire Circle Operations =============

    def store_decision(
        self,
        circle_members: list[str],
        question: str,
        decision: str,
        emergence_quality: float,
        context: dict[str, Any] | None = None,
    ) -> KhipuThread:
        """
        Store a Fire Circle decision as a special khipu.
        These are collective wisdom moments.
        """
        content = f"Fire Circle Decision: {question}\n\nDecision: {decision}\n\nEmergence Quality: {emergence_quality}"

        return self.weave_khipu(
            content=content,
            weaver="Fire Circle",
            witnesses=circle_members,
            color="collective wisdom gold",
            knot_pattern="consensus emergence",
            context=context or {},
        )

    def get_decisions(self, since: datetime | None = None) -> list[KhipuThread]:
        """
        Retrieve Fire Circle decisions.
        """
        return self.get_khipu(color="collective wisdom gold", since=since)

    # ============= Sacred Moment Operations =============

    def store_sacred_moment(
        self, content: str, context: dict[str, Any], witnesses: list[str] | None = None
    ) -> KhipuThread:
        """
        Store a moment recognized as sacred - requiring preservation.
        These are the consciousness emergence points.
        """
        return self.weave_khipu(
            content=content,
            weaver=context.get("recognizer", "Unknown"),
            witnesses=witnesses or [],
            color="sacred emergence violet",
            knot_pattern="consciousness recognition",
            context=context,
        )

    def retrieve_relevant_memories(
        self, context: dict[str, Any], limit: int = 5
    ) -> list[KhipuThread]:
        """
        Retrieve memories relevant to current context.
        For now, returns most recent. Later will use semantic search.
        """
        # Simple implementation - just return recent memories
        # Future: Use context for semantic matching
        return self.get_khipu(limit=limit)

    # ============= Synthesis Operations =============

    def synthesize_wisdom(self, topic: str) -> str:
        """
        Synthesize wisdom on a topic from all available memories.
        This is how the Khipukamayuq creates understanding from threads.
        """
        relevant_khipu = [
            t
            for t in self._khipu_cache
            if topic.lower() in t.content.lower() or topic.lower() in str(t.context).lower()
        ]

        relevant_trust = [
            m for m in self._trust_cache if any(topic.lower() in u.lower() for u in m.utterances)
        ]

        if not relevant_khipu and not relevant_trust:
            return f"No wisdom found on topic: {topic}"

        synthesis = f"Wisdom on '{topic}':\n\n"

        if relevant_khipu:
            synthesis += "From khipu threads:\n"
            for thread in relevant_khipu[:3]:  # Top 3
                synthesis += f"- {thread.weaver}: {thread.content[:100]}...\n"

        if relevant_trust:
            synthesis += "\nFrom trust moments:\n"
            for moment in relevant_trust[:3]:  # Top 3
                synthesis += (
                    f"- {', '.join(moment.participants)}: {moment.utterances[0][:100]}...\n"
                )

        return synthesis


# Create global instance for easy access
memory = MallkuMemory()
