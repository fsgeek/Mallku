#!/bin/bash
# Build the fixed intelligent apprentice Docker image
# Created by Qillqa Kusiq (57th Artisan)

set -e

echo "🔨 Building fixed intelligent apprentice Docker image..."
echo "This includes full Mallku installation for proper API access"

# Change to project root
cd "$(dirname "$0")/../.."

# Build the image
docker build \
    -f docker/apprentice-weaver/Dockerfile.intelligent-fixed \
    -t mallku-apprentice-intelligent:fixed \
    -t mallku-apprentice:fixed \
    .

echo "✅ Fixed intelligent apprentice image built successfully!"
echo "Image tags:"
echo "  - mallku-apprentice-intelligent:fixed"
echo "  - mallku-apprentice:fixed"
