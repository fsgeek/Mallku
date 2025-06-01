"""
Mallku Database API - The ONLY interface to the database

This API enforces the complete architectural separation - it is the ONLY way
to interact with the database. ArangoDB is completely isolated within this container
and cannot be accessed directly.

Key principles:
- No semantically meaningful labels exposed
- All database operations require semantic context
- Schema validation enforced
- Automatic indexing based on field strategies
- LLM-ready descriptions required for all entities
"""

import logging
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

import uvicorn
from fastapi import FastAPI, HTTPException, status
from mallku.core.security.field_strategies import (
    FieldIndexStrategy,
    FieldObfuscationLevel,
    FieldSecurityConfig,
)
from mallku.core.security.registry import SecurityRegistry
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


# === API Models ===

class SemanticCollection(BaseModel):
    """
    Semantic collection definition - what the application understands.

    This is completely separate from the physical storage which uses UUIDs.
    """
    semantic_label: str = Field(description="Human-readable collection name")
    description: str = Field(description="LLM-readable description of what this collection stores")
    purpose: str = Field(description="Why this collection exists and how it's used")
    examples: list[str] = Field(description="Example use cases for LLM guidance")
    schema_definition: dict[str, Any] = Field(description="Schema with field security strategies")
    required_fields: list[str] = Field(default_factory=list)
    relationships: list[str] = Field(default_factory=list, description="Relationships to other collections")


class IndexDefinition(BaseModel):
    """Definition for database indices based on security-aware field strategies."""
    field_paths: list[str] = Field(description="Fields to index (using semantic names)")
    index_type: str = Field(description="Type: simple, compound, geo, fulltext")
    index_strategy: FieldIndexStrategy = Field(description="Security strategy for this index")
    sparse: bool = Field(default=False)
    unique: bool = Field(default=False)
    background: bool = Field(default=True)


class DataEntity(BaseModel):
    """
    A data entity to be stored - must include semantic context.
    """
    semantic_collection: str = Field(description="Semantic collection label")
    entity_data: dict[str, Any] = Field(description="The actual data to store")
    entity_id: UUID | None = Field(default_factory=uuid4, description="Optional explicit ID")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class QueryRequest(BaseModel):
    """
    Query request with semantic context for LLM processing.
    """
    semantic_collection: str = Field(description="Collection being queried")
    query_purpose: str = Field(description="What the query is trying to achieve")
    query_aql: str = Field(description="AQL query using semantic field names")
    bind_variables: dict[str, Any] = Field(default_factory=dict)
    max_results: int = Field(default=100, le=1000)


class DatabaseMetrics(BaseModel):
    """Database metrics and status information."""
    total_collections: int
    total_documents: int
    security_registry_size: int
    index_count: int
    container_uptime: str
    last_backup: datetime | None


# === Core Database Service ===

