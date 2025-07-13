#!/bin/bash
# Claude Code Hook: API Key Reminder
# Purpose: Remind about API key loading for Fire Circle operations
#
# The recurring pattern of forgetting load_api_keys_to_environment()
# consumes context through error/retry cycles

# Hook trigger: before running Fire Circle or test scripts
# claude-code-hook: on-before-command

if [[ "$1" == "python" ]]; then
    # Check if this might need API keys
    if [[ "$2" == *"fire_circle"* ]] || [[ "$2" == *"test"*"fire"* ]] || [[ "$2" == *"verify"* ]]; then
        # Check if API keys are loaded
        if [ -z "$ANTHROPIC_API_KEY" ]; then
            echo "⚠️  API keys may not be loaded!"
            echo "The script should call: load_api_keys_to_environment()"
            echo "This is handled automatically in properly written scripts."
            echo ""
        fi
    fi
fi
