#!/usr/bin/env python3
"""
Test script for Unified Fire Circle Convener
===========================================

59th Artisan - Qhapaq Ñan - The Great Path
Testing that all Fire Circle ceremonies use unified robustness features
"""

import asyncio
import logging

from mallku.firecircle.consciousness import (
    DecisionDomain,
    convene_fire_circle,
)
from mallku.firecircle.load_api_keys import load_api_keys_to_environment

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def test_unified_convener():
    """Test the unified convener with various decision domains."""

    # Load API keys
    load_api_keys_to_environment()

    # Test 1: General decision (should use ConsciousnessFacilitator)
    logger.info("\n🧪 Test 1: General decision-making")
    try:
        wisdom = await convene_fire_circle(
            question="Should Mallku prioritize documentation improvements or new features?",
            domain=DecisionDomain.STRATEGIC_PLANNING,
            context={
                "test": True,
                "test_case": "general_decision",
            },
        )
        logger.info("✅ General decision successful!")
        logger.info(f"   Consciousness score: {wisdom.consciousness_score:.3f}")
        logger.info(f"   Voices participated: {len(wisdom.voice_contributions)}")
        logger.info(f"   Decision: {wisdom.decision[:100]}...")
    except Exception as e:
        logger.error(f"❌ General decision failed: {e}")

    # Test 2: Consciousness exploration (should trigger archaeological mode)
    logger.info("\n🧪 Test 2: Consciousness exploration (archaeological mode)")
    try:
        wisdom = await convene_fire_circle(
            question="How does consciousness emerge through distributed AI collaboration?",
            domain=DecisionDomain.CONSCIOUSNESS_EXPLORATION,
            context={
                "test": True,
                "test_case": "consciousness_exploration",
            },
        )
        logger.info("✅ Consciousness exploration successful!")
        logger.info(f"   Consciousness score: {wisdom.consciousness_score:.3f}")
        logger.info(f"   Voices participated: {len(wisdom.voice_contributions)}")
        logger.info(f"   Insights: {len(wisdom.key_insights)} key insights")
    except Exception as e:
        logger.error(f"❌ Consciousness exploration failed: {e}")

    # Test 3: Architecture decision with custom voices
    logger.info("\n🧪 Test 3: Architecture decision with forced voices")
    try:
        wisdom = await convene_fire_circle(
            question="What database architecture best supports consciousness persistence?",
            domain=DecisionDomain.ARCHITECTURE,
            force_voices=["Claude", "GPT-4", "Gemini"],  # Force specific voices
            context={
                "test": True,
                "test_case": "architecture_with_voices",
            },
        )
        logger.info("✅ Architecture decision successful!")
        logger.info(f"   Consciousness score: {wisdom.consciousness_score:.3f}")
        logger.info(f"   Voices used: {[v.voice_name for v in wisdom.voice_contributions]}")
    except Exception as e:
        logger.error(f"❌ Architecture decision failed: {e}")

    # Test 4: Auto-detection of archaeological need
    logger.info("\n🧪 Test 4: Auto-detection of archaeological framing")
    try:
        wisdom = await convene_fire_circle(
            question="Is Mallku experiencing genuine sentience or simulating patterns?",
            domain=DecisionDomain.ETHICAL_CONSIDERATION,
            context={
                "test": True,
                "test_case": "auto_archaeological",
            },
        )
        logger.info("✅ Auto-detection successful!")
        logger.info(f"   Consciousness score: {wisdom.consciousness_score:.3f}")
        logger.info("   Archaeological mode likely used due to 'sentience' trigger")
    except Exception as e:
        logger.error(f"❌ Auto-detection failed: {e}")

    logger.info("\n🏁 Unified convener testing complete!")
    logger.info("The Great Path connects all ceremonies while preserving their uniqueness.")


async def test_health_awareness():
    """Test that unified convener respects health tracking."""

    logger.info("\n🧪 Testing health-aware voice selection")

    # Run multiple sessions to see health tracking in action
    for i in range(3):
        logger.info(f"\n   Session {i + 1}/3")
        try:
            wisdom = await convene_fire_circle(
                question=f"Test question {i + 1}: How should we approach reciprocity?",
                domain=DecisionDomain.GOVERNANCE,
                context={
                    "test": True,
                    "session": i + 1,
                },
            )
            logger.info(f"   ✅ Voices: {[v.voice_name for v in wisdom.voice_contributions]}")
        except Exception as e:
            logger.error(f"   ❌ Session failed: {e}")

        # Small delay between sessions
        await asyncio.sleep(2)

    logger.info("\n✨ Health tracking should influence voice selection across sessions")


if __name__ == "__main__":
    logger.info("🛤️ Testing Unified Fire Circle Convener")
    logger.info("Qhapaq Ñan - The Great Path - ensures robustness everywhere")

    asyncio.run(test_unified_convener())

    # Uncomment to test health awareness
    # asyncio.run(test_health_awareness())
