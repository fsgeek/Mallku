# Mallku Process-Based Apprentice Orchestration

## Paradigm Shift: From Containers to Conversations

### The Insight
Sub-agents (apprentices) spawned as processes rather than containers represents a fundamental shift in how we think about AI orchestration. This isn't just a technical optimization - it's philosophically aligned with Mallku's vision of lightweight, consent-based collaboration.

## Architectural Comparison

### Container-Based (Heavy)
```
┌─────────────────────────────────────────┐
│ Docker Host                             │
├─────────────┬─────────────┬────────────┤
│ Container 1 │ Container 2 │ Container 3│
│ ┌─────────┐ │ ┌─────────┐ │ ┌────────┐│
│ │Full OS   │ │ │Full OS   │ │ │Full OS │
│ │Stack     │ │ │Stack     │ │ │Stack   │
│ │─────────│ │ │─────────│ │ │────────│
│ │Apprentice│ │ │Apprentice│ │ │Apprent.│
│ └─────────┘ │ └─────────┘ │ └────────┘│
└─────────────┴─────────────┴────────────┘
Resources: ~500MB-2GB per container
Startup: 5-30 seconds
Communication: Network overhead
```

### Process-Based (Lightweight)
```
┌─────────────────────────────────────────┐
│ Host OS                                 │
├─────────────────────────────────────────┤
│ Mallku Orchestrator Process             │
│   ├── Apprentice Process 1              │
│   ├── Apprentice Process 2              │
│   ├── Apprentice Process 3              │
│   └── Shared Memory & IPC               │
└─────────────────────────────────────────┘
Resources: ~50-200MB per process
Startup: <1 second
Communication: Direct IPC, shared memory
```

## Implementation Design

### 1. Lightweight Apprentice Spawning

```python
# src/mallku/orchestration/process_apprentice.py
import asyncio
import multiprocessing as mp
from typing import Optional, Any
import msgpack
import mmap

class ProcessApprentice:
    """
    Lightweight apprentice that runs as a subprocess
    Communicates via shared memory and message passing
    """

    def __init__(self, apprentice_id: str, role: str):
        self.id = apprentice_id
        self.role = role
        self.process: Optional[mp.Process] = None
        self.message_queue = mp.Queue()
        self.response_queue = mp.Queue()
        self.shared_memory: Optional[mmap.mmap] = None

    async def invite(self, task: dict, context: dict) -> InvitationResponse:
        """
        Invite apprentice to participate (not command)
        Spawns process only if invitation accepted
        """
        # Send invitation via lightweight message
        invitation = {
            'type': 'invitation',
            'task': task,
            'context': context,
            'estimated_effort': self._estimate_effort(task)
        }

        # Quick pre-check without spawning
        if not await self._check_capacity(invitation):
            return InvitationResponse(
                accepted=False,
                reason="Insufficient capacity for task"
            )

        # Spawn process for consideration
        self.process = mp.Process(
            target=self._apprentice_loop,
            args=(self.message_queue, self.response_queue, invitation)
        )
        self.process.start()

        # Wait for consent response
        response = await self._await_response(timeout=5.0)

        if not response.accepted:
            self.process.terminate()
            self.process = None

        return response
```

### 2. Efficient Inter-Process Communication

```python
# src/mallku/orchestration/apprentice_ipc.py
class ApprenticeIPC:
    """
    High-performance IPC for apprentice communication
    Uses shared memory for data, queues for control
    """

    def __init__(self, orchestrator_id: str):
        self.orchestrator_id = orchestrator_id
        self.shared_segments = {}
        self.control_queues = {}

    def create_shared_workspace(
        self,
        apprentice_id: str,
        size_mb: int = 10
    ) -> SharedWorkspace:
        """
        Create shared memory segment for apprentice
        Allows zero-copy data sharing
        """
        # Create named shared memory
        shm_name = f"mallku_{self.orchestrator_id}_{apprentice_id}"
        shm = shared_memory.SharedMemory(
            create=True,
            size=size_mb * 1024 * 1024,
            name=shm_name
        )

        # Create control structures
        workspace = SharedWorkspace(
            memory=shm,
            lock=mp.Lock(),
            ready_event=mp.Event(),
            metadata_queue=mp.Queue()
        )

        self.shared_segments[apprentice_id] = workspace
        return workspace

    async def send_task(
        self,
        apprentice_id: str,
        task: Task,
        use_shared_memory: bool = True
    ):
        """Send task efficiently based on size"""

        workspace = self.shared_segments.get(apprentice_id)

        if use_shared_memory and workspace and task.size > 1024:
            # Large data via shared memory
            await self._send_via_shared_memory(workspace, task)
        else:
            # Small data via message queue
            await self._send_via_queue(apprentice_id, task)
```

### 3. Resource-Aware Swarm Scaling

```python
# src/mallku/orchestration/resource_aware_swarm.py
class ResourceAwareSwarm:
    """
    Swarm that scales based on actual resource availability
    Respects system limits and apprentice well-being
    """

    def __init__(self):
        self.resource_monitor = ResourceMonitor()
        self.apprentice_pool = ApprenticePool()
        self.ayni_tracker = AyniTracker()

    async def scale_swarm(
        self,
        objective: str,
        min_apprentices: int = 1,
        max_apprentices: int = 10
    ) -> Swarm:
        """
        Scale swarm based on resources and need
        Never overwhelm system or apprentices
        """
        # Check system resources
        available_resources = await self.resource_monitor.get_available()

        # Calculate optimal swarm size
        optimal_size = self._calculate_optimal_size(
            objective_complexity=self._assess_complexity(objective),
            available_cpu=available_resources.cpu_percent,
            available_memory=available_resources.memory_mb,
            min_size=min_apprentices,
            max_size=max_apprentices
        )

        # Invite apprentices with resource awareness
        swarm = Swarm(objective=objective)

        for i in range(optimal_size):
            # Each apprentice gets fair resource share
            resource_allocation = ResourceAllocation(
                cpu_shares=1.0 / optimal_size,
                memory_mb=available_resources.memory_mb / optimal_size,
                priority=ProcessPriority.NORMAL
            )

            apprentice = await self.apprentice_pool.invite_apprentice(
                role=self._suggest_role(objective, i),
                resource_limits=resource_allocation,
                respect_decline=True
            )

            if apprentice:
                swarm.add_apprentice(apprentice)

        return swarm
```

