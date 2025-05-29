#!/bin/bash
# Pre-commit Setup Script for Mallku
# Sets up local development guardrails

set -e  # Exit on any error

echo "Installing pre-commit via uv..."
uv pip install pre-commit

echo "Installing pre-commit hooks..."
pre-commit install

echo "Running all pre-commit hooks on existing files..."
pre-commit run --all-files

echo "✅ Pre-commit setup complete. Your code will now walk the path of clarity and care."
