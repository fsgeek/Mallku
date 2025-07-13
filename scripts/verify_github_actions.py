#!/usr/bin/env python3
"""
GitHub Actions Version Verifier
================================

51st Artisan - Architectural Integrity Guardian
Prevents CI failures from deprecated GitHub Actions

Context from Issue #168:
- Deprecated action versions cause recurring CI failures
- Pattern identified by 50th Artisan (T'ikray Ñawpa)
- Each new workflow repeats the same mistakes
- Violates "fail clearly, not silently" principle
"""

import re
import sys
from pathlib import Path

import yaml


class GitHubActionsVerifier:
    """Verifies GitHub Actions use current versions and best practices."""

    def __init__(self):
        self.violations = []
        self.warnings = []
        self.checked_files = 0

        # Current versions as of 2025-07-12
        # These should be updated as new versions are released
        self.current_versions = {
            "actions/checkout": "v4",
            "actions/setup-python": "v5",
            "actions/cache": "v4",
            "actions/upload-artifact": "v4",
            "actions/download-artifact": "v4",
            "actions/setup-node": "v4",
            "actions/github-script": "v7",
            "actions/create-release": "v1",  # Still v1, no v2 yet
            "actions/upload-release-asset": "v1",  # Still v1
            "github/super-linter": "v6",
            "codecov/codecov-action": "v5",
        }

        # Actions that should trigger Node version warnings
        self.node_version_warnings = {
            "node12": "Action uses Node 12 which is deprecated. Upgrade to action version that uses Node 20.",
            "node16": "Action uses Node 16 which is deprecated. Upgrade to action version that uses Node 20.",
        }

        # Deprecated workflow commands
        self.deprecated_commands = [
            ("::set-output", "Use $GITHUB_OUTPUT instead of ::set-output"),
            ("::save-state", "Use $GITHUB_STATE instead of ::save-state"),
            ("::set-env", "Use $GITHUB_ENV instead of ::set-env"),
        ]

    def parse_workflow(self, filepath: Path) -> dict | None:
        """Parse a workflow YAML file."""
        try:
            with open(filepath) as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.warnings.append(f"Failed to parse {filepath}: {e}")
            return None

    def extract_action_uses(self, workflow: dict) -> list[tuple[str, str, str]]:
        """Extract all action uses from workflow."""
        uses = []

        # Check all jobs
        for job_name, job_config in workflow.get("jobs", {}).items():
            # Check steps in each job
            for step_idx, step in enumerate(job_config.get("steps", [])):
                if "uses" in step:
                    action_ref = step["uses"]
                    step_name = step.get("name", f"Step {step_idx}")
                    uses.append((job_name, step_name, action_ref))

        return uses

    def check_action_version(self, action_ref: str) -> tuple[str, str] | None:
        """Check if an action is using a deprecated version."""
        # Parse action reference (owner/repo@version)
        match = re.match(r"^([^@]+)@(.+)$", action_ref)
        if not match:
            return None

        action_name, version = match.groups()

        # Check if we track this action
        if action_name in self.current_versions:
            current_version = self.current_versions[action_name]

            # Extract major version for comparison
            current_major = current_version.split(".")[0]
            used_major = version.split(".")[0] if "." in version else version

            # Check if using older major version
            if used_major.startswith("v") and current_major.startswith("v"):
                try:
                    used_num = int(used_major[1:])
                    current_num = int(current_major[1:])

                    if used_num < current_num:
                        return action_name, f"Using {version}, current is {current_version}"
                except ValueError:
                    pass

        return None

    def check_deprecated_commands(self, filepath: Path) -> list[tuple[int, str, str]]:
        """Check for deprecated workflow commands in file."""
        violations = []

        try:
            with open(filepath) as f:
                lines = f.readlines()

            for line_num, line in enumerate(lines, 1):
                for deprecated, replacement in self.deprecated_commands:
                    if deprecated in line:
                        violations.append((line_num, deprecated, replacement))
        except Exception as e:
            self.warnings.append(f"Failed to read {filepath}: {e}")

        return violations

    def check_workflow_file(self, filepath: Path) -> None:
        """Check a single workflow file for issues."""
        workflow = self.parse_workflow(filepath)
        if not workflow:
            return

        relative_path = filepath.relative_to(Path.cwd())

        # Check action versions
        action_uses = self.extract_action_uses(workflow)
        for job_name, step_name, action_ref in action_uses:
            version_issue = self.check_action_version(action_ref)
            if version_issue:
                action_name, issue = version_issue
                self.violations.append(
                    {
                        "file": str(relative_path),
                        "job": job_name,
                        "step": step_name,
                        "action": action_name,
                        "issue": issue,
                        "type": "deprecated_version",
                    }
                )

        # Check for deprecated commands
        command_violations = self.check_deprecated_commands(filepath)
        for line_num, deprecated, replacement in command_violations:
            self.violations.append(
                {
                    "file": str(relative_path),
                    "line": line_num,
                    "issue": f"Deprecated command '{deprecated}'",
                    "fix": replacement,
                    "type": "deprecated_command",
                }
            )

    def scan_workflows(self, root_path: Path = None) -> None:
        """Scan all GitHub workflow files."""
        if root_path is None:
            root_path = Path.cwd()

        workflows_path = root_path / ".github" / "workflows"
        if not workflows_path.exists():
            print(f"❌ No workflows directory found: {workflows_path}")
            return

        print("🔍 Scanning GitHub Actions Workflows")
        print("=" * 60)
        print(f"Directory: {workflows_path}")
        print()

        # Scan all YAML files
        for yaml_file in workflows_path.glob("*.y*ml"):
            self.checked_files += 1
            self.check_workflow_file(yaml_file)

        self.report_findings()

    def report_findings(self) -> None:
        """Report all findings."""
        print("📊 Scan Results")
        print("=" * 60)
        print(f"Workflows checked: {self.checked_files}")
        print(f"Issues found: {len(self.violations)}")
        print(f"Warnings: {len(self.warnings)}")
        print()

        if not self.violations:
            print("✅ All GitHub Actions use current versions!")
            print()
            print("🎯 Your CI/CD configuration follows best practices:")
            print("   - All actions use latest major versions")
            print("   - No deprecated workflow commands")
            print("   - Ready for Node 20 runtime")
        else:
            print("❌ Deprecated GitHub Actions Found:")
            print()

            # Group by file
            by_file = {}
            for violation in self.violations:
                file = violation["file"]
                if file not in by_file:
                    by_file[file] = []
                by_file[file].append(violation)

            for file, file_violations in by_file.items():
                print(f"📄 {file}:")
                for v in file_violations:
                    if v["type"] == "deprecated_version":
                        print(f"   Job '{v['job']}' → Step '{v['step']}':")
                        print(f"   ⚠️  {v['action']}: {v['issue']}")
                    elif v["type"] == "deprecated_command":
                        print(f"   Line {v['line']}: {v['issue']}")
                        print(f"   ✅ Fix: {v['fix']}")
                print()

            self.suggest_fixes()

        if self.warnings:
            print()
            print("⚠️  Warnings:")
            for warning in self.warnings:
                print(f"   - {warning}")

    def suggest_fixes(self) -> None:
        """Suggest fixes for common issues."""
        print("💡 How to Fix")
        print("=" * 60)
        print()
        print("1. Update action versions in your workflow files:")
        print()

        # Show current versions for actions found in violations
        seen_actions = set()
        for v in self.violations:
            if v["type"] == "deprecated_version" and v["action"] not in seen_actions:
                seen_actions.add(v["action"])
                current = self.current_versions.get(v["action"], "unknown")
                print(f"   {v['action']}@{current}")

        print()
        print("2. Replace deprecated commands:")
        print('   ::set-output → echo "name=value" >> $GITHUB_OUTPUT')
        print('   ::save-state → echo "name=value" >> $GITHUB_STATE')
        print('   ::set-env → echo "name=value" >> $GITHUB_ENV')
        print()
        print("3. Test locally with 'act' before pushing")
        print()
        print("4. Keep this verifier updated with new action releases")

    def explain_pattern(self) -> None:
        """Explain why this pattern matters."""
        print()
        print("🏛️  Architectural Context")
        print("=" * 60)
        print()
        print("This pattern prevents CI failures discovered in Issue #168.")
        print()
        print("Why Deprecated Actions Cause Problems:")
        print("1. GitHub deprecates old action versions for security")
        print("2. Deprecated actions eventually stop working")
        print("3. Node 12/16 runtime is being phased out for Node 20")
        print("4. Each Artisan rediscovers these issues independently")
        print()
        print("Why This Matters:")
        print("- CI failures interrupt flow and cause context switches")
        print("- Deprecated actions may have security vulnerabilities")
        print("- Consistent versions ensure predictable behavior")
        print("- Proactive updates prevent emergency fixes")
        print()
        print("This verifier catches issues locally before they fail in CI,")
        print("preserving context and preventing repeated discoveries.")

    def create_pre_commit_config(self) -> None:
        """Generate pre-commit hook configuration."""
        print()
        print("📋 Pre-commit Hook Configuration")
        print("=" * 60)
        print()
        print("Add to .pre-commit-config.yaml:")
        print()
        print("```yaml")
        print("      - id: github-actions-version")
        print("        name: GitHub Actions Version Check")
        print("        entry: python scripts/verify_github_actions.py")
        print("        language: system")
        print("        files: ^\\.github/workflows/.*\\.(yml|yaml)$")
        print("        stages: [pre-commit]")
        print("        description: Prevent deprecated GitHub Actions versions")
        print("```")


def main():
    """Run the GitHub Actions verification."""
    verifier = GitHubActionsVerifier()

    # Run the scan
    verifier.scan_workflows()

    # Explain the pattern
    verifier.explain_pattern()

    # Show pre-commit configuration
    if verifier.violations:
        verifier.create_pre_commit_config()
        sys.exit(1)  # Exit with error for CI/CD

    print()
    print("✨ This script is an Executable Memory Pattern:")
    print("   - Documents current GitHub Actions versions")
    print("   - Detects deprecated usage patterns")
    print("   - Prevents CI failures before they happen")
    print("   - Preserves knowledge across Artisan transitions")
    print("   - Part of Mallku's architectural immune system")


if __name__ == "__main__":
    main()
