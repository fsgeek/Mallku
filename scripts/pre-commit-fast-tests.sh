#!/bin/bash
# Run fast tests for pre-commit - local development only
# In CI, these tests are handled by the dedicated test job

set -e

# Skip in CI environment
if [ -n "$CI" ]; then
    echo "Skipping pre-commit tests in CI (handled by dedicated test job)"
    exit 0
fi

# Activate virtual environment
if [ -d ".venv-linux-python3.13" ]; then
    source .venv-linux-python3.13/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo "Warning: No virtual environment found"
fi

# Ensure mallku is installed
./scripts/ensure-mallku-installed.sh >/dev/null 2>&1 || true

# Run fast tests
echo "Running fast tests..."
pytest tests/test_simple.py tests/test_minimal_ci.py tests/test_system_health.py tests/test_mallku_imports.py -q --tb=short
