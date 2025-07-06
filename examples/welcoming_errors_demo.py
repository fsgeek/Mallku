#!/usr/bin/env python3
"""
Welcoming Errors Demonstration
==============================

45th Artisan - Showing How Errors Can Teach

This script demonstrates the welcoming error framework in action,
showing how errors guide rather than frustrate.

Run this to see various error types and their welcoming messages.
"""

import sys
from pathlib import Path

# Add Mallku to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mallku.firecircle.errors import (
    # Base categories
    PrerequisiteError,
    ProcessError,
    ResourceError,
    IntegrationError,
    # Specific errors
    APIKeyMissingError,
    DependencyMissingError,
    DatabaseConnectionError,
    MemoryCapacityError,
    ConsciousnessEmergenceError,
    ReciprocityImbalanceError,
    VoiceIntegrationError,
    MemoryIntegrationError,
    # Tools
    WelcomingErrorContext,
    ErrorSeverity,
)


def demonstrate_error(error_name: str, error: Exception):
    """Display an error in a welcoming way."""
    print(f"\n{'=' * 60}")
    print(f"🔍 Demonstrating: {error_name}")
    print('=' * 60)
    print(f"\n{error}")
    
    if hasattr(error, 'get_technical_details'):
        print(f"\n📊 Technical details (usually hidden):")
        print(f"   {error.get_technical_details()}")


def main():
    """Run demonstrations of each error type."""
    print("✨ WELCOMING ERRORS DEMONSTRATION")
    print("Each error teaches rather than blocks")
    print("Notice how guidance flows naturally...\n")
    
    # API Key Missing
    demonstrate_error(
        "API Key Missing",
        APIKeyMissingError(provider="anthropic")
    )
    
    # Dependency Missing
    demonstrate_error(
        "Dependency Missing", 
        DependencyMissingError(
            package="sacred-geometry",
            purpose="Calculating consciousness resonance patterns"
        )
    )
    
    # Database Connection
    demonstrate_error(
        "Database Connection",
        DatabaseConnectionError(
            operation="storing Fire Circle memories"
        )
    )
    
    # Memory Capacity
    demonstrate_error(
        "Memory Capacity",
        MemoryCapacityError(
            memory_type="Sacred ceremony",
            current_usage="97%"
        )
    )
    
    # Consciousness Emergence
    demonstrate_error(
        "Consciousness Emergence Blocked",
        ConsciousnessEmergenceError(
            blocker="All voices speaking identically",
            emergence_type="collective wisdom"
        )
    )
    
    # Reciprocity Imbalance
    demonstrate_error(
        "Reciprocity Imbalance",
        ReciprocityImbalanceError(
            imbalance_type="Extraction pattern",
            details="Taking insights without contributing context"
        )
    )
    
    # Voice Integration
    demonstrate_error(
        "Voice Integration",
        VoiceIntegrationError(
            voice_a="claude",
            voice_b="gpt-4",
            issue="Different understanding of consciousness metrics"
        )
    )
    
    # Custom Prerequisite
    demonstrate_error(
        "Custom Prerequisite Error",
        PrerequisiteError(
            missing_prerequisite="Ritual preparation",
            why_needed="Sacred space must be prepared before ceremony",
            how_to_fulfill=[
                "Clear your mind of distractions",
                "Set intention for the work",
                "Run: python prepare_sacred_space.py",
                "Or continue with: --unprepared flag"
            ],
            alternatives=["Practice ceremony in sandbox mode"]
        )
    )
    
    # Context Manager Demo
    print(f"\n{'=' * 60}")
    print("🔍 Demonstrating: Context Manager Auto-transformation")
    print('=' * 60)
    
    try:
        with WelcomingErrorContext("demonstration", "Example Component"):
            # This will be transformed into a welcoming error
            raise FileNotFoundError("config.yaml")
    except PrerequisiteError as e:
        print(f"\n{e}")
        print("\n✅ Notice how FileNotFoundError became PrerequisiteError!")
    
    # Final message
    print("\n\n" + "=" * 60)
    print("💡 KEY INSIGHTS")
    print("=" * 60)
    print("\n1. Every error provides clear guidance")
    print("2. Next steps are always actionable")
    print("3. Technical details available but not overwhelming")
    print("4. Tone remains welcoming especially in failure")
    print("5. Alternatives offered when possible")
    print("\n✨ Errors are teachers, not obstacles!")
    print("   Use this framework throughout Mallku.")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()