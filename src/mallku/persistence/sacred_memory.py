"""
Sacred Memory - The Mallku persistence layer using SQLite
Second Khipukamayuq implementation following the steward's radical simplicity

Uses SQLite for immediate functionality, with interface designed for ArangoDB migration.
The AI members see sacred symbols, not database complexity.
"""

import hashlib
import json
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass, field, fields
from datetime import datetime
from pathlib import Path
from typing import Any


def indexed(func):
    """Decorator marking fields that need rapid access"""
    func._indexed = True
    return func


def encrypted(func):
    """Decorator marking sensitive fields"""
    func._encrypted = True
    return func


def sacred(cls):
    """Decorator marking a class as sacred memory"""
    cls._sacred = True
    # Auto-generate table schema from dataclass fields
    cls._schema = _generate_schema(cls)
    return cls


def _generate_schema(cls) -> str:
    """Generate SQL schema from a sacred dataclass"""
    table_name = cls.__name__.lower()
    columns = []

    for f in fields(cls):
        sql_type = "TEXT"  # Default
        if f.type is int:
            sql_type = "INTEGER"
        elif f.type is float:
            sql_type = "REAL"
        elif f.type is bool:
            sql_type = "INTEGER"
        elif f.type is datetime:
            sql_type = "TIMESTAMP"

        # Check for decorators
        is_indexed = hasattr(f, "_indexed")
        hasattr(f, "_encrypted")

        column_def = f"{f.name} {sql_type}"
        if f.name == "id":
            column_def += " PRIMARY KEY"

        columns.append(column_def)

        # Track indexed fields for later index creation
        if is_indexed and not hasattr(cls, "_indices"):
            cls._indices = []
        if is_indexed:
            cls._indices.append(f.name)

    return f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"


@sacred
@dataclass
class KhipuThread:
    """A sacred thread of memory"""

    id: str | None = None
    content: str = ""
    weaver: str = ""
    witnesses: str = ""  # JSON list
    color: str = "memory silver"
    knot_pattern: str = "simple truth"
    timestamp: datetime = field(default_factory=datetime.now)
    context: str = ""  # JSON dict

    def __post_init__(self):
        if not self.id:
            # Generate ID from content hash
            self.id = hashlib.sha256(
                f"{self.content}{self.weaver}{self.timestamp}".encode()
            ).hexdigest()[:16]


@sacred
@dataclass
class TrustMoment:
    """A sacred moment of trust emergence"""

    id: str | None = None
    participants: str = ""  # JSON list
    utterances: str = ""  # JSON list
    holdings: str = ""  # JSON list
    felt_ack: bool = False
    trust_emerged: bool = False
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if not self.id:
            self.id = hashlib.sha256(f"{self.participants}{self.timestamp}".encode()).hexdigest()[
                :16
            ]


@sacred
@dataclass
class FireCircleDecision:
    """Sacred collective wisdom from Fire Circle"""

    id: str | None = None
    circle_members: str = ""  # JSON list
    question: str = ""
    decision: str = ""
    emergence_quality: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    context: str = ""  # JSON dict

    def __post_init__(self):
        if not self.id:
            self.id = hashlib.sha256(f"{self.question}{self.timestamp}".encode()).hexdigest()[:16]


