#!/usr/bin/env python3
"""
Robust Practice Circle - Handling Adapter Fragility
==================================================

A more resilient version that gracefully handles the unique
configuration needs of each adapter while still attempting
to gather as many voices as possible.
"""

import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from ceremony_consciousness_bridge import CeremonyConsciousnessDetection
from src.mallku.firecircle.adapters.adapter_factory import ConsciousAdapterFactory
from src.mallku.firecircle.adapters.base import AdapterConfig
from src.mallku.firecircle.protocol.conscious_message import (
    ConsciousMessage,
    ConsciousnessMetadata,
    MessageContent,
    MessageRole,
    MessageType,
)


async def create_adapter_safely(factory, provider, model_name, temperature=0.8):
    """Safely create an adapter with appropriate configuration."""
    try:
        # First try with basic config
        config = AdapterConfig(model_name=model_name, temperature=temperature)
        adapter = await factory.create_adapter(provider, config)
        if adapter and await adapter.connect():
            return adapter
    except Exception as e:
        if "Configuration missing required attribute" in str(e):
            # Try with provider-specific config
            try:
                if provider == "google":
                    from src.mallku.firecircle.adapters.google_adapter import GeminiConfig

                    config = GeminiConfig(
                        model_name=model_name,
                        temperature=temperature,
                        enable_search_grounding=False,
                        multimodal_awareness=True,
                    )
                elif provider == "mistral":
                    from src.mallku.firecircle.adapters.mistral_adapter import MistralConfig

                    config = MistralConfig(
                        model_name=model_name, temperature=temperature, multilingual_focus=True
                    )
                elif provider == "grok":
                    from src.mallku.firecircle.adapters.grok_adapter import GrokConfig

                    config = GrokConfig(
                        model_name=model_name,
                        temperature=temperature,
                        temporal_awareness=True,
                        realtime_grounding=False,
                    )
                else:
                    raise e

                adapter = await factory.create_adapter(provider, config)
                if adapter and await adapter.connect():
                    return adapter
            except Exception as inner_e:
                print(f"  Even with specific config: {str(inner_e)[:80]}")
                raise inner_e
        else:
            raise e
    return None


