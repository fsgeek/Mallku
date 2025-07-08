#!/usr/bin/env python3
"""
Transforming Harsh Errors Demo
==============================

46th Artisan - Continuing the Welcoming Journey

This script demonstrates how to transform harsh errors found throughout
Mallku into welcoming ones that teach rather than frustrate.

Shows before/after examples from real Mallku code.
"""

import sys
from pathlib import Path

# Add Mallku to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mallku.firecircle.errors import (
    PrerequisiteError,
    ProcessError,
    ResourceError,
    ConfigurationError,
    WelcomingError,
    WelcomingErrorContext,
)


def demonstrate_transformation(title: str, before: str, after: Exception):
    """Show the transformation from harsh to welcoming."""
    print(f"\n{'=' * 60}")
    print(f"🔄 {title}")
    print("=" * 60)
    print("\n❌ BEFORE (harsh):")
    print(f"   {before}")
    print("\n✅ AFTER (welcoming):")
    print(f"{after}")


def main():
    """Run demonstrations of error transformations."""
    print("🌟 TRANSFORMING HARSH ERRORS INTO WELCOMING TEACHERS")
    print("Each transformation shows how to guide rather than block")
    print("Notice how the tone shifts from frustration to support...\n")

    # From secrets.py line 168
    demonstrate_transformation(
        "Required Secret Not Found",
        "ValueError: Required secret 'anthropic_api_key' not found in any source",
        PrerequisiteError(
            missing_prerequisite="API key for Anthropic",
            why_needed="Anthropic's voice needs authentication to join the Fire Circle",
            how_to_fulfill=[
                "Create .secrets/api_keys.json with your Anthropic API key",
                "Or set ANTHROPIC_API_KEY environment variable",
                "Get your key from: https://console.anthropic.com/account/keys",
                "Example: {'anthropic_api_key': 'sk-ant-...'}"
            ],
            alternatives=["Try another AI provider like OpenAI or Google"]
        )
    )
    
    # From khipu/service.py line 55
    demonstrate_transformation(
        "Invalid Khipu Filename",
        'ValueError: Invalid filename format, expected YYYY-MM-DD-..: emergence_patterns',
        ProcessError(
            process_name="Khipu file parsing",
            what_happened="filename validation failed",
            why_it_matters="Khipu filenames encode the date for chronological ordering",
            recovery_steps=[
                "Rename the file to include date: YYYY-MM-DD-original-name.md",
                "Example: 2025-06-07-emergence_patterns.md",
                "This preserves the timeline of insights"
            ],
            context={"filename": "emergence_patterns", "expected_pattern": "YYYY-MM-DD-*"}
        )
    )
    
    # From adapter_factory.py line 112 (modified)
    demonstrate_transformation(
        "Database Connection Failed",
        'RuntimeError: Failed to connect to database: Connection refused',
        ResourceError(
            resource_type="Database connection",
            current_state="unavailable",
            needed_state="connected",
            suggestions=[
                "Continue without persistence (memories won't be saved)",
                "Check if MongoDB is running: sudo systemctl status mongod",
                "Start MongoDB: sudo systemctl start mongod",
                "Or set MALLKU_SKIP_DATABASE=true to proceed without storage"
            ]
        )
    )
    
    
    # From prompt/manager.py (ContractViolationError)
    demonstrate_transformation(
        "Prompt Contract Violation",
        "ContractViolationError: Contract violations: missing required field 'schema', insufficient examples",
        ProcessError(
            process_name="Prompt validation",
            what_happened="contract compliance check failed",
            why_it_matters="Contracts ensure LLM responses meet quality standards",
            recovery_steps=[
                "Add 'schema' field to your prompt context",
                "Include at least 2 examples (you provided 0)",
                "Example structure:",
                "  context = {",
                "    'schema': {'user': {'name': 'string', 'age': 'int'}},",
                "    'examples': [example1, example2]",
                "  }"
            ],
            context={"violations": ["missing 'schema'", "need 2 examples"]}
        )
    )
    
    # Generic file not found transformation
    demonstrate_transformation(
        "Configuration File Missing",
        'FileNotFoundError: config.yaml',
        PrerequisiteError(
            missing_prerequisite="Configuration file (config.yaml)",
            why_needed="Configuration defines how Mallku connects with AI voices",
            how_to_fulfill=[
                "Copy the example configuration:",
                "  cp config.example.yaml config.yaml",
                "Or create a minimal config.yaml:",
                "  echo 'voices: []' > config.yaml",
                "Then customize with your preferences"
            ],
            alternatives=["Use default configuration with --use-defaults flag"]
        )
    )
    
    # Show context manager in action
    print(f"\n{'=' * 60}")
    print("🔍 Context Manager Auto-transformation")
    print('=' * 60)
    print("\nThe WelcomingErrorContext can transform any error automatically:")
    
    try:
        with WelcomingErrorContext("configuration", "Settings Loader"):
            # Simulate a harsh error
            raise ValueError("Invalid setting: temperature must be between 0 and 1")
    except WelcomingError as e:
        print(f"\n{e}")
        print("\n✅ Notice how ValueError became a welcoming error!")
    
    # Design patterns
    print("\n\n" + "=" * 60)
    print("💡 TRANSFORMATION PATTERNS")
    print("=" * 60)
    print("\n1. Missing Prerequisites → PrerequisiteError")
    print("   - What's missing and why it's needed")
    print("   - Clear steps to fulfill")
    print("   - Alternatives when possible")

    print("\n2. Process Failures → ProcessError")
    print("   - Where in the process it failed")
    print("   - Why this step matters")
    print("   - Recovery steps to continue")
    
    print("\n3. Resource Issues → ResourceError")
    print("   - What resource is unavailable")
    print("   - What operation needs it")
    print("   - Alternatives or workarounds")
    
    print("\n4. Configuration Problems → ConfigurationError")
    print("   - What's misconfigured")
    print("   - Valid configuration examples")
    print("   - How to validate settings")

    print("\n✨ Remember: Every error is a teaching opportunity!")
    print("   Transform frustration into guidance throughout Mallku.")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
