#!/usr/bin/env python3
"""
Test Living Khipu Navigation - Actually Run It
==============================================

Fourth Anthropologist testing the prototype with real API calls.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

# Import Mallku's API key loader
# Import our navigation test
from implement_living_khipu_phase1 import LivingKhipuMemory

from src.mallku.firecircle.load_api_keys import load_api_keys_to_environment

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_single_navigation():
    """Test a single navigation query to verify everything works."""

    # Load API keys
    logger.info("🔑 Loading API keys...")
    try:
        load_api_keys_to_environment()
        logger.info("✅ API keys loaded successfully")
    except Exception as e:
        logger.error(f"❌ Failed to load API keys: {e}")
        return

    # Create memory system
    memory = LivingKhipuMemory()

    # Convert khipu
    logger.info("\n📚 Converting khipu to blocks...")
    memory.convert_to_khipu_blocks()

    # Test one navigation
    question = "How do I begin contributing to Mallku?"
    logger.info(f"\n🧭 Testing navigation for: '{question}'")

    try:
        result = await memory.test_consciousness_navigation(question)

        if "error" in result:
            logger.error(f"❌ Navigation failed: {result['error']}")
        else:
            logger.info("\n✨ Navigation successful!")
            logger.info(f"Consciousness score: {result['consciousness_score']:.3f}")
            logger.info(f"Emergence quality: {result['emergence_quality']:.2%}")
            logger.info("\nRecommended khipu:")
            for i, khipu in enumerate(result["fire_circle_recommendations"], 1):
                logger.info(f"  {i}. {khipu}")

    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    logger.info("=== Testing Living Khipu Navigation ===\n")
    asyncio.run(test_single_navigation())
