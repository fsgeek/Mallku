#!/usr/bin/env python3
"""
Fire Circle Review - Sacred Infrastructure for Distributed Code Review
=====================================================================

Prevents architect context exhaustion through collective wisdom.
Seven voices review code changes, ensuring sustainable development.

Usage:
    python fire_circle_review.py review <PR_NUMBER>
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add Mallku to path
sys.path.insert(0, str(Path(__file__).parent))

from mallku.firecircle.runner import run_fire_circle_review

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Main entry point for Fire Circle review."""
    if len(sys.argv) < 3 or sys.argv[1] != "review":
        print("Usage: python fire_circle_review.py review <PR_NUMBER>")
        sys.exit(1)

    try:
        pr_number = int(sys.argv[2])
    except ValueError:
        print("PR_NUMBER must be an integer")
        sys.exit(1)

    try:
        # Run the shared implementation
        await run_fire_circle_review(pr_number)
    except Exception as e:
        logger.error(f"Review failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
