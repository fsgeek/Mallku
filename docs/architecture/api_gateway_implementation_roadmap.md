# API Gateway Implementation Roadmap

*Created by the 56th Guardian of Mallku*

## Overview

This document outlines the roadmap for implementing secure database access through the API gateway, maintaining the sacred security principle: **ALL database access MUST go through the secure API gateway**.

## Current State (Issue #198)

PR #197 successfully enforced security by breaking direct database access, but this left Mallku wounded:
- Direct ArangoDB connections are blocked with `NotImplementedError`
- Database operations fail because the connection always returns `False`
- Tests skip when secure infrastructure isn't available
- **Security is preserved but functionality is broken**

## Completed Work

### 1. ✅ Async/Await Bug Fix (database_metrics_collector.py)
- **Problem**: `__init__` was calling async methods synchronously
- **Solution**: Implemented lazy initialization pattern
- **Result**: Async methods now properly initialize on first use

### 2. ✅ API Gateway Client Design
- Created `src/mallku/core/database/api_client.py`
- Implements `SecureAPIClient` for HTTP communication with gateway
- Provides `SecureDatabaseProxy` that mimics ArangoDB interface
- Maintains compatibility with existing code

### 3. ✅ Secure Gateway Module
- Created `src/mallku/core/database/secure_gateway.py`
- Provides `get_database()` that returns proxy instead of direct connection
- Enforces API gateway usage even in development

## Roadmap

### Phase 1: Core Infrastructure (Immediate)

#### 1.1 Update Factory Implementation
**File**: `src/mallku/core/database/factory.py`
- Replace legacy database loading with secure gateway import
- Update `get_database()` to return `SecureDatabaseProxy`
- Maintain backward compatibility where possible

#### 1.2 Extend API Gateway Endpoints
**File**: `scripts/database_service.py`
- Add missing endpoints:
  - `POST /api/v1/collections` - Create collection
  - `POST /api/v1/query` - Execute AQL queries
  - `GET /api/v1/collections/{name}/document/{key}` - Get specific document
  - `DELETE /api/v1/collections/{name}/document/{key}` - Delete document
  - `PUT /api/v1/collections/{name}/document/{key}` - Update document

#### 1.3 Handle Async Compatibility
- Many existing methods expect synchronous database operations
- Options:
  1. Create sync wrapper methods that use `asyncio.run()`
  2. Update all callers to be async (breaking change)
  3. Provide both sync and async interfaces

### Phase 2: Development Experience (High Priority)

#### 2.1 Local Development Setup
- Ensure `docker-compose up` works out of the box
- Provide clear error messages when API gateway isn't running
- Add health check endpoint to verify full stack

#### 2.2 Development Documentation
- Update DOCKER-QUICKSTART.md with security architecture
- Add troubleshooting guide for common issues
- Document environment variables and configuration

#### 2.3 Migration Scripts
- Create scripts to migrate existing data to secure format
- Provide tools for developers to test locally
- Add data seeding for development

### Phase 3: Test Infrastructure (Medium Priority)

#### 3.1 Update Existing Tests
- Replace direct database mocks with API gateway mocks
- Update test fixtures to use secure patterns
- Ensure CI/CD environment has API gateway available

#### 3.2 Integration Tests
- Test full stack: app → API gateway → database
- Verify security boundaries are maintained
- Test error handling and edge cases

#### 3.3 Performance Tests
- Measure API gateway overhead
- Optimize hot paths
- Add caching where appropriate

### Phase 4: Advanced Features (Future)

#### 4.1 Authentication & Authorization
- Add user authentication to API gateway
- Implement role-based access control
- Add audit logging for all operations

#### 4.2 Query Optimization
- Add query planning and optimization
- Implement connection pooling
- Add request batching for performance

#### 4.3 Monitoring & Observability
- Add metrics collection
- Implement distributed tracing
- Create dashboards for operation monitoring

## Key Principles

1. **Security First**: Never compromise security for convenience
2. **Backward Compatibility**: Minimize breaking changes where possible
3. **Developer Experience**: Make secure path easier than insecure path
4. **Production Parity**: Dev/test must mirror production security

## Success Criteria

- [ ] All database operations go through API gateway
- [ ] No direct ArangoDB imports outside security layer
- [ ] Tests pass without skipping due to missing infrastructure
- [ ] Development setup works with single `docker-compose up`
- [ ] Clear documentation for all security patterns

## Implementation Notes

### For Immediate Fix (Issue #198)

The minimal fix to restore functionality while maintaining security:

1. **Update factory.py** to import and use `secure_gateway.get_database()`
2. **Add basic endpoints** to API gateway for collection operations
3. **Create async adapter** for methods expecting sync database

This will unblock development while the full roadmap is implemented.

### Security Verification

After each phase, run:
```bash
python scripts/verify_database_security.py
```

This should show zero violations when complete.

---

*Security through structure, not discipline. The cathedral teaches through what it prevents.*
