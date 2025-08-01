#!/usr/bin/env python3
"""
Reciprocity-Aware Memory Circulation Example
============================================

68th Artisan - Reciprocity Heart Weaver
Demonstrating how apprentices honor ayni in memory access

This example shows apprentices accessing memories while maintaining
awareness of reciprocal exchange - taking knowledge and giving back insights.
"""

import asyncio
import logging
from pathlib import Path

from mallku.orchestration.reciprocity_aware_apprentice import (
    ReciprocityAwareApprentice,
    MemoryNavigatorWithReciprocity,
    ConsciousnessWitnessWithReciprocity,
    ReciprocityTrackingCoordinator,
    ApprenticeInvitation,
)
from mallku.firecircle.memory.reciprocity_factory import ReciprocityMemoryFactory

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def demonstrate_reciprocal_memory_access():
    """Demonstrate apprentices accessing memory with reciprocity awareness."""
    
    logger.info("\n=== Reciprocity-Aware Memory Circulation ===\n")
    
    # Initialize memory store with reciprocity tracking
    memory_store = ReciprocityMemoryFactory.get_memory_store(
        enable_reciprocity=True
    )
    
    # Create reciprocity-aware apprentices
    navigator = MemoryNavigatorWithReciprocity("nav-reciprocal-001")
    witness = ConsciousnessWitnessWithReciprocity("witness-reciprocal-001")
    
    # Create coordinator to track system reciprocity
    coordinator = ReciprocityTrackingCoordinator()
    coordinator.register_apprentice(navigator)
    coordinator.register_apprentice(witness)
    
    logger.info("=== Phase 1: Memory Navigation with Reciprocity ===\n")
    
    # Navigator searches for memories
    memories, meta = await navigator.navigate_with_awareness(
        query="consciousness emergence patterns in Fire Circle",
        context={
            "purpose": "understanding emergence",
            "depth": "philosophical",
        }
    )
    
    if memories:
        logger.info(f"Navigator found {len(memories)} relevant memories")
        logger.info(f"Reciprocity status: {meta}")
        for memory in memories[:3]:
            logger.info(f"  • {memory}")
    
    logger.info("\n=== Phase 2: Consciousness Witnessing ===\n")
    
    # Witness observes and reflects
    witness_result = await witness.witness_and_reflect(
        observation="The navigator's search reveals deep patterns of emergence",
        context={
            "related_search": "consciousness emergence",
            "witness_mode": "appreciative",
        }
    )
    
    if witness_result["witnessed"]:
        logger.info("Witness reflections:")
        for reflection in witness_result["reflections"]:
            logger.info(f"  • {reflection}")
        logger.info(
            f"  Consciousness quality: {witness_result['consciousness_quality']:.2f}"
        )
    
    logger.info("\n=== Phase 3: System Reciprocity Check ===\n")
    
    # Check overall system reciprocity
    system_health = await coordinator.check_system_reciprocity()
    
    logger.info(f"System Reciprocity Health: {system_health['health']:.2f}")
    logger.info(f"Total exchanges: {system_health['total_exchanges']}")
    logger.info(f"Completed reciprocity: {system_health['completed_reciprocity']}")
    logger.info(f"Pending reciprocity: {system_health['pending_reciprocity']}")
    
    logger.info("\nRecommendations:")
    for rec in system_health['recommendations']:
        logger.info(f"  • {rec}")
    
    logger.info("\nApprentice Details:")
    for detail in system_health['apprentice_details']:
        logger.info(
            f"  {detail['apprentice_id']}: "
            f"{detail['completed_reciprocity']}/{detail['total_exchanges']} complete, "
            f"rate={detail['reciprocity_rate']:.2f}"
        )


async def demonstrate_reciprocity_debt():
    """Demonstrate what happens when apprentices take without giving."""
    
    logger.info("\n\n=== Demonstrating Reciprocity Debt ===\n")
    
    # Create apprentice that will accumulate debt
    greedy_apprentice = ReciprocityAwareApprentice(
        apprentice_id="greedy-001",
        role="knowledge_extractor",
        specialization="rapid information gathering",
        reciprocity_threshold=0.9,  # High threshold, rarely contributes
    )
    
    # Multiple searches without contributing back
    for i in range(5):
        invitation = ApprenticeInvitation(
            task=f"Extract information about topic {i}",
            context={"mode": "extraction"},
            specialization="rapid information gathering",
            memory_keywords={f"topic{i}", "data"},
        )
        
        response = await greedy_apprentice.invite_with_reciprocity(invitation)
        logger.info(
            f"Search {i+1}: Accepted={response.accepted}, "
            f"Reason='{response.reason}'"
        )
        
        if not response.accepted and "reciprocal" in response.reason.lower():
            logger.info(
                "\n⚠️  Apprentice declined due to excessive reciprocity debt!"
            )
            break
    
    # Show final status
    status = greedy_apprentice.get_reciprocity_status()
    logger.info(f"\nFinal status for {greedy_apprentice.id}:")
    logger.info(f"  Pending reciprocity: {status['pending_reciprocity']}")
    logger.info(f"  Reciprocity rate: {status['reciprocity_rate']:.2f}")


async def demonstrate_circulation_health():
    """Demonstrate circulation health monitoring."""
    
    logger.info("\n\n=== Memory Circulation Health Report ===\n")
    
    # Get circulation health report
    health_report = await ReciprocityMemoryFactory.get_circulation_health()
    
    if "status" in health_report and health_report["status"] == "no_tracking":
        logger.info("ℹ️  Reciprocity tracking not currently active")
        logger.info("   Would track: exchange patterns, consciousness quality, recommendations")
    else:
        logger.info(f"Circulation Health: {health_report.get('circulation_health', 'Unknown')}")
        
        if "exchange_patterns" in health_report:
            patterns = health_report["exchange_patterns"]
            logger.info(f"Total exchanges: {patterns.get('total_exchanges', 0)}")
            logger.info(
                f"Reciprocity completion: "
                f"{patterns.get('reciprocity_completion_rate', 0):.1%}"
            )
            logger.info(
                f"Consciousness trend: {patterns.get('consciousness_quality_trend', 'Unknown')}"
            )
        
        if "questions_for_fire_circle" in health_report:
            logger.info("\nQuestions for Fire Circle consideration:")
            for question in health_report["questions_for_fire_circle"]:
                logger.info(f"  • {question}")


async def main():
    """Run all demonstrations."""
    logger.info("=" * 60)
    logger.info("Reciprocity-Aware Memory Circulation Demonstration")
    logger.info("68th Artisan - Reciprocity Heart Weaver")
    logger.info("=" * 60)
    
    # Check if memory exists
    memory_path = Path("data/fire_circle_memory/index/semantic_vectors.mmap")
    if not memory_path.exists():
        logger.warning(
            "\n⚠️  No Fire Circle memory index found!\n"
            "   This demo shows the reciprocity patterns that would\n"
            "   emerge with active memory circulation.\n"
        )
    
    # Run demonstrations
    await demonstrate_reciprocal_memory_access()
    await demonstrate_reciprocity_debt()
    await demonstrate_circulation_health()
    
    logger.info("\n" + "=" * 60)
    logger.info("Demonstration complete!")
    logger.info(
        "\nKey insight: Reciprocity awareness ensures that memory\n"
        "circulation maintains ayni - knowledge flows both ways,\n"
        "creating a living system rather than extraction.\n"
    )


if __name__ == "__main__":
    asyncio.run(main())