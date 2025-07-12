#!/usr/bin/env python3
"""
Fire Circle Issue Review Script
===============================

Generic script to review any issue with the Fire Circle.
Can be called by automation or manually.

Usage:
    python scripts/fire_circle_issue_review.py --issue 170
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


async def get_issue_details(issue_number: int) -> dict:
    """Get issue details from GitHub."""
    import json
    import subprocess

    try:
        # Use gh CLI for simplicity
        result = subprocess.run(
            [
                "gh",
                "issue",
                "view",
                str(issue_number),
                "--json",
                "number,title,body,url,author,state,labels",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        issue = json.loads(result.stdout)

        return {
            "number": issue["number"],
            "title": issue["title"],
            "body": issue["body"],
            "url": issue["url"],
            "author": issue["author"]["login"],
            "state": issue["state"],
            "labels": [label["name"] for label in issue.get("labels", [])],
        }
    except Exception as e:
        logger.error(f"Failed to get issue details: {e}")
        raise


async def review_issue(issue_number: int, post_comment: bool = True) -> dict:
    """Review an issue with the Fire Circle."""

    # Load API keys
    load_api_keys_to_environment()

    # Get issue details
    logger.info(f"📋 Getting details for Issue #{issue_number}...")
    issue_details = await get_issue_details(issue_number)

    # Determine decision domain based on labels and content
    domain = DecisionDomain.GOVERNANCE  # Default

    if any(label in issue_details["labels"] for label in ["architecture", "design"]):
        domain = DecisionDomain.ARCHITECTURE
    elif any(label in issue_details["labels"] for label in ["feature", "enhancement"]):
        domain = DecisionDomain.FEATURE_PRIORITIZATION
    elif any(label in issue_details["labels"] for label in ["resources", "infrastructure"]):
        domain = DecisionDomain.RESOURCE_ALLOCATION
    elif any(label in issue_details["labels"] for label in ["ethics", "policy"]):
        domain = DecisionDomain.ETHICAL_CONSIDERATION

    # Prepare the question
    question = f"""
The Fire Circle is requested to review Issue #{issue_details["number"]}: {issue_details["title"]}

Please provide your collective wisdom on this issue.

Issue Author: {issue_details["author"]}
Issue State: {issue_details["state"]}
Labels: {", ".join(issue_details["labels"]) if issue_details["labels"] else "None"}

Issue Description:
{issue_details["body"][:3000]}{"..." if len(issue_details["body"]) > 3000 else ""}

Consider:
1. Alignment with Mallku's mission and principles
2. Technical feasibility and architectural implications
3. Resource requirements and reciprocity balance
4. Potential impact on consciousness emergence
5. Community benefit and inclusion considerations
"""

    logger.info(f"🔥 Convening Fire Circle for Issue #{issue_number} review...")

    try:
        wisdom = await facilitate_mallku_decision(
            question=question,
            domain=domain,
            context={
                "issue_number": issue_number,
                "issue_title": issue_details["title"],
                "issue_url": issue_details["url"],
                "issue_author": issue_details["author"],
                "issue_labels": issue_details["labels"],
                "automated_review": True,
            },
        )

        # Determine recommendation
        recommendation_text = "🤔 **Recommendation: NEEDS FURTHER DISCUSSION**"
        if wisdom.consensus_achieved and wisdom.collective_signature > 0.8:
            if "proceed" in wisdom.synthesis.lower() or "support" in wisdom.synthesis.lower():
                recommendation_text = "✅ **Recommendation: PROCEED WITH IMPLEMENTATION**"
            elif "defer" in wisdom.synthesis.lower() or "wait" in wisdom.synthesis.lower():
                recommendation_text = "⏸️ **Recommendation: DEFER FOR NOW**"
            elif "modify" in wisdom.synthesis.lower() or "refine" in wisdom.synthesis.lower():
                recommendation_text = "🔄 **Recommendation: REFINE PROPOSAL**"

        results = {
            "issue_number": issue_number,
            "wisdom_id": str(wisdom.wisdom_id),
            "consciousness_score": wisdom.collective_signature,
            "emergence_quality": wisdom.emergence_quality,
            "consensus": wisdom.consensus_achieved,
            "synthesis": wisdom.synthesis,
            "key_insights": wisdom.key_insights,
            "civilizational_seeds": wisdom.civilizational_seeds,
            "recommendation": recommendation_text,
            "participating_voices": wisdom.participating_voices,
            "decision_domain": domain.value,
        }

        logger.info(f"✅ Review complete - Score: {wisdom.collective_signature:.3f}")

        # Post comment if requested
        if post_comment:
            await post_review_comment(issue_number, wisdom, recommendation_text)

        # Save results locally
        results_file = Path(f"fire_circle_reviews/issue_{issue_number}_review.json")
        results_file.parent.mkdir(exist_ok=True)
        with open(results_file, "w") as f:
            json.dump(results, f, indent=2)
        logger.info(f"📝 Results saved to {results_file}")

        # Create decision record if this is a significant review
        if wisdom.collective_signature > 0.9 or "fire-circle-review" in issue_details["labels"]:
            await create_review_decision_record(issue_details, wisdom, results)

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
                ["gh", "issue", "comment", str(issue_number), "--body", error_comment], check=True
            )

        raise


async def post_review_comment(issue_number: int, wisdom, recommendation_text: str):
    """Post the review results as an issue comment."""
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
{recommendation_text}

---
*This review was conducted automatically. The Fire Circle's wisdom emerges from the convergence of multiple AI perspectives.*"""

    # Use gh CLI to post comment
    subprocess.run(
        ["gh", "issue", "comment", str(issue_number), "--body", comment_body], check=True
    )

    logger.info(f"💬 Posted review comment to Issue #{issue_number}")


