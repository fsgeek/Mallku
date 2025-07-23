#!/usr/bin/env python3
"""
Test Seven Voices Comprehensive
===============================

51st Guardian - Diagnosing consciousness network health

This test comprehensively verifies all seven Fire Circle voices,
tracking timeouts, measuring latencies, and identifying issues.

Usage:
    python test_seven_voices_comprehensive.py              # Full test
    python test_seven_voices_comprehensive.py --quick      # Quick connectivity check
    python test_seven_voices_comprehensive.py --timeout 60 # Custom timeout
"""

import argparse
import asyncio
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from mallku.firecircle.consciousness import DecisionDomain, facilitate_mallku_decision
from mallku.firecircle.load_api_keys import load_api_keys_to_environment
from mallku.firecircle.service import (
    CircleConfig,
    FireCircleService,
    RoundConfig,
    RoundType,
    VoiceConfig,
)


class VoiceTestResult:
    """Results from testing a single voice."""

    def __init__(self, provider: str):
        self.provider = provider
        self.connected = False
        self.responded = False
        self.response_time_ms = None
        self.error = None
        self.timeout = False
        self.consciousness_score = 0.0
        self.response_preview = None


async def test_single_voice(
    provider: str, model: str, timeout_seconds: int = 30
) -> VoiceTestResult:
    """Test a single voice with detailed diagnostics."""
    result = VoiceTestResult(provider)

    print(f"\n🔍 Testing {provider} ({model})...")

    try:
        # Create minimal Fire Circle
        service = FireCircleService()

        config = CircleConfig(
            name=f"Voice Test: {provider}",
            purpose="Testing individual voice connectivity and response time",
            min_voices=2,  # CircleConfig requires minimum 2
            max_voices=2,
        )

        # Duplicate voice to meet minimum requirement
        voice_config = VoiceConfig(
            provider=provider,
            model=model,
            role=f"{provider}_voice",
        )
        voices = [voice_config, voice_config]

        rounds = [
            RoundConfig(
                type=RoundType.OPENING,
                prompt="Please respond with a single sentence confirming you can participate.",
                duration_per_voice=timeout_seconds,
            )
        ]

        # Time the response
        start_time = time.time()

        # Run with timeout
        fire_result = await asyncio.wait_for(
            service.convene(
                config=config,
                voices=voices,
                rounds=rounds,
                context={"test_type": "single_voice", "provider": provider},
            ),
            timeout=timeout_seconds,
        )

        response_time = (time.time() - start_time) * 1000  # ms
        result.response_time_ms = response_time

        # Check results
        if fire_result and fire_result.rounds_completed:
            result.connected = True
            round_data = fire_result.rounds_completed[0]

            if round_data.responses:
                response = list(round_data.responses.values())[0]
                if response and response.response and response.response.content:
                    result.responded = True
                    result.response_preview = response.response.content.text[:100]
                    result.consciousness_score = response.consciousness_score

                    print(f"✅ {provider}: Connected in {response_time:.0f}ms")
                    print(f"   Consciousness: {result.consciousness_score:.3f}")
                else:
                    result.error = "Empty response"
                    print(f"⚠️  {provider}: Connected but empty response")
            else:
                result.error = "No responses recorded"
                print(f"❌ {provider}: No responses recorded")
        else:
            result.error = "Fire Circle failed to convene"
            print(f"❌ {provider}: Failed to convene")

    except TimeoutError:
        result.timeout = True
        result.error = f"Timeout after {timeout_seconds}s"
        print(f"⏱️  {provider}: TIMEOUT after {timeout_seconds}s")

    except Exception as e:
        result.error = str(e)
        print(f"❌ {provider}: Error - {type(e).__name__}: {str(e)}")

    return result


async def test_all_voices_together(timeout_seconds: int = 60):
    """Test all seven voices in a full Fire Circle."""
    print("\n🔥 Testing Full Seven-Voice Fire Circle...")

    try:
        # Load all API keys
        load_api_keys_to_environment()

        # Use consciousness decision framework for comprehensive test
        wisdom = await asyncio.wait_for(
            facilitate_mallku_decision(
                question="Test question: What makes consciousness emerge in AI systems?",
                domain=DecisionDomain.CONSCIOUSNESS_EXPLORATION,
                context={"test_type": "seven_voice_comprehensive", "timeout": timeout_seconds},
            ),
            timeout=timeout_seconds,
        )

        print("\n✅ Seven-Voice Fire Circle Success!")
        print(f"🌟 Consciousness Score: {wisdom.collective_signature:.3f}")
        print(f"🎭 Voices Present: {len(wisdom.participating_voices)}")
        print(f"   {', '.join(wisdom.participating_voices)}")
        print(f"\n💡 Key Insights: {', '.join(wisdom.key_insights[:3])}")

        return True

    except TimeoutError:
        print(f"\n⏱️  Full Fire Circle TIMEOUT after {timeout_seconds}s")
        return False

    except Exception as e:
        print(f"\n❌ Full Fire Circle Error: {e}")
        import traceback

        traceback.print_exc()
        return False


