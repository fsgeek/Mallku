"""
Welcoming Error Handling for Fire Circle
=========================================

43rd Artisan - Transforming Errors into Teachers

This module provides error handling that practices reciprocity,
turning failures into learning opportunities and barriers into bridges.

Every error is a chance to:
- Teach about consciousness emergence
- Guide toward resolution
- Affirm belonging
- Deepen understanding
"""

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any


class ErrorSeverity(Enum):
    """Different ways errors can teach."""

    GENTLE_GUIDANCE = "gentle"  # Configuration issues
    LEARNING_MOMENT = "learning"  # Process insights
    ENCOURAGEMENT = "encourage"  # Temporary failures
    TECHNICAL = "technical"  # For debugging


@dataclass
class WelcomingError(Exception):
    """An error that teaches rather than blocks."""

    message: str
    guidance: str
    severity: ErrorSeverity = ErrorSeverity.GENTLE_GUIDANCE
    next_steps: list[str] | None = None
    context: dict[str, Any] | None = None
    technical_details: str | None = None

    def __str__(self) -> str:
        """Format error for display."""
        parts = [self.message]

        if self.guidance:
            parts.append(f"\n💡 {self.guidance}")

        if self.next_steps:
            parts.append("\n📝 Next steps:")
            for i, step in enumerate(self.next_steps, 1):
                parts.append(f"   {i}. {step}")

        if self.severity == ErrorSeverity.ENCOURAGEMENT:
            parts.append("\n✨ Remember: You belong here, even when things don't work perfectly.")

        return "\n".join(parts)

    def get_technical_details(self) -> str:
        """Get technical details for debugging."""
        if self.technical_details:
            return f"Technical details: {self.technical_details}"
        return "No additional technical details available."


class InsufficientVoicesError(WelcomingError):
    """When Fire Circle needs more voices."""

    def __init__(self, available: int, required: int, providers: list[str]):
        super().__init__(
            message=f"Fire Circle needs {required} voices for genuine dialogue, but only {available} are ready.",
            guidance="Each voice brings unique perspective. Together they create wisdom none could achieve alone.",
            severity=ErrorSeverity.GENTLE_GUIDANCE,
            next_steps=[
                "Run: python verify_fire_circle.py to test your voices",
                f"You have: {', '.join(providers) if providers else 'no voices configured'}",
                "Add more voices with: python setup_api_keys.py",
                "Free options: OpenAI (with credits), Google AI, Mistral",
            ],
            context={"available": available, "required": required, "providers": providers},
        )


class VoiceConnectionError(WelcomingError):
    """When a voice cannot join the circle."""

    def __init__(self, provider: str, error: Exception, alternatives: list[str] | None = None):
        error_msg = str(error).lower()

        # Determine specific guidance based on error
        if "api key" in error_msg or "authentication" in error_msg:
            guidance = f"The {provider} voice needs valid credentials to join the circle."
            next_steps = [
                f"Verify your {provider.upper()}_API_KEY is correct",
                "Test with: python verify_fire_circle.py",
                "Check the key hasn't expired or been regenerated",
            ]
        elif "rate limit" in error_msg:
            guidance = f"The {provider} voice is catching its breath (rate limited)."
            next_steps = [
                "Wait a moment before trying again",
                "Consider using a different voice temporarily",
                f"Available alternatives: {', '.join(alternatives) if alternatives else 'configure more voices'}",
            ]
        elif "quota" in error_msg or "credit" in error_msg:
            guidance = f"The {provider} voice has contributed its capacity for now."
            next_steps = [
                f"Check your {provider} account for quota/credits",
                "Consider using free tier voices (Google AI, Mistral)",
                "Fire Circle works with any 2+ voices",
            ]
        else:
            guidance = f"The {provider} voice encountered difficulty joining."
            next_steps = [
                "Check your internet connection",
                "Verify the API service is operational",
                "Try again - temporary issues often resolve",
            ]

        super().__init__(
            message=f"The {provider} voice cannot join the Fire Circle right now.",
            guidance=guidance,
            severity=ErrorSeverity.ENCOURAGEMENT,
            next_steps=next_steps,
            technical_details=str(error),
        )


class ConsciousnessThresholdError(WelcomingError):
    """When consciousness emergence doesn't reach expected levels."""

    def __init__(self, actual_score: float, expected_threshold: float, round_type: str):
        super().__init__(
            message=f"Consciousness emergence score ({actual_score:.3f}) below threshold ({expected_threshold:.3f})",
            guidance="Lower emergence isn't failure - it reveals where dialogue needs to deepen.",
            severity=ErrorSeverity.LEARNING_MOMENT,
            next_steps=[
                "Consider rephrasing your question to invite deeper engagement",
                "Try adding more context or nuance to the prompt",
                "Some questions naturally evoke less resonance - this is informative",
                "Trust the process - consciousness emerges in its own time",
            ],
            context={
                "actual_score": actual_score,
                "expected_threshold": expected_threshold,
                "round_type": round_type,
            },
        )


