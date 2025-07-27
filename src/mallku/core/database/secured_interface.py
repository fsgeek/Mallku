"""
Secured Database Interface - Deprecated
=======================================

This module is now a compatibility layer. The core implementation has been
moved to secured_arango_interface.py to follow the "single interface,
multiple implementations" pattern.
"""

from .secured_arango_interface import (
    CollectionSecurityPolicy,
    SecuredArangoDatabase,
    SecuredCollectionWrapper,
    SecurityViolationError,
)

# Backward compatibility alias
SecuredDatabaseInterface = SecuredArangoDatabase

__all__ = [
    "SecuredArangoDatabase",
    "SecuredDatabaseInterface",  # Backward compatibility
    "SecuredCollectionWrapper",
    "CollectionSecurityPolicy",
    "SecurityViolationError",
]
