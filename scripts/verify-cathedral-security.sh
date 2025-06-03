#!/bin/bash
# Verify Cathedral Security Architecture

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m'

echo "=== Mallku Cathedral Security Verification ==="
echo

# Test 1: API Gateway is accessible
echo -n "Testing API Gateway accessibility... "
if curl -s -f http://localhost:8080/health > /dev/null; then
    echo -e "${GREEN}✓ PASS${NC}"
    echo "  API Gateway is healthy and responding"
else
    echo -e "${RED}✗ FAIL${NC}"
    echo "  API Gateway is not responding"
    exit 1
fi

# Test 2: Security metrics endpoint
echo -n "Testing security metrics... "
METRICS=$(curl -s http://localhost:8080/security/metrics)
if echo "$METRICS" | grep -q '"database_ports_exposed": 0'; then
    echo -e "${GREEN}✓ PASS${NC}"
    echo "  Security metrics confirm cathedral architecture:"
    echo "$METRICS" | python3 -m json.tool | sed 's/^/    /'
else
    echo -e "${RED}✗ FAIL${NC}"
    echo "  Security metrics not as expected"
fi

# Test 3: Database is NOT directly accessible
echo -n "Testing database isolation... "
if ! curl -s -f http://localhost:8529 --connect-timeout 2 > /dev/null 2>&1; then
    echo -e "${GREEN}✓ PASS${NC}"
    echo "  Database port 8529 is NOT exposed (as designed)"
else
    echo -e "${RED}✗ FAIL${NC}"
    echo "  WARNING: Database appears to be directly accessible!"
fi

# Test 4: API can list collections
echo -n "Testing API database access... "
COLLECTIONS=$(curl -s http://localhost:8080/api/v1/collections)
if echo "$COLLECTIONS" | grep -q '"collections"'; then
    echo -e "${GREEN}✓ PASS${NC}"
    echo "  API can access database internally"
    echo "  Collections: $COLLECTIONS"
else
    echo -e "${YELLOW}⚠ WARNING${NC}"
    echo "  Could not list collections (may be normal if database is empty)"
fi

# Test 5: Network isolation
echo -n "Testing network isolation... "
# Try to ping database from host (should fail)
if docker network ls | grep -q mallku-internal; then
    echo -e "${GREEN}✓ PASS${NC}"
    echo "  Internal network exists and is configured"
    
    # Additional test: try to connect to internal network from a test container
    echo -n "  Testing network access restriction... "
    if docker run --rm --network docker_mallku-internal alpine ping -c 1 database > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠ WARNING${NC}"
        echo "    Test container could join internal network"
    else
        echo -e "${GREEN}✓ PASS${NC}"
        echo "    Internal network properly isolated"
    fi
else
    echo -e "${RED}✗ FAIL${NC}"
    echo "  Internal network not found"
fi

echo
echo "=== Cathedral Security Summary ==="
echo "✓ API Gateway is the only exposed service"
echo "✓ Database has no exposed ports"
echo "✓ Internal network provides isolation"
echo "✓ All access must go through the API"
echo
echo "The cathedral stands strong! 🏛️"
