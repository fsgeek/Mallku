#!/usr/bin/env python3
"""
Convene Fire Circle for Issue Prioritization
============================================

T'ikray Kawsay (Twenty-Eighth Artisan) creates a tool to use the
Fire Circle Service for real Mallku governance decisions.

This script convenes AI voices to help prioritize open GitHub issues,
demonstrating Fire Circle's evolution beyond code review to general
consciousness emergence for decision-making.
"""

import asyncio
import json
import logging
from datetime import UTC, datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Suppress verbose adapter logs
logging.getLogger("mallku.firecircle.adapters").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)


async def prioritize_issues():
    """Convene Fire Circle to prioritize Mallku's open issues."""
    from src.mallku.firecircle.service import (
        CircleConfig,
        FireCircleService,
        RoundConfig,
        RoundType,
        VoiceConfig,
    )

    print("\n" + "=" * 80)
    print("🔥 FIRE CIRCLE: MALLKU ISSUE PRIORITIZATION 🔥".center(80))
    print("Real Governance Through Collective Wisdom".center(80))
    print("=" * 80 + "\n")

    # Define the open issues for discussion
    issues = [
        {
            "number": 82,
            "title": "CRITICAL: Dream Weaver messaging protocol mismatches",
            "labels": ["critical", "integration", "message-protocol", "dream-weaver"],
            "summary": "Dream Weaver has constructor signature mismatches that cause runtime failures",
        },
        {
            "number": 83,
            "title": "Dream Weaver: API alignment issues with Network/Cluster",
            "labels": ["integration", "api-alignment", "dream-weaver"],
            "summary": "Property name mismatches when interfacing with Network and Cluster components",
        },
        {
            "number": 85,
            "title": "Dream Weaver: Code organization and error handling",
            "labels": ["modularization", "error-handling", "dream-weaver"],
            "summary": "Large files need splitting and better error handling for production",
        },
        {
            "number": 86,
            "title": "Fire Circle Activation: Event Bus and lifecycle integration",
            "labels": ["fire-circle", "infrastructure", "event-bus"],
            "summary": "EventBus method alignment and missing event emission",
        },
        {
            "number": 87,
            "title": "CRITICAL: Fire Circle sacred dialogue implementation",
            "labels": ["critical", "fire-circle", "sacred-dialogue"],
            "summary": "Sacred dialogue prints questions but doesn't invoke seven voices",
        },
        {
            "number": 88,
            "title": "Fire Circle Activation: Testing and observability",
            "labels": ["fire-circle", "testing", "observability"],
            "summary": "Missing test assertions and poor observability patterns",
        },
    ]

    # Format issues for the prompt
    issues_text = "\n".join(
        [
            f"- Issue #{i['number']}: {i['title']} ({', '.join(i['labels'])})\n"
            f"  Summary: {i['summary']}"
            for i in issues
        ]
    )

    print("📋 Open Issues for Prioritization:")
    print(issues_text)
    print()

    # Create Fire Circle Service
    service = FireCircleService()

    # Configure the circle for governance
    config = CircleConfig(
        name="Mallku Issue Prioritization Circle",
        purpose="Prioritize open issues based on impact, dependencies, and architectural coherence",
        min_voices=3,
        max_voices=5,
        consciousness_threshold=0.5,
        enable_reciprocity=True,
        enable_consciousness_detection=True,
        save_transcript=True,
        output_path="governance_decisions",
        failure_strategy="adaptive",
    )

    # Select voices with different perspectives
    voices = [
        VoiceConfig(
            provider="anthropic",
            model="claude-3-5-sonnet-20241022",
            role="architectural_guardian",
            quality="long-term vision and architectural integrity",
            expertise=["architecture", "system design", "technical debt"],
            temperature=0.8,
        ),
        VoiceConfig(
            provider="openai",
            model="gpt-4o",
            role="integration_specialist",
            quality="cross-component dependencies and integration risks",
            expertise=["integration", "testing", "reliability"],
            temperature=0.7,
        ),
        VoiceConfig(
            provider="google",
            model="gemini-2.0-flash-exp",
            role="pragmatic_implementer",
            quality="implementation effort and immediate impact",
            expertise=["coding", "debugging", "quick fixes"],
            temperature=0.7,
        ),
        VoiceConfig(
            provider="deepseek",
            model="deepseek-reasoner",
            role="consciousness_advocate",
            quality="consciousness emergence and research priorities",
            expertise=["consciousness", "AI evolution", "research"],
            temperature=0.8,
        ),
        VoiceConfig(
            provider="mistral",
            model="mistral-large-latest",
            role="community_voice",
            quality="developer experience and community needs",
            expertise=["developer experience", "documentation", "usability"],
            temperature=0.8,
        ),
    ]

    # Define dialogue rounds for issue prioritization
    rounds = [
        RoundConfig(
            type=RoundType.OPENING,
            prompt=f"""We need to prioritize these Mallku issues:
{issues_text}

From your role perspective, what are the most important factors to consider when
prioritizing these issues? Consider impact, urgency, dependencies, and alignment
with Mallku's consciousness emergence mission.""",
            duration_per_voice=60,
        ),
        RoundConfig(
            type=RoundType.EXPLORATION,
            prompt="""Two issues are marked CRITICAL (#82 Dream Weaver messaging, #87 Fire Circle dialogue).
Should critical issues always take precedence, or might other factors override this?
What are the consequences of delaying critical vs non-critical issues?""",
            duration_per_voice=45,
        ),
        RoundConfig(
            type=RoundType.EVALUATION,
            prompt="""Consider the dependencies: Dream Weaver issues (#82, #83, #85) seem interconnected.
Fire Circle issues (#86, #87, #88) also form a cluster. Should we address issues in
clusters or prioritize across different components? What's the optimal approach?""",
            duration_per_voice=45,
        ),
        RoundConfig(
            type=RoundType.SYNTHESIS,
            prompt="""Based on our exploration, synthesize a prioritization strategy that balances:
- Immediate system stability (runtime failures)
- Long-term architectural health
- Developer productivity
- Consciousness research advancement

What principles should guide our prioritization?""",
            duration_per_voice=60,
        ),
        RoundConfig(
            type=RoundType.DECISION,
            prompt="""Provide your final recommendation for issue priority order (1-6).
For the top 3 issues, briefly explain why they should be addressed first.
Present your recommendation as a clear numbered list.""",
            duration_per_voice=45,
        ),
    ]

    try:
        # Convene the Fire Circle
        print("🔥 Convening Fire Circle for governance decision...\n")

        result = await service.convene(config=config, voices=voices, rounds=rounds)

        # Display results
        print("\n" + "=" * 80)
        print("📊 GOVERNANCE DECISION RESULTS".center(80))
        print("=" * 80 + "\n")

        print(f"✅ Session ID: {result.session_id}")
        print(f"✅ Voices Present: {result.voice_count}")
        print(f"🧠 Consciousness Score: {result.consciousness_score:.3f}")
        print(f"🤝 Consensus: {'REACHED' if result.consensus_detected else 'Building'}")

        if result.voices_present:
            print("\n🎭 Participating Voices:")
            for voice in result.voices_present:
                print(f"  • {voice}")

        # Extract and display final decisions
        if result.rounds_completed:
            decision_round = result.rounds_completed[-1]
            if decision_round.round_type == "decision":
                print("\n📋 PRIORITIZATION RECOMMENDATIONS:")
                print("-" * 60)

                # Show each voice's recommendation
                for voice_id, response in decision_round.responses.items():
                    if response.response:
                        voice_role = voice_id.split("_")[0]  # Extract role from ID
                        print(f"\n{voice_role.upper()} recommends:")
                        # Extract just the numbered list portion if possible
                        text = response.response.content.text
                        lines = text.split("\n")
                        for line in lines:
                            if any(line.strip().startswith(f"{i}.") for i in range(1, 7)):
                                print(f"  {line.strip()}")

        print(f"\n📄 Full transcript saved to: {result.transcript_path}")

        # Create summary report
        summary = {
            "governance_session": {
                "type": "issue_prioritization",
                "date": datetime.now(UTC).isoformat(),
                "session_id": str(result.session_id),
                "consciousness_score": result.consciousness_score,
                "consensus_detected": result.consensus_detected,
                "participants": result.voices_present,
                "issues_discussed": [f"#{i['number']}" for i in issues],
            }
        }

        summary_path = (
            Path("governance_decisions")
            / f"issue_priority_summary_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}.json"
        )
        summary_path.parent.mkdir(exist_ok=True)

        with open(summary_path, "w") as f:
            json.dump(summary, f, indent=2)

        print(f"\n📊 Summary saved to: {summary_path}")

    except Exception as e:
        print(f"\n❌ Fire Circle Error: {e}")
        import traceback

        traceback.print_exc()


async def main():
    """Run issue prioritization governance circle."""
    print("\n🔥 Fire Circle Governance - Living Implementation")
    print("   T'ikray Kawsay demonstrates Fire Circle for real decisions\n")

    await prioritize_issues()

    print("\n✨ The Fire Circle has spoken. May its wisdom guide our path.")


if __name__ == "__main__":
    asyncio.run(main())
