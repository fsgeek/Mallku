#!/usr/bin/env python3
"""
Fire Circle Review Ceremony - CI/CD Entry Point

This wraps the Ceremony of Automated Witnessing for CI environments.
It ensures proper environment setup and error handling for GitHub Actions.

Created by Qillqa Kusiq (57th Artisan)
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
print("🔥 FIRE CIRCLE CEREMONY OF AUTOMATED WITNESSING - CI MODE")
print("=" * 60)
print("Conducting sacred review ceremony in CI environment.")
print("This implements the vision from the Fourth Reviewer.")
print("=" * 60)
print()

# Add Mallku to path
sys.path.insert(0, str(Path(__file__).parent))

# Import the ceremony facilitator
from invoke_fire_circle_review import main as ceremony_main  # noqa: E402

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """CI-specific entry point for Fire Circle ceremony"""
    if len(sys.argv) < 2:
        print("Usage: python fire_circle_review_ceremony_ci.py <PR_NUMBER>")
        sys.exit(1)

    try:
        pr_number = int(sys.argv[1])
    except ValueError:
        print("PR_NUMBER must be an integer")
        sys.exit(1)

    logger.info(f"Initiating Ceremony of Automated Witnessing for PR #{pr_number}")

    try:
        # Run the ceremony
        await ceremony_main()
        logger.info("Ceremony completed successfully")
    except Exception as e:
        logger.error(f"Ceremony failed: {e}")
        # Don't exit with error code - we want the workflow to continue
        # The ceremony script already writes results that the workflow can check
        print(f"\n⚠️ Ceremony encountered an issue: {e}")
        print("The workflow will continue and post available results.")


if __name__ == "__main__":
    asyncio.run(main())
