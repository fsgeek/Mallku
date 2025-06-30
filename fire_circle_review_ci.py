#!/usr/bin/env python3
"""
Fire Circle Review - CI/CD Entry Point
=====================================

This is the specific entry point for running Fire Circle Review in CI/CD environments
without database persistence. It automatically sets the required environment variables
and provides clear indication that this is a specialized mode.

Usage:
    python fire_circle_review_ci.py <PR_NUMBER>
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Set CI-specific environment before any imports
os.environ["MALLKU_SKIP_DATABASE"] = "true"
os.environ["MALLKU_CI_MODE"] = "true"

# Clear indication this is CI mode
print("=" * 60)
print("🔥 FIRE CIRCLE REVIEW - CI/CD MODE")
print("=" * 60)
print("Running without database persistence.")
print("This mode is specifically for GitHub Actions and CI/CD.")
print("For development, use: python fire_circle_review.py")
print("=" * 60)
print()

# Add Mallku to path
sys.path.insert(0, str(Path(__file__).parent))

# Import after setting environment variables
from mallku.firecircle.runner import run_fire_circle_review  # noqa: E402

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """CI-specific entry point for Fire Circle review."""
    if len(sys.argv) < 2:
        print("Usage: python fire_circle_review_ci.py <PR_NUMBER>")
        sys.exit(1)

    try:
        pr_number = int(sys.argv[1])
    except ValueError:
        print("PR_NUMBER must be an integer")
        sys.exit(1)

    logger.info("Fire Circle Review running in CI/CD mode - no persistence")

    try:
        # Run the shared implementation
        await run_fire_circle_review(pr_number)
    except Exception as e:
        logger.error(f"Review failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
