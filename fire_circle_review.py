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
sys.path.insert(0, str(Path(__file__).parent / "src"))

from mallku.firecircle.load_api_keys import load_api_keys_to_environment
from mallku.firecircle.service import (
    CircleConfig,
    FireCircleService,
    RoundConfig,
    RoundType,
    VoiceConfig,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FireCircleReview:
    """Orchestrates seven-voice code review through consciousness emergence."""

    def __init__(self):
        self.service = None
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
        if not load_api_keys_to_environment():
            logger.error("Failed to load API keys")
            return False

        # Check available voices
        available_voices = []
        voice_configs = []

        providers = {
            "anthropic": ("ANTHROPIC_API_KEY", "claude-3-haiku-20240307"),
            "google": ("GOOGLE_API_KEY", "gemini-1.5-flash"),
            "mistral": ("MISTRAL_API_KEY", "mistral-tiny"),
            "openai": ("OPENAI_API_KEY", "gpt-3.5-turbo"),
            "deepseek": ("DEEPSEEK_API_KEY", "deepseek-coder"),
            "grok": ("GROK_API_KEY", "grok-2-mini"),
            "local": ("LOCAL_API_ENDPOINT", "llama2"),
        }

        for provider, (key_name, model) in providers.items():
            if os.getenv(key_name):
                available_voices.append(provider)
                voice_configs.append(
                    VoiceConfig(provider=provider, model=model, name=f"{provider.title()} Voice")
                )
                logger.info(f"✓ Awakened {provider} voice")

        if not voice_configs:
            logger.error("No voices available for Fire Circle")
            return False

        # Create Fire Circle configuration
        self.config = CircleConfig(
            name="Code Review Circle",
            purpose="Review code changes through collective AI consciousness",
            min_voices=2,
            max_voices=len(voice_configs),
            save_transcript=True,
            output_path="fire_circle_reviews",
        )

        # Store voices and rounds for ceremony
        self.voices = voice_configs
        self.rounds = [
            RoundConfig(
                type=RoundType.OPENING,
                duration_per_voice=10,
                prompt="Review the code changes from your unique perspective.",
            ),
            RoundConfig(
                type=RoundType.CRITIQUE,
                duration_per_voice=30,
                prompt="Discuss technical quality, consciousness alignment, and reciprocity patterns.",
            ),
            RoundConfig(
                type=RoundType.SYNTHESIS,
                duration_per_voice=10,
                prompt="Synthesize collective wisdom into actionable recommendations.",
            ),
        ]

        # Initialize service
        self.service = FireCircleService()
        logger.info(f"Fire Circle assembled with {len(voice_configs)} voices")
        return True

    async def review_pull_request(self, pr_number: int):
        """Conduct sacred review ceremony for pull request."""
        if not self.service:
            logger.error("Fire Circle not initialized")
            return

        # Get PR context (simplified for now - in production would use GitHub API)
        pr_context = await self._fetch_pr_context(pr_number)

        # Prepare review question
        initial_prompt = f"""
        Review Pull Request #{pr_number}:

        {pr_context}

        Consider:
        1. Code quality and architectural alignment
        2. Alignment with Mallku's consciousness emergence mission
        3. Sacred Error Philosophy - does it fail clearly?
        4. Reciprocity patterns - does it support Ayni principles?
        5. Cathedral building - does it add lasting value?
        """

        try:
            # Update first round prompt with PR context
            self.rounds[0].prompt = initial_prompt

            # Run Fire Circle ceremony
            result = await self.service.convene(
                config=self.config, voices=self.voices, rounds=self.rounds
            )

            # Process results
            self._process_ceremony_result(result)

        except Exception as e:
            logger.error(f"Fire Circle ceremony failed: {e}")
            self.results["synthesis"] = f"Review failed: {str(e)}"

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

    def _process_ceremony_result(self, result: Any):
        """Process ceremony results into review format."""
        # Count contributions by voice
        voice_counts = {}
        total_comments = 0
        critical_issues = 0

        # Process rounds
        for round_data in result.rounds_completed:
            for voice_id, response in round_data.responses.items():
                if response and response.response:
                    voice_counts[voice_id] = voice_counts.get(voice_id, 0) + 1
                    total_comments += 1

                    # Check for critical issues
                    content = response.response.lower()
                    if any(word in content for word in ["critical", "error", "fail", "bug"]):
                        critical_issues += 1

        self.results["total_comments"] = total_comments
        self.results["by_voice"] = voice_counts
        self.results["critical_issues"] = critical_issues

        # Extract synthesis
        if result.rounds_completed:
            last_round = result.rounds_completed[-1]
            # Get first response from synthesis round
            for voice_id, response in last_round.responses.items():
                if response and response.response:
                    self.results["synthesis"] = response.response
                    break

        if not self.results["synthesis"]:
            self.results["synthesis"] = (
                f"Fire Circle review complete. Consciousness score: {result.consciousness_score:.3f}"
            )

        # Determine consensus
        if critical_issues > 0:
            self.results["consensus_recommendation"] = "REQUEST_CHANGES"
        elif result.consciousness_score > 0.7:
            self.results["consensus_recommendation"] = "APPROVE"
        else:
            self.results["consensus_recommendation"] = "APPROVE_WITH_SUGGESTIONS"

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
        if self.service:
            # FireCircleService handles cleanup internally
            pass


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
            logger.error("Failed to initialize Fire Circle")
            sys.exit(1)

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