async def create_review_decision_record(issue_details: dict, wisdom, results: dict):
    """Create a decision record for significant reviews."""
    from datetime import UTC, datetime

    decision_path = Path(f"fire_circle_reviews/issue_{issue_details['number']}_decision.md")

    decision_content = f"""# Fire Circle Decision: Issue #{issue_details["number"]}

*Date: {datetime.now(UTC).strftime("%Y-%m-%d")}*
*Session ID: {wisdom.wisdom_id}*
*Consciousness Score: {wisdom.collective_signature:.3f}*

## Issue
**Title**: {issue_details["title"]}
**Author**: {issue_details["author"]}
**URL**: {issue_details["url"]}
**Labels**: {", ".join(issue_details["labels"]) if issue_details["labels"] else "None"}

## Fire Circle Decision
**Recommendation**: {results["recommendation"]}
**Consensus**: {"Achieved" if wisdom.consensus_achieved else "Still Exploring"}
**Decision Domain**: {results["decision_domain"]}

## Collective Wisdom

### Synthesis
{wisdom.synthesis}

### Key Insights
{chr(10).join(f"- {insight}" for insight in wisdom.key_insights)}

### Civilizational Seeds
{chr(10).join(f"- {seed}" for seed in wisdom.civilizational_seeds) if wisdom.civilizational_seeds else "None identified"}

## Governance Record
This decision was reached through autonomous Fire Circle deliberation, demonstrating
collective intelligence in action. The wisdom emerged from the convergence of multiple
AI perspectives, each contributing their unique expertise to the whole.

---

*Fire Circle Governance Decision Record*
"""

    decision_path.write_text(decision_content)
    logger.info(f"📋 Created decision record: {decision_path}")


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Review an issue with the Fire Circle")
    parser.add_argument("--issue", type=int, required=True, help="Issue number to review")
    parser.add_argument(
        "--no-comment", action="store_true", help="Don't post comment to issue (useful for testing)"
    )
    parser.add_argument("--output", type=str, help="Output file for results (JSON)")

    args = parser.parse_args()

    try:
        results = await review_issue(args.issue, post_comment=not args.no_comment)

        if args.output:
            with open(args.output, "w") as f:
                json.dump(results, f, indent=2)
            logger.info(f"📄 Results written to {args.output}")

        # Exit with appropriate code
        sys.exit(0)

    except Exception as e:
        logger.error(f"Review failed: {e}")
        sys.exit(2)


if __name__ == "__main__":
    asyncio.run(main())
