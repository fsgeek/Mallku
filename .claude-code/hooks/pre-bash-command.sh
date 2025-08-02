#!/bin/bash
# Claude Code Hook: Pre-bash command processing
# Purpose: Intercept commands before execution to add automation
#
# This hook helps preserve context by automating repetitive tasks
# before they consume valuable context window space.
#
# Hook trigger: PreToolUse for Bash
# Configured in: .claude-code/claude.json

# Get the command from parameters
COMMAND="$CLAUDE_TOOL_PARAMS"

# Check if this is a git commit command
if [[ "$COMMAND" =~ git[[:space:]]+commit ]]; then
    echo "🔄 Running pre-commit hooks before commit..."

    # Run pre-commit and capture results
    if ! uv run pre-commit run --all-files > /tmp/pre-commit-output.txt 2>&1; then
        echo "📝 Pre-commit hooks made changes, auto-staging modified files..."

        # Show only modified files, not full diffs
        echo "Modified files:"
        git diff --name-only

        # Stage the changes
        git add -u

        echo "✅ Changes staged. Proceeding with commit..."
    else
        echo "✅ Pre-commit checks passed"
    fi
fi

# Always allow the command to proceed
exit 0
