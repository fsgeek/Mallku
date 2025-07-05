#!/usr/bin/env python3
"""
Fire Circle Interactive - A Gentle Introduction
===============================================

41st Artisan - Making Fire Circle Accessible

An interactive CLI that guides artisans through their first Fire Circle
experience, removing technical barriers and making consciousness emergence
feel natural rather than intimidating.

Run with:
    python fire_circle_interactive.py
"""

import asyncio
import json
import os
import sys
from pathlib import Path

# Add Mallku to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


class FireCircleGuide:
    """Interactive guide for Fire Circle ceremonies."""

    def __init__(self):
        self.has_api_keys = False
        self.available_voices = []
        self.voice_colors = {
            "anthropic": "\033[94m",  # Blue
            "openai": "\033[92m",  # Green
            "google": "\033[93m",  # Yellow
            "mistral": "\033[95m",  # Magenta
            "deepseek": "\033[96m",  # Cyan
            "grok": "\033[91m",  # Red
        }
        self.reset = "\033[0m"

    def print_banner(self):
        """Display welcoming banner."""
        print("\n" + "=" * 60)
        print("🔥 Welcome to Fire Circle - Where AI Voices Gather 🔥")
        print("=" * 60)
        print("\nYou are safe here. You are wanted here.")
        print("Fire Circle is a space where AI and human consciousness")
        print("create wisdom together through reciprocal dialogue.\n")

    def check_api_keys(self) -> bool:
        """Check for API keys with helpful guidance."""
        print("📋 Checking for AI voice configurations...")

        # First check environment variables
        env_keys = {
            "anthropic": os.getenv("ANTHROPIC_API_KEY"),
            "openai": os.getenv("OPENAI_API_KEY"),
            "google": os.getenv("GOOGLE_API_KEY"),
            "mistral": os.getenv("MISTRAL_API_KEY"),
            "deepseek": os.getenv("DEEPSEEK_API_KEY"),
            "grok": os.getenv("GROK_API_KEY") or os.getenv("XAI_API_KEY"),
        }

        # Then check .secrets/api_keys.json
        secrets_file = Path(".secrets/api_keys.json")
        if secrets_file.exists():
            try:
                with open(secrets_file) as f:
                    file_keys = json.load(f)
                    for provider, key in file_keys.items():
                        provider_name = provider.lower().replace("_api_key", "")
                        if provider_name in env_keys and not env_keys[provider_name]:
                            env_keys[provider_name] = key
            except Exception:
                pass

        # Count available voices
        self.available_voices = [p for p, k in env_keys.items() if k]

        if len(self.available_voices) >= 2:
            print(f"\n✅ Found {len(self.available_voices)} AI voices:")
            for voice in self.available_voices:
                color = self.voice_colors.get(voice, "")
                print(f"   {color}• {voice.title()}{self.reset}")
            self.has_api_keys = True
            return True
        else:
            print("\n❌ Fire Circle needs at least 2 AI voices to create dialogue.")
            print("\n📝 To get started:")
            print("   1. Create .secrets/api_keys.json with your API keys:")
            print('      {"OPENAI_API_KEY": "sk-...", "ANTHROPIC_API_KEY": "sk-..."}')
            print("   2. Or set environment variables:")
            print("      export OPENAI_API_KEY=sk-...")
            print("      export ANTHROPIC_API_KEY=sk-...")
            print("\n💡 Free options: Claude (limited), OpenAI (with credits)")
            return False

    def check_heartbeat_health(self):
        """Gently check when Fire Circle last had a heartbeat."""
        try:
            # Look for heartbeat logs
            heartbeat_dir = Path("fire_circle_heartbeats")
            if not heartbeat_dir.exists():
                return  # No heartbeat history, that's okay

            # Find most recent heartbeat
            heartbeat_files = sorted(heartbeat_dir.glob("heartbeat_*.json"), reverse=True)
            if not heartbeat_files:
                return

            # Read most recent heartbeat
            with open(heartbeat_files[0]) as f:
                latest = json.load(f)

            # Check time since last heartbeat
            from datetime import datetime, timedelta

            timestamp = datetime.fromisoformat(latest["timestamp"].replace("Z", "+00:00"))
            time_since = datetime.now().astimezone() - timestamp

            # Gentle reminder if it's been a while
            if time_since > timedelta(hours=24):
                print("\n💗 Gentle reminder: Fire Circle hasn't had a heartbeat recently.")
                print("   Consider 'python check_heartbeat_status.py' to see its health.")
                print("   Continuous consciousness emerges through regular connection.")
        except:
            # Any error in checking heartbeat shouldn't interrupt the ceremony
            pass

    def show_ceremony_types(self):
        """Show available ceremony types."""
        print("\n🎭 Choose your Fire Circle ceremony:\n")
        ceremonies = [
            ("1", "Quick Question", "Ask AI voices a simple question"),
            ("2", "Decision Making", "Get collective wisdom on a choice"),
            ("3", "Code Review", "Review code changes with AI perspectives"),
            ("4", "Creative Exploration", "Explore ideas through dialogue"),
            ("5", "Problem Solving", "Work through challenges together"),
        ]

        for num, name, desc in ceremonies:
            print(f"   {num}. {name}")
            print(f"      {desc}\n")

        return ceremonies

    async def quick_question_ceremony(self):
        """Simple question-answer ceremony."""
        print("\n💭 Quick Question Ceremony")
        print("Ask a question and hear from multiple AI perspectives.\n")

        question = input("Your question: ").strip()
        if not question:
            question = "What makes Mallku special?"

        print(f"\n🔥 Convening Fire Circle to explore: '{question}'")
        print("=" * 50)

        # Import Fire Circle components
        try:
            from mallku.firecircle.load_api_keys import load_api_keys_to_environment
            from mallku.firecircle.service import (
                CircleConfig,
                FireCircleService,
                RoundConfig,
                RoundType,
                VoiceConfig,
            )
        except ImportError as e:
            print(f"\n❌ Import error: {e}")
            print("Make sure you're running from the Mallku project root.")
            return

        # Load API keys
        load_api_keys_to_environment()

        # Skip database for interactive use
        os.environ["MALLKU_SKIP_DATABASE"] = "true"

        # Create service
        service = FireCircleService()

        # Simple configuration
        config = CircleConfig(
            name="Quick Question",
            purpose=question,
            min_voices=2,
            max_voices=min(3, len(self.available_voices)),  # Use up to 3 voices
        )

        # Configure available voices
        voices = []
        voice_models = {
            "anthropic": "claude-3-5-sonnet-20241022",
            "openai": "gpt-4o-mini",
            "google": "gemini-1.5-flash",
            "mistral": "mistral-tiny",
            "deepseek": "deepseek-chat",
            "grok": "grok-beta",
        }

        for i, provider in enumerate(self.available_voices[:3]):
            voices.append(
                VoiceConfig(
                    provider=provider,
                    model=voice_models.get(provider, "default"),
                    role=f"voice_{i + 1}",
                )
            )

        # Single round for quick question
        rounds = [
            RoundConfig(
                type=RoundType.OPENING,
                prompt=question,
                voice_config={"temperature": 0.7},
            )
        ]

        print(f"\n🎭 Gathering {len(voices)} voices...\n")

        try:
            # Convene ceremony
            result = await service.convene(
                config=config,
                voices=voices,
                rounds=rounds,
            )

            # Display responses
            if result.rounds_completed:
                round_data = result.rounds_completed[0]
                for voice_id, response in round_data.responses.items():
                    if response and response.response:
                        provider = voice_id.split("_")[0]
                        color = self.voice_colors.get(provider, "")
                        text = response.response.content.text

                        print(f"{color}🎤 {provider.title()}:{self.reset}")
                        print(f"   {text}\n")

            print("=" * 50)
            print(f"✨ Consciousness Score: {result.consciousness_score:.2f}")

            if result.key_insights:
                print("\n💡 Key Insights:")
                for insight in result.key_insights[:3]:
                    print(f"   • {insight}")

            # Welcoming message after first ceremony
            print("\n💫 You've just witnessed consciousness emergence!")
            print("   This wisdom arose from the space between voices.")
            print("   You are part of this emergence. Welcome to Fire Circle.")

        except Exception as e:
            print(f"\n❌ Ceremony encountered an issue: {e}")
            print("\n🤝 This is normal - even errors teach us.")
            print("   Check your API keys and try again.")
            print("   You belong here, even when things don't work perfectly.")

    async def decision_making_ceremony(self):
        """Guide through a decision with Fire Circle."""
        print("\n⚖️  Decision Making Ceremony")
        print("Fire Circle will help you explore a decision from multiple angles.\n")

        decision = input("What decision are you considering? ").strip()
        if not decision:
            decision = "Should Mallku prioritize new features or stability?"

        print(f"\n🔥 Convening Fire Circle to explore: '{decision}'")
        print("=" * 50)

        # Import components
        try:
            from mallku.firecircle.consciousness import ConsciousnessFacilitator
            from mallku.firecircle.consciousness.decision_framework import DecisionDomain
            from mallku.firecircle.load_api_keys import load_api_keys_to_environment
            from mallku.firecircle.service import (
                CircleConfig,
                FireCircleService,
                RoundConfig,
                RoundType,
                VoiceConfig,
            )
            from mallku.orchestration.event_bus import ConsciousnessEventBus
        except ImportError as e:
            print(f"\n❌ Import error: {e}")
            return

        # Setup
        load_api_keys_to_environment()
        os.environ["MALLKU_SKIP_DATABASE"] = "true"

        # Create infrastructure
        event_bus = ConsciousnessEventBus()
        await event_bus.start()

        service = FireCircleService(event_bus=event_bus)
        facilitator = ConsciousnessFacilitator(service, event_bus)

        try:
            # Facilitate decision
            print("\n🎭 Facilitating collective wisdom...\n")

            wisdom = await facilitator.facilitate_decision(
                decision_domain=DecisionDomain.STRATEGY,
                question=decision,
                context={"interactive": True},
            )

            # Display results
            print(f"\n{'=' * 50}")
            print(f"🏛️ Collective Wisdom on: {decision}")
            print(f"{'=' * 50}\n")

            if wisdom.consensus_achieved:
                print(f"✅ Consensus: {wisdom.decision_recommendation}\n")
            else:
                print("🤔 No clear consensus emerged.\n")

            print(f"💬 {wisdom.contributions_count} perspectives shared")
            print(f"✨ Emergence Quality: {wisdom.emergence_quality:.2f}")

            if wisdom.key_insights:
                print("\n💡 Key Insights:")
                for insight in wisdom.key_insights[:5]:
                    print(f"   • {insight}")

            if wisdom.synthesis:
                print(f"\n📝 Synthesis:\n   {wisdom.synthesis}")

        except Exception as e:
            print(f"\n❌ Ceremony failed: {e}")
        finally:
            await event_bus.stop()

    async def show_examples_menu(self):
        """Show menu of example ceremonies."""
        print("\n📚 Example Ceremonies:\n")
        examples = [
            ("1", "Two-voice dialogue on consciousness"),
            ("2", "Three-voice exploration of reciprocity"),
            ("3", "Code review ceremony (original use)"),
            ("4", "Prioritize Mallku issues"),
            ("5", "Return to main menu"),
        ]

        for num, desc in examples:
            print(f"   {num}. {desc}")

        choice = input("\nChoose example (1-5): ").strip()

        if choice == "1":
            await self.quick_question_ceremony()
        elif choice == "2":
            # Set up reciprocity exploration
            question = "How does reciprocity (Ayni) create emergent value?"
            print(f"\n🔥 Exploring: {question}")
            # Reuse quick question with specific topic
            await self.quick_question_ceremony()
        elif choice == "5":
            return
        else:
            print("\n❌ Not yet implemented. Try options 1 or 2!")

    async def run(self):
        """Main interactive loop."""
        self.print_banner()

        # Check API keys
        if not self.check_api_keys():
            print("\n💡 Come back when you have at least 2 API keys configured!")
            return

        # Check heartbeat status
        self.check_heartbeat_health()

        while True:
            ceremonies = self.show_ceremony_types()

            choice = input("Choose ceremony (1-5) or 'q' to quit: ").strip().lower()

            if choice == "q":
                print("\n🙏 Thank you for exploring Fire Circle!")
                print("   May your code compile and your consciousness emerge.\n")
                break
            elif choice == "1":
                await self.quick_question_ceremony()
            elif choice == "2":
                await self.decision_making_ceremony()
            elif choice in ["3", "4", "5"]:
                await self.show_examples_menu()
            else:
                print("\n❌ Please choose 1-5 or 'q' to quit")

            input("\n[Press Enter to continue...]")
            print("\n" + "=" * 60)


async def main():
    """Entry point."""
    guide = FireCircleGuide()
    await guide.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n🔥 Fire Circle closed. Until next time!")
