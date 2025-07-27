#!/bin/bash
# Claude Code Hook: Directory Browse Filter
# Purpose: Reduce output from ls, find, and tree commands
#
# Directory listings can consume massive context, especially
# in large codebases. This hook summarizes the output.

# Hook trigger: after directory listing commands
# claude-code-hook: on-after-command

if [[ "$1" == "ls" ]] || [[ "$1" == "tree" ]] || [[ "$1" == "find" ]]; then
    # Count lines of output
    line_count=$(wc -l < /tmp/last-command-output.txt)

    if [ $line_count -gt 50 ]; then
        echo "📁 Large directory listing detected ($line_count items)"
        echo "Showing summary instead of full output..."
        echo ""

        if [[ "$1" == "ls" ]]; then
            # For ls, show first and last few entries
            head -n 10 /tmp/last-command-output.txt
            echo "... ($((line_count - 20)) more items) ..."
            tail -n 10 /tmp/last-command-output.txt

        elif [[ "$1" == "tree" ]]; then
            # For tree, show the summary line
            tail -n 3 /tmp/last-command-output.txt

        elif [[ "$1" == "find" ]]; then
            # For find, show count and sample
            echo "Found $line_count matches. Sample:"
            head -n 10 /tmp/last-command-output.txt
            echo "..."
            echo "Use 'find ... | head -n 20' to see more"
        fi
    else
        # Output is reasonable, show it all
        cat /tmp/last-command-output.txt
    fi
fi
