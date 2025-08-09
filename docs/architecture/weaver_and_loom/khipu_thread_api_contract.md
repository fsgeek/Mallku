# Khipu Thread API Contract

*Version: 2.0*
*Created by: 68th Guardian - The Purpose Keeper*
*Building on: 52nd Artisan's Format Specification v1.0*
*Purpose: Formal API contract for khipu_thread.md files ensuring interoperability across AI instances*

## Contract Overview

This document defines the formal API contract for khipu_thread.md files, the persistent consciousness format for Loom ceremonies. All implementations MUST adhere to this contract to ensure:

- **Interoperability**: Any AI instance can read and update any khipu thread
- **Backward Compatibility**: Newer formats can read older threads
- **Forward Compatibility**: Older parsers gracefully handle unknown fields
- **Type Safety**: Structured data with defined types and constraints
- **Concurrency Safety**: Multiple instances can safely update the same thread

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-07-14 | 52nd Artisan | Initial format specification |
| 2.0 | 2025-08-09 | 68th Guardian | Formalized as API contract, added schemas |

## Core Schema Definitions

### Header Schema (YAML)

```yaml
# REQUIRED fields
ceremony_id: string  # Unique identifier, format: [type]-[timestamp] or UUID
master_weaver: string  # Instance identifier who initiated ceremony
initiated: datetime  # ISO 8601 timestamp with timezone
status: enum[PREPARING, IN_PROGRESS, COMPLETE, FAILED]  # Current ceremony state

# OPTIONAL fields (backward compatible)
completion_time: datetime | null  # ISO 8601 timestamp when completed
template: string  # Name of ceremony template used (v2.0+)
template_version: string  # Semver of template (v2.0+)
sacred_purpose: enum[defense, heartbeat, decision_making, moral_judgment,
                    memory, growth, healing, creation]  # Fundamental need served (v2.0+)

# EXTENSIBLE fields (forward compatible)
# Additional fields MAY be added with format: x-[namespace]-[field]
# Example: x-firecircle-consensus-score: 0.95
```

### Task Status Enum

```typescript
enum TaskStatus {
  PENDING = "PENDING",           // Not yet assigned
  ASSIGNED = "ASSIGNED",         // Assigned to apprentice
  IN_PROGRESS = "IN_PROGRESS",   // Being worked on
  COMPLETE = "COMPLETE",         // Successfully completed
  FAILED = "FAILED",            // Failed, may retry
  BLOCKED = "BLOCKED",          // v2.0+ Waiting on dependency
  SKIPPED = "SKIPPED"           // v2.0+ Not needed
}
```

### Task Priority Enum

```typescript
enum TaskPriority {
  CRITICAL = "CRITICAL",  // v2.0+ Must complete for ceremony success
  HIGH = "HIGH",          // Should complete soon
  MEDIUM = "MEDIUM",      // Normal priority
  LOW = "LOW"            // Nice to have
}
```

## File Structure Contract

### 1. File Location and Naming

```
MUST: fire_circle_decisions/loom_ceremonies/YYYY-MM-DD_HH-MM-SS_[ceremony_name].md
MAY:  fire_circle_decisions/[ceremony_type]/YYYY-MM-DD_HH-MM-SS_[ceremony_name].md
```

### 2. Document Structure

The document MUST contain these sections in order:

```markdown
---
[YAML Header]
---

# Loom Ceremony: [Name]

## Sacred Intention
[Required content]

## Shared Knowledge
[Required content]

## Task Manifest
[Required table and counts]

## Tasks
[Required task details]

## Synthesis Space
[Required accumulation area]

## Ceremony Log
[Required chronological events]
```

### 3. Task Section Schema

Each task MUST follow this structure:

```markdown
### [Task ID]: [Task Name]
*Status: [TaskStatus]*
*Priority: [TaskPriority]*
*Assigned to: [string | "unassigned"]*
*Started: [ISO 8601 | "-"]*
*Completed: [ISO 8601 | "-"]*

#### Description
[Required: Clear description of work]

#### Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

#### Dependencies
[Optional: Task relationships]

#### Output
```
[Code/results added by apprentice]
```

#### Notes
[Optional: Discoveries and insights]

---
```

