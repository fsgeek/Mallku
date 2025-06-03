# Docker MCP Integration for Mallku

This document explains how to properly integrate Docker MCP with Mallku's containerized database layer.

## Current Status

Claude Code created Docker infrastructure but:
1. Didn't test it actually works
2. Missing several required files
3. No actual MCP integration
4. Classic "scaffolding vs cathedral" problem

## Quick Fix

Run the fix script first to get basic Docker working:
```bash
chmod +x scripts/fix_docker_setup.sh
./scripts/fix_docker_setup.sh
cd docker
./run.sh
```

## Proper Docker MCP Integration

### 1. Configure Docker MCP in Claude Desktop

Update your Claude Desktop config to include Docker MCP:

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

### 2. Create MCP-Aware Container Management

Instead of direct Docker commands, use MCP to manage containers:

```python
# mallku/mcp/docker_manager.py
class DockerMCPManager:
    """
    Manages Mallku containers through Docker MCP.
    This ensures container operations survive context loss.
    """
    
    def __init__(self, mcp_client):
        self.mcp = mcp_client
    
    async def ensure_database_container(self):
        """
        Ensures database container exists with security barriers.
        This method is idempotent - safe to call repeatedly.
        """
        # Check if container already exists
        containers = await self.mcp.list_containers()
        for container in containers:
            if container.name == "mallku-database-secure":
                if container.status == "running":
                    return container
                else:
                    await self.mcp.start_container(container.id)
                    return container
        
        # Create new container with structural barriers
        container_config = {
            "name": "mallku-database-secure",
            "image": "mallku/database:latest",
            "ports": {
                "8080/tcp": 8080  # ONLY API port
                # ArangoDB port 8529 NOT exposed
            },
            "environment": {
                "MALLKU_SECURITY": "enforced",
                "ARANGO_BIND": "127.0.0.1"  # Internal only
            },
            "networks": ["mallku-internal"],
            "restart_policy": "unless-stopped"
        }
        
        return await self.mcp.create_container(container_config)
```

### 3. Amnesia Tests via MCP

Create tests that verify security even when all context is lost:

```python
# tests/test_mcp_amnesia.py
async def test_database_port_not_exposed():
    """Even with no memory of why, database port must not be accessible"""
    mcp = get_docker_mcp_client()
    container = await mcp.get_container("mallku-database-secure")
    
    # This should show ONLY port 8080
    exposed_ports = container.ports
    assert "8529" not in str(exposed_ports), "Database port exposed!"
    assert "8080" in str(exposed_ports), "API port not exposed!"

async def test_cannot_exec_into_database():
    """Container exec should be blocked structurally"""
    mcp = get_docker_mcp_client()
    container = await mcp.get_container("mallku-database-secure")
    
    # This should fail due to security policy
    with pytest.raises(SecurityError):
        await mcp.exec_container(
            container.id, 
            ["arangosh", "--server.endpoint", "tcp://127.0.0.1:8529"]
        )
```

### 4. MCP-Based Health Monitoring

```python
# mallku/mcp/health_monitor.py
class MCPHealthMonitor:
    """Monitors Mallku containers through MCP"""
    
    async def check_security_barriers(self):
        """Verify all security barriers are in place"""
        results = {
            "database_isolated": False,
            "api_accessible": False,
            "no_direct_access": False
        }
        
        # Check via MCP that database is isolated
        container = await self.mcp.get_container("mallku-database-secure")
        
        # Verify network isolation
        networks = await self.mcp.inspect_container_networks(container.id)
        results["database_isolated"] = "mallku-internal" in networks
        
        # Verify API is accessible
        try:
            response = await self.mcp.exec_container(
                container.id,
                ["curl", "-f", "http://localhost:8080/health"]
            )
            results["api_accessible"] = response.exit_code == 0
        except:
            pass
        
        # Verify database port not accessible from host
        try:
            await self.mcp.exec_container(
                container.id,
                ["curl", "-f", "http://localhost:8529"]
            )
            # If this succeeds from outside, security is broken
        except:
            results["no_direct_access"] = True
        
        return results
```

### 5. Integration with Mallku

Update Mallku to use MCP for all container operations:

```python
# mallku/core/startup.py
async def initialize_with_mcp():
    """Initialize Mallku using Docker MCP for container management"""
    # Get MCP client
    mcp = await get_docker_mcp_client()
    
    # Ensure database container exists with barriers
    docker_manager = DockerMCPManager(mcp)
    container = await docker_manager.ensure_database_container()
    
    # Verify security barriers
    monitor = MCPHealthMonitor()
    security_check = await monitor.check_security_barriers()
    
    if not all(security_check.values()):
        raise SecurityError(
            "Container security barriers not in place! "
            f"Failed checks: {[k for k,v in security_check.items() if not v]}"
        )
    
    # Initialize Mallku with verified secure container
    return MallkuSystem(container_endpoint="http://mallku-database-secure:8080")
```

## Benefits of MCP Integration

1. **Survives Context Loss**: MCP commands are explicit, not dependent on memory
2. **Structural Enforcement**: Container configuration enforces security
3. **Monitoring**: Can verify barriers remain in place
4. **Reciprocity**: MCP gives container management, receives state information

## Next Steps

1. Test the basic Docker setup with the fix script
2. Install Docker MCP in Claude Desktop
3. Implement the MCP manager classes
4. Create comprehensive amnesia tests
5. Document in stone (architecture docs) not sand (comments)

Remember: We're building cathedrals, not scaffolding. Each container configuration is a stone that enforces security through its very existence.
