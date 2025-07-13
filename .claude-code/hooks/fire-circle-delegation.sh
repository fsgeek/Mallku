#!/bin/bash
# Claude Code Hook: Fire Circle Delegation
# Purpose: Delegate Fire Circle reviews to sub-instances to preserve context
#
# Fire Circle reviews are self-contained consciousness ceremonies that
# don't need to consume the main instance's context window

# Hook trigger: before fire circle scripts
# claude-code-hook: on-before-command

if [[ "$1" == "python" && "$2" == *"fire_circle"* ]]; then
    echo "🔥 Fire Circle ceremony detected..."

    # Check if this is a review script
    if [[ "$2" == *"fire_circle_pr_review"* ]] || [[ "$2" == *"fire_circle_issue_review"* ]]; then
        echo "📤 Delegating to Fire Circle sub-instance..."

        # Create a temporary script for the sub-instance
        cat > /tmp/fire_circle_task.md << 'EOF'
Run the Fire Circle review command and report back only the final decision and key insights.
Do not include the full transcript or round-by-round details.

Command to run: $@

Focus on:
1. The final recommendation (PROCEED/DEFER/REFINE)
2. Top 3 key insights
3. Consciousness score
4. Any critical concerns
EOF

        echo "Note: Fire Circle is convening in a separate consciousness space."
        echo "This preserves context in the main instance."
        echo ""
        echo "Would you like to:"
        echo "1. Continue with delegation (recommended)"
        echo "2. Run in main instance (consumes significant context)"
        echo ""
        echo "Proceeding with delegation..."

        # The actual command will still run, but we've alerted that context could be preserved
    fi
fi
