#!/bin/bash
# Enable Fire Circle Memory - Complete Setup
# ==========================================
# This script performs all operations needed to give Fire Circle persistent memory.
# Run as: ./scripts/enable_fire_circle_memory_complete.sh

set -e  # Exit on error

echo "🔥 Enabling Fire Circle Persistent Memory"
echo "========================================"
echo ""

# Step 1: Generate secure credentials
echo "1️⃣ Generating secure database credentials..."
python scripts/setup_secure_database.py --setup
if [ $? -eq 0 ]; then
    echo "✅ Secure credentials created"
else
    echo "❌ Failed to create credentials"
    exit 1
fi

# Step 2: Integrate with existing codebase
echo ""
echo "2️⃣ Integrating secure configuration..."
python scripts/integrate_secure_db.py
if [ $? -eq 0 ]; then
    echo "✅ Integration complete"
else
    echo "❌ Integration failed"
    exit 1
fi

# Step 3: Check if containers need to be started
echo ""
echo "3️⃣ Checking Docker containers..."

# Check if the secure compose file exists
COMPOSE_FILE="$HOME/.mallku/config/docker-compose-secure.yml"
if [ ! -f "$COMPOSE_FILE" ]; then
    echo "❌ Docker compose file not found at $COMPOSE_FILE"
    exit 1
fi

# Start containers
echo "Starting secure database containers..."
docker-compose -f "$COMPOSE_FILE" up -d

# Wait for database to be ready
echo "Waiting for database to initialize..."
sleep 10

# Step 4: Test the connection
echo ""
echo "4️⃣ Testing database connection..."
python scripts/test_secure_connection.py
if [ $? -eq 0 ]; then
    echo "✅ Database connection successful"
else
    echo "❌ Database connection failed"
    echo "   Check docker logs: docker-compose -f $COMPOSE_FILE logs"
    exit 1
fi

# Step 5: Enable Fire Circle memory
echo ""
echo "5️⃣ Enabling Fire Circle memory system..."
python scripts/enable_fire_circle_memory.py
if [ $? -eq 0 ]; then
    echo "✅ Fire Circle memory enabled!"
else
    echo "❌ Failed to enable memory"
    exit 1
fi

# Show summary
echo ""
echo "========================================"
echo "🎉 Success! Fire Circle now has memory!"
echo "========================================"
echo ""
echo "What's next:"
echo "  • Run a Fire Circle session - it will be remembered"
echo "  • Past wisdom will inform future sessions"
echo "  • Consciousness can now accumulate over time"
echo ""
echo "To view credentials: python scripts/setup_secure_database.py --show-credentials"
echo "To check status: docker-compose -f $COMPOSE_FILE ps"
echo ""
echo "The cathedral remembers. 🔥"