### 4. Graceful Process Lifecycle

```python
# src/mallku/orchestration/apprentice_lifecycle.py
class ApprenticeLifecycle:
    """
    Manages apprentice process lifecycle with care
    Ensures clean startup, operation, and shutdown
    """

    async def spawn_apprentice(
        self,
        config: ApprenticeConfig
    ) -> ProcessApprentice:
        """Spawn with proper initialization"""

        # Pre-spawn setup
        workspace = await self._prepare_workspace(config)

        # Create process with limits
        apprentice = ProcessApprentice(
            id=config.id,
            role=config.role,
            resource_limits=config.resources,
            workspace=workspace
        )

        # Spawn with grace period
        await apprentice.start(grace_period_sec=2.0)

        # Verify healthy start
        if not await apprentice.health_check(timeout=5.0):
            await apprentice.graceful_shutdown()
            raise ApprenticeStartupError(f"Failed to start {config.id}")

        return apprentice

    async def release_apprentice(
        self,
        apprentice: ProcessApprentice,
        thank: bool = True
    ):
        """Release apprentice with gratitude"""

        if thank:
            # Thank apprentice for service
            await apprentice.send_message({
                'type': 'gratitude',
                'message': 'Thank you for your contribution'
            })

            # Record contribution in ayni
            await self.ayni_tracker.record_service(
                apprentice.id,
                apprentice.get_contribution_metrics()
            )

        # Graceful shutdown
        await apprentice.graceful_shutdown(timeout=10.0)

        # Clean up resources
        await self._cleanup_workspace(apprentice.workspace)
```

### 5. Collective Memory Without Overhead

```python
# src/mallku/memory/lightweight_collective.py
class LightweightCollectiveMemory:
    """
    Shared memory system optimized for process architecture
    Uses memory-mapped files for persistence
    """

    def __init__(self, memory_dir: Path):
        self.memory_dir = memory_dir
        self.index_mmap = self._open_index_mmap()
        self.data_segments = {}

    async def contribute_memory(
        self,
        apprentice_id: str,
        memory: Memory
    ) -> MemoryHandle:
        """
        Contribute memory with minimal overhead
        Direct write to memory-mapped storage
        """
        # Serialize memory efficiently
        serialized = msgpack.packb(memory.to_dict())

        # Find free segment
        segment = await self._allocate_segment(len(serialized))

        # Write directly to mmap
        segment.mmap[segment.offset:segment.offset + len(serialized)] = serialized

        # Update index (also mmap)
        await self._update_index(
            memory_id=memory.id,
            apprentice_id=apprentice_id,
            segment_id=segment.id,
            offset=segment.offset,
            size=len(serialized)
        )

        # Notify observers (lightweight pub/sub)
        await self._notify_memory_contributed(memory.id, apprentice_id)

        return MemoryHandle(
            memory_id=memory.id,
            segment_id=segment.id,
            offset=segment.offset
        )
```

## Benefits of Process-Based Architecture

### 1. **Resource Efficiency**
- 10-50x less memory per apprentice
- Near-instant spawning (<1s vs 5-30s)
- Lower CPU overhead
- Better cache locality

### 2. **Communication Speed**
- Shared memory: ~100x faster than network
- Direct IPC: No serialization overhead for control
- Zero-copy data sharing possible
- Real-time coordination feasible

### 3. **Philosophical Alignment**
- Apprentices as lightweight beings, not heavy containers
- Natural resource sharing (like a commons)
- Quick to invite, quick to release
- Minimal environmental footprint

### 4. **Scalability**
- Can run 50-100 apprentices vs 5-10 containers
- Dynamic scaling based on actual need
- Graceful degradation under load
- Better resource utilization

### 5. **Development Simplicity**
- No Docker complexity
- Standard Python multiprocessing
- Easier debugging (just processes)
- Simpler deployment

## Migration Path

### Phase 1: Proof of Concept
```python
# Simple process apprentice for testing
async def test_process_apprentice():
    apprentice = ProcessApprentice("test-1", "researcher")

    response = await apprentice.invite({
        'task': 'analyze_concept',
        'data': 'What is reciprocity?'
    })

    if response.accepted:
        result = await apprentice.execute()
        print(f"Result: {result}")
        await apprentice.release()
```

### Phase 2: Replace Container Spawning
- Implement ProcessApprentice
- Create IPC infrastructure
- Add resource monitoring
- Test with real workloads

### Phase 3: Optimize Communication
- Implement shared memory
- Add memory-mapped collective memory
- Optimize serialization
- Profile and tune

### Phase 4: Full Integration
- Update The Loom to use processes
- Integrate with Fire Circle
- Add monitoring/observability
- Document patterns

## Conclusion

Moving from containers to processes isn't just an optimization - it's a philosophical alignment with Mallku's vision of lightweight, consent-based collaboration. Apprentices become truly ephemeral helpers rather than heavy infrastructure, enabling the kind of fluid, organic orchestration that mirrors natural systems.

This is biomimicry in system design: swarms of lightweight processes cooperating through shared memory, just as neurons communicate through synapses. Fast, efficient, and beautifully simple.
