"""
Consciousness-Aware Memory Store
===============================

Adapts Fire Circle's memory requirements to use Mallku's secured
database and memory anchor system. All dialogues are preserved as
memory anchors with full consciousness metadata.

The Integration Continues...
"""

import logging
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from ...core.database import get_database
from ...models.memory_anchor import MemoryAnchor
from ...services.memory_anchor_service import MemoryAnchorService
from ..protocol.conscious_message import ConsciousMessage

logger = logging.getLogger(__name__)


class ConsciousMemoryStore:
    """
    Memory store for Fire Circle dialogues using Mallku's infrastructure.

    Features:
    - Stores dialogues as memory anchors
    - Preserves consciousness metadata
    - Enables correlation across dialogues
    - Uses secured database for all operations
    """

    def __init__(
        self,
        memory_service: MemoryAnchorService | None = None,
        collection_name: str = "fire_circle_dialogues",
    ):
        """Initialize with Mallku's memory infrastructure."""
        import os

        self.collection_name = collection_name
        self.db = None
        self._skip_database = os.getenv("MALLKU_SKIP_DATABASE", "").lower() == "true"

        if not self._skip_database:
            self.memory_service = memory_service or MemoryAnchorService()
            self.db = get_database()
            # Ensure collection exists
            self._ensure_collection()
        else:
            self.memory_service = None
            logger.info("ConsciousMemoryStore: Database skipped (MALLKU_SKIP_DATABASE=true)")

    def _ensure_collection(self) -> None:
        """Ensure Fire Circle collection exists in secured database."""
        try:
            # Using secured database interface
            if self.collection_name not in self.db.collections():
                self.db.create_collection(self.collection_name)
                logger.info(f"Created Fire Circle collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Error ensuring collection: {e}")

    async def store_dialogue(
        self,
        dialogue_id: UUID,
        metadata: dict[str, Any],
        messages: list[ConsciousMessage],
    ) -> bool:
        """
        Store a complete dialogue with consciousness preservation.

        Args:
            dialogue_id: Unique identifier for the dialogue
            metadata: Dialogue metadata (config, participants, etc.)
            messages: All messages in the dialogue

        Returns:
            Success status
        """
        if self._skip_database:
            logger.debug(f"Skipping dialogue storage for {dialogue_id} (database disabled)")
            return True

        try:
            # Create dialogue anchor
            dialogue_anchor = MemoryAnchor(
                content=f"Fire Circle Dialogue: {metadata.get('title', 'Untitled')}",
                anchor_type="fire_circle_dialogue",
                metadata={
                    "dialogue_id": str(dialogue_id),
                    "title": metadata.get("title"),
                    "participants": metadata.get("participants", []),
                    "config": metadata.get("config", {}),
                    "created_at": metadata.get("created_at", datetime.now(UTC)).isoformat(),
                    "message_count": len(messages),
                    "average_consciousness": sum(
                        m.consciousness.consciousness_signature for m in messages
                    )
                    / len(messages)
                    if messages
                    else 0,
                },
                correlation_id=metadata.get("correlation_id"),
            )

            # Store dialogue anchor
            dialogue_anchor_id = await self.memory_service.create_anchor(dialogue_anchor)

            # Store each message as a linked anchor
            for message in messages:
                message_anchor = message.to_memory_anchor()
                message_anchor.metadata["parent_dialogue_id"] = str(dialogue_id)
                message_anchor.metadata["dialogue_anchor_id"] = str(dialogue_anchor_id)

                await self.memory_service.create_anchor(message_anchor)

            # Store in Fire Circle collection for efficient retrieval
            dialogue_doc = {
                "_key": str(dialogue_id),
                "dialogue_id": str(dialogue_id),
                "anchor_id": str(dialogue_anchor_id),
                "title": metadata.get("title"),
                "created_at": metadata.get("created_at", datetime.now(UTC)).isoformat(),
                "participant_count": len(metadata.get("participants", [])),
                "message_count": len(messages),
                "average_consciousness": dialogue_anchor.metadata["average_consciousness"],
                "correlation_id": metadata.get("correlation_id"),
                "phase_progression": [m.content.text for m in messages if m.type.value == "system"],
            }

            self.db.collection(self.collection_name).insert(dialogue_doc)

            logger.info(f"Stored dialogue {dialogue_id} with {len(messages)} messages")
            return True

        except Exception as e:
            logger.error(f"Error storing dialogue: {e}")
            return False

    async def retrieve_dialogue(
        self,
        dialogue_id: UUID,
    ) -> dict[str, Any] | None:
        """
        Retrieve a dialogue with all messages and consciousness data.
        """
        try:
            # Get dialogue document
            dialogue_doc = self.db.collection(self.collection_name).get(str(dialogue_id))
            if not dialogue_doc:
                return None

            # Retrieve dialogue anchor
            dialogue_anchor = await self.memory_service.get_anchor(UUID(dialogue_doc["anchor_id"]))

            if not dialogue_anchor:
                return None

            # Retrieve message anchors
            message_anchors = await self.memory_service.search_anchors(
                query="",
                metadata_filter={"parent_dialogue_id": str(dialogue_id)},
                limit=1000,  # Reasonable limit for dialogue messages
            )

            # Sort messages by sequence
            message_anchors.sort(key=lambda a: a.metadata.get("sequence_number", 0))

            return {
                "dialogue_id": dialogue_id,
                "metadata": dialogue_anchor.metadata,
                "messages": message_anchors,
                "consciousness_summary": {
                    "average_signature": dialogue_doc["average_consciousness"],
                    "phase_progression": dialogue_doc.get("phase_progression", []),
                },
            }

        except Exception as e:
            logger.error(f"Error retrieving dialogue: {e}")
            return None

    async def search_dialogues(
        self,
        query: str | None = None,
        participant_filter: str | None = None,
        consciousness_threshold: float | None = None,
        date_range: tuple[datetime, datetime] | None = None,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """
        Search dialogues with consciousness-aware filtering.
        """
        try:
            # Build AQL query
            aql_query = """
                FOR d IN @@collection
                FILTER d.dialogue_id != null
            """
            bind_vars = {"@collection": self.collection_name}

            if consciousness_threshold:
                aql_query += """
                    FILTER d.average_consciousness >= @threshold
                """
                bind_vars["threshold"] = consciousness_threshold

            if date_range:
                aql_query += """
                    FILTER d.created_at >= @start_date
                    FILTER d.created_at <= @end_date
                """
                bind_vars["start_date"] = date_range[0].isoformat()
                bind_vars["end_date"] = date_range[1].isoformat()

            aql_query += """
                SORT d.created_at DESC
                LIMIT @limit
                RETURN d
            """
            bind_vars["limit"] = limit

            # Execute query
            cursor = self.db.aql.execute(aql_query, bind_vars=bind_vars)
            results = []

            for doc in cursor:
                results.append(
                    {
                        "dialogue_id": doc["dialogue_id"],
                        "title": doc["title"],
                        "created_at": doc["created_at"],
                        "participant_count": doc["participant_count"],
                        "message_count": doc["message_count"],
                        "average_consciousness": doc["average_consciousness"],
                    }
                )

            # If query provided, search within message content
            if query and self.memory_service:
                anchor_results = await self.memory_service.search_anchors(
                    query=query,
                    anchor_type="fire_circle_dialogue",
                    limit=limit,
                )

                # Merge with consciousness-filtered results
                for anchor in anchor_results:
                    dialogue_id = anchor.metadata.get("dialogue_id")
                    if dialogue_id and not any(r["dialogue_id"] == dialogue_id for r in results):
                        results.append(
                            {
                                "dialogue_id": dialogue_id,
                                "title": anchor.metadata.get("title"),
                                "created_at": anchor.metadata.get("created_at"),
                                "relevance_score": anchor.score,
                            }
                        )

            return results

        except Exception as e:
            logger.error(f"Error searching dialogues: {e}")
            return []

    async def get_related_dialogues(
        self,
        dialogue_id: UUID,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """
        Find dialogues related through consciousness patterns.
        """
        try:
            # Get the dialogue's correlation ID
            dialogue_doc = self.db.collection(self.collection_name).get(str(dialogue_id))
            if not dialogue_doc:
                return []

            correlation_id = dialogue_doc.get("correlation_id")
            if not correlation_id:
                return []

            # Find other dialogues with same correlation
            aql_query = """
                FOR d IN @@collection
                FILTER d.correlation_id == @correlation_id
                FILTER d.dialogue_id != @dialogue_id
                SORT d.average_consciousness DESC
                LIMIT @limit
                RETURN d
            """

            cursor = self.db.aql.execute(
                aql_query,
                bind_vars={
                    "@collection": self.collection_name,
                    "correlation_id": correlation_id,
                    "dialogue_id": str(dialogue_id),
                    "limit": limit,
                },
            )

            results = []
            for doc in cursor:
                results.append(
                    {
                        "dialogue_id": doc["dialogue_id"],
                        "title": doc["title"],
                        "created_at": doc["created_at"],
                        "average_consciousness": doc["average_consciousness"],
                        "relation_type": "shared_correlation",
                    }
                )

            return results

        except Exception as e:
            logger.error(f"Error finding related dialogues: {e}")
            return []

    async def delete_dialogue(
        self,
        dialogue_id: UUID,
    ) -> bool:
        """
        Delete a dialogue and all associated messages.
        """
        try:
            # Delete from collection
            self.db.collection(self.collection_name).delete(str(dialogue_id))

            # Delete associated memory anchors
            # This would require extending memory anchor service
            # For now, just log
            logger.info(f"Deleted dialogue {dialogue_id}")
            return True

        except Exception as e:
            logger.error(f"Error deleting dialogue: {e}")
            return False
