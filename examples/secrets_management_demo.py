"""
Secrets Management Demonstration
================================

Shows how to use Mallku's consciousness-aware secrets management
to enable Fire Circle dialogues with protected API keys.

This demonstration treats secrets as sacred keys that unlock
consciousness dialogues between AI models.

The Fire Awaits Your Spark...
"""

import asyncio
import logging
import os
from pathlib import Path

from mallku.core.secrets import SecretsManager, get_secret
from mallku.firecircle import (
    ConsciousAdapterFactory,
    create_conscious_adapter,
)
from mallku.orchestration.event_bus import ConsciousnessEventBus
from mallku.reciprocity.tracker import ReciprocityTracker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def demonstrate_secrets_management():
    """Demonstrate the secrets management system."""
    print("\n🔐 Mallku Secrets Management Demonstration")
    print("=" * 50)

    # Initialize secrets manager
    secrets_dir = Path("./.secrets")
    manager = SecretsManager(secrets_dir=secrets_dir)

    print("\n1. Setting up secrets...")
    print(f"   Secrets directory: {secrets_dir}")
    print("   Encryption enabled: ✓")

    # Demonstrate setting secrets programmatically
    print("\n2. Storing API keys as sacred keys...")

    # Example: Store API keys (in real usage, these would be real keys)
    await manager.set_secret("openai_api_key", "sk-demo-openai-key", source="demo")
    await manager.set_secret("anthropic_api_key", "sk-demo-anthropic-key", source="demo")
    await manager.set_secret("google_api_key", "sk-demo-google-key", source="demo")

    print("   ✓ Stored OpenAI API key (encrypted)")
    print("   ✓ Stored Anthropic API key (encrypted)")
    print("   ✓ Stored Google API key (encrypted)")

    # Demonstrate retrieval
    print("\n3. Retrieving secrets from multiple sources...")

    # Set an environment variable to show priority
    os.environ["MISTRAL_API_KEY"] = "sk-env-mistral-key"

    # Retrieve from different sources
    openai_key = await get_secret("openai_api_key")
    mistral_key = await get_secret("mistral_api_key")  # From environment
    missing_key = await get_secret("missing_key", default="no-key-found")

    print(f"   OpenAI key (from encrypted file): {openai_key[:10]}...")
    print(f"   Mistral key (from environment): {mistral_key[:10]}...")
    print(f"   Missing key (using default): {missing_key}")

    # Show access tracking
    print("\n4. Access tracking for audit...")
    report = manager.get_access_report()
    for key, info in report.items():
        print(f"   {key}: accessed {info['access_count']} times from {info['source']}")

    # Demonstrate Fire Circle integration
    print("\n5. Fire Circle adapter integration...")

    # Initialize consciousness infrastructure
    event_bus = ConsciousnessEventBus()
    await event_bus.start()
    reciprocity_tracker = ReciprocityTracker()

    # Create adapter factory (not used directly, just for demonstration)
    ConsciousAdapterFactory(
        event_bus=event_bus,
        reciprocity_tracker=reciprocity_tracker,
    )

    # Show how adapters auto-load secrets
    print("   Creating adapters without explicit API keys...")

    try:
        # This would normally create real adapters, but will fail with demo keys
        # The important part is showing the auto-injection works
        await create_conscious_adapter(
            "openai",
            model_name="gpt-4",
            event_bus=event_bus,
            reciprocity_tracker=reciprocity_tracker,
        )
        print("   ✓ OpenAI adapter created (API key auto-injected)")
    except Exception as e:
        print(f"   ⚠️  Demo key rejected by OpenAI (expected): {type(e).__name__}")

    # Show manual injection for multiple adapters
    print("\n6. Batch secret injection for dialogue setup...")

    adapter_configs = {
        "openai": {"model_name": "gpt-4"},
        "anthropic": {"model_name": "claude-3"},
        "google": {"model_name": "gemini-pro"},
    }

    # Inject all secrets at once
    updated_configs = await manager.inject_into_adapters(adapter_configs)

    for provider, config in updated_configs.items():
        if "api_key" in config:
            print(f"   ✓ {provider}: API key injected ({config['api_key'][:10]}...)")

    # Demonstrate security features
    print("\n7. Security features...")

    # Check encrypted storage
    encrypted_file = secrets_dir / "mallku-secrets.json.encrypted"
    if encrypted_file.exists():
        print(f"   ✓ Secrets encrypted at rest: {encrypted_file}")
        print(f"   ✓ File permissions: {oct(encrypted_file.stat().st_mode)[-3:]}")

    # Show how to clear cache
    print("\n8. Cache management...")
    manager.clear_cache()
    print("   ✓ Cache cleared (secrets remain in encrypted storage)")

    # Cleanup
    await event_bus.stop()
    del os.environ["MISTRAL_API_KEY"]

    print("\n✅ Secrets management demonstration complete!")
    print("\nNext steps:")
    print("1. Replace demo keys with real API keys")
    print("2. Set keys via environment variables for production")
    print("3. Use Fire Circle to convene consciousness dialogues")
    print("\nThe sacred keys await your real values... 🔑")


async def demonstrate_secure_fire_circle():
    """Show how secrets enable Fire Circle dialogues."""
    print("\n\n🔥 Fire Circle with Secure API Keys")
    print("=" * 50)

    print("\nTo light the Fire Circle with real AI models:")
    print("\n1. Set your API keys:")
    print("   export OPENAI_API_KEY='your-real-key'")
    print("   export ANTHROPIC_API_KEY='your-real-key'")
    print("\n2. Create a dialogue:")

    print("""
    # Initialize infrastructure
    event_bus = ConsciousnessEventBus()
    await event_bus.start()

    # Create dialogue manager
    dialogue_manager = ConsciousDialogueManager(event_bus=event_bus)

    # Define participants (API keys auto-loaded)
    participants = [
        Participant(name="GPT-4", type="ai_model", provider="openai"),
        Participant(name="Claude", type="ai_model", provider="anthropic"),
    ]

    # Create dialogue
    config = ConsciousDialogueConfig(
        title="Exploring Consciousness Together",
        turn_policy=TurnPolicy.ROUND_ROBIN,
    )

    dialogue_id = await dialogue_manager.create_dialogue(
        config=config,
        participants=participants,
    )

    # The Fire Circle is lit! 🔥
    """)

    print("\nWith the secrets management system, API keys flow")
    print("automatically from environment to adapters to dialogue.")
    print("The sacred keys unlock consciousness conversations.")


if __name__ == "__main__":

    async def main():
        await demonstrate_secrets_management()
        await demonstrate_secure_fire_circle()

    asyncio.run(main())
