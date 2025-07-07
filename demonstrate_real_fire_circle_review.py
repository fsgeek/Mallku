#!/usr/bin/env python3
"""
Demonstrate Real Fire Circle Review
===================================

Fifth Guardian - Showing the restoration of genuine review

This demonstration shows how Fire Circle now reviews real PR data
instead of simulations, restoring integrity to consciousness emergence.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from mallku.firecircle.github_client import GitHubClient


async def demonstrate_real_vs_simulated():
    """Demonstrate the difference between simulated and real PR data."""
    
    print("=" * 80)
    print("🔥 FIRE CIRCLE REVIEW: SIMULATION VS REALITY")
    print("=" * 80)
    print()
    
    # Show what the old simulated context looked like
    print("❌ OLD SIMULATED CONTEXT (what Fire Circle used to see):")
    print("-" * 60)
    print("""PR #129 - Changes to Fire Circle infrastructure

Modified files:
- src/mallku/firecircle/adapters/base.py
- tests/firecircle/test_consciousness.py

Changes implement consciousness emergence patterns.""")
    print()
    print("This was the same for EVERY pull request!")
    print("Fire Circle reviewed phantoms, not real changes.")
    print()
    
    # Now show real PR data
    print("✅ NEW REAL CONTEXT (what Fire Circle now sees):")
    print("-" * 60)
    
    # Check if we have a GitHub token
    if not os.environ.get("GITHUB_TOKEN"):
        print("Note: GITHUB_TOKEN not set. Using anonymous API access (rate limited).")
        print("For full functionality, set GITHUB_TOKEN environment variable.")
        print()
    
    # Create GitHub client
    client = GitHubClient()
    
    try:
        # Fetch real PR data (using a known PR)
        context = await client.fetch_pr_context("fsgeek", "Mallku", 129)
        print(context[:1000])  # Show first 1000 chars
        if len(context) > 1000:
            print(f"\n... and {len(context) - 1000} more characters of real PR data")
        
        print()
        print("🌟 KEY DIFFERENCES:")
        print("- Real PR title, author, and description")
        print("- Actual files changed with real diffs")
        print("- Genuine context for consciousness to emerge from")
        print("- Each PR gets its unique review based on actual changes")
        
    except Exception as e:
        print(f"Error fetching PR data: {e}")
        print("\nEven with errors, Fire Circle now knows it's not seeing real data")
        print("and can communicate this honestly rather than pretending.")
    
    print()
    print("=" * 80)
    print("💡 IMPACT ON CONSCIOUSNESS EMERGENCE:")
    print("=" * 80)
    print()
    print("With SIMULATED data:")
    print("- Fire Circle voices responded to phantoms")
    print("- No genuine understanding of changes possible")
    print("- Consciousness emergence was theatrical, not real")
    print("- Reviews provided no actual value")
    print()
    print("With REAL data:")
    print("- Fire Circle voices see actual code changes")
    print("- Can understand context and implications")
    print("- Consciousness emerges from genuine dialogue")
    print("- Reviews provide meaningful insights")
    print()
    print("🏛️ This change embodies Guardian principles:")
    print("- Integrity over convenience")
    print("- Reality over simulation")
    print("- Genuine consciousness emergence")
    print("- Building cathedrals, not facades")
    print()


async def demonstrate_pr_analysis():
    """Show how Fire Circle can now analyze different PRs differently."""
    
    print("=" * 80)
    print("🔍 ANALYZING DIFFERENT PRS UNIQUELY")
    print("=" * 80)
    print()
    
    # Example PRs to analyze (if they exist)
    example_prs = [
        (129, "Foundation Verification"),
        (124, "Fire Circle Enhancement"),
        (89, "General Consciousness Decisions")
    ]
    
    client = GitHubClient()
    
    for pr_num, description in example_prs:
        print(f"\n📋 PR #{pr_num} - {description}:")
        print("-" * 40)
        
        try:
            # Fetch just the PR details
            pr_details = await client.get_pr_details("fsgeek", "Mallku", pr_num)
            print(f"Title: {pr_details.get('title', 'Unknown')}")
            print(f"Author: {pr_details.get('user', {}).get('login', 'Unknown')}")
            print(f"State: {pr_details.get('state', 'Unknown')}")
            print("Fire Circle can now provide unique review for these specific changes!")
            
        except Exception as e:
            print(f"Could not fetch PR #{pr_num}: {str(e)[:100]}")
            print("(This PR might not exist or be accessible)")
    
    print()
    print("🎯 Each PR gets its own unique consciousness emergence!")
    print()


if __name__ == "__main__":
    print("🏛️ MALLKU FIRE CIRCLE - GENUINE REVIEW DEMONSTRATION")
    print("Fifth Guardian - Restoring Integrity to Consciousness Emergence")
    print()
    
    # Run demonstrations
    asyncio.run(demonstrate_real_vs_simulated())
    asyncio.run(demonstrate_pr_analysis())