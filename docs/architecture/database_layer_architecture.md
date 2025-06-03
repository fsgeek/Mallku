# Mallku Database Layer Architecture

## Overview

This document defines the architectural design for Mallku's database layer, implementing containerized security boundaries and semantic registration to ensure data integrity, privacy, and meaningful structure.

## Core Principles

1. **Security by Architecture**: Components cannot bypass security because they cannot access the raw database
2. **Semantic Preservation**: UUID obfuscation maintains meaning through explicit semantic mappings
3. **Schema Enforcement**: All collections require schemas with semantic definitions
4. **Balanced Design**: Security measures enhance rather than compromise system utility

## Architectural Components

### 1. Containerized Database Layer

```yaml
# Container Architecture
mallku-database-container:
  internal:
    - ArangoDB instance
    - Mallku Database Layer service
    - Schema Registry
    - Security Transformer
    - Semantic Mapper

  exposed:
    - Mallku Database API (REST/gRPC)
    - Health endpoints
    - Metrics endpoints

  never-exposed:
    - Direct ArangoDB ports
    - Raw data access
    - Internal configuration
```

### 2. Mallku Database Interface

```python
class MallkuDatabaseLayer:
    """
    The ONLY interface to persistent storage.
    Enforces schemas, security, and semantic mappings.
    """

    def __init__(self):
        self._db = ArangoDB()  # Private, never exposed
        self._registry = CollectionRegistry()
        self._schemas = SchemaRegistry()
        self._security = SecurityTransformer()
        self._semantics = SemanticMapper()

    async def register_collection(
        self,
        semantic_name: str,
        description: str,
        schema: CollectionSchema,
        semantic_definitions: Dict[str, str]
    ) -> CollectionRegistration:
        """
        Register a new collection with full semantic context.
        Creates UUID mapping and configures indices.
        """
        # Validate semantic coherence
        await self._validate_semantic_coherence(
            description, schema, semantic_definitions
        )

        # Generate UUID for collection
        collection_uuid = self._security.generate_collection_uuid()

        # Store semantic mappings
        self._semantics.register_collection(
            semantic_name, collection_uuid, description
        )

        # Create schema with semantic field definitions
        self._schemas.register(collection_uuid, schema, semantic_definitions)

        # Create indices for marked fields
        await self._create_indices(collection_uuid, schema)

        # Initialize collection in ArangoDB
        await self._db.create_collection(collection_uuid)

        return CollectionRegistration(
            semantic_name=semantic_name,
            uuid=collection_uuid,
            created_at=datetime.utcnow()
        )

    async def store(
        self,
        collection_name: str,
        data: Dict[str, Any]
    ) -> StorageResult:
        """
        Store data with schema validation and security transformation.
        """
        # Resolve collection UUID
        collection_uuid = self._semantics.get_collection_uuid(collection_name)

        # Validate against schema
        schema = self._schemas.get_schema(collection_uuid)
        validation_result = schema.validate(data)
        if not validation_result.valid:
            raise SchemaValidationError(validation_result.errors)

        # Apply security transformations
        secured_data = self._security.transform(
            collection_uuid,
            data,
            schema.security_config
        )

        # Store in ArangoDB
        doc = await self._db.insert(collection_uuid, secured_data)

        # Return obfuscated reference
        return StorageResult(
            id=self._security.obfuscate_id(doc._id),
            collection=collection_name,
            stored_at=datetime.utcnow()
        )
```

### 3. Semantic Registration Model

```python
@dataclass
class CollectionSchema:
    """Schema definition with semantic context."""

    fields: Dict[str, FieldDefinition]
    required_fields: List[str]
    indices: List[IndexDefinition]
    security_config: SecurityConfiguration

@dataclass
class FieldDefinition:
    """Field definition with semantic meaning."""

    type: FieldType
    semantic_description: str
    indexed: bool = False
    encrypted: bool = False
    temporal_offset: bool = False
    privacy_level: PrivacyLevel = PrivacyLevel.PRIVATE

@dataclass
class SemanticValidation:
    """Ensures semantic descriptions align with schemas."""

    async def validate_coherence(
        self,
        collection_description: str,
        schema: CollectionSchema,
        field_definitions: Dict[str, str]
    ) -> ValidationResult:
        """
        Use prompt-manager style validation to ensure
        semantic descriptions match actual schema structure.
        """
        # Validate collection description matches field purposes
        # Ensure field types align with semantic descriptions
        # Check for cognitive dissonance between layers
        pass
```

### 4. Index Management

```python
class IndexManager:
    """Manages indices based on schema definitions."""

    async def create_indices(
        self,
        collection_uuid: str,
        schema: CollectionSchema
    ):
        """Create indices for all marked fields."""

        for field_name, field_def in schema.fields.items():
            if field_def.indexed:
                # Map semantic field name to UUID
                field_uuid = self._security.get_field_uuid(
                    collection_uuid, field_name
                )

                # Create appropriate index type
                if field_def.type in [FieldType.TEXT, FieldType.STRING]:
                    await self._create_inverted_index(
                        collection_uuid, field_uuid
                    )
                else:
                    await self._create_standard_index(
                        collection_uuid, field_uuid
                    )
```

### 5. Container Deployment

```dockerfile
# Dockerfile for Mallku Database Layer
FROM arangodb:3.11

# Install Mallku database layer
COPY mallku-db-layer /opt/mallku/

# Configure ArangoDB for internal use only
COPY arangodb.conf /etc/arangodb3/

# Expose only Mallku API port
EXPOSE 8529

# Start both ArangoDB and Mallku layer
CMD ["/opt/mallku/start.sh"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  mallku-database:
    build: ./database-layer
    ports:
      - "7474:7474"  # Mallku API only
    environment:
      - MALLKU_SECURITY_LEVEL=production
      - ARANGODB_ROOT_PASSWORD_FILE=/run/secrets/db_password
    volumes:
      - mallku-data:/var/lib/arangodb3
      - ./schemas:/opt/mallku/schemas
    secrets:
      - db_password
```

## Security Benefits

1. **Physical Isolation**: Database never directly accessible
2. **Enforced Schemas**: No arbitrary data insertion
3. **Semantic Preservation**: Meaning maintained despite UUIDs
4. **Audit Trail**: All access logged at API layer
5. **Evolution Path**: Security can be enhanced without breaking contracts

## Implementation Considerations

### Migration Strategy

1. **Phase 1**: Implement database layer with current direct access
2. **Phase 2**: Migrate components to use new API
3. **Phase 3**: Containerize and remove direct access
4. **Phase 4**: Implement full semantic registration

### Performance Impact

- Single API layer adds ~1-2ms latency
- Schema validation adds ~0.5ms per operation
- Security transformations depend on encryption choices
- Index creation is one-time cost at registration

### Development Workflow

1. Define collection semantics
2. Create schema with field definitions
3. Register collection through API
4. Use semantic names in application code
5. Database layer handles all transformations

## Alignment with Cathedral Principles

This architecture embodies:
- **Intentional Design**: Every piece serves security and meaning
- **Balanced Approach**: Security enhances rather than restricts
- **Semantic Integrity**: Meaning preserved through all transformations
- **Evolutionary Path**: Can strengthen over time without breaking

---

*This database layer forms the bedrock of Mallku's cathedral - secure, meaningful, and designed for permanence.*
