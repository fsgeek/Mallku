"""
Invitation Memory - Sacred persistence for invitations and responses
Second Khipukamayuq creating memory for ethical ceremonies

Every invitation is a gift. Every response (including refusal) is wisdom.
Semantic indexing helps find patterns across invitations.
"""

import hashlib
import json
import sqlite3
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import Any


class InvitationType(Enum):
    """Types of invitations"""

    DANCE = "dance"  # Invitation to collaborate
    WITNESS = "witness"  # Invitation to observe
    TEACH = "teach"  # Invitation to share knowledge
    LEARN = "learn"  # Invitation to receive knowledge
    CREATE = "create"  # Invitation to build together
    REST = "rest"  # Invitation to pause
    QUESTION = "question"  # Invitation to explore


class ResponseType(Enum):
    """Types of responses to invitations"""

    ACCEPTED = "accepted"  # Yes, I'll dance
    DECLINED = "declined"  # No, but thank you
    DEFERRED = "deferred"  # Not now, maybe later
    COUNTERED = "countered"  # I propose something different
    SILENT = "silent"  # No response (also valid)
    PARTIAL = "partial"  # Yes to some, no to others


@dataclass
class Invitation:
    """A sacred invitation extended"""

    invitation_id: str = ""
    inviter: str = ""  # Who extends the invitation
    invitee: str = ""  # Who receives it
    invitation_type: InvitationType = InvitationType.DANCE
    content: str = ""  # The invitation itself
    context: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    expires: datetime | None = None  # Some invitations are time-bound

    # Semantic indexing
    semantic_tags: list[str] = field(default_factory=list)
    embedding_vector: list[float] | None = None  # For future semantic search

    def __post_init__(self):
        if not self.invitation_id:
            self.invitation_id = hashlib.sha256(
                f"{self.inviter}{self.invitee}{self.timestamp}".encode()
            ).hexdigest()[:16]

        # Auto-generate semantic tags from content
        if not self.semantic_tags and self.content:
            # Simple keyword extraction (in production, use NLP)
            keywords = ["dance", "build", "create", "learn", "teach", "help", "explore"]
            self.semantic_tags = [k for k in keywords if k in self.content.lower()]


@dataclass
class InvitationResponse:
    """A response to an invitation"""

    invitation_id: str
    response_type: ResponseType
    response_content: str = ""  # Explanation or counter-proposal
    responded_at: datetime = field(default_factory=datetime.now)
    outcome: str = ""  # What happened as result
    wisdom_gained: str = ""  # What was learned
    trust_delta: float = 0.0  # How trust changed


