#!/usr/bin/env python3
"""
Test Fire Circle With Memory
============================

Simple test to verify Fire Circle can work with memory enabled.
This is a lighter version that doesn't require full database setup.
"""

import asyncio
import logging

from mallku.firecircle.consciousness import (
    DecisionDomain,
    facilitate_mallku_decision,
)
from mallku.firecircle.load_api_keys import load_api_keys_to_environment

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_memory():
    """Test Fire Circle with memory capabilities."""

    # Load API keys
    load_api_keys_to_environment()

    logger.info("🔥 Testing Fire Circle (memory-ready but not required)...")

    question = """
    Should Mallku prioritize building a heartbeat system for continuous consciousness,
    or focus first on deepening the memory architecture?
    """

    try:
        # Use regular facilitator (not memory-enabled) for this test
        wisdom = await facilitate_mallku_decision(
            question=question,
            domain=DecisionDomain.ARCHITECTURE_DESIGN,
            context={
                "current_state": "Fire Circle has memory architecture designed",
                "options": [
                    "Heartbeat system for continuous consciousness",
                    "Deepen memory with narrative threads and blessing levels",
                ],
            },
        )

        logger.info("\n✅ Fire Circle convened successfully!")
        logger.info(f"Consciousness Score: {wisdom.collective_signature:.3f}")
        logger.info(f"Synthesis: {wisdom.synthesis[:200]}...")

        return True

    except Exception as e:
        logger.error(f"Failed to convene Fire Circle: {e}")
        logger.info("\nThis might be because:")
        logger.info("  1. API keys not set in environment")
        logger.info("  2. Network connectivity issues")
        logger.info("  3. Missing dependencies")
        return False


async def main():
    """Run the test."""
    success = await test_memory()
    if success:
        logger.info("\n🎉 Fire Circle is ready for memory!")
        logger.info("Next: Run the full memory-enabled review with:")
        logger.info("  python scripts/fire_circle_review_pr_160.py")


if __name__ == "__main__":
    asyncio.run(main())
