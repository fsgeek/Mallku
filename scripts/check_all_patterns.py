#!/usr/bin/env python3
"""Run all Artisan memory pattern checks."""

import subprocess
import sys

scripts = [
    "ensure_dev_environment.py",
    "verify_fire_circle_setup.py",
    "verify_ci_cd_patterns.py",
    "verify_database_security.py",
    "verify_duplicate_definitions.py",
    "verify_github_actions.py",
]

print("🧠 Running All Memory Pattern Checks")
print("=" * 60)

for script in scripts:
    print(f"\n▶️  Running {script}...")
    print("-" * 40)
    try:
        subprocess.run([sys.executable, f"scripts/{script}"], check=True)
    except subprocess.CalledProcessError:
        print(f"⚠️  {script} reported issues")
    except FileNotFoundError:
        print(f"❌ {script} not found")

print("\n✅ Memory pattern checks complete!")
