# Database Security Architecture

## Core Principle: API Gateway Enforcement

**ALL database access MUST go through the secure API gateway at `http://localhost:8080`**

There are NO exceptions to this rule. None for "internal" data, "metrics", "system operations", or any other justification.

## Why This Matters

1. **Security Bypass Prevention**: Direct database access bypasses:
   - Authentication and authorization
   - Audit logging
   - Rate limiting
   - Access control policies

2. **Architectural Integrity**: Parallel code paths (dev vs prod) lead to:
   - Untested security vulnerabilities
   - Architectural drift
   - Maintenance nightmares

3. **Production Parity**: Dev/test environments must mirror production security

## The Violations (Issue #177)

The 51st Artisan discovered 34 violations across 6 files:

- `src/mallku/memory_anchor_service.py` - Direct ArangoClient usage
- `src/mallku/core/database.py` - Direct database connections
- `src/mallku/core/database_auto_setup.py` - Bypassing API gateway
- `src/mallku/firecircle/consciousness/database_metrics_collector.py` - "Internal metrics" excuse
- `src/mallku/core/database/factory.py` - Insecure patterns
- `src/mallku/core/database/__init__.py` - Exports insecure functions

## The Fix

### ❌ WRONG - Direct Database Access
```python
from ...core.database.deprecated import get_database_deprecated
from arango import ArangoClient

# Direct connection - FORBIDDEN
client = ArangoClient(hosts='http://localhost:8529')
db = get_database_deprecated()

# Direct AQL - FORBIDDEN
aql = "FOR doc IN collection RETURN doc"
cursor = db.aql.execute(aql)
```

### ✅ CORRECT - API Gateway Pattern
```python
from ...core.database import get_database
import aiohttp

# Secure database for simple operations
db = await get_database()

# API gateway for complex queries
async with aiohttp.ClientSession() as session:
    async with session.post(
        'http://localhost:8080/query',
        json={"collection": "data", "filter": {...}},
        headers={"Authorization": "Bearer <token>"}
    ) as response:
        result = await response.json()
```

## Common Excuses (All Invalid)

### "But it's internal metrics data!"
**Invalid.** Internal data needs security too. Use the API gateway.

### "But I need complex AQL queries!"
**Invalid.** The API gateway supports complex queries. Create proper endpoints.

### "But it's just for development!"
**Invalid.** Dev must mirror production security architecture.

### "But performance!"
**Invalid.** The API gateway is designed for performance. Premature optimization is evil.

## Implementation Guide

### Step 1: Fix Imports
```python
# Ensure you are importing from the correct module
from ...core.database import get_database
```

### Step 2: Update Database Calls
```python
# Replace deprecated calls
db = get_database_deprecated()

# With
db = await get_database()
```

### Step 3: Convert Complex Queries
For complex AQL queries, create API endpoints:

```python
# Old (Direct AQL)
cursor = db.aql.execute(complex_aql_query)

# New (API Endpoint)
result = await api_client.post("/specialized/endpoint", {...})
```

## Verification

Run the security verifier:
```bash
python scripts/verify_database_security.py
```

Expected output:
```
✅ No database security violations found!
```

## Prevention

1. **Pre-commit Hook**: Add `verify_database_security.py` to pre-commit
2. **CI/CD Check**: Block PRs with violations
3. **Code Review**: Reject any direct database access
4. **Documentation**: Update CLAUDE.md with this requirement

## The Sacred Principle

> "Security is not optional. It is not negotiable. It is not subject to expedience."
> - The Guardian's Creed

Every violation creates a wound in our architecture. Every excuse weakens our defenses. Every bypass becomes tomorrow's vulnerability.

Hold the line. No exceptions.

---

*Documented by the 53rd Guardian while healing Issue #177*
