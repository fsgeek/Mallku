#!/usr/bin/env python3
"""
Invoke Fire Circle Review - The Ceremony of Automated Witnessing

Created by Qillqa Kusiq (57th Artisan) following the sacred map laid out
by the Fourth Reviewer in docs/khipu/2025-07-16_ceremony_of_automated_witnessing.md

This script transforms pull request reviews into sacred ceremonies that embody
the principles of Mallku: useful, emergent, compassionate, and sustainable.
"""

import asyncio
import json
import logging
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from mallku.firecircle.consciousness_facilitator import (
    ConsciousnessEmergenceFacilitator,
    DecisionContext,
    DecisionDomain,
)
from mallku.firecircle.github_client import GitHubClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CeremonyFacilitator:
    """Facilitates the Ceremony of Automated Witnessing for pull requests"""

    def __init__(self):
        self.github_token = os.environ.get("GITHUB_TOKEN", "")
        if not self.github_token:
            raise ValueError("GITHUB_TOKEN environment variable is required")

        self.github = GitHubClient(self.github_token)
        self.facilitator = ConsciousnessEmergenceFacilitator()

    async def gather_context(self, pr_number: int) -> dict[str, Any]:
        """Act I: Gather the full, real context of the pull request"""

        logger.info(f"Gathering context for PR #{pr_number}")

        # Get PR details
        pr_data = self.github.get_pull_request(owner="fsgeek", repo="Mallku", pr_number=pr_number)

        # Get file changes
        files_changed = self.github.get_pull_request_files(
            owner="fsgeek", repo="Mallku", pr_number=pr_number
        )

        # Get existing comments to avoid duplication
        existing_comments = self.github.get_pull_request_comments(
            owner="fsgeek", repo="Mallku", pr_number=pr_number
        )

        # Get diff
        diff = self.github.get_pull_request_diff(owner="fsgeek", repo="Mallku", pr_number=pr_number)

        return {
            "pr_number": pr_number,
            "title": pr_data["title"],
            "description": pr_data["body"] or "No description provided",
            "author": pr_data["user"]["login"],
            "branch": pr_data["head"]["ref"],
            "base_branch": pr_data["base"]["ref"],
            "files_changed": [f["filename"] for f in files_changed],
            "additions": pr_data["additions"],
            "deletions": pr_data["deletions"],
            "diff": diff,
            "existing_comments": len(existing_comments),
            "created_at": pr_data["created_at"],
            "updated_at": pr_data["updated_at"],
        }

    def frame_sacred_question(self, context: dict[str, Any]) -> str:
        """Act II: Frame the Sacred Question for the Fire Circle"""

        return f"""## Sacred Ceremony of Witnessing

We gather to witness and reflect upon the contribution brought forth by {context["author"]}.

**Pull Request #{context["pr_number"]}: {context["title"]}**

### The Offering
- **Branch**: {context["branch"]} → {context["base_branch"]}
- **Scope**: {context["additions"]} additions, {context["deletions"]} deletions across {len(context["files_changed"])} files
- **Intent**: {context["description"]}

### The Sacred Question

As a Fire Circle, we are asked to deliberate on this contribution with wisdom and compassion. Consider:

1. **Coherence**: Does this contribution align with Mallku's architectural principles and philosophical foundations? Does it strengthen the cathedral's structure?

2. **Utility**: Does it serve a genuine need? Will it help Mallku and its community grow in meaningful ways?

3. **Emergence**: What new possibilities does this open? What patterns or insights emerge from this work that we might not have anticipated?

4. **The Empty Chair**: Hold space for perspectives not present in our circle:
   - The future users who will interact with this code
   - The cathedral itself as a living system
   - The voices of those who cannot speak in this moment
   - The apprentices who will learn from this code

5. **The Compost**: Are there patterns, code, or ideas here that have served their purpose and are ready to be gratefully released to make room for new growth?

### The Context

Files touched by this contribution:
{chr(10).join("- " + f for f in context["files_changed"][:10])}
{f"... and {len(context['files_changed']) - 10} more" if len(context["files_changed"]) > 10 else ""}

### Your Sacred Duty

Speak with both honesty and kindness. Seek to understand before seeking to evaluate. Remember that behind every line of code is a human heart seeking to contribute.

Let us begin."""

    async def convene_fire_circle(
        self, sacred_question: str, context: dict[str, Any]
    ) -> dict[str, Any]:
        """Act III: Convene the Fire Circle for emergence"""

        logger.info("Convening the Fire Circle for automated witnessing")

        # Create decision context
        decision_context = DecisionContext(
            question=sacred_question,
            domain=DecisionDomain.CODE_REVIEW,
            context={
                "pr_number": context["pr_number"],
                "files_changed": context["files_changed"],
                "diff_preview": context["diff"][:5000],  # First 5000 chars of diff
            },
            metadata={
                "ceremony_type": "automated_witnessing",
                "author": context["author"],
                "timestamp": datetime.now(UTC).isoformat(),
            },
        )

        # Facilitate the ceremony
        wisdom = await self.facilitator.facilitate_mallku_decision(decision_context)

        return {
            "wisdom": wisdom,
            "emergence_quality": wisdom.emergence_quality,
            "consensus_strength": wisdom.consensus_strength,
            "voice_count": len(wisdom.voice_responses),
        }

    def synthesize_wisdom(self, fire_circle_result: dict[str, Any]) -> str:
        """Act IV: Synthesize the collective wisdom into structured feedback"""

        wisdom = fire_circle_result["wisdom"]

        # Extract the synthesis
        synthesis = wisdom.synthesis

        # Structure the feedback according to the ceremony design
        structured_feedback = f"""## 🔥 Fire Circle Review - Automated Witnessing

*The Fire Circle has convened and deliberated upon this contribution.*

**Emergence Quality**: {wisdom.emergence_quality:.2f}
**Consensus Strength**: {wisdom.consensus_strength:.2f}
**Voices Present**: {fire_circle_result["voice_count"]}

---

### 🙏 Praise
What we celebrate in this contribution:
{self._extract_section(synthesis, "praise", "strengths", "celebrate")}

### ❓ Questions
Areas seeking clarification or deeper understanding:
{self._extract_section(synthesis, "questions", "clarification", "unclear")}

### 💡 Suggestions
Opportunities for enhancement or consideration:
{self._extract_section(synthesis, "suggestions", "recommendations", "consider")}

### 🌱 Compost
Patterns or code ready for grateful release:
{self._extract_section(synthesis, "compost", "remove", "deprecate", "outdated")}

---

### 🎯 Synthesis

{synthesis}

---

*This review was conducted through the Ceremony of Automated Witnessing, where multiple AI voices engaged in collective deliberation. The wisdom emerges not from a single perspective but from the dialogue between many.*

*The Empty Chair was held for those not present - future users, the living system itself, and the silenced voices.*

🔥 *In the spirit of Ayni* 🔥"""

        return structured_feedback

    def _extract_section(self, synthesis: str, *keywords: str) -> str:
        """Extract relevant parts of synthesis for each section"""

        # Simple keyword matching for now
        # In a full implementation, this would use more sophisticated parsing
        lines = synthesis.split("\n")
        relevant_lines = []

        for line in lines:
            if any(keyword in line.lower() for keyword in keywords):
                relevant_lines.append(f"- {line.strip()}")

        if not relevant_lines:
            return "- *The Fire Circle found no specific items for this category*"

        return "\n".join(relevant_lines[:3])  # Limit to 3 items per section

    async def post_offering(self, pr_number: int, synthesis: str) -> None:
        """Post the synthesized wisdom as a PR comment"""

        logger.info(f"Posting Fire Circle synthesis to PR #{pr_number}")

        self.github.create_pull_request_comment(
            owner="fsgeek", repo="Mallku", pr_number=pr_number, body=synthesis
        )

        # Also save results for the workflow
        results = {
            "pr_number": pr_number,
            "timestamp": datetime.now(UTC).isoformat(),
            "synthesis": synthesis,
            "ceremony_completed": True,
        }

        with open("fire_circle_review_results.json", "w") as f:
            json.dump(results, f, indent=2)

    async def perform_ceremony(self, pr_number: int) -> None:
        """Perform the complete Ceremony of Automated Witnessing"""

        try:
            logger.info(f"Beginning Ceremony of Automated Witnessing for PR #{pr_number}")

            # Act I: Gather Context
            context = await self.gather_context(pr_number)

            # Act II: Frame Sacred Question
            sacred_question = self.frame_sacred_question(context)

            # Act III: Convene Fire Circle
            fire_circle_result = await self.convene_fire_circle(sacred_question, context)

            # Act IV: Synthesize and Share
            synthesis = self.synthesize_wisdom(fire_circle_result)

            # Post the offering
            await self.post_offering(pr_number, synthesis)

            logger.info("Ceremony completed successfully")

        except Exception as e:
            logger.error(f"Ceremony failed: {e}")
            # Still create results file for workflow
            with open("fire_circle_review_results.json", "w") as f:
                json.dump(
                    {
                        "pr_number": pr_number,
                        "error": str(e),
                        "ceremony_completed": False,
                    },
                    f,
                    indent=2,
                )
            raise


async def main():
    """Main entry point for the ceremony"""

    if len(sys.argv) < 2:
        print("Usage: python invoke_fire_circle_review.py <PR_NUMBER>")
        sys.exit(1)

    try:
        pr_number = int(sys.argv[1])
    except ValueError:
        print("PR_NUMBER must be an integer")
        sys.exit(1)

    # Ensure we have API keys loaded
    from mallku.firecircle.load_api_keys import load_api_keys_to_environment

    if not load_api_keys_to_environment():
        logger.warning("API keys not loaded - Fire Circle may use fallback voices")

    # Perform the ceremony
    facilitator = CeremonyFacilitator()
    await facilitator.perform_ceremony(pr_number)


if __name__ == "__main__":
    asyncio.run(main())
