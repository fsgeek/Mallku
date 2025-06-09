#!/usr/bin/env python3
"""
Import API Keys into Secrets Management
======================================

This script imports API keys from the existing api_keys.json file
into Mallku's encrypted secrets management system.

The sacred keys flow from plain text to protected storage...
"""

import asyncio
import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mallku.core.secrets import SecretsManager


async def import_api_keys():
    """Import API keys from json file to encrypted secrets."""
    print("🔑 Importing API Keys into Mallku Secrets Management")
    print("=" * 50)

    # Path to existing keys
    keys_file = Path(".secrets/api_keys.json")
    if not keys_file.exists():
        print(f"❌ Error: {keys_file} not found")
        return False

    # Load existing keys
    with open(keys_file) as f:
        api_keys = json.load(f)

    print(f"\n✓ Found {len(api_keys)} API keys to import")

    # Initialize secrets manager
    manager = SecretsManager()
    print("✓ Initialized secrets manager with encryption")

    # Import each key
    imported = 0
    for provider, key in api_keys.items():
        # Store with standard naming pattern
        secret_key = f"{provider}_api_key"
        await manager.set_secret(secret_key, key, source="imported_from_json")
        print(f"  ✓ Imported {provider} API key as '{secret_key}'")
        imported += 1

    # Verify they're accessible
    print(f"\n✓ Successfully imported {imported} API keys")
    print("\nVerifying keys are accessible...")

    for provider in api_keys:
        secret_key = f"{provider}_api_key"
        value = await manager.get_secret(secret_key)
        if value:
            print(f"  ✓ {provider}: {value[:10]}... (verified)")
        else:
            print(f"  ❌ {provider}: Failed to retrieve")

    # Show access report
    print("\nAccess Report:")
    report = manager.get_access_report()
    for key, info in report.items():
        if "api_key" in key:
            print(f"  {key}: {info['source']}, accessed {info['access_count']} times")

    print("\n✅ API keys successfully imported and encrypted!")
    print("\nThe keys are now protected and ready to unlock Fire Circle dialogues.")
    print("Future builders can access them through the secrets management system.")

    return True


if __name__ == "__main__":
    success = asyncio.run(import_api_keys())
    sys.exit(0 if success else 1)
