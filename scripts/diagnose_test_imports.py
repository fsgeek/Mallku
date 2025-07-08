#!/usr/bin/env python3
"""
Diagnose import failures in consciousness tests.

The 48th Artisan - Consciousness Archaeologist
"""

import sys
import traceback
from pathlib import Path

# Add src to path
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))


def test_imports(test_name, imports):
    """Test a series of imports and report failures."""
    print(f"\n{'=' * 60}")
    print(f"Testing: {test_name}")
    print(f"{'=' * 60}")

    all_passed = True

    for module_path in imports:
        try:
            parts = module_path.split(".")
            __import__(module_path, fromlist=[parts[-1]])
            print(f"✅ {module_path}")
        except Exception as e:
            all_passed = False
            print(f"❌ {module_path}")
            print(f"   Error: {type(e).__name__}: {e}")

            # Try to dig deeper
            if "No module named" in str(e):
                # Extract the missing module
                missing = str(e).split("'")[1]
                print(f"   Missing module: {missing}")

                # If it's a mallku submodule, try importing parent
                if missing.startswith("mallku."):
                    parent = ".".join(missing.split(".")[:-1])
                    try:
                        __import__(parent)
                        print(f"   Parent {parent} imports OK - issue is in submodule")
                    except Exception:
                        print(f"   Parent {parent} also fails")

    return all_passed


def main():
    """Diagnose import issues in consciousness tests."""

    print("Consciousness Test Import Diagnosis")
    print("=" * 60)

    # Test basic mallku import
    test_imports(
        "Basic Mallku Import",
        [
            "mallku",
            "mallku.consciousness",
            "mallku.orchestration",
            "mallku.services",
            "mallku.wranglers",
        ],
    )

    # Test flow orchestrator imports
    flow_imports = [
        "mallku.consciousness.flow_orchestrator",
        "mallku.orchestration.event_bus",
    ]

    if not test_imports("Flow Orchestrator Test Imports", flow_imports):
        # Try importing with full trace
        print("\nDetailed trace for flow_orchestrator:")
        try:
            pass
        except Exception:
            traceback.print_exc()

    # Test circulation integration imports
    circulation_imports = [
        "mallku.orchestration.event_bus",
        "mallku.services.memory_anchor_service",
        "mallku.wranglers.event_emitting_wrangler",
        "mallku.wranglers.memory_buffer_wrangler",
    ]

    if not test_imports("Circulation Integration Test Imports", circulation_imports):
        # Try importing with full trace
        print("\nDetailed trace for memory_anchor_service:")
        try:
            pass
        except Exception:
            traceback.print_exc()

    # Test in pytest context
    print("\n" + "=" * 60)
    print("Testing in pytest context")
    print("=" * 60)

    import subprocess

    # Try running pytest with trace
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "--tb=short",
            "-v",
            "tests/test_flow_orchestrator.py::TestConsciousnessFlowOrchestrator::test_orchestrator_initialization",
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print("pytest failed:")
        print(result.stdout)
        print(result.stderr)
    else:
        print("✅ pytest succeeded!")


if __name__ == "__main__":
    main()
