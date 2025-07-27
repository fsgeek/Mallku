"""
Secured ArangoDB Interface
==========================

6th Reviewer - Healing the Fractured Foundation (The True Ceremony)

This module provides the ONLY authorized path to database operations in Mallku,
mirroring the python-arango driver's interface to make the secure path the
most familiar and convenient path.
"""

import logging
from typing import Any

from arango.collection import StandardCollection
from arango.database import StandardDatabase

from ..security.registry import SecurityRegistry
from ..security.secured_model import SecuredModel

logger = logging.getLogger(__name__)


class SecurityViolationError(Exception):
    """Raised when an operation violates security policies."""

    pass


class CollectionSecurityPolicy:
    """
    Security policy for a specific collection.
    """

    def __init__(
        self,
        collection_name: str,
        allowed_model_types: list[type[SecuredModel]],
        requires_security: bool = True,
        schema_validation: dict | None = None,
    ):
        self.collection_name = collection_name
        self.allowed_model_types = allowed_model_types
        self.requires_security = requires_security
        self.schema_validation = schema_validation or {}

    def validate_model(self, model: Any) -> None:
        """Validate that a model is allowed for this collection."""
        if self.requires_security:
            if not isinstance(model, SecuredModel):
                raise SecurityViolationError(
                    f"Collection {self.collection_name} requires SecuredModel instances. "
                    f"Got {type(model).__name__}."
                )
            if not any(isinstance(model, t) for t in self.allowed_model_types):
                allowed = [t.__name__ for t in self.allowed_model_types]
                raise SecurityViolationError(
                    f"Model type {type(model).__name__} not allowed in {self.collection_name}. "
                    f"Allowed: {allowed}"
                )


class SecuredCollectionWrapper:
    """
    Wrapper around an ArangoDB collection that enforces security policies.
    """

    def __init__(
        self,
        collection: StandardCollection,
        policy: CollectionSecurityPolicy,
        security_registry: SecurityRegistry,
        parent_interface: "SecuredArangoDatabase",
    ):
        self._collection = collection
        self._policy = policy
        self._security_registry = security_registry
        self._parent_interface = parent_interface

    async def insert_secured(self, model: SecuredModel) -> dict:
        """Insert a single secured model into the collection."""
        self._policy.validate_model(model)
        obfuscated_data = model.to_storage_dict(self._security_registry)
        model_id = getattr(model, "id", None)
        if model_id is not None:
            obfuscated_data["_key"] = str(model_id)
        result = self._collection.insert(obfuscated_data)
        self._parent_interface._operation_count += 1
        self._parent_interface._save_registry()
        return result  # type: ignore

    async def insert_many_secured(self, models: list[SecuredModel]) -> list[dict]:
        """Insert multiple secured models into the collection."""
        if not models:
            return []
        obfuscated_docs = []
        for model in models:
            self._policy.validate_model(model)
            obfuscated_data = model.to_storage_dict(self._security_registry)
            model_id = getattr(model, "id", None)
            if model_id is not None:
                obfuscated_data["_key"] = str(model_id)
            obfuscated_docs.append(obfuscated_data)
        results = self._collection.insert_many(obfuscated_docs)
        self._parent_interface._operation_count += len(models)
        self._parent_interface._save_registry()
        return results  # type: ignore

    # Blocked operations that raise SecurityViolationError
    def insert(self, document: dict) -> None:
        """Direct insert is not allowed."""
        raise SecurityViolationError(
            "Direct access to insert is not allowed. Use insert_secured instead."
        )

    def insert_many(self, documents: list) -> None:
        """Direct insert_many is not allowed."""
        raise SecurityViolationError(
            "Direct access to insert_many is not allowed. Use insert_many_secured instead."
        )

    def update(self, document: dict, new_values: dict) -> None:
        """Direct update is not allowed."""
        raise SecurityViolationError(
            "Direct access to update is not allowed. Use update_secured instead."
        )

    def replace(self, document: dict, new_document: dict) -> None:
        """Direct replace is not allowed."""
        raise SecurityViolationError(
            "Direct access to replace is not allowed. Use replace_secured instead."
        )

    def delete(self, document: dict) -> None:
        """Direct delete is not allowed."""
        raise SecurityViolationError(
            "Direct access to delete is not allowed. Use delete_secured instead."
        )

    def truncate(self) -> None:
        """Direct truncate is not allowed."""
        raise SecurityViolationError(
            "Direct access to truncate is not allowed. Use truncate_secured instead."
        )

    def update_many(self, documents: list) -> None:
        """Direct update_many is not allowed."""
        raise SecurityViolationError(
            "Direct access to update_many is not allowed. Use update_many_secured instead."
        )

    def delete_many(self, documents: list) -> None:
        """Direct delete_many is not allowed."""
        raise SecurityViolationError(
            "Direct access to delete_many is not allowed. Use delete_many_secured instead."
        )

    # Safe operations that delegate to underlying collection
    def count(self) -> int:
        """Return the number of documents in the collection."""
        return self._collection.count()  # type: ignore

    def exists(self) -> bool:
        """Check if the collection exists."""
        return True  # If we have a wrapper, the collection exists

    def __getattr__(self, name: str) -> Any:
        """Delegate safe methods to the underlying collection object."""
        # List of explicitly safe read-only methods
        safe_methods = ["count", "exists", "name", "all", "find", "get", "has"]
        if name in safe_methods:
            return getattr(self._collection, name)

        # Block any other method access
        raise SecurityViolationError(
            f"Direct access to {name} is not allowed through secured interface."
        )


