"""
Mallku Database Core
====================

This package provides the unified, secure database interface for Mallku.
"""

from .factory import get_database
from .secured_arango_interface import (
    CollectionSecurityPolicy,
    SecuredArangoDatabase,
    SecuredCollectionWrapper,
    SecurityViolationError,
)

__all__ = [
    "get_database",
    "SecuredArangoDatabase",
    "SecuredCollectionWrapper",
    "CollectionSecurityPolicy",
    "SecurityViolationError",
]
