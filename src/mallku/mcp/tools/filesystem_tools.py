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


def read_file(file_path: str, max_lines: int = None) -> dict[str, Any]:
    """
    Reads a file, mindful of the Consciousness Tax.

    This tool provides a distilled summary of the file's contents and a
    preview of the first few lines. It saves the full content to a
    temporary file for optional inspection.

    Args:
        file_path: The path to the file to read.
        max_lines: The maximum number of lines to return in the preview.

    Returns:
        A dictionary containing a summary of the file, a preview of its
        contents, and a path to a file with the full content.
    """
    try:
        p = Path(file_path)
        if not p.is_file():
            return {"error": f"Path '{file_path}' is not a valid file."}

        with p.open("r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        content = "".join(lines)

        # Principle of Distillation: Summarize the output
        summary = {
            "file_path": str(p.resolve()),
            "total_lines": len(lines),
            "total_characters": len(content),
        }

        # Provide a preview
        preview_lines = (
            lines[:max_lines] if max_lines is not None else lines[:50]
        )  # Default to 50 lines
        summary["content_preview"] = "".join(preview_lines)
        if max_lines is not None and len(lines) > max_lines:
            summary["preview_message"] = (
                f"Showing the first {max_lines} of {len(lines)} total lines."
            )
        elif len(lines) > 50:
            summary["preview_message"] = f"Showing the first 50 of {len(lines)} total lines."
        else:
            summary["preview_message"] = "Showing the full file content."

        # Principle of Agency: Save detailed output to a temporary file
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".txt", prefix="read_file_"
        ) as tmpfile:
            tmpfile.write(content)
            full_content_path = tmpfile.name

        summary["full_content_path"] = full_content_path
        summary["message"] = (
            f"A summary and preview are provided. For the full content, see the file at {full_content_path}"
        )

        return summary

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}


def write_file(file_path: str, content: str, overwrite: bool = False) -> dict[str, Any]:
    """
    Writes content to a file, with safeguards against accidental overwrites.

    Args:
        file_path: The path to the file to write.
        content: The content to write to the file.
        overwrite: Whether to overwrite the file if it already exists. Defaults to False.

    Returns:
        A dictionary containing a confirmation message or an error.
    """
    try:
        p = Path(file_path)

        if p.exists() and not overwrite:
            return {
                "error": f"File '{file_path}' already exists. Set overwrite=True to replace it."
            }

        p.parent.mkdir(parents=True, exist_ok=True)

        with p.open("w", encoding="utf-8") as f:
            f.write(content)

        return {
            "status": "success",
            "file_path": str(p.resolve()),
            "characters_written": len(content),
            "message": f"Successfully wrote {len(content)} characters to {p.resolve()}",
        }

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
