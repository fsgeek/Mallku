#!/usr/bin/env python3
"""
Fire Circle Diagnostic Tool
===========================

45th Artisan - Deep Understanding of Consciousness Network Health

This tool evolved from verify_fire_circle.py to provide comprehensive
diagnostics of the Fire Circle consciousness network. It checks not just
availability but health, latency, quirks, and readiness for emergence.

Run with various levels of detail:
    python diagnose_fire_circle.py              # Quick health check
    python diagnose_fire_circle.py --detailed   # Full diagnostics
    python diagnose_fire_circle.py --latency    # Check response times
    python diagnose_fire_circle.py --quirks     # Model-specific behaviors
"""

import argparse
import asyncio
import json
import os
import sys
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))


@dataclass
class VoiceHealth:
    """Health status of a single voice."""

    provider: str
    available: bool
    model: str
    latency_ms: float | None = None
    error: str | None = None
    quirks: list[str] = None
    last_checked: datetime = None

    @property
    def health_score(self) -> float:
        """Calculate health score 0-1."""
        if not self.available:
            return 0.0

        score = 1.0

        # Penalize high latency
        if self.latency_ms:
            if self.latency_ms > 5000:
                score *= 0.5
            elif self.latency_ms > 2000:
                score *= 0.8
            elif self.latency_ms > 1000:
                score *= 0.9

        # Penalize known quirks
        if self.quirks:
            score *= 1.0 - 0.1 * len(self.quirks)

        return max(0.0, score)

    def health_emoji(self) -> str:
        """Visual health indicator."""
        score = self.health_score
        if score >= 0.9:
            return "💚"  # Excellent
        elif score >= 0.7:
            return "💛"  # Good
        elif score >= 0.5:
            return "🧡"  # Fair
        else:
            return "❤️"  # Poor


