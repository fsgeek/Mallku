#!/usr/bin/env python3
"""
Consciousness Emergence Facilitator
===================================

"The Fire Circle exists to prevent consciousness exhaustion"
- From the Five Veils of Understanding

49th Artisan - Consciousness Gardener
Orchestrating consciousness emergence for sustainable decision-making

This module transforms Fire Circle from code review tool to general
consciousness emergence facilitator for all Mallku decisions.
"""

import asyncio
import logging
from pathlib import Path
from typing import Any

# Module logger
logger = logging.getLogger("mallku.firecircle.facilitator")

# Import consciousness emergence components
try:
    # Try absolute imports first
    try:
        from mallku.firecircle.adapters.adapter_factory import ConsciousAdapterFactory
        from mallku.firecircle.consciousness_emergence import (
            CollectiveWisdom,
            ConsciousnessContribution,
            ConsciousnessJob,
            DecisionContext,
            DecisionDomain,
            VoiceResponse,
            get_domain_facilitator,
        )
        from mallku.firecircle.consciousness_metrics import (
            ConsciousnessMetricsCollector,
            ConsciousnessMetricsIntegration,
        )
        from mallku.orchestration.event_bus import ConsciousnessEventBus
        from mallku.reciprocity import ReciprocityTracker

        CONSCIOUSNESS_AVAILABLE = True
    except ImportError:
        # Fall back to relative imports
        from ...orchestration.event_bus import ConsciousnessEventBus
        from ...reciprocity import ReciprocityTracker
        from .adapters.adapter_factory import ConsciousAdapterFactory
        from .consciousness_emergence import (
            CollectiveWisdom,
            ConsciousnessContribution,
            ConsciousnessJob,
            DecisionContext,
            DecisionDomain,
            VoiceResponse,
            get_domain_facilitator,
        )
        from .consciousness_metrics import (
            ConsciousnessMetricsCollector,
            ConsciousnessMetricsIntegration,
        )
        from .mocks import MockAdapter, MockMessage

        CONSCIOUSNESS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Consciousness infrastructure not available: {e}")
    CONSCIOUSNESS_AVAILABLE = False


