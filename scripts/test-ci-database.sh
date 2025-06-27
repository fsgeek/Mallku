#!/bin/bash
# Test script to verify CI database configuration

echo "Testing CI database configuration..."

# Set CI environment variables
export CI=1
export CI_DATABASE_AVAILABLE=1
export ARANGODB_HOST=localhost
export ARANGODB_PORT=8529
export ARANGODB_DATABASE=test_mallku
export ARANGODB_NO_AUTH=1

# Run a simple database test
python3 -c "
import os
from mallku.core.database import MallkuDBConfig

config = MallkuDBConfig()
print(f'Host: {config.config[\"database\"][\"host\"]}')
print(f'Port: {config.config[\"database\"][\"port\"]}')
print(f'Database: {config.config[\"database\"][\"database\"]}')
print(f'No Auth: {os.getenv(\"ARANGODB_NO_AUTH\")}')

if config.connect():
    print('✓ Connected to database successfully')
else:
    print('✗ Failed to connect to database')
"
