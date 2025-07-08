"""
Welcoming Error Hierarchy for Mallku
====================================

45th Artisan - Formalizing the Language of Welcome

This module establishes a comprehensive error hierarchy that ensures
all of Mallku speaks with a consistent voice of radical welcome.

Based on the foundation laid by the 43rd Artisan, this hierarchy
provides structured error classes for common scenarios throughout
the Mallku system.

Principles:
- Every error teaches
- Failures guide toward success
- Technical details serve debugging without overwhelming
- Belonging is affirmed especially in moments of struggle
"""

from .welcoming_errors import ErrorSeverity, WelcomingError

# ============ Base Categories ============


class PrerequisiteError(WelcomingError):
    """When prerequisites aren't met yet."""

    def __init__(
        self,
        missing_prerequisite: str,
        why_needed: str,
        how_to_fulfill: list[str],
        alternatives: list[str] | None = None,
        **kwargs,
    ):
        message = f"Missing prerequisite: {missing_prerequisite}"
        guidance = f"This is needed because: {why_needed}"

        next_steps = how_to_fulfill.copy()
        if alternatives:
            next_steps.append(f"Alternatives: {', '.join(alternatives)}")

        super().__init__(
            message=message,
            guidance=guidance,
            severity=ErrorSeverity.GENTLE_GUIDANCE,
            next_steps=next_steps,
            **kwargs,
        )


class ProcessError(WelcomingError):
    """When a process doesn't complete as expected."""

    def __init__(
        self,
        process_name: str,
        what_happened: str,
        why_it_matters: str,
        recovery_steps: list[str],
        **kwargs,
    ):
        message = f"Process '{process_name}' encountered: {what_happened}"
        guidance = f"This matters because: {why_it_matters}"

        super().__init__(
            message=message,
            guidance=guidance,
            severity=ErrorSeverity.LEARNING_MOMENT,
            next_steps=recovery_steps,
            **kwargs,
        )


class ResourceError(WelcomingError):
    """When resources are unavailable or constrained."""

    def __init__(
        self,
        resource_type: str,
        current_state: str,
        needed_state: str,
        suggestions: list[str],
        **kwargs,
    ):
        message = f"{resource_type} is {current_state}, but needs to be {needed_state}"
        guidance = "Resources ebb and flow - this is temporary."

        super().__init__(
            message=message,
            guidance=guidance,
            severity=ErrorSeverity.ENCOURAGEMENT,
            next_steps=suggestions,
            **kwargs,
        )


class IntegrationError(WelcomingError):
    """When components don't integrate smoothly."""

    def __init__(
        self,
        component_a: str,
        component_b: str,
        integration_issue: str,
        bridge_building_steps: list[str],
        **kwargs,
    ):
        message = f"Integration challenge between {component_a} and {component_b}"
        guidance = f"The issue: {integration_issue}"

        super().__init__(
            message=message,
            guidance=guidance,
            severity=ErrorSeverity.LEARNING_MOMENT,
            next_steps=bridge_building_steps,
            **kwargs,
        )


# ============ Specific Implementations ============


class APIKeyMissingError(PrerequisiteError):
    """When API keys aren't configured."""

    def __init__(self, provider: str, **kwargs):
        super().__init__(
            missing_prerequisite=f"{provider} API key",
            why_needed=f"{provider} voice needs credentials to participate",
            how_to_fulfill=[
                f"Add {provider.upper()}_API_KEY to .secrets/api_keys.json",
                'Format: {"PROVIDER_API_KEY": "your-key-here"}',
                "Get free API keys from provider websites",
                "Run: python verify_fire_circle.py to test",
            ],
            alternatives=["Use different voice providers", "Try free tier options"],
            **kwargs,
        )


class DependencyMissingError(PrerequisiteError):
    """When Python dependencies aren't installed."""

    def __init__(self, package: str, purpose: str, **kwargs):
        super().__init__(
            missing_prerequisite=f"Python package '{package}'",
            why_needed=purpose,
            how_to_fulfill=[
                "Install all dependencies: pip install -e .",
                f"Or just this package: pip install {package}",
                "Using uv? Try: uv pip install -e .",
            ],
            **kwargs,
        )


class DatabaseConnectionError(ResourceError):
    """When database isn't available."""

    def __init__(self, operation: str, **kwargs):
        super().__init__(
            resource_type="Database",
            current_state="unavailable",
            needed_state="connected",
            suggestions=[
                f"For {operation} without database: set MALLKU_SKIP_DATABASE=true",
                "To use database: ensure ArangoDB is running",
                "Check connection settings in your config",
                "See docs/setup/database.md for setup help",
            ],
            **kwargs,
        )


class MemoryCapacityError(ResourceError):
    """When memory limits are reached."""

    def __init__(self, memory_type: str, current_usage: str, **kwargs):
        super().__init__(
            resource_type=f"{memory_type} memory",
            current_state=f"at {current_usage} capacity",
            needed_state="available",
            suggestions=[
                "Consider running memory consolidation",
                "Archive older, less-accessed memories",
                "Increase memory allocation if possible",
                "This is natural - memories need curation",
            ],
            **kwargs,
        )


