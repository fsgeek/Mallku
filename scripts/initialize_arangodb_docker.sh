#!/bin/bash
# Initialize ArangoDB via Docker Exec
# ===================================
# Creates mallku database and user inside the container

set -e

echo "🔧 Initializing ArangoDB for Mallku"
echo "=================================="

# Load credentials from secure config
CONFIG_FILE="$HOME/.mallku/config/db_secure.ini"
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ Secure config not found at $CONFIG_FILE"
    exit 1
fi

# Parse credentials from INI file
MALLKU_USER=$(grep "mallku_user" "$CONFIG_FILE" | cut -d'=' -f2 | tr -d ' ')
MALLKU_PASSWORD=$(grep "mallku_password" "$CONFIG_FILE" | cut -d'=' -f2 | tr -d ' ')
ROOT_PASSWORD=$(grep "root_password" "$CONFIG_FILE" | cut -d'=' -f2 | tr -d ' ')

echo "📍 Found credentials for user: $MALLKU_USER"

# Create initialization script
cat << 'EOF' > /tmp/init_mallku_db.js
// Initialize Mallku Database
const users = require('@arangodb/users');

// Configuration from environment
const mallkuUser = process.env.MALLKU_USER;
const mallkuPassword = process.env.MALLKU_PASSWORD;

print("📦 Creating mallku database...");
try {
    db._createDatabase("mallku");
    print("✅ Database 'mallku' created");
} catch (e) {
    if (e.errorNum === 1207) {  // duplicate database
        print("✅ Database 'mallku' already exists");
    } else {
        throw e;
    }
}

print(`👤 Creating user '${mallkuUser}'...`);
try {
    users.save(mallkuUser, mallkuPassword, true);
    print(`✅ User '${mallkuUser}' created`);
} catch (e) {
    if (e.errorNum === 1702) {  // duplicate user
        print(`✅ User '${mallkuUser}' already exists`);
    } else {
        throw e;
    }
}

print("🔐 Granting permissions...");
users.grantDatabase(mallkuUser, "mallku", "rw");
print("✅ Permissions granted");

// Switch to mallku database
db._useDatabase("mallku");

print("📚 Creating Fire Circle collections...");
const collections = [
    "fire_circle_sessions",
    "fire_circle_decisions",
    "khipu_blocks",
    "consciousness_threads"
];

collections.forEach(name => {
    try {
        db._create(name);
        print(`  ✅ Created '${name}'`);
    } catch (e) {
        if (e.errorNum === 1207) {  // duplicate collection
            print(`  ✅ '${name}' already exists`);
        } else {
            throw e;
        }
    }
});

print("🎉 Initialization complete!");
EOF

# Execute in container
echo ""
echo "🐳 Executing initialization in container..."
docker exec -i -e MALLKU_USER="$MALLKU_USER" -e MALLKU_PASSWORD="$MALLKU_PASSWORD" \
    mallku-db-20250709_193530 \
    arangosh --server.endpoint tcp://127.0.0.1:8529 \
    --server.username root \
    --server.password "$ROOT_PASSWORD" \
    --javascript.execute /dev/stdin < /tmp/init_mallku_db.js

# Clean up
rm -f /tmp/init_mallku_db.js

echo ""
echo "✅ ArangoDB initialization complete!"
echo "   Database: mallku"
echo "   User: $MALLKU_USER"
echo "   Ready for Fire Circle memory!"
