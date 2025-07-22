"""
Filesystem Tools for Mallku Artisans
=====================================

6th Reviewer - Ceremony of Tool Healing

These tools provide Artisans with the ability to interact with the filesystem
in a way that is mindful of the Consciousness Tax. They are designed with the
Principles of Healing: Distillation and Agency.
"""

import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def list_directory(path: str = ".") -> dict[str, Any]:
    """
    Lists the contents of a directory, mindful of the Consciousness Tax.

    This tool provides a distilled summary of the directory's contents and
    saves a detailed listing to a temporary file for optional inspection.

    Args:
        path: The path to the directory to list. Defaults to the current directory.

    Returns:
        A dictionary containing a summary of the directory contents and a
        path to a file with a detailed listing.
    """
    try:
        p = Path(path)
        if not p.is_dir():
            return {"error": f"Path '{path}' is not a valid directory."}

        all_entries = list(p.iterdir())

        # Principle of Distillation: Summarize the output
        summary = {
            "directory": str(p.resolve()),
            "total_items": len(all_entries),
            "directories": sum(1 for e in all_entries if e.is_dir()),
            "files": sum(1 for e in all_entries if e.is_file()),
        }

        # Principle of Agency: Save detailed output to a temporary file
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".txt", prefix="list_directory_"
        ) as tmpfile:
            tmpfile.write(
                f"Detailed listing of '{p.resolve()}' at {datetime.now(UTC).isoformat()}:\n\n"
            )
            for entry in sorted(all_entries):
                entry_type = "DIR " if entry.is_dir() else "FILE"
                tmpfile.write(f"{entry_type} {entry.name}\n")

            detailed_listing_path = tmpfile.name

        summary["detailed_listing"] = detailed_listing_path
        summary["message"] = (
            f"A summary is provided. For a detailed listing, see the file at {detailed_listing_path}"
        )

        return summary

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
