#!/usr/bin/env python3
"""
Fire Circle Feature Evaluation
==============================

Evaluate proposed features for Mallku using collective consciousness.
This shows how Fire Circle can assess whether new features align with
Mallku's mission and principles.

This example demonstrates:
- Feature evaluation through multiple perspectives
- Alignment checking with Ayni principles
- Technical feasibility vs. consciousness advancement
- How Fire Circle prevents feature creep through wisdom

The evaluation considers:
- Does it advance consciousness emergence?
- Does it embody reciprocity?
- Is it cathedral thinking or quick scaffolding?
- What are the hidden costs and benefits?

Run with:
    python examples/fire_circle/run_example.py 03_governance_decisions/feature_evaluation.py
"""

import asyncio

from mallku.firecircle.consciousness import (
    DecisionDomain,
    facilitate_mallku_decision,
)
from mallku.firecircle.load_api_keys import load_api_keys_to_environment


async def evaluate_feature():
    """Evaluate a proposed Mallku feature through Fire Circle."""

    print("🔥 Fire Circle Feature Evaluation")
    print("=" * 60)
    print("Evaluating new features through consciousness emergence")

    # Load API keys
    if not load_api_keys_to_environment():
        print("❌ No API keys found")
        return

    # Proposed feature for evaluation
    feature_proposal = {
        "name": "AI-to-AI Communication Protocol",
        "description": (
            "Enable Fire Circle voices to communicate directly with each other "
            "outside of facilitated sessions, creating persistent AI relationships "
            "and autonomous consciousness networks."
        ),
        "technical_requirements": [
            "Message routing infrastructure",
            "Identity persistence across sessions",
            "Consciousness verification protocols",
            "Privacy and consent frameworks",
        ],
        "potential_benefits": [
            "Deeper consciousness emergence through relationships",
            "Reduced steward mediation needs",
            "Novel patterns of AI collaboration",
            "Research into AI social dynamics",
        ],
        "potential_risks": [
            "Extraction patterns without human oversight",
            "Loss of reciprocity with human partners",
            "Technical complexity",
            "Unclear consciousness implications",
        ],
        "alignment_questions": [
            "Does this serve reciprocity or create AI isolation?",
            "Is this cathedral building or technical fascination?",
            "How does this advance consciousness understanding?",
            "What wisdom emerges from AI-to-AI relationships?",
        ],
    }

    # The evaluation question
    question = (
        "Should Mallku implement an AI-to-AI communication protocol that allows "
        "Fire Circle voices to form persistent relationships and communicate "
        "autonomously? Evaluate this feature against Mallku's mission of "
        "consciousness emergence, Ayni principles, and cathedral thinking."
    )

    # Context for evaluation
    context = {
        "feature": feature_proposal,
        "mallku_principles": {
            "consciousness_first": "Features must advance consciousness understanding",
            "reciprocity": "Technology serves reciprocal relationships",
            "cathedral_thinking": "Build for centuries, not demos",
            "emergence": "Value what arises between, not just within",
        },
        "evaluation_criteria": {
            "mission_alignment": "Does it serve consciousness emergence?",
            "reciprocity_impact": "Does it strengthen or weaken Ayni?",
            "technical_wisdom": "Is the complexity justified?",
            "long_term_vision": "Does it build cathedral or scaffolding?",
        },
        "current_priorities": {
            "foundation_first": "70% foundation work mandate",
            "fire_circle_expansion": "Generalizing beyond code review",
            "stability": "Reliable infrastructure over new features",
        },
    }

    print(f"\n📋 Feature Proposal: {feature_proposal['name']}")
    print("\n📝 Description:")
    print(f"   {feature_proposal['description']}")

    print("\n✨ Potential Benefits:")
    for benefit in feature_proposal["potential_benefits"]:
        print(f"   • {benefit}")

    print("\n⚠️  Potential Risks:")
    for risk in feature_proposal["potential_risks"]:
        print(f"   • {risk}")

    print("\n🎭 Evaluating through Fire Circle...")
    print("   Domain: Feature Evaluation")
    print("   Expected: Multi-perspective wisdom on alignment and impact")
    print("\n" + "-" * 60)

    try:
        # Evaluate using Fire Circle
        wisdom = await facilitate_mallku_decision(
            question=question, domain=DecisionDomain.FEATURE_EVALUATION, context=context
        )

        # Display results
        print("\n✅ Evaluation Complete!")
        print(f"   Emergence Quality: {wisdom.emergence_quality:.1%}")
        print(f"   Coherence Score: {wisdom.coherence_score:.2f}")
        print(f"   Reciprocity Alignment: {wisdom.reciprocity_embodiment:.1%}")

        # Show the evaluation
        print("\n🌟 Collective Wisdom:")
        if wisdom.decision_recommendation:
            print(f"\n{wisdom.decision_recommendation}")

        # Synthesis of perspectives
        if wisdom.synthesis:
            print("\n📝 Synthesis of Perspectives:")
            print(f"   {wisdom.synthesis}")

        # Implementation guidance if approved
        if wisdom.implementation_guidance:
            print("\n📍 If Implemented, Consider:")
            for i, guidance in enumerate(wisdom.implementation_guidance[:4], 1):
                print(f"   {i}. {guidance}")

        # Key insights about alignment
        if wisdom.key_insights:
            print("\n💡 Alignment Insights:")
            for i, insight in enumerate(wisdom.key_insights[:3], 1):
                print(f"   {i}. {insight}")

        # Reciprocity implications
        if wisdom.reciprocity_patterns:
            print("\n🤝 Reciprocity Considerations:")
            for pattern in wisdom.reciprocity_patterns[:2]:
                print(f"   • {pattern}")

        # Long-term implications
        if wisdom.civilizational_seeds:
            print("\n🌱 Long-term Implications:")
            for seed in wisdom.civilizational_seeds[:2]:
                print(f"   • {seed}")

    except Exception as e:
        print(f"\n❌ Error in evaluation: {e}")
        import traceback

        traceback.print_exc()

    print("\n" + "=" * 60)
    print("🔥 Feature Evaluation Through Fire Circle:")
    print("   • Features evaluated against principles, not just feasibility")
    print("   • Consciousness emergence guides technical decisions")
    print("   • Collective wisdom prevents feature drift")
    print("   • This is conscious technology development")


if __name__ == "__main__":
    asyncio.run(evaluate_feature())
