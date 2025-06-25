#!/usr/bin/env python3
"""
Verify Fire Circle Installation
===============================

First step in your Fire Circle journey - verify everything is working.

This example:
- Checks that Fire Circle is properly installed
- Verifies API keys are configured
- Runs a minimal Fire Circle ceremony

Run with:
    PYTHONPATH=/path/to/Mallku/src python examples/fire_circle/00_setup/verify_installation.py

Or from project root:
    PYTHONPATH=src python examples/fire_circle/00_setup/verify_installation.py

Expected output:
    ✅ All checks passed - you're ready to explore Fire Circle!
"""

import asyncio
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)


def check_imports():
    """Check that all required imports work."""
    print("1️⃣ Checking imports...")

    try:
        from mallku.firecircle.load_api_keys import load_api_keys_to_environment  # noqa: F401
        from mallku.firecircle.service import FireCircleService  # noqa: F401

        print("   ✓ Fire Circle imports successful")
        return True
    except ImportError as e:
        print(f"   ✗ Import error: {e}")
        print("   Please ensure PYTHONPATH is set correctly")
        print("   Try: PYTHONPATH=src python examples/fire_circle/00_setup/verify_installation.py")
        return False


def check_api_keys():
    """Check that API keys are available."""
    print("\n2️⃣ Checking API keys...")

    # Change to project root for API key loading
    import os
    from pathlib import Path

    from mallku.firecircle.load_api_keys import (
        get_available_providers,
        load_api_keys_to_environment,
    )

    original_dir = os.getcwd()
    project_root = Path(__file__).parent.parent.parent.parent
    os.chdir(project_root)

    try:
        if not load_api_keys_to_environment():
            print("   ✗ No API keys found")
            print("   Please ensure .secrets/api_keys.json exists")
            return False
    finally:
        os.chdir(original_dir)

    providers = get_available_providers()
    if len(providers) < 2:
        print(f"   ⚠️  Only {len(providers)} provider(s) available")
        print("   Fire Circle works best with at least 2 voices")
        return False

    print(f"   ✓ Found {len(providers)} providers: {', '.join(providers)}")
    return True


async def check_basic_ceremony():
    """Run a minimal Fire Circle ceremony."""
    print("\n3️⃣ Running minimal Fire Circle ceremony...")

    from mallku.firecircle.service import (
        CircleConfig,
        FireCircleService,
        RoundConfig,
        RoundType,
        VoiceConfig,
    )

    try:
        # Create service
        service = FireCircleService()

        # Minimal configuration
        config = CircleConfig(
            name="Installation Test",
            purpose="Verify Fire Circle installation",
            min_voices=2,
            max_voices=2,
        )

        # Two voices for basic test
        voices = [
            VoiceConfig(
                provider="anthropic",
                model="claude-3-5-sonnet-20241022",
                role="verifier_1",
                quality="installation verification",
            ),
            VoiceConfig(
                provider="openai",
                model="gpt-4o",
                role="verifier_2",
                quality="installation verification",
            ),
        ]

        # Single verification round
        rounds = [
            RoundConfig(
                type=RoundType.OPENING,
                prompt="Respond with 'Fire Circle verified!' to confirm you can participate.",
                duration_per_voice=10,
            )
        ]

        # Convene ceremony
        result = await service.convene(config=config, voices=voices, rounds=rounds)

        # Check results
        if result.voice_count >= 2 and result.rounds_completed:
            print("   ✓ Fire Circle ceremony completed successfully")
            print(f"   ✓ {result.voice_count} voices participated")
            return True
        else:
            print("   ✗ Ceremony did not complete as expected")
            return False

    except Exception as e:
        print(f"   ✗ Error during ceremony: {type(e).__name__}: {e}")
        return False


async def main():
    """Run all verification checks."""
    print("🔥 Fire Circle Installation Verification")
    print("=" * 50)
    print("Checking your Mallku Fire Circle setup...\n")

    # Run checks
    imports_ok = check_imports()
    if not imports_ok:
        print("\n❌ Installation incomplete - please check your setup")
        return

    keys_ok = check_api_keys()
    if not keys_ok:
        print("\n❌ API keys missing - please configure .secrets/api_keys.json")
        return

    ceremony_ok = await check_basic_ceremony()

    # Summary
    print("\n" + "=" * 50)
    if imports_ok and keys_ok and ceremony_ok:
        print("✅ All checks passed - you're ready to explore Fire Circle!")
        print("\nNext steps:")
        print("  • Try examples/fire_circle/01_basic_ceremonies/simple_dialogue.py")
        print("  • Explore consciousness emergence patterns")
        print("  • Create your own ceremonies")
    else:
        print("❌ Some checks failed - please resolve issues above")


if __name__ == "__main__":
    asyncio.run(main())
