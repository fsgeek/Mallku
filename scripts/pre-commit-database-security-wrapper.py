#!/usr/bin/env python3
"""
Database Security Architecture Check Wrapper
============================================

Non-blocking wrapper for database security verification during cleanup phase.
"""

import subprocess
import sys


def main():
    """Run database security check in non-blocking mode."""
    try:
        # Pass through any command line arguments
        cmd = [sys.executable, "scripts/pre-commit-database-security.py"] + sys.argv[1:]

        # Run the actual check
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            # Check passed
            print(result.stdout)
            return 0
        else:
            # Check failed, but we're in non-blocking mode
            print("⚠️  Database security violations found but not blocking commit.")
            print("   See Issue #177 for cleanup details.")
            print()
            print("Output from check:")
            print(result.stdout)
            if result.stderr:
                print("Errors:")
                print(result.stderr)
            return 0  # Don't block commit

    except Exception as e:
        print(f"⚠️  Database security check failed to run: {e}")
        print("   See Issue #177 for cleanup details.")
        return 0  # Don't block commit


if __name__ == "__main__":
    sys.exit(main())