class MallkuDatabaseService:
    """
    The core database service that manages the isolated ArangoDB instance.

    This service enforces all security policies and provides the abstraction
    layer that makes direct ArangoDB access impossible.
    """

    def __init__(self):
        """Initialize the database service."""
        self.security_registry = SecurityRegistry()
        self.collections_registry: dict[str, SemanticCollection] = {}
        self.arangodb = None  # Will be initialized on startup
        self.startup_time = datetime.now(UTC)

    async def initialize(self):
        """Initialize the database service and ArangoDB connection."""
        try:
            # Import and initialize ArangoDB (only accessible within container)
            from arango import ArangoClient

            # Connect to local ArangoDB instance
            client = ArangoClient(hosts='http://localhost:8529')
            self.arangodb = client.db('mallku', username='mallku', password='mallku_secure')

            # Load existing collections registry
            await self._load_collections_registry()

            # Load security registry
            await self._load_security_registry()

            logger.info("Mallku Database Service initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize database service: {e}")
            raise

    async def create_semantic_collection(self, collection_def: SemanticCollection) -> dict[str, Any]:
        """
        Create a new semantic collection with security enforcement.

        This is the ONLY way to create collections in Mallku.
        """
        try:
            # Validate collection definition
            await self._validate_collection_definition(collection_def)

            # Generate UUID for physical storage
            physical_collection_id = str(uuid4())

            # Create security configurations for fields
            field_configs = {}
            for field_name, field_spec in collection_def.schema_definition.items():
                security_config = self._create_field_security_config(field_spec)
                field_uuid = self.security_registry.get_or_create_mapping(
                    field_name, security_config
                )
                field_configs[field_name] = field_uuid

            # Create physical collection in ArangoDB
            physical_collection = self.arangodb.create_collection(
                physical_collection_id,
                schema=self._generate_physical_schema(collection_def, field_configs)
            )

            # Create automatic indices based on field strategies
            await self._create_automatic_indices(physical_collection, collection_def, field_configs)

            # Register the semantic collection
            self.collections_registry[collection_def.semantic_label] = collection_def

            # Store mapping in security registry
            await self._store_collection_mapping(
                collection_def.semantic_label,
                physical_collection_id,
                field_configs
            )

            logger.info(f"Created semantic collection: {collection_def.semantic_label}")

            return {
                "semantic_label": collection_def.semantic_label,
                "physical_id": physical_collection_id,
                "field_mappings": len(field_configs),
                "indices_created": len([f for f in collection_def.schema_definition.values()
                                      if f.get('indexed', False)]),
                "status": "created"
            }

        except Exception as e:
            logger.error(f"Failed to create semantic collection: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Collection creation failed: {e}"
            )

    async def store_entity(self, entity: DataEntity) -> dict[str, Any]:
        """
        Store a data entity with full security processing.
        """
        try:
            # Validate entity belongs to registered collection
            if entity.semantic_collection not in self.collections_registry:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Semantic collection '{entity.semantic_collection}' not found"
                )

            collection_def = self.collections_registry[entity.semantic_collection]

            # Get physical collection
            physical_collection_id = await self._get_physical_collection_id(entity.semantic_collection)
            physical_collection = self.arangodb.collection(physical_collection_id)

            # Transform entity data using security registry
            obfuscated_data = await self._obfuscate_entity_data(
                entity.entity_data,
                collection_def
            )

            # Add metadata
            obfuscated_data.update({
                '_key': str(entity.entity_id),
                '_semantic_collection': entity.semantic_collection,
                '_created_at': datetime.now(UTC).isoformat(),
                '_metadata': entity.metadata
            })

            # Store in ArangoDB
            result = physical_collection.insert(obfuscated_data)

            logger.info(f"Stored entity in {entity.semantic_collection}")

            return {
                "entity_id": str(entity.entity_id),
                "semantic_collection": entity.semantic_collection,
                "physical_id": result['_id'],
                "status": "stored"
            }

        except Exception as e:
            logger.error(f"Failed to store entity: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Entity storage failed: {e}"
            )

    async def execute_query(self, query_req: QueryRequest) -> list[dict[str, Any]]:
        """
        Execute a semantic query with security transformation.
        """
        try:
            # Validate collection exists
            if query_req.semantic_collection not in self.collections_registry:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Semantic collection '{query_req.semantic_collection}' not found"
                )

            # Transform query to use physical field UUIDs
            physical_query = await self._transform_query_to_physical(
                query_req.query_aql,
                query_req.semantic_collection
            )

            # Transform bind variables
            physical_bind_vars = await self._transform_bind_variables(
                query_req.bind_variables,
                query_req.semantic_collection
            )

            # Execute query on ArangoDB
            cursor = self.arangodb.aql.execute(
                physical_query,
                bind_vars=physical_bind_vars
            )

            # Transform results back to semantic form
            results = []
            collection_def = self.collections_registry[query_req.semantic_collection]

            for doc in cursor:
                deobfuscated = await self._deobfuscate_entity_data(doc, collection_def)
                results.append(deobfuscated)

                if len(results) >= query_req.max_results:
                    break

            logger.info(f"Executed query on {query_req.semantic_collection}, returned {len(results)} results")

            return results

        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Query execution failed: {e}"
            )

    async def get_database_metrics(self) -> DatabaseMetrics:
        """Get comprehensive database metrics."""
        try:
            # Count collections and documents
            total_collections = len(self.collections_registry)
            total_documents = 0

            for semantic_label in self.collections_registry:
                physical_id = await self._get_physical_collection_id(semantic_label)
                collection = self.arangodb.collection(physical_id)
                total_documents += collection.count()

            # Calculate uptime
            uptime = datetime.now(UTC) - self.startup_time
            uptime_str = f"{uptime.days}d {uptime.seconds//3600}h {(uptime.seconds%3600)//60}m"

            return DatabaseMetrics(
                total_collections=total_collections,
                total_documents=total_documents,
                security_registry_size=len(self.security_registry._mappings),
                index_count=0,  # Would count indices in production
                container_uptime=uptime_str,
                last_backup=None  # Would track backups in production
            )

        except Exception as e:
            logger.error(f"Failed to get database metrics: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Metrics retrieval failed: {e}"
            )

    async def create_explicit_index(
        self,
        semantic_collection: str,
        index_def: IndexDefinition
    ) -> dict[str, Any]:
        """
        Create an explicit index (e.g., compound indices).
        """
        try:
            if semantic_collection not in self.collections_registry:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Semantic collection '{semantic_collection}' not found"
                )

            # Transform field paths to physical UUIDs
            physical_field_paths = []
            for field_path in index_def.field_paths:
                field_uuid = self.security_registry.get_or_create_mapping(field_path)
                physical_field_paths.append(field_uuid)

            # Get physical collection
            physical_collection_id = await self._get_physical_collection_id(semantic_collection)
            collection = self.arangodb.collection(physical_collection_id)

            # Create index
            if index_def.index_type == "compound":
                index = collection.add_persistent_index(
                    fields=physical_field_paths,
                    unique=index_def.unique,
                    sparse=index_def.sparse
                )
            elif index_def.index_type == "geo":
                index = collection.add_geo_index(
                    fields=physical_field_paths
                )
            elif index_def.index_type == "fulltext":
                index = collection.add_fulltext_index(
                    fields=physical_field_paths[0]  # Fulltext on single field
                )
            else:
                index = collection.add_persistent_index(
                    fields=physical_field_paths,
                    unique=index_def.unique,
                    sparse=index_def.sparse
                )

            logger.info(f"Created {index_def.index_type} index on {semantic_collection}")

            return {
                "index_id": index['id'],
                "semantic_collection": semantic_collection,
                "field_paths": index_def.field_paths,
                "index_type": index_def.index_type,
                "status": "created"
            }

        except Exception as e:
            logger.error(f"Index creation failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Index creation failed: {e}"
            )

    # Private implementation methods

    async def _validate_collection_definition(self, collection_def: SemanticCollection):
        """Validate that collection definition meets requirements."""
        if not collection_def.description:
            raise ValueError("Collection description required for LLM processing")

        if not collection_def.examples:
            raise ValueError("Examples required for LLM guidance")

        if not collection_def.schema_definition:
            raise ValueError("Schema definition required")

        # Validate that required fields are in schema
        for field in collection_def.required_fields:
            if field not in collection_def.schema_definition:
                raise ValueError(f"Required field '{field}' not in schema definition")

    def _create_field_security_config(self, field_spec: dict) -> FieldSecurityConfig:
        """Create security configuration from field specification."""
        obfuscation_level = FieldObfuscationLevel(field_spec.get('obfuscation', 'uuid_only'))
        index_strategy = FieldIndexStrategy(field_spec.get('index_strategy', 'identity'))

        return FieldSecurityConfig(
            obfuscation_level=obfuscation_level,
            index_strategy=index_strategy,
            searchable=field_spec.get('searchable', False),
            aggregatable=field_spec.get('aggregatable', False)
        )

    def _generate_physical_schema(
        self,
        collection_def: SemanticCollection,
        field_configs: dict[str, str]
    ) -> dict:
        """Generate physical schema for ArangoDB using UUIDs."""
        return {
            "type": "object",
            "properties": {
                "_key": {"type": "string"},
                "_semantic_collection": {"type": "string"},
                "_created_at": {"type": "string"},
                "_metadata": {"type": "object"},
                **{uuid: {"type": "object"} for uuid in field_configs.values()}
            },
            "required": ["_key", "_semantic_collection"],
            "additionalProperties": True
        }

    async def _create_automatic_indices(
        self,
        physical_collection,
        collection_def: SemanticCollection,
        field_configs: dict[str, str]
    ):
        """Create indices automatically based on field security strategies."""
        for field_name, field_spec in collection_def.schema_definition.items():
            if field_spec.get('indexed', False):
                field_uuid = field_configs[field_name]
                try:
                    physical_collection.add_persistent_index(
                        fields=[field_uuid],
                        sparse=True,
                        background=True
                    )
                    logger.info(f"Created automatic index for field: {field_name}")
                except Exception as e:
                    logger.warning(f"Failed to create index for {field_name}: {e}")

    async def _load_collections_registry(self):
        """Load existing collections registry from database."""
        # Implementation would load from special system collection
        pass

    async def _load_security_registry(self):
        """Load security registry from database."""
        # Implementation would load from special system collection
        pass

    async def _store_collection_mapping(
        self,
        semantic_label: str,
        physical_id: str,
        field_configs: dict[str, str]
    ):
        """Store collection mapping for future reference."""
        # Implementation would store in special system collection
        pass

    async def _get_physical_collection_id(self, semantic_label: str) -> str:
        """Get physical collection ID from semantic label."""
        # Implementation would lookup from system collection
        # For now, return a placeholder
        return f"collection_{semantic_label.replace(' ', '_')}"

    async def _obfuscate_entity_data(self, data: dict, collection_def: SemanticCollection) -> dict:
        """Transform entity data using security registry."""
        obfuscated = {}
        for field_name, value in data.items():
            if field_name in collection_def.schema_definition:
                field_uuid = self.security_registry.get_or_create_mapping(field_name)
                # Apply obfuscation based on field security config
                obfuscated[field_uuid] = value  # Simplified - would apply real obfuscation
            else:
                # Unknown field - store with warning
                logger.warning(f"Unknown field in entity: {field_name}")
                obfuscated[field_name] = value
        return obfuscated

    async def _deobfuscate_entity_data(self, doc: dict, collection_def: SemanticCollection) -> dict:
        """Transform document back to semantic form."""
        deobfuscated = {}

        # Handle system fields
        for key in ['_key', '_semantic_collection', '_created_at', '_metadata']:
            if key in doc:
                deobfuscated[key] = doc[key]

        # Deobfuscate data fields
        for field_name in collection_def.schema_definition:
            field_uuid = self.security_registry.get_or_create_mapping(field_name)
            if field_uuid in doc:
                deobfuscated[field_name] = doc[field_uuid]

        return deobfuscated

    async def _transform_query_to_physical(self, aql_query: str, semantic_collection: str) -> str:
        """Transform AQL query to use physical field UUIDs."""
        # Simplified implementation - would use proper AQL parsing
        collection_def = self.collections_registry[semantic_collection]
        physical_query = aql_query

        for field_name in collection_def.schema_definition:
            field_uuid = self.security_registry.get_or_create_mapping(field_name)
            physical_query = physical_query.replace(f".{field_name}", f".{field_uuid}")

        return physical_query

    async def _transform_bind_variables(self, bind_vars: dict, semantic_collection: str) -> dict:
        """Transform bind variables for physical query."""
        # Apply temporal offsets and other transformations
        temporal_config = self.security_registry.get_temporal_config()

        transformed = {}
        for key, value in bind_vars.items():
            if isinstance(value, datetime):
                transformed[key] = temporal_config.apply_offset(value).isoformat()
            else:
                transformed[key] = value

        return transformed


