# CorrelationEngine and SecuredDatabaseInterface Tests

This directory contains tests that demonstrate the architectural boundaries between the CorrelationEngine and the SecuredDatabaseInterface, a critical security layer in the Mallku architecture.

## Test Files

### 1. `test_correlation_engine_secured_db.py`
Full integration test requiring a real database connection. Tests the complete flow from correlation detection to memory anchor storage through the secured database interface.

**Key Points Tested:**
- CorrelationEngine uses `get_secured_database()` - the only authorized database access path
- Memory anchors are created through the secured interface
- Query service respects secured database boundaries
- Security metrics are properly tracked

### 2. `test_correlation_engine_secured_db_mock.py`
Mock-based version of the integration test that doesn't require database credentials. Uses extensive mocking to test the same architectural boundaries.

**Key Points Tested:**
- Same architectural boundaries as above but with mocks
- Pattern detection with sufficient event occurrences
- Proper use of SecuredCollectionWrapper for memory_anchors

### 3. `test_correlation_engine_architectural_boundaries.py`
Focused architectural test that documents and verifies the design decisions without requiring full component initialization.

**Key Points Tested:**
- Memory anchors collection security policy design
- Component initialization patterns
- Data structure compatibility
- Architectural flow documentation

## Architectural Design

### Security Model

The SecuredDatabaseInterface enforces security by design:

1. **Single Entry Point**: `get_secured_database()` is the ONLY authorized way to access the database
2. **Collection Policies**: Every collection must have a registered security policy
3. **Secured Models**: Most collections require data to be wrapped in SecuredModel instances
4. **Audit Trail**: All operations are tracked for security monitoring

### Memory Anchors Exception

The `memory_anchors` collection has a special security policy:

```python
CollectionSecurityPolicy(
    collection_name="memory_anchors",
    allowed_model_types=[],  # Empty for legacy compatibility
    requires_security=False,  # Legacy compatibility
    schema_validation={...}
)
```

This is intentional - memory_anchors predates the security layer and uses the legacy `MemoryAnchor` class rather than a `SecuredModel`. However, it still goes through the secured interface for access control and monitoring.

### Architectural Flow

```
CorrelationEngine.process_event_stream()
    ↓ (detects patterns)
CorrelationEngine._create_memory_anchor()
    ↓ (calls get_secured_database())
SecuredDatabaseInterface.get_secured_collection("memory_anchors")
    ↓ (returns wrapper with legacy policy)
collection.insert(anchor_document)
    ↓ (direct insertion allowed due to requires_security=False)
Database Storage
```

### Query Path

```
MemoryAnchorQueryService.execute_query()
    ↓ (uses get_secured_database())
SecuredDatabaseInterface.execute_secured_query()
    ↓ (enforces collection boundaries)
Results with proper access control
```

## Running the Tests

```bash
# Run all correlation engine tests
pytest tests/test_correlation_engine*.py -v

# Run architectural boundaries test (no DB required)
pytest tests/test_correlation_engine_architectural_boundaries.py -v

# Run with mock database (no credentials required)
pytest tests/test_correlation_engine_secured_db_mock.py -v

# Run full integration test (requires database)
pytest tests/test_correlation_engine_secured_db.py -v
```

## Key Insights

1. **Legacy Compatibility**: The memory_anchors collection demonstrates how to maintain backward compatibility while still enforcing architectural boundaries.

2. **Security Layers**: Even collections with `requires_security=False` must go through the SecuredDatabaseInterface, ensuring monitoring and access control.

3. **Pattern Detection**: The CorrelationEngine requires minimum occurrences (default 3) to detect patterns, preventing false correlations.

4. **Architectural Enforcement**: Components cannot bypass the security model - all database access is channeled through the secured interface.

## Future Considerations

- When migrating memory_anchors to use SecuredModel, update the collection policy
- Consider adding more granular security policies for different correlation types
- Enhance security metrics to track correlation-specific operations