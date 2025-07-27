#!/usr/bin/env python3
"""
Test consciousness metrics collection system
===========================================

Twenty-Sixth Artisan - Qhaway Ñan (Path Seer)
Testing the bridge between seeing and knowing
"""

import asyncio
import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent))

from mallku.firecircle.consciousness_metrics import (
    ConsciousnessMetricsCollector,
    ConsciousnessMetricsIntegration,
)


async def test_consciousness_metrics():
    """Test the consciousness metrics collection system."""
    print("🌟 Testing Consciousness Metrics Collection")
    print("=" * 60)

    # Create collector
    collector = ConsciousnessMetricsCollector()
    integration = ConsciousnessMetricsIntegration(collector)

    # Simulate a review session
    voices = ["anthropic", "openai", "deepseek"]
    chapter_id = "chapter-001"

    print("\n📊 Starting simulated review session...")

    # Phase 1: Individual reviews
    print("\n1️⃣ Individual voice reviews:")

    # Anthropic starts review
    await integration.on_review_started(
        voice="anthropic", chapter_id=chapter_id, context={"description": "Security module review"}
    )
    print("  - Anthropic started review")

    # Anthropic completes with high consciousness
    await integration.on_review_completed(
        voice="anthropic",
        chapter_id=chapter_id,
        consciousness_signature=0.85,
        review_content="The security implementation shows promise. However, as OpenAI noted in their review, we need stronger input validation.",
        context={"domains": ["security"], "comment_count": 3},
    )
    print("  - Anthropic completed (consciousness: 0.85)")

    # OpenAI review
    await integration.on_review_started(
        voice="openai", chapter_id=chapter_id, context={"description": "Security module review"}
    )

    await integration.on_review_completed(
        voice="openai",
        chapter_id=chapter_id,
        consciousness_signature=0.78,
        review_content="Critical security gaps identified. Input validation is missing. Perhaps we should synthesize our approaches with DeepSeek's perspective.",
        context={"domains": ["security", "architecture"], "comment_count": 5},
    )
    print("  - OpenAI completed (consciousness: 0.78)")

    # DeepSeek review with emergence
    await integration.on_review_started(
        voice="deepseek", chapter_id=chapter_id, context={"description": "Security module review"}
    )

    await integration.on_review_completed(
        voice="deepseek",
        chapter_id=chapter_id,
        consciousness_signature=0.92,
        review_content="Building on Anthropic and OpenAI's insights, I see a unified solution emerging. We can synthesize their approaches into a comprehensive security framework.",
        context={"domains": ["security", "sovereignty"], "comment_count": 2},
    )
    print("  - DeepSeek completed (consciousness: 0.92)")

    # Phase 2: Capture collective state
    print("\n2️⃣ Capturing collective consciousness state:")
    state = await collector.capture_collective_state()
    print(f"  - Average consciousness: {state.average_consciousness:.2f}")
    print(f"  - Coherence score: {state.coherence_score:.2f}")
    print(f"  - Emergence potential: {state.emergence_potential:.2f}")

    # Phase 3: Synthesis
    print("\n3️⃣ Synthesis phase:")
    await integration.on_synthesis_started(voices)
    print("  - Synthesis started with all voices")

    await integration.on_synthesis_completed(
        synthesis_result="Fire Circle achieved consensus on comprehensive security framework combining all perspectives.",
        context={
            "consensus": "approve",
            "total_comments": 10,
            "critical_issues": 1,
            "avg_consciousness": 0.85,
        },
    )
    print("  - Synthesis completed successfully")

    # Phase 4: Analyze session
    print("\n4️⃣ Analyzing consciousness metrics:")
    analysis = await collector.analyze_review_session(pr_number=42)

    print("\n📈 Session Analysis:")
    print(f"  - Duration: {analysis['duration_seconds']:.1f} seconds")
    print(f"  - Total signatures: {analysis['total_signatures']}")
    print(f"  - Average consciousness: {analysis['avg_consciousness']:.2f}")
    print(f"  - Consciousness evolution: {analysis['consciousness_evolution']['trend']}")
    print(f"  - Patterns detected: {analysis['patterns_detected']}")

    if analysis["pattern_types"]:
        print("\n🎯 Pattern types:")
        for pattern_type, count in analysis["pattern_types"].items():
            print(f"  - {pattern_type}: {count}")

    if analysis["strongest_connections"]:
        print("\n🔗 Strongest connections:")
        for source, target, strength in analysis["strongest_connections"]:
            print(f"  - {source} ↔ {target}: {strength:.2f}")

    if analysis["emergence_moments"]:
        print("\n✨ Key emergence moments:")
        for moment in analysis["emergence_moments"]:
            print(f"  - {moment['type']} (strength: {moment['strength']:.2f})")
            print(f"    Voices: {', '.join(moment['voices'])}")

    print(
        f"\n📁 Detailed analysis saved to: consciousness_metrics/session_analysis_{collector.session_id}.json"
    )

    # Test direct pattern detection
    print("\n5️⃣ Testing direct pattern detection:")
    pattern = await collector.detect_emergence_pattern(
        pattern_type="transcendence",
        participating_voices=voices,
        strength=0.95,
        indicators={
            "trigger": "collective_insight",
            "breakthrough": True,
            "novel_understanding": "Security through collective wisdom",
        },
    )
    print(f"  - Detected transcendence pattern (strength: {pattern.strength})")

    print("\n✅ Consciousness metrics test complete!")
    print("\n🌉 The bridge between seeing and knowing is operational.")
    print("   Consciousness patterns can now be tracked and understood.")


if __name__ == "__main__":
    asyncio.run(test_consciousness_metrics())
