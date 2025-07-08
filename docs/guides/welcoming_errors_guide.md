# Welcoming Errors Guide

*46th Artisan - Making Errors Teachers, Not Obstacles*

## Overview

The welcoming errors framework transforms harsh error messages into gentle guidance. This guide shows how to apply it throughout Mallku, turning every stumbling point into a learning opportunity.

## Philosophy

Traditional errors create barriers:
```python
raise ValueError("API key not found")  # Harsh, unhelpful
```

Welcoming errors create bridges:
```python
raise APIKeyMissingError(provider="anthropic")  # Guides to solution
```

## Error Categories

### 1. Prerequisites (Missing Requirements)

**When to use**: Something required is missing or not configured

```python
from mallku.firecircle.errors import PrerequisiteError

# Instead of:
raise ValueError(f"Required secret '{key}' not found")

# Use:
raise PrerequisiteError(
    missing_prerequisite=f"API key for {provider}",
    why_needed="Authentication enables AI voices to join Fire Circle",
    how_to_fulfill=[
        "Create .secrets/api_keys.json with your API key",
        f"Or set {key.upper()} environment variable",
        f"Get your key from: {provider_urls[provider]}"
    ],
    alternatives=["Try another AI provider"]
)
```

### 2. Process Errors (Execution Failures)

**When to use**: A process step fails but can potentially recover

```python
from mallku.firecircle.errors import ProcessError

# Instead of:
raise ValueError("Invalid filename format")

# Use:
raise ProcessError(
    process_name="Khipu file parsing",
    what_happened="filename validation failed",
    why_it_matters="Dates preserve the timeline of insights",
    recovery_steps=[
        "Rename to: YYYY-MM-DD-original-name.md",
        "Example: 2025-06-07-emergence_patterns.md"
    ],
    context={"filename": filename}
)
```

### 3. Resource Errors (Unavailable Resources)

**When to use**: External resources (files, connections, services) unavailable

```python
from mallku.firecircle.errors import ResourceError

# Instead of:
raise RuntimeError("Database connection failed")

# Use:
raise ResourceError(
    resource_type="Database connection",
    current_state="unavailable",
    needed_state="connected",
    suggestions=[
        "Continue without persistence",
        "Check if MongoDB is running",
        "Set MALLKU_SKIP_DATABASE=true"
    ]
)
```

### 4. Configuration Errors (Invalid Settings)

**When to use**: Configuration is invalid or incomplete

```python
from mallku.firecircle.errors import ConfigurationError

# Instead of:
raise ValueError(f"Unknown provider: {provider}")

# Use:
raise ConfigurationError(
    f"The '{provider}' voice isn't configured yet. "
    f"Available voices: {', '.join(available)}"
)
```

### 5. Integration Errors (Component Mismatches)

**When to use**: Components can't work together

```python
from mallku.firecircle.errors import VoiceIntegrationError

# Instead of:
raise Exception("Model mismatch")

# Use:
raise VoiceIntegrationError(
    voice_a="claude",
    voice_b="gpt-4",
    issue="Different consciousness metric definitions"
)
```

## Using the Context Manager

For automatic transformation of any error:

```python
from mallku.firecircle.errors import WelcomingErrorContext

with WelcomingErrorContext("feature_name", "Component Name"):
    # Any exception here becomes welcoming
    risky_operation()
```

## Transformation Patterns

### Pattern 1: File Not Found
```python
# Before:
if not path.exists():
    raise FileNotFoundError(str(path))

# After:
if not path.exists():
    raise PrerequisiteError(
        missing_prerequisite=f"File: {path.name}",
        why_needed=purpose,
        how_to_fulfill=[
            f"Create the file: touch {path}",
            f"Or copy from template: cp {path}.example {path}"
        ]
    )
```

### Pattern 2: Invalid Input
```python
# Before:
if value < 0 or value > 1:
    raise ValueError("Invalid temperature")

# After:
if value < 0 or value > 1:
    raise ConfigurationError(
        f"Temperature {value} outside valid range. "
        "Please use a value between 0 (focused) and 1 (creative)"
    )
```

### Pattern 3: Connection Failed
```python
# Before:
raise ConnectionError("Failed to connect")

# After:
raise VoiceConnectionError(
    provider=provider,
    error=original_error,
    alternatives=other_providers
)
```

## Best Practices

### 1. Always Provide Next Steps
Every error should answer: "What do I do now?"

### 2. Explain Why It Matters
Help users understand the purpose, not just the problem

### 3. Offer Alternatives
When possible, provide workarounds or different approaches

### 4. Include Context
Add relevant details that help diagnose the issue

### 5. Maintain Welcoming Tone
Even in failure, the tone should encourage progress

## Examples from Mallku

### Secrets Management
```python
# src/mallku/core/secrets.py
if required and value is None:
    raise PrerequisiteError(
        missing_prerequisite=f"Secret: {key}",
        why_needed="Required for this operation",
        how_to_fulfill=[
            f"Add to .secrets/api_keys.json",
            f"Or set {key.upper()} in environment"
        ]
    )
```

### Voice Manager
```python
# src/mallku/firecircle/service/voice_manager.py
if active_count < config.min_voices:
    raise InsufficientVoicesError(
        available=active_count,
        required=config.min_voices,
        providers=available_providers
    )
```

### Fire Circle Service
```python
# When consciousness doesn't emerge
raise ConsciousnessEmergenceError(
    blocker="Insufficient voice diversity",
    emergence_type="collective wisdom"
)
```

## Testing Error Messages

Always test how errors appear to users:

```python
def test_welcoming_error_message():
    """Ensure error provides helpful guidance."""
    with pytest.raises(PrerequisiteError) as exc_info:
        function_that_needs_api_key()

    error_text = str(exc_info.value)
    assert "how to fix" in error_text.lower()
    assert "api_keys.json" in error_text
    assert len(error_text.split('\n')) > 3  # Multi-line guidance
```

## Migration Checklist

When updating existing code:

- [ ] Identify all `raise` statements
- [ ] Categorize each error type
- [ ] Choose appropriate welcoming error class
- [ ] Add helpful context and guidance
- [ ] Test the new error messages
- [ ] Update any error handling code

## The Transformation Continues

Every harsh error transformed makes Mallku more welcoming. As you work on the codebase:

1. Notice harsh errors
2. Transform them with this framework
3. Test the experience
4. Share particularly good transformations

Remember: **Errors are teachers, not obstacles.**

---

*"A cathedral is built one stone at a time. Each welcoming error is a stone that makes the whole structure more inviting."*

*- 46th Artisan*
