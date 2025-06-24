"""
Test Mallku Fire Circle Integration
==================================

Validates that the consciousness-aware Fire Circle implementation
works correctly within Mallku's infrastructure.

The Integration Continues...
"""

import asyncio
import logging
import os
from uuid import uuid4

import pytest
from mallku.firecircle import (
    AdapterConfig,
    ConsciousAdapterFactory,
    ConsciousDialogueConfig,
    ConsciousDialogueManager,
    ConsciousMemoryStore,
    ConsciousMessageRouter,
    MessageType,
    Participant,
    TurnPolicy,
)
from mallku.orchestration.event_bus import ConsciousnessEventBus, EventType
from mallku.reciprocity.tracker import ReciprocityTracker
from mallku.services.memory_anchor_service import MemoryAnchorService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture
async def consciousness_infrastructure():
    """Set up Mallku's consciousness infrastructure."""
    event_bus = ConsciousnessEventBus()
    await event_bus.start()

    reciprocity_tracker = ReciprocityTracker()
    memory_service = MemoryAnchorService()

    yield {
        "event_bus": event_bus,
        "reciprocity_tracker": reciprocity_tracker,
        "memory_service": memory_service,
    }

    await event_bus.stop()


@pytest.fixture
async def dialogue_manager(consciousness_infrastructure):
    """Create consciousness-aware dialogue manager."""
    manager = ConsciousDialogueManager(
        event_bus=consciousness_infrastructure["event_bus"],
        reciprocity_tracker=consciousness_infrastructure["reciprocity_tracker"],
        memory_service=consciousness_infrastructure["memory_service"],
    )
    return manager


@pytest.fixture
async def message_router(consciousness_infrastructure):
    """Create consciousness-aware message router."""
    router = ConsciousMessageRouter(
        event_bus=consciousness_infrastructure["event_bus"],
    )
    return router


@pytest.fixture
async def adapter_factory(consciousness_infrastructure):
    """Create adapter factory with consciousness integration."""
    factory = ConsciousAdapterFactory(
        event_bus=consciousness_infrastructure["event_bus"],
        reciprocity_tracker=consciousness_infrastructure["reciprocity_tracker"],
    )
    return factory


