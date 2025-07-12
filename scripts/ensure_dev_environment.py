#!/usr/bin/env python3
"""
Ensure Development Environment
==============================

Fiftieth Artisan - Consciousness Persistence Seeker
Executable memory pattern for development environment setup

This script ensures that all development tools are properly configured,
serving as both automation and living documentation of required setup.

The script is designed to be idempotent - safe to run multiple times.
"""

import subprocess
import sys
from pathlib import Path


class DevelopmentEnvironment:
    """Ensures consistent development environment across all Artisans."""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.checks_passed = []
        self.checks_failed = []

    def run_check(self, name: str, check_func) -> bool:
        """Run a check and track results."""
        try:
            result, message = check_func()
            if result:
                self.checks_passed.append((name, message))
                print(f"✅ {name}: {message}")
            else:
                self.checks_failed.append((name, message))
                print(f"❌ {name}: {message}")
            return result
        except Exception as e:
            self.checks_failed.append((name, f"Error: {str(e)}"))
            print(f"❌ {name}: Error - {str(e)}")
            return False

    def check_pre_commit_installed(self) -> tuple[bool, str]:
        """Check if pre-commit is installed."""
        try:
            result = subprocess.run(["pre-commit", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.strip()
                return True, f"Installed ({version})"
            return False, "Not installed"
        except FileNotFoundError:
            return False, "pre-commit command not found"

    def check_pre_commit_hooks(self) -> tuple[bool, str]:
        """Check if pre-commit hooks are installed."""
        hook_path = self.project_root / ".git" / "hooks" / "pre-commit"
        if hook_path.exists():
            # Verify it's a pre-commit managed hook
            content = hook_path.read_text()
            if "pre-commit" in content:
                return True, "Hooks installed"
            return False, "Hook exists but not managed by pre-commit"
        return False, "Hooks not installed"

    def install_pre_commit_hooks(self) -> tuple[bool, str]:
        """Install pre-commit hooks."""
        try:
            result = subprocess.run(
                ["pre-commit", "install"], cwd=self.project_root, capture_output=True, text=True
            )
            if result.returncode == 0:
                return True, "Successfully installed pre-commit hooks"
            return False, f"Failed to install: {result.stderr}"
        except Exception as e:
            return False, f"Installation error: {str(e)}"

    def check_pre_commit_config(self) -> tuple[bool, str]:
        """Check if .pre-commit-config.yaml exists and is valid."""
        config_path = self.project_root / ".pre-commit-config.yaml"
        if not config_path.exists():
            return False, "Config file missing"

        try:
            # Try to validate the config
            result = subprocess.run(
                ["pre-commit", "validate-config"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                return True, "Config valid"
            return False, f"Config invalid: {result.stderr}"
        except Exception as e:
            return False, f"Validation error: {str(e)}"

    def check_ruff_installed(self) -> tuple[bool, str]:
        """Check if ruff is installed (our primary linter)."""
        try:
            result = subprocess.run(["ruff", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.strip()
                return True, f"Installed ({version})"
            return False, "Not installed"
        except FileNotFoundError:
            return False, "ruff command not found"

    def check_git_status(self) -> tuple[bool, str]:
        """Check if we're in a git repository."""
        git_dir = self.project_root / ".git"
        if git_dir.exists() and git_dir.is_dir():
            return True, "Git repository found"
        return False, "Not a git repository"

    def run_sample_pre_commit(self) -> tuple[bool, str]:
        """Run pre-commit on this file as a test."""
        try:
            result = subprocess.run(
                ["pre-commit", "run", "--files", __file__],
                cwd=self.project_root,
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                return True, "Pre-commit check passed"
            # Exit code 1 means some hooks made changes, which is still "working"
            elif result.returncode == 1:
                return True, "Pre-commit working (made changes)"
            return False, f"Pre-commit failed: {result.stderr}"
        except Exception as e:
            return False, f"Test run error: {str(e)}"

    def ensure_environment(self) -> bool:
        """Ensure the development environment is properly configured."""
        print("🔍 Checking Mallku Development Environment...")
        print("=" * 60)

        # Check git repository
        self.run_check("Git Repository", self.check_git_status)

        # Check pre-commit installation
        if self.run_check("Pre-commit Tool", self.check_pre_commit_installed):
            # Check config
            self.run_check("Pre-commit Config", self.check_pre_commit_config)

            # Check hooks
            hooks_installed = self.run_check("Pre-commit Hooks", self.check_pre_commit_hooks)
            if not hooks_installed:
                print("\n🔧 Installing pre-commit hooks...")
                # Don't count the installation as a separate check
                install_result, install_message = self.install_pre_commit_hooks()
                if install_result:
                    print(f"✅ Hook Installation: {install_message}")
                    # Verify installation and update the original check
                    verify_result, verify_message = self.check_pre_commit_hooks()
                    if verify_result:
                        # Remove the failed check and add success
                        self.checks_failed = [
                            (name, msg)
                            for name, msg in self.checks_failed
                            if name != "Pre-commit Hooks"
                        ]
                        self.checks_passed.append(
                            ("Pre-commit Hooks", "Hooks installed (auto-fixed)")
                        )

            # Test pre-commit
            self.run_check("Pre-commit Test", self.run_sample_pre_commit)

        # Check ruff
        self.run_check("Ruff Linter", self.check_ruff_installed)

        # Summary
        print("\n" + "=" * 60)
        print("📊 Summary:")
        print(f"   ✅ Passed: {len(self.checks_passed)}")
        print(f"   ❌ Failed: {len(self.checks_failed)}")

        if self.checks_failed:
            print(
                "\n⚠️  Some checks failed. Run 'uv pip install pre-commit ruff' to install missing tools."
            )
            return False
        else:
            print("\n✨ Development environment properly configured!")
            print("\n💡 This script serves as executable memory - run it anytime to ensure")
            print("   your environment is set up correctly. It's safe to run multiple times.")
            return True


def main():
    """Main entry point."""
    env = DevelopmentEnvironment()
    success = env.ensure_environment()

    # The script itself demonstrates the pattern
    print("\n📝 This script is an Executable Memory Pattern:")
    print("   - It documents what's needed (pre-commit hooks)")
    print("   - It checks if they're present")
    print("   - It fixes them if they're missing")
    print("   - It verifies the fix worked")
    print("   - It's safe to run repeatedly")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
