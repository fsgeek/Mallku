#!/bin/bash
#
# Initialize ArangoDB Inside Docker Container
# ===========================================
#
# This script runs inside the Docker container to create the Mallku database
# and user, since Python can't reach the internal Docker network directly.
#
# Usage:
#   ./scripts/initialize_arangodb_docker.sh
#

set -e

echo "🗄️ Initializing ArangoDB for Mallku"
echo "===================================="

# Load credentials from secure config
CONFIG_FILE="$HOME/.mallku/config/docker_secure.json"
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ No secure configuration found at $CONFIG_FILE"
    echo "Please run first: python scripts/setup_secure_database.py --setup"
    exit 1
fi

# Extract values from JSON config
CONTAINER_NAME=$(jq -r '.container' "$CONFIG_FILE")
ROOT_PASSWORD=$(jq -r '.root_password' "$CONFIG_FILE")

# Get Mallku user credentials from INI file
INI_FILE="$HOME/.mallku/config/db_secure.ini"
MALLKU_USER=$(grep "mallku_user" "$INI_FILE" | cut -d'=' -f2 | tr -d ' ')
MALLKU_PASSWORD=$(grep "mallku_password" "$INI_FILE" | cut -d'=' -f2 | tr -d ' ')

echo "📦 Using container: $CONTAINER_NAME"

# Create initialization script
INIT_SCRIPT=$(cat <<EOF
// Initialize Mallku Database
const db = require('@arangodb');

// Create database if it doesn't exist
try {
    db._createDatabase('mallku');
    console.log('✅ Created database: mallku');
} catch (e) {
    if (e.errorNum === 1207) {
        console.log('✓ Database mallku already exists');
    } else {
        throw e;
    }
}

// Switch to mallku database
db._useDatabase('mallku');

// Create user if it doesn't exist
try {
    const users = require('@arangodb/users');
    users.save('$MALLKU_USER', '$MALLKU_PASSWORD', true);
    users.grantDatabase('$MALLKU_USER', 'mallku', 'rw');
    console.log('✅ Created user: $MALLKU_USER with full access to mallku database');
} catch (e) {
    if (e.errorNum === 1702) {
        console.log('✓ User $MALLKU_USER already exists');
        // Update permissions anyway
        const users = require('@arangodb/users');
        users.grantDatabase('$MALLKU_USER', 'mallku', 'rw');
    } else {
        throw e;
    }
}

// Create collections for Fire Circle
const collections = [
    'fire_circle_sessions',
    'khipu_blocks',
    'narrative_threads',
    'consciousness_metrics'
];

collections.forEach(name => {
    try {
        db._create(name);
        console.log(\`✅ Created collection: \${name}\`);
    } catch (e) {
        if (e.errorNum === 1207) {
            console.log(\`✓ Collection \${name} already exists\`);
        } else {
            throw e;
        }
    }
});

console.log('\\n🎉 Mallku database initialization complete!');
EOF
)

# Run the initialization inside the container
echo
echo "🔄 Running initialization script..."
docker exec -i "$CONTAINER_NAME" arangosh \
    --server.password "$ROOT_PASSWORD" \
    --javascript.execute-string "$INIT_SCRIPT"

echo
echo "✅ Database initialization complete!"
echo "===================================="
echo
echo "Created:"
echo "  - Database: mallku"
echo "  - User: $MALLKU_USER (with full access)"
echo "  - Collections:"
echo "    - fire_circle_sessions"
echo "    - khipu_blocks"
echo "    - narrative_threads"
echo "    - consciousness_metrics"
echo
