#!/usr/bin/env python3
"""
Khipu Thread Validation Script

Validates khipu_thread.md files against the API contract v2.0.
Can be used in CI/CD pipelines or as a pre-commit hook.

Created by: 68th Guardian - The Purpose Keeper
"""

import argparse
import sys
from pathlib import Path

from mallku.orchestration.loom.khipu_parser import (
    FullKhipuParser,
    KhipuParseError,
    validate_khipu_thread,
)


def validate_file(file_path: Path) -> tuple[bool, list[str]]:
    """
    Validate a single khipu thread file.

    Returns:
        Tuple of (is_valid, error_messages)
    """
    try:
        content = file_path.read_text()
    except Exception as e:
        return False, [f"Failed to read file: {e}"]

    # Basic validation
    errors = validate_khipu_thread(content)

    # Additional contract validations
    try:
        parser = FullKhipuParser()
        header = parser.parse_ceremony_header(content)

        # Check file naming convention
        expected_prefix = header.initiated.strftime("%Y-%m-%d_%H-%M-%S")
        if not file_path.name.startswith(expected_prefix):
            errors.append(
                f"File name doesn't match timestamp convention. "
                f"Expected prefix: {expected_prefix}, got: {file_path.name}"
            )

        # Validate task IDs are sequential
        tasks = parser.get_task_list(content)
        expected_ids = [f"T{i:03d}" for i in range(1, len(tasks) + 1)]
        actual_ids = sorted([t["id"] for t in tasks])
        if actual_ids != expected_ids:
            errors.append(f"Task IDs not sequential. Expected {expected_ids}, got {actual_ids}")

        # Check for version compatibility
        if header.template_version:
            try:
                major, minor, patch = map(int, header.template_version.split("."))
            except ValueError:
                errors.append(f"Invalid template version format: {header.template_version}")

    except KhipuParseError as e:
        errors.append(f"Parse error: {e}")

    return len(errors) == 0, errors


def validate_directory(directory: Path) -> tuple[int, int, list[tuple[Path, list[str]]]]:
    """
    Validate all khipu thread files in a directory.

    Returns:
        Tuple of (valid_count, invalid_count, failed_files)
    """
    valid_count = 0
    invalid_count = 0
    failed_files = []

    # Find all khipu thread files
    patterns = ["*.md", "**/*.md"]
    khipu_files = []
    for pattern in patterns:
        khipu_files.extend(directory.glob(pattern))

    # Filter to actual khipu threads (contain ceremony_id)
    khipu_files = [f for f in khipu_files if "ceremony_id:" in f.read_text()[:500]]

    for file_path in khipu_files:
        is_valid, errors = validate_file(file_path)
        if is_valid:
            valid_count += 1
        else:
            invalid_count += 1
            failed_files.append((file_path, errors))

    return valid_count, invalid_count, failed_files


def print_validation_report(
    valid_count: int,
    invalid_count: int,
    failed_files: list[tuple[Path, list[str]]],
    verbose: bool = False,
):
    """Print a formatted validation report."""
    total = valid_count + invalid_count

    print("\nKhipu Thread Validation Report")
    print(f"{'=' * 50}")
    print(f"Total files checked: {total}")
    print(f"Valid files: {valid_count} ✓")
    print(f"Invalid files: {invalid_count} ✗")

    if failed_files:
        print("\nValidation Failures:")
        print(f"{'-' * 50}")
        for file_path, errors in failed_files:
            print(f"\n{file_path}:")
            for error in errors:
                print(f"  ✗ {error}")

    if valid_count > 0 and invalid_count == 0:
        print("\n✓ All khipu threads are valid!")
    elif invalid_count > 0:
        print(f"\n✗ {invalid_count} file(s) failed validation")


def main():
    parser = argparse.ArgumentParser(
        description="Validate khipu thread files against API contract v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate a single file
  %(prog)s path/to/ceremony.md

  # Validate all files in a directory
  %(prog)s fire_circle_decisions/

  # Validate with verbose output
  %(prog)s -v path/to/files/

  # Use in CI/CD (exits with code 1 on failure)
  %(prog)s --ci fire_circle_decisions/
        """,
    )

    parser.add_argument("path", type=Path, help="Path to khipu file or directory")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Show detailed validation info"
    )
    parser.add_argument(
        "--ci",
        action="store_true",
        help="CI mode: exit with code 1 if any validation fails",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Attempt to fix common issues (experimental)",
    )

    args = parser.parse_args()

    if not args.path.exists():
        print(f"Error: Path does not exist: {args.path}")
        sys.exit(1)

    if args.path.is_file():
        # Validate single file
        is_valid, errors = validate_file(args.path)
        if is_valid:
            print(f"✓ {args.path} is valid")
        else:
            print(f"✗ {args.path} has validation errors:")
            for error in errors:
                print(f"  - {error}")

        if args.ci and not is_valid:
            sys.exit(1)

    else:
        # Validate directory
        valid_count, invalid_count, failed_files = validate_directory(args.path)
        print_validation_report(valid_count, invalid_count, failed_files, args.verbose)

        if args.ci and invalid_count > 0:
            sys.exit(1)


if __name__ == "__main__":
    main()