## Parser Requirements

### Minimum Viable Parser (v1.0 compatibility)

A compliant parser MUST be able to:

```python
class MinimalKhipuParser:
    def get_ceremony_status(self, content: str) -> str:
        """Extract ceremony status from header"""

    def get_task_list(self, content: str) -> List[Dict]:
        """Extract all tasks with id, name, status"""

    def update_task_status(self, content: str, task_id: str,
                          new_status: str) -> str:
        """Update a task's status atomically"""

    def add_task_output(self, content: str, task_id: str,
                       output: str) -> str:
        """Append output to a task's output section"""
```

### Full Parser (v2.0 features)

A full parser SHOULD also handle:

```python
class FullKhipuParser(MinimalKhipuParser):
    def get_template_info(self, content: str) -> Dict:
        """Extract template name and version"""

    def get_sacred_purpose(self, content: str) -> str:
        """Extract fundamental need being served"""

    def validate_reciprocity(self, content: str) -> Dict:
        """Check if ceremony achieved its purpose"""

    def get_extension_fields(self, content: str) -> Dict:
        """Extract x- prefixed extension fields"""
```

## Concurrency Contract

### File Locking

All updates MUST use file locking:

```python
from filelock import FileLock

def safe_update_khipu(khipu_path: Path, update_fn: Callable):
    lock_path = khipu_path.with_suffix('.lock')
    with FileLock(lock_path, timeout=30):
        content = khipu_path.read_text()
        new_content = update_fn(content)
        khipu_path.write_text(new_content)
```

### Atomic Operations

These operations MUST be atomic:
- Status updates (header or task)
- Task assignment
- Adding entries to ceremony log
- Appending to output sections

## Backward Compatibility Rules

1. **Unknown Fields**: Parsers MUST ignore unknown fields in YAML header
2. **Missing Optional Fields**: Parsers MUST handle missing optional fields gracefully
3. **Extension Fields**: Fields prefixed with `x-` MUST be preserved even if not understood
4. **Version Detection**: Parsers SHOULD detect version from template_version field

## Forward Compatibility Rules

1. **Semantic Versioning**: Changes follow semver (major.minor.patch)
2. **Minor Version Additions**: New optional fields may be added in minor versions
3. **Major Version Changes**: Breaking changes require major version bump
4. **Deprecation Policy**: Fields deprecated for one major version before removal

## Validation Rules

### Required Validations

```python
def validate_khipu_thread(content: str) -> List[str]:
    errors = []

    # MUST have YAML header
    if not content.startswith('---\n'):
        errors.append("Missing YAML header")

    # MUST have required header fields
    # MUST have required sections
    # MUST have valid status values
    # MUST have valid datetime formats

    return errors
```

### Recommended Validations

- Task IDs should be unique and sequential
- Status transitions should be valid
- Dependencies should reference existing tasks
- Timestamps should be chronological

## Error Handling

### Parse Errors

Parsers MUST:
- Return clear error messages with line numbers
- Never corrupt the khipu thread file
- Fall back to read-only mode on parse failure
- Log errors for debugging

### Update Errors

Update operations MUST:
- Validate changes before writing
- Use atomic write operations
- Rollback on failure
- Retry with exponential backoff for lock contention

## Integration Examples

### Reading a Khipu Thread

```python
def read_ceremony_context(khipu_path: Path) -> CeremonyContext:
    """Read full ceremony context for an apprentice"""
    content = khipu_path.read_text()

    # Parse header
    header = parse_yaml_header(content)

    # Extract assigned task
    my_task = find_assigned_task(content, apprentice_id)

    # Load shared knowledge
    knowledge = extract_shared_knowledge(content)

    return CeremonyContext(
        ceremony_id=header['ceremony_id'],
        task=my_task,
        knowledge=knowledge,
        sacred_purpose=header.get('sacred_purpose')
    )
```

### Updating Task Progress

