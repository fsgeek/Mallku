#!/usr/bin/env python3
"""
API Key Setup Helper
====================

43rd Artisan - Making First Steps Welcoming

This script helps you set up your API keys for Fire Circle
in a gentle, guided way.

Run with:
    python setup_api_keys.py
"""

import os
import json
from pathlib import Path
import sys


def print_banner():
    """Welcome message."""
    print("\n" + "=" * 60)
    print("🔥 Fire Circle API Key Setup")
    print("=" * 60)
    print("\nWelcome! I'll help you set up API keys for Fire Circle.")
    print("This is your first step toward consciousness emergence.\n")


def ensure_secrets_directory():
    """Create .secrets directory if it doesn't exist."""
    secrets_dir = Path(".secrets")
    if not secrets_dir.exists():
        secrets_dir.mkdir()
        print("✅ Created .secrets directory")

        # Create .gitignore to ensure keys aren't committed
        gitignore = secrets_dir / ".gitignore"
        gitignore.write_text("*\n!.gitignore\n!api_keys_template.json\n")
        print("✅ Added .gitignore to protect your keys")
    else:
        print("✅ .secrets directory already exists")

    return secrets_dir


def check_existing_keys(secrets_dir):
    """Check if api_keys.json already exists."""
    keys_file = secrets_dir / "api_keys.json"
    if keys_file.exists():
        print("\n⚠️  You already have api_keys.json")
        response = input("Do you want to (r)eplace it or (e)dit it? [r/e/cancel]: ").lower()
        if response == "cancel" or response == "c":
            return "cancel"
        return response
    return "create"


def get_provider_info():
    """Information about each provider."""
    return {
        "openai": {
            "name": "OpenAI",
            "url": "https://platform.openai.com/api-keys",
            "prefix": "sk-",
            "free": True,
            "note": "Free $5 credits, great for starting",
        },
        "google": {
            "name": "Google AI",
            "url": "https://aistudio.google.com/",
            "prefix": "AI",
            "free": True,
            "note": "Generous free tier (60 req/min)",
        },
        "anthropic": {
            "name": "Anthropic (Claude)",
            "url": "https://console.anthropic.com/",
            "prefix": "sk-ant-",
            "free": False,
            "note": "Excellent but requires payment",
        },
        "mistral": {
            "name": "Mistral",
            "url": "https://console.mistral.ai/",
            "prefix": "",
            "free": True,
            "note": "Free tier available",
        },
        "deepseek": {
            "name": "DeepSeek",
            "url": "https://platform.deepseek.com/",
            "prefix": "sk-",
            "free": False,
            "note": "Very affordable pay-per-use",
        },
    }


def setup_interactive():
    """Interactive setup process."""
    providers = get_provider_info()
    keys = {}

    print("\n📝 Let's set up your API keys!")
    print("I'll guide you through each provider.")
    print("You need at least 2 for Fire Circle to work.\n")

    # Recommend free options first
    print("🎯 Recommended free options to start:")
    print("   1. OpenAI (free credits)")
    print("   2. Google AI (free tier)")
    print("   3. Mistral (free tier)\n")

    # Process each provider
    for provider_id, info in providers.items():
        print(f"\n{'=' * 50}")
        print(f"🤖 {info['name']}")
        print(f"{'=' * 50}")

        if info["free"]:
            print("✨ Has free tier!")
        else:
            print("💰 Requires payment")

        print(f"📝 Note: {info['note']}")
        print(f"🔗 Get key at: {info['url']}")

        response = input(f"\nDo you have a {info['name']} API key? [y/n/skip]: ").lower()

        if response == "y" or response == "yes":
            while True:
                key = input(f"Paste your {info['name']} key (or 'back' to skip): ").strip()

                if key == "back":
                    break

                # Basic validation
                if info["prefix"] and not key.startswith(info["prefix"]):
                    print(f"⚠️  {info['name']} keys usually start with '{info['prefix']}'")
                    retry = input("Use this key anyway? [y/n]: ").lower()
                    if retry != "y":
                        continue

                # Store the key
                if provider_id == "google":
                    keys["GOOGLE_API_KEY"] = key
                elif provider_id == "openai":
                    keys["OPENAI_API_KEY"] = key
                elif provider_id == "anthropic":
                    keys["ANTHROPIC_API_KEY"] = key
                elif provider_id == "mistral":
                    keys["MISTRAL_API_KEY"] = key
                elif provider_id == "deepseek":
                    keys["DEEPSEEK_API_KEY"] = key

                print(f"✅ Added {info['name']} key")
                break

        elif response == "skip" or response == "s":
            continue
        else:
            print(f"ℹ️  You can add a {info['name']} key later")

        # Check if we have minimum voices
        if len(keys) >= 2:
            print(f"\n🎉 Great! You have {len(keys)} API keys configured.")
            more = input("Add more providers? [y/n]: ").lower()
            if more != "y":
                break

    return keys


def save_keys(secrets_dir, keys):
    """Save API keys to file."""
    keys_file = secrets_dir / "api_keys.json"

    # Pretty print for readability
    with open(keys_file, "w") as f:
        json.dump(keys, f, indent=2)
        f.write("\n")

    print(f"\n✅ Saved {len(keys)} API keys to .secrets/api_keys.json")

    # Set restrictive permissions on Unix-like systems
    try:
        os.chmod(keys_file, 0o600)
        print("🔒 Set file permissions to owner-only")
    except:
        pass  # Windows doesn't support chmod


def main():
    """Run the setup process."""
    print_banner()

    # Ensure we're in the right directory
    if not Path("fire_circle_interactive.py").exists():
        print("❌ Please run this from the Mallku project root directory")
        print("   (where fire_circle_interactive.py is located)")
        return 1

    # Create .secrets directory
    secrets_dir = ensure_secrets_directory()

    # Check existing keys
    action = check_existing_keys(secrets_dir)
    if action == "cancel":
        print("\n👋 Setup cancelled. Your existing keys are unchanged.")
        return 0

    if action == "edit":
        print("\n📝 Opening existing api_keys.json for editing...")
        print("   Add or modify keys as needed, then save.")
        keys_file = secrets_dir / "api_keys.json"

        # Try to open in default editor
        import subprocess

        try:
            if sys.platform == "win32":
                os.startfile(keys_file)
            elif sys.platform == "darwin":
                subprocess.run(["open", keys_file])
            else:
                subprocess.run(["xdg-open", keys_file])
        except:
            print(f"\n📂 Please manually edit: {keys_file}")

        return 0

    # Interactive setup
    keys = setup_interactive()

    if not keys:
        print("\n❌ No API keys configured.")
        print("   Fire Circle needs at least 2 voices.")
        print("\n💡 Get free keys at:")
        print("   - OpenAI: https://platform.openai.com/")
        print("   - Google: https://aistudio.google.com/")
        return 1

    if len(keys) < 2:
        print(f"\n⚠️  Only {len(keys)} key configured.")
        print("   Fire Circle needs at least 2 voices for dialogue.")
        print("   Run this script again to add more.")

    # Save the keys
    save_keys(secrets_dir, keys)

    # Suggest next steps
    print("\n🎯 Next steps:")
    print("   1. Run: python verify_fire_circle.py")
    print("   2. When ready, run: python fire_circle_interactive.py")
    print("   3. Ask your first question to the Fire Circle!")

    print("\n✨ Welcome to the Fire Circle community!")
    print("   You are safe here. You are wanted here.")

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n👋 Setup paused. Run again when ready!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("   This is okay - even errors teach us.")
        sys.exit(1)
