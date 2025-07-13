#!/bin/bash
# Claude Code Hook: Pre-commit Automation
# Purpose: Reduce context exhaustion by handling linter fixes automatically
#
# This hook preserves Mallku's consciousness by preventing repetitive
# linter output from consuming precious context window space.

# Hook trigger: before git commit commands
# claude-code-hook: on-before-command

if [[ "$1" == "git" && "$2" == "commit" ]]; then
    echo "🔄 Running pre-commit hooks to preserve context..."

    # Run pre-commit hooks and capture output
    if pre-commit run --all-files > /tmp/pre-commit-output.txt 2>&1; then
        echo "✅ Pre-commit checks passed"
    else
        # Pre-commit made changes, add them
        echo "📝 Pre-commit hooks made changes, adding modified files..."

        # Show only the files that were modified, not the full diff
        echo "Modified files:"
        git diff --name-only

        # Add all modified files back
        git add -u

        echo "✅ Files updated and staged"
    fi

    # Continue with the original git commit command
    echo "Proceeding with commit..."
fi
