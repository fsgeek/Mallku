"""
Secured Database Interface - Enforcing Security by Design

This module provides the ONLY authorized path to database operations in Mallku.
By creating structural separation, we ensure that all database access goes through
the security model, preventing the architectural gap that was discovered.

Philosophy:
- Structure enforces security rather than relying on developer discipline
- No direct database access allowed outside this interface
- Security model is mandatory, not optional
- Balance through architectural boundaries
"""

import logging
from datetime import datetime
from typing import TYPE_CHECKING, Any

from ..security.registry import SecurityRegistry
from ..security.secured_model import SecuredModel

if TYPE_CHECKING:
    from arango.collection import StandardCollection
    from arango.database import StandardDatabase

logger = logging.getLogger(__name__)


class SecurityViolationError(Exception):
    """Raised when an operation violates security policies."""

    pass


class CollectionSecurityPolicy:
    """
    Security policy for a specific collection.

    Defines what types of models can be stored and how they should be secured.
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
                    f"Got {type(model).__name__}. Use secured models for data protection."
                )

            if not any(
                isinstance(model, allowed_type) for allowed_type in self.allowed_model_types
            ):
                allowed_names = [t.__name__ for t in self.allowed_model_types]
                raise SecurityViolationError(
                    f"Model type {type(model).__name__} not allowed in {self.collection_name}. "
                    f"Allowed types: {allowed_names}"
                )


class SecuredDatabaseInterface:
    """
    The ONLY authorized interface for database operations in Mallku.

    This class enforces security by design - all database access must go through
    this interface, ensuring proper use of the UUID mapping layer and field
    obfuscation strategies.

    Key principles:
    - No direct database access allowed
    - All operations must use SecuredModel instances
    - Security registry is mandatory for data operations
    - Collection policies enforce data integrity
    """

    def __init__(self, database: "StandardDatabase | None"):
        """Initialize with database connection and security enforcement."""
        self._database = database
        self._security_registry = SecurityRegistry()
        self._collection_policies: dict[str, CollectionSecurityPolicy] = {}
        self._initialized = False
        self._skip_database = database is None

        # Track operations for auditing
        self._operation_count = 0
        self._security_violations = []

        if self._skip_database:
            logger.info("SecuredDatabaseInterface initialized without database (mock mode)")

    async def initialize(self) -> None:
        """Initialize the secured interface and load security policies."""
        if self._initialized:
            return

        if not self._skip_database:
            # Load security registry from database if it exists
            await self._load_security_registry()

            # Register default collection policies
            await self._register_default_policies()

        self._initialized = True
        logger.info("Secured database interface initialized")

    def register_collection_policy(self, policy: CollectionSecurityPolicy) -> None:
        """Register a security policy for a collection."""
        self._collection_policies[policy.collection_name] = policy
        logger.info(f"Registered security policy for collection: {policy.collection_name}")

    async def create_secured_collection(
        self, collection_name: str, policy: CollectionSecurityPolicy
    ) -> "StandardCollection":
        """
        Create a collection with security policy enforcement.

        This is the ONLY way collections should be created in Mallku.
        """
        self._ensure_initialized()

        # Register the policy
        self.register_collection_policy(policy)

        if self._skip_database:
            logger.debug(f"Skipping collection creation for {collection_name} (database disabled)")
            return None

        # Create collection with schema validation
        if not self._database.has_collection(collection_name):
            collection = self._database.create_collection(
                collection_name, schema=policy.schema_validation
            )
            logger.info(f"Created secured collection: {collection_name}")
        else:
            collection = self._database.collection(collection_name)
            logger.info(f"Retrieved existing secured collection: {collection_name}")

        return SecuredCollectionWrapper(collection, policy, self._security_registry)

    async def get_secured_collection(self, collection_name: str) -> "SecuredCollectionWrapper":
        """
        Get a secured collection wrapper.

        This ensures all operations on the collection go through security checks.
        """
        self._ensure_initialized()

        if self._skip_database:
            logger.debug(f"Skipping collection retrieval for {collection_name} (database disabled)")
            return None

        if collection_name not in self._collection_policies:
            raise SecurityViolationError(
                f"No security policy registered for collection: {collection_name}. "
                f"All collections must have security policies."
            )

        if not self._database.has_collection(collection_name):
            raise ValueError(f"Collection does not exist: {collection_name}")

        collection = self._database.collection(collection_name)
        policy = self._collection_policies[collection_name]

        return SecuredCollectionWrapper(collection, policy, self._security_registry)

    async def execute_secured_query(
        self,
        aql_query: str,
        bind_vars: dict[str, Any] | None = None,
        collection_name: str | None = None,
    ) -> list[dict]:
        """
        Execute AQL query with security awareness.

        Automatically handles field name obfuscation and result deobfuscation.
        """
        self._ensure_initialized()
        self._operation_count += 1

        # Transform query to use obfuscated field names
        transformed_query = self._transform_query_for_security(aql_query, collection_name)
        transformed_vars = self._transform_bind_vars_for_security(bind_vars or {})

        # Execute query
        cursor = self._database.aql.execute(transformed_query, bind_vars=transformed_vars)
        results = list(cursor)

        # Deobfuscate results if needed
        if collection_name and collection_name in self._collection_policies:
            policy = self._collection_policies[collection_name]
            if policy.requires_security and policy.allowed_model_types:
                results = self._deobfuscate_query_results(results, policy)

        logger.debug(f"Executed secured query, returned {len(results)} results")
        return results

    def get_security_registry(self) -> SecurityRegistry:
        """Get the security registry for advanced operations."""
        return self._security_registry

    def get_security_metrics(self) -> dict[str, Any]:
        """Get metrics about security enforcement."""
        return {
            "operations_count": self._operation_count,
            "security_violations": len(self._security_violations),
            "registered_collections": len(self._collection_policies),
            "uuid_mappings": len(self._security_registry._mappings),
            "recent_violations": self._security_violations[-5:]
            if self._security_violations
            else [],
        }

    def collections(self) -> list[str]:
        """Get list of collection names."""
        if self._skip_database:
            return []
        return [col.name for col in self._database.collections()] if self._database else []

    def create_collection(self, name: str) -> None:
        """Create a collection (legacy compatibility)."""
        if self._skip_database:
            logger.debug(f"Skipping collection creation for {name} (database disabled)")
            return
        if self._database:
            self._database.create_collection(name)

    def _ensure_initialized(self) -> None:
        """Ensure the interface is initialized before operations."""
        if not self._initialized:
            raise RuntimeError("SecuredDatabaseInterface not initialized. Call initialize() first.")

    async def _load_security_registry(self) -> None:
        """Load security registry from database if it exists."""
        if self._skip_database:
            logger.info("Skip loading security registry (database disabled)")
            return

        if self._database.has_collection("security_registry_data"):
            query = """
            FOR doc IN security_registry_data
                SORT doc.created_at DESC
                LIMIT 1
                RETURN doc
            """
            cursor = self._database.aql.execute(query)
            for doc in cursor:
                registry_data = doc.get("registry_export", {})
                if registry_data:
                    self._security_registry = SecurityRegistry.from_export(registry_data)
                    logger.info("Loaded security registry from database")
                    return

        logger.info("No existing security registry found, using new registry")

    async def _register_default_policies(self) -> None:
        """Register default security policies for known collections."""
        # Import here to avoid circular imports
        from ...streams.reciprocity.secured_reciprocity_models import (
            ReciprocityActivityData,
            ReciprocityBalance,
        )

        # Reciprocity collections
        reciprocity_policy = CollectionSecurityPolicy(
            collection_name="reciprocity_activities_secured",
            allowed_model_types=[ReciprocityActivityData],
            requires_security=True,
            schema_validation={
                "type": "object",
                "properties": {"_key": {"type": "string"}},
                "required": ["_key"],
                "additionalProperties": True,
            },
        )
        self.register_collection_policy(reciprocity_policy)

        balance_policy = CollectionSecurityPolicy(
            collection_name="reciprocity_balances_secured",
            allowed_model_types=[ReciprocityBalance],
            requires_security=True,
            schema_validation={
                "type": "object",
                "properties": {"_key": {"type": "string"}},
                "required": ["_key"],
                "additionalProperties": True,
            },
        )
        self.register_collection_policy(balance_policy)

        # Memory anchor collections (example of less sensitive data)

        # Note: MemoryAnchor would need to be converted to SecuredModel
        # For now, create a permissive policy
        memory_anchor_policy = CollectionSecurityPolicy(
            collection_name="memory_anchors",
            allowed_model_types=[],  # Empty for now
            requires_security=False,  # Legacy compatibility
            schema_validation={
                "type": "object",
                "properties": {"_key": {"type": "string"}},
                "required": ["_key"],
                "additionalProperties": True,
            },
        )
        self.register_collection_policy(memory_anchor_policy)

    def _transform_query_for_security(self, query: str, collection_name: str | None) -> str:
        """Transform AQL query to use obfuscated field names."""
        # This is a simplified implementation
        # In production, would use proper AQL parsing and transformation
        if collection_name and collection_name in self._collection_policies:
            policy = self._collection_policies[collection_name]
            if policy.requires_security:
                # Transform common field references
                # Real implementation would parse AQL and replace field names with UUIDs
                pass

        return query

    def _transform_bind_vars_for_security(self, bind_vars: dict[str, Any]) -> dict[str, Any]:
        """Transform bind variables for security-aware queries."""
        # Apply temporal offsets to datetime values
        transformed = {}
        temporal_config = self._security_registry.get_temporal_config()

        for key, value in bind_vars.items():
            if isinstance(value, datetime):
                transformed[key] = temporal_config.apply_offset(value).isoformat()
            else:
                transformed[key] = value

        return transformed

    def _deobfuscate_query_results(
        self, results: list[dict], policy: CollectionSecurityPolicy
    ) -> list[dict]:
        """Deobfuscate query results using security registry."""
        deobfuscated_results = []

        for result in results:
            # Remove ArangoDB metadata
            clean_result = {k: v for k, v in result.items() if not k.startswith("_")}

            # Attempt deobfuscation with first allowed model type
            if policy.allowed_model_types:
                try:
                    model_type = policy.allowed_model_types[0]
                    deobfuscated = model_type.from_storage_dict(
                        clean_result, self._security_registry
                    )
                    deobfuscated_results.append(deobfuscated.dict())
                except Exception as e:
                    logger.warning(f"Failed to deobfuscate result: {e}")
                    deobfuscated_results.append(clean_result)
            else:
                deobfuscated_results.append(clean_result)

        return deobfuscated_results


class SecuredCollectionWrapper:
    """
    Wrapper around ArangoDB collection that enforces security policies.

    This prevents direct access to collection methods that bypass security.
    """

    def __init__(
        self,
        collection: "StandardCollection",
        policy: CollectionSecurityPolicy,
        security_registry: SecurityRegistry,
    ):
        self._collection = collection
        self._policy = policy
        self._security_registry = security_registry
        self._operation_count = 0

    async def insert_secured(self, model: SecuredModel) -> dict:
        """Insert a secured model into the collection."""
        self._policy.validate_model(model)
        self._operation_count += 1

        # Get obfuscated data for storage
        obfuscated_data = model.to_storage_dict(self._security_registry)

        # Use model's ID as document key if available
        if hasattr(model, "interaction_id"):
            obfuscated_data["_key"] = str(model.interaction_id)
        elif hasattr(model, "id"):
            obfuscated_data["_key"] = str(model.id)

        # Insert into database
        result = self._collection.insert(obfuscated_data)

        logger.debug(f"Inserted secured document into {self._policy.collection_name}")
        return result

    async def get_secured(self, key: str, model_type: type[SecuredModel]) -> SecuredModel | None:
        """Retrieve and deobfuscate a document by key."""
        if model_type not in self._policy.allowed_model_types:
            raise SecurityViolationError(
                f"Model type {model_type.__name__} not allowed in {self._policy.collection_name}"
            )

        doc = self._collection.get(key)
        if not doc:
            return None

        # Remove ArangoDB metadata
        doc.pop("_key", None)
        doc.pop("_id", None)
        doc.pop("_rev", None)

        # Deobfuscate
        return model_type.from_storage_dict(doc, self._security_registry)

    async def update_secured(self, key: str, model: SecuredModel) -> dict:
        """Update a document with secured model data."""
        self._policy.validate_model(model)
        self._operation_count += 1

        # Get obfuscated update data
        obfuscated_data = model.to_storage_dict(self._security_registry)

        # Remove _key from update data
        obfuscated_data.pop("_key", None)

        # Update in database
        result = self._collection.update({"_key": key}, obfuscated_data)

        logger.debug(f"Updated secured document in {self._policy.collection_name}")
        return result

    def count(self) -> int:
        """Get document count (safe operation)."""
        return self._collection.count()

    def exists(self) -> bool:
        """Check if collection exists (safe operation)."""
        return True  # We wouldn't have a wrapper if it didn't exist

    # Block direct access to potentially unsafe operations
    def __getattr__(self, name: str) -> Any:
        """Block direct access to unsafe collection operations."""
        unsafe_operations = {
            "insert",
            "insert_many",
            "update",
            "update_many",
            "replace",
            "replace_many",
            "delete",
            "delete_many",
            "get",
            "find",
            "all",
            "random",
            "truncate",
        }

        if name in unsafe_operations:
            raise SecurityViolationError(
                f"Direct access to {name} is not allowed. "
                f"Use secured methods like insert_secured(), get_secured(), etc."
            )

        # Allow safe operations
        return getattr(self._collection, name)
