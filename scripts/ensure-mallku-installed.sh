#!/bin/bash
# Ensure mallku is installed in the current environment
# This script is used by pre-commit hooks to avoid recurring "mallku not installed" errors

set -e

# Try to import mallku
if python -c "import mallku" 2>/dev/null; then
    exit 0
fi

echo "mallku not installed, installing in editable mode..."

# Try uv first (preferred in CI)
if command -v uv >/dev/null 2>&1; then
    uv pip install -e . >/dev/null 2>&1 && exit 0
fi

# Fall back to pip
pip install -e . >/dev/null 2>&1