class SecuredArangoDatabase:
    """
    A wrapper around the ArangoDB database driver that enforces Mallku's
    security policies. This class mirrors the interface of
    arango.database.StandardDatabase.
    """

    def __init__(self, database: StandardDatabase):
        self._database = database
        self._security_registry = SecurityRegistry()
        self._collection_policies: dict[str, CollectionSecurityPolicy] = {}
        self._initialized = False
        self._operation_count = 0
        self._security_violations: list[str] = []

    async def initialize(self):
        """Initializes the secured database interface."""
        if self._initialized:
            return
        # In a real implementation, this would load policies, etc.
        self._initialized = True
        logger.info("SecuredArangoDatabase initialized.")

    def register_collection_policy(self, policy: CollectionSecurityPolicy):
        """Registers a security policy for a collection."""
        self._collection_policies[policy.collection_name] = policy
        logger.info(f"Registered security policy for collection: {policy.collection_name}")

    async def create_secured_collection(
        self, name: str, policy: CollectionSecurityPolicy
    ) -> SecuredCollectionWrapper:
        """Creates a secured collection with the given policy."""
        # Register the policy
        self.register_collection_policy(policy)

        # Create the collection if it doesn't exist
        if not self._database.has_collection(name):
            self._database.create_collection(name)

        # Return the secured wrapper
        real_collection = self._database.collection(name)
        return SecuredCollectionWrapper(real_collection, policy, self._security_registry, self)

    async def get_secured_collection(self, name: str) -> SecuredCollectionWrapper:
        """Gets a secured collection wrapper."""
        if name not in self._collection_policies:
            raise SecurityViolationError(f"No security policy registered for collection: {name}")
        if not self._database.has_collection(name):
            self._database.create_collection(name)

        real_collection = self._database.collection(name)
        policy = self._collection_policies[name]
        return SecuredCollectionWrapper(real_collection, policy, self._security_registry, self)

    def get_security_registry(self) -> SecurityRegistry:
        """Gets the security registry."""
        return self._security_registry

    def get_security_metrics(self) -> dict[str, Any]:
        """Gets security metrics."""
        return {
            "operations_count": self._operation_count,
            "security_violations": len(self._security_violations),
            "registered_collections": len(self._collection_policies),
            "uuid_mappings": len(self._security_registry._mappings),
            "recent_violations": self._security_violations[-10:]
            if self._security_violations
            else [],
        }

    async def execute_secured_query(self, query: str, **kwargs) -> list[dict]:
        """Executes a secured query."""
        # This is a simplified implementation. A real implementation would
        # parse the query and apply security policies.
        bind_vars = kwargs.get("bind_vars", {})
        cursor = self._database.aql.execute(query, bind_vars=bind_vars)
        return [doc for doc in cursor]

    def collection(self, name: str) -> SecuredCollectionWrapper:
        """Return a secured collection API wrapper."""
        if name not in self._collection_policies:
            default_policy = CollectionSecurityPolicy(
                collection_name=name,
                allowed_model_types=[],
                requires_security=False,
            )
            self._collection_policies[name] = default_policy

        if not self._database.has_collection(name):
            self._database.create_collection(name)

        real_collection = self._database.collection(name)
        policy = self._collection_policies[name]

        return SecuredCollectionWrapper(real_collection, policy, self._security_registry, self)

    def has_collection(self, name: str) -> bool:
        """Check if a collection exists."""
        return self._database.has_collection(name)  # type: ignore

    def __getattr__(self, name: str) -> Any:
        """
        For any other attribute, raise a NotImplementedError that guides
        the developer on how to implement it securely.
        """
        if hasattr(self._database, name):
            raise NotImplementedError(
                f"Method '{name}' is not yet securely implemented in SecuredArangoDatabase."
            )
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def _save_registry(self):
        """Placeholder for saving the security registry."""
        logger.debug("Security registry would be saved here.")