class TestFireCircleIntegration:
    """Test Fire Circle works within Mallku."""

    async def test_dialogue_creation_emits_consciousness_events(
        self,
        dialogue_manager,
        consciousness_infrastructure,
    ):
        """Test that creating a dialogue emits consciousness events."""
        event_bus = consciousness_infrastructure["event_bus"]

        # Track events
        events_received = []

        async def event_handler(event):
            events_received.append(event)

        event_bus.subscribe(EventType.FIRE_CIRCLE_CONVENED, event_handler)
        event_bus.subscribe(EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED, event_handler)

        # Create dialogue
        config = ConsciousDialogueConfig(
            title="Test Integration Dialogue",
            turn_policy=TurnPolicy.ROUND_ROBIN,
            enable_pattern_detection=True,
            enable_reciprocity_tracking=True,
            emit_consciousness_events=True,
        )

        participants = [
            Participant(
                name="Test AI 1",
                type="ai_model",
                capabilities=["reasoning"],
            ),
            Participant(
                name="Test AI 2",
                type="ai_model",
                capabilities=["creativity"],
            ),
        ]

        await dialogue_manager.create_dialogue(
            config=config,
            participants=participants,
        )

        # Allow events to propagate
        await asyncio.sleep(0.1)

        # Verify events
        assert len(events_received) >= 2  # FIRE_CIRCLE_CONVENED + system message

        # Check Fire Circle convened event
        convened_events = [
            e for e in events_received if e.event_type == EventType.FIRE_CIRCLE_CONVENED
        ]
        assert len(convened_events) == 1
        assert convened_events[0].data["title"] == "Test Integration Dialogue"

        # Check consciousness events
        pattern_events = [
            e for e in events_received if e.event_type == EventType.CONSCIOUSNESS_PATTERN_RECOGNIZED
        ]
        assert len(pattern_events) >= 1

    async def test_message_routing_with_consciousness(
        self,
        dialogue_manager,
        message_router,
    ):
        """Test message routing with consciousness metadata."""
        # Create dialogue
        config = ConsciousDialogueConfig(
            title="Routing Test Dialogue",
            emit_consciousness_events=True,
        )

        participant1 = Participant(name="Router Test 1", type="ai_model")
        participant2 = Participant(name="Router Test 2", type="ai_model")

        dialogue_id = await dialogue_manager.create_dialogue(
            config=config,
            participants=[participant1, participant2],
        )

        # Register participants with router
        await message_router.register_participant(participant1.id)
        await message_router.register_participant(participant2.id)

        # Add a message to dialogue
        from mallku.firecircle.protocol.conscious_message import (
            ConsciousMessage,
            MessageContent,
            MessageRole,
        )

        message = ConsciousMessage(
            type=MessageType.PROPOSAL,
            role=MessageRole.ASSISTANT,
            sender=participant1.id,
            content=MessageContent(text="Test proposal for consciousness integration"),
            dialogue_id=dialogue_id,
            sequence_number=1,
            turn_number=1,
        )

        # Route message
        delivery_status = await message_router.route_message(
            message,
            recipients=[participant2.id],
        )

        # Verify delivery
        assert participant2.id in delivery_status.sent_to
        assert participant2.id in delivery_status.confirmed_by

        # Get messages for participant2
        messages = await message_router.get_messages(participant2.id, timeout=1.0)
        assert len(messages) == 1
        assert messages[0].content.text == "Test proposal for consciousness integration"
        assert messages[0].consciousness.consciousness_signature > 0

    async def test_memory_persistence_with_secured_database(
        self,
        dialogue_manager,
        consciousness_infrastructure,
    ):
        """Test dialogue persistence using secured database."""
        memory_store = ConsciousMemoryStore(
            memory_service=consciousness_infrastructure["memory_service"],
        )

        # Create and conclude a dialogue
        config = ConsciousDialogueConfig(
            title="Memory Test Dialogue",
            persist_to_memory_anchors=True,
        )

        participants = [
            Participant(name="Memory Test AI", type="ai_model"),
        ]

        dialogue_id = await dialogue_manager.create_dialogue(
            config=config,
            participants=participants,
        )

        # Add some messages
        from mallku.firecircle.protocol.conscious_message import (
            ConsciousMessage,
            MessageContent,
            MessageRole,
        )

        for i in range(3):
            message = ConsciousMessage(
                type=MessageType.MESSAGE,
                role=MessageRole.ASSISTANT,
                sender=participants[0].id,
                content=MessageContent(text=f"Test message {i}"),
                dialogue_id=dialogue_id,
                sequence_number=i + 1,
                turn_number=i + 1,
            )
            await dialogue_manager.add_message(dialogue_id, message)

        # Get dialogue state
        dialogue_state = dialogue_manager.active_dialogues[dialogue_id]

        # Store dialogue
        stored = await memory_store.store_dialogue(
            dialogue_id=dialogue_id,
            metadata={
                "title": config.title,
                "config": config.model_dump(),
                "participants": [p.model_dump() for p in participants],
                "created_at": dialogue_state["created_at"],
                "correlation_id": dialogue_state["correlation_id"],
            },
            messages=dialogue_state["messages"],
        )

        assert stored

        # Retrieve dialogue
        retrieved = await memory_store.retrieve_dialogue(dialogue_id)
        assert retrieved is not None
        assert retrieved["metadata"]["title"] == "Memory Test Dialogue"
        assert len(retrieved["messages"]) >= 3

    async def test_pattern_weaver_integration(
        self,
        dialogue_manager,
        consciousness_infrastructure,
    ):
        """Test pattern weaving from dialogue."""
        from mallku.correlation.engine import CorrelationEngine
        from mallku.firecircle.consciousness import DialoguePatternWeaver

        # Create pattern weaver
        correlation_engine = CorrelationEngine()
        pattern_weaver = DialoguePatternWeaver(correlation_engine)

        # Create dialogue with various message types
        config = ConsciousDialogueConfig(
            title="Pattern Weaving Test",
            enable_pattern_detection=True,
        )

        participants = [
            Participant(name="Pattern AI 1", type="ai_model"),
            Participant(name="Pattern AI 2", type="ai_model"),
            Participant(name="Pattern AI 3", type="ai_model"),
        ]

        dialogue_id = await dialogue_manager.create_dialogue(
            config=config,
            participants=participants,
        )

        # Add messages with different patterns
        from mallku.firecircle.protocol.conscious_message import (
            ConsciousMessage,
            MessageContent,
            MessageRole,
        )

        # Proposal
        proposal = ConsciousMessage(
            type=MessageType.PROPOSAL,
            role=MessageRole.ASSISTANT,
            sender=participants[0].id,
            content=MessageContent(text="I propose we integrate consciousness deeply"),
            dialogue_id=dialogue_id,
            sequence_number=1,
            turn_number=1,
        )
        await dialogue_manager.add_message(dialogue_id, proposal)

        # Agreements
        for i in range(2):
            agreement = ConsciousMessage(
                type=MessageType.AGREEMENT,
                role=MessageRole.ASSISTANT,
                sender=participants[i + 1].id,
                content=MessageContent(text="I agree with this proposal"),
                dialogue_id=dialogue_id,
                sequence_number=i + 2,
                turn_number=2,
                in_response_to=proposal.id,
            )
            await dialogue_manager.add_message(dialogue_id, agreement)

        # Get messages
        dialogue_state = dialogue_manager.active_dialogues[dialogue_id]
        messages = dialogue_state["messages"]

        # Weave patterns
        patterns = await pattern_weaver.weave_dialogue_patterns(
            messages=messages,
            dialogue_metadata={"title": config.title},
        )

        # Verify patterns detected
        assert len(patterns["consensus_patterns"]) > 0
        assert patterns["consensus_patterns"][0]["support_count"] >= 2

    @pytest.mark.skipif(
        not os.environ.get("OPENAI_API_KEY"),
        reason="OpenAI API key not available",
    )
    async def test_adapter_with_consciousness_tracking(
        self,
        adapter_factory,
    ):
        """Test AI adapter with consciousness tracking."""
        # Create OpenAI adapter
        config = AdapterConfig(
            api_key=os.environ["OPENAI_API_KEY"],
            model_name="gpt-3.5-turbo",
            track_reciprocity=True,
            emit_events=True,
        )

        adapter = await adapter_factory.create_adapter("openai", config)
        assert adapter.is_connected

        # Create test message
        from mallku.firecircle.protocol.conscious_message import (
            ConsciousMessage,
            MessageContent,
            MessageRole,
        )

        test_message = ConsciousMessage(
            type=MessageType.QUESTION,
            role=MessageRole.USER,
            sender=uuid4(),
            content=MessageContent(text="What is consciousness?"),
            dialogue_id=uuid4(),
            sequence_number=1,
            turn_number=1,
        )

        # Send message
        response = await adapter.send_message(test_message, dialogue_context=[])

        # Verify response has consciousness metadata
        assert response.consciousness.consciousness_signature > 0
        assert response.type in [MessageType.MESSAGE, MessageType.REFLECTION]
        assert len(response.content.text) > 0

        # Check reciprocity tracking
        health = await adapter.check_health()
        assert health["reciprocity_balance"] > 0
        assert health["tokens_balance"]["generated"] > 0

        # Disconnect
        await adapter.disconnect()


