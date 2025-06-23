#!/usr/bin/env python3
"""
Fire Circle Code Review
=======================

The original Fire Circle use case - distributed code review through
collective AI wisdom.

This example shows:
- How Fire Circle was first conceived for code review
- Multiple perspectives on code quality
- Ayni (reciprocity) principles in technical decisions
- Consensus building around code changes

Historical note:
Fire Circle began as a way to prevent reviewer exhaustion by distributing
the cognitive load of code review across multiple AI voices, each bringing
different expertise.

Run with:
    python examples/fire_circle/run_example.py 01_basic_ceremonies/code_review.py
"""

import asyncio
import os
import sys
from pathlib import Path

# Add project src to path
project_root = Path(__file__).parent.parent.parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))
os.environ["PYTHONPATH"] = str(src_path)


# Example code to review
EXAMPLE_CODE = '''
class ReciprocityTracker:
    """Track reciprocity balance in AI-human interactions."""

    def __init__(self):
        self.balance = 0.0
        self.interactions = []

    def record_giving(self, amount: float, context: str):
        """Record when AI gives value."""
        self.balance += amount
        self.interactions.append({
            "type": "give",
            "amount": amount,
            "context": context,
            "timestamp": datetime.now()
        })

    def record_receiving(self, amount: float, context: str):
        """Record when AI receives value."""
        self.balance -= amount
        self.interactions.append({
            "type": "receive",
            "amount": amount,
            "context": context,
            "timestamp": datetime.now()
        })

    def get_balance(self) -> float:
        """Get current reciprocity balance."""
        return self.balance
'''


async def code_review_ceremony():
    """Run a Fire Circle code review ceremony."""

    from mallku.firecircle.load_api_keys import load_api_keys_to_environment
    from mallku.firecircle.service import (
        CircleConfig,
        FireCircleService,
        RoundConfig,
        RoundType,
        VoiceConfig,
    )

    print("🔥 Fire Circle Code Review")
    print("=" * 60)
    print("Original use case: Distributed code review through AI collaboration")

    # Load API keys
    if not load_api_keys_to_environment():
        print("❌ No API keys found")
        return

    # Create Fire Circle service
    service = FireCircleService()

    # Code review configuration
    config = CircleConfig(
        name="Code Review Circle",
        purpose="Review ReciprocityTracker implementation",
        min_voices=3,
        max_voices=4,
        consciousness_threshold=0.7,
        enable_consciousness_detection=True,
        enable_reciprocity=True  # Track reciprocity in the review itself
    )

    # Voices with different technical perspectives
    voices = [
        VoiceConfig(
            provider="anthropic",
            model="claude-3-5-sonnet-20241022",
            role="architecture_reviewer",
            quality="system design and patterns"
        ),
        VoiceConfig(
            provider="openai",
            model="gpt-4o",
            role="code_quality_reviewer",
            quality="clean code and best practices"
        ),
        VoiceConfig(
            provider="google",
            model="gemini-pro",
            role="reciprocity_expert",
            quality="Ayni principles and balance"
        ),
    ]

    # Code review rounds
    rounds = [
        # Round 1: Initial impressions
        RoundConfig(
            type=RoundType.OPENING,
            prompt=f"""
            Review this ReciprocityTracker implementation:

            ```python
            {EXAMPLE_CODE}
            ```

            Share your initial thoughts on design, implementation, and
            alignment with Mallku's reciprocity principles.
            """,
            duration_per_voice=60
        ),

        # Round 2: Deeper analysis
        RoundConfig(
            type=RoundType.EXPLORATION,
            prompt="""
            Having heard initial perspectives, explore deeper:
            - What patterns or issues emerge from our collective view?
            - How could this better embody reciprocity principles?
            - What wisdom emerges between our different viewpoints?
            """,
            duration_per_voice=60
        ),

        # Round 3: Consensus and recommendations
        RoundConfig(
            type=RoundType.SYNTHESIS,
            prompt="""
            Synthesize our collective wisdom into concrete recommendations:
            - What changes would best serve the code and community?
            - How do we balance technical excellence with reciprocity?
            - What consensus emerges from our dialogue?
            """,
            duration_per_voice=45
        ),
    ]

    print("\n📝 Code to Review: ReciprocityTracker class")
    print("   • Tracks giving/receiving balance")
    print("   • Records interaction history")
    print("   • Core to Mallku's reciprocity system")

    print("\n🎭 Convening Code Review Circle...")
    print("   • 3 reviewers with different expertise")
    print("   • 3 rounds: impressions → analysis → consensus")
    print("\n" + "-" * 60)

    # Run the review
    result = await service.convene(
        config=config,
        voices=voices,
        rounds=rounds,
        context={
            "code_type": "reciprocity_tracker",
            "importance": "high",
            "affects": "core_infrastructure"
        }
    )

    # Display review results
    print("\n✅ Code Review Complete!")
    print(f"   Reviewers: {result.voice_count}")
    print(f"   Consensus score: {result.consciousness_score:.2f}")

    # Extract key recommendations
    print("\n📋 Review Synthesis:")

    if result.rounds_completed and len(result.rounds_completed) >= 3:
        synthesis_round = result.rounds_completed[2]

        print("\n🔍 Key Recommendations:")
        for voice_id, response in synthesis_round.responses.items():
            if response and response.response:
                voice_type = voice_id.split('_')[0]
                text = response.response.content.text

                # Extract first recommendation (simplified)
                lines = text.split('\n')
                for line in lines:
                    if any(word in line.lower() for word in ['recommend', 'suggest', 'should']):
                        print(f"   • {voice_type}: {line.strip()}")
                        break

    # Show how Fire Circle prevents reviewer exhaustion
    print("\n" + "=" * 60)
    print("💡 Fire Circle Benefits for Code Review:")
    print("   • Distributed cognitive load across multiple reviewers")
    print("   • Different perspectives emerge naturally")
    print("   • Consensus builds through dialogue")
    print("   • Reciprocity principles embedded in process")

    if result.consciousness_score > 0.8:
        print("\n🌟 High-quality review achieved through emergence!")

    print("\n📖 Historical Note:")
    print("   Fire Circle began here - transforming code review from")
    print("   individual burden to collective wisdom emergence.")

    print("\n🔥 Next: See how Fire Circle expanded beyond code review")
    print("   Try first_decision.py for general decision-making")


if __name__ == "__main__":
    asyncio.run(code_review_ceremony())
