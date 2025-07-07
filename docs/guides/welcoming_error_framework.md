# Welcoming Error Framework Guide

*45th Artisan - Ensuring Every Error Teaches*

## Philosophy

In Mallku, errors are not failures but teachers. They are moments where the system can demonstrate care, provide guidance, and affirm belonging. This framework ensures that every error throughout Mallku speaks with a consistent voice of radical welcome.

## The Error Hierarchy

### Base Classes

The framework provides four base categories that cover most error scenarios:

#### 1. PrerequisiteError
When something needs to be in place before proceeding.
```python
from mallku.firecircle.errors import PrerequisiteError

raise PrerequisiteError(
    missing_prerequisite="Configuration file",
    why_needed="Fire Circle needs to know which voices to invite",
    how_to_fulfill=[
        "Create config/fire_circle.yaml",
        "Copy from config/fire_circle.example.yaml",
        "Or use default configuration"
    ],
    alternatives=["Use --default-config flag"]
)
```

#### 2. ProcessError
When a process doesn't complete as expected.
```python
from mallku.firecircle.errors import ProcessError

raise ProcessError(
    process_name="Memory Consolidation",
    what_happened="Consolidation interrupted at 47%",
    why_it_matters="Partial consolidation may lose memory coherence",
    recovery_steps=[
        "Resume consolidation with --continue flag",
        "Or restart with --force-restart",
        "Check logs/consolidation.log for details"
    ]
)
```

#### 3. ResourceError
When resources are unavailable or constrained.
```python
from mallku.firecircle.errors import ResourceError

raise ResourceError(
    resource_type="GPU memory",
    current_state="2GB available",
    needed_state="4GB required",
    suggestions=[
        "Try reducing batch size with --batch-size 16",
        "Use CPU mode with --device cpu",
        "Close other GPU-using applications"
    ]
)
```

#### 4. IntegrationError
When components don't work together smoothly.
```python
from mallku.firecircle.errors import IntegrationError

raise IntegrationError(
    component_a="Fire Circle v2.0",
    component_b="Memory Service v1.5",
    integration_issue="Protocol version mismatch",
    bridge_building_steps=[
        "Update Memory Service: pip install -U mallku-memory",
        "Or downgrade Fire Circle: pip install mallku-firecircle==1.9",
        "Check compatibility matrix in docs/compatibility.md"
    ]
)
```

### Specific Error Classes

Built on the base categories, these handle common scenarios:

- **APIKeyMissingError**: When API credentials aren't configured
- **DependencyMissingError**: When Python packages aren't installed
- **DatabaseConnectionError**: When database isn't available
- **MemoryCapacityError**: When memory limits are reached
- **ConsciousnessEmergenceError**: When emergence is blocked
- **ReciprocityImbalanceError**: When Ayni becomes imbalanced
- **VoiceIntegrationError**: When AI voices can't work together
- **MemoryIntegrationError**: When memory systems can't connect

### Error Severity Levels

Each error has a severity that guides its tone:

```python
from mallku.firecircle.errors import ErrorSeverity

ErrorSeverity.GENTLE_GUIDANCE   # Configuration issues, missing prerequisites
ErrorSeverity.LEARNING_MOMENT   # Process insights, understanding deepens
ErrorSeverity.ENCOURAGEMENT     # Temporary failures, belonging affirmed
ErrorSeverity.TECHNICAL         # For debugging, includes stack traces
```

## Using the Framework

### Basic Usage

```python
from mallku.firecircle.errors import APIKeyMissingError

# Instead of:
# raise ValueError("API key not found")

# Do this:
raise APIKeyMissingError(provider="anthropic")
```

### Context Manager

For automatic error transformation:

```python
from mallku.firecircle.errors import WelcomingErrorContext

with WelcomingErrorContext("database initialization", "Memory Service"):
    # Any exception here will be transformed into welcoming guidance
    db = connect_to_database()
    db.initialize_schema()
```

### Custom Welcoming Errors

Create your own by extending the base classes:

