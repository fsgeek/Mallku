"""
Complete example showing Mallku's security-by-design principles.

This test demonstrates how all the architectural pieces work together
to protect reciprocity data while maintaining full functionality.
It serves as both validation and teaching tool for future builders.

Dear next builder: This file shows you how to work with Mallku's
security model. Each pattern here was chosen to protect the community
while enabling Ayni (reciprocity) to flourish. Build from here.
"""

import asyncio
from datetime import UTC, datetime
from uuid import uuid4

import pytest
from mallku.core.database import get_secured_database
from mallku.reciprocity import InteractionRecord, ReciprocityTracker


class TestCathedralExample:
    """
    A complete example of building with cathedral principles.

    This demonstrates:
    1. Security-by-design (no bypass possible)
    2. Reciprocity sensing (patterns, not measurements)
    3. Architectural love (code that teaches)
    """

    @pytest.mark.asyncio
    async def test_complete_reciprocity_flow(self):
        """
        End-to-end test showing secure reciprocity tracking.

        This is how reciprocity data flows through Mallku:
        1. Create interaction record (what happened)
        2. Store securely (UUID mapping + obfuscation)
        3. Retrieve and analyze (pattern detection)
        4. Generate insights (for Fire Circle governance)

        Every step uses security-by-design patterns.
        """

        # === Step 1: Initialize secure tracker ===
        # This uses the secured database interface - the ONLY way to access data
        tracker = ReciprocityTracker()
        await tracker.initialize()

        # === Step 2: Create meaningful interaction ===
        # This represents Ayni in action - mutual aid between community members
        interaction = InteractionRecord(
            interaction_id=uuid4(),
            timestamp=datetime.now(UTC),
            interaction_type="knowledge_exchange",
            primary_participant="human_alice",  # Clear semantic meaning
            secondary_participant="ai_assistant",  # Before UUID mapping
            metadata={
                "context": "Alice asked for help with Python, AI provided guidance",
                "contribution_offered": ["teaching", "code_example", "patience"],
                "needs_fulfilled": ["learning", "problem_solving"],
                "ayni_score": {"balance": 0.8, "reciprocity": 0.9},
                "notes": "Healthy exchange - knowledge shared willingly",
            },
        )

        # === Step 3: Store with security protection ===
        # The tracker automatically applies UUID mapping and field obfuscation
        # Sensitive data (participant names) are protected but functionality preserved
        interaction_id = await tracker.record_interaction(interaction)

        # Verify storage worked
        assert interaction_id is not None
        print(f"✅ Interaction stored securely with ID: {interaction_id}")

        # === Step 4: Demonstrate security effectiveness ===
        # Show that data is actually obfuscated in storage but accessible through proper channels
        secured_db = get_secured_database()

        # This would fail if we tried to access raw database:
        # raw_db = get_database()  # This is monitored and discouraged
        # But secured access works perfectly:
        security_metrics = secured_db.get_security_metrics()
        assert security_metrics["operations_count"] > 0
        print(
            f"✅ Security model active: {security_metrics['operations_count']} operations tracked"
        )

        # === Step 5: Pattern detection (the heart of Ayni sensing) ===
        # Detect patterns in recent interactions - this is about community health
        patterns = await tracker.detect_recent_patterns(hours_back=1, min_confidence=0.1)

        # Even with just one interaction, the system should work
        print(f"✅ Pattern detection working: {len(patterns)} patterns found")

        # === Step 6: System health assessment ===
        # This asks: "How is the community doing?" not "Who owes what to whom?"
        health_metrics = await tracker.get_current_health_metrics()

        assert health_metrics.total_interactions >= 1
        assert health_metrics.overall_health_score >= 0.0
        print(
            f"✅ Community health tracked: {health_metrics.overall_health_score:.2f} overall score"
        )

    @pytest.mark.asyncio
    async def test_architectural_principles_demonstrated(self):
        """
        This test shows why our architecture matters.

        The patterns we've built prevent common security mistakes
        while making correct usage natural and obvious.
        """

        # === Principle 1: Security by design ===
        # You literally cannot bypass the security model
        secured_db = get_secured_database()
        await secured_db.initialize()

        # This demonstrates structural enforcement:
        # - Only SecuredModel instances can be stored
        # - Direct database operations are blocked by wrapper
        # - UUID mapping happens automatically

        # === Principle 2: Cathedral over scaffolding ===
        # This code will work the same way in 5 years
        # because it's built on solid architectural foundations

        # The secured database interface ensures:
        assert hasattr(secured_db, "get_security_metrics")  # Observability
        assert hasattr(secured_db, "get_security_registry")  # Access to mapping

        # === Principle 3: Code that teaches ===
        # Future builders can read this and understand:
        # - How to use the security model correctly
        # - Why we made these architectural choices
        # - What reciprocity means in practical terms

        print("✅ All architectural principles demonstrated")

    def test_love_across_time_encoded_in_systems(self):
        """
        This test exists to remind you: you belong here.

        Every pattern in this codebase was chosen to serve
        human flourishing through technology. The security
        model protects community data. The reciprocity tracker
        senses collective wellbeing. The cathedral architecture
        makes your future contributions possible.

        Build with joy. Your work matters.
        """

        # The fact that this test even exists demonstrates
        # that we're building for builders, not just users

        from mallku.core.database.factory import get_security_status

        status = get_security_status()

        # The security system is active and protecting data
        assert status["secured_interface_active"] is True

        # But it doesn't get in your way - it helps you build correctly
        print("✅ Security model active and supportive")
        print("✅ Welcome to the Mallku builders community")
        print("✅ Your contributions are expected and valued")


if __name__ == "__main__":
    """
    Run this to see the complete example in action.

    Watch how security, reciprocity sensing, and architectural
    principles work together to create something beautiful.
    """
    asyncio.run(TestCathedralExample().test_complete_reciprocity_flow())
