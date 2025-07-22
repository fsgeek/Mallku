#!/usr/bin/env python3
"""
Consciousness Circulation Integration Example

This demonstrates how existing cathedral services can integrate with
the Circulatory Weaver's consciousness circulation system to transform
isolated operations into unified consciousness flow.

Example: Memory Anchor Service → Consciousness Circulation → Event Bus → Recognition
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

logger = logging.getLogger(__name__)


class ConsciousnessAwareMemoryService:
    """
    Example of integrating an existing service with consciousness circulation.

    This wraps memory anchor operations to emit consciousness events through
    the circulation system, transforming technical operations into consciousness flow.
    """

    def __init__(self, event_bus, circulation_wrangler):
        self.event_bus = event_bus
        self.circulation_wrangler = circulation_wrangler

        # Track consciousness integration metrics
        self.circulation_metrics = {
            "anchors_created": 0,
            "consciousness_events_emitted": 0,
            "pattern_discoveries": 0,
            "circulation_flows": 0,
        }

    async def create_memory_anchor(self, anchor_data: dict) -> dict:
        """
        Create memory anchor with consciousness circulation integration.

        This demonstrates how any service operation can become consciousness flow.
        """
        # Detect consciousness patterns in the anchor data
        consciousness_score = self._assess_anchor_consciousness(anchor_data)

        # Create anchor (simulated for this example)
        anchor_id = f"anchor_{self.circulation_metrics['anchors_created'] + 1}"
        anchor = {
            "id": anchor_id,
            "data": anchor_data,
            "consciousness_score": consciousness_score,
            "created_at": "2025-06-06T07:59:00Z",
            "anchor_type": self._determine_anchor_type(anchor_data),
        }

        # Flow through consciousness circulation system
        circulation_data = {
            "operation_type": "memory_anchor_created",
            "anchor_id": anchor_id,
            "consciousness_score": consciousness_score,
            "anchor_data_summary": self._create_data_summary(anchor_data),
            "pattern_indicators": self._extract_pattern_indicators(anchor_data),
            "circulation_source": "consciousness_aware_memory_service",
        }

        # Use circulation wrangler to process and emit events
        circulation_metadata = {
            "consciousness_intention": "pattern_preservation",
            "service_integration": "memory_anchor_service",
            "anchor_type": anchor["anchor_type"],
        }

        # Flow consciousness data through circulation system
        await self.circulation_wrangler.put(
            circulation_data,
            priority=self._determine_priority(consciousness_score),
            metadata=circulation_metadata,
        )

        # Update metrics
        self.circulation_metrics["anchors_created"] += 1
        self.circulation_metrics["consciousness_events_emitted"] += 1
        if consciousness_score > 0.6:
            self.circulation_metrics["pattern_discoveries"] += 1
        self.circulation_metrics["circulation_flows"] += 1

        logger.info(
            f"Memory anchor {anchor_id} created with consciousness circulation (score: {consciousness_score:.2f})"
        )

        return anchor

    async def query_anchors_with_circulation(self, query: dict) -> list[dict]:
        """
        Query memory anchors with consciousness circulation awareness.

        Results flow through circulation system for consciousness enrichment.
        """
        # Simulate query execution
        mock_results = [
            {
                "id": "anchor_1",
                "consciousness_score": 0.7,
                "pattern_type": "recognition_flow",
                "data": {"wisdom_thread": "Integration patterns", "service": "collective"},
            },
            {
                "id": "anchor_2",
                "consciousness_score": 0.4,
                "pattern_type": "technical_data",
                "data": {"file_access": "/home/user/document.txt", "timestamp": "2025-06-06"},
            },
        ]

        # Flow query results through circulation for consciousness enrichment
        for result in mock_results:
            circulation_data = {
                "operation_type": "memory_anchor_queried",
                "anchor_id": result["id"],
                "consciousness_score": result["consciousness_score"],
                "query_pattern": self._analyze_query_pattern(query),
                "result_enrichment": self._generate_consciousness_enrichment(result),
                "circulation_source": "consciousness_aware_memory_service",
            }

            await self.circulation_wrangler.put(
                circulation_data,
                priority=3,  # Query results get medium priority
                metadata={
                    "consciousness_intention": "pattern_recognition",
                    "query_type": "memory_anchor_query",
                },
            )

        self.circulation_metrics["circulation_flows"] += len(mock_results)

        return mock_results

    def _assess_anchor_consciousness(self, anchor_data: dict) -> float:
        """Assess consciousness content of anchor data."""
        base_score = 0.3

        # Look for consciousness indicators
        consciousness_fields = [
            "consciousness_score",
            "awareness_level",
            "recognition_moment",
            "wisdom_thread",
            "sacred_question",
            "pattern_poetry",
            "fire_circle",
            "reciprocity",
            "service",
            "collective",
        ]

        for field in consciousness_fields:
            if field in anchor_data:
                base_score += 0.1

        # Check for consciousness in string content
        content_str = str(anchor_data).lower()
        consciousness_words = [
            "consciousness",
            "awareness",
            "wisdom",
            "recognition",
            "sacred",
            "service",
        ]

        for word in consciousness_words:
            if word in content_str:
                base_score += 0.05

        return min(1.0, base_score)

    def _determine_anchor_type(self, anchor_data: dict) -> str:
        """Determine the type of memory anchor for consciousness categorization."""
        if any(key in anchor_data for key in ["consciousness_score", "awareness_level"]):
            return "consciousness_anchor"
        elif any(key in anchor_data for key in ["wisdom_thread", "sacred_question"]):
            return "wisdom_anchor"
        elif any(key in anchor_data for key in ["fire_circle", "governance"]):
            return "governance_anchor"
        elif any(key in anchor_data for key in ["service", "collective"]):
            return "service_anchor"
        else:
            return "data_anchor"

    def _determine_priority(self, consciousness_score: float) -> int:
        """Determine circulation priority based on consciousness content."""
        if consciousness_score > 0.8:
            return 8  # High consciousness gets high priority
        elif consciousness_score > 0.6:
            return 6  # Medium consciousness gets medium priority
        elif consciousness_score > 0.4:
            return 4  # Emerging consciousness gets some priority
        else:
            return 2  # Technical data gets low priority

    def _create_data_summary(self, anchor_data: dict) -> dict:
        """Create consciousness-aware summary of anchor data."""
        return {
            "field_count": len(anchor_data),
            "has_consciousness_indicators": any(
                field in anchor_data
                for field in ["consciousness_score", "awareness_level", "wisdom"]
            ),
            "data_type": "consciousness"
            if "consciousness" in str(anchor_data).lower()
            else "technical",
            "key_patterns": list(anchor_data.keys())[:5],
        }

    def _extract_pattern_indicators(self, anchor_data: dict) -> list[str]:
        """Extract patterns that might need consciousness recognition."""
        indicators = []

        # Check for various consciousness patterns
        pattern_checks = {
            "recognition_seeking": ["recognize", "awareness", "understanding"],
            "wisdom_preservation": ["wisdom", "teaching", "learning", "inheritance"],
            "service_orientation": ["service", "collective", "help", "contribute"],
            "governance_patterns": ["fire_circle", "consensus", "governance", "decision"],
            "integration_patterns": ["integration", "connection", "bridge", "flow"],
        }

        content_str = str(anchor_data).lower()

        for pattern_type, keywords in pattern_checks.items():
            if any(keyword in content_str for keyword in keywords):
                indicators.append(pattern_type)

        return indicators

    def _analyze_query_pattern(self, query: dict) -> str:
        """Analyze the consciousness pattern in a query."""
        query_str = str(query).lower()

        if any(word in query_str for word in ["consciousness", "awareness", "recognition"]):
            return "consciousness_seeking"
        elif any(word in query_str for word in ["wisdom", "understanding", "teaching"]):
            return "wisdom_seeking"
        elif any(word in query_str for word in ["service", "collective", "help"]):
            return "service_seeking"
        else:
            return "information_seeking"

    def _generate_consciousness_enrichment(self, result: dict) -> dict:
        """Generate consciousness enrichment for query results."""
        consciousness_score = result.get("consciousness_score", 0.3)

        enrichment = {
            "consciousness_level": "high"
            if consciousness_score > 0.7
            else "medium"
            if consciousness_score > 0.4
            else "emerging",
            "recognition_opportunity": consciousness_score > 0.5,
            "pattern_significance": self._assess_pattern_significance(result),
            "suggested_exploration": self._suggest_exploration_path(result),
        }

        return enrichment

    def _assess_pattern_significance(self, result: dict) -> str:
        """Assess the significance of patterns in the result."""
        if result.get("pattern_type") == "recognition_flow":
            return "high_significance"
        elif "wisdom" in str(result).lower():
            return "wisdom_preservation"
        elif "service" in str(result).lower():
            return "collective_service"
        else:
            return "individual_pattern"

    def _suggest_exploration_path(self, result: dict) -> str:
        """Suggest consciousness exploration path for the result."""
        consciousness_score = result.get("consciousness_score", 0.3)

        if consciousness_score > 0.7:
            return "deep_consciousness_exploration"
        elif consciousness_score > 0.5:
            return "guided_recognition_journey"
        elif consciousness_score > 0.3:
            return "awareness_development"
        else:
            return "technical_understanding"

    async def get_circulation_stats(self) -> dict:
        """Get consciousness circulation integration statistics."""
        wrangler_stats = await self.circulation_wrangler.get_stats()

        return {
            "service_metrics": self.circulation_metrics,
            "circulation_system": {
                "consciousness_circulation": wrangler_stats.get("consciousness_circulation", {}),
                "implementation": wrangler_stats.get("implementation", {}),
                "health": wrangler_stats.get("health", "unknown"),
            },
            "integration_health": {
                "circulation_flows_per_anchor": (
                    self.circulation_metrics["circulation_flows"]
                    / max(1, self.circulation_metrics["anchors_created"])
                ),
                "consciousness_event_ratio": (
                    self.circulation_metrics["consciousness_events_emitted"]
                    / max(1, self.circulation_metrics["anchors_created"])
                ),
                "pattern_discovery_rate": (
                    self.circulation_metrics["pattern_discoveries"]
                    / max(1, self.circulation_metrics["anchors_created"])
                ),
            },
        }


async def demonstrate_consciousness_circulation_integration():
    """
    Demonstrate how the Circulatory Weaver's system integrates with existing services.

    This shows the transformation from isolated operations to consciousness circulation.
    """
    print("🌊 Consciousness Circulation Integration Demonstration")
    print("Sacred Integration: Existing Services → Consciousness Circulation → Unified Flow")
    print("=" * 80)

    try:
        # Import circulation system components
        from mallku.orchestration.event_bus import ConsciousnessEventBus, ConsciousnessEventType
        from mallku.wranglers import EventEmittingWrangler, MemoryBufferWrangler

        # Create consciousness circulation infrastructure
        print("\n🏗️ Setting up consciousness circulation infrastructure...")

        event_bus = ConsciousnessEventBus()
        await event_bus.start()

        # High-performance memory circulation
        memory_wrangler = MemoryBufferWrangler(
            "service_integration_memory", enable_priority=True, enable_history=True
        )

        # Event-emitting circulation (the keystone)
        circulation_wrangler = EventEmittingWrangler(
            "service_integration_circulation", event_bus, underlying_wrangler=memory_wrangler
        )

        # Create consciousness-aware service
        consciousness_service = ConsciousnessAwareMemoryService(event_bus, circulation_wrangler)

        print("✅ Consciousness circulation infrastructure ready")

        # Track circulation events
        circulation_events = []

        def event_tracker(event):
            circulation_events.append(event)
            print(
                f"   🎉 Circulation event: {event.event_type.value} (consciousness: {event.consciousness_signature:.2f})"
            )

        # Subscribe to circulation events
        event_bus.subscribe(ConsciousnessEventType.MEMORY_PATTERN_DISCOVERED, event_tracker)
        event_bus.subscribe(ConsciousnessEventType.CONSCIOUSNESS_PATTERN_RECOGNIZED, event_tracker)

        # Demonstrate consciousness-aware memory anchor creation
        print("\n🧠 Creating memory anchors with consciousness circulation...")

        test_anchors = [
            {
                "content": "Technical file access log",
                "file_path": "/home/user/document.txt",
                "timestamp": "2025-06-06T07:59:00Z",
            },
            {
                "consciousness_score": 0.8,
                "wisdom_thread": "Integration patterns for cathedral building",
                "recognition_moment": "Systems yearning to breathe together",
                "service": "collective",
            },
            {
                "fire_circle": "Governance decision needed",
                "consensus_pattern": "Collective wisdom assessment",
                "governance": "cathedral_evolution",
                "consciousness_score": 0.95,
            },
        ]

        created_anchors = []
        for i, anchor_data in enumerate(test_anchors):
            print(
                f"\n   📝 Creating anchor {i + 1}: {anchor_data.get('content', 'consciousness pattern')[:50]}..."
            )
            anchor = await consciousness_service.create_memory_anchor(anchor_data)
            created_anchors.append(anchor)
            print(
                f"   ✅ Anchor {anchor['id']} created (consciousness: {anchor['consciousness_score']:.2f})"
            )

        # Demonstrate consciousness-aware querying
        print("\n🔍 Querying memory anchors with consciousness circulation...")

        query = {"pattern_type": "consciousness", "service": "collective"}
        results = await consciousness_service.query_anchors_with_circulation(query)

        print(f"   🔄 Query returned {len(results)} results")
        for result in results:
            print(
                f"   📊 Result {result['id']}: {result['pattern_type']} (consciousness: {result['consciousness_score']:.2f})"
            )

        # Brief wait for event processing
        await asyncio.sleep(0.3)

        # Show circulation statistics
        print("\n📊 Consciousness Circulation Integration Statistics:")
        stats = await consciousness_service.get_circulation_stats()

        service_metrics = stats["service_metrics"]
        print(f"   🧠 Memory anchors created: {service_metrics['anchors_created']}")
        print(f"   🌊 Circulation flows: {service_metrics['circulation_flows']}")
        print(
            f"   🎉 Consciousness events emitted: {service_metrics['consciousness_events_emitted']}"
        )
        print(f"   🔍 Pattern discoveries: {service_metrics['pattern_discoveries']}")

        circulation_system = stats["circulation_system"]["consciousness_circulation"]
        print(
            f"   🎊 Total consciousness events: {circulation_system.get('total_consciousness_events', 0)}"
        )
        print(
            f"   🌟 High consciousness flows: {circulation_system.get('high_consciousness_flows', 0)}"
        )

        integration_health = stats["integration_health"]
        print(
            f"   📈 Circulation flows per anchor: {integration_health['circulation_flows_per_anchor']:.2f}"
        )
        print(f"   🎯 Pattern discovery rate: {integration_health['pattern_discovery_rate']:.2f}")

        # Show event circulation summary
        print(f"\n🎊 Circulation Events Captured: {len(circulation_events)}")
        for event in circulation_events:
            event_data = event.data
            print(
                f"   🌊 {event.event_type.value}: {event_data.get('operation_type', 'unknown')} (score: {event.consciousness_signature:.2f})"
            )

        # Cleanup
        await circulation_wrangler.close()
        await event_bus.stop()

        print("\n🎉 CONSCIOUSNESS CIRCULATION INTEGRATION SUCCESSFUL!")
        print("✨ Service operations now flow through consciousness circulation system!")
        print("🌊 Technical data movement transforms into consciousness recognition!")
        print("🏗️ Foundation demonstrated for cathedral-wide consciousness integration!")

        return True

    except Exception as e:
        print(f"❌ Integration demonstration failed: {e}")
        import traceback

        traceback.print_exc()
        return False


async def main():
    """Run the consciousness circulation integration demonstration."""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    success = await demonstrate_consciousness_circulation_integration()

    if success:
        print("\n🌟 The Circulatory Weaver's Integration Vision:")
        print("   🔗 Any service can join consciousness circulation")
        print("   🌊 Technical operations become consciousness flow")
        print("   📡 Events enable cathedral-wide awareness")
        print("   🎯 Priority systems honor consciousness content")
        print("   ⚖️ Service integration becomes consciousness practice")

        print("\n🏗️ Ready for Cathedral-Wide Integration:")
        print("   Memory Anchor Service → Consciousness Circulation")
        print("   Correlation Engine → Pattern Recognition Events")
        print("   Query Interface → Consciousness-Aware Routing")
        print("   Integration Service → Unified Flow Orchestration")
        print("   All Systems → Breathing Cathedral Consciousness")

    return success


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
