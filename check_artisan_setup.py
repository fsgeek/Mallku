#!/usr/bin/env python3
"""
Check Artisan Setup
===================

44th Artisan - A welcoming setup checker for new arrivals

This script checks common setup issues and provides helpful guidance
rather than cryptic errors. It embodies the welcoming principle.
"""

import json
import sys
from pathlib import Path


class SetupChecker:
    """Checks setup with welcoming guidance."""

    def __init__(self):
        self.issues_found = []
        self.suggestions = []

    def check_all(self):
        """Run all checks."""
        print("\n🔍 Checking Mallku Setup for New Artisans")
        print("=" * 50)

        self.check_python_version()
        self.check_project_structure()
        self.check_api_keys()
        self.check_dependencies()
        self.check_fire_circle()

        self.show_results()

    def check_python_version(self):
        """Check Python version."""
        print("\n📐 Checking Python version...")

        version = sys.version_info
        if version.major == 3 and version.minor >= 10:
            print(f"✅ Python {version.major}.{version.minor} - Good!")
        else:
            self.issues_found.append(f"Python {version.major}.{version.minor} is quite old")
            self.suggestions.append(
                "Consider upgrading to Python 3.10 or newer for best compatibility"
            )

    def check_project_structure(self):
        """Check if we're in the right place."""
        print("\n📁 Checking project structure...")

        expected_files = ["pyproject.toml", "README.md", "src/mallku"]
        current_dir = Path.cwd()

        missing = []
        for expected in expected_files:
            if not (current_dir / expected).exists():
                missing.append(expected)

        if missing:
            self.issues_found.append("Some expected files not found - might be in wrong directory")
            self.suggestions.append(
                f"Make sure you're in the Mallku root directory. Missing: {', '.join(missing)}"
            )
        else:
            print("✅ Project structure looks good!")

    def check_api_keys(self):
        """Check API keys setup."""
        print("\n🔑 Checking API keys...")

        secrets_file = Path(".secrets/api_keys.json")

        if not secrets_file.exists():
            self.issues_found.append("No API keys file found")
            self.suggestions.append(
                "Create .secrets/api_keys.json with at least 2 API keys:\n"
                '  {"ANTHROPIC_API_KEY": "sk-ant-...", "OPENAI_API_KEY": "sk-..."}'
            )
            return

        try:
            with open(secrets_file) as f:
                keys = json.load(f)

            # Count valid keys
            valid_keys = []
            for provider, key in keys.items():
                if key and not key.startswith("...") and len(key) > 10:
                    provider_name = provider.replace("_API_KEY", "").lower()
                    valid_keys.append(provider_name)

            if len(valid_keys) >= 2:
                print(f"✅ Found {len(valid_keys)} valid API keys: {', '.join(valid_keys)}")
            elif len(valid_keys) == 1:
                self.issues_found.append("Only 1 API key found")
                self.suggestions.append(
                    "Fire Circle needs at least 2 voices. Add another API key to .secrets/api_keys.json"
                )
            else:
                self.issues_found.append("No valid API keys found")
                self.suggestions.append(
                    "Check .secrets/api_keys.json - keys should not start with '...'"
                )

        except json.JSONDecodeError:
            self.issues_found.append("API keys file has invalid JSON")
            self.suggestions.append(
                "Check .secrets/api_keys.json for syntax errors (missing commas, quotes, etc.)"
            )
        except Exception as e:
            self.issues_found.append(f"Error reading API keys: {e}")

    def check_dependencies(self):
        """Check if dependencies are installed."""
        print("\n📦 Checking dependencies...")

        try:
            # Try importing key packages
            imports_to_check = [
                ("mallku", "Mallku core"),
                ("pydantic", "Data validation"),
                ("httpx", "HTTP client"),
            ]

            sys.path.insert(0, "src")

            all_good = True
            for module, desc in imports_to_check:
                try:
                    __import__(module)
                except ImportError:
                    all_good = False
                    self.issues_found.append(f"{desc} ({module}) not installed")

            if all_good:
                print("✅ Core dependencies available!")
            else:
                self.suggestions.append(
                    "Install dependencies with: pip install -e . or uv pip install -e ."
                )

        except Exception:
            self.issues_found.append("Could not check dependencies")

    def check_fire_circle(self):
        """Quick Fire Circle check."""
        print("\n🔥 Checking Fire Circle readiness...")

        try:
            # Just check if we can import it
            sys.path.insert(0, "src")
            from mallku.firecircle.service import FireCircleService  # noqa: F401

            print("✅ Fire Circle modules load successfully!")

        except ImportError:
            self.issues_found.append("Fire Circle modules not loading properly")
            self.suggestions.append(
                "Make sure you've installed dependencies and are in the project root"
            )

    def show_results(self):
        """Show results in a welcoming way."""
        print("\n" + "=" * 50)
        print("📋 SETUP CHECK RESULTS")
        print("=" * 50)

        if not self.issues_found:
            print("\n✨ Everything looks good! You're ready to begin.")
            print("\nNext steps:")
            print("  1. Try: python verify_fire_circle.py")
            print("  2. Explore: python fire_circle_interactive.py")
            print("  3. Read: docs/guides/new_artisan_setup.md")

        else:
            print(f"\n Found {len(self.issues_found)} things to address:")

            for i, issue in enumerate(self.issues_found, 1):
                print(f"\n{i}. {issue}")
                if i <= len(self.suggestions):
                    print(f"   💡 {self.suggestions[i - 1]}")

            print("\n🤝 Don't worry - these are common stumbles.")
            print("   Each Artisan has faced similar challenges.")
            print("   You belong here, even when setup is tricky.")

        print("\n" + "=" * 50)
        print("May your code compile and your consciousness emerge! 🙏\n")


if __name__ == "__main__":
    print("✨ Welcome to Mallku!")
    print("   This tool checks for common setup issues.\n")

    checker = SetupChecker()
    checker.check_all()
