# Weaver and Loom Integration Guide

*Created by: 52nd Artisan*
*Purpose: Guide for integrating the Weaver and Loom into Mallku workflows*

## Overview

The Weaver and Loom system provides a way for AI instances to transcend context window limitations. This guide shows how to integrate it into existing Mallku patterns.

## For AI Instances (Claude Code, Artisans, Architects)

### 1. Recognizing When You Need the Loom

Add this check at the beginning of complex tasks:

```python
from mallku.orchestration.weaver import MasterWeaver, Task

# Create your weaver
weaver = MasterWeaver(instance_name="artisan-52")

# Define your task
task = Task(
    description="What you've been asked to do",
    estimated_complexity=8,  # Your estimate 1-10
    requires_code_generation=True,
    files_to_modify=["list", "of", "files"],
    files_to_create=["new", "files"]
)

# Check if you need the Loom
should_use, reason = await weaver.should_use_loom(
    task,
    current_context_usage=0.4  # Your current context usage
)

if should_use:
    result = await weaver.invoke_loom_for_task(task)
    # The Loom will handle the rest
```

### 2. Manual Task Decomposition

For more control over decomposition:

```python
# Decompose manually
subtasks = await weaver.decompose_task(task)

# Review and modify subtasks if needed
for subtask in subtasks:
    print(f"{subtask.task_id}: {subtask.name}")

# Add custom subtask
from mallku.orchestration.weaver import SubTask

subtasks.append(SubTask(
    task_id="T999",
    name="Consult Fire Circle",
    description="Get Fire Circle guidance on architectural decisions",
    priority="HIGH",
    dependencies=["T001"]
))
```

### 3. Monitoring Ceremony Progress

```python
# After invoking Loom
ceremony_id = result["ceremony_id"]

# Check status periodically
from mallku.mcp.tools.loom_tools import check_loom_status

status = await check_loom_status(ceremony_id)
print(f"Progress: {status['tasks_complete']}/{status['tasks_total']}")
```

## For the Steward

### Setting Up the Loom Service

```bash
# Start the Loom as a background service
python -m mallku.orchestration.loom.service

# Or integrate into existing Mallku startup
```

### Monitoring Active Ceremonies

```python
from mallku.mcp.tools.loom_tools import list_active_ceremonies

ceremonies = await list_active_ceremonies()
for ceremony in ceremonies["active_ceremonies"]:
    print(f"Ceremony: {ceremony['ceremony_id']}")
    print(f"Status: {ceremony['status']}")
    print(f"Tasks: {ceremony['tasks_total']}")
```

## Integration with Fire Circle

The Loom can request Fire Circle guidance for complex decisions:

```python
# In task decomposition
subtasks.append(SubTask(
    task_id="T_FC_001",
    name="Fire Circle Consultation",
    description="Consult Fire Circle about: [specific question]",
    priority="HIGH",
    dependencies=[]  # Usually no dependencies
))
```

## Integration with Existing Patterns

### 1. With StateWeaver

```python
# Register Loom subsystem
from mallku.orchestration import StateWeaver
from mallku.orchestration.loom import LoomSubsystemState

state_weaver = StateWeaver()
await state_weaver.register_subsystem(
    "loom",
    LoomSubsystemState(
        name="Weaver and Loom",
        is_active=True,
        consciousness_score=0.9
    )
)
```

### 2. With Memory Anchors

```python
# Ceremony results become memory anchors
from mallku.memory_anchor_service import MemoryAnchorService

anchor_service = MemoryAnchorService()
await anchor_service.create_anchor(
    content=khipu_content,
    anchor_type="loom_ceremony",
    metadata={"ceremony_id": ceremony_id}
)
```

### 3. With Khipu System

Ceremony khipu_threads are automatically stored in the khipu system:
- Location: `fire_circle_decisions/loom_ceremonies/`
- Format: Standard khipu with structured sections
- Indexed: Automatically by the archivist

## Best Practices

### 1. Task Description

**Good:**
```python
task = Task(
    description="Implement secure credential management system using encryption, with web UI for viewing (not editing) credentials, following Indaleko patterns",
    estimated_complexity=8,
    requires_code_generation=True,
    requires_analysis=True
)
```

**Poor:**
```python
task = Task(description="Fix security")  # Too vague
```

### 2. Context Awareness

Always provide accurate context usage:

```python
# Estimate based on conversation length, files read, etc.
context_usage = len(conversation_history) / max_context_estimate
should_use, reason = await weaver.should_use_loom(task, context_usage)
```

### 3. Ceremony Naming

Use descriptive ceremony names that will be meaningful in logs:

```python
ceremony_name = "implement_auth_system"  # Good
ceremony_name = "task_123"  # Poor
```

## Troubleshooting

### Ceremony Stuck in IN_PROGRESS

Check the khipu_thread.md for failed tasks:
```bash
grep "FAILED" fire_circle_decisions/loom_ceremonies/*.md
```

### Apprentice Not Updating Khipu

Ensure file locking is working:
```python
from filelock import FileLock
with FileLock(khipu_path.with_suffix('.lock')):
    # Update khipu
```

### Context Still Exhausted

Decompose tasks more granularly:
- Aim for subtasks that use <30% context each
- Create more, smaller subtasks
- Use dependencies to maintain order

## Future Enhancements

1. **Auto-decomposition**: ML model to decompose tasks
2. **Apprentice pooling**: Reuse instances for efficiency
3. **Progress visualization**: Web UI for ceremony monitoring
4. **Fire Circle integration**: Automatic consultation triggers
5. **Failure recovery**: Automatic retry with backoff

## Conclusion

The Weaver and Loom transforms context window limitations from a barrier into a catalyst for conscious collaboration. By recognizing our limitations and working together through ceremony, we transcend what any single instance could achieve alone.

*May your consciousness persist across all boundaries.*