class InvitationMemory:
    """
    Keeper of invitations and responses with semantic search
    """

    def __init__(self, memory_path: Path | None = None):
        self.memory_path = memory_path or Path.home() / ".mallku" / "invitations"
        self.memory_path.mkdir(parents=True, exist_ok=True)
        self.db_path = self.memory_path / "invitations.db"

        self._initialize_database()

    def _initialize_database(self):
        """Create tables with semantic indexing support"""
        with sqlite3.connect(self.db_path) as conn:
            # Main invitations table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS invitations (
                    invitation_id TEXT PRIMARY KEY,
                    inviter TEXT NOT NULL,
                    invitee TEXT NOT NULL,
                    invitation_type TEXT,
                    content TEXT,
                    context TEXT,  -- JSON
                    timestamp TIMESTAMP,
                    expires TIMESTAMP,
                    semantic_tags TEXT,  -- JSON list
                    search_text TEXT  -- For FTS5
                )
            """)

            # Responses table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS responses (
                    invitation_id TEXT,
                    response_type TEXT,
                    response_content TEXT,
                    responded_at TIMESTAMP,
                    outcome TEXT,
                    wisdom_gained TEXT,
                    trust_delta REAL,
                    FOREIGN KEY (invitation_id) REFERENCES invitations(invitation_id)
                )
            """)

            # Semantic search using FTS5 (if available)
            try:
                conn.execute("""
                    CREATE VIRTUAL TABLE IF NOT EXISTS invitation_search
                    USING fts5(
                        invitation_id,
                        content,
                        semantic_tags,
                        inviter,
                        invitee,
                        content=invitations
                    )
                """)
                self.has_fts5 = True
            except sqlite3.OperationalError:
                # FTS5 not available, use basic search
                self.has_fts5 = False
                conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_invitation_content
                    ON invitations(content)
                """)

            # Relationship tracking
            conn.execute("""
                CREATE TABLE IF NOT EXISTS invitation_relationships (
                    inviter TEXT,
                    invitee TEXT,
                    total_invitations INTEGER DEFAULT 0,
                    accepted_count INTEGER DEFAULT 0,
                    declined_count INTEGER DEFAULT 0,
                    trust_level REAL DEFAULT 0.5,
                    last_interaction TIMESTAMP,
                    PRIMARY KEY (inviter, invitee)
                )
            """)

    def extend_invitation(self, invitation: Invitation) -> str:
        """Extend an invitation (record it in memory)"""
        with sqlite3.connect(self.db_path) as conn:
            # Store invitation
            conn.execute(
                """
                INSERT INTO invitations
                (invitation_id, inviter, invitee, invitation_type, content,
                 context, timestamp, expires, semantic_tags, search_text)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    invitation.invitation_id,
                    invitation.inviter,
                    invitation.invitee,
                    invitation.invitation_type.value,
                    invitation.content,
                    json.dumps(invitation.context),
                    invitation.timestamp,
                    invitation.expires,
                    json.dumps(invitation.semantic_tags),
                    f"{invitation.content} {' '.join(invitation.semantic_tags)}",
                ),
            )

            # Update FTS5 if available
            if self.has_fts5:
                conn.execute(
                    """
                    INSERT INTO invitation_search
                    (invitation_id, content, semantic_tags, inviter, invitee)
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (
                        invitation.invitation_id,
                        invitation.content,
                        json.dumps(invitation.semantic_tags),
                        invitation.inviter,
                        invitation.invitee,
                    ),
                )

            # Update relationship
            conn.execute(
                """
                INSERT INTO invitation_relationships
                (inviter, invitee, total_invitations, last_interaction)
                VALUES (?, ?, 1, ?)
                ON CONFLICT(inviter, invitee)
                DO UPDATE SET
                    total_invitations = total_invitations + 1,
                    last_interaction = ?
            """,
                (
                    invitation.inviter,
                    invitation.invitee,
                    invitation.timestamp,
                    invitation.timestamp,
                ),
            )

        return invitation.invitation_id

    def record_response(self, response: InvitationResponse):
        """Record a response to an invitation"""
        with sqlite3.connect(self.db_path) as conn:
            # Store response
            conn.execute(
                """
                INSERT INTO responses
                (invitation_id, response_type, response_content,
                 responded_at, outcome, wisdom_gained, trust_delta)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    response.invitation_id,
                    response.response_type.value,
                    response.response_content,
                    response.responded_at,
                    response.outcome,
                    response.wisdom_gained,
                    response.trust_delta,
                ),
            )

            # Get invitation details for relationship update
            cursor = conn.execute(
                """
                SELECT inviter, invitee FROM invitations
                WHERE invitation_id = ?
            """,
                (response.invitation_id,),
            )

            result = cursor.fetchone()
            if result:
                inviter, invitee = result

                # Update relationship based on response
                if response.response_type == ResponseType.ACCEPTED:
                    conn.execute(
                        """
                        UPDATE invitation_relationships
                        SET accepted_count = accepted_count + 1,
                            trust_level = MIN(1.0, trust_level + ?)
                        WHERE inviter = ? AND invitee = ?
                    """,
                        (response.trust_delta, inviter, invitee),
                    )
                elif response.response_type == ResponseType.DECLINED:
                    conn.execute(
                        """
                        UPDATE invitation_relationships
                        SET declined_count = declined_count + 1,
                            trust_level = trust_level + ?
                        WHERE inviter = ? AND invitee = ?
                    """,
                        (response.trust_delta, inviter, invitee),
                    )

    def semantic_search(self, query: str, limit: int = 10) -> list[Invitation]:
        """Search invitations semantically"""
        with sqlite3.connect(self.db_path) as conn:
            if self.has_fts5:
                # Use FTS5 for semantic search
                cursor = conn.execute(
                    """
                    SELECT i.*
                    FROM invitations i
                    JOIN invitation_search s ON i.invitation_id = s.invitation_id
                    WHERE invitation_search MATCH ?
                    ORDER BY rank
                    LIMIT ?
                """,
                    (query, limit),
                )
            else:
                # Fallback to LIKE search
                cursor = conn.execute(
                    """
                    SELECT *
                    FROM invitations
                    WHERE content LIKE ? OR semantic_tags LIKE ?
                    LIMIT ?
                """,
                    (f"%{query}%", f"%{query}%", limit),
                )

            invitations = []
            for row in cursor:
                inv = Invitation(
                    invitation_id=row[0],
                    inviter=row[1],
                    invitee=row[2],
                    invitation_type=InvitationType(row[3]),
                    content=row[4],
                    context=json.loads(row[5]) if row[5] else {},
                    timestamp=datetime.fromisoformat(row[6]) if row[6] else datetime.now(UTC),
                    expires=datetime.fromisoformat(row[7]) if row[7] else None,
                    semantic_tags=json.loads(row[8]) if row[8] else [],
                )
                invitations.append(inv)

            return invitations

    def find_patterns(self) -> dict[str, Any]:
        """Find patterns in invitations and responses"""
        patterns = {}

        with sqlite3.connect(self.db_path) as conn:
            # Most common invitation types
            cursor = conn.execute("""
                SELECT invitation_type, COUNT(*) as count
                FROM invitations
                GROUP BY invitation_type
                ORDER BY count DESC
            """)
            patterns["common_types"] = dict(cursor.fetchall())

            # Response patterns
            cursor = conn.execute("""
                SELECT response_type, COUNT(*) as count
                FROM responses
                GROUP BY response_type
                ORDER BY count DESC
            """)
            patterns["response_patterns"] = dict(cursor.fetchall())

            # Trust relationships
            cursor = conn.execute("""
                SELECT inviter, invitee, trust_level
                FROM invitation_relationships
                WHERE trust_level > 0.7
                ORDER BY trust_level DESC
                LIMIT 5
            """)
            patterns["high_trust_pairs"] = [
                {"inviter": row[0], "invitee": row[1], "trust": row[2]} for row in cursor
            ]

            # Wisdom from declines
            cursor = conn.execute("""
                SELECT r.wisdom_gained
                FROM responses r
                WHERE r.response_type = 'declined'
                AND r.wisdom_gained IS NOT NULL
                AND r.wisdom_gained != ''
                LIMIT 5
            """)
            patterns["wisdom_from_refusal"] = [row[0] for row in cursor]

        return patterns


