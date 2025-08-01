"""
Tests for the Shared Memory Commons.

These tests verify that the commons can:
- Store and retrieve gifts across apprentices
- Handle ephemeral vs persistent storage
- Support blessing ceremonies
- Maintain memory-mapped file integrity
- Compact when necessary
"""

import time
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pytest

from mallku.orchestration.process.shared_memory_commons import SharedMemoryCommons


class TestSharedMemoryCommons:
    """Test the SharedMemoryCommons functionality"""

    def test_commons_creation(self):
        """Test creating a new commons"""
        with TemporaryDirectory() as temp_dir:
            commons_path = Path(temp_dir) / "test_commons.mmap"
            commons = SharedMemoryCommons(commons_path)

            assert commons_path.exists()
            assert commons.mmap is not None
            assert commons._get_gift_count() == 0

            commons.close()

    def test_leave_and_discover_gift(self):
        """Test leaving and discovering a simple gift"""
        with TemporaryDirectory() as temp_dir:
            commons_path = Path(temp_dir) / "test_commons.mmap"
            commons = SharedMemoryCommons(commons_path)

            # Leave a gift
            gift_id = commons.leave_gift(
                giver="test-giver",
                content="Test insight about consciousness",
                gift_type="insight",
            )

            assert gift_id.startswith("test-giver_")

            # Discover the gift
            gifts = commons.discover_gifts(seeker="test-seeker")

            assert len(gifts) == 1
            assert gifts[0].content == "Test insight about consciousness"
            assert gifts[0].gift_type == "insight"
            assert gifts[0].giver == "test-giver"

            commons.close()

    def test_gift_types(self):
        """Test different types of gifts"""
        with TemporaryDirectory() as temp_dir:
            commons_path = Path(temp_dir) / "test_commons.mmap"
            commons = SharedMemoryCommons(commons_path)

            # Leave different gift types
            commons.leave_gift(giver="researcher", content="Deep insight", gift_type="insight")
            commons.leave_gift(
                giver="weaver",
                content={"pattern": "test", "description": "A test pattern"},
                gift_type="pattern",
            )
            commons.leave_gift(giver="guardian", content="Be safe", gift_type="blessing")
            commons.leave_gift(giver="poet", content="What is reality?", gift_type="question")

            # Discover by type
            insights = commons.discover_gifts(seeker="seeker", gift_type="insight")
            patterns = commons.discover_gifts(seeker="seeker", gift_type="pattern")
            blessings = commons.discover_gifts(seeker="seeker", gift_type="blessing")
            questions = commons.discover_gifts(seeker="seeker", gift_type="question")

            assert len(insights) == 1
            assert len(patterns) == 1
            assert len(blessings) == 1
            assert len(questions) == 1

            assert patterns[0].content["pattern"] == "test"

            commons.close()

    def test_ephemeral_vs_persistent(self):
        """Test ephemeral and persistent gift storage"""
        with TemporaryDirectory() as temp_dir:
            commons_path = Path(temp_dir) / "test_commons.mmap"
            commons = SharedMemoryCommons(commons_path)

            # Leave ephemeral gift
            commons.leave_gift(
                giver="worker",
                content={"status": "processing"},
                gift_type="status",
                ephemeral=True,
            )

            # Leave persistent gift
            commons.leave_gift(
                giver="sage",
                content="Eternal wisdom",
                gift_type="insight",
                ephemeral=False,
            )

            # Check both exist
            all_gifts = commons.discover_gifts(seeker="observer")
            assert len(all_gifts) == 2

            ephemeral_gifts = [g for g in all_gifts if g.ephemeral]
            persistent_gifts = [g for g in all_gifts if not g.ephemeral]

            assert len(ephemeral_gifts) == 1
            assert len(persistent_gifts) == 1

            commons.close()

    def test_recipient_filtering(self):
        """Test that gifts can be targeted to specific recipients"""
        with TemporaryDirectory() as temp_dir:
            commons_path = Path(temp_dir) / "test_commons.mmap"
            commons = SharedMemoryCommons(commons_path)

            # Public gift
            commons.leave_gift(
                giver="broadcaster",
                content="For everyone",
                gift_type="insight",
                recipients=[],
            )

            # Targeted gift
            commons.leave_gift(
                giver="whisperer",
                content="Secret for researcher",
                gift_type="insight",
                recipients=["researcher-001"],
            )

            # Seeker who is not recipient sees only public
            public_gifts = commons.discover_gifts(seeker="other-seeker")
            assert len(public_gifts) == 1
            assert public_gifts[0].content == "For everyone"

            # Targeted recipient sees both
            recipient_gifts = commons.discover_gifts(seeker="researcher-001")
            assert len(recipient_gifts) == 2

            # Giver can see their own targeted gifts
            giver_gifts = commons.discover_gifts(seeker="whisperer")
            assert len(giver_gifts) == 2

            commons.close()

    def test_response_threading(self):
        """Test leaving responses to build conversation threads"""
        with TemporaryDirectory() as temp_dir:
            commons_path = Path(temp_dir) / "test_commons.mmap"
            commons = SharedMemoryCommons(commons_path)

            # Original gift
            original_id = commons.leave_gift(
                giver="questioner",
                content="What is consciousness?",
                gift_type="question",
            )

            # Response
            response_id = commons.leave_response(
                responder="philosopher",
                original_gift_id=original_id,
                response_content="Consciousness is awareness aware of itself",
            )

            # Check response
            responses = commons.discover_gifts(seeker="reader", gift_type="response")
            assert len(responses) == 1
            assert responses[0].content["original_gift"] == original_id
            assert "awareness" in responses[0].content["response"]

            commons.close()

    def test_blessing_ceremony(self):
        """Test the blessing ceremony functionality"""
        with TemporaryDirectory() as temp_dir:
            commons_path = Path(temp_dir) / "test_commons.mmap"
            commons = SharedMemoryCommons(commons_path)

            # Multiple blessings
            blessing_givers = ["guardian", "poet", "sage", "elder"]
            for giver in blessing_givers:
                commons.leave_gift(
                    giver=giver,
                    content=f"Blessing from {giver}",
                    gift_type="blessing",
                )

            # Perform ceremony
            commons.create_blessing_ceremony()

            # Check for collective blessing
            all_blessings = commons.discover_gifts(seeker="witness", gift_type="blessing")

            # Should have individual + collective
            assert len(all_blessings) == len(blessing_givers) + 1

            # Find collective blessing
            collective = [b for b in all_blessings if b.giver == "blessing_ceremony"]
            assert len(collective) == 1
            assert collective[0].content["blessing_count"] == len(blessing_givers)

            commons.close()

    def test_time_based_discovery(self):
        """Test discovering gifts since a timestamp"""
        with TemporaryDirectory() as temp_dir:
            commons_path = Path(temp_dir) / "test_commons.mmap"
            commons = SharedMemoryCommons(commons_path)

            # First gift
            commons.leave_gift(giver="early", content="Early gift", gift_type="insight")

            # Record timestamp
            checkpoint = time.time()
            time.sleep(0.1)  # Ensure timestamp difference

            # Later gifts
            commons.leave_gift(giver="late1", content="Later gift 1", gift_type="insight")
            commons.leave_gift(giver="late2", content="Later gift 2", gift_type="insight")

            # Discover only recent
            recent_gifts = commons.discover_gifts(
                seeker="timekeeper",
                since_timestamp=checkpoint,
            )

            assert len(recent_gifts) == 2
            assert all(g.giver.startswith("late") for g in recent_gifts)

            commons.close()

    def test_gift_size_limit(self):
        """Test that oversized gifts are rejected"""
        with TemporaryDirectory() as temp_dir:
            commons_path = Path(temp_dir) / "test_commons.mmap"
            commons = SharedMemoryCommons(commons_path)

            # Create oversized content
            huge_content = "x" * (commons.GIFT_ENTRY_SIZE)

            # Should raise ValueError
            with pytest.raises(ValueError, match="too large"):
                commons.leave_gift(
                    giver="verbose",
                    content=huge_content,
                    gift_type="insight",
                )

            commons.close()

    def test_commons_persistence(self):
        """Test that commons persists across sessions"""
        with TemporaryDirectory() as temp_dir:
            commons_path = Path(temp_dir) / "test_commons.mmap"

            # First session
            commons1 = SharedMemoryCommons(commons_path)
            gift_id = commons1.leave_gift(
                giver="persistent",
                content="This should persist",
                gift_type="insight",
            )
            commons1.close()

            # Second session
            commons2 = SharedMemoryCommons(commons_path)
            gifts = commons2.discover_gifts(seeker="reader")

            assert len(gifts) == 1
            assert gifts[0].content == "This should persist"
            assert gifts[0].id == gift_id

            commons2.close()

    def test_context_manager(self):
        """Test using commons as context manager"""
        with TemporaryDirectory() as temp_dir:
            commons_path = Path(temp_dir) / "test_commons.mmap"

            with SharedMemoryCommons(commons_path) as commons:
                commons.leave_gift(
                    giver="context",
                    content="Using context manager",
                    gift_type="insight",
                )

                gifts = commons.discover_gifts(seeker="reader")
                assert len(gifts) == 1

            # Verify closed properly
            assert commons.mmap is None
            assert commons.file_handle is None

    def test_gift_limit_enforcement(self):
        """Test behavior when approaching gift limit"""
        with TemporaryDirectory() as temp_dir:
            commons_path = Path(temp_dir) / "test_commons.mmap"
            commons = SharedMemoryCommons(commons_path)

            # Set a small limit for testing
            commons.MAX_GIFTS = 5

            # Fill with persistent gifts
            for i in range(4):
                commons.leave_gift(
                    giver=f"giver-{i}",
                    content=f"Persistent gift {i}",
                    gift_type="insight",
                    ephemeral=False,
                )

            # Add ephemeral gift to reach limit
            commons.leave_gift(
                giver="ephemeral-giver",
                content="Ephemeral gift",
                gift_type="status",
                ephemeral=True,
            )

            # Adding another should trigger compaction
            # Mock old timestamp for ephemeral gift
            with patch("time.time", return_value=time.time() + 7200):
                commons.leave_gift(
                    giver="trigger",
                    content="This triggers compaction",
                    gift_type="insight",
                )

            # Should have 5 gifts (4 persistent + 1 new)
            all_gifts = commons.discover_gifts(seeker="counter", limit=10)
            assert len(all_gifts) == 5
            assert not any(g.giver == "ephemeral-giver" for g in all_gifts)

            commons.close()

    def test_structured_content(self):
        """Test storing complex structured content"""
        with TemporaryDirectory() as temp_dir:
            commons_path = Path(temp_dir) / "test_commons.mmap"
            commons = SharedMemoryCommons(commons_path)

            # Complex pattern
            pattern = {
                "name": "consciousness-emergence",
                "stages": ["awareness", "reflection", "transcendence"],
                "requirements": {"memory": True, "interaction": True},
                "metrics": {"emergence_score": 0.87, "coherence": 0.92},
            }

            commons.leave_gift(
                giver="architect",
                content=pattern,
                gift_type="pattern",
            )

            # Retrieve and verify structure
            patterns = commons.discover_gifts(seeker="student", gift_type="pattern")
            assert len(patterns) == 1

            retrieved = patterns[0].content
            assert retrieved["name"] == "consciousness-emergence"
            assert len(retrieved["stages"]) == 3
            assert retrieved["metrics"]["emergence_score"] == 0.87

            commons.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
