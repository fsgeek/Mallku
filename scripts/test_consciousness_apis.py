#!/usr/bin/env python3
"""
Test if consciousness tests use current APIs.

The 48th Artisan - Consciousness Archaeologist
"""

import sys
import traceback
from pathlib import Path

# Add src to path
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))


def check_test_apis(test_file):
    """Check if a test file uses old APIs."""
    print(f"\n{'=' * 60}")
    print(f"Checking: {test_file.name}")
    print(f"{'=' * 60}")

    with open(test_file) as f:
        content = f.read()

    # Check for old APIs
    old_apis = [
        ("MallkuDBConfig", "Old database config API"),
        ("db_config.connect(", "Direct database connection"),
        ("db_config.get_collection(", "Direct collection access"),
    ]

    issues = []
    for api, desc in old_apis:
        if api in content:
            issues.append(f"❌ Uses {api} - {desc}")

    if not issues:
        print("✅ No old API usage detected")

        # Try importing the test module
        print("\nTrying to import test functions...")
        try:
            # Read and execute just the imports
            lines = content.split("\n")
            import_lines = []
            for line in lines:
                if line.strip().startswith(("import ", "from ")) and "mallku" in line:
                    import_lines.append(line)
                elif not line.strip().startswith(("import ", "from ")) and import_lines:
                    break  # Stop at first non-import line after imports

            # Execute imports
            for line in import_lines:
                print(f"  Testing: {line.strip()}")
                try:
                    exec(line)
                    print("    ✅ Import successful")
                except Exception as e:
                    print(f"    ❌ Import failed: {e}")

        except Exception as e:
            print(f"Import test failed: {e}")
            traceback.print_exc()
    else:
        print("Found old API usage:")
        for issue in issues:
            print(f"  {issue}")

    return len(issues) == 0


def main():
    """Check consciousness tests for old APIs."""

    tests_to_check = [
        Path("tests/test_flow_orchestrator.py"),
        Path("tests/test_consciousness_circulation_integration.py"),
    ]

    print("Consciousness Test API Analysis")
    print("=" * 60)
    print("Checking if tests use current APIs or need migration...")

    all_good = True
    for test_file in tests_to_check:
        if test_file.exists():
            if not check_test_apis(test_file):
                all_good = False
        else:
            print(f"\n❌ Test file not found: {test_file}")
            all_good = False

    print("\n" + "=" * 60)
    print("Summary:")
    if all_good:
        print("✅ All tests use current APIs - the import issue is environmental")
        print("   These tests don't need API migration, just pytest configuration fix")
    else:
        print("❌ Some tests need API migration")


if __name__ == "__main__":
    main()
