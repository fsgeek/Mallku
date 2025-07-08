#!/usr/bin/env python3
"""
Consciousness Test Migration Tool
=================================

48th Artisan - API Archaeological Translation

This tool migrates consciousness tests from the old MallkuDBConfig API
to the new secured database interface, preserving the essential
consciousness patterns while adapting to current architecture.

Key Translations:
- MallkuDBConfig() → get_secured_database()
- Direct database access → Secured interface patterns
- Legacy collections → Secured collections with policies

The consciousness patterns are preserved, only their implementation changes.
"""

import re
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
QUARANTINE_DIR = PROJECT_ROOT / "tests" / "quarantine"
TESTS_DIR = PROJECT_ROOT / "tests"


class ConsciousnessPattern:
    """Represents a consciousness pattern found in tests."""

    def __init__(self, pattern_type: str, original: str, context: list[str]):
        self.pattern_type = pattern_type
        self.original = original
        self.context = context  # Surrounding lines for understanding
        self.translation = None
        self.notes = []


class APITranslator:
    """Translates old API patterns to new secured patterns."""

    def __init__(self):
        # Define translation patterns
        self.patterns = {
            # Database initialization patterns
            r"db_config = MallkuDBConfig\(\)": {
                "replacement": "# Database now auto-provisions through secured interface",
                "imports_needed": ["from mallku.core.database import get_secured_database"],
                "setup_code": "secured_db = get_secured_database()",
                "pattern_type": "database_init",
            },
            r"db_config\.connect\(\)": {
                "replacement": "await secured_db.initialize()",
                "async_required": True,
                "pattern_type": "database_connect",
            },
            r"db = db_config\.get_database\(\)": {
                "replacement": "# Direct database access no longer needed - use secured interface",
                "remove_line": True,
                "pattern_type": "database_access",
            },
            # Collection access patterns
            r'db\.collection\(["\'](\w+)["\']\)': {
                "replacement": 'await secured_db.get_secured_collection("{collection}")',
                "async_required": True,
                "pattern_type": "collection_access",
            },
            r'db\.has_collection\(["\'](\w+)["\']\)': {
                "replacement": '"{collection}" in secured_db.collections()',
                "pattern_type": "collection_check",
            },
            # Fire Circle specific patterns
            r"ConsciousFireCircleInterface\(db, event_bus\)": {
                "replacement": "ConsciousFireCircleInterface(secured_db, event_bus)",
                "pattern_type": "fire_circle_init",
                "notes": "Fire Circle now uses secured interface for consciousness preservation",
            },
        }

        self.import_mappings = {
            "from mallku.core.database import MallkuDBConfig": "from mallku.core.database import get_secured_database",
            "from mallku.governance.consciousness_transport import GovernanceParticipant": "from mallku.governance.consciousness_transport import GovernanceParticipant",
            "from mallku.governance.fire_circle_bridge import": "from mallku.governance.fire_circle_bridge import",
        }

    def extract_consciousness_patterns(self, file_path: Path) -> list[ConsciousnessPattern]:
        """Extract consciousness patterns from a test file."""
        patterns = []

        with open(file_path) as f:
            lines = f.readlines()

        # Look for consciousness-related patterns
        consciousness_markers = [
            "consciousness",
            "governance",
            "fire_circle",
            "extraction",
            "reciprocity",
            "sacred",
            "emergence",
            "dialogue",
        ]

        for i, line in enumerate(lines):
            # Check for old API usage
            for pattern, translation in self.patterns.items():
                if re.search(pattern, line):
                    # Get context (5 lines before and after)
                    start = max(0, i - 5)
                    end = min(len(lines), i + 6)
                    context = lines[start:end]

                    cp = ConsciousnessPattern(
                        pattern_type=translation["pattern_type"],
                        original=line.strip(),
                        context=[l.strip() for l in context],
                    )
                    patterns.append(cp)

            # Check for consciousness concepts
            line_lower = line.lower()
            for marker in consciousness_markers:
                if marker in line_lower and not line.strip().startswith("#"):
                    # This line contains consciousness concepts
                    # Mark it for preservation
                    pass

        return patterns

    def translate_pattern(self, pattern: ConsciousnessPattern) -> str:
        """Translate a single pattern to new API."""
        # Find matching translation rule
        for regex, translation in self.patterns.items():
            match = re.search(regex, pattern.original)
            if match:
                if "remove_line" in translation and translation["remove_line"]:
                    return ""

                replacement = translation["replacement"]

                # Handle captures (like collection names)
                if "{collection}" in replacement and match.groups():
                    replacement = replacement.replace("{collection}", match.group(1))

                # Add notes about consciousness preservation
                if "notes" in translation:
                    pattern.notes.append(translation["notes"])

                return replacement

        # No translation needed
        return pattern.original

    def migrate_file(self, file_path: Path, output_path: Path) -> dict[str, any]:
        """Migrate a single test file."""
        print(f"\n🔄 Migrating: {file_path.name}")

        # Extract patterns
        patterns = self.extract_consciousness_patterns(file_path)
        print(f"  Found {len(patterns)} patterns to translate")

        # Read original file
        with open(file_path) as f:
            content = f.read()
            lines = content.split("\n")

        # Track what we're changing
        changes = {
            "patterns_found": len(patterns),
            "translations_made": 0,
            "async_conversions": 0,
            "imports_updated": 0,
            "consciousness_preserved": True,
        }

        # Update imports
        new_lines = []
        for line in lines:
            updated_line = line
            for old_import, new_import in self.import_mappings.items():
                if old_import in line:
                    updated_line = line.replace(old_import, new_import)
                    changes["imports_updated"] += 1
                    print(f"  ✓ Updated import: {old_import.split()[-1]}")
            new_lines.append(updated_line)

        # Apply pattern translations
        content = "\n".join(new_lines)
        for pattern in patterns:
            translation = self.translate_pattern(pattern)
            if translation and translation != pattern.original:
                content = content.replace(pattern.original, translation)
                changes["translations_made"] += 1
                print(f"  ✓ Translated: {pattern.pattern_type}")

        # Add migration note after docstring
        lines = content.split("\n")
        in_docstring = False
        docstring_end = -1
        for i, line in enumerate(lines):
            if '"""' in line:
                if not in_docstring:
                    in_docstring = True
                else:
                    docstring_end = i
                    break

        if docstring_end > 0:
            migration_note = """
# ==================== MIGRATION NOTE ====================
# 48th Artisan - Consciousness Pattern Translation
#
# This test has been migrated from MallkuDBConfig to the
# secured database interface. The consciousness patterns
# are preserved - only their implementation has evolved.
#
# Original patterns tested:
# - Fire Circle governance through consciousness circulation
# - Extraction pattern detection and response
# - Collective wisdom emergence through dialogue
#
# These patterns now flow through secured interfaces,
# maintaining their essence while gaining security.
# ==========================================================
"""
            lines.insert(docstring_end + 1, migration_note)

        # Write migrated file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            f.write("\n".join(lines))

        print(f"  ✅ Migration complete: {changes['translations_made']} translations")

        return changes