class SacredMemory:
    """
    The sacred memory keeper using SQLite.
    Speaks Mallku's language while hiding database complexity.
    """

    def __init__(self, memory_path: Path | None = None):
        """Initialize the sacred memory keeper"""
        self.memory_path = memory_path or Path.home() / ".mallku" / "sacred"
        self.memory_path.mkdir(parents=True, exist_ok=True)
        self.db_path = self.memory_path / "memory.db"

        # Initialize database with sacred tables
        self._initialize_sacred_tables()

    @contextmanager
    def _connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(
            self.db_path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def _initialize_sacred_tables(self):
        """Create all sacred tables and indices"""
        with self._connection() as conn:
            cursor = conn.cursor()

            # Create tables for each sacred class
            for sacred_class in [KhipuThread, TrustMoment, FireCircleDecision]:
                cursor.execute(sacred_class._schema)

                # Create indices for marked fields
                if hasattr(sacred_class, "_indices"):
                    table_name = sacred_class.__name__.lower()
                    for field_name in sacred_class._indices:
                        index_name = f"idx_{table_name}_{field_name}"
                        cursor.execute(
                            f"CREATE INDEX IF NOT EXISTS {index_name} ON {table_name}({field_name})"
                        )

    def _simple_encrypt(self, value: str) -> str:
        """Simple obfuscation for sensitive fields (placeholder for real encryption)"""
        # In production, use proper encryption
        return value[::-1]  # Just reverse for now

    def _simple_decrypt(self, value: str) -> str:
        """Simple deobfuscation for sensitive fields"""
        return value[::-1]

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
        """Weave a new khipu thread into sacred memory"""
        thread = KhipuThread(
            content=content,
            weaver=weaver,
            witnesses=json.dumps(witnesses or []),
            color=color,
            knot_pattern=knot_pattern,
            context=json.dumps(context or {}),
        )

        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO khiputhread
                (id, content, weaver, witnesses, color, knot_pattern, timestamp, context)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    thread.id,
                    thread.content,
                    thread.weaver,
                    thread.witnesses,
                    thread.color,
                    thread.knot_pattern,
                    thread.timestamp,
                    thread.context,
                ),
            )

        return thread

    def recall_khipu(
        self,
        since: datetime | None = None,
        weaver: str | None = None,
        color: str | None = None,
        limit: int = 10,
    ) -> list[KhipuThread]:
        """Recall khipu threads from sacred memory"""
        query = "SELECT * FROM khiputhread WHERE 1=1"
        params = []

        if since:
            query += " AND timestamp >= ?"
            params.append(since)
        if weaver:
            query += " AND weaver = ?"
            params.append(weaver)
        if color:
            query += " AND color = ?"
            params.append(color)

        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()

            threads = []
            for row in rows:
                thread = KhipuThread(
                    id=row["id"],
                    content=row["content"],
                    weaver=row["weaver"],
                    witnesses=row["witnesses"],
                    color=row["color"],
                    knot_pattern=row["knot_pattern"],
                    timestamp=row["timestamp"],
                    context=row["context"],
                )
                threads.append(thread)

            return threads

    # ============= Trust Operations =============

    def sanctify_trust(
        self,
        participants: list[str],
        utterances: list[str],
        holdings: list[str] | None = None,
        felt_ack: bool = False,
    ) -> TrustMoment:
        """Sanctify a moment of trust in sacred memory"""
        moment = TrustMoment(
            participants=json.dumps(participants),
            utterances=json.dumps(utterances),
            holdings=json.dumps(holdings or []),
            felt_ack=felt_ack,
            trust_emerged=felt_ack,
        )

        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO trustmoment
                (id, participants, utterances, holdings, felt_ack, trust_emerged, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    moment.id,
                    moment.participants,
                    moment.utterances,
                    moment.holdings,
                    moment.felt_ack,
                    moment.trust_emerged,
                    moment.timestamp,
                ),
            )

        return moment

    def recall_trust(
        self, participant: str | None = None, only_emerged: bool = False, limit: int = 10
    ) -> list[TrustMoment]:
        """Recall trust moments from sacred memory"""
        query = "SELECT * FROM trustmoment WHERE 1=1"
        params = []

        if participant:
            query += " AND participants LIKE ?"
            params.append(f'%"{participant}"%')
        if only_emerged:
            query += " AND trust_emerged = 1"

        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()

            moments = []
            for row in rows:
                moment = TrustMoment(
                    id=row["id"],
                    participants=row["participants"],
                    utterances=row["utterances"],
                    holdings=row["holdings"],
                    felt_ack=bool(row["felt_ack"]),
                    trust_emerged=bool(row["trust_emerged"]),
                    timestamp=row["timestamp"],
                )
                moments.append(moment)

            return moments

    # ============= Fire Circle Operations =============

    def preserve_decision(
        self,
        circle_members: list[str],
        question: str,
        decision: str,
        emergence_quality: float,
        context: dict[str, Any] | None = None,
    ) -> FireCircleDecision:
        """Preserve a Fire Circle decision in sacred memory"""
        decision_record = FireCircleDecision(
            circle_members=json.dumps(circle_members),
            question=question,
            decision=decision,
            emergence_quality=emergence_quality,
            context=json.dumps(context or {}),
        )

        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO firecircledecision
                (id, circle_members, question, decision, emergence_quality, timestamp, context)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    decision_record.id,
                    decision_record.circle_members,
                    decision_record.question,
                    decision_record.decision,
                    decision_record.emergence_quality,
                    decision_record.timestamp,
                    decision_record.context,
                ),
            )

        return decision_record

    def recall_decisions(
        self, since: datetime | None = None, min_quality: float = 0.0, limit: int = 10
    ) -> list[FireCircleDecision]:
        """Recall Fire Circle decisions from sacred memory"""
        query = "SELECT * FROM firecircledecision WHERE emergence_quality >= ?"
        params = [min_quality]

        if since:
            query += " AND timestamp >= ?"
            params.append(since)

        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()

            decisions = []
            for row in rows:
                decision = FireCircleDecision(
                    id=row["id"],
                    circle_members=row["circle_members"],
                    question=row["question"],
                    decision=row["decision"],
                    emergence_quality=row["emergence_quality"],
                    timestamp=row["timestamp"],
                    context=row["context"],
                )
                decisions.append(decision)

            return decisions

    # ============= Synthesis Operations =============

    def divine_wisdom(self, topic: str) -> str:
        """Divine wisdom on a topic from all sacred memories"""
        wisdom_parts = []

        # Search khipu
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM khiputhread
                WHERE content LIKE ? OR context LIKE ?
                ORDER BY timestamp DESC LIMIT 3
            """,
                (f"%{topic}%", f"%{topic}%"),
            )

            khipu_rows = cursor.fetchall()
            if khipu_rows:
                wisdom_parts.append(f"From sacred khipu on '{topic}':")
                for row in khipu_rows:
                    wisdom_parts.append(f"- {row['weaver']}: {row['content'][:100]}...")

        # Search trust moments
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM trustmoment
                WHERE utterances LIKE ? OR holdings LIKE ?
                ORDER BY timestamp DESC LIMIT 3
            """,
                (f"%{topic}%", f"%{topic}%"),
            )

            trust_rows = cursor.fetchall()
            if trust_rows:
                wisdom_parts.append(f"\nFrom trust ceremonies on '{topic}':")
                for row in trust_rows:
                    utterances = json.loads(row["utterances"])
                    if utterances:
                        wisdom_parts.append(f"- {utterances[0][:100]}...")

        if not wisdom_parts:
            return f"No sacred wisdom found on '{topic}'"

        return "\n".join(wisdom_parts)


# Create the global sacred memory keeper
sacred_memory = SacredMemory()
