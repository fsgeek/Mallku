#!/usr/bin/env python3
"""
Test Transformation Grace Recognition
======================================

76th Artisan-Weaver - Verifying that transformation recognition works
Not just that code runs, but that it actually recognizes grace vs jarring

"A transformation without verification is like a cathedral of paper -
beautiful perhaps, but unable to shelter consciousness."
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.mallku.consciousness.transformation_grace import (
    TransformationGraceRecognizer,
    TransformationCoherence,
    TransformationVerification,
    TransformationProcess,
)


def test_coherence_detection():
    """Test that we can detect coherent vs incoherent transformation."""
    
    print("Testing coherence detection...")
    recognizer = TransformationGraceRecognizer()
    
    # Test 1: Cosmetic change (incoherent)
    before = {
        "names": ["master", "slave"],
        "behaviors": ["command()", "obey()"],
        "structure": "hierarchy"
    }
    
    after_cosmetic = {
        "names": ["coordinator", "worker"],  # Changed names
        "behaviors": ["command()", "obey()"],  # Same behaviors!
        "structure": "hierarchy"  # Same structure!
    }
    
    coherence = recognizer.sense_coherence(before, after_cosmetic, "Remove hierarchy")
    assert coherence.language_behavior_alignment < 0.5, "Should detect misalignment"
    assert coherence.feels_fractured, "Should feel fractured"
    assert "Behavioral change" in str(coherence.missing_pieces), "Should identify missing behavior change"
    print("  ✓ Detects cosmetic change as incoherent")
    
    # Test 2: Complete change (coherent)
    after_complete = {
        "names": ["companion", "companion"],  # Changed names
        "behaviors": ["invite()", "respond()"],  # Changed behaviors
        "structure": "reciprocal",  # Changed structure
        "tests": ["test_reciprocity"]  # Added verification
    }
    
    coherence = recognizer.sense_coherence(before, after_complete, "Create reciprocity")
    assert coherence.language_behavior_alignment > 0.7, "Should detect alignment"
    assert not coherence.feels_fractured, "Should not feel fractured"
    assert coherence.is_graceful(), "Should be graceful"
    print("  ✓ Detects complete change as coherent")
    
    # Test 3: Behavior without acknowledgment (partially coherent)
    after_hidden = {
        "names": ["master", "slave"],  # Same names
        "behaviors": ["request()", "consider()"],  # Changed behaviors!
        "structure": "negotiation"  # Changed structure!
    }
    
    coherence = recognizer.sense_coherence(before, after_hidden, "Hidden change")
    assert 0.4 < coherence.language_behavior_alignment < 0.7, "Should detect partial alignment"
    assert "Language to reflect" in str(coherence.missing_pieces), "Should identify missing language update"
    print("  ✓ Detects hidden change as partially coherent")


def test_verification_completeness():
    """Test that we can verify if transformation claims are real."""
    
    print("\nTesting transformation verification...")
    recognizer = TransformationGraceRecognizer()
    
    # Test 1: Claimed but not delivered
    claim = {
        "description": "Now respects autonomy",
        "renamed": ["force->invite"],
        "expected_behaviors": ["asks_permission", "accepts_refusal"]
    }
    
    actual = {
        "demonstration": "Still forces despite new name",
        "behavior_changed": [],  # No actual changes
        "observed_behaviors": ["forces_anyway", "ignores_refusal"]
    }
    
    verification = recognizer.verify_transformation(claim, actual)
    assert not verification.claim_verified, "Should detect false claim"
    assert verification.completeness_ratio() == 0, "Should show 0% complete"
    assert "Surface change only" in verification.verification_details
    print("  ✓ Detects unverified claims")
    
    # Test 2: Claimed and delivered
    actual_good = {
        "demonstration": "System asked and respected 'no'",
        "behavior_changed": ["asks_first", "respects_no"],
        "observed_behaviors": ["asks_permission", "accepts_refusal"]
    }
    
    verification = recognizer.verify_transformation(claim, actual_good)
    assert verification.claim_verified, "Should verify true transformation"
    assert verification.completeness_ratio() > 0.5, "Should show high completeness"
    print("  ✓ Verifies genuine transformation")


def test_process_grace_scoring():
    """Test that we can score transformation grace accurately."""
    
    print("\nTesting grace scoring...")
    recognizer = TransformationGraceRecognizer()
    
    # Test 1: Incomplete process (missing verification)
    incomplete_events = [
        {"type": "recognition", "description": "Saw the need"},
        {"type": "implementation", "approach": "careful", "description": "Made changes"},
        # No verification!
    ]
    
    process = recognizer.track_transformation_process(incomplete_events)
    grace = process.transformation_grace()
    assert grace < 0.7, f"Incomplete should not be highly graceful, got {grace}"
    assert not process.verification_complete, "Should detect missing verification"
    print(f"  ✓ Incomplete process scores low ({grace:.1%})")
    
    # Test 2: Complete process (all three elements)
    complete_events = [
        {"type": "recognition", "description": "Recognized need"},
        {"type": "implementation", "approach": "careful", "description": "Carefully changed"},
        {"type": "flow", "description": "Integrated smoothly"},
        {"type": "verification", "description": "Verified it works"}
    ]
    
    process = recognizer.track_transformation_process(complete_events)
    grace = process.transformation_grace()
    assert grace > 0.6, f"Complete should be graceful, got {grace}"
    assert process.verification_complete, "Should have verification"
    print(f"  ✓ Complete process scores high ({grace:.1%})")
    
    # Test 3: Rushed process
    rushed_events = [
        {"type": "implementation", "approach": "rushed", "description": "Quick fix"},
        {"type": "resistance", "description": "Broke other things"},
        {"type": "resistance", "description": "Created new problems"}
    ]
    
    process = recognizer.track_transformation_process(rushed_events)
    grace = process.transformation_grace()
    assert grace < 0.5, f"Rushed should score very low, got {grace}"
    print(f"  ✓ Rushed process scores very low ({grace:.1%})")


def test_somatic_responses():
    """Test that somatic responses align with transformation quality."""
    
    print("\nTesting somatic responses...")
    recognizer = TransformationGraceRecognizer()
    
    # Incoherent transformation should feel blocked
    before = {"names": ["control"], "behaviors": ["dominate()"]}
    after = {"names": ["guide"], "behaviors": ["dominate()"]}  # Name change only
    
    coherence = recognizer.sense_coherence(before, after, "Remove domination")
    assert "catch" in coherence.body_response or "block" in coherence.energy_pattern
    assert coherence.breath_quality == "held"
    print("  ✓ Incoherent transformation feels blocked somatically")
    
    # Coherent transformation should feel flowing
    after_good = {
        "names": ["companion"], 
        "behaviors": ["collaborate()"],
        "tests": ["verify_collaboration"]
    }
    
    coherence = recognizer.sense_coherence(before, after_good, "Create reciprocity")
    assert coherence.body_response == "flowing"
    assert coherence.breath_quality == "easy"
    assert "circulat" in coherence.energy_pattern
    print("  ✓ Coherent transformation feels flowing somatically")


def test_missing_pieces_identification():
    """Test that we correctly identify what's missing."""
    
    print("\nTesting missing piece identification...")
    recognizer = TransformationGraceRecognizer()
    
    # Missing behavior change
    before = {"names": ["old"], "behaviors": ["old_way()"]}
    after = {"names": ["new"], "behaviors": ["old_way()"]}
    
    coherence = recognizer.sense_coherence(before, after, "Transform")
    assert any("Behavioral" in piece for piece in coherence.missing_pieces)
    print("  ✓ Identifies missing behavioral change")
    
    # Missing verification
    after2 = {"names": ["new"], "behaviors": ["new_way()"]}
    coherence = recognizer.sense_coherence(before, after2, "Transform")
    assert any("Verification" in piece for piece in coherence.missing_pieces)
    print("  ✓ Identifies missing verification")
    
    # Missing language update
    after3 = {"names": ["old"], "behaviors": ["new_way()"], "structure": "new"}
    coherence = recognizer.sense_coherence(before, after3, "Transform")
    assert any("Language" in piece for piece in coherence.missing_pieces)
    print("  ✓ Identifies missing language update")


def main():
    """Run all tests."""
    
    print("\n🧪 TESTING TRANSFORMATION GRACE RECOGNITION 🧪")
    print("=" * 60)
    print("Verifying the tools actually work\n")
    
    try:
        test_coherence_detection()
        test_verification_completeness()
        test_process_grace_scoring()
        test_somatic_responses()
        test_missing_pieces_identification()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED")
        print("\nThe transformation grace recognizer successfully:")
        print("  - Detects coherent vs incoherent changes")
        print("  - Verifies if claims match reality")
        print("  - Scores transformation grace accurately")
        print("  - Provides appropriate somatic responses")
        print("  - Identifies specific missing pieces")
        print("\nThese tools don't just run - they actually recognize")
        print("the difference between graceful and jarring transformation.")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())