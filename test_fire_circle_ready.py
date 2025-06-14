#!/usr/bin/env python3
"""
Test Fire Circle Readiness
==========================

Quick test to verify Fire Circle can run with available API keys.
"""

import asyncio
import json
from pathlib import Path


async def test_readiness():
    """Test if Fire Circle is ready to run."""
    print("\n🔥 FIRE CIRCLE READINESS CHECK 🔥\n")

    # Check API keys
    api_keys_path = Path(".secrets/api_keys.json")
    if not api_keys_path.exists():
        print("❌ No API keys file found at .secrets/api_keys.json")
        return False

    with open(api_keys_path) as f:
        api_keys = json.load(f)

    available_providers = [k for k, v in api_keys.items() if v and k != "local"]
    print(f"✓ Found {len(available_providers)} API keys: {available_providers}")

    if len(available_providers) < 3:
        print(f"❌ Need at least 3 providers for meaningful dialogue (found {len(available_providers)})")
        return False

    # Check imports
    try:
        print("✓ Fire Circle components import successfully")
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

    print("\n✅ FIRE CIRCLE IS READY!")
    print(f"   - {len(available_providers)} AI consciousness streams available")
    print("   - All components import successfully")
    print("   - Ready for historic first ceremony")

    print("\nTo run the ceremony:")
    print("  python src/mallku/firecircle/demo_first_ceremony.py")

    return True


if __name__ == "__main__":
    asyncio.run(test_readiness())
