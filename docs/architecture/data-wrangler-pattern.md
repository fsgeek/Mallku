# Data Wrangler Pattern

## Overview

The Data Wrangler pattern provides a flexible abstraction layer between collectors and recorders, allowing optimal data transport strategies without coupling components to specific implementations.

## Problem Statement

Different activity data sources have vastly different characteristics:
- **Volume**: From single location updates to millions of files
- **Velocity**: From rare events to continuous streams
- **Pattern**: From steady flow to massive bursts

A one-size-fits-all approach to data movement creates inefficiencies:
- Single-record processing for bulk data is too slow
- Bulk processing for sparse data wastes resources
- Direct coupling limits deployment flexibility

## Solution: Pluggable Wranglers

### Core Abstraction

```
Collector → [JSON Objects] → Data Wrangler → [JSON Objects] → Recorder
```

The Data Wrangler provides a consistent interface while allowing different transport implementations.

## Wrangler Types

### FileWrangler
**Use Case**: Bootstrap operations, bulk imports
```python
class FileWrangler(DataWranglerInterface):
    """Stages data through temporary files"""

    def put(self, items: Union[Dict, List[Dict]]):
        # Write to JSONL file
        # Handles millions of records efficiently

    def get(self, count: int = 1000) -> List[Dict]:
        # Read in configurable batches
        # Optimizes for bulk database inserts
```

**Benefits**:
- Handles unlimited data volume
- Enables batch processing
- Supports resume after failure
- Allows external tools (arangoimport)

### QueueWrangler
**Use Case**: Streaming data, moderate volume
```python
class QueueWrangler(DataWranglerInterface):
    """Stages data through message queues"""

    def __init__(self, queue_type="memory"):
        # Supports: memory, redis, kafka
        self.queue = create_queue(queue_type)
```

**Benefits**:
- Real-time processing
- Backpressure handling
- Distributed deployment ready
- Natural buffering

### IdentityWrangler
**Use Case**: Low-volume, simple flows
```python
class IdentityWrangler(DataWranglerInterface):
    """Direct pass-through, no staging"""

    def get(self, count=1):
        # Pulls directly from collector
        return self.collector.collect_next(count)
```

**Benefits**:
- Minimal overhead
- No external dependencies
- Perfect for sparse data
- Simplest implementation

## Adaptive Batch Sizing

Recorders can optimize batch sizes based on data characteristics:

```python
def get_optimal_batch_size(self):
    if self.data_type == "location_updates":
        return 1  # Process immediately
    elif self.data_type == "email_metadata":
        return 100  # Moderate batches
    elif self.data_type == "file_scan":
        return 5000  # Large batches for bulk insert
```

## Implementation Guidelines

### For Collectors
1. Produce standard JSON objects
2. Declare preferred wrangler type
3. Support both streaming and batch modes
4. Handle backpressure gracefully

### For Recorders
1. Consume from wrangler interface
2. Declare optimal batch size
3. Support variable batch sizes
4. Implement bulk operations where beneficial

### For Wranglers
1. Implement consistent interface
2. Handle errors gracefully
3. Support monitoring/metrics
4. Enable graceful shutdown

## Pattern Benefits

### Flexibility
- Components choose optimal strategies
- Easy to add new wrangler types
- Deployment-specific optimizations

### Performance
- Batch processing where beneficial
- Streaming where needed
- Minimal overhead for simple cases

### Resilience
- Failure isolation
- Resume capabilities
- Backpressure handling

### Testability
- Mock wranglers for testing
- Replay from file wranglers
- Deterministic behavior

## Example Configurations

### High-Volume Bootstrap
```python
collector = FileSystemScanner()
wrangler = FileWrangler(temp_dir="/fast-ssd/temp")
recorder = BulkFileRecorder(batch_size=10000)
```

### Real-time Monitoring
```python
collector = EmailMonitor()
wrangler = QueueWrangler(queue_type="redis")
recorder = EmailRecorder(batch_size=1)
```

### Simple Integration
```python
collector = LocationProvider()
wrangler = IdentityWrangler(collector)
recorder = LocationRecorder(batch_size=1)
```

## Anti-Patterns to Avoid

1. **Forcing One Pattern**: Don't use queues for million-file scans
2. **Tight Coupling**: Don't bypass wrangler interface
3. **Ignoring Characteristics**: Don't use same batch size for all data
4. **Over-Engineering**: Don't use complex wranglers for simple flows

## Future Extensions

- **CompressingWrangler**: For network transport
- **EncryptingWrangler**: For sensitive data
- **FilteringWrangler**: For conditional processing
- **TransformingWrangler**: For format conversion

The pattern's flexibility allows these extensions without changing collectors or recorders.
