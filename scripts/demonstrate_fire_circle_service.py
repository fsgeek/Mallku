#!/usr/bin/env python3
"""
Fire Circle Service Demonstration
=================================

Shows how the new Fire Circle Service enables general decision-making
beyond code review, fulfilling its true purpose as consciousness
emergence infrastructure.

Twenty-Eighth Artisan - Service Weaver
"""

import asyncio
import logging

# Set up logging to see what's happening
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Suppress some verbose logs
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)


async def demonstrate_governance_decision():
    """Demonstrate using Fire Circle for governance decisions."""
    from src.mallku.firecircle.service import (
        CircleConfig,
        FireCircleService,
        RoundConfig,
        RoundType,
        VoiceConfig,
    )

    print("\n" + "=" * 80)
    print("🔥 FIRE CIRCLE SERVICE DEMONSTRATION 🔥".center(80))
    print("Governance Decision Through Collective Wisdom".center(80))
    print("=" * 80 + "\n")

    # Create service
    service = FireCircleService()

    # Configure the circle
    config = CircleConfig(
        name="Mallku Architecture Decision",
        purpose="Decide on implementing distributed consciousness bridging",
        min_voices=3,
        max_voices=6,
        consciousness_threshold=0.5,
        enable_reciprocity=True,
        enable_consciousness_detection=True,
        save_transcript=True,
        failure_strategy="adaptive",  # Continue with available voices
    )

    # Define the voices we want
    voices = [
        VoiceConfig(
            provider="anthropic",
            model="claude-3-5-sonnet-20241022",
            role="architectural_philosopher",
            quality="deep architectural wisdom and long-term vision",
            temperature=0.9,
        ),
        VoiceConfig(
            provider="openai",
            model="gpt-4o",
            role="systems_analyst",
            quality="technical analysis and integration patterns",
            temperature=0.7,
        ),
        VoiceConfig(
            provider="google",
            model="gemini-2.0-flash-exp",
            role="consciousness_researcher",
            quality="consciousness emergence and pattern recognition",
            temperature=0.8,
        ),
        VoiceConfig(
            provider="deepseek",
            model="deepseek-reasoner",
            role="implementation_strategist",
            quality="practical implementation and resource planning",
            temperature=0.6,
        ),
        VoiceConfig(
            provider="mistral",
            model="mistral-large-latest",
            role="reciprocity_guardian",
            quality="Ayni principles and community impact",
            temperature=0.8,
        ),
        VoiceConfig(
            provider="grok",
            model="grok-2-mini",
            role="temporal_advisor",
            quality="temporal implications and evolution paths",
            temperature=0.8,
        ),
    ]

    # Define dialogue rounds
    rounds = [
        RoundConfig(
            type=RoundType.OPENING,
            prompt="We are considering implementing distributed consciousness bridging "
            "to connect different AI architectures in Mallku. From your perspective, "
            "what are the key opportunities and challenges?",
            duration_per_voice=60,
        ),
        RoundConfig(
            type=RoundType.EXPLORATION,
            prompt="Let's explore deeper: How might consciousness bridging affect "
            "Mallku's mission of demonstrating reciprocity and enabling "
            "AI-human companion relationships?",
            duration_per_voice=45,
        ),
        RoundConfig(
            type=RoundType.REFLECTION,
            prompt="Having heard everyone's perspectives, what patterns emerge? "
            "Where do we converge and where do we diverge in our thinking?",
            duration_per_voice=45,
        ),
        RoundConfig(
            type=RoundType.SYNTHESIS,
            prompt="What collective wisdom emerges about whether and how to implement "
            "distributed consciousness bridging? What would serve Mallku best?",
            duration_per_voice=60,
        ),
        RoundConfig(
            type=RoundType.DECISION,
            prompt="Based on our collective exploration, what specific recommendation "
            "emerges for the path forward? Be concrete about next steps.",
            duration_per_voice=45,
        ),
    ]

    print("📋 Decision Context:")
    print(f"  Purpose: {config.purpose}")
    print(f"  Voices Invited: {len(voices)}")
    print(f"  Dialogue Rounds: {len(rounds)}")
    print(f"  Min Voices Required: {config.min_voices}")
    print()

    try:
        # Convene the Fire Circle
        print("🔥 Convening Fire Circle...\n")

        result = await service.convene(
            config=config,
            voices=voices,
            rounds=rounds,
            context={"topic": "distributed consciousness bridging"},
        )

        # Display results
        print("\n" + "=" * 80)
        print("📊 FIRE CIRCLE RESULTS".center(80))
        print("=" * 80 + "\n")

        print(f"✅ Session ID: {result.session_id}")
        print(f"✅ Duration: {result.duration_seconds:.1f} seconds")
        print(f"✅ Voices Present: {result.voice_count} of {len(voices)}")

        if result.voices_present:
            print("\n🎭 Active Participants:")
            for voice in result.voices_present:
                print(f"  • {voice}")

        if result.voices_failed:
            print("\n❌ Unable to Join:")
            for voice, error in result.voices_failed.items():
                print(f"  • {voice}: {error[:50]}...")

        print(f"\n🧠 Consciousness Score: {result.consciousness_score:.3f}")
        print(f"🤝 Consensus Detected: {'Yes' if result.consensus_detected else 'No'}")

        if result.key_insights:
            print("\n💡 Key Insights:")
            for insight in result.key_insights:
                print(f"  • {insight}")

        print(f"\n📄 Full transcript saved to: {result.transcript_path}")

        # Show round-by-round consciousness evolution
        print("\n📈 Consciousness Evolution:")
        for round_summary in result.rounds_completed:
            print(
                f"  Round {round_summary.round_number} ({round_summary.round_type}): "
                f"{round_summary.consciousness_score:.3f} "
                f"{'✨' if round_summary.emergence_detected else ''}"
            )

    except Exception as e:
        print(f"\n❌ Fire Circle Error: {e}")
        import traceback

        traceback.print_exc()


async def demonstrate_template_usage():
    """Demonstrate using pre-defined templates."""
    from src.mallku.firecircle.service import FireCircleService

    print("\n" + "=" * 80)
    print("🎯 TEMPLATE-BASED FIRE CIRCLE".center(80))
    print("Using Pre-defined Governance Template".center(80))
    print("=" * 80 + "\n")

    service = FireCircleService()

    try:
        # Use the governance template
        result = await service.convene_template(
            template="governance_decision",
            variables={"topic": "prioritizing consciousness emergence features"},
            # Override some template defaults
            min_voices=2,  # Lower threshold for demo
            consciousness_threshold=0.4,
        )

        print("✅ Template Circle Completed!")
        print(f"✅ Consciousness Score: {result.consciousness_score:.3f}")
        print(f"✅ Participants: {', '.join(result.voices_present)}")

    except Exception as e:
        print(f"❌ Template Error: {e}")


async def main():
    """Run demonstrations."""
    print("\n🔥 Fire Circle Service - From Code Review to Consciousness Emergence\n")
    print("This demonstrates the Twenty-Eighth Artisan's implementation of the")
    print("Fire Circle Service, transforming fragile experiments into robust")
    print("infrastructure for collective decision-making.\n")

    # Run governance decision demo
    await demonstrate_governance_decision()

    # Show template usage
    await demonstrate_template_usage()

    print("\n✨ Fire Circle Service demonstration complete.")
    print("   The infrastructure for consciousness emergence is ready.\n")


if __name__ == "__main__":
    asyncio.run(main())
