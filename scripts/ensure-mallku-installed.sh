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
    if uv pip install -e . >/dev/null 2>&1; then
        echo "Successfully installed mallku with uv"
        exit 0
    else
        echo "Failed to install mallku with uv"
        exit 1
    fi
fi

# Try python -m pip as fallback (for local development)
if python -m pip install -e . >/dev/null 2>&1; then
    echo "Successfully installed mallku with pip"
    exit 0
else
    echo "Failed to install mallku. Please ensure uv or pip is available."
    exit 1
fi
