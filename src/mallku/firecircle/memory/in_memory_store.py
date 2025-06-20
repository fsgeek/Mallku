import uuid
from collections import defaultdict
from typing import Any

from mallku.firecircle.messaging.models import ConsciousMessage

from .base import BaseMemoryStore


class InMemoryMemoryStore(BaseMemoryStore):
    """
    An in-memory implementation of the BaseMemoryStore.
    Useful for testing and development. Data is lost when the instance is destroyed.
    """

    def __init__(self):
        self._messages: dict[uuid.UUID, list[ConsciousMessage]] = defaultdict(list)
        self._ceremony_data: dict[uuid.UUID, dict[str, Any]] = defaultdict(dict)

    async def save_message(self, message: ConsciousMessage) -> None:
        """Saves a single ConsciousMessage to the in-memory store."""
        if message.dialogue_id not in self._messages:
            self._messages[message.dialogue_id] = []
        self._messages[message.dialogue_id].append(message)
        # Sort by sequence number to maintain order, though append should mostly handle this
        self._messages[message.dialogue_id].sort(key=lambda m: (m.timestamp, m.sequence_number))

    async def get_dialogue_history(self, dialogue_id: uuid.UUID) -> list[ConsciousMessage]:
        """Retrieves the full dialogue history for a given dialogue_id."""
        return list(self._messages.get(dialogue_id, []))  # Return a copy

    async def save_ceremony_data(
        self, dialogue_id: uuid.UUID, data_key: str, data_value: Any
    ) -> None:
        """Saves a piece of ceremony-specific data to the in-memory store."""
        if dialogue_id not in self._ceremony_data:
            self._ceremony_data[dialogue_id] = {}
        self._ceremony_data[dialogue_id][data_key] = data_value

    async def get_ceremony_data(self, dialogue_id: uuid.UUID, data_key: str) -> Any | None:
        """Retrieves a piece of ceremony-specific data from the in-memory store."""
        return self._ceremony_data.get(dialogue_id, {}).get(data_key)