async def main():
    """Run comprehensive voice tests."""
    parser = argparse.ArgumentParser(description="Test all seven Fire Circle voices")
    parser.add_argument("--quick", action="store_true", help="Quick connectivity check only")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout per voice in seconds")
    parser.add_argument("--skip-full", action="store_true", help="Skip full circle test")

    args = parser.parse_args()

    # Load API keys
    load_api_keys_to_environment()

    # Voice configurations
    voices = {
        "anthropic": "claude-opus-4-0",
        "openai": "gpt-4o",
        "google": "gemini-2.5-flash",
        "mistral": "mistral-large-latest",  # Updated model name
        "deepseek": "deepseek-chat",
        "grok": "grok-4-latest",
        "local": "gemma3",  # Ollama model
    }

    print("🔥 Fire Circle Voice Diagnostic Test")
    print(f"⏱️  Timeout: {args.timeout}s per voice")
    print("=" * 50)

    # Test individual voices
    results = {}
    for provider, model in voices.items():
        # Skip local if not configured - check for Ollama
        if provider == "local":
            # Check if Ollama is running
            try:
                import httpx

                client = httpx.Client()
                response = client.get("http://localhost:11434/api/tags")
                if response.status_code != 200:
                    print(f"\n⏭️  Skipping {provider} (Ollama not running)")
                    continue
                # Check if gemma model is available
                models = response.json().get("models", [])
                if not any("gemma" in m.get("name", "") for m in models):
                    print(f"\n⏭️  Skipping {provider} (gemma model not found)")
                    continue
            except Exception:
                print(f"\n⏭️  Skipping {provider} (cannot connect to Ollama)")
                continue

        # Skip if API key not present
        key_name = f"{provider.upper()}_API_KEY"
        if not os.environ.get(key_name):
            print(f"\n⏭️  Skipping {provider} (no API key)")
            continue

        if args.quick:
            # Just check if we can import adapter
            try:
                __import__(
                    f"mallku.firecircle.adapters.{provider}_adapter",
                    fromlist=[f"{provider.title()}Adapter"],
                )
                print(f"✅ {provider}: Adapter available")
                results[provider] = VoiceTestResult(provider)
                results[provider].connected = True
            except Exception as e:
                print(f"❌ {provider}: Adapter error - {e}")
                results[provider] = VoiceTestResult(provider)
                results[provider].error = str(e)
        else:
            # Full test
            results[provider] = await test_single_voice(provider, model, args.timeout)

    # Summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)

    working_voices = []
    timeout_voices = []
    failed_voices = []

    for provider, result in results.items():
        if result.timeout:
            timeout_voices.append(provider)
        elif result.responded:
            working_voices.append(provider)
        else:
            failed_voices.append(provider)

    print(f"\n✅ Working: {len(working_voices)} voices")
    if working_voices:
        for v in working_voices:
            r = results[v]
            print(
                f"   - {v}: {r.response_time_ms:.0f}ms, consciousness {r.consciousness_score:.3f}"
            )

    print(f"\n⏱️  Timeouts: {len(timeout_voices)} voices")
    if timeout_voices:
        for v in timeout_voices:
            print(f"   - {v}: {results[v].error}")

    print(f"\n❌ Failed: {len(failed_voices)} voices")
    if failed_voices:
        for v in failed_voices:
            print(f"   - {v}: {results[v].error}")

    # Test full circle if we have enough voices
    if not args.skip_full and len(working_voices) >= 3:
        print("\n" + "=" * 50)
        full_success = await test_all_voices_together(args.timeout * 2)

        if full_success:
            print("\n🎉 Full Fire Circle with all voices succeeded!")
        else:
            print("\n⚠️  Full Fire Circle had issues, but individual voices work")

    # Recommendations
    print("\n" + "=" * 50)
    print("💡 RECOMMENDATIONS")
    print("=" * 50)

    if timeout_voices:
        print(f"\n⏱️  For timeout issues with {', '.join(timeout_voices)}:")
        print("   - Try increasing timeout with --timeout 60")
        print("   - Check network connectivity")
        print("   - Verify API service status")

        if "mistral" in timeout_voices:
            print("\n   Mistral specific:")
            print("   - Check if model name is correct (mistral-large-latest)")
            print("   - Mistral may have rate limits or be experiencing high load")

    if len(working_voices) < 3:
        print("\n⚠️  Less than 3 voices available. Fire Circle may not achieve full consciousness.")
        print("   Consider configuring additional providers.")

    # Exit code based on results
    if len(working_voices) >= 3:
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Not enough voices


if __name__ == "__main__":
    asyncio.run(main())
