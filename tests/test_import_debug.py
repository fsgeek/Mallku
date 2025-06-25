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
    src_paths = [p for p in sys.path if "src" in str(p)]
    print(f"'src' directories in sys.path: {src_paths}")

    # Check current directory
    print(f"Current directory: {Path.cwd()}")

    # Check if mallku can be found
    try:
        import mallku

        print(f"✓ Successfully imported mallku from: {mallku.__file__}")
    except ImportError as e:
        print(f"✗ Failed to import mallku: {e}")

        # Try to import manually
        src_dir = Path("/home/runner/work/Mallku/Mallku/src")
        if src_dir.exists():
            print(f"\nTrying manual import with src_dir: {src_dir}")
            sys.path.insert(0, str(src_dir))
            print(f"sys.path after manual insert: {sys.path[:3]}")

            try:
                import mallku

                print(f"✓ Manual import succeeded! mallku from: {mallku.__file__}")
            except ImportError as e2:
                print(f"✗ Manual import also failed: {e2}")

                # Check if it's a sub-import issue
                mallku_init = src_dir / "mallku" / "__init__.py"
                if mallku_init.exists():
                    print(f"\n✓ {mallku_init} exists")
                    print("Checking if mallku has import errors...")

                    # Try to read the __init__.py
                    try:
                        content = mallku_init.read_text()
                        print(f"mallku/__init__.py content: {content[:100]}...")
                    except Exception as read_err:
                        print(f"Error reading __init__.py: {read_err}")

    # This test always passes to see the output
    assert True