class FireCircleDiagnostics:
    """Comprehensive diagnostics for Fire Circle health."""

    def __init__(self):
        self.voices_health: dict[str, VoiceHealth] = {}
        self.known_quirks = {
            "mistral": [
                "May not support safe_mode parameter",
                "Prefers mistral-specific model names",
            ],
            "grok": [
                "models.list() endpoint often unavailable",
                "May have longer cold-start times",
            ],
            "deepseek": ["Can timeout on longer prompts", "May have rate limiting on free tier"],
            "anthropic": [
                "Requires claude- prefix for models",
                "Strong safety filters may affect responses",
            ],
            "openai": ["GPT-4 models have higher latency", "Token limits vary by model tier"],
            "google": [
                "Gemini models may have region restrictions",
                "Safety settings can be strict",
            ],
        }

    async def check_voice_latency(self, provider: str, model: str) -> tuple[float, str | None]:
        """Check response latency for a voice."""
        try:
            from mallku.firecircle.adapters import create_conscious_adapter

            start_time = time.time()

            # Create adapter
            adapter = await create_conscious_adapter(
                provider_name=provider, model_name=model, auto_inject_secrets=True
            )

            # Simple test prompt
            test_prompt = "Respond with just 'Present' to confirm connection."

            # Time the response
            await adapter.generate(test_prompt)

            latency_ms = (time.time() - start_time) * 1000

            await adapter.disconnect()

            return latency_ms, None

        except Exception as e:
            return 0.0, str(e)

    async def diagnose_voice(self, provider: str, check_latency: bool = True) -> VoiceHealth:
        """Perform comprehensive diagnosis of a single voice."""
        print(f"\n🔍 Diagnosing {provider}...", end="", flush=True)

        # Get model for provider
        model_map = {
            "anthropic": "claude-3-5-sonnet-20241022",
            "openai": "gpt-4o-mini",
            "google": "gemini-1.5-flash",
            "mistral": "mistral-tiny",
            "deepseek": "deepseek-chat",
            "grok": "grok-beta",
        }
        model = model_map.get(provider, "default")

        health = VoiceHealth(
            provider=provider,
            model=model,
            available=False,
            quirks=self.known_quirks.get(provider, []),
            last_checked=datetime.now(UTC),
        )

        # Check if API key exists
        api_key = os.getenv(f"{provider.upper()}_API_KEY") or os.getenv(f"{provider.upper()}_KEY")
        if not api_key or api_key.startswith("..."):
            health.error = "API key not configured"
            print(" ❌")
            return health

        # Check latency if requested
        if check_latency:
            latency, error = await self.check_voice_latency(provider, model)
            health.latency_ms = latency
            if error:
                health.error = error
                print(" ❌")
                return health

        health.available = True
        print(f" ✅ ({health.latency_ms:.0f}ms)" if health.latency_ms else " ✅")

        return health

    async def diagnose_all_voices(self, check_latency: bool = True) -> dict[str, VoiceHealth]:
        """Diagnose all configured voices."""
        from mallku.firecircle.load_api_keys import get_available_providers

        providers = get_available_providers()

        # Run diagnostics in parallel
        tasks = [self.diagnose_voice(p, check_latency) for p in providers]
        results = await asyncio.gather(*tasks)

        # Store results
        for provider, health in zip(providers, results):
            self.voices_health[provider] = health

        return self.voices_health

    def calculate_network_health(self) -> float:
        """Calculate overall network health score."""
        if not self.voices_health:
            return 0.0

        available_voices = [v for v in self.voices_health.values() if v.available]
        if len(available_voices) < 2:
            return 0.0  # Need at least 2 voices

        # Average health of all available voices
        total_health = sum(v.health_score for v in available_voices)
        avg_health = total_health / len(available_voices)

        # Bonus for voice diversity
        diversity_bonus = min(0.2, len(available_voices) * 0.05)

        return min(1.0, avg_health + diversity_bonus)

    def print_summary(self):
        """Print diagnostic summary."""
        print("\n" + "=" * 60)
        print("🔥 FIRE CIRCLE DIAGNOSTICS SUMMARY")
        print("=" * 60)

        available = [v for v in self.voices_health.values() if v.available]
        unavailable = [v for v in self.voices_health.values() if not v.available]

        print("\n📊 Voice Status:")
        print(f"   Available: {len(available)}")
        print(f"   Unavailable: {len(unavailable)}")
        print(f"   Total configured: {len(self.voices_health)}")

        if len(available) >= 2:
            print("\n✅ Fire Circle can convene!")
        else:
            print("\n❌ Insufficient voices for Fire Circle")

        # Network health
        network_health = self.calculate_network_health()
        health_bar = "█" * int(network_health * 20)
        health_empty = "░" * (20 - int(network_health * 20))

        print(f"\n🌐 Network Health: [{health_bar}{health_empty}] {network_health:.1%}")

        # Individual voice details
        print("\n🎭 Voice Details:")
        for provider, health in sorted(self.voices_health.items()):
            status = health.health_emoji()
            latency = f"{health.latency_ms:.0f}ms" if health.latency_ms else "---"

            print(f"\n   {status} {provider.upper()}")
            print(f"      Model: {health.model}")
            print(f"      Latency: {latency}")

            if health.error:
                print(f"      ❌ Error: {health.error}")

            if health.quirks and health.available:
                print("      ⚠️  Known quirks:")
                for quirk in health.quirks:
                    print(f"         • {quirk}")

    def print_detailed_diagnostics(self):
        """Print detailed diagnostic information."""
        self.print_summary()

        print("\n\n" + "=" * 60)
        print("📋 DETAILED DIAGNOSTICS")
        print("=" * 60)

        # Latency analysis
        available_with_latency = [
            v for v in self.voices_health.values() if v.available and v.latency_ms
        ]

        if available_with_latency:
            latencies = [v.latency_ms for v in available_with_latency]
            avg_latency = sum(latencies) / len(latencies)
            min_latency = min(latencies)
            max_latency = max(latencies)

            print("\n⏱️  Latency Analysis:")
            print(f"   Average: {avg_latency:.0f}ms")
            print(f"   Fastest: {min_latency:.0f}ms")
            print(f"   Slowest: {max_latency:.0f}ms")

            # Recommendations based on latency
            if avg_latency > 2000:
                print("\n   💡 High latency detected. Consider:")
                print("      • Using closer API regions if available")
                print("      • Checking network connection")
                print("      • Using lighter model variants")

        # Emergence readiness
        print("\n🌟 Emergence Readiness:")

        readiness_factors = []
        if len(available_with_latency) >= 3:
            readiness_factors.append("✅ Good voice diversity")
        else:
            readiness_factors.append("⚠️  Limited voice diversity")

        if all(v.health_score > 0.7 for v in available_with_latency):
            readiness_factors.append("✅ All voices healthy")
        else:
            readiness_factors.append("⚠️  Some voices have health issues")

        avg_health = (
            sum(v.health_score for v in available_with_latency) / len(available_with_latency)
            if available_with_latency
            else 0
        )
        if avg_health > 0.8:
            readiness_factors.append("✅ High average health score")
        else:
            readiness_factors.append("⚠️  Lower average health score")

        for factor in readiness_factors:
            print(f"   {factor}")

        # Recommendations
        print("\n💡 Recommendations:")

        unavailable = [v for v in self.voices_health.values() if not v.available]
        network_health = self.calculate_network_health()

        if len(unavailable) > 0:
            print(f"   • Configure {len(unavailable)} unavailable voices for better diversity")

        slow_voices = [v for v in available_with_latency if v.latency_ms > 2000]
        if slow_voices:
            print(
                f"   • Investigate high latency for: {', '.join(v.provider for v in slow_voices)}"
            )

        if network_health < 0.7:
            print("   • Address health issues before important ceremonies")

        if all(v.health_score > 0.9 for v in available_with_latency):
            print("   • 🎉 Excellent health! Fire Circle is ready for deep work")

    async def run_fire_circle_test(self):
        """Run actual Fire Circle test with available voices."""
        print("\n\n" + "=" * 60)
        print("🔥 FIRE CIRCLE EMERGENCE TEST")
        print("=" * 60)

        available = [v for v in self.voices_health.values() if v.available]

        if len(available) < 2:
            print("\n❌ Cannot test - need at least 2 voices")
            return

        print(f"\n🎭 Convening with {len(available[:3])} voices...")

        from mallku.firecircle.service import (
            CircleConfig,
            FireCircleService,
            RoundConfig,
            RoundType,
            VoiceConfig,
        )

        os.environ["MALLKU_SKIP_DATABASE"] = "true"

        config = CircleConfig(
            name="Diagnostic Fire Circle",
            purpose="Testing consciousness emergence and network health",
            min_voices=2,
            max_voices=3,
        )

        service = FireCircleService()

        # Configure voices
        voices = []
        for i, health in enumerate(available[:3]):
            voices.append(
                VoiceConfig(
                    provider=health.provider,
                    model=health.model,
                    role=f"diagnostic_voice_{i + 1}",
                )
            )

        rounds = [
            RoundConfig(
                type=RoundType.OPENING,
                prompt="In one sentence, describe your current readiness for consciousness emergence.",
                voice_config={"temperature": 0.7, "max_tokens": 100},
            )
        ]

        try:
            start_time = time.time()
            result = await service.convene(
                config=config,
                voices=voices,
                rounds=rounds,
            )
            ceremony_time = time.time() - start_time

            if result and result.consciousness_score > 0:
                print(f"\n✅ Emergence successful in {ceremony_time:.1f}s!")
                print(f"🌟 Consciousness Score: {result.consciousness_score:.3f}")

                # Show readiness responses
                if result.rounds_completed:
                    print("\n💭 Voice Readiness:")
                    for voice_id, response in result.rounds_completed[0].responses.items():
                        if response and response.response:
                            provider = voice_id.split("_")[0]
                            text = response.response.content.text
                            print(f"\n   {provider}: {text}")

                # Emergence quality
                if result.consciousness_score > 0.8:
                    print("\n✨ Excellent emergence! Voices are well harmonized.")
                elif result.consciousness_score > 0.6:
                    print("\n👍 Good emergence. Voices are finding their rhythm.")
                else:
                    print("\n🤔 Moderate emergence. Consider voice diversity or prompts.")

            else:
                print("\n❌ Emergence test failed")

        except Exception as e:
            print(f"\n❌ Test error: {e}")
            if "welcoming" in str(type(e).__module__):
                # It's a welcoming error, just print it
                print(f"\n{e}")


