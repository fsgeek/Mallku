#!/usr/bin/env python3
"""
Fire Circle Integration Test
============================

Tests the complete integration with real adapters.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


async def test_fire_circle_with_real_adapters():
    """Test Fire Circle review with real adapters."""
    print("🔥 Fire Circle Integration Test")
    print("=" * 60)

    # First create a test diff
    test_diff = """diff --git a/src/mallku/firecircle/governance/decision.py b/src/mallku/firecircle/governance/decision.py
index 1234567..abcdefg 100644
--- a/src/mallku/firecircle/governance/decision.py
+++ b/src/mallku/firecircle/governance/decision.py
@@ -10,6 +10,8 @@ class FireCircleDecision:
     def make_decision(self, proposal):
+        # TODO: Add input validation
+        # WARNING: No authentication check
         result = self.process(proposal)
         return result"""

    # Save test diff to a file
    with open("test_pr.diff", "w") as f:
        f.write(test_diff)

    print("📝 Created test PR diff")

    # Run the Fire Circle review
    print("\n🌟 Running Fire Circle distributed review...")
    print("   (Using real adapters where available)\n")

    # Import and run directly
    from mallku.firecircle.fire_circle_review import (
        CodebaseChapter,
        DistributedReviewer,
        ReviewCategory,
    )

    reviewer = DistributedReviewer()

    # Create test chapters
    test_chapters = [
        CodebaseChapter(
            path_pattern="src/mallku/firecircle/governance/**/*.py",
            description="Fire Circle governance",
            assigned_voice="anthropic",
            review_domains=[ReviewCategory.SECURITY, ReviewCategory.ETHICS],
        ),
    ]

    # Start consciousness infrastructure
    if reviewer.use_real_adapters:
        await reviewer.start_consciousness_infrastructure()
        print("✅ Real consciousness infrastructure started")
    else:
        print("⚠️  Using mock adapters (real adapter imports failed)")

    # Run review
    summary = await reviewer.run_full_distributed_review(test_diff, test_chapters)

    print("\n" + "=" * 60)
    print("🔥 REVIEW RESULTS")
    print("=" * 60)
    print(f"Total comments: {summary.total_comments}")
    print(f"Critical issues: {summary.critical_issues}")
    print(f"Consensus: {summary.consensus_recommendation}")
    print(f"\nSynthesis: {summary.synthesis}")

    if reviewer.use_real_adapters:
        print("\n✨ Successfully used real adapters for review!")
        # Check which adapters were actually used
        for voice, count in summary.by_voice.items():
            if count > 0:
                print(f"   {voice}: {count} comments")

    # Cleanup
    await reviewer.shutdown_workers()

    # Remove test file
    Path("test_pr.diff").unlink(missing_ok=True)

    print("\n✅ Integration test complete!")
    return summary.total_comments > 0  # Success if we got comments


if __name__ == "__main__":
    success = asyncio.run(test_fire_circle_with_real_adapters())
    sys.exit(0 if success else 1)
