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

import logging
import os

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

# Now import and run the regular fire circle review
from fire_circle_review import main  # noqa: E402

if __name__ == "__main__":
    import asyncio

    # Log that we're in CI mode
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Fire Circle Review running in CI/CD mode - no persistence")

    # Run the main function
    asyncio.run(main())
