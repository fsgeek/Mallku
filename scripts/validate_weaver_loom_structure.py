#!/usr/bin/env python3
"""
Validate the Weaver and Loom implementation structure

This script checks that all components are in place without
requiring dependency installation or execution.
"""

import sys
from pathlib import Path


def check_file_exists(path: str, description: str) -> bool:
    """Check if a file exists and report"""
    file_path = Path(path)
    exists = file_path.exists()
    status = "✓" if exists else "✗"
    print(f"{status} {description}: {path}")
    return exists


def main():
    print("Validating Weaver and Loom Implementation Structure")
    print("=" * 60)

    all_good = True

    # Core implementation files
    print("\nCore Implementation:")
    all_good &= check_file_exists("src/mallku/orchestration/loom/__init__.py", "Loom package init")
    all_good &= check_file_exists(
        "src/mallku/orchestration/loom/the_loom.py", "The Loom orchestrator"
    )
    all_good &= check_file_exists(
        "src/mallku/orchestration/weaver/__init__.py", "Weaver package init"
    )
    all_good &= check_file_exists(
        "src/mallku/orchestration/weaver/master_weaver.py", "Master Weaver"
    )
    all_good &= check_file_exists(
        "src/mallku/orchestration/weaver/apprentice_template.py", "Apprentice template"
    )

    # MCP tools
    print("\nMCP Tools:")
    all_good &= check_file_exists("src/mallku/mcp/__init__.py", "MCP package init")
    all_good &= check_file_exists("src/mallku/mcp/tools/__init__.py", "MCP tools init")
    all_good &= check_file_exists("src/mallku/mcp/tools/loom_tools.py", "Loom MCP tools")

    # Documentation
    print("\nDocumentation:")
    all_good &= check_file_exists(
        "docs/architecture/weaver_and_loom/technical_design.md", "Technical design"
    )
    all_good &= check_file_exists(
        "docs/architecture/weaver_and_loom/khipu_thread_format.md", "Khipu format spec"
    )
    all_good &= check_file_exists(
        "docs/architecture/weaver_and_loom/integration_guide.md", "Integration guide"
    )
    all_good &= check_file_exists(
        "docs/architecture/weaver_and_loom/IMPLEMENTATION_COMPLETE.md", "Implementation summary"
    )

    # Demonstration
    print("\nDemonstration:")
    all_good &= check_file_exists("demonstrate_weaver_loom.py", "Demonstration script")

    # Check for key classes/functions
    print("\nValidating key components exist in code:")

    try:
        with open("src/mallku/orchestration/loom/the_loom.py") as f:
            loom_content = f.read()
            components = ["class TheLoom", "class LoomSession", "class TaskStatus"]
            for component in components:
                if component in loom_content:
                    print(f"✓ Found {component} in the_loom.py")
                else:
                    print(f"✗ Missing {component} in the_loom.py")
                    all_good = False
    except Exception as e:
        print(f"✗ Error reading the_loom.py: {e}")
        all_good = False

    # Summary
    print("\n" + "=" * 60)
    if all_good:
        print("✓ All Weaver and Loom components are in place!")
        print("\nThe implementation is structurally complete.")
        print("Next steps:")
        print("1. Install dependencies: aiofiles, filelock, pyyaml")
        print("2. Connect real MCP infrastructure for spawning instances")
        print("3. Test with actual Mallku tasks")
    else:
        print("✗ Some components are missing!")
        sys.exit(1)


if __name__ == "__main__":
    main()
