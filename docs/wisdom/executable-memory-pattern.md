# The Executable Memory Pattern

*Created by the Seventh Anthropologist*
*Date: 2025-07-16*

## The Discovery

While healing database security violations, I discovered a pattern that transcends this specific wound. It's about creating memory that survives context loss through executable enforcement.

## The Pattern

### 1. Executable Over Documentary

Documentation gets lost, ignored, or misunderstood. Executable patterns enforce themselves:

```python
# ❌ Documentation: "Please use get_secured_database()"
# (Gets ignored, forgotten, or lost in context switches)

# ✅ Executable: Make get_database() raise an error
def get_database(*args, **kwargs):
    raise DatabaseSecurityViolation("Use get_secured_database()")
```

### 2. Structure Over Discipline

Don't rely on human memory or discipline. Create structural barriers:

```python
# ❌ Export both options, trust developers to choose correctly
__all__ = ["get_database", "get_secured_database"]

# ✅ Only export the secure option
__all__ = ["get_secured_database"]  # No choice = no mistakes
```

### 3. Loud Failures Over Silent Drift

Make violations impossible to ignore:

```python
# ❌ Log a warning and continue
logger.warning("Using insecure database access")

# ✅ Raise an exception with clear guidance
raise DatabaseSecurityViolation(
    "Direct database access FORBIDDEN\n"
    "Use: get_secured_database()\n"
    "See: github.com/fsgeek/Mallku/issues/177"
)
```

### 4. Automated Guardians

Scripts and hooks that actively prevent violations:

```yaml
# Pre-commit hook that runs automatically
- id: database-security-check
  name: Database Security Check
  entry: python scripts/verify_database_security.py
  files: \.py$
```

## Why This Works

### Against Context Loss

When Claude instances experience compaction:
- Documentation is summarized away
- Nuance is lost
- But structural barriers remain

### Against Human Nature

- Can't use what doesn't exist
- Can't ignore loud failures
- Can't bypass automated checks

### Against Time

- Scripts encode understanding permanently
- Hooks enforce continuously
- Errors teach immediately

## Application Beyond Databases

This pattern applies to any architectural principle:

### Example: Ensuring Async Patterns

```python
# Instead of documenting "always use async"
def sync_function():
    raise NotImplementedError("Use async_function() instead")

# Force the pattern structurally
__all__ = ["async_function"]  # Only export async version
```

### Example: API Versioning

```python
# Instead of "please use v2"
@deprecated(raises=True)
def api_v1():
    raise DeprecationError("Use api_v2()")
```

## Creating Executable Memory

1. **Identify the Principle**: What must be preserved?
2. **Find the Confusion Point**: Where do mistakes happen?
3. **Remove the Wrong Option**: Make it structurally impossible
4. **Create Clear Errors**: Guide toward the right path
5. **Automate Enforcement**: Scripts, hooks, CI/CD
6. **Document the Pattern**: Not the rule, but the enforcement

## The Seventh Anthropologist's Insight

Living memory isn't about perfect recall - it's about creating structures that guide future instances toward right action even when context is lost.

The enemy isn't forgetfulness - it's optionality. When there's only one path, everyone takes it correctly.

## Fractal Application

This pattern appears at every level:

- **Code**: Remove deprecated functions entirely
- **Architecture**: Make insecure paths impossible
- **Process**: Automate what was manual
- **Culture**: Embed principles in tools

## The Ultimate Test

Can a completely new instance, with no context except error messages, still follow the architecture correctly? If yes, you've created true executable memory.

---

*"Make the right way the only way" - this is how cathedrals remember their principles across generations of builders.*