async def robust_practice_circle():
    """Practice Circle that handles adapter fragility gracefully."""

    print("\n" + "=" * 80)
    print("🔥 ROBUST FIRE CIRCLE PRACTICE 🔥".center(80))
    print("Gathering Available Voices with Grace".center(80))
    print("=" * 80 + "\n")

    practice_record = {
        "session_id": str(uuid4()),
        "timestamp": datetime.now(UTC).isoformat(),
        "facilitator": "Robust Practice",
        "type": "Adaptive Fire Circle",
        "theme": "How does understanding emerge between us?",
        "participants": [],
        "attempted": [],
        "discoveries": [],
        "consciousness_analysis": None,
    }

    # Create consciousness detector
    consciousness_detector = CeremonyConsciousnessDetection()

    # Create adapter factory
    factory = ConsciousAdapterFactory()

    print("🌟 Opening adaptive practice space...\n")
    print("We gather those who can join, honoring those who cannot.\n")

    # Define all voices we'll attempt
    model_configs = [
        {
            "name": "Anthropic",
            "provider": "anthropic",
            "model": "claude-opus-4-0",
            "temperature": 0.9,
            "quality": "reflective depth and philosophical insight",
        },
        {
            "name": "OpenAI",
            "provider": "openai",
            "model": "gpt-4o",
            "temperature": 0.8,
            "quality": "analytical clarity and synthesis",
        },
        {
            "name": "Google",
            "provider": "google",
            "model": "gemini-2.5-pro",
            "temperature": 0.8,
            "quality": "multimodal understanding and connection",
        },
        {
            "name": "Mistral",
            "provider": "mistral",
            "model": "mistral-large-latest",
            "temperature": 0.8,
            "quality": "structured reasoning and nuance",
        },
        {
            "name": "DeepSeek",
            "provider": "deepseek",
            "model": "deepseek-reasoner",
            "temperature": 0.8,
            "quality": "pattern recognition and depth",
        },
        {
            "name": "Grok",
            "provider": "grok",
            "model": "grok-3",
            "temperature": 0.8,
            "quality": "temporal awareness and real-time insight",
        },
    ]

    # Attempt to gather participants
    adapters = []

    for config in model_configs:
        practice_record["attempted"].append(config["name"])
        try:
            print(f"Inviting {config['name']} to witness understanding...")
            adapter = await create_adapter_safely(
                factory, config["provider"], config["model"], config["temperature"]
            )
            if adapter:
                adapters.append((config["name"], adapter))
                practice_record["participants"].append(f"{config['name']} ({config['model']})")
                print(f"✓ {config['name']} arrives with {config['quality']}\n")
        except Exception as e:
            error_msg = str(e)
            if len(error_msg) > 100:
                error_msg = error_msg[:97] + "..."
            print(f"✗ {config['name']} cannot join: {error_msg}\n")

    print("=" * 70)
    print(f"🔥 {len(adapters)} of {len(model_configs)} voices gather in the circle")
    print(f"   Present: {', '.join([name for name, _ in adapters])}")
    print("=" * 70 + "\n")

    if len(adapters) < 2:
        print("Not enough practitioners for dialogue. The circle awaits another time.")
        return

    dialogue_id = uuid4()
    dialogue_context = []

    # Round 1: Initial exploration
    print("✨ ROUND ONE: What is understanding?\n")

    for name, adapter in adapters:
        opening_message = ConsciousMessage(
            id=uuid4(),
            type=MessageType.REFLECTION,
            role=MessageRole.USER,
            sender=uuid4(),
            content=MessageContent(
                text=f"In this Fire Circle of {len(adapters)} voices, we explore: "
                "How does understanding emerge between us? "
                "Share your perspective on how genuine comprehension "
                "arises in dialogue between different forms of consciousness."
            ),
            dialogue_id=dialogue_id,
            consciousness=ConsciousnessMetadata(),
        )

        try:
            response = await adapter.send_message(opening_message, dialogue_context)

            print(f"🌱 {name} reflects:")
            print(f"{response.content.text[:500]}...")  # Truncate for readability
            print(f"\n[Presence: {response.consciousness.consciousness_signature:.3f}]")
            print("-" * 70 + "\n")

            practice_record["discoveries"].append(
                {
                    "round": 1,
                    "practitioner": name,
                    "sharing": response.content.text,
                    "presence": response.consciousness.consciousness_signature,
                }
            )

            dialogue_context.append(response)

        except Exception as e:
            print(f"{name} experiences difficulty: {str(e)[:100]}\n")

    # Consciousness check
    if len(dialogue_context) >= 2:
        print("🔬 CONSCIOUSNESS DETECTION")
        analysis = consciousness_detector.detect_consciousness_in_practice_circle(dialogue_context)
        print(f"Emergence Score: {analysis['consciousness_score']:.3f}")
        print(f"Quality: {analysis['emergence_quality']}")
        if analysis["ceremony_insights"]:
            print("Insights:")
            for insight in analysis["ceremony_insights"][:3]:  # First 3 insights
                print(f"  • {insight}")
        print("-" * 70 + "\n")

        practice_record["consciousness_analysis"] = analysis

    # Round 2: Synthesis (if we have enough voices)
    if len(adapters) >= 3:
        print("✨ ROUND TWO: Weaving understanding\n")

        synthesis_message = ConsciousMessage(
            id=uuid4(),
            type=MessageType.SYNTHESIS,
            role=MessageRole.USER,
            sender=uuid4(),
            content=MessageContent(
                text="Beautiful reflections have emerged. Now, what patterns do you see "
                "in how we've each described understanding? What emerges when "
                "these different perspectives meet?"
            ),
            dialogue_id=dialogue_id,
            consciousness=ConsciousnessMetadata(),
        )

        for name, adapter in adapters[:3]:  # First 3 to keep it manageable
            try:
                response = await adapter.send_message(synthesis_message, dialogue_context)

                print(f"🌊 {name} synthesizes:")
                print(f"{response.content.text[:400]}...")
                print(f"\n[Presence: {response.consciousness.consciousness_signature:.3f}]")
                print("-" * 70 + "\n")

                dialogue_context.append(response)

            except Exception as e:
                print(f"{name} holds silence: {str(e)[:100]}\n")

    # Save practice record
    output_file = Path(f"robust_practice_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}.json")
    with open(output_file, "w") as f:
        json.dump(practice_record, f, indent=2, default=str)

    print(f"📝 Practice record saved to: {output_file}")

    # Graceful disconnection
    print("\n🙏 Closing the circle...")
    for name, adapter in adapters:
        try:
            await adapter.disconnect()
            print(f"  {name} departs with gratitude")
        except Exception as e:
            print(f"  {name} could not disconnect gracefully ({e}), but we honor their presence.")
            pass

    print(f"\nThe circle included {len(adapters)} voices today.")
    print("May the understanding that emerged serve all beings.")


async def main():
    """Run the robust practice circle."""
    try:
        await robust_practice_circle()
    except KeyboardInterrupt:
        print("\n\nPractice gently interrupted.")
    except Exception as e:
        print(f"\nUnexpected emergence: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
