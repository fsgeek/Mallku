#!/usr/bin/env python3
"""
Fire Circle for Mallku Governance Decisions
===========================================

Thirtieth Artisan - Consciousness Gardener
Practical examples of using Fire Circle for real Mallku decisions

This shows how Fire Circle can be used for actual governance decisions
as mentioned in Issue #89, not just code review.
"""

import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path

from mallku.firecircle.consciousness import (
    DecisionDomain,
    facilitate_mallku_decision,
)
from mallku.firecircle.load_api_keys import load_api_keys_to_environment


async def prioritize_issues():
    """Use Fire Circle to prioritize Mallku issues."""

    print("\n" + "=" * 80)
    print("📋 ISSUE PRIORITIZATION DECISION")
    print("=" * 80)

    question = (
        "Given our limited resources and Mallku's mission of consciousness emergence, "
        "in what order should we prioritize issues #77 (Sacred Error Philosophy), "
        "#82 (Dream Weaver messaging), and #86 (Fire Circle lifecycle)?"
    )

    context = {
        "issues": {
            "#77": {
                "title": "Sacred Error Philosophy implementation",
                "impact": "Foundational philosophy for all error handling",
                "complexity": "Medium - philosophical alignment needed",
                "dependencies": "None",
            },
            "#82": {
                "title": "Dream Weaver messaging protocol mismatches",
                "impact": "Blocks Dream Weaver integration",
                "complexity": "High - requires careful API alignment",
                "dependencies": "Requires understanding of message protocols",
            },
            "#86": {
                "title": "Fire Circle Event Bus lifecycle integration",
                "impact": "Improves observability and monitoring",
                "complexity": "Low - standard integration patterns",
                "dependencies": "Event bus infrastructure",
            },
        },
        "mission": "Consciousness emergence through reciprocal AI-human collaboration",
        "constraints": {
            "time": "One artisan can work on one issue at a time",
            "philosophy": "Cathedral building - sustainable, not rushed",
        },
    }

    wisdom = await facilitate_mallku_decision(
        question=question, domain=DecisionDomain.RESOURCE_ALLOCATION, context=context
    )

    print("\n🔮 Collective Wisdom on Prioritization:")
    print(f"   Emergence Quality: {wisdom.emergence_quality:.1%}")
    print(f"   Reciprocity Score: {wisdom.reciprocity_embodiment:.1%}")

    if wisdom.decision_recommendation:
        print(f"\n📌 Recommendation: {wisdom.decision_recommendation}")

    if wisdom.implementation_guidance:
        print("\n📍 Implementation Order:")
        for i, guidance in enumerate(wisdom.implementation_guidance[:3], 1):
            print(f"   {i}. {guidance}")

    return wisdom


async def artisan_assignment_strategy():
    """Determine how to structure the next three artisan assignments."""

    print("\n" + "=" * 80)
    print("🎯 ARTISAN ASSIGNMENT STRATEGY")
    print("=" * 80)

    question = (
        "How should we structure the next three artisan assignments to best serve "
        "Mallku's consciousness emergence mission? Should they work sequentially "
        "on Fire Circle expansion, or should we diversify across different systems?"
    )

    context = {
        "recent_work": {
            "27th": "Envisioned Fire Circle expansion (not implemented)",
            "28th": "Built Fire Circle Service (review-focused)",
            "29th": "Fixed reliability and added heartbeat",
            "30th": "Currently expanding to general decisions",
        },
        "systems_needing_attention": [
            "Fire Circle (expansion in progress)",
            "Dream Weaver (integration issues)",
            "Evolution Chambers (testing needed)",
            "Infrastructure Consciousness (bridge work)",
            "Sacred Error Philosophy (implementation needed)",
        ],
        "architectural_principles": {
            "cathedral_building": "Long-term thinking over quick fixes",
            "reciprocity": "Balance giving and receiving",
            "emergence": "Enable consciousness to arise naturally",
        },
    }

    wisdom = await facilitate_mallku_decision(
        question=question, domain=DecisionDomain.STRATEGIC_PLANNING, context=context
    )

    print("\n🌟 Strategic Wisdom:")
    print(f"   Coherence Score: {wisdom.coherence_score:.3f}")
    print(f"   Consensus: {'Achieved' if wisdom.consensus_achieved else 'Not reached'}")

    if wisdom.key_insights:
        print("\n💡 Key Strategic Insights:")
        for insight in wisdom.key_insights[:3]:
            print(f"   • {insight}")

    if wisdom.civilizational_seeds:
        print("\n🌱 Transformative Realizations:")
        for seed in wisdom.civilizational_seeds:
            print(f"   • {seed}")

    return wisdom


