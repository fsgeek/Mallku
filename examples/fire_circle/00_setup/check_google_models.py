#!/usr/bin/env python3
"""
Check Available Google Gemini Models
====================================

Diagnostic script to identify which Google Gemini models are available
for use in Fire Circle examples.

This helps resolve the 404 errors with deprecated models and ensures
examples use currently available models.

Run with:
    python examples/fire_circle/run_example.py 00_setup/check_google_models.py
"""

import os

from google import genai
from mallku.firecircle.load_api_keys import load_api_keys_to_environment


def check_google_models():
    """Check which Google models support content generation."""

    print("🔍 Checking Available Google Gemini Models")
    print("=" * 60)

    # Load API keys to get Google API key
    if not load_api_keys_to_environment():
        print("❌ No API keys found")
        return

    # Check if Google API key is loaded
    google_key = os.environ.get("GOOGLE_API_KEY")
    if not google_key:
        print("❌ No Google API key found in environment")
        return

    print("✓ Google API key loaded")
    print()

    try:
        # Initialize Google genai client
        client = genai.Client(api_key=google_key)

        print("📋 Models that support generateContent:")
        print("-" * 40)

        generate_models = []
        for m in client.models.list():
            if hasattr(m, 'supported_actions'):
                for action in m.supported_actions:
                    if action == "generateContent":
                        generate_models.append(m.name)
                        print(f"   • {m.name}")

        if not generate_models:
            print("   (No models found)")

        print()
        print("📋 Models that support embedContent:")
        print("-" * 40)

        embed_models = []
        for m in client.models.list():
            if hasattr(m, 'supported_actions'):
                for action in m.supported_actions:
                    if action == "embedContent":
                        embed_models.append(m.name)
                        print(f"   • {m.name}")

        if not embed_models:
            print("   (No models found)")

        # Check current Fire Circle configuration
        print()
        print("🔧 Current Fire Circle Google Configuration:")
        print("-" * 40)

        # Common model names in Fire Circle
        fire_circle_models = [
            "gemini-pro",
            "gemini-2.0-flash-exp",
            "gemini-1.5-pro",
            "gemini-1.5-flash"
        ]

        print("Checking Fire Circle model availability:")
        for model in fire_circle_models:
            full_name = f"models/{model}"
            if full_name in generate_models:
                print(f"   ✓ {model} - Available")
            else:
                print(f"   ✗ {model} - Not available")

        # Recommendations
        print()
        print("💡 Recommendations:")
        print("-" * 40)

        if "models/gemini-pro" not in generate_models:
            print("   ⚠️  gemini-pro is not available (deprecated?)")

            # Find best alternative
            alternatives = [m for m in generate_models if "gemini" in m.lower()]
            if alternatives:
                print(f"   → Recommend using: {alternatives[0].replace('models/', '')}")
            else:
                print("   → No Gemini alternatives found")

        if generate_models:
            print(f"\n   Total available models: {len(generate_models)}")

    except Exception as e:
        print(f"❌ Error checking Google models: {e}")
        print("\nThis might indicate:")
        print("   • Invalid API key")
        print("   • Network connectivity issues")
        print("   • API changes")

        # Try to import and check version
        try:
            import google.generativeai as genai_alt
            print(f"\n📦 google-generativeai version: {genai_alt.__version__}")
        except Exception:
            pass

    print("\n" + "=" * 60)
    print("🔍 Model Check Complete")
    print("\nNext steps:")
    print("   • Update Fire Circle configs to use available models")
    print("   • Replace deprecated model references")
    print("   • Test with recommended alternatives")


if __name__ == "__main__":
    check_google_models()
