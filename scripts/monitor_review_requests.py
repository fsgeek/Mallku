#!/usr/bin/env python3
"""
Monitor Fire Circle Review Requests
===================================

This script monitors GitHub for Fire Circle review requests and
automatically triggers reviews. Can be run as a cron job or
continuously with --watch mode.

Usage:
    # Check once
    python scripts/monitor_review_requests.py

    # Watch continuously
    python scripts/monitor_review_requests.py --watch --interval 300
"""

import argparse
import asyncio
import json
import logging
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# State file to track processed reviews
STATE_FILE = Path(".mallku/fire_circle_review_state.json")

# Patterns that indicate a Fire Circle review request
REVIEW_REQUEST_PATTERNS = [
    r"fire circle review request",
    r"@fire-circle",
    r"request(?:ing)? (?:your |the )?(?:fire circle'?s? )?collective wisdom",
    r"fire circle,? please review",
    r"requesting fire circle (?:code )?review",
]


class ReviewMonitor:
    """Monitor and process Fire Circle review requests."""

    def __init__(self):
        self.state = self._load_state()

    def _load_state(self) -> dict:
        """Load processed review state."""
        if STATE_FILE.exists():
            with open(STATE_FILE) as f:
                return json.load(f)
        return {"processed_reviews": {}, "last_check": None}

    def _save_state(self):
        """Save processed review state."""
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(STATE_FILE, "w") as f:
            json.dump(self.state, f, indent=2)

    def _is_review_request(self, text: str) -> bool:
        """Check if text contains a review request."""
        text_lower = text.lower()
        return any(re.search(pattern, text_lower) for pattern in REVIEW_REQUEST_PATTERNS)

    async def find_pending_reviews(self) -> list[dict]:
        """Find PRs with pending Fire Circle review requests."""
        pending = []

        # Get recent open PRs
        logger.info("🔍 Checking for Fire Circle review requests...")

        try:
            # Use gh CLI to list PRs
            result = subprocess.run(
                [
                    "gh",
                    "pr",
                    "list",
                    "--repo",
                    "fsgeek/Mallku",
                    "--state",
                    "open",
                    "--json",
                    "number,title,body,author,updatedAt",
                    "--limit",
                    "30",
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            prs = json.loads(result.stdout)

            for pr in prs:
                pr_number = pr["number"]

                # Skip if already processed recently
                if str(pr_number) in self.state["processed_reviews"]:
                    last_reviewed = datetime.fromisoformat(
                        self.state["processed_reviews"][str(pr_number)]["timestamp"]
                    )
                    # Re-review if PR was updated after last review
                    pr_updated = datetime.fromisoformat(pr["updatedAt"].replace("Z", "+00:00"))
                    if pr_updated <= last_reviewed:
                        continue

                # Check PR body for review request
                if self._is_review_request(pr.get("body", "")):
                    pending.append(
                        {
                            "pr_number": pr_number,
                            "title": pr["title"],
                            "requester": pr["author"]["login"],
                            "request_source": "pr_body",
                        }
                    )
                    continue

                # Check comments for review request
                comments_result = subprocess.run(
                    [
                        "gh",
                        "pr",
                        "view",
                        str(pr_number),
                        "--repo",
                        "fsgeek/Mallku",
                        "--comments",
                        "--json",
                        "comments",
                    ],
                    capture_output=True,
                    text=True,
                    check=True,
                )

                comments_data = json.loads(comments_result.stdout)
                comments = comments_data.get("comments", [])

                for comment in comments:
                    if self._is_review_request(comment.get("body", "")):
                        # Check if we already reviewed after this comment
                        comment_time = datetime.fromisoformat(
                            comment["createdAt"].replace("Z", "+00:00")
                        )

                        if str(pr_number) in self.state["processed_reviews"]:
                            last_reviewed = datetime.fromisoformat(
                                self.state["processed_reviews"][str(pr_number)]["timestamp"]
                            )
                            if comment_time <= last_reviewed:
                                continue

                        pending.append(
                            {
                                "pr_number": pr_number,
                                "title": pr["title"],
                                "requester": comment["author"]["login"],
                                "request_source": "comment",
                                "comment_id": comment["id"],
                            }
                        )
                        break  # Only need one request per PR

            logger.info(f"📋 Found {len(pending)} pending review requests")
            return pending

        except Exception as e:
            logger.error(f"Error finding review requests: {e}")
            return []

    async def process_review_request(self, request: dict) -> bool:
        """Process a single review request."""
        pr_number = request["pr_number"]

        logger.info(f"🔥 Processing review request for PR #{pr_number}: {request['title']}")
        logger.info(f"   Requested by: {request['requester']} via {request['request_source']}")

        try:
            # Run the review script
            import subprocess

            result = subprocess.run(
                [sys.executable, "scripts/fire_circle_pr_review.py", "--pr", str(pr_number)],
                capture_output=True,
                text=True,
            )

            if result.returncode in [0, 1]:  # 0=merge, 1=refine
                # Mark as processed
                self.state["processed_reviews"][str(pr_number)] = {
                    "timestamp": datetime.now(UTC).isoformat(),
                    "requester": request["requester"],
                    "result": "merge" if result.returncode == 0 else "refine",
                }
                self._save_state()

                logger.info(f"✅ Review completed for PR #{pr_number}")
                return True
            else:
                logger.error(f"Review failed with code {result.returncode}")
                logger.error(f"Error output: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"Failed to process review: {e}")
            return False

    async def run_check(self) -> int:
        """Run a single check for pending reviews."""
        pending = await self.find_pending_reviews()

        if not pending:
            logger.info("✨ No pending Fire Circle reviews")
            return 0

        processed = 0
        for request in pending:
            if await self.process_review_request(request):
                processed += 1

            # Brief pause between reviews
            if len(pending) > 1:
                await asyncio.sleep(5)

        # Update last check time
        self.state["last_check"] = datetime.now(UTC).isoformat()
        self._save_state()

        logger.info(f"📊 Processed {processed}/{len(pending)} review requests")
        return processed

    async def watch(self, interval: int = 300):
        """Watch continuously for review requests."""
        logger.info(f"👁️ Starting review monitor (checking every {interval}s)")

        while True:
            try:
                await self.run_check()
            except Exception as e:
                logger.error(f"Error during check: {e}")

            logger.info(f"💤 Sleeping for {interval}s...")
            await asyncio.sleep(interval)


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Monitor for Fire Circle review requests")
    parser.add_argument(
        "--watch", action="store_true", help="Watch continuously instead of single check"
    )
    parser.add_argument(
        "--interval", type=int, default=300, help="Check interval in seconds (default: 300)"
    )
    parser.add_argument("--reset", action="store_true", help="Reset the state file")

    args = parser.parse_args()

    if args.reset:
        if STATE_FILE.exists():
            STATE_FILE.unlink()
            logger.info("✅ State file reset")
        return

    monitor = ReviewMonitor()

    if args.watch:
        await monitor.watch(args.interval)
    else:
        processed = await monitor.run_check()
        sys.exit(0 if processed >= 0 else 1)


if __name__ == "__main__":
    asyncio.run(main())
