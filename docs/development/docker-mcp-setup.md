# Docker MCP Integration Setup

This guide helps you set up Docker MCP for Mallku's containerized database layer.

## Prerequisites

1. Docker Desktop installed and running
2. Claude Desktop (or another MCP-compatible client)
3. Python environment for Mallku

## Installation Steps

### 1. Install Docker MCP

Choose one of these methods:

#### Option A: Using the QuantGeekDev implementation
```bash
# Clone the docker-mcp repository
git clone https://github.com/QuantGeekDev/docker-mcp.git
cd docker-mcp

# Install dependencies (if running locally)
pip install -r requirements.txt
```

#### Option B: Using Docker Hub (when available)
```bash
# Pull the Docker MCP container
docker pull mcp/docker-mcp:latest
```

### 2. Configure Claude Desktop

Add this to your Claude Desktop configuration file:

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "docker-mcp": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-v", "/var/run/docker.sock:/var/run/docker.sock",
        "ghcr.io/quantgeekdev/docker-mcp:latest"
      ]
    }
  }
}
```

For local development:
```json
{
  "mcpServers": {
    "docker-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "<path-to-docker-mcp>",
        "run",
        "docker-mcp"
      ]
    }
  }
}
```

### 3. Create Mallku Database Container Configuration

Create `docker/mallku-db/docker-compose.yml`:

```yaml
version: '3.8'

services:
  mallku-database:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: mallku-db-secure
    ports:
      - "7474:7474"  # Only Mallku API port exposed
    environment:
      - MALLKU_SECURITY_LEVEL=production
      - ARANGODB_ROOT_PASSWORD_FILE=/run/secrets/db_password
      - MALLKU_ENFORCE_SECURITY=true
      - DISABLE_DIRECT_ACCESS=true
    networks:
      - mallku-internal
    volumes:
      - mallku-data:/var/lib/arangodb3
      - ./schemas:/opt/mallku/schemas
    secrets:
      - db_password
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:7474/health"]
      interval: 30s
      timeout: 10s
      retries: 3

networks:
  mallku-internal:
    driver: bridge
    internal: true  # No external access

volumes:
  mallku-data:
    driver: local
    driver_opts:
      type: none
      device: ${PWD}/data
      o: bind

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

### 4. Create Database Layer Dockerfile

Create `docker/mallku-db/Dockerfile`:

```dockerfile
FROM arangodb:3.11

# Install Python for Mallku API layer
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Mallku database layer
COPY mallku-db-layer/ /opt/mallku/

# Install Python dependencies
RUN pip3 install -r /opt/mallku/requirements.txt

# Configure ArangoDB for internal use only
COPY arangodb.conf /etc/arangodb3/

# Copy startup script
COPY start.sh /opt/mallku/start.sh
RUN chmod +x /opt/mallku/start.sh

# Expose only Mallku API port
EXPOSE 7474

# Start both ArangoDB and Mallku layer
CMD ["/opt/mallku/start.sh"]
```

### 5. Create Startup Script

Create `docker/mallku-db/start.sh`:

```bash
#!/bin/bash

# Start ArangoDB in background
/usr/sbin/arangod &

# Wait for ArangoDB to be ready
until curl -s http://localhost:8529/_api/version > /dev/null; do
    echo "Waiting for ArangoDB..."
    sleep 2
done

# Start Mallku API layer
cd /opt/mallku
python3 -m mallku.database.api_server --port 7474
```

### 6. Test MCP Integration

Once configured, you can interact with Docker through Claude:

```
"Show me running containers"
"Create a new mallku-database container"
"Check the health of mallku-db-secure"
```

## Security Validation

### Amnesia Test 1: Port Security
```bash
# This should fail - ArangoDB port not exposed
curl http://localhost:8529

# This should succeed - Only API port exposed
curl http://localhost:7474/health
```

### Amnesia Test 2: Network Isolation
```bash
# Try to access database from outside container
docker exec mallku-db-secure curl http://localhost:8529  # Works inside

# But external access fails due to internal network
ping mallku-db-secure  # Should fail from host
```

### Amnesia Test 3: Direct Access Prevention
```bash
# Even with container access, direct DB operations blocked
docker exec mallku-db-secure arangosh \
  --server.endpoint http://localhost:8529 \
  # Should be blocked by configuration
```

## Next Steps

1. Implement the Mallku Database API layer (Issue #14)
2. Create MCP-specific container management commands
3. Add monitoring and metrics through MCP
4. Implement volume encryption for data at rest

## Troubleshooting

### MCP Not Connecting
- Ensure Docker Desktop is running
- Check that Docker socket is accessible
- Verify Claude Desktop configuration path

### Container Won't Start
- Check Docker logs: `docker logs mallku-db-secure`
- Ensure secrets file exists: `./secrets/db_password.txt`
- Verify network configuration

### Performance Issues
- Monitor with: `docker stats mallku-db-secure`
- Check MCP overhead in Claude Desktop logs
- Adjust container resources if needed

---

*This setup ensures that security boundaries are structurally enforced through containerization, surviving any loss of context or developer memory.*
