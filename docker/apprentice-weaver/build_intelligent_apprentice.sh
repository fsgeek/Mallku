#!/bin/bash
# Build script for Intelligent Apprentice Docker image
# Created by Yuyay Rikch'aq (56th Artisan)

set -e

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║         Building Intelligent Apprentice Image                ║"
echo "║                                                              ║"
echo "║  'The apprentices breathe. Now they shall think.'            ║"
echo "║                   - Yuyay Rikch'aq                           ║"
echo "╚══════════════════════════════════════════════════════════════╝"

# Navigate to project root
cd "$(dirname "$0")/../.."

# Build the intelligent apprentice image
echo "🔨 Building mallku-apprentice-intelligent:latest..."
docker build \
    -f docker/apprentice-weaver/Dockerfile.intelligent \
    -t mallku-apprentice-intelligent:latest \
    .

# Tag it as the default apprentice image
docker tag mallku-apprentice-intelligent:latest mallku-apprentice:latest

echo "✅ Build complete!"
echo ""
echo "The intelligent apprentice image is now available as:"
echo "  - mallku-apprentice-intelligent:latest"
echo "  - mallku-apprentice:latest (default)"
echo ""
echo "Apprentices spawned from now on will have AI reasoning capabilities."
