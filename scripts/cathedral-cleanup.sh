#!/bin/bash
# Cathedral Cleanup - Remove scaffolding, keep structure
# This script tidies the Docker workspace after our learning journey

echo "=== Cathedral Cleanup - Docker Workspace ==="
echo "Removing scaffolding files and promoting cathedral architecture"
echo

# Document what we're doing
echo "Files to remove (scaffolding):"
echo "  - docker-compose.yml (old mixed-concerns version)"
echo "  - Dockerfile.database (attempted to modify ArangoDB)"
echo "  - Dockerfile.database.alpine (Alpine experiment)"
echo "  - Dockerfile.database.ubuntu (Ubuntu variant)"
echo "  - fix-build.sh (workaround script)"
echo "  - requirements-database.txt (no longer needed)"
echo

echo "Files to keep (cathedral):"
echo "  - Dockerfile.api (single-purpose API container)"
echo "  - requirements-api.txt (API dependencies)"
echo "  - docker-compose.cathedral.yml → docker-compose.yml"
echo

# Ask for confirmation
read -p "Proceed with cleanup? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cleanup cancelled"
    exit 1
fi

# Remove scaffolding files
echo
echo "Removing scaffolding files..."
git rm docker/Dockerfile.database
git rm docker/Dockerfile.database.alpine
git rm docker/Dockerfile.database.ubuntu
git rm docker/fix-build.sh
git rm docker/requirements-database.txt
git rm docker/docker-compose.yml

# Promote cathedral architecture
echo
echo "Promoting cathedral architecture to default..."
git mv docker/docker-compose.cathedral.yml docker/docker-compose.yml

# Commit the cleanup
echo
echo "Creating cleanup commit..."
git commit -m "Clean Docker workspace - remove scaffolding, keep cathedral

Removed experimental files and workarounds:
- Multiple database Dockerfiles (now using vanilla ArangoDB)
- fix-build.sh workaround script
- Old docker-compose.yml with mixed concerns

Kept cathedral architecture:
- Dockerfile.api for single-purpose API container
- docker-compose.yml (renamed from cathedral version)
- Clear separation of concerns

The workspace now shows only the final architecture."

echo
echo "=== Cleanup Complete ==="
echo "The Docker workspace now contains only cathedral architecture files."
echo "Test with: cd docker && docker-compose build && docker-compose up"
