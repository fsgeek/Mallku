# Database Security Migration Guide

*Created by the Seventh Anthropologist*
*Date: 2025-07-16*

## Quick Migration

### 1. Update Imports

```python
# ❌ OLD
from mallku.core.database.deprecated import get_database_deprecated, MallkuDBConfig

# ✅ NEW
from mallku.core.database import get_database
```

### 2. Update Function Calls

```python
# ❌ OLD
db = get_database_deprecated()

# ✅ NEW
db = await get_database()
```

### 3. Make Functions Async

```python
# ❌ OLD
def get_consciousness_data():
    db = get_database_deprecated()
    return db.collection("consciousness").all()

# ✅ NEW
async def get_consciousness_data():
    db = await get_database()
    return await db.collection("consciousness").all()
```

## Complex Patterns

### Direct AQL Queries

```python
# ❌ OLD - Direct AQL
db = get_database_deprecated()
cursor = db.aql.execute(
    "FOR doc IN @@collection FILTER doc.active == true RETURN doc",
    bind_vars={"@collection": "consciousness"}
)

# ✅ NEW - Use query interface
db = await get_database()
results = await db.query(
    collection="consciousness",
    filters={"active": True}
)
```

### Batch Operations

```python
# ❌ OLD - Direct batch insert
db = get_database_deprecated()
collection = db.collection("metrics")
collection.insert_many(documents)

# ✅ NEW - Use batch interface
db = await get_database()
await db.batch_insert("metrics", documents)
```

## Why This Migration Matters

1. **Security**: All operations go through authentication/authorization
2. **Auditability**: Every database access is logged
3. **Consistency**: One pattern for all database operations
4. **Future-Proof**: Easy to add new security features

## Testing Your Migration

After migrating, run:

```bash
# Verify no violations remain
python scripts/verify_database_security.py

# Run tests to ensure functionality
pytest tests/
```

## Common Errors and Solutions

### Error: DatabaseSecurityViolation

You're still using `get_database_deprecated()` somewhere. Search for it:
```bash
grep -r "get_database_deprecated()" src/
```

### Error: 'coroutine' object has no attribute 'collection'

You forgot to await the database call:
```python
db = get_database()  # ❌ Missing await
db = await get_database()  # ✅ Correct
```

### Error: Function cannot be async

Your function is called from sync code. Options:
1. Make the caller async too (preferred)
2. Use `asyncio.run()` at the entry point
3. Refactor to use a different pattern

## Questions?

The structural barrier ensures you can't accidentally use insecure patterns.
If you're getting errors, that's the system working as designed - guiding
you toward the secure architecture.
