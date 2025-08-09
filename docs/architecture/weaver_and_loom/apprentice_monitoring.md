# Apprentice Lifecycle Monitoring

*Created by: 69th Guardian*
*Purpose: To maintain continuous awareness of the health and progress of all who serve*

## Overview

The Apprentice Lifecycle Monitor provides comprehensive observability for apprentice weavers in the Mallku orchestration system. This monitoring serves Mallku's fundamental need for **HEARTBEAT** - continuous operation, maintenance, and health awareness.

## Architecture

### Core Components

1. **ApprenticeMonitor** - Central monitoring service that tracks all active apprentices
2. **ApprenticeRecord** - Complete lifecycle record for each apprentice
3. **ApprenticeMetrics** - Performance and health metrics
4. **Monitoring API** - HTTP endpoints for external monitoring systems

### Lifecycle States

```
INITIALIZING → READY → WORKING → COMPLETING → COMPLETED
                 ↓         ↓          ↓
              FAILED   TIMEOUT   TERMINATED
                 ↓         ↓          ↓
                      CLEANED
```

## Features

### Real-time State Tracking

The monitor tracks each apprentice through its complete lifecycle:

```python
# Register a new apprentice
record = await monitor.register_spawn(
    apprentice_id="apprentice-001",
    task_id="T001",
    ceremony_id="bug-healing-2025",
    container_name="mallku-apprentice-001"
)

# Update state as work progresses
await monitor.update_state(apprentice_id, ApprenticeState.WORKING)
```

### Performance Metrics Collection

Continuous collection of resource usage and performance data:

```python
await monitor.record_metrics(apprentice_id, {
    "memory_mb": 256.5,
    "cpu_percent": 45.2,
    "khipu_updates": 3,
    "log_lines": 150
})
```

### Error and Warning Tracking

Capture issues for debugging and analysis:

```python
await monitor.record_error(apprentice_id, "Out of memory error")
await monitor.record_error(apprentice_id, "Large allocation", error_type="warning")
```

### Ceremony-wide Metrics

Aggregate metrics across all apprentices in a ceremony:

```python
metrics = await monitor.get_ceremony_metrics(ceremony_id)
# Returns:
# - total_apprentices, active_apprentices, completed_apprentices
# - total_memory_mb, average_cpu_percent
# - total_errors, average_task_time
```

## Integration

### With The Loom

The monitor integrates seamlessly with the Loom orchestrator:

```python
# In _spawn_apprentice method
monitor = get_apprentice_monitor()
await monitor.register_spawn(...)
await monitor.update_state(apprentice_id, ApprenticeState.READY)

# In _monitor_apprentice_progress
await monitor.update_state(apprentice_id, ApprenticeState.WORKING)
```

### HTTP API Endpoints

The monitoring API provides RESTful endpoints:

- `GET /api/v1/monitoring/health` - Overall system health
- `GET /api/v1/monitoring/apprentices` - List active apprentices
- `GET /api/v1/monitoring/apprentices/{id}` - Get specific apprentice status
- `GET /api/v1/monitoring/ceremonies/{id}/metrics` - Get ceremony metrics
- `GET /api/v1/monitoring/metrics/prometheus` - Prometheus-compatible metrics

### Database Persistence

When enabled, the monitor persists:
- Lifecycle events to `apprentice_lifecycle_events` collection
- Final records to `apprentice_records` collection

## Usage Examples

### Basic Monitoring

```python
from mallku.orchestration.loom.apprentice_monitor import get_apprentice_monitor

monitor = get_apprentice_monitor()

# Monitor will automatically track apprentices spawned by the Loom
# Access current status anytime:
for apprentice_id, record in monitor.active_apprentices.items():
    print(f"{apprentice_id}: {record.current_state.value}")
```

### Custom Integration

```python
# Create a monitor with custom intervals
monitor = ApprenticeMonitor(
    persistence_enabled=True,
    metrics_interval=60,      # Collect metrics every minute
    health_check_interval=30  # Health check every 30 seconds
)

# Register external apprentice
await monitor.register_spawn(...)

# Update based on external events
await monitor.update_state(apprentice_id, ApprenticeState.WORKING)
await monitor.record_metrics(apprentice_id, custom_metrics)
```

### Prometheus Integration

Configure Prometheus to scrape:
```yaml
scrape_configs:
  - job_name: 'mallku_apprentices'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/api/v1/monitoring/metrics/prometheus'
```

## Metrics Collected

### Timing Metrics
- **container_startup_time** - Time from spawn to READY state
- **task_execution_time** - Time from WORKING to COMPLETED state

### Resource Metrics
- **memory_usage_mb** - Current memory usage
- **cpu_usage_percent** - Current CPU utilization

### Activity Metrics
- **khipu_updates_count** - Number of updates to khipu thread
- **log_lines_generated** - Total log output
- **errors_encountered** - Error count
- **warnings_encountered** - Warning count

## Future Enhancements

1. **Predictive Analytics** - Detect patterns that lead to failures
2. **Resource Optimization** - Suggest optimal resource allocations
3. **Distributed Tracing** - Track requests across apprentices
4. **Custom Alerts** - Configurable alerting rules
5. **Historical Analysis** - Long-term trend analysis

## Philosophy

This monitoring system embodies the principle of **continuous awareness without judgment**. Like a gardener tending plants, we observe growth and health, intervening only when needed. The metrics serve not as judgment but as understanding - helping Mallku learn what conditions allow apprentices to flourish.

Through monitoring, we teach Mallku about:
- **Patience** - Allowing time for tasks to complete
- **Attention** - Noticing when help is needed
- **Balance** - Managing resources wisely
- **Care** - Maintaining health of all who serve

---

*"To watch over is an act of love. To measure without judgment is wisdom."*

*69th Guardian*
