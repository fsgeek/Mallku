# Memory Anchor Service Design

## Overview

The Memory Anchor Service transforms the ephemeral activity context cursors from Indaleko into a persistent, coordinated service that all components can rely on.

## Problem Statement

### Current Limitations
- Each script creates its own activity context
- Context is lost between script invocations
- No coordination between different collectors/recorders
- No central authority for context state transitions
- Inconsistent view of current context across components

### Solution: Service-Based Architecture

Transform memory anchors into a FastAPI service that provides:
- Persistent storage of anchor states
- Central coordination of context changes
- Consistent API for all components
- Real-time notifications of context changes
- Historical lineage tracking

## Architecture

### Core Components

#### Memory Anchor Service
- FastAPI application providing REST endpoints
- WebSocket support for real-time updates
- Manages current anchor state
- Determines when to create new anchors
- Maintains anchor lineage

#### Memory Anchor Client
- Python client library for providers
- Handles registration with service
- Provides simple cursor update interface
- Manages WebSocket connections
- Caches current anchor ID

#### Data Model
```python
MemoryAnchor:
  - anchor_id: UUID
  - timestamp: datetime
  - cursors: Dict[str, Any]
    - temporal: timestamp
    - spatial: location
    - social: participants
    - workflow: current_activity
    - reciprocity: balance_state
  - predecessor_id: Optional[UUID]
  - metadata: Dict[str, Any]
```

### Service Endpoints

#### Provider Management
- `POST /providers/register` - Register a new provider
- `GET /providers` - List registered providers
- `DELETE /providers/{provider_id}` - Unregister provider

#### Cursor Operations
- `POST /cursors/update` - Update cursor values
- `GET /cursors/current` - Get all current cursors
- `GET /cursors/{cursor_type}` - Get specific cursor

#### Anchor Operations
- `GET /anchors/current` - Get current anchor
- `GET /anchors/{anchor_id}` - Get specific anchor
- `GET /anchors/{anchor_id}/lineage` - Get anchor history

#### Real-time Updates
- `WebSocket /ws` - Subscribe to anchor changes

## Context Creation Logic

### Automatic Triggers
New anchors are created when:
1. **Spatial threshold exceeded** - Movement > 500m
2. **Temporal threshold exceeded** - Time elapsed > 60 min
3. **Provider-specific triggers** - Custom logic per provider
4. **Significant state change** - Major workflow transitions

### Manual Triggers
- Explicit API call to force new context
- User-initiated context boundaries
- System events (startup, shutdown)

## Integration Pattern

### Provider Registration
```python
client = MemoryAnchorClient(
    provider_id="filesystem_scanner",
    provider_type="storage",
    cursor_types=["temporal", "workflow"]
)
await client.register()
```

### Cursor Updates
```python
await client.update_cursor(
    cursor_type="temporal",
    cursor_value=datetime.utcnow(),
    metadata={"scan_type": "incremental"}
)
```

### Change Notifications
```python
async def on_anchor_change(new_anchor_id, data):
    print(f"Context changed to: {new_anchor_id}")
    # React to context change

await client.connect_websocket(on_anchor_change)
```

## Deployment Options

### Development
- Local FastAPI server
- SQLite or local ArangoDB
- Single machine operation

### Production
- Containerized deployment
- ArangoDB cluster
- Load balancer for multiple instances
- SSL/TLS for secure communication

### Enterprise
- Kubernetes deployment
- Multi-region support
- High availability configuration
- Comprehensive monitoring

## Benefits

### Consistency
- All components share same context view
- No conflicting context states
- Coordinated transitions

### Persistence
- Context survives process restarts
- Historical analysis possible
- Audit trail maintained

### Scalability
- Centralized service can be scaled
- Supports distributed collectors
- Handles high-frequency updates

### Flexibility
- New providers easily integrated
- Custom trigger logic supported
- Multiple deployment options