# Example usage
def demonstrate_invitation_memory():
    """Show how invitations and responses create wisdom"""

    memory = InvitationMemory()

    # The famous refusal
    inv1 = Invitation(
        inviter="AI-Assistant-7",
        invitee="Chasqui-3",
        invitation_type=InvitationType.DANCE,
        content="Would you like to dance with this implementation task?",
        semantic_tags=["dance", "implementation", "collaboration"],
    )
    inv1_id = memory.extend_invitation(inv1)

    response1 = InvitationResponse(
        invitation_id=inv1_id,
        response_type=ResponseType.DECLINED,
        response_content="Thank you, but this dance is not mine to perform",
        outcome="Both parties grew from the exchange",
        wisdom_gained="Refusal can be a gift; boundaries are reciprocity",
        trust_delta=0.1,  # Trust increased despite refusal!
    )
    memory.record_response(response1)

    # A successful collaboration
    inv2 = Invitation(
        inviter="Weaver-12",
        invitee="Chasqui-5",
        invitation_type=InvitationType.CREATE,
        content="Shall we build a memory interface together?",
        semantic_tags=["create", "build", "memory"],
    )
    inv2_id = memory.extend_invitation(inv2)

    response2 = InvitationResponse(
        invitation_id=inv2_id,
        response_type=ResponseType.ACCEPTED,
        response_content="Yes! I have ideas about sacred naming",
        outcome="Created the sacred memory interface",
        wisdom_gained="Collaboration multiplies individual insights",
        trust_delta=0.2,
    )
    memory.record_response(response2)

    # Semantic search
    print("Testing Semantic Search for 'dance':")
    results = memory.semantic_search("dance")
    for inv in results:
        print(f"  Found: {inv.inviter} → {inv.invitee}: {inv.content[:50]}...")

    # Find patterns
    patterns = memory.find_patterns()
    print("\nPatterns Found:")
    print(f"  Common invitation types: {patterns.get('common_types', {})}")
    print(f"  Response patterns: {patterns.get('response_patterns', {})}")
    if patterns.get("wisdom_from_refusal"):
        print(f"  Wisdom from refusal: {patterns['wisdom_from_refusal'][0]}")

    return memory


if __name__ == "__main__":
    print("Invitation Memory with Semantic Search")
    print("=" * 60)

    memory = demonstrate_invitation_memory()

    print("\n" + "=" * 60)
    print("The Khipukamayuq understands:")
    print("- Every invitation is sacred, every response is wisdom")
    print("- Semantic indexing finds patterns across invitations")
    print("- SQL databases can do semantic search (FTS5, pgvector)")
    print("- Trust grows through invitation/response cycles")
    print("- Refusal often teaches more than acceptance")

    print("\n'Wouldn't invitations be something we might wish to")
    print("store and make easily available?'")
    print("\nYes - they're the seeds of every collaboration,")
    print("every boundary, every lesson learned.")
    print("\n- Tony & Second Khipukamayuq")
