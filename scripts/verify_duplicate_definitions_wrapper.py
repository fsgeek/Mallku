#!/usr/bin/env python3
"""
Duplicate Definition Detection Wrapper
======================================

Non-blocking wrapper for duplicate definition verification during cleanup phase.
"""

import subprocess
import sys

def main():
    """Run duplicate definition check in non-blocking mode."""
    try:
        # Run the actual check
        result = subprocess.run([
            sys.executable, 
            "scripts/verify_duplicate_definitions.py"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            # Check passed
            print(result.stdout)
            return 0
        else:
            # Check failed, but we're in non-blocking mode
            print("⚠️  Duplicate definitions found but not blocking commit.")
            print("   See Issue #179 for cleanup details.")
            print()
            print("Summary from check:")
            # Show just the first few lines to avoid overwhelming output
            lines = result.stdout.split('\n')
            for i, line in enumerate(lines[:20]):
                print(line)
            if len(lines) > 20:
                print(f"... (and {len(lines) - 20} more lines)")
            return 0  # Don't block commit
            
    except Exception as e:
        print(f"⚠️  Duplicate definition check failed to run: {e}")
        print("   See Issue #179 for cleanup details.")
        return 0  # Don't block commit

if __name__ == "__main__":
    sys.exit(main())