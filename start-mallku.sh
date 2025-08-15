#!/bin/bash
# Quick start for Mallku Cathedral Architecture

set -e

echo "🏔️ Starting Mallku Services..."
echo

cd "$(dirname "$0")/docker"
docker-compose up -d

echo
echo "⏳ Waiting for services to be healthy..."
sleep 5

if curl -s -f http://localhost:8080/health > /dev/null; then
    echo "✅ Mallku is running!"
    echo
    echo "🔗 API Gateway: http://localhost:8080/health"
    echo "🔒 Security: http://localhost:8080/security/metrics"
    echo
    echo "📚 View logs: docker-compose -f docker/docker-compose.yml logs -f"
    echo "🛑 Stop: ./scripts/mallku-docker.sh stop"
else
    echo "❌ API Gateway health check failed"
    echo "Check logs: docker-compose -f docker/docker-compose.yml logs"
    exit 1
fi
