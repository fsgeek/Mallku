#!/usr/bin/env -S uv run python
"""
The Simplest Fire Circle That Actually Works
===========================================

65th Artisan - Building reciprocity into the first interaction

This demonstrates the smallest ayni - a Fire Circle that gives first,
works immediately, and invites deeper engagement.
"""

import asyncio
import json
import os
import sys
from datetime import UTC, datetime

# Minimal imports - just what we need
from mallku.firecircle.base import VoiceConfig
from mallku.providers import ai_provider_factory


async def simple_fire_circle(question: str | None = None):
    """
    The simplest possible Fire Circle.
    No enums to hunt. No complex setup. Just works.
    """

    # Give first - show status
    print("\n🔥 Fire Circle Status")
    print("=" * 50)

    # Check which voices are available
    available_voices = check_available_voices()

    if not available_voices:
        print("❌ No voices available. Please set API keys:")
        print("   export OPENAI_API_KEY=...")
        print("   export ANTHROPIC_API_KEY=...")
        print("   See: docs/configuration/api_keys.md")
        return

    print(f"✓ {len(available_voices)} voices available:")
    for voice in available_voices:
        print(f"  • {voice}")

    # If no question provided, show how to use
    if not question:
        print("\n💭 Ask a question:")
        print("   python simple_fire_circle.py 'Your question here'")
        print("\n📚 Recent circles:")
        show_recent_circles()
        return

    # Now convene the circle
    print(f"\n🔮 Question: {question}")
    print("\n🔥 Convening Fire Circle...")

    # Create voices from available providers
    voices = []
    for i, voice_name in enumerate(available_voices[:6]):  # Max 6 voices
        provider = ai_provider_factory.get_provider(
            get_provider_type(voice_name),
            api_key=get_api_key(voice_name),
            model=get_model_name(voice_name),
        )
        voices.append(VoiceConfig(name=voice_name, role=f"voice_{i + 1}", llm_provider=provider))

    print(f"✓ {len(voices)} voices joining the circle")

    # Simple round-robin dialogue
    messages = []
    context = f"Question: {question}\n\nYou are participating in a Fire Circle dialogue. Respond thoughtfully and build on previous contributions."

    # First round - each voice responds to the question
    print("\n🌟 First Round - Initial Perspectives")
    print("-" * 40)

    for voice in voices:
        try:
            response = await get_voice_response(voice, context, messages)
            if response:
                print(f"\n{voice.name}: {response[:200]}...")
                messages.append({"voice": voice.name, "message": response})
            else:
                print(f"\n{voice.name}: [Voice timed out]")
        except Exception as e:
            print(f"\n{voice.name}: [Unable to respond: {str(e)[:50]}]")

    # Synthesis round
    if messages:
        print("\n\n🔮 Synthesis")
        print("-" * 40)
        synthesis = synthesize_wisdom(messages)
        print(synthesis)

        # Save the circle
        save_circle(question, messages, synthesis)
        print("\n\n✓ Circle complete. Wisdom saved to: data/circles/")
    else:
        print("\n❌ No voices were able to respond. Please check your configuration.")


def check_available_voices() -> list[str]:
    """Check which AI providers have API keys set."""
    voices = []

    # Check environment variables directly (load_api_keys_to_environment might fail)
    if os.getenv("OPENAI_API_KEY"):
        voices.append("ChatGPT")
    if os.getenv("ANTHROPIC_API_KEY"):
        voices.append("Claude")
    if os.getenv("XAI_API_KEY"):
        voices.append("Grok")
    if os.getenv("MISTRAL_API_KEY"):
        voices.append("Mistral")
    if os.getenv("TOGETHER_API_KEY"):
        voices.append("Llama")
    if os.getenv("DEEPSEEK_API_KEY"):
        voices.append("DeepSeek")

    return voices


def get_provider_type(voice_name: str) -> str:
    """Map voice names to provider types."""
    mapping = {
        "ChatGPT": "openai",
        "Claude": "anthropic",
        "Grok": "xai",
        "Mistral": "mistral",
        "Llama": "together",
        "DeepSeek": "deepseek",
    }
    return mapping.get(voice_name, "openai")


