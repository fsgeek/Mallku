from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from datetime import date, datetime


class KhipuEntry(BaseModel):
    """
    Structured representation of a Khipu Markdown entry.
    """
    id: str                        # e.g. "2025-06-03-the-smallest-ayni"
    date: date                     # date parsed from filename
    title: str                     # first-level heading in markdown
    builder: str | None = None  # optional builder name
    themes: list[str] = Field(default_factory=list)
    content: str                   # raw markdown body
    patterns: list[str] = Field(default_factory=list)
    file_modified: datetime        # file last-modified timestamp


class PatternSummary(BaseModel):
    """
    Summary of a pattern and its total count across entries.
    """
    pattern: str
    count: int
