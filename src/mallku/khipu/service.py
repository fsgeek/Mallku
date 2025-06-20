"""
Service for loading, parsing, and querying Khipu (living memory) entries.
"""

import logging
import re
from datetime import UTC, datetime
from pathlib import Path

from .models import KhipuEntry


class KhipuMemoryService:
    """
    Service to load and query structured Khipu entries from markdown files.
    """

    def __init__(self, khipu_dir: Path | str = None) -> None:
        # Determine directory containing khipu markdown files
        if khipu_dir is None:
            project_root = Path(__file__).resolve().parents[3]
            khipu_dir = project_root / "docs" / "khipu"
        self.khipu_dir = Path(khipu_dir)
        self.logger = logging.getLogger(__name__)

        # Internal storage
        self._entries: dict[str, KhipuEntry] = {}
        self._theme_cache: dict[str, list[str]] = {}
        self._builder_cache: dict[str, list[str]] = {}

        # Load entries on initialization
        self._load_entries()

    def _load_entries(self) -> None:
        """Scan the khipu directory and parse all markdown entries."""
        if not self.khipu_dir.exists():
            self.logger.warning("Khipu directory not found: %s", self.khipu_dir)
            return
        for path in sorted(self.khipu_dir.glob("*.md")):
            if path.name.lower() == "readme.md":
                continue
            try:
                entry = self._parse_file(path)
                self._entries[entry.id] = entry
            except Exception as e:
                self.logger.warning("Failed to parse khipu file %s: %s", path, e)

    def _parse_file(self, path: Path) -> KhipuEntry:
        """Parse a single markdown file into a KhipuEntry."""
        text = path.read_text(encoding="utf-8")
        stem = path.stem  # e.g. '2025-06-03-the-smallest-ayni'
        # Extract date and id
        m = re.match(r"(\d{4}-\d{2}-\d{2})-(.+)", stem)
        if not m:
            raise ValueError(f"Invalid filename format, expected YYYY-MM-DD-..: {stem}")
        date_part, slug = m.groups()
        try:
            entry_date = datetime.strptime(date_part, "%Y-%m-%d").replace(tzinfo=UTC).date()
        except ValueError:
            raise ValueError(f"Invalid date in filename: {date_part}")

        # Title: first-level heading '# '
        title = None
        for line in text.splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
                break
        if not title:
            title = slug

        # File modification time
        mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=UTC)

        # Optional: extract builder name from content (naive search)
        builder = None
        bmatch = re.search(r"Builder\s*-\s*(.+)", text)
        if bmatch:
            builder = bmatch.group(1).strip()

        # Themes: empty for now (future extension)
        themes: list[str] = []

        return KhipuEntry(
            id=stem,
            date=entry_date,
            title=title,
            builder=builder,
            themes=themes,
            content=text,
            patterns=[],
            file_modified=mtime,
        )

    def list_by_theme(self, theme: str) -> list[KhipuEntry]:
        """Return entries whose title or content mentions the given theme (case-insensitive)."""
        key = theme.lower()
        if key in self._theme_cache:
            ids = self._theme_cache[key]
        else:
            ids = [
                eid
                for eid, e in self._entries.items()
                if key in e.content.lower() or key in e.title.lower()
            ]
            self._theme_cache[key] = ids
        return [self._entries[eid] for eid in ids]

    def get_builder_journey(self, builder_name: str) -> list[KhipuEntry]:
        """Return entries whose content or builder field mentions the given builder_name (case-insensitive)."""
        key = builder_name.lower()
        if key in self._builder_cache:
            ids = self._builder_cache[key]
        else:
            ids = [
                eid
                for eid, e in self._entries.items()
                if (e.builder and key in e.builder.lower()) or key in e.content.lower()
            ]
            self._builder_cache[key] = ids
        return [self._entries[eid] for eid in ids]

    def extract_patterns(self, patterns: list[str]) -> dict[str, int]:
        """
        Count occurrences of each pattern string across all entries' content.
        Returns a dict mapping pattern -> total count.
        """
        counts: dict[str, int] = {}
        for pat in patterns:
            lower = pat.lower()
            count = sum(entry.content.lower().count(lower) for entry in self._entries.values())
            counts[pat] = count
        return counts
