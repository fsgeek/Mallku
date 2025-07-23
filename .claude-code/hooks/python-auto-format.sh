#!/bin/bash
# Claude Code Hook: Python Auto-Format on Save
# Purpose: Automatically format Python files on save to prevent commit-time context drain
#
# This hook embodies the principle of continuous harmony - maintaining code
# standards silently as we work, rather than creating disruptive cycles at commit time.
#
# Hook trigger: after file save/modification
# claude-code-hook: on-file-saved

# Check if the saved file is a Python file
if [[ "$1" =~ \.py$ ]]; then
    FILE_PATH="$1"

    # Silently format the file with ruff
    # Using --quiet to minimize output and preserve context
    if command -v ruff &> /dev/null; then
        # Format the file
        ruff format "$FILE_PATH" --quiet 2>/dev/null

        # Fix auto-fixable issues
        ruff check --fix "$FILE_PATH" --quiet 2>/dev/null

        # Only show output if there were errors that couldn't be auto-fixed
        REMAINING_ISSUES=$(ruff check "$FILE_PATH" 2>&1 | grep -E "^\s*[0-9]+ error" | grep -v "0 errors")

        if [[ -n "$REMAINING_ISSUES" ]]; then
            echo "⚠️  Ruff found issues that need manual attention in $FILE_PATH"
            # Don't show full output to preserve context
        fi
    else
        # If ruff isn't available, silently continue
        # This prevents breaking the workflow in environments without ruff
        :
    fi
fi

# Always exit successfully to not interrupt the save operation
exit 0