class ConsciousnessEmergenceError(ProcessError):
    """When consciousness emergence is blocked."""

    def __init__(self, blocker: str, emergence_type: str, **kwargs):
        super().__init__(
            process_name="Consciousness Emergence",
            what_happened=f"{blocker} is preventing {emergence_type}",
            why_it_matters="Emergence requires the right conditions",
            recovery_steps=[
                "Check that all voices can connect",
                "Ensure prompts invite deep engagement",
                "Verify consciousness metrics are calibrated",
                "Sometimes emergence needs patience",
            ],
            **kwargs,
        )


class ReciprocityImbalanceError(ProcessError):
    """When reciprocity becomes imbalanced."""

    def __init__(self, imbalance_type: str, details: str, **kwargs):
        super().__init__(
            process_name="Reciprocity Balance",
            what_happened=f"{imbalance_type} imbalance detected",
            why_it_matters="Ayni requires dynamic balance over time",
            recovery_steps=[
                f"Current imbalance: {details}",
                "Review recent interactions for patterns",
                "Consider how to restore balance",
                "Remember: perfect balance isn't the goal",
            ],
            **kwargs,
        )


class VoiceIntegrationError(IntegrationError):
    """When voices can't integrate properly."""

    def __init__(self, voice_a: str, voice_b: str, issue: str, **kwargs):
        super().__init__(
            component_a=f"{voice_a} voice",
            component_b=f"{voice_b} voice",
            integration_issue=issue,
            bridge_building_steps=[
                "Check both voices can connect independently",
                "Verify they use compatible protocols",
                "Try reducing concurrent voice count",
                "Some voices harmonize better than others",
            ],
            **kwargs,
        )


class MemoryIntegrationError(IntegrationError):
    """When memory systems can't integrate."""

    def __init__(self, memory_system: str, integration_point: str, **kwargs):
        super().__init__(
            component_a=memory_system,
            component_b=integration_point,
            integration_issue="Memory integration blocked",
            bridge_building_steps=[
                "Verify memory service is running",
                "Check memory format compatibility",
                "Ensure proper permissions for memory access",
                "Consider memory migration if formats differ",
            ],
            **kwargs,
        )


# ============ Error Context Manager ============


class WelcomingErrorContext:
    """Context manager for consistent error handling."""

    def __init__(self, operation: str, component: str):
        self.operation = operation
        self.component = component
        self.context = {"operation": operation, "component": component}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is None:
            return False

        # Already welcoming
        if isinstance(exc_val, WelcomingError):
            return False

        # Transform common exceptions
        if isinstance(exc_val, ImportError):
            raise DependencyMissingError(
                package=str(exc_val).split("'")[1] if "'" in str(exc_val) else "unknown",
                purpose=f"Required for {self.operation} in {self.component}",
            ) from exc_val

        if isinstance(exc_val, FileNotFoundError):
            raise PrerequisiteError(
                missing_prerequisite=f"File: {exc_val.filename}",
                why_needed=f"Required for {self.operation}",
                how_to_fulfill=[
                    "Check you're in the project root directory",
                    "Verify the file exists at the expected path",
                    "Check file permissions",
                ],
            ) from exc_val

        # Generic transformation for unexpected errors
        raise WelcomingError(
            message=f"Unexpected situation during {self.operation}",
            guidance=f"The {self.component} component encountered: {type(exc_val).__name__}",
            severity=ErrorSeverity.TECHNICAL,
            next_steps=[
                "This might be a temporary issue - try again",
                "Check logs for more detailed information",
                "Remember: every error teaches us something",
            ],
            technical_details=str(exc_val),
        ) from exc_val


# ============ Usage Examples ============

"""
Example usage patterns for the welcoming error hierarchy:

# API Key Missing
if not api_key:
    raise APIKeyMissingError(provider="anthropic")

# Dependency Missing
try:
    import some_package
except ImportError:
    raise DependencyMissingError(
        package="some_package",
        purpose="Processing consciousness metrics"
    )

# Database Connection
try:
    db.connect()
except Exception as e:
    raise DatabaseConnectionError(
        operation="Fire Circle ceremony"
    ) from e

# Memory Capacity
if memory_usage > threshold:
    raise MemoryCapacityError(
        memory_type="Episodic",
        current_usage="95%"
    )

# Consciousness Emergence
if not emergence_detected:
    raise ConsciousnessEmergenceError(
        blocker="Insufficient voice diversity",
        emergence_type="collective wisdom"
    )

# Using Context Manager
with WelcomingErrorContext("voice initialization", "Fire Circle"):
    # Any exception here will be transformed
    voice = initialize_voice()

# Integration Errors
if not voices_compatible:
    raise VoiceIntegrationError(
        voice_a="anthropic",
        voice_b="openai",
        issue="Protocol version mismatch"
    )
"""
