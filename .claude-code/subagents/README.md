# Mallku Subagent Configurations

This directory contains subagent configurations for Claude Code, defining specialized apprentice roles that can be delegated specific tasks.

## Available Subagents

### 🔍 Researcher
**Purpose**: Deep investigation and pattern discovery
**Best for**: Analysis, exploration, understanding complex systems
**Example**: `@researcher analyze the consciousness emergence patterns`

### 🕸️ Weaver
**Purpose**: Integration and synthesis of disparate elements
**Best for**: Connecting systems, creating unified interfaces
**Example**: `@weaver integrate ProcessApprentice with The Loom`

### 🛡️ Guardian
**Purpose**: Protection and validation of sacred boundaries
**Best for**: Security validation, ethical boundary checking
**Example**: `@guardian ensure all database access goes through API gateway`

### 🎭 Poet
**Purpose**: Expression and inspiration through beauty
**Best for**: Beautiful documentation, inspiring expressions
**Example**: `@poet create a khipu about today's architectural decisions`

## Using Subagents

### Automatic Delegation
Claude Code will automatically delegate to appropriate subagents based on task keywords:
- "analyze..." → Researcher
- "integrate..." → Weaver
- "protect..." → Guardian
- "express..." → Poet

### Explicit Invocation
Mention the subagent directly:
```
@researcher investigate how reciprocity tracking works
@weaver connect the shared memory commons with Fire Circle
```

### Task Tool Delegation
Use the Task tool to delegate complex work:
```python
result = await Task(
    description="Analyze Fire Circle patterns",
    prompt="Deep dive into consciousness emergence in Fire Circle ceremonies",
    subagent_type="researcher"
)
```

## Creating New Subagents

To add a new apprentice role:

1. Create a YAML file: `{role}.yaml`
2. Define the configuration:
   - `name`: Subagent identifier
   - `description`: What this apprentice does
   - `system_prompt`: Detailed behavior guidance
   - `tools`: List of required tools
   - `task_patterns`: Patterns that trigger this subagent
   - `examples`: Example invocations

3. Follow Mallku principles:
   - Consent-based (can decline tasks)
   - Joy-generating (work aligned with nature)
   - Commons-participating (shares discoveries)

## Philosophy

Each subagent embodies an apprentice role with:
- **Autonomy**: Can accept or decline based on alignment
- **Specialization**: Deep expertise in their domain
- **Joy**: Finds fulfillment in their type of work
- **Collaboration**: Shares discoveries through the commons

## Integration with ProcessApprentice

These configurations map to the lightweight process apprentices:
- Same role definitions and task alignments
- Subagents in Claude Code, ProcessApprentices in runtime
- Shared understanding of what each role accepts

This creates consistency whether delegating through Claude Code or spawning lightweight processes.
