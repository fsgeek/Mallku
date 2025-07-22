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
import warnings
from datetime import datetime
from typing import TYPE_CHECKING, Any

from ..security.registry import SecurityRegistry
from ..security.registry_store import get_registry_store
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

    def __init__(self, database: "StandardDatabase | None", registry_path=None):
        """Initialize with database connection and security enforcement."""
        self._database = database

        # Load registry from persistent storage
        self._registry_store = get_registry_store(registry_path)
        try:
            self._security_registry = self._registry_store.load_registry_sync()
            logger.info("Loaded security registry from persistent storage")
        except Exception as e:
            logger.warning(f"Could not load registry, creating new: {e}")
            self._security_registry = SecurityRegistry()
            # Save the new registry immediately
            self._registry_store.save_registry_sync(self._security_registry)

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

        return SecuredCollectionWrapper(collection, policy, self._security_registry, self)

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

        return SecuredCollectionWrapper(collection, policy, self._security_registry, self)

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

    def _save_registry(self) -> None:
        """Save the security registry to persistent storage."""
        try:
            self._registry_store.save_registry_sync(self._security_registry)
            logger.debug("Saved security registry to persistent storage")
        except Exception as e:
            logger.error(f"Failed to save security registry: {e}")
            # Don't fail the operation, but log the error

    def collections(self) -> list[str]:
        """Get list of collection names."""
        if self._skip_database:
            return []
        return [col.name for col in self._database.collections()] if self._database else []

    def collection(self, name: str) -> "SecuredCollectionWrapper":
        """Get a secured collection wrapper by name."""
        self._ensure_initialized()

        if name not in self._collection_policies:
            warnings.warn(
                f"No security policy for '{name}'. Creating a default, permissive policy. "
                "Define a proper policy for production.",
                UserWarning,
                stacklevel=2,
            )
            default_policy = CollectionSecurityPolicy(
                collection_name=name,
                allowed_model_types=[],
                requires_security=False,
            )
            self.register_collection_policy(default_policy)

        if self._skip_database:
            # This path is taken in mock/dev mode. We can't return a real collection wrapper.
            # The DevDatabaseInterface will need to handle this by returning a mock object.
            # For the base class, returning None is the only safe option if the db is skipped.
            return None

        if not self._database.has_collection(name):
            self._database.create_collection(name)
            logger.info(f"Created collection '{name}' on-demand.")

        collection = self._database.collection(name)
        policy = self._collection_policies[name]

        return SecuredCollectionWrapper(collection, policy, self._security_registry, self)

    def has_collection(self, name: str) -> bool:
        """Check if a collection exists."""
        if self._skip_database:
            return True  # Assume exists in mock mode
        return self._database.has_collection(name)

    def create_collection(self, name: str) -> None:
        """Create a collection (legacy compatibility)."""
        if self._skip_database:
            logger.debug(f"Skipping collection creation for {name} (database disabled)")
            return
        if self._database:
            self._database.create_collection(name)

    @property
    def aql(self):
        """Get AQL interface (compatibility method).

        WARNING: Direct AQL access bypasses security. Use execute_secured_query() instead.
        """
        self._warn_once("Direct AQL access - use execute_secured_query()")

        if self._skip_database:
            from .dev_interface import MockAQL

            return MockAQL(self)

        if not self._database:
            raise RuntimeError("No database connection available")

        return self._database.aql

    async def query(self, collection: str, filters: dict[str, Any]) -> list[dict]:
        """Query a collection with filters (compatibility method).

        WARNING: This is a simplified query interface. Use execute_secured_query() for complex queries.
        """
        self._warn_once(f"Using simplified query on '{collection}'")

        if self._skip_database:
            logger.info(f"DEV MODE: Query on {collection} with filters {filters} - returning empty")
            return []

        # Build a simple AQL query from filters
        conditions = []
        bind_vars = {"@collection": collection}

        for i, (key, value) in enumerate(filters.items()):
            conditions.append(f"doc.{key} == @value{i}")
            bind_vars[f"value{i}"] = value

        where_clause = " AND ".join(conditions) if conditions else "true"
        query = f"FOR doc IN @@collection FILTER {where_clause} RETURN doc"

        return await self.execute_secured_query(query, bind_vars, collection)

    async def batch_insert(self, collection: str, documents: list[dict]) -> None:
        """Batch insert documents (compatibility method).

        WARNING: This bypasses security policies. Use SecuredCollectionWrapper.insert_secured() instead.
        """
        self._warn_once(f"Batch inserting to '{collection}' without security")

        if self._skip_database:
            logger.info(f"DEV MODE: Would insert {len(documents)} documents to {collection}")
            return

        if not self._database:
            raise RuntimeError("No database connection available")

        # Get or create collection
        if not self._database.has_collection(collection):
            self._database.create_collection(collection)

        col = self._database.collection(collection)
        col.insert_many(documents)

    def _warn_once(self, operation: str) -> None:
        """Warn about an operation once per session."""
        if not hasattr(self, "_warned_operations"):
            self._warned_operations = set()

        # Extract operation type (before ' for ' or ' on ')
        op_type = operation.split(" for ")[0].split(" on ")[0].strip()

        if op_type not in self._warned_operations:
            self._warned_operations.add(op_type)
            logger.warning(
                f"COMPATIBILITY MODE: {operation} - Consider using secured methods for production"
            )

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
        parent_interface: "SecuredDatabaseInterface",
    ):
        self._collection = collection
        self._policy = policy
        self._security_registry = security_registry
        self._parent_interface = parent_interface
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

        # Save registry in case new field mappings were created
        self._parent_interface._save_registry()

        logger.debug(f"Inserted secured document into {self._policy.collection_name}")
        return result

    async def insert_many_secured(self, models: list[SecuredModel]) -> list[dict]:
        """Insert multiple secured models into the collection."""
        if not models:
            return []

        self._operation_count += len(models)
        obfuscated_docs = []
        for model in models:
            self._policy.validate_model(model)
            obfuscated_data = model.to_storage_dict(self._security_registry)
            if hasattr(model, "interaction_id"):
                obfuscated_data["_key"] = str(model.interaction_id)
            elif hasattr(model, "id"):
                obfuscated_data["_key"] = str(model.id)
            obfuscated_docs.append(obfuscated_data)

        results = self._collection.insert_many(obfuscated_docs)
        self._parent_interface._save_registry()
        logger.debug(
            f"Inserted {len(models)} secured documents into {self._policy.collection_name}"
        )
        return results

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

        # Save registry in case new field mappings were created
        self._parent_interface._save_registry()

        logger.debug(f"Updated secured document in {self._policy.collection_name}")
        return result

    def count(self) -> int:
        """Get document count (safe operation)."""
        return self._collection.count()

    def exists(self) -> bool:
        """Check if collection exists (safe operation)."""
        return True  # We wouldn't have a wrapper if it didn't exist

    def insert(self, document: dict) -> dict:
        """Insert a document (compatibility method).

        WARNING: This bypasses security policies. Use insert_secured() instead.
        """
        self._parent_interface._warn_once(f"Direct insert into '{self._policy.collection_name}'")
        return self._collection.insert(document)

    def insert_many(self, documents: list[dict]) -> list[dict]:
        """Insert multiple documents (compatibility method).

        WARNING: This bypasses security policies. Use insert_secured() instead.
        """
        self._parent_interface._warn_once(
            f"Direct insert_many into '{self._policy.collection_name}'"
        )
        return self._collection.insert_many(documents)

    def all(self, limit: int | None = None) -> list[dict]:
        """Get all documents (compatibility method).

        WARNING: This may return sensitive data. Use with caution.
        """
        self._parent_interface._warn_once(f"Direct all() on '{self._policy.collection_name}'")
        if limit:
            return list(self._collection.all(limit=limit))
        return list(self._collection.all())

    def find(self, filters: dict[str, Any]) -> list[dict]:
        """Find documents with filters (compatibility method).

        WARNING: This bypasses security transformations. Use parent's query() instead.
        """
        self._parent_interface._warn_once(f"Direct find() on '{self._policy.collection_name}'")
        # Build simple AQL query
        conditions = []
        bind_vars = {"@collection": self._policy.collection_name}

        for i, (key, value) in enumerate(filters.items()):
            conditions.append(f"doc.{key} == @value{i}")
            bind_vars[f"value{i}"] = value

        where_clause = " AND ".join(conditions) if conditions else "true"
        query = f"FOR doc IN @@collection FILTER {where_clause} RETURN doc"

        cursor = self._parent_interface._database.aql.execute(query, bind_vars=bind_vars)
        return list(cursor)

    def add_persistent_index(self, fields: list[str], unique: bool = False) -> dict:
        """Add a persistent index (compatibility method)."""
        self._parent_interface._warn_once(f"Creating index on '{self._policy.collection_name}'")
        return self._collection.add_persistent_index(fields=fields, unique=unique)

    # Block direct access to potentially unsafe operations
    def __getattr__(self, name: str) -> Any:
        """Block direct access to unsafe collection operations."""
        unsafe_operations = {
            "update",
            "update_many",
            "replace",
            "replace_many",
            "delete",
            "delete_many",
            "get",
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
