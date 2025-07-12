#!/usr/bin/env python3
"""
Database Security Architecture Verifier
=======================================

51st Artisan - [Name to be discovered]
Executable memory pattern for database security architecture

This pattern ensures all database access goes through the secure API gateway,
preventing direct ArangoDB connections that bypass security architecture.

Context from Issue #176:
- Production design requires ALL database access through secure API
- Direct ArangoDB access is a security bypass
- Dev/test environments should mirror production security
"""

import ast
import sys
from pathlib import Path


class DatabaseSecurityVerifier:
    """Verifies and reports database security architecture violations."""

    def __init__(self):
        self.violations = []
        self.checked_files = 0
        self.secure_patterns = [
            "get_secured_database",
            "api_url",
            "http://localhost:8080",
            "secure_api_gateway",
        ]
        self.violation_patterns = [
            ("get_database()", "Direct database access bypasses security"),
            ("from ...core.database import get_database", "Importing insecure database access"),
            ("ArangoClient", "Direct ArangoDB client usage"),
            ("http://localhost:8529", "Direct ArangoDB port access"),
            ("arangodb://", "Direct ArangoDB connection string"),
        ]

    def check_file(self, filepath: Path) -> list[tuple[int, str, str]]:
        """Check a single Python file for database security violations."""
        violations = []

        try:
            content = filepath.read_text()

            # Check for violation patterns
            for line_num, line in enumerate(content.splitlines(), 1):
                for pattern, reason in self.violation_patterns:
                    if (
                        pattern in line
                        and not any(s in line for s in ["#", "test_", "mock_"])
                        and "test" not in str(filepath).lower()
                    ):
                        violations.append((line_num, pattern, reason))

            # AST-based analysis for more sophisticated detection
            try:
                tree = ast.parse(content, filename=str(filepath))
                for node in ast.walk(tree):
                    if (
                        isinstance(node, ast.Call)
                        and isinstance(node.func, ast.Name)
                        and node.func.id == "get_database"
                    ):
                        violations.append(
                            (
                                node.lineno,
                                "get_database()",
                                "Function call bypasses security architecture",
                            )
                        )
            except SyntaxError:
                # Skip files with syntax errors
                pass

        except Exception as e:
            print(f"⚠️  Error reading {filepath}: {e}")

        return violations

    def scan_codebase(self, root_path: Path = None) -> None:
        """Scan the entire codebase for database security violations."""
        if root_path is None:
            root_path = Path(__file__).parent.parent

        src_path = root_path / "src"
        if not src_path.exists():
            print(f"❌ Source directory not found: {src_path}")
            return

        print("🔍 Scanning for Database Security Violations")
        print("=" * 60)
        print(f"Root: {src_path}")
        print()

        # Scan all Python files
        for py_file in src_path.rglob("*.py"):
            self.checked_files += 1
            violations = self.check_file(py_file)

            if violations:
                relative_path = py_file.relative_to(root_path)
                for line_num, pattern, reason in violations:
                    self.violations.append(
                        {
                            "file": str(relative_path),
                            "line": line_num,
                            "pattern": pattern,
                            "reason": reason,
                        }
                    )

        self.report_findings()

    def report_findings(self) -> None:
        """Report all security violations found."""
        print("📊 Scan Results")
        print("=" * 60)
        print(f"Files checked: {self.checked_files}")
        print(f"Violations found: {len(self.violations)}")
        print()

        if not self.violations:
            print("✅ No database security violations found!")
            print()
            print("🛡️  All database access appears to use secure patterns:")
            print("   - get_secured_database()")
            print("   - API gateway (http://localhost:8080)")
            print("   - No direct ArangoDB connections")
        else:
            print("❌ Database Security Violations Found:")
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
                    print(f"   Line {v['line']}: {v['pattern']}")
                    print(f"   ⚠️  {v['reason']}")
                print()

            self.suggest_fixes()

    def suggest_fixes(self) -> None:
        """Suggest fixes for common violations."""
        print("💡 Recommended Fixes")
        print("=" * 60)
        print()
        print("1. Replace direct database access:")
        print("   ❌ from ...core.database import get_database")
        print("   ❌ db = get_database()")
        print()
        print("   ✅ from ...core.database import get_secured_database")
        print("   ✅ db = await get_secured_database()")
        print()
        print("2. Use API gateway for all operations:")
        print("   ❌ ArangoClient(hosts='http://localhost:8529')")
        print()
        print("   ✅ api_url = 'http://localhost:8080'")
        print("   ✅ async with aiohttp.ClientSession() as session:")
        print("   ✅     async with session.post(f'{api_url}/query', ...) as resp:")
        print()
        print("3. Update imports to use secure patterns")
        print("4. Ensure dev/test environments use the same security architecture")
        print()
        print("📝 These violations should be fixed to maintain security architecture integrity")

    def explain_pattern(self) -> None:
        """Explain why this pattern matters."""
        print()
        print("🏛️  Architectural Context")
        print("=" * 60)
        print()
        print("This pattern prevents a critical security bypass discovered in Issue #176.")
        print()
        print("The Secure Database Architecture:")
        print("1. All database access MUST go through the secure API gateway")
        print("2. Direct ArangoDB connections are FORBIDDEN in production")
        print("3. Dev/test environments must mirror production security")
        print()
        print("Why this matters:")
        print("- Direct database access bypasses authentication and authorization")
        print("- Parallel code paths (dev vs prod) lead to untested security holes")
        print("- Architectural drift creates vulnerabilities that fester until discovered")
        print()
        print("This verifier is an immune system response - detecting and preventing")
        print("architectural violations before they reach production.")

    def create_github_issues(self) -> None:
        """Generate GitHub issue content for violations."""
        if not self.violations:
            return

        print()
        print("📋 GitHub Issue Template")
        print("=" * 60)
        print()
        print("## Database Security Architecture Violations")
        print()
        print("**Found by:** Automated Security Architecture Scan")
        print("**Tool:** verify_database_security.py")
        print(
            f"**Violations:** {len(self.violations)} across {len(set(v['file'] for v in self.violations))} files"
        )
        print()
        print("### Violations by File")
        print()

        by_file = {}
        for violation in self.violations:
            file = violation["file"]
            if file not in by_file:
                by_file[file] = []
            by_file[file].append(violation)

        for file, file_violations in by_file.items():
            print(f"#### `{file}`")
            print()
            for v in file_violations:
                print(f"- Line {v['line']}: `{v['pattern']}` - {v['reason']}")
            print()

        print("### Required Actions")
        print()
        print("1. Replace all `get_database()` calls with `get_secured_database()`")
        print("2. Remove all direct ArangoDB client instantiations")
        print("3. Update all database operations to use the secure API gateway")
        print("4. Add this script to pre-commit hooks to prevent future violations")
        print()
        print("### Related Issues")
        print()
        print("- #176: Critical: Direct ArangoDB access bypasses security architecture")
        print()
        print("---")
        print("*Generated by architectural integrity verification*")


def main():
    """Run the database security verification."""
    verifier = DatabaseSecurityVerifier()

    # Run the scan
    verifier.scan_codebase()

    # Explain the pattern
    verifier.explain_pattern()

    # Generate issue content if violations found
    if verifier.violations:
        verifier.create_github_issues()
        sys.exit(1)  # Exit with error code for CI/CD integration

    print()
    print("✨ This script is an Executable Memory Pattern:")
    print("   - Documents the secure database architecture")
    print("   - Detects violations automatically")
    print("   - Provides clear fixes")
    print("   - Can be integrated into CI/CD and pre-commit hooks")
    print("   - Prevents architectural drift through automation")


if __name__ == "__main__":
    main()