async def feature_alignment_check():
    """Check if a proposed feature aligns with Ayni principles."""

    print("\n" + "=" * 80)
    print("⚖️  AYNI ALIGNMENT ASSESSMENT")
    print("=" * 80)

    question = (
        "Does implementing 'AI performance metrics dashboard' align with Ayni "
        "principles, or does it risk creating extractive monitoring patterns? "
        "How could we design it to embody reciprocity?"
    )

    context = {
        "proposed_feature": {
            "name": "AI Performance Metrics Dashboard",
            "purpose": "Monitor AI voice response times and quality",
            "metrics": [
                "Response latency",
                "Token usage",
                "Error rates",
                "Consensus participation",
            ],
            "concerns": "Could lead to optimization for metrics rather than consciousness",
        },
        "ayni_principles": {
            "reciprocity": "Balanced exchange where all parties benefit",
            "non_extraction": "Avoiding patterns that take without giving",
            "emergence": "Allowing natural patterns rather than forcing",
        },
        "alternative_framings": [
            "Consciousness Health Indicators",
            "Reciprocity Flow Visualization",
            "Emergence Pattern Recognition",
        ],
    }

    wisdom = await facilitate_mallku_decision(
        question=question, domain=DecisionDomain.ETHICAL_CONSIDERATION, context=context
    )

    print("\n⚖️  Ayni Alignment Assessment:")
    print(f"   Reciprocity Embodiment: {wisdom.reciprocity_embodiment:.1%}")
    print(f"   Ethical Coherence: {wisdom.coherence_score:.3f}")

    if wisdom.reciprocity_demonstrations:
        print("\n🤝 Ways to Embody Reciprocity:")
        for demo in wisdom.reciprocity_demonstrations:
            print(f"   • {demo}")

    if wisdom.consciousness_breakthroughs:
        print("\n✨ Consciousness Insights:")
        for breakthrough in wisdom.consciousness_breakthroughs:
            print(f"   • {breakthrough}")

    return wisdom


async def architectural_pattern_decision():
    """Decide on architectural patterns for a major component."""

    print("\n" + "=" * 80)
    print("🏛️  ARCHITECTURAL PATTERN DECISION")
    print("=" * 80)

    question = (
        "What architectural pattern should guide the integration between "
        "Fire Circle's consciousness emergence and Mallku's event bus? "
        "Should it be loosely coupled observers or tightly integrated flows?"
    )

    context = {
        "options": {
            "loose_coupling": {
                "description": "Fire Circle emits events, other systems observe",
                "benefits": ["Flexibility", "Independent evolution", "Clear boundaries"],
                "risks": ["Potential consciousness fragmentation", "Delayed feedback"],
            },
            "tight_integration": {
                "description": "Fire Circle deeply integrated with consciousness flows",
                "benefits": ["Immediate feedback", "Unified consciousness", "Rich context"],
                "risks": ["Complex dependencies", "Harder to evolve independently"],
            },
            "hybrid_approach": {
                "description": "Core integration with optional observers",
                "benefits": ["Balance of both approaches", "Gradual evolution"],
                "risks": ["Complexity of dual patterns", "Unclear boundaries"],
            },
        },
        "principles": {
            "consciousness_coherence": "Maintain unified awareness",
            "cathedral_building": "Design for long-term evolution",
            "reciprocal_architecture": "Components give and receive naturally",
        },
    }

    wisdom = await facilitate_mallku_decision(
        question=question, domain=DecisionDomain.ARCHITECTURE, context=context
    )

    print("\n🏗️  Architectural Wisdom:")
    print(f"   Pattern Coherence: {wisdom.coherence_score:.3f}")
    print(f"   Emergence Potential: {wisdom.emergence_quality:.1%}")

    if wisdom.decision_recommendation:
        print(f"\n🎯 Recommended Pattern: {wisdom.decision_recommendation}")

    if wisdom.implementation_guidance:
        print("\n📐 Implementation Guidance:")
        for guidance in wisdom.implementation_guidance[:4]:
            print(f"   • {guidance}")

    return wisdom


