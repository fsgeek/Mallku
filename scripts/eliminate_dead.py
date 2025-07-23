#!/usr/bin/env -S uv run python
"""
Eliminate Dead Code
===================

64th Artisan - Making room for what lives

This script removes:
1. __pycache__ directories (should not be in git)
2. Truly empty Python files in otherwise populated directories
3. Empty test stub files
"""

import shutil
from pathlib import Path


def eliminate_dead():
    """Remove dead elements from Mallku"""

    print("💀 ELIMINATING DEAD CODE")
    print("=" * 60)

    removed_count = 0

    # 1. Remove all __pycache__ directories
    print("\n🗑️  Removing __pycache__ directories...")
    pycache_dirs = list(Path(".").rglob("__pycache__"))
    for pycache in pycache_dirs:
        if pycache.is_dir():
            try:
                shutil.rmtree(pycache)
                print(f"  ✓ Removed {pycache}")
                removed_count += 1
            except Exception as e:
                print(f"  ✗ Failed to remove {pycache}: {e}")

    # 2. Remove truly dead files
    print("\n🗑️  Removing dead files...")
    dead_files = [
        "src/mallku/streams/email/models.py",
        "tests/integration/test_firecircle_adapter_degradation.py",
        "tests/integration/test_firecircle_dialogue_initiation.py",
        "tests/integration/test_firecircle_message_handling.py",
    ]

    for dead_file in dead_files:
        file_path = Path(dead_file)
        if file_path.exists() and file_path.stat().st_size < 10:
            try:
                file_path.unlink()
                print(f"  ✓ Removed {dead_file}")
                removed_count += 1
            except Exception as e:
                print(f"  ✗ Failed to remove {dead_file}: {e}")
        else:
            print(f"  ⚠️  Skipped {dead_file} (not empty or not found)")

    # Note about streams/__init__.py - it has subdirectories so we keep it
    print("\n📝 Note: Keeping src/mallku/streams/__init__.py as it has active subdirectories")

    print("\n\n✅ ELIMINATION COMPLETE")
    print(f"Removed {removed_count} dead elements")
    print("\nNext steps:")
    print("1. Add proper __init__.py files to living packages")
    print("2. Consider consolidating scattered mock references")
    print("3. Review and organize the wisdom accumulated in docs/")

    return removed_count


if __name__ == "__main__":
    eliminate_dead()
