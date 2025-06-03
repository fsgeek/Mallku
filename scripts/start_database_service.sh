#!/bin/bash
# Start script for Mallku Database Container
# Embodies "security through architecture" by controlling service startup

set -e

echo "Starting Mallku Database Service - Cathedral Foundation"
echo "Philosophy: Security through architecture, not guidelines"

# Function to check if ArangoDB is ready
wait_for_arangodb() {
    echo "Waiting for ArangoDB to be ready..."
    local max_attempts=30
    local attempt=1

    while [ $attempt -le $max_attempts ]; do
        if curl -s -f http://localhost:8529/_api/version > /dev/null 2>&1; then
            echo "ArangoDB is ready!"
            return 0
        fi

        echo "Attempt $attempt/$max_attempts: ArangoDB not ready yet..."
        sleep 2
        attempt=$((attempt + 1))
    done

    echo "ArangoDB failed to start within timeout"
    return 1
}

# Function to setup initial database
setup_database() {
    echo "Setting up initial Mallku database configuration..."

    # Create initial admin user if needed
    # Note: In production, this should use proper credential management
    curl -X POST http://localhost:8529/_api/user \
         -H "Content-Type: application/json" \
         -d '{"user": "mallku", "passwd": "changeme", "active": true}' \
         > /dev/null 2>&1 || true

    echo "Database setup completed"
}

# Function to cleanup on exit
cleanup() {
    echo "Received shutdown signal - cleaning up..."

    # Stop Mallku service gracefully
    if [ ! -z "$MALLKU_PID" ]; then
        echo "Stopping Mallku API service..."
        kill -TERM "$MALLKU_PID" 2>/dev/null || true
        wait "$MALLKU_PID" 2>/dev/null || true
    fi

    # Stop ArangoDB gracefully
    if [ ! -z "$ARANGO_PID" ]; then
        echo "Stopping ArangoDB..."
        kill -TERM "$ARANGO_PID" 2>/dev/null || true
        wait "$ARANGO_PID" 2>/dev/null || true
    fi

    echo "Cleanup completed"
    exit 0
}

# Setup signal handlers
trap cleanup SIGTERM SIGINT

# Start ArangoDB in the background
echo "Starting ArangoDB server..."
su arangodb -c "arangod --configuration /etc/arangodb3/arangodb-secured.conf" &
ARANGO_PID=$!

# Wait for ArangoDB to be ready
if ! wait_for_arangodb; then
    echo "Failed to start ArangoDB"
    exit 1
fi

# Setup database
setup_database

# Start the Mallku API service
echo "Starting Mallku secured interface API..."
su mallku -c "cd /opt/mallku && python3 database_service.py" &
MALLKU_PID=$!

echo "Mallku Database Service started successfully"
echo "ArangoDB PID: $ARANGO_PID"
echo "Mallku API PID: $MALLKU_PID"
echo ""
echo "Remember: This container embodies Ayni - reciprocal architecture"
echo "- Structure provides safety, applications get freedom within boundaries"
echo "- Direct database access is impossible, only secured interface available"
echo "- Built for those who come after us - cathedral stones placed with care"
echo ""
echo "Health check: curl http://localhost:8080/health"
echo "Security metrics: curl http://localhost:8080/security/metrics"

# Wait for either process to exit
wait
