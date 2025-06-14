"""
Async Base Class for Mallku Components
=====================================

Provides common async lifecycle management for all Mallku components.
"""

import logging
from abc import ABC

logger = logging.getLogger(__name__)


class AsyncBase(ABC):
    """
    Base class for async components in Mallku.

    Provides:
    - Initialization lifecycle
    - Shutdown lifecycle
    - Logging setup
    - Common state management
    """

    def __init__(self):
        """Initialize base component."""
        self._initialized = False
        self.logger = logging.getLogger(self.__class__.__module__)

    async def initialize(self) -> None:
        """Initialize the component."""
        if self._initialized:
            self.logger.warning(f"{self.__class__.__name__} already initialized")
            return

        self._initialized = True
        self.logger.info(f"{self.__class__.__name__} initialized")

    async def shutdown(self) -> None:
        """Shutdown the component."""
        if not self._initialized:
            self.logger.warning(f"{self.__class__.__name__} not initialized")
            return

        self._initialized = False
        self.logger.info(f"{self.__class__.__name__} shut down")

    @property
    def is_initialized(self) -> bool:
        """Check if component is initialized."""
        return self._initialized

    def __repr__(self) -> str:
        """String representation."""
        return f"{self.__class__.__name__}(initialized={self._initialized})"
