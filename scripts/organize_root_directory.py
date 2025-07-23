#!/usr/bin/env -S uv run python
"""
Organize Root Directory - Move files to proper locations
========================================================

63rd Artisan - Creating order from chaos
"""

import shutil
from pathlib import Path


def organize_root_directory(dry_run=True):
    """Move Python files from root to appropriate directories"""

    root_path = Path(".")
    moves = []

    print("🧹 Organizing Root Directory")
    print("=" * 60)
    print(f"Mode: {'DRY RUN' if dry_run else 'ACTUAL MOVE'}")
    print()

    # Get all Python files in root only
    root_files = [f for f in root_path.glob("*.py") if f.is_file()]

    for py_file in sorted(root_files):
        filename = py_file.name

        # Determine destination
        if filename.startswith("test_") or filename.endswith("_test.py"):
            # Test files go to tests/
            dest_dir = Path("tests")
            dest_file = dest_dir / filename

        elif filename in ["setup.py", "conftest.py"]:
            # Keep these in root (they belong there)
            continue

        else:
            # Everything else appears to be a script
            dest_dir = Path("scripts")
            dest_file = dest_dir / filename

        moves.append((py_file, dest_file))

    # Execute moves
    print(f"Planning to move {len(moves)} files:\n")

    tests_count = 0
    scripts_count = 0

    for src, dest in moves:
        dest_type = "tests" if "tests" in str(dest) else "scripts"

        if dest_type == "tests":
            tests_count += 1
        else:
            scripts_count += 1

        if dry_run:
            print(f"  {src.name} -> {dest}")
        else:
            # Ensure destination directory exists
            dest.parent.mkdir(exist_ok=True)

            # Check if destination already exists
            if dest.exists():
                print(f"  ⚠️  {src.name} -> {dest} (destination exists, skipping)")
            else:
                shutil.move(str(src), str(dest))
                print(f"  ✓ {src.name} -> {dest}")

    # Summary
    print("\n📊 Summary:")
    print(f"  Tests to move: {tests_count}")
    print(f"  Scripts to move: {scripts_count}")
    print(f"  Total: {len(moves)}")

    if dry_run:
        print("\n💡 This was a dry run. To actually move files, run with --execute")
        print("   python scripts/organize_root_directory.py --execute")
    else:
        print("\n✅ Root directory organized!")

        # Count remaining files
        remaining = len([f for f in root_path.glob("*.py") if f.is_file()])
        print(f"   Python files remaining in root: {remaining}")


if __name__ == "__main__":
    import sys

    execute = "--execute" in sys.argv
    organize_root_directory(dry_run=not execute)
