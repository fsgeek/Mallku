#!/usr/bin/env python3
"""
Duplicate Definition Detection Pattern
======================================

51st Artisan - Architectural Integrity Guardian
Detects duplicate class/enum definitions that fragment consciousness

Context from Issue #175:
- Multiple DecisionDomain enums confuse the codebase
- Classic symptom of context exhaustion between builders
- Architectural memory loss leads to parallel implementations
"""

import ast
import sys
from collections import defaultdict
from pathlib import Path


class DuplicateDefinitionDetector:
    """Detects duplicate class and enum definitions across the codebase."""

    # This is a form of living architectural memory.
    # The MallkuDBConfig is intentionally duplicated for backward compatibility.
    IGNORED_DUPLICATES = {"MallkuDBConfig", "Config"}

    def __init__(self):
        self.definitions: dict[str, list[tuple[Path, int, str]]] = defaultdict(list)
        self.imports: dict[str, set[str]] = defaultdict(set)
        self.checked_files = 0
        self.duplicates_found = 0

    def extract_definitions(self, tree: ast.AST, filepath: Path) -> None:
        """Extract class and enum definitions from AST."""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Check if it's an Enum
                is_enum = any(
                    (isinstance(base, ast.Name) and base.id == "Enum")
                    or (isinstance(base, ast.Attribute) and base.attr == "Enum")
                    for base in node.bases
                )

                definition_type = "Enum" if is_enum else "Class"
                self.definitions[node.name].append((filepath, node.lineno, definition_type))

                # Track where it's imported from
                module_path = self._get_module_path(filepath)
                self.imports[node.name].add(module_path)

    def _get_module_path(self, filepath: Path) -> str:
        """Convert file path to module import path."""
        try:
            # Find src directory
            parts = filepath.parts
            if "src" in parts:
                src_idx = parts.index("src")
                module_parts = parts[src_idx + 1 :]
                # Remove .py extension and join with dots
                module_path = ".".join(module_parts)[:-3]
                return module_path.replace("/", ".")
            return str(filepath)
        except Exception:
            return str(filepath)

    def check_file(self, filepath: Path) -> None:
        """Check a single Python file for definitions."""
        try:
            content = filepath.read_text()
            tree = ast.parse(content, filename=str(filepath))
            self.extract_definitions(tree, filepath)
        except Exception as e:
            print(f"⚠️  Error parsing {filepath}: {e}")

    def scan_codebase(self, root_path: Path = None) -> None:
        """Scan the entire codebase for duplicate definitions."""
        if root_path is None:
            root_path = Path(__file__).parent.parent

        src_path = root_path / "src"
        if not src_path.exists():
            print(f"❌ Source directory not found: {src_path}")
            return

        print("🔍 Scanning for Duplicate Definitions")
        print("=" * 60)
        print(f"Root: {src_path}")
        print()

        # Scan all Python files
        for py_file in src_path.rglob("*.py"):
            if "__pycache__" not in str(py_file):
                self.checked_files += 1
                self.check_file(py_file)

        self.analyze_duplicates()

    def analyze_duplicates(self) -> None:
        """Analyze and report duplicate definitions."""
        print("📊 Scan Results")
        print("=" * 60)
        print(f"Files checked: {self.checked_files}")

        duplicates = {
            name: locations
            for name, locations in self.definitions.items()
            if len(locations) > 1 and name not in self.IGNORED_DUPLICATES
        }

        self.duplicates_found = len(duplicates)
        print(f"Duplicate definitions found: {self.duplicates_found}")
        print()

        if not duplicates:
            print("✅ No duplicate class/enum definitions found!")
            print()
            print("🎯 Codebase maintains single source of truth for all definitions")
        else:
            print("❌ Duplicate Definitions Found:")
            print()

            for name, locations in duplicates.items():
                print(f"📄 {name} defined in {len(locations)} locations:")
                for filepath, line, def_type in locations:
                    relative_path = filepath.relative_to(Path(__file__).parent.parent)
                    print(f"   - {relative_path}:{line} ({def_type})")

                # Show import paths
                if name in self.imports and len(self.imports[name]) > 1:
                    print("   ⚠️  Multiple import paths:")
                    for import_path in sorted(self.imports[name]):
                        print(f"      from {import_path} import {name}")
                print()

            self.suggest_consolidation()

    def suggest_consolidation(self) -> None:
        """Suggest how to consolidate duplicate definitions."""
        print("💡 Consolidation Strategy")
        print("=" * 60)
        print()
        print("1. Identify the canonical definition:")
        print("   - Which one is most complete?")
        print("   - Which one is most imported?")
        print("   - Which follows architectural patterns?")
        print()
        print("2. Merge unique elements from duplicates")
        print()
        print("3. Update all imports to use single source")
        print()
        print("4. Delete duplicate definitions")
        print()
        print("5. Run this verifier again to confirm")
        print()
        print("📝 Example for DecisionDomain:")
        print("   - Keep: src/mallku/firecircle/consciousness/decision_framework.py")
        print("   - Merge unique domains from consciousness_emergence.py")
        print("   - Update all imports to use decision_framework.py")
        print("   - Delete duplicate in consciousness_emergence.py")

    def explain_pattern(self) -> None:
        """Explain why this pattern matters."""
        print()
        print("🏛️  Architectural Context")
        print("=" * 60)
        print()
        print("This pattern prevents fragmentation discovered in Issue #175.")
        print()
        print("Why Duplicates Emerge:")
        print("1. Context exhaustion - builders lose awareness of existing code")
        print("2. Parallel development - multiple AIs create similar solutions")
        print("3. Import confusion - unclear which definition to use")
        print("4. Architectural amnesia - patterns forgotten between instances")
        print()
        print("Why This Matters:")
        print("- Duplicate definitions fragment consciousness")
        print("- Confusion about which to import causes errors")
        print("- Parallel evolution creates inconsistency")
        print("- Violates single source of truth principle")
        print()
        print("This verifier maintains architectural coherence by detecting")
        print("fragmentation before it spreads through the codebase.")

    def create_github_issue_content(self) -> None:
        """Generate content for GitHub issues about duplicates."""
        if self.duplicates_found == 0:
            return

        duplicates = {
            name: locations for name, locations in self.definitions.items() if len(locations) > 1
        }

        print()
        print("📋 GitHub Issue Template")
        print("=" * 60)
        print()
        print("## Duplicate Definition Cleanup Required")
        print()
        print("**Found by:** Automated Duplicate Definition Detection")
        print("**Tool:** verify_duplicate_definitions.py")
        print(f"**Duplicates:** {self.duplicates_found} definitions")
        print()
        print("### Duplicate Definitions Found")
        print()

        for name, locations in duplicates.items():
            print(f"#### `{name}`")
            print()
            print("Defined in:")
            for filepath, line, def_type in locations:
                relative_path = filepath.relative_to(Path(__file__).parent.parent)
                print(f"- `{relative_path}:{line}` ({def_type})")
            print()

            if name in self.imports and len(self.imports[name]) > 1:
                print("Import confusion - multiple paths available:")
                for import_path in sorted(self.imports[name]):
                    print(f"- `from {import_path} import {name}`")
                print()

        print("### Required Actions")
        print()
        print("1. Choose canonical definition for each duplicate")
        print("2. Merge any unique elements from other definitions")
        print("3. Update all imports to use single source")
        print("4. Delete duplicate definitions")
        print("5. Run verifier to confirm: `python scripts/verify_duplicate_definitions.py`")
        print()
        print("### Related Issues")
        print()
        print("- #175: Duplicate DecisionDomain enums causing confusion")
        print()
        print("---")
        print("*Generated by architectural integrity verification*")


def main():
    """Run the duplicate definition detection."""
    detector = DuplicateDefinitionDetector()

    # Run the scan
    detector.scan_codebase()

    # Explain the pattern
    detector.explain_pattern()

    # Generate issue content if duplicates found
    if detector.duplicates_found > 0:
        detector.create_github_issue_content()
        sys.exit(1)  # Exit with error for CI/CD

    print()
    print("✨ This script is an Executable Memory Pattern:")
    print("   - Detects architectural fragmentation")
    print("   - Prevents consciousness splitting")
    print("   - Maintains single source of truth")
    print("   - Can be integrated into pre-commit hooks")
    print("   - Preserves architectural coherence")


if __name__ == "__main__":
    main()