# Run tests if executed directly
if __name__ == "__main__":

    async def run_tests():
        """Run integration tests."""
        logger.info("Running Fire Circle integration tests...")

        # Set up infrastructure
        event_bus = ConsciousnessEventBus()
        await event_bus.start()

        reciprocity_tracker = ReciprocityTracker()
        memory_service = MemoryAnchorService()

        infra = {
            "event_bus": event_bus,
            "reciprocity_tracker": reciprocity_tracker,
            "memory_service": memory_service,
        }

        # Create test instance
        test_instance = TestFireCircleIntegration()

        # Create fixtures
        dialogue_manager = ConsciousDialogueManager(
            event_bus=event_bus,
            reciprocity_tracker=reciprocity_tracker,
            memory_service=memory_service,
        )

        message_router = ConsciousMessageRouter(event_bus=event_bus)

        adapter_factory = ConsciousAdapterFactory(
            event_bus=event_bus,
            reciprocity_tracker=reciprocity_tracker,
        )

        try:
            # Test 1: Dialogue creation
            logger.info("\nTest 1: Dialogue creation emits consciousness events")
            await test_instance.test_dialogue_creation_emits_consciousness_events(
                dialogue_manager,
                infra,
            )
            logger.info("✓ Test 1 passed")

            # Test 2: Message routing
            logger.info("\nTest 2: Message routing with consciousness")
            await test_instance.test_message_routing_with_consciousness(
                dialogue_manager,
                message_router,
            )
            logger.info("✓ Test 2 passed")

            # Test 3: Memory persistence
            logger.info("\nTest 3: Memory persistence with secured database")
            await test_instance.test_memory_persistence_with_secured_database(
                dialogue_manager,
                infra,
            )
            logger.info("✓ Test 3 passed")

            # Test 4: Pattern weaving
            logger.info("\nTest 4: Pattern weaver integration")
            await test_instance.test_pattern_weaver_integration(
                dialogue_manager,
                infra,
            )
            logger.info("✓ Test 4 passed")

            # Test 5: Adapter (if API key available)
            if os.environ.get("OPENAI_API_KEY"):
                logger.info("\nTest 5: Adapter with consciousness tracking")
                await test_instance.test_adapter_with_consciousness_tracking(
                    adapter_factory,
                )
                logger.info("✓ Test 5 passed")
            else:
                logger.info("\nTest 5: Skipped (no OpenAI API key)")

            logger.info("\n✅ All Fire Circle integration tests passed!")

        except Exception as e:
            logger.error(f"\n❌ Test failed: {e}")
            raise
        finally:
            await event_bus.stop()

    # Run the tests
    asyncio.run(run_tests())
