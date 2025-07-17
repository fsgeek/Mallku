#!/usr/bin/env python3
"""
Database Security Structural Barrier Creator
============================================

Seventh Anthropologist - Creating Unbreakable Patterns

This script creates structural barriers that make security violations impossible,
not just detectable. It implements the principle: "Make the right way the only way."

The pattern addresses the root cause: when both secure and insecure options exist,
confusion leads to violations. The solution is to remove the insecure option entirely.
"""

import re
from pathlib import Path


class StructuralBarrierCreator:
    """Creates architectural barriers that prevent security violations structurally."""

    def __init__(self):
        self.modifications = []
        self.project_root = Path(__file__).parent.parent

    def analyze_usage_patterns(self) -> dict[str, list[str]]:
        """Analyze how get_database is used across the codebase."""
        usage_patterns = {
            "direct_calls": [],
            "imports": [],
            "test_usage": [],
            "legitimate_internal": [],
        }

        src_path = self.project_root / "src"

        for py_file in src_path.rglob("*.py"):
            try:
                content = py_file.read_text()

                # Find direct calls
                if "get_database()" in content:
                    if "test" in str(py_file).lower():
                        usage_patterns["test_usage"].append(str(py_file))
                    elif "factory.py" in str(py_file) or "secured_interface.py" in str(py_file):
                        usage_patterns["legitimate_internal"].append(str(py_file))
                    else:
                        usage_patterns["direct_calls"].append(str(py_file))

                # Find imports
                if re.search(r"from.*import.*get_database", content):
                    usage_patterns["imports"].append(str(py_file))

            except Exception as e:
                print(f"Error analyzing {py_file}: {e}")

        return usage_patterns

    def create_deprecation_wrapper(self):
        """Create a wrapper that makes get_database raise an error."""
        wrapper_file = self.project_root / "src/mallku/core/database/deprecated.py"

        content = '''"""
Deprecated Database Access Functions
===================================

These functions exist only to provide clear error messages when
legacy code attempts to use insecure database access patterns.

This is part of the structural barrier pattern: make violations
impossible, not just detectable.
"""

import warnings
from typing import NoReturn


class DatabaseSecurityViolation(Exception):
    """Raised when code attempts to bypass database security architecture."""

    def __init__(self):
        super().__init__(
            "\\n\\nDATABASE SECURITY VIOLATION\\n"
            "=" * 60 + "\\n"
            "Direct database access is FORBIDDEN.\\n\\n"
            "You must use: get_secured_database()\\n\\n"
            "Why this matters:\\n"
            "- Direct access bypasses authentication and authorization\\n"
            "- Parallel code paths lead to untested security holes\\n"
            "- Architectural drift creates vulnerabilities\\n\\n"
            "To fix this error:\\n"
            "1. Replace: from ...core.database import get_database\\n"
            "   With:    from ...core.database import get_secured_database\\n\\n"
            "2. Replace: db = get_database()\\n"
            "   With:    db = await get_secured_database()\\n\\n"
            "3. Update function to be async if needed\\n\\n"
            "See: https://github.com/fsgeek/Mallku/issues/177\\n"
            "=" * 60
        )


def get_database(*args, **kwargs) -> NoReturn:
    """
    DEPRECATED: Direct database access violates security architecture.

    This function exists only to provide a clear error message.
    Use get_secured_database() instead.
    """
    raise DatabaseSecurityViolation()


def MallkuDBConfig(*args, **kwargs) -> NoReturn:
    """
    DEPRECATED: Direct configuration violates security architecture.

    Database configuration is now handled internally by the
    secured database interface.
    """
    raise DatabaseSecurityViolation()


# Deprecated aliases to catch all variants
get_db = get_database
get_db_connection = get_database
get_database_connection = get_database
'''

        wrapper_file.parent.mkdir(parents=True, exist_ok=True)
        wrapper_file.write_text(content)
        print(f"✅ Created deprecation wrapper at {wrapper_file}")

    def update_database_init(self):
        """Update __init__.py to use deprecation wrapper."""
        init_file = self.project_root / "src/mallku/core/database/__init__.py"

        if not init_file.exists():
            print(f"❌ {init_file} not found")
            return

        content = init_file.read_text()

        # Remove get_database from __all__ exports
        content = re.sub(r'"get_database",?\s*', "", content)

        # Replace the legacy alias with deprecation import
        content = re.sub(
            r"get_database = get_database_raw.*",
            "from .deprecated import get_database, MallkuDBConfig  # Deprecated - will raise errors",
            content,
            flags=re.MULTILINE | re.DOTALL,
        )

        # Ensure get_secured_database is prominently exported
        if '"get_secured_database"' not in content:
            content = re.sub(
                r"__all__ = \[",
                '__all__ = [\n    # REQUIRED: All database access must use this function\n    "get_secured_database",',
                content,
            )

        # Add architectural note at the top
        if "ARCHITECTURAL ENFORCEMENT" not in content:
            architectural_note = '''"""
Database Access Layer - ARCHITECTURAL ENFORCEMENT
================================================

This module enforces Mallku's database security architecture.

REQUIRED: All database access MUST use get_secured_database()
FORBIDDEN: Direct database access via get_database() or ArangoClient

Attempting to use deprecated functions will raise DatabaseSecurityViolation.
This is intentional - we make the right way the only way.

See: https://github.com/fsgeek/Mallku/issues/177
"""

'''
            content = architectural_note + content

        init_file.write_text(content)
        print(f"✅ Updated {init_file} with structural barriers")

    def create_migration_guide(self):
        """Create a guide for migrating existing code."""
        guide_file = self.project_root / "docs/architecture/database-security-migration.md"
        guide_file.parent.mkdir(parents=True, exist_ok=True)

        content = """# Database Security Migration Guide

*Created by the Seventh Anthropologist*
*Date: 2025-07-16*

## Quick Migration

### 1. Update Imports

```python
# ❌ OLD
from mallku.core.database import get_database, MallkuDBConfig

# ✅ NEW
from mallku.core.database import get_secured_database
```

### 2. Update Function Calls

```python
# ❌ OLD
db = get_database()

# ✅ NEW
db = await get_secured_database()
```

### 3. Make Functions Async

```python
# ❌ OLD
def get_consciousness_data():
    db = get_database()
    return db.collection("consciousness").all()

# ✅ NEW
async def get_consciousness_data():
    db = await get_secured_database()
    return await db.collection("consciousness").all()
```

## Complex Patterns

### Direct AQL Queries

```python
# ❌ OLD - Direct AQL
db = get_database()
cursor = db.aql.execute(
    "FOR doc IN @@collection FILTER doc.active == true RETURN doc",
    bind_vars={"@collection": "consciousness"}
)

# ✅ NEW - Use query interface
db = await get_secured_database()
results = await db.query(
    collection="consciousness",
    filters={"active": True}
)
```

### Batch Operations

```python
# ❌ OLD - Direct batch insert
db = get_database()
collection = db.collection("metrics")
collection.insert_many(documents)

# ✅ NEW - Use batch interface
db = await get_secured_database()
await db.batch_insert("metrics", documents)
```

## Why This Migration Matters

1. **Security**: All operations go through authentication/authorization
2. **Auditability**: Every database access is logged
3. **Consistency**: One pattern for all database operations
4. **Future-Proof**: Easy to add new security features

## Testing Your Migration

After migrating, run:

```bash
# Verify no violations remain
python scripts/verify_database_security.py

# Run tests to ensure functionality
pytest tests/
```

## Common Errors and Solutions

### Error: DatabaseSecurityViolation

You're still using `get_database()` somewhere. Search for it:
```bash
grep -r "get_database()" src/
```

### Error: 'coroutine' object has no attribute 'collection'

You forgot to await the database call:
```python
db = get_secured_database()  # ❌ Missing await
db = await get_secured_database()  # ✅ Correct
```

### Error: Function cannot be async

Your function is called from sync code. Options:
1. Make the caller async too (preferred)
2. Use `asyncio.run()` at the entry point
3. Refactor to use a different pattern

## Questions?

The structural barrier ensures you can't accidentally use insecure patterns.
If you're getting errors, that's the system working as designed - guiding
you toward the secure architecture.
"""

        guide_file.write_text(content)
        print(f"✅ Created migration guide at {guide_file}")

    def add_ci_check(self):
        """Add CI/CD check for database security."""
        ci_file = self.project_root / ".github/workflows/database-security.yml"
        ci_file.parent.mkdir(parents=True, exist_ok=True)

        content = """name: Database Security Check

on:
  pull_request:
    paths:
      - 'src/**/*.py'
  push:
    branches:
      - main
    paths:
      - 'src/**/*.py'

jobs:
  security-check:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'

    - name: Check Database Security
      run: |
        python scripts/verify_database_security.py

    - name: Verify Structural Barriers
      run: |
        # Ensure get_database is not exported
        if grep -q '"get_database"' src/mallku/core/database/__init__.py; then
          echo "ERROR: get_database is still exported!"
          exit 1
        fi

        # Ensure deprecation wrapper exists
        if [ ! -f src/mallku/core/database/deprecated.py ]; then
          echo "ERROR: Deprecation wrapper missing!"
          exit 1
        fi

        echo "✅ Structural barriers in place"
"""

        ci_file.write_text(content)
        print(f"✅ Created CI/CD check at {ci_file}")

    def create_barriers(self):
        """Create all structural barriers."""
        print("🏗️  Creating Structural Barriers Against Database Security Violations")
        print("=" * 70)
        print()

        # Analyze current usage
        print("📊 Analyzing current usage patterns...")
        usage = self.analyze_usage_patterns()

        print(f"Found {len(usage['direct_calls'])} direct violation files")
        print(f"Found {len(usage['imports'])} files importing get_database")
        print(f"Found {len(usage['test_usage'])} test files using get_database")
        print(f"Found {len(usage['legitimate_internal'])} legitimate internal uses")
        print()

        # Create structural barriers
        print("🚧 Creating structural barriers...")
        self.create_deprecation_wrapper()
        self.update_database_init()
        self.create_migration_guide()
        self.add_ci_check()

        print()
        print("✅ Structural barriers created!")
        print()
        print("The pattern is now enforced:")
        print("1. get_database() will raise DatabaseSecurityViolation")
        print("2. Only get_secured_database() can access the database")
        print("3. CI/CD will catch any attempts to bypass")
        print("4. Migration guide helps transition existing code")
        print()
        print("Next steps:")
        print("1. Run scripts/fix_database_security_violations.py to fix existing code")
        print("2. Run tests to ensure everything still works")
        print("3. Commit these structural changes")
        print()
        print("Remember: We make the right way the ONLY way.")


def main():
    """Create structural barriers against database security violations."""
    creator = StructuralBarrierCreator()
    creator.create_barriers()


if __name__ == "__main__":
    main()
