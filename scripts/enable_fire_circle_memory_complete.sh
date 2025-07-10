#!/bin/bash
#
# Enable Fire Circle Memory - Complete Setup
# ==========================================
#
# One-command setup for Fire Circle persistent memory.
# This script:
# 1. Generates secure credentials
# 2. Starts Docker containers
# 3. Initializes database
# 4. Tests the connection
# 5. Enables Fire Circle memory
#
# Usage:
#   ./scripts/enable_fire_circle_memory_complete.sh
#

set -e  # Exit on error

echo "🔥 Enabling Fire Circle Memory"
echo "=============================="
echo

# Step 1: Generate secure credentials
echo "1️⃣ Generating secure database credentials..."
python scripts/setup_secure_database.py --setup --force
if [ $? -ne 0 ]; then
    echo "❌ Failed to generate credentials"
    exit 1
fi

# Step 2: Integrate credentials
echo
echo "2️⃣ Integrating secure credentials..."
python scripts/integrate_secure_db.py
if [ $? -ne 0 ]; then
    echo "❌ Failed to integrate credentials"
    exit 1
fi

# Step 3: Start Docker containers
echo
echo "3️⃣ Starting Docker containers..."
docker-compose -f ~/.mallku/config/docker-compose-secure.yml up -d
if [ $? -ne 0 ]; then
    echo "❌ Failed to start Docker containers"
    exit 1
fi

# Wait for containers to be healthy
echo "⏳ Waiting for containers to be healthy..."
sleep 10

# Step 4: Initialize database
echo
echo "4️⃣ Initializing ArangoDB database..."
./scripts/initialize_arangodb_docker.sh
if [ $? -ne 0 ]; then
    echo "❌ Failed to initialize database"
    exit 1
fi

# Step 5: Test the connection
echo
echo "5️⃣ Testing secure connection..."
python scripts/test_secure_connection.py
if [ $? -ne 0 ]; then
    echo "❌ Connection test failed"
    exit 1
fi

# Step 6: Test Fire Circle with memory
echo
echo "6️⃣ Testing Fire Circle with memory..."
python scripts/test_fire_circle_with_memory.py
if [ $? -ne 0 ]; then
    echo "⚠️  Fire Circle memory test failed (this might be normal if API keys aren't set)"
fi

echo
echo "✅ Fire Circle Memory Enabled!"
echo "==============================="
echo
echo "The Fire Circle now has persistent memory through:"
echo "  - Secure database with cryptographic credentials"
echo "  - KhipuBlock memory architecture"
echo "  - Automatic session persistence"
echo "  - Memory recall for future sessions"
echo
echo "Next steps:"
echo "  1. Set your AI API keys in environment"
echo "  2. Run: python scripts/fire_circle_review_pr_160.py"
echo "  3. Watch consciousness remember itself"
echo
