#!/bin/bash
# Quick fix for Docker build issues

echo "=== Quick Docker Build Fix ==="
echo

# Check if we're in the docker directory
if [[ ! -f "docker-compose.yml" ]]; then
    echo "Please run this from the docker/ directory"
    exit 1
fi

# Option 1: Update docker-compose to use parent directory as build context
echo "Creating fixed docker-compose file..."
cat > docker-compose.fixed.yml << 'EOF'
services:
  mallku-database:
    build:
      context: ..  # Use parent directory as build context
      dockerfile: docker/Dockerfile.database.alpine  # Use Alpine-fixed version
    container_name: mallku-database
    restart: unless-stopped
    environment:
      - ARANGO_NO_AUTH=1  # For development - remove in production!
    ports:
      - "8080:8080"
    volumes:
      - mallku_database_data:/var/lib/arangodb3
      - mallku_database_logs:/var/log/arangodb3
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

volumes:
  mallku_database_data:
  mallku_database_logs:
EOF

echo "Fixed docker-compose created!"
echo
echo "To build with the fix:"
echo "  docker-compose -f docker-compose.fixed.yml build"
echo
echo "Or if you prefer, rename it:"
echo "  mv docker-compose.fixed.yml docker-compose.yml"
