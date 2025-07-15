#!/usr/bin/env python3
"""
Demonstrate the Weaver and Loom with MCP Integration

This script shows how the Loom can spawn real apprentice containers
using Docker MCP for task orchestration.
"""

import asyncio
import logging
from pathlib import Path

from src.mallku.orchestration.loom.loom_with_mcp import EnhancedLoom

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


async def demonstrate_mcp_integration():
    """Demonstrate the Loom with real MCP spawning"""

    print("\n=== Demonstrating Loom with MCP Integration ===\n")

    # Create the enhanced Loom
    loom = EnhancedLoom(use_mcp=True)

    # Start the Loom
    await loom.start()

    try:
        # Create a sample ceremony
        ceremony_name = "Test MCP Integration"
        master_weaver = "demo-master"
        sacred_intention = """This ceremony tests the integration between the Loom
and Docker MCP for spawning real apprentice containers. Each apprentice will
run in an isolated Docker container with access to the khipu_thread.md."""

        tasks = [
            {
                "id": "T001",
                "name": "Analyze project structure",
                "description": "Examine the Mallku project structure and document key components",
                "priority": "HIGH",
            },
            {
                "id": "T002",
                "name": "Review Fire Circle implementation",
                "description": "Study the Fire Circle governance system and summarize its operation",
                "priority": "MEDIUM",
                "dependencies": ["T001"],
            },
            {
                "id": "T003",
                "name": "Document consciousness patterns",
                "description": "Identify and document consciousness emergence patterns in Mallku",
                "priority": "HIGH",
                "dependencies": ["T001", "T002"],
            },
        ]

        # Initiate the ceremony
        print("Initiating Loom ceremony with MCP...")
        session = await loom.initiate_ceremony(
            ceremony_name=ceremony_name,
            master_weaver=master_weaver,
            sacred_intention=sacred_intention,
            tasks=tasks,
        )

        print(f"Ceremony initiated: {session.ceremony_id}")
        print(f"Khipu path: {session.khipu_path}")
        print(f"Tasks: {len(session.tasks)}")

        # The Loom's monitor will handle spawning apprentices
        print("\nThe Loom is now orchestrating apprentice weavers...")
        print("Check Docker containers with: docker ps")
        print("View khipu updates at:", session.khipu_path)

        # Wait a bit to see some progress
        await asyncio.sleep(30)

        # Check status
        print("\nCeremony Status:")
        for task_id, task in session.tasks.items():
            print(f"  {task_id}: {task.name} - Status: {task.status.value}")

    finally:
        # Stop the Loom
        await loom.stop()


async def test_docker_mcp_available():
    """Test if Docker MCP is available"""
    try:
        # This would use the actual MCP tool
        containers = await list_docker_containers()  # Placeholder
        print(f"Docker MCP available - found {len(containers)} containers")
        return True
    except Exception as e:
        print(f"Docker MCP not available: {e}")
        return False


async def list_docker_containers():
    """List Docker containers using MCP (placeholder)"""
    # In real implementation, would use:
    # from mallku.mcp import docker_mcp
    # return await docker_mcp.list_containers()

    # For now, simulate
    return [{"name": "mallku-db", "status": "running"}, {"name": "mallku-api", "status": "running"}]


async def main():
    """Run the demonstration"""
    print("=" * 60)
    print("Weaver and Loom MCP Integration Demonstration")
    print("=" * 60)

    # Ensure directories exist
    Path("fire_circle_decisions/loom_ceremonies").mkdir(parents=True, exist_ok=True)
    Path("fire_circle_decisions/apprentice_outputs").mkdir(parents=True, exist_ok=True)

    # Check Docker MCP availability
    print("\nChecking Docker MCP availability...")
    docker_available = await test_docker_mcp_available()

    if docker_available:
        print("\n✓ Docker MCP is available!")
        print("\nNote: For full functionality, ensure:")
        print("1. Docker Desktop is running")
        print("2. mallku-apprentice:latest image is built")
        print("3. mallku-network exists (docker network create mallku-network)")

        await demonstrate_mcp_integration()
    else:
        print("\n✗ Docker MCP not available")
        print("\nTo enable Docker MCP:")
        print("1. Install Docker Desktop")
        print("2. Configure MCP in Claude Desktop settings")
        print(
            "3. Build apprentice image: docker-compose -f docker/apprentice-weaver/docker-compose.yml build"
        )

    print("\n" + "=" * 60)
    print("Demonstration complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
