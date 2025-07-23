#!/usr/bin/env -S uv run python
"""
Run CI/CD Tests with Simple Test Apprentice
===========================================

62nd Artisan - A real CI/CD testing solution

This script uses the Simple Test Apprentice to run the same tests
that would run in CI/CD, giving immediate feedback about what would
pass or fail.

No mocks, no simulations - just real test execution.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mallku.testing.simple_test_apprentice import SimpleTestApprentice


async def run_ci_tests():
    """Run the core CI/CD test suite"""
    apprentice = SimpleTestApprentice()

    print("🧪 Running CI/CD Test Suite")
    print("=" * 60)

    # 1. Verify core imports
    print("\n📦 Verifying core imports...")
    core_modules = [
        "mallku",
        "mallku.firecircle",
        "mallku.orchestration",
        "mallku.core.database",
    ]

    for module in core_modules:
        result = await apprentice.verify_imports(module)
        status = "✓" if result.passed else "✗"
        print(f"  {status} {module}")

    # 2. Run security verification
    print("\n🔒 Running security checks...")
    security_scripts = [
        "scripts/verify_database_security.py",
        "scripts/check_secure_credentials.py",
    ]

    for script in security_scripts:
        if Path(script).exists():
            result = await apprentice.run_script(script)
            status = "✓" if result.passed else "✗"
            print(f"  {status} {script}")

    # 3. Run unit tests
    print("\n🧪 Running unit tests...")
    test_paths = [
        "tests/test_simple.py",
        "tests/core/test_models.py",
        "tests/firecircle/test_adapter_smoke.py",
    ]

    for test_path in test_paths:
        if Path(test_path).exists():
            result = await apprentice.run_pytest(test_path, verbose=False)
            status = "✓" if result.passed else "✗"
            print(f"  {status} {test_path}")

    # 4. Run linting checks
    print("\n📝 Running linting checks...")
    lint_result = await apprentice.run_script("-m", "ruff", "check", "--statistics")
    if lint_result.passed:
        print("  ✓ Ruff check passed")
    else:
        print("  ✗ Ruff found issues")
        # Show first few lines of output
        lines = lint_result.output.split("\n")[:5]
        for line in lines:
            if line.strip():
                print(f"    {line}")

    # Print summary
    apprentice.print_summary()

    # Save detailed results
    results_path = Path("ci_test_results.json")
    apprentice.save_results(results_path)

    # Return exit code based on results
    failed = sum(1 for r in apprentice.results if not r.passed)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_ci_tests())
    sys.exit(exit_code)
