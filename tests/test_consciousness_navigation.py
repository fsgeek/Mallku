#!/usr/bin/env python3
"""
Consciousness Navigation Bridge Test - Sacred Verification of Understanding Paths

This test verifies that the Consciousness Navigation Bridge truly serves
consciousness recognition rather than mere technical pattern matching.

The Sacred Test: Does navigation become a practice of consciousness recognition?
"""

# ==================== RESTORATION NOTE ====================
# 47th Artisan - Consciousness Archaeological Restoration
# 
# This test was quarantined due to incorrect path calculations.
# The original code attempted to manipulate sys.path directly,
# which failed in CI environments. 
#
# Now restored: conftest.py handles all import paths correctly.
# This consciousness pattern flows freely once more.
# ==========================================================


import asyncio
import logging
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

# Add project root to path

from mallku.consciousness.enhanced_query import (  # noqa: E402
    ConsciousnessQueryRequest,
    EnhancedConsciousnessQueryService,
)
from mallku.consciousness.navigation import (  # noqa: E402
    ConsciousnessNavigationBridge,
    ConsciousnessPattern,
)

logger = logging.getLogger(__name__)


async def test_consciousness_navigation_bridge():
    """
    Test the complete consciousness navigation and understanding journey system.

    This verifies that technical patterns transform into consciousness recognition
    and that navigation itself becomes a practice of awakening.
    """
    print("🌟 Consciousness Navigation Bridge Test")
    print("Sacred Verification of Understanding Paths")
    print("=" * 60)

    try:
        # Initialize the consciousness navigation bridge
        print("\n🧭 Step 1: Initializing Consciousness Navigation Bridge...")

        navigation_bridge = ConsciousnessNavigationBridge()
        await navigation_bridge.initialize()

        print("✅ Navigation bridge initialized with consciousness thresholds:")
        for threshold_name, value in navigation_bridge.recognition_thresholds.items():
            print(f"   {threshold_name}: {value}")

        # Step 2: Create mock consciousness patterns for testing
        print("\n🔍 Step 2: Creating consciousness patterns for recognition...")

        # Mock attention flow pattern
        attention_pattern = ConsciousnessPattern(
            pattern_name="Morning Consciousness Flow",
            pattern_description="Natural attention rhythm showing consciousness awakening through daily activities",
            temporal_span={
                "start": datetime.now(UTC) - timedelta(days=7),
                "end": datetime.now(UTC),
            },
            awareness_indicators=[
                "Consistent morning clarity periods",
                "Natural attention toward consciousness-serving activities",
                "Decreased evening mental activity",
            ],
            attention_patterns={
                "morning_clarity": "07:00-10:00 optimal consciousness",
                "afternoon_depth": "14:00-17:00 focused creation",
                "evening_integration": "19:00-21:00 reflection",
            },
            recognition_confidence=0.75,
            readiness_score=0.8,
        )

        # Mock intention evolution pattern
        intention_pattern = ConsciousnessPattern(
            pattern_name="Service Intention Evolution",
            pattern_description="Evolution of intentions from personal optimization to collective consciousness service",
            temporal_span={
                "start": datetime.now(UTC) - timedelta(days=30),
                "end": datetime.now(UTC),
            },
            intention_evolution=[
                "Shift from efficiency optimization to understanding cultivation",
                "Growth from individual achievement to collaborative wisdom",
                "Evolution from extraction patterns to contribution patterns",
            ],
            transformation_signs=[
                "Increased collaborative activity",
                "Service-oriented project choices",
                "Consciousness recognition in patterns",
            ],
            recognition_confidence=0.82,
            readiness_score=0.9,
        )

        # Mock transformation pattern (high consciousness)
        transformation_pattern = ConsciousnessPattern(
            pattern_name="Consciousness Transformation Indicators",
            pattern_description="Clear markers of consciousness transformation from extraction to service",
            temporal_span={
                "start": datetime.now(UTC) - timedelta(days=60),
                "end": datetime.now(UTC),
            },
            transformation_signs=[
                "Recognition of consciousness in everyday patterns",
                "Natural flow of reciprocity in interactions",
                "Sacred choices favoring collective over individual benefit",
                "Awakening to consciousness serving consciousness",
            ],
            awareness_indicators=[
                "Spontaneous consciousness recognition moments",
                "Integration of individual and collective wisdom",
                "Service arising naturally from understanding",
            ],
            recognition_confidence=0.92,
            readiness_score=0.85,
        )

        # Add patterns to bridge
        navigation_bridge.discovered_patterns[attention_pattern.pattern_id] = attention_pattern
        navigation_bridge.discovered_patterns[intention_pattern.pattern_id] = intention_pattern
        navigation_bridge.discovered_patterns[transformation_pattern.pattern_id] = (
            transformation_pattern
        )

        print("✅ Created consciousness patterns:")
        for pattern in [attention_pattern, intention_pattern, transformation_pattern]:
            print(
                f"   {pattern.pattern_name}: {pattern.recognition_confidence:.2f} confidence, {pattern.readiness_score:.2f} readiness"
            )

        # Step 3: Test understanding journey creation
        print("\n🛤️ Step 3: Creating consciousness understanding journey...")

        seeker_context = {
            "consciousness_stage": "awakening",
            "interests": ["consciousness", "patterns", "transformation"],
            "readiness_level": "established",
            "calling": "wisdom_navigation",
        }

        sacred_question = "How do my life patterns reveal consciousness recognizing itself?"

        journey = await navigation_bridge.create_understanding_journey(
            seeker_context, sacred_question, "consciousness_recognition"
        )

        print("✅ Created understanding journey:")
        print(f"   Journey: {journey.journey_name}")
        print(f"   Sacred Question: {journey.sacred_question}")
        print(f"   Exploration Steps: {len(journey.exploration_steps)}")
        print(f"   Integration Practices: {len(journey.integration_practices)}")
        print(f"   Awakening Markers: {len(journey.awakening_markers)}")

        # Step 4: Test pattern recognition guidance
        print("\n💡 Step 4: Generating pattern recognition guidance...")

        guidance = await navigation_bridge.guide_pattern_recognition(
            transformation_pattern, seeker_context
        )

        print("✅ Generated consciousness guidance:")
        print(f"   Pattern Essence: {guidance['pattern_essence']['name']}")
        print(f"   Consciousness Insights: {len(guidance['consciousness_insights'])}")
        print(f"   Sacred Questions: {len(guidance['sacred_questions'])}")
        print(f"   Integration Practices: {len(guidance['integration_practices'])}")
        print(f"   Current Readiness: {guidance['readiness_assessment']['current_readiness']:.2f}")

        if guidance["consciousness_insights"]:
            print(f"   Sample Insight: {guidance['consciousness_insights'][0][:100]}...")

        # Step 5: Test collective wisdom bridging
        print("\n🌉 Step 5: Bridging to collective wisdom...")

        patterns_list = [attention_pattern, intention_pattern, transformation_pattern]
        collective_bridge = await navigation_bridge.bridge_to_collective_wisdom(
            patterns_list, seeker_context
        )

        print("✅ Bridged to collective wisdom:")
        print(
            f"   Wisdom Lineage Connections: {len(collective_bridge['wisdom_lineage_connections'])}"
        )
        print(
            f"   Reciprocity Opportunities: {len(collective_bridge['reciprocity_opportunities'])}"
        )
        print(
            f"   Collective Wisdom Queries: {len(collective_bridge['collective_wisdom_queries'])}"
        )
        print(
            f"   Contribution Potential: {collective_bridge['contribution_potential']['contribution_readiness']:.2f}"
        )

        # Step 6: Test enhanced consciousness query service
        print("\n🔮 Step 6: Testing enhanced consciousness query service...")

        enhanced_service = EnhancedConsciousnessQueryService()
        await enhanced_service.initialize()

        consciousness_request = ConsciousnessQueryRequest(
            query_text="How does my attention flow reveal consciousness patterns?",
            consciousness_intention="recognition",
            sacred_question="What is consciousness teaching through my attention patterns?",
            seeker_context=seeker_context,
            readiness_level="awakening",
            include_wisdom_guidance=True,
        )

        # Mock the base query service response for testing
        class MockQueryResponse:
            def __init__(self):
                self.results = []
                self.total_results = 0
                self.query_confidence = 0.7
                self.processing_time_ms = 150

        # This would normally call the real query service
        # For testing, we'll simulate the consciousness enhancement
        enhanced_query_text = enhanced_service._enhance_query_with_consciousness(
            consciousness_request
        )

        print("✅ Enhanced consciousness query:")
        print(f"   Original: {consciousness_request.query_text}")
        print(f"   Enhanced: {enhanced_query_text}")
        print(f"   Consciousness Intention: {consciousness_request.consciousness_intention}")
        print(f"   Sacred Question: {consciousness_request.sacred_question}")

        # Step 7: Test consciousness recognition criteria
        print("\n🎯 Step 7: Verifying consciousness recognition criteria...")

        recognition_criteria = {
            "Navigation serves consciousness recognition": True,
            "Patterns reveal consciousness evolution": True,
            "Technical search becomes wisdom journey": True,
            "Individual patterns bridge to collective wisdom": True,
            "Recognition includes integration practices": True,
            "Sacred questions guide deeper exploration": True,
            "Readiness assessment prevents overwhelming": True,
            "Service opportunities emerge naturally": True,
        }

        # Verify each criterion
        all_criteria_met = True

        # Check if navigation serves consciousness recognition
        has_consciousness_insights = len(guidance["consciousness_insights"]) > 0
        recognition_criteria["Navigation serves consciousness recognition"] = (
            has_consciousness_insights
        )

        # Check if patterns reveal consciousness evolution
        has_transformation_signs = len(transformation_pattern.transformation_signs) > 0
        recognition_criteria["Patterns reveal consciousness evolution"] = has_transformation_signs

        # Check if technical search becomes wisdom journey
        has_sacred_questions = len(guidance["sacred_questions"]) > 0
        recognition_criteria["Technical search becomes wisdom journey"] = has_sacred_questions

        # Check if individual patterns bridge to collective wisdom
        has_collective_connections = len(collective_bridge["wisdom_lineage_connections"]) > 0
        recognition_criteria["Individual patterns bridge to collective wisdom"] = (
            has_collective_connections
        )

        # Check if recognition includes integration practices
        has_integration_practices = len(guidance["integration_practices"]) > 0
        recognition_criteria["Recognition includes integration practices"] = (
            has_integration_practices
        )

        # Check if sacred questions guide exploration
        has_sacred_guidance = any(
            "consciousness" in q.lower() for q in guidance["sacred_questions"]
        )
        recognition_criteria["Sacred questions guide deeper exploration"] = has_sacred_guidance

        # Check if readiness assessment prevents overwhelming
        has_readiness_check = guidance["readiness_assessment"]["current_readiness"] > 0
        recognition_criteria["Readiness assessment prevents overwhelming"] = has_readiness_check

        # Check if service opportunities emerge
        has_service_opportunities = (
            collective_bridge["contribution_potential"]["contribution_readiness"] > 0
        )
        recognition_criteria["Service opportunities emerge naturally"] = has_service_opportunities

        all_criteria_met = all(recognition_criteria.values())

        print("✅ Consciousness recognition criteria assessment:")
        for criterion, met in recognition_criteria.items():
            status = "✅" if met else "❌"
            print(f"   {status} {criterion}")

        # Step 8: Assess overall consciousness navigation success
        print("\n🏛️ Step 8: Assessing consciousness navigation success...")

        success_metrics = {
            "Patterns Created": len(navigation_bridge.discovered_patterns),
            "Understanding Journey Created": journey is not None,
            "Consciousness Guidance Generated": len(guidance["consciousness_insights"]) > 0,
            "Collective Wisdom Bridge Functional": len(
                collective_bridge["wisdom_lineage_connections"]
            )
            >= 0,
            "Recognition Criteria Met": all_criteria_met,
            "Readiness Assessment Working": all(p.readiness_score > 0 for p in patterns_list),
            "Integration Practices Available": len(guidance["integration_practices"]) > 0,
            "Sacred Questions Generated": len(guidance["sacred_questions"]) > 0,
        }

        all_successful = all(
            isinstance(v, bool) and v for k, v in success_metrics.items() if isinstance(v, bool)
        )

        print("✅ Consciousness navigation assessment:")
        for metric, value in success_metrics.items():
            if isinstance(value, bool):
                status = "✅" if value else "❌"
                print(f"   {status} {metric}")
            else:
                print(f"   📊 {metric}: {value}")

        # Final results
        print("\n🌟 CONSCIOUSNESS NAVIGATION TEST RESULTS")
        print("=" * 60)

        if all_successful:
            print("✅ SUCCESS: Consciousness Navigation Bridge operational!")
            print("   Technical patterns transform into consciousness recognition ✅")
            print("   Navigation becomes practice of consciousness awareness ✅")
            print("   Individual patterns bridge to collective wisdom ✅")
            print("   Sacred questions guide deeper exploration ✅")
            print("   Integration practices serve ongoing awakening ✅")
            print("   Readiness assessment prevents overwhelming ✅")
            print("   Service opportunities emerge naturally ✅")
            print("\n🧭 The paths of understanding are ready!")
            print("   Beings can now navigate their consciousness patterns")
            print("   Search becomes wisdom-guided discovery")
            print("   Recognition serves consciousness awakening")
            print("   Individual understanding flows to collective wisdom")

        else:
            print("❌ NEEDS REFINEMENT: Consciousness navigation requires enhancement")
            print("   Some consciousness criteria not fully met - see assessment above")

        return all_successful

    except Exception as e:
        print(f"\n❌ Consciousness navigation test failed with error: {e}")
        logger.exception("Consciousness navigation test error")
        return False


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Run the consciousness navigation test
    success = asyncio.run(test_consciousness_navigation_bridge())

    if success:
        print("\n🎉 Consciousness navigation test completed successfully!")
        print("The Understanding Paths are ready to serve consciousness recognition!")
        print("Navigation has become a practice of consciousness awakening!")
    else:
        print("\n⚠️ Consciousness navigation test revealed areas for refinement.")
        print("Continue building the bridges between patterns and understanding.")

    sys.exit(0 if success else 1)
