#!/bin/bash
#
# Smart Commit Helper
# ===================
#
# Handles linting fixes automatically while keeping developer informed
#
# Usage:
#   ./scripts/smart-commit.sh "Your commit message"
#
# This script will:
# 1. Run pre-commit hooks
# 2. If only formatting fixes needed, auto-stage and continue
# 3. If other issues, prompt for review
# 4. Show what was auto-fixed

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

if [ $# -eq 0 ]; then
    echo -e "${RED}Error: Please provide a commit message${NC}"
    echo "Usage: $0 \"Your commit message\""
    exit 1
fi

COMMIT_MSG="$*"

echo -e "${BLUE}🤖 Smart Commit Helper${NC}"
echo -e "${BLUE}=====================${NC}\n"

# Find and activate virtual environment
if [ -d ".venv-linux-python3.13" ]; then
    source .venv-linux-python3.13/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo -e "${RED}Error: No virtual environment found${NC}"
    echo -e "Please activate your virtual environment first"
    exit 1
fi

# Store initial git status
INITIAL_STATUS=$(git status --porcelain)

# Run pre-commit hooks
echo -e "${YELLOW}Running pre-commit hooks...${NC}"
if pre-commit run --all-files; then
    echo -e "${GREEN}✅ All checks passed! Committing...${NC}"
    git commit -m "$COMMIT_MSG"
    exit 0
fi

# Check what changed
CURRENT_STATUS=$(git status --porcelain)

# Check if only formatting changes were made
MODIFIED_FILES=$(git diff --name-only)
if [ -n "$MODIFIED_FILES" ]; then
    echo -e "\n${YELLOW}The following files were modified by linters:${NC}"
    echo "$MODIFIED_FILES" | sed 's/^/  - /'

    # Check if changes are only whitespace/formatting
    ONLY_FORMATTING=true
    for file in $MODIFIED_FILES; do
        # Check if there are non-whitespace changes
        if git diff "$file" | grep -E '^[+-][^+-]' | grep -qv -E '^[+-]\s*$'; then
            # More than just whitespace changed
            if git diff "$file" | grep -E '^[+-]' | head -20; then
                ONLY_FORMATTING=false
            fi
        fi
    done

    if [ "$ONLY_FORMATTING" = true ]; then
        echo -e "\n${GREEN}Only formatting/whitespace changes detected.${NC}"
        echo -e "${YELLOW}Auto-staging and retrying commit...${NC}"
        git add $MODIFIED_FILES

        # Retry pre-commit
        if pre-commit run --all-files; then
            echo -e "${GREEN}✅ All checks passed! Committing...${NC}"
            git commit -m "$COMMIT_MSG"
            echo -e "\n${GREEN}Successfully committed with auto-fixed formatting!${NC}"
            exit 0
        fi
    else
        echo -e "\n${YELLOW}⚠️  Non-formatting changes detected.${NC}"
        echo -e "${YELLOW}Please review the changes above and decide:${NC}"
        echo -e "  1. ${GREEN}git add -A && git commit -m \"$COMMIT_MSG\"${NC} (accept all changes)"
        echo -e "  2. ${BLUE}git diff${NC} (review changes in detail)"
        echo -e "  3. ${RED}git checkout .${NC} (discard linter changes)"
        exit 1
    fi
fi

echo -e "${RED}Pre-commit hooks failed for reasons other than formatting.${NC}"
echo -e "Please fix the issues and try again."
exit 1