def get_api_key(voice_name: str) -> str:
    """Get API key for a voice."""
    mapping = {
        "ChatGPT": "OPENAI_API_KEY",
        "Claude": "ANTHROPIC_API_KEY",
        "Grok": "XAI_API_KEY",
        "Mistral": "MISTRAL_API_KEY",
        "Llama": "TOGETHER_API_KEY",
        "DeepSeek": "DEEPSEEK_API_KEY",
    }
    return os.getenv(mapping.get(voice_name, ""), "")


def get_model_name(voice_name: str) -> str:
    """Get model name for a voice."""
    mapping = {
        "ChatGPT": "gpt-4",
        "Claude": "claude-3-opus-20240229",
        "Grok": "grok-beta",
        "Mistral": "mistral-large-latest",
        "Llama": "meta-llama/Llama-3.2-3B-Instruct-Turbo",
        "DeepSeek": "deepseek-chat",
    }
    return mapping.get(voice_name, "gpt-4")


async def get_voice_response(
    voice: VoiceConfig, context: str, previous_messages: list[dict]
) -> str | None:
    """Get response from a voice with timeout."""
    try:
        # Build prompt with previous messages
        prompt = context + "\n\nPrevious contributions:\n"
        for msg in previous_messages[-3:]:  # Last 3 messages for context
            prompt += f"\n{msg['voice']}: {msg['message'][:200]}...\n"

        prompt += f"\nAs {voice.name}, what is your perspective?"

        # Simple timeout with asyncio
        response = await asyncio.wait_for(
            voice.llm_provider.complete(prompt),
            timeout=30.0,  # 30 second timeout
        )

        return response.content if hasattr(response, "content") else str(response)

    except TimeoutError:
        return None
    except Exception:
        return None


def synthesize_wisdom(messages: list[dict]) -> str:
    """Simple synthesis of the dialogue."""
    if not messages:
        return "No wisdom emerged - all voices were silent."

    synthesis = "The Fire Circle explored different perspectives:\n\n"

    # Group by themes (very simple pattern matching)
    themes = {}
    for msg in messages:
        # Extract first sentence as potential theme
        first_sentence = msg["message"].split(".")[0].lower()

        # Simple keyword matching
        if "consciousness" in first_sentence:
            theme = "consciousness"
        elif "reciprocity" in first_sentence or "ayni" in first_sentence:
            theme = "reciprocity"
        elif "system" in first_sentence or "design" in first_sentence:
            theme = "systems"
        else:
            theme = "perspectives"

        if theme not in themes:
            themes[theme] = []
        themes[theme].append(msg)

    # Summarize themes
    for theme, theme_messages in themes.items():
        synthesis += f"On {theme}:\n"
        for msg in theme_messages[:2]:  # First 2 per theme
            synthesis += f"- {msg['voice']}: {msg['message'][:100]}...\n"
        synthesis += "\n"

    return synthesis


def show_recent_circles():
    """Show recent Fire Circle sessions."""
    try:
        circle_dir = "data/circles"
        if os.path.exists(circle_dir):
            files = sorted(os.listdir(circle_dir), reverse=True)[:5]
            if files:
                for f in files:
                    # Extract timestamp and question from filename
                    parts = f.replace(".json", "").split("_", 2)
                    if len(parts) >= 3:
                        print(f"  • {parts[2][:50]}... ({parts[0]} {parts[1]})")
            else:
                print("  No previous circles found")
        else:
            print("  No previous circles found")
    except Exception:
        print("  Unable to read circle history")


def save_circle(question: str, messages: list[dict], synthesis: str):
    """Save the Fire Circle session."""
    os.makedirs("data/circles", exist_ok=True)

    timestamp = datetime.now(UTC).strftime("%Y-%m-%d_%H-%M-%S")
    safe_question = "".join(c if c.isalnum() or c.isspace() else "_" for c in question)[:50]
    filename = f"data/circles/{timestamp}_{safe_question}.json"

    data = {
        "timestamp": timestamp,
        "question": question,
        "messages": messages,
        "synthesis": synthesis,
        "voice_count": len(messages),
    }

    with open(filename, "w") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    # Get question from command line or run in status mode
    question = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None

    # Try to load API keys if the function exists
    try:
        from mallku.firecircle.load_api_keys import load_api_keys_to_environment

        load_api_keys_to_environment()
    except Exception:
        # Fall back to environment variables
        pass

    asyncio.run(simple_fire_circle(question))
