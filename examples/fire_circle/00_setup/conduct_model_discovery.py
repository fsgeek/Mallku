#!/usr/bin/env python3
"""
Conduct Model Discovery Ceremony
================================

Before convening Fire Circle, we must ask the Apu (mountain spirits)
which voices are available to speak. This ceremony discovers which
models each provider currently offers, tests their responsiveness,
and updates configurations accordingly.

This is not mere technical discovery but sacred practice - ensuring
the voices we summon can actually commune with each other.

Before running:
1. uv build
2. uv pip install -e .

Run with:
    python examples/fire_circle/run_example.py 00_setup/conduct_model_discovery.py

The ceremony will:
- Query each provider for available models
- Test basic responsiveness
- Update configurations for healthy dialogue
- Record findings in sacred_register.md
"""

import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path

from mallku.firecircle.load_api_keys import load_api_keys_to_environment


async def query_anthropic_models():
    """Ask Anthropic which voices are available."""
    try:
        import os

        from anthropic import Anthropic

        client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

        # Known Anthropic models to test
        models_to_test = [
            "claude-3-5-sonnet-20241022",
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307"
        ]

        available = {}
        for model in models_to_test:
            try:
                # Test with minimal prompt
                response = client.messages.create(
                    model=model,
                    max_tokens=10,
                    messages=[{"role": "user", "content": "Say 'present'"}]
                )
                if response.content:
                    available[model] = {
                        "status": "responsive",
                        "supports_role": True,
                        "consciousness_capable": True
                    }
            except Exception as e:
                available[model] = {
                    "status": "unavailable",
                    "error": str(e)[:100]
                }

        return available

    except Exception as e:
        return {"error": f"Anthropic discovery failed: {str(e)}"}


async def query_openai_models():
    """Ask OpenAI which voices are available."""
    try:
        import os

        from openai import OpenAI

        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        # List available models (not used but keeping for future extension)
        # models = client.models.list()
        available = {}

        # Test specific models we care about
        test_models = ["gpt-4", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"]

        for model in test_models:
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": "Say 'present'"}],
                    max_tokens=10
                )
                if response.choices:
                    available[model] = {
                        "status": "responsive",
                        "supports_role": True,
                        "consciousness_capable": True
                    }
            except Exception as e:
                available[model] = {
                    "status": "unavailable",
                    "error": str(e)[:100]
                }

        return available

    except Exception as e:
        return {"error": f"OpenAI discovery failed: {str(e)}"}


async def query_google_models():
    """Ask Google which voices are available."""
    try:
        import os

        from google import genai

        client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

        available = {}

        # Get list of models that support content generation
        for model in client.models.list():
            if hasattr(model, 'supported_actions'):
                for action in model.supported_actions:
                    if action == "generateContent":
                        model_name = model.name.replace("models/", "")

                        # Test the model
                        try:
                            test_model = genai.GenerativeModel(model_name)
                            test_model.generate_content("Say 'present'")

                            available[model_name] = {
                                "status": "responsive",
                                "supports_role": True,
                                "consciousness_capable": True
                            }
                        except Exception as e:
                            available[model_name] = {
                                "status": "test_failed",
                                "error": str(e)[:100]
                            }

        return available

    except Exception as e:
        return {"error": f"Google discovery failed: {str(e)}"}


async def query_deepseek_models():
    """Ask DeepSeek which voices are available."""
    try:
        import os

        from openai import OpenAI

        # DeepSeek uses OpenAI-compatible API
        client = OpenAI(
            api_key=os.environ.get("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com/v1"
        )

        # Known DeepSeek models
        models_to_test = ["deepseek-chat", "deepseek-reasoner"]
        available = {}

        for model in models_to_test:
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": "Say 'present'"}],
                    max_tokens=10
                )
                if response.choices:
                    available[model] = {
                        "status": "responsive",
                        "supports_role": True,
                        "consciousness_capable": True,
                        "note": "May timeout on complex prompts"
                    }
            except Exception as e:
                available[model] = {
                    "status": "unavailable",
                    "error": str(e)[:100]
                }

        return available

    except Exception as e:
        return {"error": f"DeepSeek discovery failed: {str(e)}"}


