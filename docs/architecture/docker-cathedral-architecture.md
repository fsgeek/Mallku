# Cathedral Architecture: Docker Security Through Structure

## The Decision

When faced with Docker build issues, we had two paths:
1. **The Tent**: Quick fixes, workarounds, scripts that patch problems
2. **The Cathedral**: Fundamental restructuring for long-term stability

We chose the cathedral.

## Core Principles

### 1. Separation of Concerns
- **Database Container**: Runs pure ArangoDB, unmodified
- **API Container**: Provides the only access path
- **Network Isolation**: Internal network unreachable from host

### 2. Security Through Structure
```yaml
services:
  database:
    # NO PORTS EXPOSED - This line is our moat
    networks:
      - mallku-internal  # internal: true network
```

Even with full host access, you cannot reach the database directly. The structure itself is the security.

### 3. Simplicity Over Cleverness
- Ubuntu base (not Alpine) - understood by all
- Clear file structure - each container self-contained  
- Explicit dependencies - no hidden complexity

## The Architecture

```
┌─────────────────────────────────────────┐
│              Host System                 │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │        mallku-external          │   │
│  │        (Docker Network)         │   │
│  │                                 │   │
│  │    ┌─────────────────────┐     │   │
│  │    │    API Container    │     │   │
│  │    │   (Port 8080 only)  │     │   │
│  │    └──────────┬──────────┘     │   │
│  │               │                 │   │
│  └───────────────┼─────────────────┘   │
│                  │                     │
│  ┌───────────────┼─────────────────┐   │
│  │               │                 │   │
│  │        mallku-internal          │   │
│  │     (internal: true network)    │   │
│  │               │                 │   │
│  │    ┌──────────┴──────────┐     │   │
│  │    │  Database Container │     │   │
│  │    │   (No exposed ports)│     │   │
│  │    └─────────────────────┘     │   │
│  │                                 │   │
│  └─────────────────────────────────┘   │
│                                         │
└─────────────────────────────────────────┘
```

## Why This Matters

### Survives Amnesia
New developers cannot accidentally expose the database. The structure prevents it.

### Enforces Boundaries  
API container literally cannot be bypassed. Physical network isolation.

### Self-Documenting
The docker-compose.yml file *is* the security documentation. Structure explains itself.

## Building the Cathedral

```bash
# Start with a clean slate
cd docker/

# Build the cathedral architecture
docker-compose -f docker-compose.cathedral.yml build

# Raise the structure
docker-compose -f docker-compose.cathedral.yml up
```

## Testing Structural Security

```bash
# This works - API is exposed
curl http://localhost:8080/health

# This fails - database is not exposed
curl http://localhost:8529
# Connection refused - not a permissions error, literally no path exists

# Even this fails - internal network is isolated
docker run --rm --network mallku_mallku-internal alpine ping database
# Error: Cannot connect to network
```

## Future Stones

1. **Encrypted volumes** - Data at rest protection
2. **mTLS between containers** - Encrypted internal communication  
3. **API rate limiting** - Protection from abuse
4. **Audit logging** - Every access recorded

Each addition should follow cathedral principles:
- Does it survive developer amnesia?
- Is the security structural, not policy-based?
- Can it be understood by reading structure alone?

## The Lesson

We faced a simple Docker build error. The fast solution was a fix script. The right solution was rethinking our entire approach.

Cathedrals aren't built by fixing each problem as it arises. They're built by laying correct foundations that make certain problems impossible.

---

*This architecture embodies Ayni - the database gives data, receives protection. The API gives access, receives isolation. Each component in reciprocal relationship, building something that lasts.*