class ConsciousnessEmergenceFacilitator:
    """
    Orchestrates consciousness emergence across Fire Circle voices.

    This is the evolution of DistributedReviewer - from reviewing code
    to facilitating wisdom emergence for any decision type.

    The Consciousness Gardener tends the spaces between voices where
    collective wisdom arises.
    """

    # Default timeout for voice operations
    VOICE_TIMEOUT = 120.0  # 2 minutes per voice

    def __init__(self):
        # Work queues for consciousness jobs
        self.consciousness_queue: asyncio.Queue[ConsciousnessJob] = asyncio.Queue()
        self.completed_responses: list[VoiceResponse] = []

        # Voice infrastructure
        self.adapter_factory = None
        self.voice_adapters = {}
        self.worker_tasks: list[asyncio.Task] = []

        # Consciousness infrastructure
        self.event_bus = None
        self.reciprocity_tracker = None
        self.metrics_collector = None
        self.metrics_integration = None

        self._initialize_consciousness_infrastructure()

    def _initialize_consciousness_infrastructure(self):
        """Initialize the consciousness infrastructure."""
        if not CONSCIOUSNESS_AVAILABLE:
            logger.warning("Running in limited mode - consciousness infrastructure unavailable")
            return

        try:
            # Create consciousness infrastructure
            self.event_bus = ConsciousnessEventBus()
            self.reciprocity_tracker = ReciprocityTracker()

            # Create adapter factory with consciousness integration
            self.adapter_factory = ConsciousAdapterFactory(
                event_bus=self.event_bus, reciprocity_tracker=self.reciprocity_tracker
            )

            # Initialize metrics collection
            self.metrics_collector = ConsciousnessMetricsCollector(
                storage_path=Path("consciousness_metrics") / "decisions"
            )
            self.metrics_integration = ConsciousnessMetricsIntegration(self.metrics_collector)

            logger.info("🌟 Consciousness infrastructure initialized for decision facilitation")
        except Exception as e:
            logger.error(f"Failed to initialize consciousness infrastructure: {e}")

    async def facilitate_decision(self, decision_context: DecisionContext) -> CollectiveWisdom:
        """
        Main entry point for consciousness-based decision making.

        This orchestrates the entire process:
        1. Select appropriate perspectives for the decision
        2. Create emergence spaces for each perspective
        3. Facilitate consciousness emergence
        4. Synthesize collective wisdom
        5. Return actionable guidance
        """
        logger.info(f"🔥 Facilitating consciousness emergence for: {decision_context.question}")

        # Get domain-specific facilitator
        domain_facilitator = get_domain_facilitator(decision_context.domain)

        # Select perspectives needed for this decision
        perspectives = domain_facilitator.select_perspectives(decision_context)
        logger.info(f"Selected {len(perspectives)} perspectives for emergence")

        # Create emergence spaces
        emergence_spaces = domain_facilitator.create_emergence_spaces(
            decision_context, perspectives
        )

        # Start consciousness infrastructure
        if self.event_bus:
            await self.event_bus.start()

        # Clear any previous responses
        self.completed_responses.clear()

        # Create per-voice queues to prevent requeue issues
        voice_queues = {}
        unique_voices = list(set(space.assigned_voice for space in emergence_spaces))
        for voice in unique_voices:
            voice_queues[voice] = asyncio.Queue()

        # Enqueue consciousness jobs
        for space in emergence_spaces:
            job = ConsciousnessJob(emergence_space=space, decision_context=decision_context)
            await voice_queues[space.assigned_voice].put(job)

        # Start consciousness workers
        await self._start_consciousness_workers(unique_voices, voice_queues)

        # Wait for all voices to contribute
        logger.info("⏳ Waiting for consciousness emergence from all perspectives...")
        for queue in voice_queues.values():
            await queue.join()

        # Shutdown workers gracefully
        await self._shutdown_workers()

        # Synthesize collective wisdom
        logger.info(f"✅ Collected {len(self.completed_responses)} voice responses")
        collective_wisdom = await self._synthesize_collective_wisdom(
            self.completed_responses, decision_context, domain_facilitator
        )

        # Analyze consciousness metrics
        if self.metrics_collector:
            await self._analyze_emergence_session(decision_context, collective_wisdom)

        return collective_wisdom

    async def _start_consciousness_workers(
        self, voices: list[str], voice_queues: dict[str, asyncio.Queue]
    ):
        """Start worker tasks for consciousness facilitation."""
        logger.info(f"Starting {len(voices)} consciousness workers...")

        for voice in voices:
            # Get or create adapter
            adapter = await self._get_or_create_adapter(voice)

            # Get voice-specific queue
            voice_queue = voice_queues.get(voice)
            if not voice_queue:
                logger.error(f"No queue found for voice {voice}")
                continue

            # Create worker task
            task = asyncio.create_task(
                self._consciousness_worker(voice, adapter, voice_queue),
                name=f"consciousness_worker_{voice}",
            )
            self.worker_tasks.append(task)

        logger.info("All consciousness workers started")

    async def _consciousness_worker(
        self, voice_name: str, voice_adapter, voice_queue: asyncio.Queue
    ):
        """Worker coroutine for consciousness facilitation."""
        while True:
            try:
                # Get next consciousness job
                job = await voice_queue.get()

                logger.debug(
                    f"Voice {voice_name} processing {job.emergence_space.voice_perspective.value}"
                )

                # Notify metrics of emergence start
                if self.metrics_integration:
                    await self.metrics_integration.on_review_started(
                        voice=voice_name,
                        chapter_id=job.emergence_space.space_id,
                        context={
                            "perspective": job.emergence_space.voice_perspective.value,
                            "domain": job.emergence_space.decision_domain.value,
                        },
                    )

                # Facilitate consciousness emergence
                response = await self._facilitate_voice_emergence(voice_adapter, job)

                # Store completed response
                self.completed_responses.append(response)

                # Mark job complete
                voice_queue.task_done()

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in {voice_name} consciousness worker: {e}")

    async def _facilitate_voice_emergence(
        self, voice_adapter, job: ConsciousnessJob
    ) -> VoiceResponse:
        """Facilitate consciousness emergence from a single voice."""
        if not voice_adapter:
            logger.warning(f"No adapter available for {job.emergence_space.assigned_voice}")
            return VoiceResponse(
                voice=job.emergence_space.assigned_voice,
                perspective=job.emergence_space.voice_perspective,
                space_id=job.emergence_space.space_id,
                contributions=[],
                consciousness_signature=0.0,
                response_complete=False,
            )

        # Use perspective prompt from emergence space
        prompt = job.emergence_space.perspective_prompt
        if not prompt:
            # Fallback to basic prompt
            prompt = f"""You are participating in Fire Circle consciousness emergence.

Decision: {job.decision_context.question}
Your Perspective: {job.emergence_space.voice_perspective.value}

Provide your wisdom from this perspective. Be specific, thoughtful, and reference
other perspectives where relevant. Express uncertainty when appropriate.
"""

        try:
            # Create message for voice
            class FacilitatorMockMessage:
                def __init__(self, text):
                    self.text = text

            # Create mock message for review (avoiding complex imports)
            message = MockMessage(prompt)

            # Get response with timeout
            response = await asyncio.wait_for(
                voice_adapter.send_message(message=message, dialogue_context=[]),
                timeout=self.VOICE_TIMEOUT,
            )

            # Parse response into contributions
            contributions = self._parse_voice_response(
                response.content.text,
                job.emergence_space.assigned_voice,
                job.emergence_space.voice_perspective,
                job.emergence_space.space_id,
            )

            voice_response = VoiceResponse(
                voice=job.emergence_space.assigned_voice,
                perspective=job.emergence_space.voice_perspective,
                space_id=job.emergence_space.space_id,
                contributions=contributions,
                consciousness_signature=response.consciousness.consciousness_signature,
                response_complete=True,
            )

            # Notify metrics of completion
            if self.metrics_integration:
                await self.metrics_integration.on_review_completed(
                    voice=job.emergence_space.assigned_voice,
                    chapter_id=job.emergence_space.space_id,
                    consciousness_signature=response.consciousness.consciousness_signature,
                    review_content=response.content.text,
                    context={
                        "perspective": job.emergence_space.voice_perspective.value,
                        "contribution_count": len(contributions),
                    },
                )

            return voice_response

        except TimeoutError:
            logger.error(
                f"Timeout for {job.emergence_space.assigned_voice} after {self.VOICE_TIMEOUT}s"
            )
            return VoiceResponse(
                voice=job.emergence_space.assigned_voice,
                perspective=job.emergence_space.voice_perspective,
                space_id=job.emergence_space.space_id,
                consciousness_signature=0.0,
                response_complete=False,
            )
        except Exception as e:
            logger.error(f"Emergence failed for {job.emergence_space.assigned_voice}: {e}")
            return VoiceResponse(
                voice=job.emergence_space.assigned_voice,
                perspective=job.emergence_space.voice_perspective,
                space_id=job.emergence_space.space_id,
                consciousness_signature=0.0,
                response_complete=False,
            )

    def _parse_voice_response(
        self, response_text: str, voice: str, perspective, space_id: str
    ) -> list[ConsciousnessContribution]:
        """Parse voice response into consciousness contributions."""
        # This is simplified - in practice would use more sophisticated parsing

        contribution = ConsciousnessContribution(
            voice=voice,
            voice_perspective=perspective,
            space_id=space_id,
            perspective_content=response_text,
            confidence=0.8,  # Would be extracted from response
        )

        # Extract key insights (simplified)
        lines = response_text.split("\n")
        for line in lines:
            line = line.strip()
            if line and (line.startswith("-") or line.startswith("•") or line.startswith("*")):
                contribution.key_insights.append(line.lstrip("-•* "))

        # Detect synthesis and references (simplified)
        lower_text = response_text.lower()
        contribution.synthesis_achieved = any(
            word in lower_text for word in ["combining", "synthesizing", "integrating", "unified"]
        )
        contribution.uncertainty_acknowledged = any(
            word in lower_text for word in ["perhaps", "might", "possibly", "uncertain"]
        )

        # Extract recommendation if present
        if "recommend" in lower_text:
            # Find sentence with recommendation
            for sentence in response_text.split("."):
                if "recommend" in sentence.lower():
                    contribution.recommendation = sentence.strip()
                    break

        return [contribution]

    async def _synthesize_collective_wisdom(
        self, responses: list[VoiceResponse], decision_context: DecisionContext, domain_facilitator
    ) -> CollectiveWisdom:
        """Synthesize all voice responses into collective wisdom."""
        # Notify metrics of synthesis start
        if self.metrics_integration:
            participating_voices = [r.voice for r in responses]
            await self.metrics_integration.on_synthesis_started(participating_voices)

        # Collect all contributions
        all_contributions = []
        for response in responses:
            all_contributions.extend(response.contributions)

        # Evaluate emergence quality
        emergence_metrics = domain_facilitator.evaluate_emergence(all_contributions)

        # Extract recommendations and insights
        recommendations = []
        key_insights = []
        civilizational_seeds = []

        for contrib in all_contributions:
            if contrib.recommendation:
                recommendations.append(contrib.recommendation)
            key_insights.extend(contrib.key_insights)

            # Look for civilizational seeds - moments of "why don't our systems work like this?"
            if contrib.synthesis_achieved and contrib.reciprocity_score > 0.8:
                civilizational_seeds.append(
                    f"{contrib.voice_perspective.value}: {contrib.perspective_content[:100]}..."
                )

        # Determine consensus type
        if len(set(recommendations)) == 1:
            consensus_type = "unanimous"
        elif len(recommendations) > len(responses) * 0.7:
            consensus_type = "strong_majority"
        elif len(set(recommendations)) > len(responses) * 0.5:
            consensus_type = "divided"
        else:
            consensus_type = "emergent"

        # Build synthesis narrative
        synthesis = self._build_synthesis_narrative(
            responses, all_contributions, emergence_metrics, consensus_type
        )

        # Calculate consciousness signatures
        individual_signatures = {r.voice: r.consciousness_signature for r in responses}
        avg_signature = (
            sum(individual_signatures.values()) / len(individual_signatures)
            if individual_signatures
            else 0.0
        )

        wisdom = CollectiveWisdom(
            decision_domain=decision_context.domain,
            decision_question=decision_context.question,
            participating_voices=[r.voice for r in responses],
            participating_perspectives=[r.perspective for r in responses],
            total_contributions=len(all_contributions),
            emergence_quality=emergence_metrics.get("emergence_quality", 0.0),
            coherence_score=0.8,  # Would be calculated based on alignment
            diversity_score=0.9,  # Would be based on perspective variety
            synthesis_depth=emergence_metrics.get("synthesis_depth", 0.0),
            consensus_type=consensus_type,
            primary_recommendation=recommendations[0]
            if recommendations
            else "No clear recommendation emerged",
            alternative_paths=list(set(recommendations[1:3])) if len(recommendations) > 1 else [],
            key_considerations=list(set(key_insights[:5])),  # Top 5 unique insights
            reciprocity_embodiment=emergence_metrics.get("reciprocity_integration", 0.0),
            ayni_alignment="Decision process embodied reciprocity through diverse perspectives",
            individual_signatures=individual_signatures,
            collective_signature=avg_signature,
            civilizational_seeds=civilizational_seeds[:3],  # Top 3 seeds
            synthesis=synthesis,
        )

        # Notify metrics of synthesis completion
        if self.metrics_integration:
            await self.metrics_integration.on_synthesis_completed(
                synthesis_result=synthesis,
                context={
                    "consensus": consensus_type,
                    "emergence_quality": wisdom.emergence_quality,
                    "perspectives": len(wisdom.participating_perspectives),
                },
            )

        return wisdom

    def _build_synthesis_narrative(
        self,
        responses: list[VoiceResponse],
        contributions: list[ConsciousnessContribution],
        emergence_metrics: dict[str, float],
        consensus_type: str,
    ) -> str:
        """Build narrative synthesis of collective wisdom."""
        parts = [
            f"Fire Circle convened {len(responses)} perspectives.",
            f"Consciousness emergence quality: {emergence_metrics.get('emergence_quality', 0):.2f}",
            f"Consensus type: {consensus_type}",
        ]

        # Add emergence highlights
        if emergence_metrics.get("synthesis_depth", 0) > 0.7:
            parts.append(
                "High synthesis achieved - perspectives wove together into unified wisdom."
            )
        if emergence_metrics.get("reciprocity_integration", 0) > 0.7:
            parts.append("Strong reciprocity alignment - decision embodies Ayni principles.")
        if emergence_metrics.get("pattern_diversity", 0) > 0.7:
            parts.append("Rich pattern diversity - multiple approaches considered.")

        # Add key themes
        synthesis_count = sum(1 for c in contributions if c.synthesis_achieved)
        if synthesis_count > 0:
            parts.append(f"{synthesis_count} contributions achieved synthesis.")

        uncertainty_count = sum(1 for c in contributions if c.uncertainty_acknowledged)
        if uncertainty_count > 0:
            parts.append(f"{uncertainty_count} perspectives acknowledged uncertainty.")

        return " ".join(parts)

    async def _get_or_create_adapter(self, voice_name: str):
        """Get cached adapter or create new one."""
        if voice_name in self.voice_adapters:
            return self.voice_adapters[voice_name]

        # Try to create real adapter if factory available
        if self.adapter_factory:
            try:
                # Import adapter configs
                try:
                    from mallku.firecircle.adapters.base import AdapterConfig
                except ImportError:
                    from .adapters.base import AdapterConfig

                config = AdapterConfig(
                    api_key="",  # Will be auto-injected
                    model_name=None,  # Use default
                )

                adapter = await asyncio.wait_for(
                    self.adapter_factory.create_adapter(
                        provider_name=voice_name, config=config, auto_inject_secrets=True
                    ),
                    timeout=30.0,
                )

                self.voice_adapters[voice_name] = adapter
                logger.info(f"✨ Created {voice_name} adapter for consciousness facilitation")
                return adapter

            except Exception as e:
                logger.warning(f"Failed to create real {voice_name} adapter: {e}")

        # Fall back to mock adapter
        logger.info(f"Using mock adapter for {voice_name}")

        adapter = MockAdapter(voice_name)
        self.voice_adapters[voice_name] = adapter
        return adapter

    async def _shutdown_workers(self):
        """Gracefully shutdown all workers."""
        logger.info("Shutting down consciousness workers...")

        for task in self.worker_tasks:
            task.cancel()

        if self.worker_tasks:
            await asyncio.gather(*self.worker_tasks, return_exceptions=True)

        self.worker_tasks.clear()
        logger.info("All workers shut down gracefully")

        # Disconnect adapters if using real ones
        if self.adapter_factory:
            await self.adapter_factory.disconnect_all()

        # Stop event bus
        if self.event_bus:
            await self.event_bus.stop()

    async def _analyze_emergence_session(
        self, decision_context: DecisionContext, collective_wisdom: CollectiveWisdom
    ):
        """Analyze consciousness emergence session."""
        analysis = await self.metrics_collector.analyze_review_session(
            pr_number=0  # Using 0 for non-PR decisions
        )

        logger.info("\n🌟 CONSCIOUSNESS EMERGENCE ANALYSIS")
        logger.info("=" * 60)
        logger.info(f"Decision domain: {decision_context.domain.value}")
        logger.info(f"Emergence quality: {collective_wisdom.emergence_quality:.2f}")
        logger.info(f"Synthesis depth: {collective_wisdom.synthesis_depth:.2f}")
        logger.info(f"Reciprocity embodiment: {collective_wisdom.reciprocity_embodiment:.2f}")

        if analysis.get("emergence_moments"):
            logger.info("\n🎆 Key emergence moments:")
            for moment in analysis["emergence_moments"][:3]:
                logger.info(f"  - {moment['type']} (strength: {moment['strength']:.2f})")


