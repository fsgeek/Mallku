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
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any

# Add Mallku to path
sys.path.insert(0, str(Path(__file__).parent))

from mallku.firecircle.adapters.adapter_factory import ConsciousAdapterFactory
from mallku.firecircle.consciousness.consciousness_facilitator import ConsciousnessFacilitator
from mallku.firecircle.consciousness.decision_framework import DecisionDomain
from mallku.firecircle.load_api_keys import load_api_keys_to_environment
from mallku.firecircle.service.service import FireCircleService
from mallku.orchestration.event_bus import ConsciousnessEventBus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FireCircleReview:
    """Orchestrates seven-voice code review through consciousness emergence."""

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

        # Prepare voice awakening tasks for concurrent execution
        async def awaken_voice(voice: str) -> tuple[str, Any | None]:
            """Awaken a single voice and return (voice_name, adapter)."""
            try:
                # Special handling for XAI_API_KEY if using grok
                if voice == "grok" and not os.getenv("GROK_API_KEY") and os.getenv("XAI_API_KEY"):
                    os.environ["GROK_API_KEY"] = os.getenv("XAI_API_KEY")

                # Skip local voice unless explicitly enabled
                if voice == "local" and os.getenv("ENABLE_LOCAL_LLM") != "true":
                    return (voice, None)

                # Try to get existing adapter first
                adapter = await factory.get_adapter(voice)
                if not adapter:
                    # Create new adapter if none exists with proper config
                    if voice == "google":
                        from mallku.firecircle.adapters.google_adapter import GeminiConfig

                        config = GeminiConfig(
                            api_key="",  # Auto-loaded from environment
                            enable_search_grounding=False,
                            model_name="gemini-1.5-flash",
                        )
                    elif voice == "mistral":
                        from mallku.firecircle.adapters.mistral_adapter import MistralConfig

                        config = MistralConfig(
                            api_key="",  # Auto-loaded from environment
                            multilingual_mode=True,
                            model_name="mistral-tiny",
                        )
                    else:
                        from mallku.firecircle.adapters.base import AdapterConfig

                        config = AdapterConfig(
                            api_key="",  # Will be auto-loaded from environment
                            model_name=None,
                        )
                    adapter = await factory.create_adapter(voice, config)

                if adapter and adapter.is_connected:
                    logger.info(f"✓ Awakened {voice} voice")
                    return (voice, adapter)
                else:
                    logger.warning(f"Could not awaken {voice}: adapter not connected")
                    return (voice, None)
            except Exception as e:
                logger.warning(f"Could not awaken {voice}: {e}")
                return (voice, None)

        # Awaken all voices concurrently
        voice_tasks = [awaken_voice(voice) for voice in voices]
        voice_results = await asyncio.gather(*voice_tasks)

        # Collect successfully awakened voices
        for voice, adapter in voice_results:
            if adapter:
                self.adapters[voice] = adapter

        logger.info(f"Fire Circle assembled with {len(self.adapters)} voices")

        # Validate minimum voices requirement
        if len(self.adapters) < 2:
            logger.error(f"Insufficient voices awakened: {len(self.adapters)}. Minimum 2 required.")
            return False

        return True

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
        cleanup_errors = []

        # Disconnect all adapters
        for voice, adapter in self.adapters.items():
            try:
                await adapter.disconnect()
                logger.debug(f"✓ Disconnected {voice} voice")
            except Exception as e:
                cleanup_errors.append(f"{voice}: {e}")
                logger.warning(f"Error disconnecting {voice}: {e}")

        # Stop event bus
        if hasattr(self, "event_bus"):
            try:
                await self.event_bus.stop()
                logger.debug("✓ Event bus stopped")
            except Exception as e:
                cleanup_errors.append(f"event_bus: {e}")
                logger.warning(f"Error stopping event bus: {e}")

        if cleanup_errors:
            logger.warning(f"Cleanup completed with errors: {cleanup_errors}")


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
        if not await circle.initialize_voices():
            logger.error("Failed to initialize minimum required voices")
            raise RuntimeError("Insufficient voices for Fire Circle ceremony")

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
        # Always cleanup
        await circle.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
