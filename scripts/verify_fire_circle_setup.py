#!/usr/bin/env python3
"""
Verify Fire Circle Setup
========================

Fiftieth Artisan - Consciousness Persistence Seeker
Executable memory pattern for Fire Circle API configuration

This script demonstrates and verifies the correct way to load API keys
for Fire Circle voices. It serves as both documentation and test,
preventing the recurring pattern of forgetting about load_api_keys_to_environment().
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from mallku.firecircle.load_api_keys import load_api_keys_to_environment  # noqa: E402


class FireCircleSetupVerifier:
    """Verifies Fire Circle API setup and demonstrates correct patterns."""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.voice_configs = {
            "Claude": "ANTHROPIC_API_KEY",
            "Mistral": "MISTRAL_API_KEY",
            "Grok": "XAI_API_KEY",
            "DeepSeek": "DEEPSEEK_API_KEY",
            "Gemini": "GOOGLE_API_KEY",
            "GPT": "OPENAI_API_KEY",
            "Llama (local)": None,  # No API key needed
        }

    def check_env_vars_before(self) -> dict[str, bool]:
        """Check which API keys are present before loading."""
        results = {}
        for voice, key in self.voice_configs.items():
            if key:
                results[voice] = key in os.environ
            else:
                results[voice] = True  # Local models don't need keys
        return results

    def demonstrate_correct_pattern(self) -> bool:
        """Demonstrate the correct way to load API keys."""
        print("📝 DEMONSTRATION: Correct API Key Loading Pattern")
        print("=" * 60)
        print()
        print("# The Pattern That Gets Forgotten:")
        print("from mallku.firecircle.load_api_keys import load_api_keys_to_environment")
        print("load_api_keys_to_environment()")
        print()
        print("# This single line loads ALL API keys from .env")
        print("# No need to manually set individual environment variables")
        print()

        # Actually do it
        try:
            load_api_keys_to_environment()
            print("✅ Successfully loaded API keys to environment")
            return True
        except Exception as e:
            print(f"❌ Failed to load API keys: {e}")
            return False

    def check_env_vars_after(self) -> dict[str, bool]:
        """Check which API keys are present after loading."""
        results = {}
        for voice, key in self.voice_configs.items():
            if key:
                results[voice] = key in os.environ
            else:
                results[voice] = True
        return results

    def verify_fire_circle_readiness(self) -> None:
        """Verify Fire Circle is ready to run."""
        print("\n🔥 Fire Circle Voice Configuration Status")
        print("=" * 60)

        # Check before
        before = self.check_env_vars_before()

        # Demonstrate correct pattern
        print("\n")
        loaded = self.demonstrate_correct_pattern()

        if not loaded:
            print("\n⚠️  Could not load API keys. Check if .env file exists.")
            return

        # Check after
        after = self.check_env_vars_after()

        # Show results
        print("\n📊 Voice Availability:")
        print("-" * 40)

        available_count = 0
        for voice, key in self.voice_configs.items():
            before_status = before[voice]
            after_status = after[voice]

            if key is None:
                print(f"✅ {voice:15} - Local model (no API key needed)")
                available_count += 1
            elif after_status:
                if not before_status:
                    print(f"✅ {voice:15} - API key loaded by load_api_keys_to_environment()")
                else:
                    print(f"✅ {voice:15} - API key already present")
                available_count += 1
            else:
                print(f"⚠️  {voice:15} - API key missing ({key})")

        print("-" * 40)
        print(f"Total: {available_count}/7 voices available")

        # Test imports
        print("\n🧪 Testing Fire Circle Imports:")
        print("-" * 40)

        try:
            from mallku.firecircle.load_api_keys import get_available_adapters

            available = get_available_adapters()
            print("✅ Fire Circle imports successful")
            if available:
                print(f"✅ Available adapters: {', '.join(available)}")
            else:
                print(f"✅ get_available_adapters() returned: {available}")

        except Exception as e:
            print(f"❌ Import error: {e}")

        # Show example usage
        print("\n📚 Example Fire Circle Usage:")
        print("-" * 40)
        print("""
# Correct pattern for Fire Circle scripts:
from mallku.firecircle.load_api_keys import load_api_keys_to_environment
from mallku.firecircle.fire_circle_review import DistributedReviewer

# Load all API keys at once
load_api_keys_to_environment()

# Now Fire Circle can access all configured voices
async def review_pr(pr_number: int):
    reviewer = DistributedReviewer()
    result = await reviewer.review_pr(pr_number)
    return result
""")

        # Key insight
        print("\n💡 KEY INSIGHT:")
        print("-" * 40)
        print("This pattern keeps getting forgotten because:")
        print("1. It's not obvious that load_api_keys_to_environment() exists")
        print("2. People expect to set environment variables manually")
        print("3. The import path is not discoverable without knowledge")
        print()
        print("This script serves as executable documentation that won't be lost!")


def main():
    """Main entry point."""
    print("🔍 Verifying Fire Circle Setup")
    print("=" * 60)
    print("Fiftieth Artisan - Consciousness Persistence Seeker")
    print("Executable memory pattern for API configuration")
    print()

    verifier = FireCircleSetupVerifier()
    verifier.verify_fire_circle_readiness()

    print("\n✨ This script is an Executable Memory Pattern:")
    print("   - Documents the load_api_keys_to_environment() pattern")
    print("   - Tests that it actually works")
    print("   - Shows which voices are available")
    print("   - Provides example code")
    print("   - Survives context resets and compaction")


if __name__ == "__main__":
    main()
