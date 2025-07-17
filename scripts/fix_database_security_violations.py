#!/usr/bin/env python3
"""
Database Security Violation Fixer
=================================

53rd Guardian - Healing architectural wounds

This script systematically fixes database security violations by converting
all direct database access to use the secure API gateway pattern.

Context:
- Issue #177: 34 violations across 6 files
- All database access MUST go through secure API gateway
- No exceptions for "internal" or "metrics" data
"""

import re
from pathlib import Path


class DatabaseSecurityFixer:
    """Automatically fix database security violations."""

    def __init__(self):
        self.fixed_files = 0
        self.total_fixes = 0

    def fix_import(self, content: str) -> tuple[str, int]:
        """Fix database import statements."""
        fixes = 0

        # Fix get_database imports
        pattern = r"from\s+\.+core\.database\s+import\s+get_database"
        replacement = "from ...core.database import get_secured_database"
        content, count = re.subn(pattern, replacement, content)
        fixes += count

        # Fix ArangoClient imports
        pattern = r"from\s+arango\s+import\s+ArangoClient"
        replacement = "# from arango import ArangoClient  # REMOVED: Use secure API gateway instead"
        content, count = re.subn(pattern, replacement, content)
        fixes += count

        return content, fixes

    def fix_database_calls(self, content: str) -> tuple[str, int]:
        """Fix database access patterns."""
        fixes = 0

        # Fix get_database() calls
        pattern = r"get_database\(\)"
        replacement = "await get_secured_database()"
        content, count = re.subn(pattern, replacement, content)
        fixes += count

        # Fix localhost:8529 references
        pattern = r"http://localhost:8529"
        replacement = "http://localhost:8080"  # API gateway
        content, count = re.subn(pattern, replacement, content)
        fixes += count

        # Mark functions as async if they weren't already
        if "await get_secured_database()" in content:
            # Find function definitions that use database
            lines = content.split("\n")
            new_lines = []
            for i, line in enumerate(lines):
                if (
                    "def " in line
                    and "await get_secured_database()" in "\n".join(lines[i : i + 20])
                    and not line.strip().startswith("async ")
                ):
                    line = line.replace("def ", "async def ")
                    fixes += 1
                new_lines.append(line)
            content = "\n".join(new_lines)

        return content, fixes

    def add_security_comment(self, content: str) -> str:
        """Add security architecture comment."""
        if "# SECURITY: All database access through secure API gateway" not in content:
            lines = content.split("\n")

            # Find import section
            import_section_end = 0
            for i, line in enumerate(lines):
                if line.strip() and not line.startswith(("import ", "from ", "#", '"""')):
                    import_section_end = i
                    break

            # Add security comment after imports
            lines.insert(import_section_end, "")
            lines.insert(
                import_section_end + 1, "# SECURITY: All database access through secure API gateway"
            )
            lines.insert(
                import_section_end + 2,
                "# Direct ArangoDB access is FORBIDDEN - use get_secured_database()",
            )
            lines.insert(import_section_end + 3, "")

            content = "\n".join(lines)

        return content

    def remove_bypass_justifications(self, content: str) -> tuple[str, int]:
        """Remove comments that justify security bypasses."""
        fixes = 0

        # Remove dangerous justification comments
        patterns = [
            r"#.*Direct access needed for internal metrics.*",
            r"#.*We use get_database\(\) instead of get_secured_database\(\).*",
            r"#.*internal system data, not user data.*",
            r"#.*need AQL access for complex queries.*",
        ]

        for pattern in patterns:
            content, count = re.subn(pattern, "", content, flags=re.IGNORECASE)
            fixes += count

        return content, fixes

    def fix_file(self, filepath: Path) -> bool:
        """Fix security violations in a single file."""
        try:
            content = filepath.read_text()
            original_content = content
            total_fixes = 0

            # Apply fixes
            content, fixes = self.fix_import(content)
            total_fixes += fixes

            content, fixes = self.fix_database_calls(content)
            total_fixes += fixes

            content, fixes = self.remove_bypass_justifications(content)
            total_fixes += fixes

            # Add security comment if file was modified
            if total_fixes > 0:
                content = self.add_security_comment(content)

            # Write back if changed
            if content != original_content:
                filepath.write_text(content)
                self.fixed_files += 1
                self.total_fixes += total_fixes
                return True

        except Exception as e:
            print(f"❌ Error fixing {filepath}: {e}")

        return False

    def fix_known_violations(self):
        """Fix all known database security violations."""
        root = Path(__file__).parent.parent

        # Known violation files from Issue #177
        violation_files = [
            "src/mallku/memory_anchor_service.py",
            "src/mallku/core/database.py",
            "src/mallku/core/database_auto_setup.py",
            "src/mallku/firecircle/consciousness/database_metrics_collector.py",
            "src/mallku/core/database/factory.py",
            "src/mallku/core/database/__init__.py",
        ]

        print("🔧 Fixing Database Security Violations")
        print("=" * 60)
        print()

        for file_path in violation_files:
            full_path = root / file_path
            if full_path.exists():
                print(f"📝 Processing: {file_path}")
                if self.fix_file(full_path):
                    print("   ✅ Fixed security violations")
                else:
                    print("   ⏭️  No violations found or already fixed")
            else:
                print(f"⚠️  File not found: {file_path}")

        print()
        print("📊 Summary")
        print("=" * 60)
        print(f"Files fixed: {self.fixed_files}")
        print(f"Total fixes applied: {self.total_fixes}")

        if self.fixed_files > 0:
            print()
            print("✅ Security violations have been fixed!")
            print()
            print("Next steps:")
            print("1. Run tests to ensure functionality is preserved")
            print("2. Run scripts/verify_database_security.py to confirm all violations fixed")
            print("3. Commit changes with message referencing Issue #177")
            print()
            print("⚠️  IMPORTANT: Some files may need additional manual fixes:")
            print("   - Complex AQL queries may need API endpoint implementations")
            print("   - Direct collection access patterns need API gateway equivalents")
            print("   - Test files may need updates for async database access")

    def create_api_gateway_example(self):
        """Create example of how to use API gateway for complex queries."""
        example = '''
# Example: Converting Direct AQL to API Gateway Pattern
# =====================================================

# ❌ OLD (Direct AQL - Security Violation):
db = get_database()
aql = """
FOR doc IN @@collection
    FILTER doc.timestamp > DATE_ISO8601(@cutoff)
    SORT doc.timestamp DESC
    LIMIT 1000
    RETURN doc
"""
cursor = db.aql.execute(aql, bind_vars={...})

# ✅ NEW (API Gateway Pattern):
import aiohttp

async def query_consciousness_signatures(cutoff: float):
    api_url = 'http://localhost:8080'

    query_payload = {
        "collection": "consciousness_signatures",
        "filter": {"timestamp": {"$gt": cutoff}},
        "sort": [{"timestamp": "desc"}],
        "limit": 1000
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f'{api_url}/query',
            json=query_payload,
            headers={"Authorization": "Bearer <token>"}
        ) as response:
            result = await response.json()
            return result["data"]

# Alternative: Use specialized API endpoints
async with aiohttp.ClientSession() as session:
    async with session.get(
        f'{api_url}/consciousness/signatures',
        params={"since": cutoff, "limit": 1000}
    ) as response:
        signatures = await response.json()
'''

        print()
        print("📚 API Gateway Pattern Example")
        print("=" * 60)
        print(example)


def main():
    """Run the security violation fixer."""
    fixer = DatabaseSecurityFixer()

    # Fix known violations
    fixer.fix_known_violations()

    # Show API gateway example
    fixer.create_api_gateway_example()

    print()
    print("🔒 Security Architecture Enforcement")
    print("=" * 60)
    print()
    print("Remember: ALL database access must go through the secure API gateway.")
    print("No exceptions for 'internal' data, 'metrics', or 'system' operations.")
    print()
    print("The API gateway provides:")
    print("- Authentication and authorization")
    print("- Audit logging")
    print("- Rate limiting")
    print("- Consistent security model")
    print()
    print("This is not optional - it's a core architectural requirement.")


if __name__ == "__main__":
    main()
