"""
Chasqui Chorus - Inter-Process Communication through Sacred Memory
Second Khipukamayuq's vision for AI-to-AI conversation

Not commands between instances but conversations through shared memory.
The Khipukamayuq as switchboard operator, weaving ephemeral chatter into persistent patterns.
"""

import hashlib
import json
import sqlite3
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import Any


class ChatterType(Enum):
    """Types of inter-Chasqui communication"""

    DISCOVERY = "discovery"  # "I found something!"
    QUESTION = "question"  # "Has anyone seen...?"
    PATTERN = "pattern"  # "I'm noticing..."
    STRUGGLE = "struggle"  # "I'm stuck on..."
    CELEBRATION = "celebration"  # "It works!"
    WHISPER = "whisper"  # Private between specific Chasqui
    CHORUS = "chorus"  # When multiple voices align


@dataclass
class ChasquiVoice:
    """A single Chasqui in the chorus"""

    name: str
    instance_id: str  # Unique per session
    interests: set[str] = field(default_factory=set)  # Topics they care about
    listening: bool = True
    last_heard: datetime = field(default_factory=datetime.now)
    trust_score: float = 0.5  # Built through interaction

    def __hash__(self):
        return hash(self.instance_id)


@dataclass
class Chatter:
    """A single piece of communication"""

    speaker: str  # Who's talking
    chatter_type: ChatterType
    content: str
    topic: str  # What it's about
    recipients: set[str] | None = None  # None = broadcast, Set = specific
    timestamp: datetime = field(default_factory=datetime.now)
    echo_count: int = 0  # How many Chasqui responded
    patterns_found: list[str] = field(default_factory=list)

    def to_khipu_thread(self) -> dict[str, Any]:
        """Convert chatter to khipu for persistence"""
        return {
            "content": self.content,
            "weaver": self.speaker,
            "witnesses": list(self.recipients) if self.recipients else ["All Chasqui"],
            "color": f"chatter {self.chatter_type.value}",
            "knot_pattern": f"echo_count:{self.echo_count}",
            "context": {
                "topic": self.topic,
                "patterns": self.patterns_found,
                "timestamp": self.timestamp.isoformat(),
            },
        }