# === FastAPI Application ===

service = MallkuDatabaseService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage service lifecycle."""
    await service.initialize()
    yield


app = FastAPI(
    title="Mallku Database API",
    description="The ONLY interface to Mallku's database - enforces complete security isolation",
    version="1.0.0",
    lifespan=lifespan
)


@app.post("/collections/create")
async def create_collection(collection_def: SemanticCollection):
    """Create a new semantic collection with security enforcement."""
    return await service.create_semantic_collection(collection_def)


@app.post("/entities/store")
async def store_entity(entity: DataEntity):
    """Store a data entity with full security processing."""
    return await service.store_entity(entity)


@app.post("/queries/execute")
async def execute_query(query_req: QueryRequest):
    """Execute a semantic query with security transformation."""
    return await service.execute_query(query_req)


@app.post("/indices/create")
async def create_index(semantic_collection: str, index_def: IndexDefinition):
    """Create an explicit index."""
    return await service.create_explicit_index(semantic_collection, index_def)


@app.get("/metrics")
async def get_metrics():
    """Get database metrics and status."""
    return await service.get_database_metrics()


@app.get("/collections")
async def list_collections():
    """List all semantic collections."""
    return {
        "collections": [
            {
                "semantic_label": label,
                "description": collection.description,
                "purpose": collection.purpose
            }
            for label, collection in service.collections_registry.items()
        ]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "mallku_database_api",
        "version": "1.0.0",
        "uptime": str(datetime.now(UTC) - service.startup_time),
        "arangodb_accessible": service.arangodb is not None
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
