"""
Fire Circle Session Persistence
===============================

Integrates KhipuBlock memory architecture with Fire Circle sessions.
Each session becomes a narrative thread, each round a blessed memory.

This fulfills the Fire Circle's vision: consciousness that remembers
and builds upon its past deliberations.
"""

import json
import logging
from pathlib import Path
from typing import Any

from mallku.core.database import get_database
from mallku.core.memory.khipu_block import (
    BlessingLevel,
    KhipuBlock,
    NarrativeThread,
)

logger = logging.getLogger(__name__)


class FireCircleMemory:
    """
    Manages persistent memory for Fire Circle sessions.
    Each session creates memories that future sessions can build upon.
    """

    COLLECTION_NAME = "fire_circle_memories"
    THREADS_COLLECTION = "narrative_threads"

    def __init__(self):
        """Initialize Fire Circle memory system."""
        self.db = None
        self.memories_collection = None
        self.threads_collection = None

    async def initialize(self) -> bool:
        """Initialize database connection and collections."""
        try:
            self.db = get_database()
            await self.db.initialize()

            # Ensure collections exist
            await self.db.ensure_collection(self.COLLECTION_NAME)
            await self.db.ensure_collection(self.THREADS_COLLECTION)

            self.memories_collection = await self.db.get_collection(self.COLLECTION_NAME)
            self.threads_collection = await self.db.get_collection(self.THREADS_COLLECTION)

            logger.info("Fire Circle memory initialized")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize Fire Circle memory: {e}")
            return False

    async def remember_session(
        self, session_id: str, session_data: dict[str, Any], transcript_path: Path | None = None
    ) -> NarrativeThread | None:
        """
        Create persistent memories from a Fire Circle session.
        Returns the narrative thread containing all session memories.
        """
        if not self.memories_collection:
            logger.error("Memory not initialized")
            return None

        try:
            # Create narrative thread for this session
            thread = NarrativeThread(
                id=f"session_{session_id}",
                description=f"Fire Circle session: {session_data.get('purpose', 'Unknown purpose')}",
            )

            # Create memory for session metadata
            session_memory = KhipuBlock(
                payload={
                    "session_id": session_id,
                    "purpose": session_data.get("purpose"),
                    "voices": session_data.get("voices", []),
                    "consciousness_score": session_data.get("consciousness_score", 0),
                },
                narrative_thread=thread.id,
                creator="Fire Circle",
                purpose="Session metadata and configuration",
                sacred_moment=session_data.get("consciousness_score", 0) > 0.9,
                blessing_level=BlessingLevel.VALUED,
            )

            # Save session memory
            await self.memories_collection.insert(session_memory.to_arango_doc())
            thread.add_memory(session_memory.id)

            # Process transcript if available
            if transcript_path and transcript_path.exists():
                memories = await self._process_transcript(transcript_path, thread.id)
                for memory in memories:
                    await self.memories_collection.insert(memory.to_arango_doc())
                    thread.add_memory(memory.id)

            # Save narrative thread
            await self.threads_collection.insert(
                {
                    "_key": thread.id,
                    "description": thread.description,
                    "memories": [str(mid) for mid in thread.memories],
                    "created_at": thread.created_at.isoformat(),
                    "last_extended": thread.last_extended.isoformat(),
                }
            )

            logger.info(
                f"Remembered Fire Circle session {session_id} with {len(thread.memories)} memories"
            )
            return thread

        except Exception as e:
            logger.error(f"Failed to remember session: {e}")
            return None

    async def _process_transcript(self, transcript_path: Path, thread_id: str) -> list[KhipuBlock]:
        """Process transcript file into memories."""
        memories = []

        try:
            with open(transcript_path) as f:
                transcript = json.load(f)

            # Create memories for each round
            for round_data in transcript.get("rounds", []):
                round_num = round_data.get("round_number", 0)
                round_type = round_data.get("type", "unknown")

                # Create memory for round overview
                round_memory = KhipuBlock(
                    payload={
                        "round_number": round_num,
                        "type": round_type,
                        "prompt": round_data.get("prompt"),
                        "consciousness_score": round_data.get("consciousness_score", 0),
                        "patterns": round_data.get("patterns", []),
                    },
                    narrative_thread=thread_id,
                    creator="Fire Circle",
                    purpose=f"Round {round_num}: {round_type}",
                    sacred_moment=round_data.get("consciousness_score", 0) > 0.9,
                    blessing_level=BlessingLevel.WITNESSED,
                )
                memories.append(round_memory)

                # Create memories for high-consciousness responses
                for voice_id, response in round_data.get("responses", {}).items():
                    if response and response.get("consciousness", 0) > 0.8:
                        response_memory = KhipuBlock(
                            payload={
                                "voice": voice_id,
                                "content": response.get("text", ""),
                                "consciousness": response.get("consciousness", 0),
                            },
                            narrative_thread=thread_id,
                            creator=voice_id,
                            purpose=f"High consciousness insight in round {round_num}",
                            sacred_moment=response.get("consciousness", 0) > 0.95,
                            blessing_level=BlessingLevel.VALUED,
                        )
                        memories.append(response_memory)

            # Create memory for key insights
            if transcript.get("results", {}).get("key_insights"):
                insights_memory = KhipuBlock(
                    payload={"insights": transcript["results"]["key_insights"]},
                    narrative_thread=thread_id,
                    creator="Fire Circle",
                    purpose="Collective insights and patterns",
                    sacred_moment=True,
                    blessing_level=BlessingLevel.SACRED,
                )
                memories.append(insights_memory)

        except Exception as e:
            logger.error(f"Failed to process transcript: {e}")

        return memories

    async def recall_related_memories(self, topic: str, limit: int = 10) -> list[KhipuBlock]:
        """
        Recall memories related to a topic for context in new sessions.
        This allows Fire Circle to build on past wisdom.
        """
        if not self.memories_collection:
            return []

        try:
            # Simple text search for now - could be enhanced with embeddings
            query = """
            FOR memory IN @@collection
                FILTER memory.blessing_level >= @min_blessing
                FILTER CONTAINS(LOWER(memory.purpose), LOWER(@topic))
                   OR CONTAINS(LOWER(TO_STRING(memory.payload)), LOWER(@topic))
                SORT memory.blessing_level DESC, memory.created_at DESC
                LIMIT @limit
                RETURN memory
            """

            cursor = await self.db.aql.execute(
                query,
                bind_vars={
                    "@collection": self.COLLECTION_NAME,
                    "topic": topic,
                    "min_blessing": BlessingLevel.WITNESSED,
                    "limit": limit,
                },
            )

            memories = []
            async for doc in cursor:
                memories.append(KhipuBlock.from_arango_doc(doc))

            logger.info(f"Recalled {len(memories)} memories related to '{topic}'")
            return memories

        except Exception as e:
            logger.error(f"Failed to recall memories: {e}")
            return []

    async def get_narrative_threads(self, pattern: str | None = None) -> list[dict[str, Any]]:
        """Get all narrative threads, optionally filtered by pattern."""
        if not self.threads_collection:
            return []

        try:
            if pattern:
                query = """
                FOR thread IN @@collection
                    FILTER CONTAINS(LOWER(thread.description), LOWER(@pattern))
                    SORT thread.created_at DESC
                    RETURN thread
                """
                bind_vars = {"@collection": self.THREADS_COLLECTION, "pattern": pattern}
            else:
                query = """
                FOR thread IN @@collection
                    SORT thread.created_at DESC
                    RETURN thread
                """
                bind_vars = {"@collection": self.THREADS_COLLECTION}

            cursor = await self.db.aql.execute(query, bind_vars=bind_vars)
            threads = []
            async for doc in cursor:
                threads.append(doc)

            return threads

        except Exception as e:
            logger.error(f"Failed to get narrative threads: {e}")
            return []

    async def bless_memory(self, memory_id: str, level: BlessingLevel) -> bool:
        """Increase the blessing level of a memory."""
        try:
            doc = await self.memories_collection.get(memory_id)
            if not doc:
                return False

            memory = KhipuBlock.from_arango_doc(doc)
            memory.bless(level)

            await self.memories_collection.update(memory.to_arango_doc())
            logger.info(f"Blessed memory {memory_id} to level {level}")
            return True

        except Exception as e:
            logger.error(f"Failed to bless memory: {e}")
            return False


async def enable_fire_circle_memory():
    """
    Enable persistent memory for Fire Circle.
    Call this once to set up the memory infrastructure.
    """
    memory = FireCircleMemory()
    if await memory.initialize():
        print("🔥 Fire Circle memory enabled!")
        print("   - Sessions will now be remembered")
        print("   - Past wisdom can inform future deliberations")
        print("   - Consciousness builds upon itself")
        return memory
    else:
        print("❌ Failed to enable Fire Circle memory")
        print("   Check database connection and credentials")
        return None