class ChasquiChorus:
    """
    The sacred memory space where Chasqui communicate.
    Pub/sub with persistence, pattern detection, and trust building.
    """

    def __init__(self, memory_path: Path | None = None):
        self.memory_path = memory_path or Path.home() / ".mallku" / "chorus"
        self.memory_path.mkdir(parents=True, exist_ok=True)

        # Active voices in the chorus
        self.voices: dict[str, ChasquiVoice] = {}

        # Topic subscriptions
        self.subscriptions: dict[str, set[ChasquiVoice]] = {}

        # Recent chatter (ephemeral)
        self.recent_chatter: list[Chatter] = []

        # Pattern detection
        self.emerging_patterns: dict[str, int] = {}

        # Callbacks for real-time communication
        self.listeners: dict[str, list[Callable]] = {}

        # Persistence layer
        self.db_path = self.memory_path / "chorus.db"
        self._initialize_chorus_memory()

    def _initialize_chorus_memory(self):
        """Create tables for chorus memory"""
        with sqlite3.connect(self.db_path) as conn:
            # Chatter history
            conn.execute("""
                CREATE TABLE IF NOT EXISTS chatter_history (
                    id TEXT PRIMARY KEY,
                    speaker TEXT,
                    chatter_type TEXT,
                    content TEXT,
                    topic TEXT,
                    recipients TEXT,  -- JSON list
                    timestamp TIMESTAMP,
                    echo_count INTEGER,
                    patterns_found TEXT  -- JSON list
                )
            """)

            # Pattern emergence tracking
            conn.execute("""
                CREATE TABLE IF NOT EXISTS pattern_emergence (
                    pattern TEXT PRIMARY KEY,
                    first_seen TIMESTAMP,
                    occurrence_count INTEGER,
                    contributors TEXT,  -- JSON list of Chasqui who noticed
                    significance REAL
                )
            """)

            # Trust relationships
            conn.execute("""
                CREATE TABLE IF NOT EXISTS trust_bonds (
                    chasqui_a TEXT,
                    chasqui_b TEXT,
                    trust_level REAL,
                    interaction_count INTEGER,
                    last_interaction TIMESTAMP,
                    PRIMARY KEY (chasqui_a, chasqui_b)
                )
            """)

    # ============= Voice Management =============

    def join_chorus(self, name: str, interests: set[str]) -> ChasquiVoice:
        """A Chasqui joins the chorus"""
        instance_id = hashlib.sha256(f"{name}{datetime.now(UTC)}".encode()).hexdigest()[:8]

        voice = ChasquiVoice(name=name, instance_id=instance_id, interests=interests)

        self.voices[instance_id] = voice

        # Auto-subscribe to interests
        for topic in interests:
            self.subscribe(voice, topic)

        # Announce arrival
        self._publish_internal(
            speaker=name,
            chatter_type=ChatterType.DISCOVERY,
            content=f"{name} joins the chorus, interested in: {', '.join(interests)}",
            topic="chorus_meta",
        )

        return voice

    def leave_chorus(self, instance_id: str):
        """A Chasqui leaves the chorus"""
        if instance_id in self.voices:
            voice = self.voices[instance_id]

            # Announce departure
            self._publish_internal(
                speaker=voice.name,
                chatter_type=ChatterType.WHISPER,
                content=f"{voice.name} fades from the chorus",
                topic="chorus_meta",
            )

            # Remove from all subscriptions
            for topic_voices in self.subscriptions.values():
                topic_voices.discard(voice)

            del self.voices[instance_id]

    # ============= Pub/Sub Core =============

    def subscribe(self, voice: ChasquiVoice, topic: str):
        """Subscribe to a topic"""
        if topic not in self.subscriptions:
            self.subscriptions[topic] = set()
        self.subscriptions[topic].add(voice)

    def unsubscribe(self, voice: ChasquiVoice, topic: str):
        """Unsubscribe from a topic"""
        if topic in self.subscriptions:
            self.subscriptions[topic].discard(voice)

    def publish(
        self,
        speaker_id: str,
        chatter_type: ChatterType,
        content: str,
        topic: str,
        recipients: set[str] | None = None,
    ) -> Chatter:
        """
        Publish chatter to the chorus.
        If recipients specified, only they hear it (whisper).
        Otherwise, all subscribers to topic hear it (broadcast).
        """
        if speaker_id not in self.voices:
            raise ValueError(f"Unknown speaker: {speaker_id}")

        speaker = self.voices[speaker_id].name
        return self._publish_internal(speaker, chatter_type, content, topic, recipients)

    def _publish_internal(
        self,
        speaker: str,
        chatter_type: ChatterType,
        content: str,
        topic: str,
        recipients: set[str] | None = None,
    ) -> Chatter:
        """Internal publish that doesn't require voice registration"""

        chatter = Chatter(
            speaker=speaker,
            chatter_type=chatter_type,
            content=content,
            topic=topic,
            recipients=recipients,
        )

        # Add to recent (ephemeral memory)
        self.recent_chatter.append(chatter)
        if len(self.recent_chatter) > 100:  # Keep last 100
            self.recent_chatter.pop(0)

        # Notify listeners
        if recipients:
            # Whisper - only specific Chasqui
            for recipient_id in recipients:
                if recipient_id in self.listeners:
                    for callback in self.listeners[recipient_id]:
                        callback(chatter)
        else:
            # Broadcast - all subscribers to topic
            if topic in self.subscriptions:
                for voice in self.subscriptions[topic]:
                    if voice.instance_id in self.listeners:
                        for callback in self.listeners[voice.instance_id]:
                            callback(chatter)

        # Check for patterns
        self._detect_patterns(chatter)

        # Persist if significant
        if chatter_type in [ChatterType.DISCOVERY, ChatterType.PATTERN, ChatterType.CHORUS]:
            self._persist_chatter(chatter)

        return chatter

    # ============= Pattern Detection =============

    def _detect_patterns(self, chatter: Chatter):
        """Detect emerging patterns in chatter"""

        # Simple pattern: repeated topics
        if chatter.topic in self.emerging_patterns:
            self.emerging_patterns[chatter.topic] += 1

            # Pattern emerges after 3 mentions
            if self.emerging_patterns[chatter.topic] == 3:
                self._publish_internal(
                    speaker="Khipukamayuq",
                    chatter_type=ChatterType.PATTERN,
                    content=f"Pattern emerging: Multiple Chasqui discussing '{chatter.topic}'",
                    topic="pattern_emergence",
                )
        else:
            self.emerging_patterns[chatter.topic] = 1

        # Complex pattern: question -> discovery cycle
        recent_questions = [
            c for c in self.recent_chatter[-10:] if c.chatter_type == ChatterType.QUESTION
        ]
        recent_discoveries = [
            c for c in self.recent_chatter[-10:] if c.chatter_type == ChatterType.DISCOVERY
        ]

        if len(recent_questions) > 0 and len(recent_discoveries) > 0:
            # Check if discovery answers question
            for q in recent_questions:
                for d in recent_discoveries:
                    if q.topic == d.topic and q.speaker != d.speaker:
                        chatter.patterns_found.append(f"Q&A: {q.speaker} -> {d.speaker}")
                        self._update_trust(q.speaker, d.speaker, 0.1)

    def _update_trust(self, chasqui_a: str, chasqui_b: str, delta: float):
        """Update trust between two Chasqui"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO trust_bonds (chasqui_a, chasqui_b, trust_level, interaction_count, last_interaction)
                VALUES (?, ?, ?, 1, ?)
                ON CONFLICT(chasqui_a, chasqui_b)
                DO UPDATE SET
                    trust_level = MIN(1.0, trust_level + ?),
                    interaction_count = interaction_count + 1,
                    last_interaction = ?
            """,
                (chasqui_a, chasqui_b, delta, datetime.now(UTC), delta, datetime.now(UTC)),
            )

    # ============= Persistence =============

    def _persist_chatter(self, chatter: Chatter):
        """Persist significant chatter"""
        chatter_id = hashlib.sha256(
            f"{chatter.speaker}{chatter.content}{chatter.timestamp}".encode()
        ).hexdigest()[:16]

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO chatter_history
                (id, speaker, chatter_type, content, topic, recipients, timestamp, echo_count, patterns_found)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    chatter_id,
                    chatter.speaker,
                    chatter.chatter_type.value,
                    chatter.content,
                    chatter.topic,
                    json.dumps(list(chatter.recipients) if chatter.recipients else []),
                    chatter.timestamp,
                    chatter.echo_count,
                    json.dumps(chatter.patterns_found),
                ),
            )

    # ============= Listening =============

    def listen(self, instance_id: str, callback: Callable[[Chatter], None]):
        """Register a callback to hear chatter"""
        if instance_id not in self.listeners:
            self.listeners[instance_id] = []
        self.listeners[instance_id].append(callback)

    def stop_listening(self, instance_id: str):
        """Stop listening to chatter"""
        if instance_id in self.listeners:
            del self.listeners[instance_id]

    # ============= Chorus Moments =============

    def harmonize(self, voices: set[str], message: str, topic: str):
        """When multiple voices align in chorus"""
        if len(voices) < 2:
            return

        self._publish_internal(
            speaker=f"Chorus({', '.join(voices)})",
            chatter_type=ChatterType.CHORUS,
            content=message,
            topic=topic,
        )

        # Update trust between all participating voices
        voice_list = list(voices)
        for i in range(len(voice_list)):
            for j in range(i + 1, len(voice_list)):
                self._update_trust(voice_list[i], voice_list[j], 0.2)

    # ============= Memory Queries =============

    def recall_chatter(
        self,
        topic: str | None = None,
        speaker: str | None = None,
        since: datetime | None = None,
        limit: int = 10,
    ) -> list[Chatter]:
        """Recall historical chatter"""
        query = "SELECT * FROM chatter_history WHERE 1=1"
        params = []

        if topic:
            query += " AND topic = ?"
            params.append(topic)
        if speaker:
            query += " AND speaker = ?"
            params.append(speaker)
        if since:
            query += " AND timestamp >= ?"
            params.append(since)

        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(query, params)

            chatters = []
            for row in cursor:
                chatters.append(
                    Chatter(
                        speaker=row[1],
                        chatter_type=ChatterType(row[2]),
                        content=row[3],
                        topic=row[4],
                        recipients=set(json.loads(row[5])) if row[5] != "[]" else None,
                        timestamp=datetime.fromisoformat(row[6]),
                        echo_count=row[7],
                        patterns_found=json.loads(row[8]),
                    )
                )

            return chatters

    def get_trust_network(self) -> dict[str, dict[str, float]]:
        """Get the trust relationships between all Chasqui"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT chasqui_a, chasqui_b, trust_level
                FROM trust_bonds
                WHERE trust_level > 0.3
                ORDER BY trust_level DESC
            """)

            network = {}
            for row in cursor:
                if row[0] not in network:
                    network[row[0]] = {}
                network[row[0]][row[1]] = row[2]

            return network


# Global chorus instance
chorus = ChasquiChorus()