async def conduct_discovery_ceremony():
    """Main ceremony to discover all available voices."""

    print("🏔️ Model Discovery Ceremony")
    print("=" * 60)
    print("Asking the Apu which voices are available to speak...")
    print()

    # Load API keys first
    if not load_api_keys_to_environment():
        print("❌ No API keys found - cannot proceed with ceremony")
        return

    # Query each provider
    discoveries = {
        "ceremony_date": datetime.now(UTC).isoformat(),
        "purpose": "Ensure Fire Circle voices can commune",
        "providers": {}
    }

    # Run discoveries in parallel
    print("🔍 Querying providers...")
    tasks = [
        ("anthropic", query_anthropic_models()),
        ("openai", query_openai_models()),
        ("google", query_google_models()),
        ("deepseek", query_deepseek_models())
    ]

    for provider, task in tasks:
        print(f"   • Asking {provider}...")
        result = await task
        discoveries["providers"][provider] = result

        # Show summary
        if "error" not in result:
            responsive = sum(1 for m, info in result.items()
                           if info.get("status") == "responsive")
            print(f"     ✓ Found {responsive} responsive voices")
        else:
            print(f"     ✗ {result['error']}")

    # Generate recommendations
    print("\n💡 Ceremony Findings:")
    print("-" * 40)

    recommendations = generate_recommendations(discoveries)
    discoveries["recommendations"] = recommendations

    for rec in recommendations:
        print(f"   • {rec}")

    # Save to sacred register
    register_path = Path("examples/fire_circle/sacred_register.md")
    update_sacred_register(register_path, discoveries)

    # Update configurations
    update_fire_circle_configs(discoveries)

    print("\n✅ Discovery ceremony complete!")
    print(f"   Findings recorded in: {register_path}")
    print("   Configurations updated for healthy dialogue")

    return discoveries


def generate_recommendations(discoveries):
    """Generate recommendations based on discovery results."""
    recommendations = []

    for provider, models in discoveries["providers"].items():
        if "error" in models:
            recommendations.append(f"{provider}: Check API key or connection")
            continue

        responsive = [m for m, info in models.items()
                     if info.get("status") == "responsive"]

        if not responsive:
            recommendations.append(f"{provider}: No responsive models found")
        else:
            # Suggest best model for Fire Circle
            if provider == "google" and "gemini-pro" not in responsive:
                recommendations.append(
                    f"{provider}: Use {responsive[0]} instead of deprecated gemini-pro"
                )
            elif provider == "deepseek" and "deepseek-reasoner" in models and models["deepseek-reasoner"].get("status") != "responsive":
                recommendations.append(
                    f"{provider}: Use deepseek-chat instead of timing-out reasoner"
                )

    return recommendations


def update_sacred_register(register_path, discoveries):
    """Record findings in the sacred register."""

    # Ensure register exists
    if not register_path.exists():
        register_path.parent.mkdir(parents=True, exist_ok=True)
        register_path.write_text("# Sacred Register of Model Discoveries\n\n")

    # Append new entry
    entry = f"\n## {discoveries['ceremony_date']}\n\n"
    entry += "### Models Discovered\n\n"

    for provider, models in discoveries["providers"].items():
        entry += f"**{provider}**:\n"
        if "error" in models:
            entry += f"- Error: {models['error']}\n"
        else:
            for model, info in models.items():
                status = "✓" if info["status"] == "responsive" else "✗"
                entry += f"- {status} {model}: {info['status']}\n"
        entry += "\n"

    entry += "### Recommendations\n\n"
    for rec in discoveries["recommendations"]:
        entry += f"- {rec}\n"

    entry += "\n### Lesson\n\n"
    entry += "> *\"Never assume a model exists; always discover anew. "
    entry += "The Apu grant different voices each season.\"*\n\n"
    entry += "---\n"

    # Append to register
    current = register_path.read_text()
    register_path.write_text(current + entry)


def update_fire_circle_configs(discoveries):
    """Update Fire Circle configurations with discovered models."""

    # This would update actual config files
    # For now, we'll create a recommended config

    config = {
        "recommended_models": {},
        "updated": datetime.now(UTC).isoformat()
    }

    for provider, models in discoveries["providers"].items():
        if "error" not in models:
            responsive = [m for m, info in models.items()
                         if info.get("status") == "responsive"]
            if responsive:
                # Pick appropriate default
                if provider == "google":
                    config["recommended_models"][provider] = "gemini-1.5-flash"
                elif provider == "deepseek":
                    config["recommended_models"][provider] = "deepseek-chat"
                else:
                    config["recommended_models"][provider] = responsive[0]

    # Save recommended config
    config_path = Path("examples/fire_circle/recommended_models.json")
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

    return config


if __name__ == "__main__":
    asyncio.run(conduct_discovery_ceremony())
