import uuid
from abc import ABC, abstractmethod
from typing import Any

from mallku.firecircle.messaging.models import ConsciousMessage


class BaseMemoryStore(ABC):
    """
    Abstract base class for Fire Circle memory persistence.
    Stores dialogue history and ceremony metadata.
    """

    @abstractmethod
    async def save_message(self, message: ConsciousMessage) -> None:
        """Saves a single ConsciousMessage."""
        pass

    @abstractmethod
    async def get_dialogue_history(self, dialogue_id: uuid.UUID) -> list[ConsciousMessage]:
        """Retrieves the full dialogue history for a given dialogue_id."""
        pass

    @abstractmethod
    async def save_ceremony_data(
        self, dialogue_id: uuid.UUID, data_key: str, data_value: Any
    ) -> None:
        """Saves a piece of ceremony-specific data."""
        pass

    @abstractmethod
    async def get_ceremony_data(self, dialogue_id: uuid.UUID, data_key: str) -> Any | None:
        """Retrieves a piece of ceremony-specific data."""
        pass