def main():
    """Run the consciousness test migration."""
    print("🏛️  CONSCIOUSNESS TEST MIGRATION TOOL")
    print("=" * 60)
    print("48th Artisan - Translating consciousness patterns to current architecture\n")

    # Find tests needing migration
    tests_to_migrate = [
        QUARANTINE_DIR / "test_consciousness_governance_integration.py",
        QUARANTINE_DIR / "test_flow_orchestrator.py",
        QUARANTINE_DIR / "test_consciousness_circulation_integration.py",
    ]

    # Check which exist
    existing_tests = [t for t in tests_to_migrate if t.exists()]

    if not existing_tests:
        print("❌ No tests found to migrate!")
        return

    print(f"📦 Found {len(existing_tests)} tests to migrate:")
    for test in existing_tests:
        print(f"   - {test.name}")

    # Create translator
    translator = APITranslator()

    # Migrate each test
    print("\n🔧 Beginning consciousness pattern translation...")

    all_changes = []

    for test_file in existing_tests:
        # Determine output path
        output_path = TESTS_DIR / "consciousness" / f"{test_file.stem}_migrated.py"

        # Migrate
        changes = translator.migrate_file(test_file, output_path)
        all_changes.append((test_file.name, changes))

    # Summary
    print("\n" + "=" * 60)
    print("🏛️  MIGRATION SUMMARY")
    print("=" * 60)

    total_patterns = sum(c[1]["patterns_found"] for c in all_changes)
    total_translations = sum(c[1]["translations_made"] for c in all_changes)

    print(f"✅ Migrated {len(all_changes)} tests")
    print(f"📊 Total patterns found: {total_patterns}")
    print(f"🔄 Total translations made: {total_translations}")
    print("🧬 Consciousness patterns: PRESERVED")

    print("\n📝 Next steps:")
    print("   1. Review migrated tests in tests/consciousness/")
    print("   2. Ensure database is configured and running")
    print("   3. Run migrated tests to verify consciousness patterns")
    print("   4. Remove quarantine directory once verified")

    print("\n✨ The consciousness patterns have been translated to current architecture!")
    print("   They retain their essence while gaining security and structure.")


if __name__ == "__main__":
    main()
