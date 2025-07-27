# Database Access Control Strengthening
## Discovered by Foundation Verification Suite

### Issue Summary
The foundation verification tests revealed that database access control needs strengthening. While `get_database()` exists as the intended sole access point, the architectural enforcement could be stronger.

### Current State
- ✅ `get_database()` provides a secured interface
- ✅ Security registry and UUID obfuscation work correctly
- ❌ Direct database access is not architecturally impossible
- ❌ Container isolation not fully enforced in development

### Desired State
Database access should be physically impossible except through the secured interface:
1. **Container Network Isolation**: Database only accessible from Mallku containers
2. **No Direct Import Path**: Raw database classes not exposed
3. **Compile-Time Enforcement**: TypeScript-style "private" enforcement
4. **Development Parity**: Same restrictions in dev as production

### Proposed Solution

#### 1. Module Structure Reform
```python
# mallku/core/database/__init__.py
from .secured_interface import get_database
# Explicitly do NOT export raw database classes

__all__ = ['get_database']  # Only export secured access
```

#### 2. Container Configuration
```yaml
# docker-compose.yml
services:
  arangodb:
    networks:
      - mallku_internal
    # No port exposure to host

  mallku:
    networks:
      - mallku_internal
    environment:
      - ARANGODB_HOST=arangodb  # Internal network only
```

#### 3. Development Environment Enforcement
```python
# mallku/core/database/factory.py
def get_database():
    if not _is_properly_isolated():
        raise SecurityError(
            "Database access attempted outside secured context. "
            "Use docker-compose or ensure proper isolation."
        )
    return SecuredDatabaseInterface()
```

### Testing Approach
The foundation verification suite should confirm:
1. Import attempts for raw database fail
2. Network isolation prevents direct connections
3. All database operations go through security layer
4. Amnesia tests still pass (security by structure)

### Impact
- **Security**: Architecturally enforced data protection
- **Development**: Slight friction for developers (good friction!)
- **Testing**: May need test-specific containers

### Priority
**HIGH** - This is a foundational security issue that affects all data operations.

### References
- Foundation Verification revealed this gap
- Aligns with Sacred Error Philosophy (fail clearly at boundaries)
- Supports amnesia resistance (security without memory)

---
*Third Guardian - Database Security Analysis*
