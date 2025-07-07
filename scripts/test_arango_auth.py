#!/usr/bin/env python3
"""
Test ArangoDB Authentication Options
====================================

48th Artisan - Finding the right connection path
"""

import requests
from arango import ArangoClient

print("Testing ArangoDB authentication options...\n")

# Test 1: Check if server is running
try:
    response = requests.get("http://localhost:8529/_api/version")
    print(f"✓ Server responding: Status {response.status_code}")
    if response.status_code == 200:
        print(f"  Version: {response.json()}")
except Exception as e:
    print(f"✗ Server not responding: {e}")
    exit(1)

# Test 2: Try no-auth connection
print("\nTesting no-auth connection...")
try:
    client = ArangoClient(hosts="http://localhost:8529")
    db = client.db("_system", verify=True)
    props = db.properties()
    print("✓ No-auth connection successful!")
    print(f"  System DB: {props['name']}")
    
    # Check if Mallku database exists
    if db.has_database("Mallku"):
        print("  Mallku database: EXISTS")
    else:
        print("  Mallku database: NOT FOUND")
        print("  Creating Mallku database...")
        db.create_database("Mallku")
        print("  ✓ Created successfully")
        
except Exception as e:
    print(f"✗ No-auth failed: {e}")
    print("\n  Your ArangoDB requires authentication.")
    print("  Please update .secrets/db-config.ini with correct credentials")
    print("  or run ArangoDB with ARANGO_NO_AUTH=1 for development")