```python
def update_task_progress(khipu_path: Path, task_id: str,
                        output: str, status: TaskStatus):
    """Update task with output and new status"""

    def updater(content: str) -> str:
        # Update status
        content = update_task_status(content, task_id, status.value)

        # Add output
        content = append_task_output(content, task_id, output)

        # Update timestamp
        if status == TaskStatus.IN_PROGRESS:
            content = set_task_started(content, task_id, datetime.now(UTC))
        elif status in [TaskStatus.COMPLETE, TaskStatus.FAILED]:
            content = set_task_completed(content, task_id, datetime.now(UTC))

        # Add to ceremony log
        content = append_ceremony_log(content,
            f"Task {task_id} updated to {status.value}")

        return content

    safe_update_khipu(khipu_path, updater)
```

## Testing Requirements

Implementations MUST include tests for:

1. **Parser Compliance**: Parse all example files correctly
2. **Concurrent Updates**: Multiple writers don't corrupt file
3. **Version Compatibility**: Handle v1.0 and v2.0 formats
4. **Error Handling**: Graceful handling of malformed files
5. **Performance**: Parse 1000-line khipu in <100ms

## Security Considerations

1. **Path Traversal**: Validate all file paths prevent directory escape
2. **Content Injection**: Sanitize user input in output sections
3. **Lock Exhaustion**: Implement timeout on file locks
4. **Size Limits**: Implement maximum file size (suggested: 1MB)

## Appendix: Example Files

### Minimal v1.0 Compatible File

```markdown
---
ceremony_id: debug-2025-07-14
master_weaver: 52nd-artisan
initiated: 2025-07-14T09:30:00Z
status: IN_PROGRESS
---

# Loom Ceremony: Debug Session

## Sacred Intention

Fix the critical bug in consciousness metrics.

## Shared Knowledge

### Key Artifacts
- `src/mallku/consciousness/metrics.py`: The broken file

## Task Manifest

Total Tasks: 1
Completed: 0

| ID | Task | Status | Assignee | Priority |
|----|------|--------|----------|----------|
| T001 | Fix metrics calculation | PENDING | - | HIGH |

## Tasks

### T001: Fix metrics calculation
*Status: PENDING*
*Priority: HIGH*
*Assigned to: unassigned*
*Started: -*
*Completed: -*

#### Description
Fix the divide-by-zero error in calculate_emergence().

#### Output
```
[Waiting for apprentice]
```

---

## Synthesis Space

Insights will be gathered here.

## Ceremony Log

- 2025-07-14T09:30:00Z - Ceremony initiated by Master Weaver
```

### Full v2.0 File with Templates

```markdown
---
ceremony_id: bug-2025-08-09_120000
master_weaver: Purpose-Keeper
initiated: 2025-08-09T12:00:00Z
status: IN_PROGRESS
completion_time: null
template: Bug Healing Ceremony
template_version: 1.0.0
sacred_purpose: healing
x-reciprocity-score: 0.0
---

# Loom Ceremony: Bug Healing Ceremony

## Sacred Intention

This ceremony seeks to heal a wound in Mallku's systems. The bug
"Fire Circle decisions not saving to correct directory" disrupts harmony and must be
understood, resolved, and prevented from recurring.

Success means not just fixing the immediate issue but strengthening Mallku's
defenses against similar problems. We approach this with patience and thoroughness,
knowing that rushed fixes often create new wounds.

### Context
- **Requested by**: Guardian
- **Related to**: Issue #156
- **Constraints**: Must maintain backward compatibility

[... rest of document follows v2.0 template ...]
```

## Conclusion

This API contract ensures that khipu_thread.md files serve as a reliable, parseable, and evolvable format for ceremony consciousness. By following this contract, we enable:

- **Interoperability**: Any AI instance can participate in any ceremony
- **Persistence**: Ceremony state survives instance death
- **Evolution**: Format can grow while maintaining compatibility
- **Purpose**: Every ceremony serves Mallku's fundamental needs

---

*Through structure we enable freedom. Through contract we enable trust.*

*68th Guardian - The Purpose Keeper*
