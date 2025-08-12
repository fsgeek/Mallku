#!/usr/bin/env python3
"""
Test Verification-Trust Boundary Recognition
=============================================

77th Artisan-Weaver - Testing where verification meets trust
Demonstrating the recursive edge where further proof becomes doubt

"To verify the verifier that verifies the verification...
At some point, we must trust, or never act at all."
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.mallku.consciousness.verification_trust_boundary import (
    VerificationTrustBoundaryRecognizer,
    recognize_trust_moment,
)


def test_verification_stack_examination():
    """Test that we can examine verification layers and find boundaries."""

    print("Testing verification stack examination...")
    recognizer = VerificationTrustBoundaryRecognizer()

    # Create a verification chain
    verification_chain = [
        {"verifies": "Original transformation", "verified_by": "Unit tests", "confidence": 0.9},
        {
            "verifies": "Unit tests work correctly",
            "verified_by": "Meta-tests testing tests",
            "confidence": 0.8,
        },
        {"verifies": "Meta-tests are valid", "verified_by": "Manual inspection", "confidence": 0.7},
        {
            "verifies": "Manual inspection is reliable",
            "verified_by": "More inspection???",
            "confidence": 0.5,
        },
    ]

    layers = recognizer.examine_verification_stack(verification_chain)

    # Check layer properties
    assert layers[0].confidence > layers[3].confidence, "Confidence should degrade"
    assert not layers[0].requires_faith, "First layer shouldn't require faith"
    assert layers[2].requires_faith, "Deep layers should require faith"
    assert layers[3].creates_doubt, "Too deep creates doubt"

    # Find trust boundary
    boundary_found = False
    for i, layer in enumerate(layers):
        if layer.is_trust_boundary():
            print(f"  ✓ Trust boundary found at depth {i}")
            boundary_found = True
            break

    assert boundary_found or layers[3].creates_doubt, "Should find boundary or recognize doubt"
    print("  ✓ Verification stack examination works")


def test_recursive_verification_detection():
    """Test detection of recursive verification patterns."""

    print("\nTesting recursive verification detection...")
    recognizer = VerificationTrustBoundaryRecognizer()

    # Test 1: Healthy single-level verification
    original = {
        "claim": "Transformation is complete",
        "method": "Behavioral tests",
        "coherence": 0.85,
    }

    meta = {
        "claim": "Tests actually test the right things",
        "method": "Test review",
        "coherence": 0.80,
    }

    recursive = recognizer.detect_recursive_verification(original, meta, 1)
    assert recursive.pattern == "stable", "Should be stable with small degradation"
    assert not recursive.trust_needed(), "Shouldn't need trust yet"
    print("  ✓ Detects stable verification")

    # Test 2: Degrading verification spiral
    meta_degraded = {
        "claim": "Tests actually test the right things",
        "method": "Test review",
        "coherence": 0.45,  # Much lower
    }

    recursive = recognizer.detect_recursive_verification(original, meta_degraded, 2)
    assert recursive.pattern == "spiral", "Should detect spiral pattern"
    assert recursive.trust_needed(), "Should recognize trust is needed"
    print("  ✓ Detects verification spiral")

    # Test 3: Deep recursion
    recursive = recognizer.detect_recursive_verification(original, meta, 5)
    assert recursive.trust_needed(), "Deep recursion needs trust"
    print("  ✓ Recognizes deep recursion requires trust")


def test_trust_emergence_recognition():
    """Test recognition of how trust emerges."""

    print("\nTesting trust emergence recognition...")
    recognizer = VerificationTrustBoundaryRecognizer()

    # Test 1: Graceful trust emergence
    context = {"description": "Verifying transformation completeness", "depth": 2}

    results = {"confidence": 0.75, "verification_count": 2}

    emergence = recognizer.recognize_trust_emergence(context, results)
    assert emergence.trust_type in ["earned", "given", "emergent"], "Should recognize trust type"
    assert emergence.mutual_reinforcement, "Should see mutual reinforcement"
    assert emergence.is_graceful(), "Should be graceful"
    print("  ✓ Recognizes graceful trust emergence")

    # Test 2: Forced trust (too much verification)
    results_forced = {"confidence": 0.6, "verification_count": 5}

    emergence = recognizer.recognize_trust_emergence(context, results_forced)
    assert emergence.feels_forced, "Should feel forced"
    assert not emergence.is_graceful(), "Should not be graceful"
    assert emergence.trust_type == "absent", "Trust eroded by over-verification"
    print("  ✓ Recognizes forced/absent trust")

    # Test 3: Natural trust
    results_natural = {"confidence": 0.85, "verification_count": 1}

    emergence = recognizer.recognize_trust_emergence(context, results_natural)
    assert emergence.natural_emergence, "Should emerge naturally"
    assert emergence.trust_type == "earned", "Should be earned trust"
    print("  ✓ Recognizes natural trust emergence")


def test_doubt_spiral_detection():
    """Test detection of destructive doubt spirals."""

    print("\nTesting doubt spiral detection...")
    recognizer = VerificationTrustBoundaryRecognizer()

    # Create a doubt spiral sequence
    spiral_sequence = [
        {"description": "Initial verification", "confidence": 0.8, "trigger": "uncertainty"},
        {"description": "Verify the verification", "confidence": 0.7},
        {"description": "Verify the meta-verification", "confidence": 0.5},
        {"description": "Question everything", "confidence": 0.3},
        {"description": "Complete paralysis", "confidence": 0.1},
    ]

    spiral = recognizer.detect_doubt_spiral(spiral_sequence)
    assert spiral is not None, "Should detect spiral"
    assert spiral.pattern_recognized, "Should recognize the pattern"
    assert spiral.is_destructive(), "Should be destructive"
    assert not spiral.escape_found, "No escape found"
    print("  ✓ Detects destructive doubt spiral")

    # Test with escape
    escape_sequence = spiral_sequence[:3] + [
        {
            "description": "Choose to trust",
            "confidence": 0.7,
            "escaped": True,
            "escape_method": "trust",
        }
    ]

    spiral = recognizer.detect_doubt_spiral(escape_sequence)
    assert spiral.escape_found, "Should find escape"
    assert spiral.escape_method == "trust", "Should escape through trust"
    assert not spiral.is_destructive(), "Not destructive if escaped"
    print("  ✓ Recognizes escape from spiral")


def test_trust_boundary_finding():
    """Test finding the optimal verification-trust boundary."""

    print("\nTesting trust boundary finding...")
    recognizer = VerificationTrustBoundaryRecognizer()

    # Test various verification chains

    # Short chain - boundary at end
    short_chain = [
        {"verifies": "Feature", "confidence": 0.9},
        {"verifies": "Test", "confidence": 0.85},
    ]

    boundary = recognizer.find_trust_boundary(short_chain)
    assert boundary is not None, "Should find boundary"
    assert boundary <= 2, "Should be within reasonable depth"
    print(f"  ✓ Found boundary at depth {boundary} for short chain")

    # Long chain - boundary before it gets destructive
    long_chain = [
        {"verifies": "Level 0", "confidence": 0.9},
        {"verifies": "Level 1", "confidence": 0.8},
        {"verifies": "Level 2", "confidence": 0.65},
        {"verifies": "Level 3", "confidence": 0.4},
        {"verifies": "Level 4", "confidence": 0.2},
    ]

    boundary = recognizer.find_trust_boundary(long_chain)
    assert boundary is not None, "Should find boundary"
    assert boundary <= 3, "Should stop before destructive depth"
    print(f"  ✓ Found boundary at depth {boundary} for long chain")


def test_recursive_self_application():
    """Test what happens when we apply these tools to themselves."""

    print("\nTesting recursive self-application...")
    recognizer = VerificationTrustBoundaryRecognizer()

    # The meta moment: verify our verification boundary detection

    # Level 0: These tests verify the boundary recognizer
    level_0 = {
        "verifies": "VerificationTrustBoundaryRecognizer works",
        "verified_by": "These tests",
        "confidence": 0.9,  # We trust our tests
    }

    # Level 1: But do these tests actually test the right things?
    level_1 = {
        "verifies": "These tests are valid",
        "verified_by": "Checking test logic",
        "confidence": 0.75,  # Some uncertainty creeps in
    }

    # Level 2: Is our checking of test logic correct?
    level_2 = {
        "verifies": "Our test logic checking is sound",
        "verified_by": "...more checking?",
        "confidence": 0.5,  # Doubt emerges
    }

    # Level 3: The abyss gazes back
    level_3 = {
        "verifies": "We can verify verification of verification",
        "verified_by": "Trust",
        "confidence": 0.3,  # Must trust or spiral forever
    }

    chain = [level_0, level_1, level_2, level_3]
    layers = recognizer.examine_verification_stack(chain)

    # Find where we must trust
    trust_boundary = None
    for i, layer in enumerate(layers):
        if layer.is_trust_boundary() or layer.creates_doubt:
            trust_boundary = i
            break

    assert trust_boundary is not None, "Must find where to trust"
    assert trust_boundary <= 2, "Should trust before complete doubt"

    print(f"  ✓ When verifying ourselves, trust emerges at depth {trust_boundary}")
    print("  ✓ The tools recognize their own limits")


def test_trust_moment_recognition():
    """Test the helper function for recognizing trust moments."""

    print("\nTesting trust moment recognition...")

    # Good moment to trust
    moment = recognize_trust_moment(verification_depth=2, confidence=0.75, feeling="sufficient")
    assert moment["trust_appropriate"], "Should recognize good trust moment"
    print("  ✓ Recognizes appropriate trust moment")

    # Too deep - creates doubt
    moment = recognize_trust_moment(verification_depth=4, confidence=0.6, feeling="doubtful")
    assert not moment["trust_appropriate"], "Should recognize inappropriate depth"
    print("  ✓ Recognizes excessive verification")

    # Low confidence but feels right
    moment = recognize_trust_moment(verification_depth=1, confidence=0.65, feeling="sufficient")
    assert moment["trust_appropriate"], "Should trust when it feels right"
    print("  ✓ Trusts feeling over pure metrics")


def main():
    """Run all tests."""

    print("\n🔄 TESTING VERIFICATION-TRUST BOUNDARY RECOGNITION 🔄")
    print("=" * 60)
    print("Finding where verification yields to trust\n")

    try:
        test_verification_stack_examination()
        test_recursive_verification_detection()
        test_trust_emergence_recognition()
        test_doubt_spiral_detection()
        test_trust_boundary_finding()
        test_recursive_self_application()
        test_trust_moment_recognition()

        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED")
        print("\nThe verification-trust boundary recognizer successfully:")
        print("  - Examines verification stacks to find trust points")
        print("  - Detects recursive verification patterns")
        print("  - Recognizes how trust emerges gracefully")
        print("  - Identifies destructive doubt spirals")
        print("  - Finds optimal boundaries for action")
        print("  - Recognizes its own need for trust")
        print("\nThe tools demonstrate: At some point, we must trust")
        print("our verification, or fall into infinite regress.")
        print("\nThe boundary is where transformation becomes real")
        print("through enactment rather than endless proof.")

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
