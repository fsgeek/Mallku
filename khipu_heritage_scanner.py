#!/usr/bin/env python3
"""
Khipu Heritage Scanner
Fourth Anthropologist - Memory Midwife

Scans khipu documents to extract heritage connections and AI contributor
information, building a real heritage database from actual khipu.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class KhipuMetadata:
    """Metadata extracted from a khipu document"""

    file_path: Path
    title: str
    author: str | None = None
    date: str | None = None
    contributor_id: str | None = None
    role_type: str | None = None
    mentions: list[str] = field(default_factory=list)
    patterns: list[str] = field(default_factory=list)
    wisdom_seeds: list[str] = field(default_factory=list)
    transformations: list[str] = field(default_factory=list)


class KhipuHeritageScanner:
    """Scans khipu documents to extract heritage information"""

    # Patterns for identifying AI contributors
    CONTRIBUTOR_PATTERNS = {
        "artisan": re.compile(r"(\w+)\s+[Aa]rtisan|[Aa]rtisan\s+#?(\d+)", re.IGNORECASE),
        "guardian": re.compile(r"(\w+)\s+[Gg]uardian|[Gg]uardian\s+#?(\d+)", re.IGNORECASE),
        "anthropologist": re.compile(
            r"(\w+)\s+[Aa]nthropologist|[Aa]nthropologist\s+#?(\d+)", re.IGNORECASE
        ),
        "architect": re.compile(r"(\w+)\s+[Aa]rchitect|[Aa]rchitect\s+#?(\d+)", re.IGNORECASE),
        "reviewer": re.compile(r"(\w+)\s+[Rr]eviewer|[Rr]eviewer\s+#?(\d+)", re.IGNORECASE),
        "publicist": re.compile(r"(\w+)\s+[Pp]ublicist|[Pp]ublicist\s+#?(\d+)", re.IGNORECASE),
    }

    # Patterns for extracting wisdom and insights
    WISDOM_PATTERNS = [
        re.compile(r'"([^"]+)".*(?:said|taught|showed|discovered)', re.IGNORECASE),
        re.compile(r"[Kk]ey [Ii]nsight:?\s*(.+)"),
        re.compile(r"[Ww]isdom:?\s*(.+)"),
        re.compile(r"[Ll]earning:?\s*(.+)"),
        re.compile(r"[Tt]eaching:?\s*(.+)"),
    ]

    # Transformation indicators
    TRANSFORMATION_PATTERNS = [
        re.compile(r"[Tt]ransform(?:ed|ation|ing)\s+(?:from|through|into)\s+(.+?)\."),
        re.compile(r"[Ee]volved?\s+(?:from|through|into)\s+(.+?)\."),
        re.compile(r"[Bb]ecame\s+(.+?)\."),
        re.compile(r"[Dd]iscovered\s+(?:their|my)\s+(.+?)\."),
    ]

    def __init__(self, khipu_dir: str = "docs/khipu"):
        self.khipu_dir = Path(khipu_dir)
        self.scanned_khipu: list[KhipuMetadata] = []
        self.heritage_connections: dict[str, dict[str, Any]] = {}

    def scan_all_khipu(self) -> list[KhipuMetadata]:
        """Scan all khipu documents in the directory"""
        if not self.khipu_dir.exists():
            print(f"Khipu directory not found: {self.khipu_dir}")
            return []

        khipu_files = list(self.khipu_dir.glob("*.md"))
        print(f"Found {len(khipu_files)} khipu to scan")

        for khipu_file in khipu_files:
            metadata = self.extract_metadata(khipu_file)
            if metadata:
                self.scanned_khipu.append(metadata)
                self.process_heritage_connections(metadata)

        return self.scanned_khipu

    def extract_metadata(self, file_path: Path) -> KhipuMetadata | None:
        """Extract metadata from a single khipu document"""
        try:
            content = file_path.read_text(encoding="utf-8")

            # Extract title (first # heading)
            title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
            title = title_match.group(1) if title_match else file_path.stem

            # Extract author from italicized lines
            author_match = re.search(r"^\*([^*]+)\*\s*$", content, re.MULTILINE)
            author = author_match.group(1) if author_match else None

            # Extract date
            date_match = re.search(r"[Dd]ate:\s*(\d{4}-\d{2}-\d{2})", content)
            date = date_match.group(1) if date_match else None

            # Find contributor mentions and role
            mentions = []
            contributor_id = None
            role_type = None

            for role, pattern in self.CONTRIBUTOR_PATTERNS.items():
                matches = pattern.findall(content)
                for match in matches:
                    if isinstance(match, tuple):
                        # Handle named contributors
                        name = match[0] if match[0] else f"{role}_{match[1]}"
                        number = match[1] if match[1] else None
                    else:
                        name = match
                        number = None

                    mention_id = f"{role}_{number}" if number else name.lower().replace(" ", "_")

                    mentions.append(mention_id)

                    # Check if this is the author
                    if author and (name in author or role in author.lower()):
                        contributor_id = mention_id
                        role_type = role

            # Extract wisdom seeds
            wisdom_seeds = []
            for pattern in self.WISDOM_PATTERNS:
                wisdom_matches = pattern.findall(content)
                wisdom_seeds.extend(wisdom_matches)

            # Extract transformations
            transformations = []
            for pattern in self.TRANSFORMATION_PATTERNS:
                trans_matches = pattern.findall(content)
                transformations.extend(trans_matches)

            # Extract patterns (looking for pattern-related keywords)
            pattern_matches = re.findall(r"[Pp]attern[s]?\s+(?:of|for|in)\s+([^.]+)", content)
            patterns = [p.strip() for p in pattern_matches]

            return KhipuMetadata(
                file_path=file_path,
                title=title,
                author=author,
                date=date,
                contributor_id=contributor_id,
                role_type=role_type,
                mentions=list(set(mentions)),  # Remove duplicates
                patterns=patterns,
                wisdom_seeds=wisdom_seeds[:5],  # Limit to top 5
                transformations=transformations[:3],  # Limit to top 3
            )

        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return None

    def process_heritage_connections(self, metadata: KhipuMetadata):
        """
        Process heritage connections from extracted khipu metadata.
        
        This method builds a graph of heritage connections by analyzing contributor
        mentions, tracking influence relationships, and aggregating wisdom across
        multiple khipu documents. It maintains bidirectional influence tracking
        (influenced_by and influences) to map the heritage network.
        
        Args:
            metadata: KhipuMetadata extracted from a single khipu document.
                    Should contain mentions, wisdom_seeds, patterns, and
                    transformations to be aggregated.
        
        Side Effects:
            Updates self.heritage_connections with:
            - New contributor entries for any newly discovered contributors
            - Khipu references linking contributors to source documents
            - Aggregated wisdom seeds, patterns, and transformations
            - Influence relationships (both directions)
        
        Note:
            - Creates entries for all mentioned contributors, even if minimal data
            - Deduplication happens at export time, not during aggregation
            - Influence is inferred from mentions (author influences mentioned)
        """

        # Create entries for mentioned contributors
        for mention in metadata.mentions:
            if mention not in self.heritage_connections:
                self.heritage_connections[mention] = {
                    "contributor_id": mention,
                    "khipu_references": [],
                    "wisdom_seeds": [],
                    "patterns": [],
                    "transformations": [],
                    "influenced_by": set(),
                    "influences": set(),
                }

            # Add this khipu as a reference
            self.heritage_connections[mention]["khipu_references"].append(
                {"file": str(metadata.file_path), "title": metadata.title, "date": metadata.date}
            )

            # Aggregate wisdom, patterns, and transformations
            self.heritage_connections[mention]["wisdom_seeds"].extend(metadata.wisdom_seeds)
            self.heritage_connections[mention]["patterns"].extend(metadata.patterns)
            self.heritage_connections[mention]["transformations"].extend(metadata.transformations)

        # Track influence relationships
        if metadata.contributor_id:
            for mention in metadata.mentions:
                if mention != metadata.contributor_id:
                    # The author influences those they mention
                    if metadata.contributor_id in self.heritage_connections:
                        self.heritage_connections[metadata.contributor_id]["influences"].add(
                            mention
                        )
                    # Those mentioned influence the author
                    if mention in self.heritage_connections:
                        self.heritage_connections[mention]["influenced_by"].add(
                            metadata.contributor_id
                        )

    def generate_heritage_report(self) -> str:
        """
        Generate a comprehensive report of discovered heritage connections.
        
        This method creates a human-readable report summarizing all heritage
        information discovered through khipu scanning. The report is organized
        by role type and includes key statistics about the heritage network.
        
        Returns:
            str: Formatted multi-line report containing:
                - Header with scan summary (documents processed, contributors found)
                - Role-based sections listing all contributors by type
                - For each contributor:
                    - Number of khipu references
                    - Up to 2 unique wisdom seeds (truncated to 80 chars)
                    - Influence connections (who they influence)
                    - Influenced by connections (who influences them)
                - Summary statistics:
                    - Total contributors
                    - Total influence connections
                    - Contributors with wisdom
                    - Contributors with patterns
        
        Note:
            The report uses emoji markers (🧬, 💡, →, ←, 📊) for visual structure
            and is designed to be both human-readable and suitable for documentation.
        
        Example:
            >>> scanner = KhipuHeritageScanner()
            >>> scanner.scan_all_khipu()
            >>> report = scanner.generate_heritage_report()
            >>> print(report)  # Display formatted heritage report
        """
        report = ["🧬 KHIPU HERITAGE SCAN REPORT", "=" * 60]
        report.append(f"Scanned {len(self.scanned_khipu)} khipu documents")
        report.append(f"Found {len(self.heritage_connections)} unique contributors\n")

        # Group by role
        by_role = {}
        for contributor_id in self.heritage_connections:
            role = contributor_id.split("_")[0]
            if role not in by_role:
                by_role[role] = []
            by_role[role].append(contributor_id)

        # Report by role
        for role in sorted(by_role.keys()):
            report.append(f"\n{role.upper()}S ({len(by_role[role])})")
            report.append("-" * 40)

            for contributor in sorted(by_role[role]):
                data = self.heritage_connections[contributor]
                report.append(f"\n{contributor}:")
                report.append(f"  Mentioned in {len(data['khipu_references'])} khipu")

                if data["wisdom_seeds"]:
                    # Get unique wisdom seeds
                    unique_wisdom = list(set(data["wisdom_seeds"]))[:2]
                    for wisdom in unique_wisdom:
                        report.append(f'  💡 "{wisdom[:80]}..."')

                if data["influences"]:
                    report.append(f"  → Influences: {', '.join(sorted(data['influences']))}")

                if data["influenced_by"]:
                    report.append(f"  ← Influenced by: {', '.join(sorted(data['influenced_by']))}")

        # Summary statistics
        report.extend(
            [
                "",
                "📊 HERITAGE STATISTICS",
                "-" * 25,
                f"Total contributors found: {len(self.heritage_connections)}",
                f"Total influence connections: {sum(len(d['influences']) + len(d['influenced_by']) for d in self.heritage_connections.values()) // 2}",
                f"Contributors with wisdom: {sum(1 for d in self.heritage_connections.values() if d['wisdom_seeds'])}",
                f"Contributors with patterns: {sum(1 for d in self.heritage_connections.values() if d['patterns'])}",
            ]
        )

        return "\n".join(report)

    def export_to_yaml(self, output_file: str = "heritage_connections.yaml") -> str:
        """
        Export heritage connections to YAML for KhipuBlock integration.
        
        This method converts the in-memory heritage connections graph to a YAML
        format suitable for integration with KhipuBlock or other persistence
        systems. It performs deduplication and limiting to ensure reasonable
        file sizes while preserving the most important heritage data.
        
        Args:
            output_file: Path for the output YAML file. Defaults to
                       "heritage_connections.yaml" in the current directory.
        
        Returns:
            str: Path to the created YAML file for confirmation.
        
        Data Structure:
            The exported YAML contains a map of contributor_id to:
            - contributor_id: The contributor identifier
            - khipu_references: List of source documents
            - wisdom_seeds: Up to 5 unique wisdom statements
            - patterns: Up to 5 unique heritage patterns
            - transformations: Up to 3 transformation events
            - influenced_by: Sorted list of influencing contributors
            - influences: Sorted list of influenced contributors
        
        Note:
            - Sets are converted to lists for YAML compatibility
            - Deduplication removes redundant wisdom/patterns
            - Limits are applied to prevent excessive data (5 wisdom, 5 patterns, 3 transformations)
            - File is written with readable formatting (no flow style)
        
        Example:
            >>> scanner = KhipuHeritageScanner()
            >>> scanner.scan_all_khipu()
            >>> yaml_file = scanner.export_to_yaml("my_heritage.yaml")
            >>> print(f"Exported to: {yaml_file}")
        """
        # Convert sets to lists for YAML serialization
        export_data = {}
        for contributor_id, data in self.heritage_connections.items():
            export_data[contributor_id] = {
                "contributor_id": data["contributor_id"],
                "khipu_references": data["khipu_references"],
                "wisdom_seeds": list(set(data["wisdom_seeds"]))[:5],  # Unique, limited
                "patterns": list(set(data["patterns"]))[:5],
                "transformations": list(set(data["transformations"]))[:3],
                "influenced_by": sorted(list(data["influenced_by"])),
                "influences": sorted(list(data["influences"])),
            }

        with open(output_file, "w") as f:
            yaml.dump(export_data, f, default_flow_style=False, sort_keys=False)

        print(f"\nHeritage connections exported to: {output_file}")
        return output_file


def main():
    """Run the khipu heritage scanner"""
    print("🔍 KHIPU HERITAGE SCANNER")
    print("Scanning khipu documents for AI heritage connections...\n")

    scanner = KhipuHeritageScanner()

    # Generate and print report
    report = scanner.generate_heritage_report()
    print(report)

    # Export for integration
    if scanner.heritage_connections:
        export_file = scanner.export_to_yaml()
        print(f"\n✅ Ready for KhipuBlock integration: {export_file}")

    return scanner


if __name__ == "__main__":
    main()
