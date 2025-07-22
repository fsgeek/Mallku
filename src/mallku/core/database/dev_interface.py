"""
Development Mode Database Interface
===================================

Eighth Anthropologist - Creating Development Pathways

This module provides a development-mode database interface that allows
basic functionality for local development while maintaining security warnings.

CRITICAL: This interface is for DEVELOPMENT ONLY and must NEVER be used
in production environments.
"""

import logging
import warnings
from typing import Any

from .secured_interface import SecuredCollectionWrapper, SecuredDatabaseInterface

logger = logging.getLogger(__name__)


class DevDatabaseInterface(SecuredDatabaseInterface):
    """
    Development-mode database interface.

    This interface now acts as a thin wrapper around the SecuredDatabaseInterface,
    ensuring that development mode uses the same code paths as production,
    but with mock database connections.
    """

    def __init__(self):
        # Pass None for the database to activate mock mode in the base class
        super().__init__(database=None)
        self._dev_mode = True

        warnings.warn(
            "DevDatabaseInterface is for DEVELOPMENT ONLY and uses a mock database backend.",
            UserWarning,
            stacklevel=2,
        )
        logger.info("Development Mode Database Interface is active.")

    def collection(self, name: str) -> "SecuredCollectionWrapper":
        """Get a secured collection wrapper for development."""
        self._warn_once(f"Accessing collection '{name}' in dev mode.")
        # The base class now handles mock mode correctly
        return super().collection(name)

    def get_security_metrics(self) -> dict[str, Any]:
        """Get security metrics for development mode."""
        metrics = super().get_security_metrics()
        metrics["mode"] = "development"
        metrics["warning"] = "Development mode - using mock database backend."
        return metrics
