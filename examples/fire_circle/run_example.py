#!/usr/bin/env python3
"""
Fire Circle Example Runner
==========================

Helper script to run Fire Circle examples with correct Python path setup.

Usage:
    python examples/fire_circle/run_example.py <example_path>

Example:
    python examples/fire_circle/run_example.py 00_setup/verify_installation.py
"""

import os
import subprocess
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: python examples/fire_circle/run_example.py <example_path>")
        print("\nExample:")
        print("  python examples/fire_circle/run_example.py 00_setup/verify_installation.py")
        sys.exit(1)

    # Get the example to run
    example_path = sys.argv[1]

    # Get paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    src_path = project_root / "src"

    # Construct full path to example
    if not example_path.startswith(str(script_dir)):
        example_full_path = script_dir / example_path
    else:
        example_full_path = Path(example_path)

    if not example_full_path.exists():
        print(f"Error: Example not found: {example_full_path}")
        sys.exit(1)

    # Set up environment
    env = os.environ.copy()
    env["PYTHONPATH"] = str(src_path)

    # Run the example
    print(f"🔥 Running Fire Circle example: {example_path}")
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, str(example_full_path)] + sys.argv[2:],
        env=env
    )

    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
