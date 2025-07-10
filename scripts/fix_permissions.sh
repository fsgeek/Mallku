#!/bin/bash
# Fix ArangoDB User Permissions
# =============================

set -e

echo "🔧 Fixing ArangoDB permissions"
echo "=============================="

# Load credentials
CONFIG_FILE="$HOME/.mallku/config/db_secure.ini"
MALLKU_USER=$(grep "mallku_user" "$CONFIG_FILE" | cut -d'=' -f2 | tr -d ' ')
ROOT_PASSWORD=$(grep "root_password" "$CONFIG_FILE" | cut -d'=' -f2 | tr -d ' ')

echo "📍 Fixing permissions for user: $MALLKU_USER"

# Create permission script
cat << 'EOF' > /tmp/fix_permissions.js
// Fix permissions for mallku user
const users = require('@arangodb/users');
const mallkuUser = process.env.MALLKU_USER;

print(`🔐 Granting system permissions to ${mallkuUser}...`);

// Grant read access to _system database (needed for version() call)
users.grantDatabase(mallkuUser, "_system", "ro");
print("✅ Granted read-only access to _system database");

// Ensure full access to mallku database
users.grantDatabase(mallkuUser, "mallku", "rw");
print("✅ Granted read-write access to mallku database");

// List current permissions
print("\n📋 Current permissions for " + mallkuUser + ":");
const perms = users.permission(mallkuUser);
print(JSON.stringify(perms, null, 2));
EOF

# Execute in container
docker exec -e MALLKU_USER="$MALLKU_USER" \
    mallku-db-20250709_193530 \
    arangosh --server.endpoint tcp://127.0.0.1:8529 \
    --server.username root \
    --server.password "$ROOT_PASSWORD" \
    --javascript.execute /dev/stdin < /tmp/fix_permissions.js

# Clean up
rm -f /tmp/fix_permissions.js

echo ""
echo "✅ Permissions fixed!"
