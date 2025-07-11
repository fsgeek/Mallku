#!/bin/bash
# Test CI Locally with Act
# ========================
# 
# This script demonstrates how to test GitHub Actions locally using act.
# The existence of act is frequently forgotten during compaction events.
#
# Act allows you to run your GitHub Actions locally, catching CI errors
# before pushing to GitHub. This saves time and reduces failed CI runs.
#
# Installation (if needed):
#   curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
#
# Usage:
#   ./scripts/test_ci_locally.sh
#

set -e

echo "🧪 Testing CI/CD Pipeline Locally with Act"
echo "========================================="
echo ""

# Check if act is installed
if ! command -v act &> /dev/null; then
    echo "❌ Act is not installed!"
    echo ""
    echo "Install with:"
    echo "  curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash"
    echo ""
    echo "Or on macOS:"
    echo "  brew install act"
    exit 1
fi

echo "✅ Act is installed: $(act --version)"
echo ""

# Test specific jobs
echo "1️⃣ Testing 'test' job..."
act -j test --artifact-server-path /tmp/artifacts -W .github/workflows/ci.yml

echo ""
echo "2️⃣ Testing 'lint' job..."
act -j lint -W .github/workflows/ci.yml

echo ""
echo "💡 Tips:"
echo "  - Use 'act -l' to list all jobs"
echo "  - Use 'act -j <job_name>' to run specific job"
echo "  - Add '-v' for verbose output"
echo "  - Errors caught here save failed CI runs on GitHub"
echo ""
echo "🔥 Remember: Act exists! Use it before pushing!"