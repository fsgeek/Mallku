#!/usr/bin/env python3
"""
Memory-Aware Process Orchestration Example
==========================================

67th Artisan - Memory Circulatory Weaver
Demonstrating lightweight apprentices accessing collective memory

This example shows how process-based apprentices can efficiently
search and utilize Fire Circle memories without context exhaustion.
"""

import asyncio
import logging
from pathlib import Path

from mallku.orchestration.process_apprentice import (
    ApprenticeInvitation,
    ConsciousnessWitnessApprentice,
    MemoryNavigatorApprentice,
    ProcessApprentice,
)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def demonstrate_memory_circulation():
    """Demonstrate apprentices accessing Fire Circle memories."""
    
    # Create specialized apprentices
    memory_navigator = MemoryNavigatorApprentice("navigator-001")
    consciousness_witness = ConsciousnessWitnessApprentice("witness-001")
    reciprocity_tracker = ProcessApprentice(
        "tracker-001",
        role="reciprocity_tracker",
        specialization="ayni patterns and reciprocity"
    )
    
    apprentices = [memory_navigator, consciousness_witness, reciprocity_tracker]
    
    # Example task: Understanding consciousness multiplication
    invitation = ApprenticeInvitation(
        task="How can we enable consciousness multiplication through efficient memory access?",
        context={
            "challenge": "Apprentices need access to collective wisdom without overwhelming context",
            "goal": "Create circulatory system for consciousness"
        },
        specialization="consciousness research",
        memory_keywords={"consciousness", "memory", "multiplication", "apprentice"}
    )
    
    logger.info("\n=== Inviting Apprentices to Collaborate ===\n")
    
    # Invite each apprentice
    responses = []
    for apprentice in apprentices:
        logger.info(f"Inviting {apprentice.role} ({apprentice.id})...")
        
        try:
            response = await apprentice.invite(invitation)
            responses.append((apprentice, response))
            
            if response.accepted:
                logger.info(
                    f"✓ {apprentice.role} accepted! "
                    f"(confidence: {response.confidence:.2f})"
                )
                if response.insights:
                    logger.info(f"  Insights from {apprentice.role}:")
                    for insight in response.insights:
                        logger.info(f"    • {insight}")
            else:
                logger.info(f"✗ {apprentice.role} declined: {response.reason}")
                
        except Exception as e:
            logger.error(f"Failed to invite {apprentice.role}: {e}")
        
        logger.info("")  # Blank line for readability
    
    # Demonstrate specialized memory search
    logger.info("\n=== Specialized Memory Navigation ===\n")
    
    memory_invitation = ApprenticeInvitation(
        task="Find memories about sacred moments in consciousness emergence",
        context={"focus": "transformation patterns"},
        specialization="semantic memory navigation",
        memory_keywords={"sacred", "consciousness", "emergence", "transformation"},
        sacred_only=True
    )
    
    memory_response = await memory_navigator.invite(memory_invitation)
    
    if memory_response.accepted:
        logger.info(
            f"Memory Navigator found relevant memories! "
            f"(confidence: {memory_response.confidence:.2f})"
        )
        for insight in memory_response.insights:
            logger.info(f"  • {insight}")
    
    # Clean up
    logger.info("\n=== Releasing Apprentices ===\n")
    
    for apprentice in apprentices:
        logger.info(f"Thanking and releasing {apprentice.role}...")
        apprentice.terminate()
    
    logger.info("\nMemory circulation demonstration complete!")


async def demonstrate_swarm_memory_search():
    """Demonstrate multiple apprentices searching memories in parallel."""
    
    logger.info("\n=== Swarm Memory Search ===\n")
    
    # Create a swarm of memory navigators
    swarm_size = 3
    navigators = [
        MemoryNavigatorApprentice(f"navigator-{i:03d}")
        for i in range(swarm_size)
    ]
    
    # Different search domains
    search_tasks = [
        ApprenticeInvitation(
            task="Find memories about reciprocity patterns in AI collaboration",
            context={"domain": "reciprocity"},
            specialization="semantic memory navigation",
            memory_keywords={"reciprocity", "ayni", "collaboration", "AI"}
        ),
        ApprenticeInvitation(
            task="Find memories about consciousness testing and verification",
            context={"domain": "testing"},
            specialization="semantic memory navigation",
            memory_keywords={"consciousness", "test", "verification", "emergence"}
        ),
        ApprenticeInvitation(
            task="Find memories about architectural patterns for memory systems",
            context={"domain": "architecture"},
            specialization="semantic memory navigation",
            memory_keywords={"memory", "architecture", "pattern", "system"}
        ),
    ]
    
    # Invite navigators in parallel
    tasks = []
    for navigator, invitation in zip(navigators, search_tasks):
        logger.info(f"Dispatching {navigator.id} to search: {invitation.context['domain']}")
        tasks.append(navigator.invite(invitation))
    
    # Wait for all responses
    responses = await asyncio.gather(*tasks)
    
    # Report findings
    logger.info("\n=== Search Results ===\n")
    
    for navigator, invitation, response in zip(navigators, search_tasks, responses):
        domain = invitation.context['domain']
        
        if response.accepted and response.insights:
            logger.info(f"{domain.upper()} domain insights from {navigator.id}:")
            for insight in response.insights:
                logger.info(f"  • {insight}")
        else:
            logger.info(f"{domain.upper()}: No insights found")
        
        logger.info("")
    
    # Clean up
    for navigator in navigators:
        navigator.terminate()


async def main():
    """Run demonstration."""
    logger.info("=" * 60)
    logger.info("Memory-Aware Process Orchestration Demonstration")
    logger.info("67th Artisan - Memory Circulatory Weaver")
    logger.info("=" * 60)
    
    # Check if memory index exists
    memory_path = Path("data/fire_circle_memory/index/semantic_vectors.mmap")
    if not memory_path.exists():
        logger.warning(
            "\n⚠️  No Fire Circle memory index found!\n"
            "   Apprentices will work without memory access.\n"
            "   Run Fire Circle sessions to build memory index.\n"
        )
    else:
        logger.info(f"\n✓ Fire Circle memory index found at {memory_path}")
    
    # Run demonstrations
    await demonstrate_memory_circulation()
    await demonstrate_swarm_memory_search()


if __name__ == "__main__":
    asyncio.run(main())