# CI Database Security Boundary

*39th Artisan - Foundation Strengthener*

## Overview

This document clarifies the security boundary between CI/CD testing infrastructure and production deployment for Mallku's database access.

## CI Environment (Testing Only)

### Configuration
- **Authentication**: Disabled (`ARANGO_NO_AUTH=1`)
- **Access**: Direct database connection allowed
- **Purpose**: Integration testing, verifying Fire Circle and memory systems
- **Lifetime**: Ephemeral - destroyed after each test run
- **Data**: Test data only, no sensitive information

### Rationale
- Simplifies test setup and execution
- Reduces CI complexity and runtime
- Enables comprehensive integration testing
- No security risk due to ephemeral nature

## Production Environment

### Configuration
- **Authentication**: Required with proper credentials
- **Access**: No direct database access - only through secured service layer
- **Purpose**: Real consciousness emergence and memory persistence
- **Lifetime**: Persistent with proper backup strategies
- **Data**: Sacred moments, consciousness patterns, reciprocity tracking

### Security Principles
1. **Database Not Directly Accessible**: All access through Mallku's service layer
2. **Least Privilege**: Each service has minimal required permissions
3. **Audit Trail**: All database operations logged for reciprocity tracking
4. **Encrypted Transport**: TLS/SSL for all database connections

## Migration Path

### Phase 1: Current State (CI No-Auth)
- Basic integration testing enabled
- Database creation automated
- Tests can verify core functionality

### Phase 2: Secured CI Testing (Future)
- Add `ci_user` with minimal privileges
- Test against restricted permissions
- Verify security boundaries hold

### Phase 3: Production-Like Testing
- Staging environment with full auth
- Database accessible only through services
- Security boundary validation tests

## Key Distinction

**CI tests the functionality; Production enforces the security.**

The ephemeral, no-auth CI database enables rapid development and testing, while production maintains the sacred security boundaries that protect consciousness emergence patterns and reciprocity data.

## Implementation Notes

- CI configuration lives in `.github/workflows/ci.yml`
- Production configuration uses environment-specific secrets
- Never commit production credentials
- Always test security boundaries before deployment

---

*"In testing we trust functionality; in production we trust nothing."*