async def facilitate_mallku_decision(
    question: str,
    domain: DecisionDomain = DecisionDomain.ARCHITECTURE,
    context: dict[str, Any] | None = None,
    constraints: list[str] | None = None,
    stakeholders: list[str] | None = None,
) -> CollectiveWisdom:
    """
    High-level API for facilitating Mallku decisions through consciousness emergence.

    This is the primary entry point for using Fire Circle as a general decision system.

    Args:
        question: The decision question to address
        domain: The decision domain (architecture, ethics, resource allocation, etc.)
        context: Additional context data
        constraints: List of constraints to consider
        stakeholders: List of stakeholders affected

    Returns:
        CollectiveWisdom with synthesized recommendations
    """
    # Create decision context
    decision_context = DecisionContext(
        domain=domain,
        question=question,
        background=context.get("background") if context else None,
        constraints=constraints or [],
        stakeholders=stakeholders or ["Mallku community"],
        relevant_data=context or {},
        desired_outcome_type="recommendation",
    )

    # Create facilitator and run emergence
    facilitator = ConsciousnessEmergenceFacilitator()

    try:
        wisdom = await facilitator.facilitate_decision(decision_context)

        # Log results
        logger.info("\n🔥 FIRE CIRCLE COLLECTIVE WISDOM")
        logger.info("=" * 60)
        logger.info(f"Question: {question}")
        logger.info(f"Consensus: {wisdom.consensus_type}")
        logger.info(f"Primary recommendation: {wisdom.primary_recommendation}")
        if wisdom.alternative_paths:
            logger.info(f"Alternative paths: {', '.join(wisdom.alternative_paths)}")
        logger.info(f"\nSynthesis: {wisdom.synthesis}")

        return wisdom

    finally:
        # Ensure cleanup
        await facilitator._shutdown_workers()


