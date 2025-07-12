#!/usr/bin/env python3
"""
Pre-commit Hook: Database Security Check
========================================

51st Artisan - Architectural Integrity Guardian
Prevents commits that violate database security architecture

This can be integrated into .pre-commit-config.yaml or run standalone.
"""

import sys


def check_file(filepath: str) -> list[str]:
    """Check a file for database security violations."""
    violations = []

    # Skip test files
    if "test" in filepath.lower() or "/tests/" in filepath:
        return violations

    try:
        with open(filepath) as f:
            content = f.read()
            lines = content.splitlines()

        for i, line in enumerate(lines, 1):
            # Skip comments and strings
            if line.strip().startswith("#"):
                continue

            # Check for violations
            if "get_database()" in line and "get_secured_database" not in line:
                violations.append(f"{filepath}:{i}: Direct get_database() call")

            if "ArangoClient" in line and "# security-exception" not in line:
                violations.append(f"{filepath}:{i}: Direct ArangoClient usage")

            if "localhost:8529" in line:
                violations.append(f"{filepath}:{i}: Direct ArangoDB port access")

            if "from" in line and "database import get_database" in line:
                violations.append(f"{filepath}:{i}: Importing insecure get_database")

    except Exception as e:
        print(f"Error checking {filepath}: {e}")

    return violations


def main(files: list[str]) -> int:
    """Check all provided files for violations."""
    all_violations = []

    for filepath in files:
        if filepath.endswith(".py"):
            violations = check_file(filepath)
            all_violations.extend(violations)

    if all_violations:
        print("\n🛡️ Database Security Violations Found!\n")
        for violation in all_violations:
            print(f"  ❌ {violation}")
        print("\n📚 All database access MUST use secure patterns:")
        print("  - get_secured_database() not get_database()")
        print("  - API gateway (port 8080) not direct ArangoDB (port 8529)")
        print("  - No direct ArangoClient instantiation")
        print("\n💡 See Issue #176 for architectural context")
        print("  Add '# security-exception: reason' to override in core modules only\n")
        return 1

    return 0


if __name__ == "__main__":
    # Get files from command line args (pre-commit passes them)
    files = sys.argv[1:] if len(sys.argv) > 1 else []

    if not files:
        print("Usage: pre-commit-database-security.py <files...>")
        sys.exit(0)

    sys.exit(main(files))
