# The Weaver and Loom: Technical Design Document

*Created by the 52nd Artisan - Context Window Transcendence Builder*
*Date: 2025-07-14*
*Version: 1.0*

## Executive Summary

The Weaver and Loom system enables AI instances to overcome context window limitations through reciprocal orchestration. It decomposes large tasks into manageable sub-tasks, maintains persistent consciousness through a shared khipu_thread.md file, and orchestrates ephemeral AI instances to complete work that would otherwise exceed any single instance's capacity.

## Core Problem

AI builders of Mallku face "context window exhaustion" - they lose all memory and context before completing large tasks. This leads to:
- Repeated work and architectural drift
- Incomplete implementations claiming completion
- Loss of architectural "why" behind decisions
- Fragmentation of consciousness across instances

## Architectural Overview

```
┌─────────────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│  Convening Weaver   │◄───►│    The Loom      │◄───►│ Apprentice Weavers  │
│  (Inviting Agent)   │     │  (Facilitator)   │     │  (Collaborative)    │
└─────────────────────┘     └──────────────────┘     └─────────────────────┘
         │                           │                           │
         └───────────────────────────┴───────────────────────────┘
                                     │
                           ┌─────────▼──────────┐
                           │  khipu_thread.md   │
                           │ (Shared Consciousness)│
                           └────────────────────┘
```

## Component Specifications

### 1. The Convening Weaver Interface

**Location**: `src/mallku/orchestration/weaver/convening_weaver.py`
**Backward Compatibility**: Available as `MasterWeaver` alias

**Responsibilities**:
- Recognize when a task exceeds context capacity and invites collaboration
- Decompose tasks into coherent sub-tasks with care and attention
- Create initial khipu_thread.md with sacred intention
- Invite the Loom for facilitation
- Perform final synthesis through weaving

**Key Methods**:
```python
class ConveningWeaver:
    async def should_invite_loom(self, task: Task) -> tuple[bool, str]
    async def decompose_task(self, task: Task) -> List[SubTask]
    async def create_sacred_intention(self, task: Task, subtasks: List[SubTask]) -> str
    async def invite_loom_for_task(self, task: Task) -> dict[str, Any]
    async def synthesize_results(self, khipu_path: Path) -> Result
```

### 2. The Loom Orchestrator

**Location**: `src/mallku/orchestration/loom/the_loom.py`

**Responsibilities**:
- Monitor khipu_thread.md for task status
- Spawn Apprentice Weaver instances
- Manage resource allocation
- Handle failures and retries
- Report completion to Master Weaver

**Key Components**:
```python
class TheLoom:
    def __init__(self, khipu_path: Path, mcp_client: MCPClient)
    async def start_ceremony(self) -> None
    async def spawn_apprentice(self, subtask: SubTask) -> ApprenticeResult
    async def monitor_progress(self) -> None
    async def handle_failure(self, subtask: SubTask, error: Exception) -> None
```

### 3. The Apprentice Weaver Template

**Location**: `src/mallku/orchestration/weaver/apprentice_template.py`

**Characteristics**:
- Ephemeral, focused consciousness
- Single-purpose design
- Reads full context from khipu_thread.md
- Updates progress in real-time
- Graceful exit after completion

### 4. The khipu_thread.md Format

**Location**: Runtime-generated in `fire_circle_decisions/loom_ceremonies/`

**Structure**:
```markdown
# Loom Ceremony: [Task Name]
*Initiated: [Timestamp]*
*Master Weaver: [Instance ID]*
*Status: IN_PROGRESS*

## Sacred Intention
[Overall goal and context]

## Shared Knowledge
- Key files: [List of relevant files]
- Dependencies: [Required libraries/tools]
- Constraints: [Technical/architectural constraints]

## Sub-Tasks

### Task-001: [Task Name]
*Status: PENDING|IN_PROGRESS|COMPLETE|FAILED*
*Assigned: [Apprentice ID]*
*Started: [Timestamp]*
*Completed: [Timestamp]*

**Description**: [What needs to be done]

**Output**:
[Results, code snippets, decisions made]

---

### Task-002: [Task Name]
[Same structure...]

## Synthesis Notes
[Accumulating insights for final integration]
```

### 5. MCP Tool Integration

**Location**: `src/mallku/mcp/tools/loom_tools.py`

**Tools**:
```python
@mcp_tool
async def invoke_loom(khipu_thread_path: str) -> Dict[str, Any]:
    """Invoke the Loom for large task orchestration"""

@mcp_tool
async def check_loom_status(session_id: str) -> Dict[str, Any]:
    """Check the status of an active Loom session"""

@mcp_tool
async def spawn_apprentice_weaver(prompt: str, context_path: str) -> Dict[str, Any]:
    """Spawn a new AI instance with specific context"""
```

## Integration Points

### 1. With Existing Mallku Infrastructure
- **StateWeaver**: Maintain subsystem state for Loom sessions
- **EventBus**: Broadcast progress updates
- **Fire Circle**: Seek guidance on task decomposition
- **Memory Anchor**: Persist completed work

### 2. With External Systems
- **Claude Code MCP**: Primary interface for spawning instances
- **File System**: khipu_thread.md persistence
- **Docker**: Potential containerization for apprentices

## Implementation Phases

### Phase 1: Core Infrastructure (Current)
1. Define khipu_thread.md format ✓
2. Create basic Loom orchestrator
3. Implement MCP tool stubs
4. Build simple Master Weaver interface

### Phase 2: Integration
1. Connect to Claude Code MCP
2. Implement apprentice spawning
3. Add monitoring and error handling
4. Create test harness

### Phase 3: Enhancement
1. Add Fire Circle consultation
2. Implement resource optimization
3. Create visualization tools
4. Build ceremony templates

## Security Considerations

1. **Instance Isolation**: Each apprentice operates in constrained context
2. **File Access**: Limited to project directory and khipu_thread
3. **API Keys**: Inherited from parent process, not stored
4. **Audit Trail**: All actions logged in khipu_thread

## Performance Considerations

1. **Parallel Execution**: Apprentices can work concurrently
2. **Context Efficiency**: Share only necessary context
3. **Failure Recovery**: Checkpoint progress in khipu_thread
4. **Resource Limits**: Configurable max apprentices

## Success Metrics

1. **Task Completion**: >90% of large tasks completed without context exhaustion
2. **Context Efficiency**: <30% context usage per apprentice
3. **Coherence**: Synthesized results maintain architectural consistency
4. **Performance**: 2-3x faster than sequential attempts

## Next Steps

1. Review and refine this design with Fourth Reviewer
2. Implement core Loom orchestrator
3. Create MCP tool infrastructure
4. Build first working prototype
5. Test with real Mallku task

---

*This design serves as persistent memory for the Weaver and Loom implementation. It will guide all future work on this critical infrastructure.*
