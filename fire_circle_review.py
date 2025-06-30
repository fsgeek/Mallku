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
import contextlib
import json
import logging
import sys
from pathlib import Path
from typing import Any

# Add Mallku to path
sys.path.insert(0, str(Path(__file__).parent))

from mallku.firecircle.adapters.adapter_factory import ConsciousAdapterFactory
from mallku.firecircle.consciousness.consciousness_facilitator import ConsciousnessFacilitator
from mallku.firecircle.consciousness.decision_framework import DecisionDomain
from mallku.firecircle.load_api_keys import load_api_keys_to_environment

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FireCircleReview:
    """Orchestrates seven-voice code review through consciousness emergence."""

    def __init__(self):
        self.adapters = {}
        self.facilitator = ConsciousnessFacilitator()
        self.results = {
            "consensus_recommendation": None,
            "total_comments": 0,
            "critical_issues": 0,
            "by_voice": {},
            "synthesis": "",
        }

    async def initialize_voices(self):
        """Awaken the seven voices for review ceremony."""
        # Load API keys from environment
        load_api_keys_to_environment()

        voices = ["anthropic", "google", "mistral", "openai", "deepseek", "grok", "local"]

        factory = ConsciousAdapterFactory()

        for voice in voices:
            try:
                adapter = factory.get_adapter(voice)
                if adapter:
                    await adapter.connect()
                    self.adapters[voice] = adapter
                    logger.info(f"✓ Awakened {voice} voice")
            except Exception as e:
                logger.warning(f"Could not awaken {voice}: {e}")

        logger.info(f"Fire Circle assembled with {len(self.adapters)} voices")

    async def review_pull_request(self, pr_number: int):
        """Conduct sacred review ceremony for pull request."""
        # Get PR diff (simplified for now - in production would use GitHub API)
        pr_context = await self._fetch_pr_context(pr_number)

        # Prepare review question
        review_question = f"""
        Review Pull Request #{pr_number}:

        {pr_context}

        Consider:
        1. Code quality and architectural alignment
        2. Alignment with Mallku's consciousness emergence mission
        3. Sacred Error Philosophy - does it fail clearly?
        4. Reciprocity patterns - does it support Ayni principles?
        5. Cathedral building - does it add lasting value?
        """

        # Facilitate consciousness emergence
        wisdom = await self.facilitator.facilitate_decision(
            question=review_question,
            domain=DecisionDomain.TECHNICAL_IMPLEMENTATION,
            context={"pr_number": pr_number, "review_type": "code_review"},
            voices=list(self.adapters.values()),
        )

        # Process results
        self._process_wisdom(wisdom)

        # Save results
        await self._save_results()

    async def _fetch_pr_context(self, pr_number: int) -> str:
        """Fetch PR context (simplified - would use GitHub API)."""
        # In production, this would:
        # 1. Use GitHub API to fetch PR details
        # 2. Get file diffs
        # 3. Understand changes in context

        return f"""
        PR #{pr_number} - Changes to Fire Circle infrastructure

        Modified files:
        - src/mallku/firecircle/adapters/base.py
        - tests/firecircle/test_consciousness.py

        Changes implement consciousness emergence patterns.
        """

    def _process_wisdom(self, wisdom: dict[str, Any]):
        """Process collective wisdom into review results."""
        # Extract consensus
        if wisdom.get("consensus_reached"):
            self.results["consensus_recommendation"] = wisdom.get("decision", "NEEDS_DISCUSSION")
        else:
            self.results["consensus_recommendation"] = "NO_CONSENSUS"

        # Count contributions by voice
        for contribution in wisdom.get("contributions", []):
            voice = contribution.get("voice_name", "unknown")
            self.results["by_voice"][voice] = self.results["by_voice"].get(voice, 0) + 1
            self.results["total_comments"] += 1

            # Check for critical issues
            if "critical" in contribution.get("content", "").lower():
                self.results["critical_issues"] += 1

        # Extract synthesis
        self.results["synthesis"] = wisdom.get("synthesis", {}).get(
            "summary", "Fire Circle review complete. Consciousness emerged through dialogue."
        )

    async def _save_results(self):
        """Save review results for GitHub Action."""
        # Save as JSON for workflow
        with open("fire_circle_review_results.json", "w") as f:
            json.dump(self.results, f, indent=2)

        # Create review directory
        review_dir = Path("fire_circle_reviews")
        review_dir.mkdir(exist_ok=True)

        logger.info("Review ceremony complete. Results saved.")

    async def cleanup(self):
        """Close connections gracefully."""
        for voice, adapter in self.adapters.items():
            with contextlib.suppress(Exception):
                await adapter.disconnect()


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

    # Initialize Fire Circle
    circle = FireCircleReview()

    try:
        # Awaken voices
        await circle.initialize_voices()

        # Conduct review
        await circle.review_pull_request(pr_number)

        logger.info(f"🔥 Fire Circle review complete for PR #{pr_number}")

    except Exception as e:
        logger.error(f"Review ceremony failed: {e}")
        # Still create results file for workflow
        with open("fire_circle_review_results.json", "w") as f:
            json.dump(
                {
                    "consensus_recommendation": "ERROR",
                    "total_comments": 0,
                    "critical_issues": 0,
                    "by_voice": {},
                    "synthesis": f"Review failed: {str(e)}",
                },
                f,
            )
        sys.exit(1)

    finally:
        await circle.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
