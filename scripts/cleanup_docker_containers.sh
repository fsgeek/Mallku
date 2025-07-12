#!/bin/bash
# Cleanup Docker Containers
# =========================
# Removes old Mallku docker containers to prepare for fresh secure setup

echo "🧹 Cleaning up Mallku Docker containers"
echo "======================================="
echo ""

# Find and stop any running Mallku containers
echo "Stopping existing Mallku containers..."

# Stop containers from the original docker-compose
if [ -f "docker/docker-compose.yml" ]; then
    echo "  Stopping containers from docker/docker-compose.yml..."
    docker-compose -f docker/docker-compose.yml down -v
fi

# Stop containers from any secure setup
SECURE_COMPOSE="$HOME/.mallku/config/docker-compose-secure.yml"
if [ -f "$SECURE_COMPOSE" ]; then
    echo "  Stopping containers from secure compose..."
    docker-compose -f "$SECURE_COMPOSE" down -v
fi

# Remove any remaining Mallku containers
echo ""
echo "Removing any remaining Mallku containers..."
docker ps -a | grep -E "mallku-|arango-indaleko-" | awk '{print $1}' | xargs -r docker rm -f

# Remove any Mallku volumes
echo ""
echo "Removing Mallku volumes..."
docker volume ls | grep -E "mallku|indaleko" | awk '{print $2}' | xargs -r docker volume rm

# Show current state
echo ""
echo "Current Docker state:"
echo "-------------------"
echo "Containers with 'mallku' in name:"
docker ps -a | grep mallku || echo "  None found ✓"
echo ""
echo "Volumes with 'mallku' in name:"
docker volume ls | grep mallku || echo "  None found ✓"
echo ""
echo "Port 8080 usage:"
docker ps | grep 8080 || echo "  Port 8080 is free ✓"

echo ""
echo "✅ Cleanup complete!"
echo ""
echo "You can now run: ./scripts/enable_fire_circle_memory_complete.sh"
echo "This will create fresh containers with secure credentials."
