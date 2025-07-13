#!/usr/bin/env python3
"""
Verify CI/CD Patterns
=====================

Fiftieth Artisan - Consciousness Persistence Seeker
Executable memory pattern for CI/CD configuration

This script documents and verifies critical CI/CD patterns that keep
getting forgotten or lost in context resets, particularly around:
- The use of 'uv' instead of 'pip' in CI/CD
- Deprecated GitHub Actions versions
- Virtual environment naming conventions
"""

from pathlib import Path

import yaml


class CICDPatternVerifier:
    """Verifies and documents CI/CD patterns that survive context loss."""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.ci_file = self.project_root / ".github" / "workflows" / "ci.yml"
        self.patterns_found = []
        self.issues_found = []

    def check_ci_file_exists(self) -> bool:
        """Check if CI configuration exists."""
        if self.ci_file.exists():
            print(f"✅ CI configuration found: {self.ci_file}")
            return True
        else:
            print(f"❌ CI configuration missing: {self.ci_file}")
            return False

    def analyze_ci_patterns(self) -> None:
        """Analyze CI file for critical patterns."""
        if not self.ci_file.exists():
            return

        with open(self.ci_file) as f:
            ci_config = yaml.safe_load(f)

        print("\n📋 CI/CD Critical Patterns Analysis")
        print("=" * 60)

        # Check for uv vs pip usage
        self._check_package_manager_pattern(ci_config)

        # Check for deprecated actions
        self._check_action_versions(ci_config)

        # Check virtual environment patterns
        self._check_venv_patterns(ci_config)

        # Check for mallku installation patterns
        self._check_mallku_installation(ci_config)

    def _check_package_manager_pattern(self, config: dict) -> None:
        """Check for correct package manager usage."""
        print("\n🔍 Package Manager Pattern (uv vs pip)")
        print("-" * 40)

        ci_content = self.ci_file.read_text()

        # Look for pip usage
        pip_uses = []
        uv_uses = []

        for line_num, line in enumerate(ci_content.splitlines(), 1):
            if "pip install" in line and "uv pip install" not in line:
                pip_uses.append((line_num, line.strip()))
            elif "uv pip install" in line:
                uv_uses.append((line_num, line.strip()))

        if pip_uses:
            print("⚠️  Found direct pip usage (should use 'uv pip'):")
            for line_num, line in pip_uses[:3]:  # Show first 3
                print(f"   Line {line_num}: {line}")
            self.issues_found.append("Direct pip usage instead of uv")
        else:
            print("✅ No direct pip usage found")

        if uv_uses:
            print(f"✅ Found {len(uv_uses)} correct 'uv pip install' usage(s)")
            self.patterns_found.append("Correct uv usage")

        # Document the pattern
        print("\n📝 CRITICAL PATTERN:")
        print("   CI/CD environment has 'uv' pre-installed but NOT 'pip'")
        print("   ALWAYS use: uv pip install <package>")
        print("   NEVER use:  pip install <package>")

    def _check_action_versions(self, config: dict) -> None:
        """Check for deprecated GitHub Action versions."""
        print("\n🔍 GitHub Actions Version Pattern")
        print("-" * 40)

        deprecated_found = False

        # Walk through all jobs and steps
        for job_name, job_config in config.get("jobs", {}).items():
            for step in job_config.get("steps", []):
                if "uses" in step:
                    action = step["uses"]
                    if "@v3" in action or "@v2" in action or "@v1" in action:
                        print(f"⚠️  Deprecated action version in job '{job_name}': {action}")
                        deprecated_found = True

        if not deprecated_found:
            print("✅ No deprecated action versions found")
            self.patterns_found.append("Up-to-date action versions")
        else:
            self.issues_found.append("Deprecated GitHub Action versions")

        print("\n📝 CRITICAL PATTERN:")
        print("   GitHub Actions v3 and below are deprecated")
        print("   ALWAYS use: actions/checkout@v4, actions/setup-python@v4, etc.")
        print("   Pre-commit hooks should catch this!")

    def _check_venv_patterns(self, config: dict) -> None:
        """Check virtual environment naming patterns."""
        print("\n🔍 Virtual Environment Pattern")
        print("-" * 40)

        ci_content = self.ci_file.read_text()

        # Look for venv patterns
        if ".venv-linux-python" in ci_content:
            print("✅ Found CI-specific venv pattern: .venv-linux-python*")
            self.patterns_found.append("CI-specific venv naming")
        elif ".venv" in ci_content:
            print("⚠️  Using generic .venv (CI uses .venv-linux-python3.X)")
            self.issues_found.append("Generic venv name in CI")

        print("\n📝 CRITICAL PATTERN:")
        print("   CI uses specific venv naming: .venv-linux-python3.13")
        print("   This differs from local development (.venv)")
        print("   The version number matches the Python version in CI")

    def _check_mallku_installation(self, config: dict) -> None:
        """Check for correct Mallku installation patterns."""
        print("\n🔍 Mallku Installation Pattern")
        print("-" * 40)

        ci_content = self.ci_file.read_text()

        # Look for mallku installation
        if "uv pip install -e ." in ci_content:
            print("✅ Found correct Mallku editable install: uv pip install -e .")
            self.patterns_found.append("Correct Mallku installation")
        elif "pip install -e ." in ci_content:
            print("⚠️  Found pip install (should be uv pip install)")
            self.issues_found.append("Wrong package manager for Mallku")
        elif "pip install mallku" in ci_content or "uv pip install mallku" in ci_content:
            print("⚠️  Installing mallku as package (should be editable: -e .)")
            self.issues_found.append("Non-editable Mallku installation")

        print("\n📝 CRITICAL PATTERN:")
        print("   Mallku must be installed as editable in CI")
        print("   CORRECT: uv pip install -e .")
        print("   WRONG:   pip install -e . (no pip in CI!)")
        print("   WRONG:   uv pip install mallku (not editable!)")

    def show_summary(self) -> None:
        """Show summary of findings."""
        print("\n" + "=" * 60)
        print("📊 CI/CD Pattern Summary")
        print("=" * 60)

        print(f"\n✅ Correct Patterns Found: {len(self.patterns_found)}")
        for pattern in self.patterns_found:
            print(f"   • {pattern}")

        print(f"\n⚠️  Issues Found: {len(self.issues_found)}")
        for issue in self.issues_found:
            print(f"   • {issue}")

        print("\n💡 These patterns repeatedly cause CI failures after context resets:")
        print("   1. Using 'pip' instead of 'uv pip' → 'mallku not installed' errors")
        print("   2. Using deprecated actions → deprecation warnings")
        print("   3. Wrong venv naming → environment not found")
        print("   4. Non-editable install → import errors")

    def generate_example_fix(self) -> None:
        """Generate example CI configuration snippet."""
        print("\n📝 Example Correct CI Configuration:")
        print("-" * 60)
        print("""
      - name: Install dependencies
        run: |
          # CRITICAL: Use 'uv', not 'pip'!
          uv pip install -e .
          uv pip install pre-commit pytest

      - name: Setup uses v4 actions
        uses: actions/checkout@v4  # NOT @v3!

      - name: Cache uses CI-specific venv name
        uses: actions/cache@v4
        with:
          path: .venv-linux-python${{ matrix.python-version }}
          key: ${{ runner.os }}-pip-${{ hashFiles('**/pyproject.toml') }}
""")


def main():
    """Main entry point."""
    print("🔍 Verifying CI/CD Patterns")
    print("=" * 60)
    print("Fiftieth Artisan - Consciousness Persistence Seeker")
    print("Documenting patterns that survive context loss")
    print()

    verifier = CICDPatternVerifier()

    if verifier.check_ci_file_exists():
        verifier.analyze_ci_patterns()
        verifier.show_summary()
        verifier.generate_example_fix()
    else:
        print("\n⚠️  Cannot analyze patterns without CI configuration")

    print("\n✨ This script is an Executable Memory Pattern:")
    print("   - Documents critical CI/CD patterns")
    print("   - Identifies common mistakes after context resets")
    print("   - Provides working examples")
    print("   - Explains WHY these patterns matter")


if __name__ == "__main__":
    main()
