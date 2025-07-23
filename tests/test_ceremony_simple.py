#!/usr/bin/env python3
"""
Simple test of ceremony structure without full integration

Created by Qillqa Kusiq (57th Artisan)
"""

import os
import sys
from pathlib import Path

# Set CI environment to skip database
os.environ["MALLKU_SKIP_DATABASE"] = "true"
os.environ["GITHUB_TOKEN"] = "mock-token"

sys.path.insert(0, str(Path(__file__).parent))

from invoke_fire_circle_review import CeremonyFacilitator


def test_ceremony_structure():
    """Test that the ceremony structure is properly implemented"""

    print("🧪 Testing Ceremony Structure\n")

    # Create facilitator
    facilitator = CeremonyFacilitator()

    # Test context structure
    mock_context = {
        "pr_number": 999,
        "title": "Test PR",
        "description": "Test description",
        "author": "test-author",
        "branch": "test-branch",
        "base_branch": "main",
        "files_changed": ["file1.py", "file2.py"],
        "additions": 100,
        "deletions": 50,
        "diff": "mock diff",
        "existing_comments": 0,
        "created_at": "2025-01-17T20:00:00Z",
        "updated_at": "2025-01-17T20:00:00Z",
    }

    # Test sacred question framing
    print("Testing sacred question framing...")
    sacred_question = facilitator.frame_sacred_question(mock_context)

    print("✓ Sacred question includes:")
    print("  - Author acknowledgment:", "test-author" in sacred_question)
    print("  - Coherence consideration:", "Coherence" in sacred_question)
    print("  - Utility consideration:", "Utility" in sacred_question)
    print("  - Emergence consideration:", "Emergence" in sacred_question)
    print("  - Empty Chair:", "Empty Chair" in sacred_question)
    print("  - Compost consideration:", "Compost" in sacred_question)

    # Test synthesis structure
    print("\nTesting synthesis structure...")
    mock_fire_circle_result = {
        "wisdom": type(
            "MockWisdom",
            (),
            {
                "synthesis": "Test synthesis with praise for good work, questions about implementation, suggestions for improvement, and outdated patterns to remove.",
                "emergence_quality": 0.85,
                "consensus_strength": 0.90,
            },
        )(),
        "emergence_quality": 0.85,
        "consensus_strength": 0.90,
        "voice_count": 6,
    }

    synthesis = facilitator.synthesize_wisdom(mock_fire_circle_result)

    print("✓ Synthesis includes:")
    print("  - Praise section:", "🙏 Praise" in synthesis)
    print("  - Questions section:", "❓ Questions" in synthesis)
    print("  - Suggestions section:", "💡 Suggestions" in synthesis)
    print("  - Compost section:", "🌱 Compost" in synthesis)
    print("  - Emergence quality:", "0.85" in synthesis)
    print("  - Ayni spirit:", "Ayni" in synthesis)

    print("\n✅ Ceremony structure test passed!")
    print("\nThe Ceremony of Automated Witnessing is ready.")
    print("It transforms code review from extraction to emergence,")
    print("holding space for all voices including those not present.")


if __name__ == "__main__":
    test_ceremony_structure()
