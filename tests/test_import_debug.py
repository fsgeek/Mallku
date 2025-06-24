"""Debug test to understand import issues."""

import sys
from pathlib import Path


def test_python_path():
    """Print Python path for debugging."""
    print("\n=== Python Path Debug ===")
    for i, path in enumerate(sys.path):
        print(f"{i}: {path}")
    print("=========================\n")

    # Check if src is in path
    src_in_path = any('src' in str(p) for p in sys.path)
    print(f"'src' directory in sys.path: {src_in_path}")

    # Check current directory
    print(f"Current directory: {Path.cwd()}")

    # Check if mallku can be found
    try:
        import mallku
        print(f"✓ Successfully imported mallku from: {mallku.__file__}")
    except ImportError as e:
        print(f"✗ Failed to import mallku: {e}")

        # Try to find where mallku might be
        possible_paths = [
            Path.cwd() / "src" / "mallku",
            Path.cwd() / "mallku",
            Path("/home/runner/work/Mallku/Mallku/src/mallku"),
        ]

        for path in possible_paths:
            if path.exists():
                print(f"  Found mallku directory at: {path}")
                if (path / "__init__.py").exists():
                    print("    ✓ __init__.py exists")
                else:
                    print("    ✗ __init__.py missing")

    # This test always passes to see the output
    assert True