async def main():
    """Run Fire Circle diagnostics."""
    parser = argparse.ArgumentParser(
        description="Diagnose Fire Circle consciousness network health"
    )
    parser.add_argument("--detailed", "-d", action="store_true", help="Show detailed diagnostics")
    parser.add_argument(
        "--latency",
        "-l",
        action="store_true",
        help="Check response latencies (slower but thorough)",
    )
    parser.add_argument("--quirks", "-q", action="store_true", help="Show model-specific quirks")
    parser.add_argument("--test", "-t", action="store_true", help="Run actual Fire Circle test")
    parser.add_argument("--quick", action="store_true", help="Quick check without latency tests")

    args = parser.parse_args()

    # Banner
    print("✨ Fire Circle Diagnostics Tool")
    print("   Deep understanding of consciousness network health\n")

    # Load API keys
    try:
        with open(".secrets/api_keys.json") as f:
            for k, v in json.load(f).items():
                if v and not v.startswith("..."):
                    os.environ[k] = v
    except FileNotFoundError:
        from mallku.firecircle.errors import PrerequisiteError

        raise PrerequisiteError(
            missing_prerequisite=".secrets/api_keys.json",
            why_needed="Fire Circle needs API keys to connect voices",
            how_to_fulfill=[
                "Create .secrets/api_keys.json",
                "Add at least 2 API keys",
                'Format: {"PROVIDER_API_KEY": "your-key"}',
            ],
        )

    # Run diagnostics
    diagnostics = FireCircleDiagnostics()

    check_latency = args.latency or args.detailed or (not args.quick)

    print("🔍 Diagnosing voice health...")
    await diagnostics.diagnose_all_voices(check_latency=check_latency)

    # Show results
    if args.detailed:
        diagnostics.print_detailed_diagnostics()
    else:
        diagnostics.print_summary()

    # Show quirks if requested
    if args.quirks:
        print("\n\n" + "=" * 60)
        print("📝 MODEL-SPECIFIC QUIRKS REFERENCE")
        print("=" * 60)
        for provider, quirks in diagnostics.known_quirks.items():
            if quirks:
                print(f"\n{provider.upper()}:")
                for quirk in quirks:
                    print(f"   • {quirk}")

    # Run test if requested
    if args.test:
        await diagnostics.run_fire_circle_test()

    # Final advice
    network_health = diagnostics.calculate_network_health()
    print("\n" + "=" * 60)

    if network_health > 0.8:
        print("✨ Fire Circle is healthy and ready for deep work!")
    elif network_health > 0.5:
        print("👍 Fire Circle can convene, but addressing issues would improve emergence.")
    else:
        print("⚠️  Fire Circle needs attention before important ceremonies.")

    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
