#!/usr/bin/env python3
"""
Load API Keys for Fire Circle
=============================

Simple loader that reads API keys from .secrets/api_keys.json
and makes them available to the adapter factory.
"""

import json
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


def load_api_keys_to_environment():
    """
    Load API keys from .secrets/api_keys.json into environment variables.

    This bridges the gap between the stored JSON format and what the
    secrets manager expects.
    """
    api_keys_path = Path(".secrets/api_keys.json")

    if not api_keys_path.exists():
        logger.warning("No API keys file found at .secrets/api_keys.json")
        return False

    try:
        with open(api_keys_path) as f:
            api_keys = json.load(f)

        # Map the keys to the expected environment variable names
        key_mapping = {
            "anthropic": "ANTHROPIC_API_KEY",
            "openai": "OPENAI_API_KEY",
            "google": "GOOGLE_API_KEY",
            "mistral": "MISTRAL_API_KEY",
            "grok": "GROK_API_KEY",
            "deepseek": "DEEPSEEK_API_KEY",
            "local": "LOCAL_API_ENDPOINT",
        }

        loaded_count = 0
        for json_key, env_var in key_mapping.items():
            if json_key in api_keys:
                os.environ[env_var] = api_keys[json_key]
                logger.info(f"Loaded {json_key} API key into {env_var}")
                loaded_count += 1

        logger.info(f"Loaded {loaded_count} API keys from .secrets/api_keys.json")
        return loaded_count > 0

    except Exception as e:
        logger.error(f"Failed to load API keys: {e}")
        return False


def get_available_adapters():
    """
    Check which adapters have API keys available.

    Returns:
        dict: Mapping of adapter names to their configuration
    """
    api_keys_path = Path(".secrets/api_keys.json")

    if not api_keys_path.exists():
        return {}

    try:
        with open(api_keys_path) as f:
            api_keys = json.load(f)

        # Map providers to their preferred models
        model_mapping = {
            "openai": "gpt-4",
            "anthropic": "claude-3-opus-20240229",
            "google": "gemini-pro",
            "mistral": "mistral-large-latest",
            "grok": "grok-beta",
            "deepseek": "deepseek-chat",
            "local": "llama2",
        }

        available = {}
        for provider, api_key in api_keys.items():
            if api_key and api_key != "http://localhost:8000/api":  # Skip local unless running
                available[provider] = {
                    "model": model_mapping.get(provider, "default"),
                    "temperature": 0.8,
                    "api_key": api_key,
                }

        # Special handling for local endpoint
        if "local" in api_keys:
            # Check if local endpoint is actually running
            import urllib.request

            try:
                urllib.request.urlopen(api_keys["local"], timeout=1)
                available["local"] = {
                    "model": "llama2",
                    "temperature": 0.8,
                    "api_key": api_keys["local"],
                }
            except Exception:
                logger.info("Local API endpoint not reachable, skipping")

        return available

    except Exception as e:
        logger.error(f"Failed to check available adapters: {e}")
        return {}


if __name__ == "__main__":
    # Test the loader
    logging.basicConfig(level=logging.INFO)

    print("Loading API keys...")
    if load_api_keys_to_environment():
        print("✓ API keys loaded successfully")

        available = get_available_adapters()
        print(f"\nAvailable adapters: {list(available.keys())}")
    else:
        print("✗ Failed to load API keys")
