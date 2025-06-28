#!/bin/bash
# Setup script for act - run GitHub Actions locally

echo "Setting up act for local CI testing..."

# Detect OS and architecture
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)

# Map architecture names
case $ARCH in
    x86_64) ARCH="x86_64" ;;
    aarch64|arm64) ARCH="arm64" ;;
    armv7l) ARCH="armv7" ;;
    *) echo "Unsupported architecture: $ARCH"; exit 1 ;;
esac

# Download act
echo "Downloading act for $OS/$ARCH..."
curl -s https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Create act configuration
cat > ~/.actrc <<EOF
# Default image for ubuntu-latest
-P ubuntu-latest=catthehacker/ubuntu:act-latest
# Use docker to run containers
--container-daemon-socket unix:///var/run/docker.sock
EOF

echo "✓ act installed successfully"
echo ""
echo "Usage examples:"
echo "  act                    # Run default push event"
echo "  act -l                 # List all workflows"
echo "  act -j test            # Run specific job"
echo "  act -n                 # Dry run"
echo "  act --secret-file .secrets/.env  # Use secrets"
echo ""
echo "For CI database testing:"
echo "  act -j test --env CI=1 --env CI_DATABASE_AVAILABLE=1"
