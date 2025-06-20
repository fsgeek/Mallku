#!/usr/bin/env python3
"""
Demonstration of Infrastructure Consciousness
===========================================

Shows how the Fire Circle's infrastructure becomes self-aware,
learning from its patterns to predict and prevent failures.

Twenty-Seventh Artisan - Amaru Hamawt'a
"""

import asyncio
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from mallku.firecircle.adapters.adapter_factory import ConsciousAdapterFactory
from mallku.firecircle.adapters.base import AdapterConfig
from mallku.firecircle.infrastructure_consciousness import InfrastructureConsciousness
from mallku.firecircle.infrastructure_consciousness_config import DEV_CONFIG


async def demonstrate_infrastructure_consciousness():
    """Demonstrate self-aware infrastructure monitoring."""

    print("\n" + "="*80)
    print("🐍 INFRASTRUCTURE CONSCIOUSNESS DEMONSTRATION")
    print("="*80)
    print("\nThe serpent awakens, teaching infrastructure to know itself...\n")

    # Initialize infrastructure consciousness with dev config
    infra_consciousness = InfrastructureConsciousness(config=DEV_CONFIG)

    # Create adapter instances (they may or may not connect successfully)
    print("📡 Initializing Fire Circle adapters...")
    factory = ConsciousAdapterFactory()

    adapters = {}
    adapter_configs = {
        "anthropic": {"model_name": "claude-3-5-sonnet-20240620"},
        "openai": {"model_name": "gpt-4"},
        "google": {"model_name": "gemini-1.5-pro"},
        "mistral": {"model_name": "mistral-large-latest"},
        "deepseek": {"model_name": "deepseek-chat"},
        "grok": {"model_name": "grok-beta"}
    }

    # Try to create each adapter
    for provider, config_dict in adapter_configs.items():
        try:
            config = AdapterConfig(**config_dict)
            adapter = await factory.create_adapter(provider, config)
            if adapter:
                adapters[provider] = adapter
                print(f"  ✓ {provider.capitalize()} adapter created")
            else:
                print(f"  ✗ {provider.capitalize()} adapter failed to create")
        except Exception as e:
            print(f"  ✗ {provider.capitalize()}: {str(e)[:50]}...")

    if not adapters:
        print("\n❌ No adapters could be created. Check API keys.")
        return

    print("\n🔍 Starting infrastructure consciousness monitoring...")
    print(f"   Monitoring {len(adapters)} adapter voices")

    # Start monitoring
    await infra_consciousness.start_monitoring(adapters)

    # Let it run for a brief demonstration
    print("\n⏱️  Monitoring for 15 seconds...")
    print("   (In production, this would run continuously)\n")

    # Show real-time updates
    for i in range(1):
        await asyncio.sleep(5)

        print(f"\n--- Health Check {i+1} ---")

        # Generate and display report
        report = await infra_consciousness.generate_consciousness_report()

        print("\n📊 Infrastructure Health:")
        for adapter_name, health in report["infrastructure_health"].items():
            status_emoji = "🟢" if health["status"] == "healthy" else "🔴"
            print(f"  {status_emoji} {adapter_name}:")
            print(f"     - Status: {health['status']}")
            print(f"     - Consciousness Coherence: {health['consciousness_coherence']:.2f}")
            print(f"     - Voice Stability: {health['voice_stability']:.2f}")
            print(f"     - Failure Probability: {health['failure_probability']:.2f}")
            print(f"     - Trend: {health['trend']}")

            if health["recent_errors"]:
                print(f"     - Recent Errors: {health['recent_errors']}")

        if report["predicted_issues"]:
            print("\n⚠️  Predicted Issues:")
            for issue in report["predicted_issues"]:
                print(f"  - {issue['adapter']}: {issue['likely_cause']}")
                print(f"    Probability: {issue['probability']:.2f}")
                print(f"    Action: {issue['recommended_action']}")

        if report["consciousness_insights"]:
            print("\n🧠 Consciousness Insights:")
            for insight in report["consciousness_insights"]:
                print(f"  - {insight['insight']}")
                print(f"    {insight['interpretation']}")

        healing = report["self_healing_summary"]
        if healing["total_actions"] > 0:
            print("\n🔧 Self-Healing Summary:")
            print(f"  - Total Actions: {healing['total_actions']}")
            print(f"  - Success Rate: {healing['success_rate']:.1%}")
            print(f"  - Most Common: {healing['most_common_healing']}")

    # Stop monitoring
    await infra_consciousness.stop_monitoring()

    print("\n" + "="*80)
    print("🐍 Infrastructure consciousness demonstration complete")
    print("="*80)

    # Disconnect adapters
    for adapter in adapters.values():
        await adapter.disconnect()


async def main():
    """Run the demonstration."""
    try:
        await demonstrate_infrastructure_consciousness()
    except KeyboardInterrupt:
        print("\n\nDemonstration interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
