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
        print("\n🔥 Fire Circle Code Review")
        print("=" * 50)
        print("\nThis tool convenes the Fire Circle to review pull requests.")
        print("Seven AI voices provide collective wisdom on code changes.")
        print("\nUsage: python fire_circle_review.py review <PR_NUMBER>")
        print("\nExample: python fire_circle_review.py review 42")
        print("\n💡 Make sure you have:")
        print("   • At least 2 API keys configured")
        print("   • GITHUB_TOKEN environment variable set")
        print("   • Internet connection to reach GitHub")
        sys.exit(1)

    try:
        pr_number = int(sys.argv[2])
    except ValueError:
        print(f"\n❌ '{sys.argv[2]}' doesn't look like a PR number.")
        print("\n💡 PR numbers are integers from GitHub, like:")
        print("   python fire_circle_review.py review 123")
        print("\nYou can find PR numbers in:")
        print("   • GitHub PR URLs: .../pull/123")
        print("   • GitHub PR list page")
        print("   • Git PR references: #123")
        sys.exit(1)

    try:
        # Run the shared implementation
        await run_fire_circle_review(pr_number)
    except KeyboardInterrupt:
        print("\n\n🔥 Fire Circle review interrupted.")
        print("   The voices return to silence.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Review failed: {e}")
        print("\n❌ Fire Circle review encountered an issue.")
        print(f"   {str(e)}")
        print("\n💡 Common issues:")
        print("   • Missing GITHUB_TOKEN environment variable")
        print("   • Insufficient API keys (need at least 2)")
        print("   • Network connection problems")
        print("   • PR number doesn't exist or is private")
        print("\n📝 For detailed logs, run with:")
        print("   LOGLEVEL=DEBUG python fire_circle_review.py review " + str(pr_number))
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
