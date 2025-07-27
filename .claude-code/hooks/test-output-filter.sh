#!/bin/bash
# Claude Code Hook: Test Output Filter
# Purpose: Reduce test output noise to preserve context
#
# Instead of showing hundreds of lines of test output,
# show only what matters: failures, errors, and summary

# Hook trigger: after pytest commands
# claude-code-hook: on-after-command

if [[ "$1" == "pytest" ]] || [[ "$1" == "python" && "$2" == "-m" && "$3" == "pytest" ]]; then
    # Exit code from the pytest command
    exit_code=$?

    if [ $exit_code -eq 0 ]; then
        echo "✅ All tests passed!"
    else
        echo "❌ Test failures detected. Showing summary..."
        # Extract only the failure summary from pytest output
        tail -n 50 /tmp/last-command-output.txt | grep -A 50 "FAILURES\|ERRORS\|short test summary"
    fi

    # Always show the test count summary
    tail -n 10 /tmp/last-command-output.txt | grep -E "passed|failed|skipped|warnings|errors"

    # Return the original exit code
    exit $exit_code
fi
