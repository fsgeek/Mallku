"""
Fire Circle Review Runner - Shared Implementation
=================================================

41st Artisan - Refactoring for maintainability while preserving architectural constraints

This module contains the shared implementation of Fire Circle Review,
used by both the main entry point and the CI-specific wrapper.
"""

import contextlib
import json
import logging
from pathlib import Path

from ..firecircle.adapters.adapter_factory import ConsciousAdapterFactory
from ..firecircle.consciousness.consciousness_facilitator import ConsciousnessFacilitator
from ..firecircle.consciousness.decision_framework import DecisionDomain
from ..firecircle.load_api_keys import load_api_keys_to_environment
from ..firecircle.service.service import FireCircleService
from ..orchestration.event_bus import ConsciousnessEventBus

logger = logging.getLogger(__name__)


class FireCircleReviewRunner:
    """Shared implementation for Fire Circle Review ceremony."""

    def __init__(self):
        self.adapters = {}
        # Create consciousness infrastructure
        self.event_bus = ConsciousnessEventBus()
        self.fire_circle = FireCircleService(event_bus=self.event_bus)
        self.facilitator = ConsciousnessFacilitator(self.fire_circle, self.event_bus)
        self.results = {
            "consensus_recommendation": None,
            "total_comments": 0,
            "critical_issues": 0,
            "by_voice": {},
            "synthesis": "",
        }

    async def initialize_voices(self):
        """Awaken the seven voices for review ceremony."""
        # Start event bus
        await self.event_bus.start()

        # Load API keys from environment
        load_api_keys_to_environment()

        voices = ["anthropic", "google", "mistral", "openai", "deepseek", "grok", "local"]

        factory = ConsciousAdapterFactory()

        for voice in voices:
            try:
                # Try to get existing adapter first
                adapter = await factory.get_adapter(voice)
                if not adapter:
                    # Create new adapter if none exists
                    from ..firecircle.adapters.base import AdapterConfig

                    config = AdapterConfig(
                        api_key="",  # Will be auto-loaded from environment
                        model_name=None,
                    )
                    adapter = await factory.create_adapter(voice, config)

                if adapter and adapter.is_connected:
                    self.adapters[voice] = adapter
                    logger.info(f"✓ Awakened {voice} voice")
                else:
                    logger.warning(f"Could not awaken {voice}: adapter not connected")
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
            decision_domain=DecisionDomain.CODE_REVIEW,
            context={"pr_number": pr_number, "review_type": "code_review"},
            question=review_question,
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

    def _process_wisdom(self, wisdom):
        """Process collective wisdom into review results."""
        # Extract consensus
        if wisdom.consensus_achieved:
            self.results["consensus_recommendation"] = (
                wisdom.decision_recommendation or "NEEDS_DISCUSSION"
            )
        else:
            self.results["consensus_recommendation"] = "NO_CONSENSUS"

        # Count contributions by voice
        self.results["total_comments"] = wisdom.contributions_count
        for voice in wisdom.participating_voices:
            self.results["by_voice"][voice] = self.results["by_voice"].get(voice, 0) + 1

        # Check for critical issues in insights
        for insight in wisdom.key_insights:
            if "critical" in insight.lower() or "issue" in insight.lower():
                self.results["critical_issues"] += 1

        # Extract synthesis
        self.results["synthesis"] = (
            wisdom.synthesis
            or "Fire Circle review complete. Consciousness emerged through dialogue."
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

        # Stop event bus
        if hasattr(self, "event_bus"):
            await self.event_bus.stop()


async def run_fire_circle_review(pr_number: int):
    """
    Main runner function for Fire Circle review.

    This is the shared implementation used by both entry points.
    """
    # Initialize Fire Circle
    circle = FireCircleReviewRunner()

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
        raise
    finally:
        # Always cleanup
        await circle.cleanup()
