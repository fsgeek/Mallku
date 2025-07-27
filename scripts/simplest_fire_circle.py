#!/usr/bin/env -S uv run python
"""
The Absolute Simplest Fire Circle
=================================

No Mallku imports. No complex dependencies. Just works.

This is the smallest ayni - it gives immediately, works with what you have.
"""

import asyncio
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path

# Simple AI provider setup - no complex imports
PROVIDERS = {
    "openai": {
        "env_var": "OPENAI_API_KEY",
        "name": "ChatGPT",
        "url": "https://api.openai.com/v1/chat/completions",
        "model": "gpt-4",
    },
    "anthropic": {
        "env_var": "ANTHROPIC_API_KEY",
        "name": "Claude",
        "url": "https://api.anthropic.com/v1/messages",
        "model": "claude-3-sonnet-20240229",
    },
}


def check_available_voices():
    """See which voices we can use."""
    available = []
    for provider_id, config in PROVIDERS.items():
        if os.getenv(config["env_var"]):
            available.append(config["name"])
    return available


def show_status():
    """Give first - show what's available."""
    print("\n🔥 Fire Circle - Simple")
    print("=" * 50)

    voices = check_available_voices()

    if not voices:
        print("❌ No voices available")
        print("\n📝 To enable voices, set API keys:")
        print("   export OPENAI_API_KEY=sk-...")
        print("   export ANTHROPIC_API_KEY=sk-ant-...")
        print("\n💡 Then ask: python simplest_fire_circle.py 'Your question'")
    else:
        print(f"✓ {len(voices)} voices available: {', '.join(voices)}")
        print("\n💭 Ask a question:")
        print("   python simplest_fire_circle.py 'Your question here'")

    # Show recent circles
    print("\n📚 Recent circles:")
    circles_dir = Path("data/simple_circles")
    if circles_dir.exists():
        recent = sorted(circles_dir.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)[
            :3
        ]
        for circle_file in recent:
            with open(circle_file) as f:
                data = json.load(f)
                print(f"   • {data['question'][:50]}... ({data['timestamp']})")
    else:
        print("   (none yet)")


async def ask_gpt(question, context=""):
    """Ask ChatGPT - simple and direct."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    import aiohttp

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    data = {
        "model": "gpt-4",
        "messages": [
            {
                "role": "system",
                "content": "You are participating in a Fire Circle dialogue. Be thoughtful and build on others' ideas.",
            },
            {"role": "user", "content": f"{context}\n\nQuestion: {question}"},
        ],
        "max_tokens": 200,
        "temperature": 0.7,
    }

    try:
        async with (
            aiohttp.ClientSession() as session,
            session.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=30),
            ) as response,
        ):
            if response.status == 200:
                result = await response.json()
                return result["choices"][0]["message"]["content"]
    except Exception:
        return None


async def ask_claude(question, context=""):
    """Ask Claude - simple and direct."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return None

    import aiohttp

    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }

    data = {
        "model": "claude-3-sonnet-20240229",
        "max_tokens": 200,
        "messages": [
            {
                "role": "user",
                "content": f"You are participating in a Fire Circle dialogue. Be thoughtful and build on others' ideas.\n\n{context}\n\nQuestion: {question}",
            }
        ],
    }

    try:
        async with (
            aiohttp.ClientSession() as session,
            session.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=30),
            ) as response,
        ):
            if response.status == 200:
                result = await response.json()
                return result["content"][0]["text"]
    except Exception:
        return None


async def convene_circle(question):
    """Actually run the Fire Circle."""
    print(f"\n🔮 Question: {question}")
    print("\n🔥 Convening Fire Circle...")

    voices = check_available_voices()
    print(f"✓ {len(voices)} voices joining")

    responses = []

    # First round - ask each voice
    print("\n💭 Gathering perspectives...")

    # Ask available voices
    if "ChatGPT" in voices:
        print("  • ChatGPT thinking...")
        response = await ask_gpt(question)
        if response:
            responses.append({"voice": "ChatGPT", "text": response})
            print(f"    ✓ {response[:60]}...")
        else:
            print("    (timeout)")

    if "Claude" in voices:
        print("  • Claude thinking...")
        response = await ask_claude(question)
        if response:
            responses.append({"voice": "Claude", "text": response})
            print(f"    ✓ {response[:60]}...")
        else:
            print("    (timeout)")

    # Simple synthesis
    if responses:
        print("\n🌟 What emerged:")
        print("-" * 50)
        for r in responses:
            print(f"\n{r['voice']}:")
            print(f"{r['text']}")

        # Save it
        save_circle(question, responses)
        print("\n✓ Saved to data/simple_circles/")
    else:
        print("\n❌ No voices responded. Check your API keys.")


def save_circle(question, responses):
    """Save the circle for future reference."""
    circles_dir = Path("data/simple_circles")
    circles_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(UTC).strftime("%Y-%m-%d_%H-%M-%S")

    data = {"timestamp": timestamp, "question": question, "responses": responses}

    filename = circles_dir / f"{timestamp}_circle.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)


async def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        # User provided a question
        question = " ".join(sys.argv[1:])
        await convene_circle(question)
    else:
        # No question - show status (give first!)
        show_status()


if __name__ == "__main__":
    # Try to load Mallku API keys
    try:
        from mallku.firecircle.load_api_keys import load_api_keys_to_environment

        load_api_keys_to_environment()
    except Exception:
        pass  # Use environment variables if Mallku not available

    asyncio.run(main())
