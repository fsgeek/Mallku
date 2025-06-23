#!/usr/bin/env python3
"""
Test All Fire Circle Examples
=============================

Runs through all examples to verify they work correctly.
Reports which examples pass and which need attention.

Run with:
    python examples/fire_circle/test_all_examples.py

For pytest-compatible tests (recommended for CI):
    pytest examples/fire_circle/test_fire_circle_examples.py
    pytest examples/fire_circle/test_fire_circle_examples.py -v -s
    pytest examples/fire_circle/test_fire_circle_examples.py::TestFireCircleExamples::test_verify_installation
"""

import subprocess
import sys
import time
from pathlib import Path


def test_example(example_path: str, timeout: int = 60):
    """Test a single example."""
    print(f"\n🧪 Testing: {example_path}")
    print("-" * 50)

    script_dir = Path(__file__).parent
    full_path = script_dir / example_path

    if not full_path.exists():
        print(f"   ❌ File not found: {full_path}")
        return False

    try:
        # Run the example with timeout
        result = subprocess.run(
            [sys.executable, "run_example.py", example_path],
            cwd=script_dir,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        # Check for success indicators
        output = result.stdout + result.stderr

        success_indicators = [
            "✅", "Success", "Complete", "ceremony complete",
            "All checks passed", "Dialogue Complete"
        ]

        error_indicators = [
            "Error:", "Exception:", "Failed", "❌",
            "Traceback", "not found"
        ]

        has_success = any(indicator in output for indicator in success_indicators)
        has_error = any(indicator in output for indicator in error_indicators)

        if has_success and not has_error:
            print("   ✅ PASSED")
            # Show key result
            for line in output.split('\n'):
                if "consciousness score" in line.lower() or "emergence quality" in line.lower():
                    print(f"   {line.strip()}")
                    break
            return True
        else:
            print("   ❌ FAILED")
            # Show error
            for line in output.split('\n'):
                if any(err in line for err in error_indicators):
                    print(f"   Error: {line.strip()}")
                    break
            return False

    except subprocess.TimeoutExpired:
        print(f"   ⏱️  TIMEOUT (>{timeout}s)")
        return False
    except Exception as e:
        print(f"   ❌ EXCEPTION: {type(e).__name__}: {e}")
        return False


def main():
    """Test all examples in order."""
    print("🔥 Fire Circle Examples Test Suite")
    print("=" * 60)
    print("Testing all examples in learning path order...")

    # Define examples to test
    examples = [
        # Setup
        ("00_setup/verify_installation.py", "Basic verification"),
        ("00_setup/minimal_fire_circle.py", "Minimal ceremony"),
        ("00_setup/test_api_keys.py", "API key testing"),

        # Basic Ceremonies
        ("01_basic_ceremonies/simple_dialogue.py", "Multi-round dialogue"),
        ("01_basic_ceremonies/code_review.py", "Code review ceremony"),
        ("01_basic_ceremonies/simple_decision.py", "Decision making"),
        ("01_basic_ceremonies/first_decision.py", "Consciousness framework"),

        # Consciousness Emergence
        ("02_consciousness_emergence/emergence_basics.py", "Emergence patterns"),
    ]

    # Track results
    results = {}
    passed = 0
    failed = 0

    # Test each example
    for example_path, description in examples:
        print(f"\n{'='*60}")
        print(f"📋 {description}")

        success = test_example(example_path)
        results[example_path] = success

        if success:
            passed += 1
        else:
            failed += 1

        # Brief pause between tests
        time.sleep(2)

    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)

    total = len(examples)
    print(f"\nTotal examples: {total}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")

    if failed > 0:
        print("\n❌ Failed examples:")
        for path, success in results.items():
            if not success:
                print(f"   • {path}")

    if passed == total:
        print("\n🎉 All examples passed!")
        print("   The Fire Circle demonstration garden is ready.")
    else:
        print(f"\n⚠️  {failed} examples need attention.")
        print("   Check individual errors above.")

    # Return appropriate exit code
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