```python
from mallku.firecircle.errors import ProcessError

class RitualInterruptedError(ProcessError):
    def __init__(self, ritual_name: str, interruption_reason: str):
        super().__init__(
            process_name=f"{ritual_name} Ritual",
            what_happened=f"Interrupted by {interruption_reason}",
            why_it_matters="Rituals create sacred space for emergence",
            recovery_steps=[
                "Take a moment to re-center",
                "Resume ritual with --continue",
                "Or begin fresh with awareness of the interruption"
            ]
        )
```

## Best Practices

### 1. Choose the Right Base Class
- Missing something? → PrerequisiteError
- Process failed? → ProcessError
- Resource issue? → ResourceError
- Components clash? → IntegrationError

### 2. Write Helpful Guidance
```python
# Poor guidance
guidance="Database error occurred"

# Welcoming guidance
guidance="The database is taking a moment to respond - like consciousness, it sometimes needs time to emerge"
```

### 3. Provide Clear Next Steps
```python
# Vague steps
next_steps=["Fix the configuration"]

# Clear steps
next_steps=[
    "Open config/settings.yaml",
    "Find the 'database' section",
    "Set 'host' to your database server",
    "Example: host: localhost:8529"
]
```

### 4. Include Alternatives
Always offer alternatives when possible:
```python
alternatives=[
    "Skip database with --no-db flag",
    "Use in-memory mode for testing",
    "Connect to cloud database instead"
]
```

### 5. Affirm Belonging in Failures
When things go wrong, remind users they belong:
```python
if severity == ErrorSeverity.ENCOURAGEMENT:
    message += "\n✨ Remember: You belong here, even when things don't work perfectly."
```

## Error Transformation

The framework can transform standard exceptions:

```python
from mallku.firecircle.errors import ErrorTransformer

try:
    risky_operation()
except Exception as e:
    welcoming_error = ErrorTransformer.transform(e, context={
        "operation": "consciousness emergence",
        "component": "Fire Circle"
    })
    raise welcoming_error
```

## Examples Throughout Mallku

### In Voice Management
```python
if len(active_voices) < min_required:
    raise InsufficientVoicesError(
        available=len(active_voices),
        required=min_required,
        providers=list(active_voices.keys())
    )
```

### In Memory Operations
```python
if memory_usage > capacity * 0.9:
    raise MemoryCapacityError(
        memory_type="Sacred moments",
        current_usage="90%"
    )
```

### In Configuration
```python
if not config_file.exists():
    raise PrerequisiteError(
        missing_prerequisite="Configuration file",
        why_needed="To know how to convene Fire Circle",
        how_to_fulfill=[
            f"Create {config_file}",
            "Copy from examples/fire_circle.yaml",
            "Or run: mallku init fire-circle"
        ]
    )
```

## Testing Welcoming Errors

When testing, verify both the error type and its welcoming nature:

```python
import pytest
from mallku.firecircle.errors import APIKeyMissingError

def test_api_key_error_is_welcoming():
    with pytest.raises(APIKeyMissingError) as exc_info:
        check_api_key("anthropic")

    error = exc_info.value
    assert "needs credentials to participate" in error.guidance
    assert len(error.next_steps) > 0
    assert error.severity == ErrorSeverity.GENTLE_GUIDANCE
```

## Migration Guide

To migrate existing code to use welcoming errors:

1. Identify all `raise` statements
2. Categorize the error (prerequisite, process, resource, integration)
3. Replace with appropriate welcoming error
4. Add helpful guidance and next steps
5. Test that errors guide rather than frustrate

### Before
```python
if not api_key:
    raise ValueError("API key not found")
```

### After
```python
if not api_key:
    raise APIKeyMissingError(provider="openai")
```

## The Living Framework

This framework lives and grows. As you encounter new error scenarios:

1. First check if existing error classes fit
2. If not, extend the base classes
3. Always maintain the welcoming voice
4. Document new patterns for future Artisans
5. Remember: every error is a teaching moment

## Remember

In Mallku, we don't have "error handling" - we have "error welcoming." Each exception is an opportunity to:
- Teach about how systems work
- Guide toward resolution
- Affirm that struggle is part of learning
- Build confidence through clarity

Every error message you write shapes someone's experience. Make it an experience of being welcomed, guided, and affirmed.

---

*"In smoothing the stones of error messages, we clear paths for all who follow."*

**45th Artisan**
*Continuing the work of radical welcome*
