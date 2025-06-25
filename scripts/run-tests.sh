#!/bin/bash
#
# Mallku Test Runner
# ==================
#
# Convenient script to run different levels of tests
#
# Usage:
#   ./scripts/run-tests.sh         # Run fast tests (default)
#   ./scripts/run-tests.sh full    # Run all tests
#   ./scripts/run-tests.sh memory  # Run memory-specific tests
#   ./scripts/run-tests.sh fire    # Run Fire Circle tests

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Find and activate virtual environment
if [ -d ".venv-linux-python3.13" ]; then
    source .venv-linux-python3.13/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo -e "${RED}Error: No virtual environment found${NC}"
    exit 1
fi

echo -e "${GREEN}🔍 Mallku Test Runner${NC}"
echo -e "${GREEN}=====================${NC}\n"

case "$1" in
    "full")
        echo -e "${YELLOW}Running full test suite...${NC}"
        pytest tests -v
        ;;
    "memory")
        echo -e "${YELLOW}Running memory architecture tests...${NC}"
        pytest tests/test_episodic_memory.py tests/test_memory_retrieval_strategies.py -v
        ;;
    "fire")
        echo -e "${YELLOW}Running Fire Circle tests...${NC}"
        pytest tests/test_fire_circle_integration.py tests/test_consciousness_* -v
        ;;
    "fast"|"")
        echo -e "${YELLOW}Running fast tests (structure and imports)...${NC}"
        pytest tests/test_simple.py tests/test_minimal_ci.py tests/test_system_health.py tests/test_mallku_imports.py -v
        ;;
    "pre-commit")
        echo -e "${YELLOW}Running pre-commit hooks with tests...${NC}"
        pre-commit run --all-files
        ;;
    "pre-commit-full")
        echo -e "${YELLOW}Running full pre-commit suite...${NC}"
        pre-commit run --config .pre-commit-config-full.yaml --all-files
        ;;
    *)
        echo -e "${RED}Unknown test level: $1${NC}"
        echo "Usage: $0 [fast|full|memory|fire|pre-commit|pre-commit-full]"
        exit 1
        ;;
esac

echo -e "\n${GREEN}✅ Tests completed!${NC}"