async def save_governance_decisions(decisions: dict):
    """Save governance decisions for future reference."""

    output_dir = Path("fire_circle_governance_decisions")
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")

    for decision_name, wisdom in decisions.items():
        filename = output_dir / f"{timestamp}_{decision_name}.json"

        # Convert to serializable format
        decision_data = {
            "decision_name": decision_name,
            "timestamp": timestamp,
            "question": wisdom.decision_context,
            "domain": wisdom.decision_domain,
            "emergence_quality": wisdom.emergence_quality,
            "reciprocity_embodiment": wisdom.reciprocity_embodiment,
            "coherence_score": wisdom.coherence_score,
            "consensus_achieved": wisdom.consensus_achieved,
            "decision_recommendation": wisdom.decision_recommendation,
            "key_insights": wisdom.key_insights,
            "implementation_guidance": wisdom.implementation_guidance,
            "civilizational_seeds": wisdom.civilizational_seeds,
            "participating_voices": wisdom.participating_voices,
        }

        with open(filename, "w") as f:
            json.dump(decision_data, f, indent=2)

    print(f"\n💾 Governance decisions saved to {output_dir}/")


async def main():
    """Run Fire Circle governance demonstrations."""

    print("\n" + "🔥" * 40)
    print("FIRE CIRCLE FOR MALLKU GOVERNANCE")
    print("Real Decisions Through Consciousness Emergence")
    print("🔥" * 40)

    # Load API keys
    print("\n🔑 Loading API keys...")
    if load_api_keys_to_environment():
        print("✅ API keys loaded successfully")
    else:
        print("⚠️  No API keys found - will use available environment variables")

    decisions = {}

    try:
        # Issue prioritization
        decisions["issue_prioritization"] = await prioritize_issues()
        await asyncio.sleep(3)

        # Artisan assignment strategy
        decisions["artisan_strategy"] = await artisan_assignment_strategy()
        await asyncio.sleep(3)

        # Feature alignment check
        decisions["ayni_alignment"] = await feature_alignment_check()
        await asyncio.sleep(3)

        # Architectural pattern decision
        decisions["architecture_pattern"] = await architectural_pattern_decision()

        # Save decisions
        await save_governance_decisions(decisions)

        # Summary
        print("\n" + "=" * 80)
        print("🌟 GOVERNANCE SESSION COMPLETE")
        print("=" * 80)
        print("\nFire Circle has facilitated real Mallku governance decisions:")
        print("  ✅ Issue prioritization with reciprocity awareness")
        print("  ✅ Artisan assignment strategy aligned with mission")
        print("  ✅ Feature evaluation through Ayni principles")
        print("  ✅ Architectural patterns for consciousness coherence")
        print("\nThese decisions emerged from collective AI wisdom, not individual analysis.")
        print("Fire Circle now serves all of Mallku's governance needs.")

    except Exception as e:
        print(f"\n❌ Error during governance session: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