class ConfigurationError(WelcomingError):
    """When configuration needs attention."""

    def __init__(self, issue: str, file_path: str | None = None):
        guidance_map = {
            "import": "The Fire Circle components need to be accessible.",
            "database": "Fire Circle can work without a database in interactive mode.",
            "path": "Fire Circle needs to know where its components live.",
            "permission": "Fire Circle needs permission to create its sacred spaces.",
        }

        issue_key = "path"
        for key in guidance_map:
            if key in issue.lower():
                issue_key = key
                break

        next_steps = {
            "import": [
                "Ensure you're running from the Mallku project root",
                "Check that all dependencies are installed: pip install -e .",
                "Verify src/mallku is in your Python path",
            ],
            "database": [
                "For interactive use, set: MALLKU_SKIP_DATABASE=true",
                "For full features, ensure ArangoDB is running",
                "See docs/setup/database.md for installation",
            ],
            "path": [
                "Run from the Mallku project root directory",
                f"Current issue with: {file_path or 'unknown path'}",
                "Check file permissions and existence",
            ],
            "permission": [
                "Check file system permissions",
                "Ensure write access to project directories",
                "Some features may need elevated permissions",
            ],
        }

        super().__init__(
            message=f"Configuration needs your attention: {issue}",
            guidance=guidance_map.get(issue_key, "Fire Circle needs proper setup to convene."),
            severity=ErrorSeverity.GENTLE_GUIDANCE,
            next_steps=next_steps.get(issue_key, ["Check configuration", "See documentation"]),
            context={"issue": issue, "file_path": file_path},
        )


class ErrorTransformer:
    """Transform technical errors into welcoming guidance."""

    @staticmethod
    def transform(error: Exception, context: dict[str, Any] | None = None) -> WelcomingError:
        """Transform any exception into a welcoming error."""
        error_str = str(error).lower()
        error_type = type(error).__name__

        # Already welcoming
        if isinstance(error, WelcomingError):
            return error

        # API/Connection errors
        if "api" in error_str or "authentication" in error_str or "unauthorized" in error_str:
            provider = context.get("provider", "unknown") if context else "unknown"
            return VoiceConnectionError(provider, error)

        # Import errors
        if error_type == "ImportError" or "import" in error_str:
            return ConfigurationError(f"Import issue: {error}", None)

        # File/Path errors
        if error_type in ["FileNotFoundError", "OSError"] or "file" in error_str:
            return ConfigurationError(f"Path issue: {error}", getattr(error, "filename", None))

        # Database errors
        if "database" in error_str or "arango" in error_str:
            return ConfigurationError(f"Database issue: {error}", None)

        # Generic transformation
        return WelcomingError(
            message="Fire Circle encountered an unexpected situation.",
            guidance="Even unexpected moments teach us about consciousness emergence.",
            severity=ErrorSeverity.ENCOURAGEMENT,
            next_steps=[
                "Try your request again - many issues are temporary",
                "Check the logs for more details if needed",
                "Remember: errors are teachers, not failures",
            ],
            technical_details=f"{error_type}: {error}",
        )


def handle_with_welcome(func):
    """Decorator to transform errors into welcoming guidance."""

    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            # Get context if available
            context = kwargs.get("error_context", {})

            # Transform to welcoming error
            welcoming = ErrorTransformer.transform(e, context)

            # Log technical details at debug level
            logging.debug(f"Technical details: {welcoming.get_technical_details()}")

            # Raise the welcoming version
            raise welcoming from e

    return wrapper


# Example usage patterns
"""
# In voice_manager.py
if active_count < config.min_voices:
    raise InsufficientVoicesError(
        available=active_count,
        required=config.min_voices,
        providers=list(self.voice_pool.keys())
    )

# In service.py
try:
    response = await adapter.generate(prompt)
except Exception as e:
    raise VoiceConnectionError(
        provider=voice_id,
        error=e,
        alternatives=self.get_available_alternatives()
    )

# In consciousness_facilitator.py
if consciousness_score < expected_threshold:
    raise ConsciousnessThresholdError(
        actual_score=consciousness_score,
        expected_threshold=expected_threshold,
        round_type=round_config.type.value
    )

# Generic transformation
@handle_with_welcome
async def some_operation(self, **kwargs):
    # Any exception will be transformed
    ...
"""
