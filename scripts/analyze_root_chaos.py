#!/usr/bin/env -S uv run python
"""
Analyze Root Directory Chaos
============================

63rd Artisan - Understanding the 99 Python files in root
"""

import ast
from collections import defaultdict
from pathlib import Path


def analyze_root_files():
    """Analyze and categorize the 99 Python files in root directory"""

    root_path = Path(".")
    categories = defaultdict(list)

    print("🔍 Analyzing Root Directory Python Files")
    print("=" * 60)

    # Get all Python files in root only (not subdirectories)
    root_files = [f for f in root_path.glob("*.py") if f.is_file()]

    print(f"Found {len(root_files)} Python files in root directory\n")

    for py_file in sorted(root_files):
        try:
            content = py_file.read_text()

            # Quick categorization based on name and content
            filename = py_file.name

            # Setup/Config files
            if filename in ["setup.py", "conftest.py", "pyproject.toml"]:
                categories["setup/config"].append(filename)

            # Test files that shouldn't be in root
            elif filename.startswith("test_") or filename.endswith("_test.py"):
                categories["misplaced_tests"].append(filename)

            # Scripts that might belong in scripts/
            elif 'if __name__ == "__main__"' in content:
                categories["executable_scripts"].append(filename)

            # Temporary or experimental files
            elif any(x in filename.lower() for x in ["temp", "tmp", "experiment", "draft"]):
                categories["temporary"].append(filename)

            # Check if it's a proper module
            else:
                try:
                    tree = ast.parse(content)
                    has_classes = any(isinstance(node, ast.ClassDef) for node in ast.walk(tree))
                    has_functions = any(
                        isinstance(node, ast.FunctionDef) for node in ast.walk(tree)
                    )

                    if has_classes or has_functions:
                        # Check imports to guess purpose
                        imports = [
                            node
                            for node in ast.walk(tree)
                            if isinstance(node, ast.Import | ast.ImportFrom)
                        ]

                        if any("mallku" in str(getattr(imp, "module", "")) for imp in imports):
                            categories["mallku_modules"].append(filename)
                        else:
                            categories["utility_modules"].append(filename)
                    else:
                        categories["data_or_config"].append(filename)

                except SyntaxError:
                    categories["broken_syntax"].append(filename)

        except Exception as e:
            categories["read_errors"].append(f"{filename}: {str(e)}")

    # Print categorization
    for category, files in sorted(categories.items()):
        if files:
            print(f"\n### {category.replace('_', ' ').title()} ({len(files)} files)")
            for f in sorted(files)[:10]:  # Show first 10
                print(f"  - {f}")
            if len(files) > 10:
                print(f"  ... and {len(files) - 10} more")

    # Recommendations
    print("\n\n📋 RECOMMENDATIONS")
    print("=" * 60)

    if categories["misplaced_tests"]:
        print(f"\n1. Move {len(categories['misplaced_tests'])} test files to tests/")

    if categories["executable_scripts"]:
        print(f"\n2. Move {len(categories['executable_scripts'])} executable scripts to scripts/")

    if categories["temporary"]:
        print(f"\n3. Review and remove {len(categories['temporary'])} temporary files")

    if categories["mallku_modules"]:
        print(f"\n4. Organize {len(categories['mallku_modules'])} Mallku modules into src/mallku/")

    if categories["broken_syntax"]:
        print(f"\n5. Fix or remove {len(categories['broken_syntax'])} files with syntax errors")

    # Calculate potential reduction
    removable = len(categories["temporary"] + categories["broken_syntax"])
    movable = len(
        categories["misplaced_tests"]
        + categories["executable_scripts"]
        + categories["mallku_modules"]
    )

    print("\n\n🎯 IMPACT ANALYSIS")
    print(f"Files that can be removed: {removable}")
    print(f"Files that can be moved: {movable}")
    print(f"Root directory after cleanup: {len(root_files) - removable - movable} files")
    print(f"Context scan reduction: {((removable + movable) / len(root_files)) * 100:.1f}%")


if __name__ == "__main__":
    analyze_root_files()
