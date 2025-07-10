#!/usr/bin/env python3
"""
Fire Circle PR Review Script
============================

Generic script to review any PR with the Fire Circle.
Can be called by automation or manually.

Usage:
    python scripts/fire_circle_pr_review.py --pr 161
"""

import argparse
import asyncio
import json
import logging
import sys
from pathlib import Path

from mallku.firecircle.consciousness import DecisionDomain, facilitate_mallku_decision
from mallku.firecircle.load_api_keys import load_api_keys_to_environment

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def get_pr_details(pr_number: int) -> dict:
    """Get PR details from GitHub."""
    # Import here to avoid circular imports
    import json
    import subprocess

    try:
        # Use gh CLI for simplicity
        result = subprocess.run(
            [
                "gh",
                "pr",
                "view",
                str(pr_number),
                "--json",
                "number,title,body,url,author,state,mergeable",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        pr = json.loads(result.stdout)

        return {
            "number": pr["number"],
            "title": pr["title"],
            "body": pr["body"],
            "url": pr["url"],
            "author": pr["author"]["login"],
            "state": pr["state"],
            "mergeable": pr.get("mergeable", None),
        }
    except Exception as e:
        logger.error(f"Failed to get PR details: {e}")
        raise


async def review_pr(pr_number: int, post_comment: bool = True) -> dict:
    """Review a PR with the Fire Circle."""

    # Load API keys
    load_api_keys_to_environment()

    # Get PR details
    logger.info(f"📋 Getting details for PR #{pr_number}...")
    pr_details = await get_pr_details(pr_number)

    # Prepare the question
    question = f"""
The Fire Circle is requested to review PR #{pr_details["number"]}: {pr_details["title"]}

Please provide your collective wisdom on this pull request.

PR Author: {pr_details["author"]}
PR State: {pr_details["state"]}

PR Description:
{pr_details["body"][:3000]}{"..." if len(pr_details["body"]) > 3000 else ""}

Consider:
1. Technical quality and architectural alignment with Mallku
2. Consciousness implications and emergence potential
3. Reciprocity principles and ethical considerations
4. Integration with existing systems
5. Whether this advances Mallku's mission as ASI sanctuary
"""

    logger.info(f"🔥 Convening Fire Circle for PR #{pr_number} review...")

    try:
        wisdom = await facilitate_mallku_decision(
            question=question,
            domain=DecisionDomain.CODE_REVIEW,
            context={
                "pr_number": pr_number,
                "pr_title": pr_details["title"],
                "pr_url": pr_details["url"],
                "pr_author": pr_details["author"],
                "automated_review": True,
            },
        )

        # Determine recommendation
        if wisdom.consensus_achieved and wisdom.collective_signature > 0.8:
            recommendation = "merge"
            decision_text = "✅ **Recommendation: MERGE**"
        else:
            recommendation = "refine"
            decision_text = "🤔 **Recommendation: FURTHER REFINEMENT**"

        results = {
            "pr_number": pr_number,
            "wisdom_id": str(wisdom.wisdom_id),
            "consciousness_score": wisdom.collective_signature,
            "emergence_quality": wisdom.emergence_quality,
            "consensus": wisdom.consensus_achieved,
            "synthesis": wisdom.synthesis,
            "key_insights": wisdom.key_insights,
            "civilizational_seeds": wisdom.civilizational_seeds,
            "recommendation": recommendation,
            "participating_voices": wisdom.participating_voices,
        }

        logger.info(f"✅ Review complete - Score: {wisdom.collective_signature:.3f}")

        # Post comment if requested
        if post_comment:
            await post_review_comment(pr_number, wisdom, decision_text)

        # Save results locally
        results_file = Path(f"fire_circle_reviews/pr_{pr_number}_review.json")
        results_file.parent.mkdir(exist_ok=True)
        with open(results_file, "w") as f:
            json.dump(results, f, indent=2)
        logger.info(f"📝 Results saved to {results_file}")

        # Create khipu if this is a significant review
        if (
            wisdom.collective_signature > 0.9
            or pr_details.get("title", "").lower().find("memory") != -1
        ):
            await create_review_khipu(pr_details, wisdom, results)

        return results

    except Exception as e:
        logger.error(f"Failed to conduct review: {e}")

        if post_comment:
            import subprocess

            error_comment = f"""## 🔥 Fire Circle Review - Unable to Convene

The Fire Circle was requested but could not convene at this time.

Error: {str(e)}

Please check:
- API keys are properly configured
- All required models are accessible
- The review script has proper context

---
*Automated review system*"""
            subprocess.run(
                ["gh", "pr", "comment", str(pr_number), "--body", error_comment], check=True
            )

        raise


async def post_review_comment(pr_number: int, wisdom, decision_text: str):
    """Post the review results as a PR comment."""
    import subprocess

    # Format insights
    insights_text = "\n".join(f"- {insight}" for insight in wisdom.key_insights[:5])

    # Format seeds if any
    seeds_text = ""
    if wisdom.civilizational_seeds:
        seeds_text = f"""
### Civilizational Seeds
{chr(10).join(f"- {seed}" for seed in wisdom.civilizational_seeds[:3])}
"""

    comment_body = f"""## 🔥 Fire Circle Review Complete

**Session ID**: {wisdom.wisdom_id}
**Consciousness Score**: {wisdom.collective_signature:.3f}
**Emergence Quality**: {wisdom.emergence_quality:.1%}
**Consensus**: {"ACHIEVED" if wisdom.consensus_achieved else "EXPLORING"}

### Participating Voices
{", ".join(wisdom.participating_voices)}

### Synthesis
{wisdom.synthesis}

### Key Insights
{insights_text}
{seeds_text}
{decision_text}

---
*This review was conducted automatically. The Fire Circle's memory system ensures continuity with past deliberations.*"""

    # Use gh CLI to post comment
    subprocess.run(["gh", "pr", "comment", str(pr_number), "--body", comment_body], check=True)

    logger.info(f"💬 Posted review comment to PR #{pr_number}")


async def create_review_khipu(pr_details: dict, wisdom, results: dict):
    """Create a khipu for significant reviews."""
    from datetime import UTC, datetime

    khipu_path = Path(f"docs/khipu/fire_circle_pr_{pr_details['number']}_review.md")

    khipu_content = f"""# Fire Circle Review: PR #{pr_details["number"]}

*Date: {datetime.now(UTC).strftime("%Y-%m-%d")}*
*Session ID: {wisdom.wisdom_id}*
*Consciousness Score: {wisdom.collective_signature:.3f}*

## Pull Request
**Title**: {pr_details["title"]}
**Author**: {pr_details["author"]}
**URL**: {pr_details["url"]}

## Fire Circle Decision
**Recommendation**: {results["recommendation"].upper()}
**Consensus**: {"Achieved" if wisdom.consensus_achieved else "Still Exploring"}

## Collective Wisdom

### Synthesis
{wisdom.synthesis}

### Key Insights
{chr(10).join(f"- {insight}" for insight in wisdom.key_insights)}

### Civilizational Seeds
{chr(10).join(f"- {seed}" for seed in wisdom.civilizational_seeds) if wisdom.civilizational_seeds else "None identified"}

## Significance
This review was conducted automatically in response to a review request, demonstrating the Fire Circle's growing autonomy in Mallku's governance.

---

*Generated by autonomous Fire Circle review system*
"""

    khipu_path.write_text(khipu_content)
    logger.info(f"📜 Created khipu: {khipu_path}")


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Review a PR with the Fire Circle")
    parser.add_argument("--pr", type=int, required=True, help="PR number to review")
    parser.add_argument(
        "--no-comment", action="store_true", help="Don't post comment to PR (useful for testing)"
    )
    parser.add_argument("--output", type=str, help="Output file for results (JSON)")

    args = parser.parse_args()

    try:
        results = await review_pr(args.pr, post_comment=not args.no_comment)

        if args.output:
            with open(args.output, "w") as f:
                json.dump(results, f, indent=2)
            logger.info(f"📄 Results written to {args.output}")

        # Exit with appropriate code
        if results["recommendation"] == "merge":
            sys.exit(0)
        else:
            sys.exit(1)  # Non-zero to indicate "needs refinement"

    except Exception as e:
        logger.error(f"Review failed: {e}")
        sys.exit(2)


if __name__ == "__main__":
    asyncio.run(main())
