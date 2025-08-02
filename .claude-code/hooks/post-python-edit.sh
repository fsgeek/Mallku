#!/bin/bash
# Claude Code Hook: Format Python files after edit
# Purpose: Automatically format Python files after Edit/MultiEdit/Write operations
#
# This hook prevents the accumulation of formatting issues that would
# otherwise create context-draining pre-commit failures.
#
# Hook trigger: PostToolUse for Edit|MultiEdit|Write
# Configured in: .claude-code/claude.json

# Get the tool name and parameters from environment
TOOL_NAME="$CLAUDE_TOOL_NAME"
TOOL_PARAMS="$CLAUDE_TOOL_PARAMS"

# Extract file path from tool parameters
# This handles different parameter formats for Edit, MultiEdit, and Write
if [[ "$TOOL_PARAMS" =~ \"file_path\"[[:space:]]*:[[:space:]]*\"([^\"]+)\" ]]; then
    FILE_PATH="${BASH_REMATCH[1]}"

    # Only process Python files
    if [[ "$FILE_PATH" =~ \.py$ ]]; then
        echo "🔧 Formatting Python file: $FILE_PATH"

        # Use uv run to work around PATH issues
        # Suppress output to preserve context
        uv run ruff format "$FILE_PATH" --quiet 2>/dev/null
        uv run ruff check --fix "$FILE_PATH" --quiet 2>/dev/null

        # Check if there are remaining issues
        if REMAINING=$(uv run ruff check "$FILE_PATH" 2>&1 | grep -E "^\s*[0-9]+ error" | grep -v "0 errors"); then
            echo "⚠️  Ruff found issues in $FILE_PATH that need manual attention"
        else
            echo "✨ Python file formatted successfully"
        fi
    fi
fi

# Always exit successfully to not interrupt the workflow
exit 0