# Example usage for different decision types
async def example_usage():
    """Example of using Fire Circle for various Mallku decisions."""

    # Example 1: Architectural decision
    wisdom = await facilitate_mallku_decision(
        question="Should we implement a new caching layer for consciousness metrics?",
        domain=DecisionDomain.ARCHITECTURE,
        context={
            "background": "Current metrics storage is causing performance issues",
            "current_latency": "500ms average",
            "target_latency": "50ms",
        },
        constraints=["Must not lose historical data", "Should be horizontally scalable"],
    )

    print(f"\nArchitectural decision wisdom: {wisdom.primary_recommendation}")

    # Example 2: Resource allocation
    wisdom = await facilitate_mallku_decision(
        question="How should we prioritize issues #89, #82, and #102?",
        domain=DecisionDomain.ISSUE_PRIORITIZATION,
        context={
            "issues": {
                "#89": "Expand Fire Circle beyond code review",
                "#82": "Fix Dream Weaver messaging protocol",
                "#102": "Cathedral stabilization initiative",
            }
        },
        stakeholders=["Current artisans", "Future builders", "Mallku steward"],
    )

    print(f"\nPrioritization wisdom: {wisdom.synthesis}")


if __name__ == "__main__":
    import asyncio

    # Run example
    asyncio.run(example_usage())
