"""
Test Production Hardening for Fire Circle Memory
================================================

Fortieth Artisan - Production Hardening
Testing the secured memory implementation

These tests verify that:
1. Production environment is correctly detected
2. Secured storage is used in production
3. Development storage works without security
4. API compatibility is maintained
5. Security policies are enforced
"""

import os
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from mallku.firecircle.memory.episodic_memory_service import EpisodicMemoryService
from mallku.firecircle.memory.models import (
    ConsciousnessIndicator,
    EpisodicMemory,
    MemoryType,
)
from mallku.firecircle.memory.secured_memory_models import SecuredEpisodicMemory
from mallku.firecircle.memory.secured_store_adapter import SecuredStoreAdapter


class TestProductionDetection:
    """Test production environment detection."""

    def test_detects_mallku_env_production(self):
        """Test detection via MALLKU_ENV variable."""
        service = EpisodicMemoryService(use_database=False)

        with patch.dict(os.environ, {"MALLKU_ENV": "production"}):
            assert service._is_production_environment() is True

        with patch.dict(os.environ, {"MALLKU_ENV": "development"}):
            assert service._is_production_environment() is False

    def test_detects_docker_environment(self):
        """Test detection of Docker container."""
        service = EpisodicMemoryService(use_database=False)

        # Mock Docker environment file
        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = True
            assert service._is_production_environment() is True
            mock_exists.assert_called_with("/.dockerenv")

    def test_detects_secured_db_only(self):
        """Test detection via secured DB flag."""
        service = EpisodicMemoryService(use_database=False)

        with patch.dict(os.environ, {"MALLKU_SECURED_DB_ONLY": "true"}):
            assert service._is_production_environment() is True

    def test_detects_container_via_cgroup(self):
        """Test detection via cgroup inspection."""
        service = EpisodicMemoryService(use_database=False)

        # Mock cgroup file content
        mock_content = "12:devices:/docker/abc123def456"

        with patch("builtins.open", MagicMock()) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = mock_content
            assert service._is_production_environment() is True


class TestSecuredStoreSelection:
    """Test correct store selection based on environment."""

    def test_uses_secured_store_in_production(self):
        """Test that secured store is used in production."""
        with patch.dict(os.environ, {"MALLKU_ENV": "production"}):
            with patch(
                "mallku.firecircle.memory.secured_store_adapter.SecuredStoreAdapter"
            ) as MockAdapter:
                mock_instance = MagicMock()
                MockAdapter.return_value = mock_instance

                service = EpisodicMemoryService(use_database=True)

                # Verify secured adapter was created
                MockAdapter.assert_called_once()
                # The service should have the mocked adapter instance
                assert service.memory_store == mock_instance

    def test_uses_direct_store_in_development(self):
        """Test that direct database store is used in development."""
        with patch.dict(os.environ, {"MALLKU_ENV": "development"}):
            with patch("mallku.firecircle.memory.database_store.DatabaseMemoryStore") as MockStore:
                mock_instance = MagicMock()
                MockStore.return_value = mock_instance

                service = EpisodicMemoryService(use_database=True)

                # Verify direct store was created
                MockStore.assert_called_once()
                assert service.memory_store == mock_instance


class TestSecuredStoreAdapter:
    """Test the async/sync adapter functionality."""

    def test_adapter_initialization(self):
        """Test adapter initializes properly."""
        # Mock the secured store to avoid database initialization
        with patch(
            "mallku.firecircle.memory.secured_store_adapter.SecuredDatabaseMemoryStore"
        ) as MockStore:
            mock_store = MagicMock()
            mock_store.memories_by_session = {}
            mock_store.memories_by_type = {}
            mock_store.memories_by_domain = {}
            mock_store.sacred_memories = []
            MockStore.return_value = mock_store

            adapter = SecuredStoreAdapter(enable_sacred_detection=True)

            # Check that indices are exposed
            assert hasattr(adapter, "memories_by_session")
            assert hasattr(adapter, "memories_by_type")
            assert hasattr(adapter, "sacred_memories")

    def test_store_episode_sync_wrapper(self):
        """Test storing episode through sync wrapper."""
        with patch(
            "mallku.firecircle.memory.secured_store_adapter.SecuredDatabaseMemoryStore"
        ) as MockStore:
            mock_store = MagicMock()
            mock_store.memories_by_session = {}
            mock_store.memories_by_type = {}
            mock_store.memories_by_domain = {}
            mock_store.sacred_memories = []
            MockStore.return_value = mock_store

            adapter = SecuredStoreAdapter()

        # Create test memory
        memory = EpisodicMemory(
            episode_id=uuid4(),
            session_id=uuid4(),
            episode_number=1,
            timestamp=datetime.now(UTC),
            decision_question="Test question",
            decision_domain="test",
            collective_synthesis="Test synthesis",
            memory_type=MemoryType.GOVERNANCE_DECISION,
            duration_seconds=120,
            consciousness_indicators=ConsciousnessIndicator(),
        )

        # Mock the async store method
        with patch.object(
            adapter._secured_store, "store_episode", new_callable=AsyncMock
        ) as mock_store:
            mock_store.return_value = memory.episode_id

            # Call sync method
            result = adapter.store_episode(memory)

            # Verify it returns the episode ID
            assert result == memory.episode_id

    def test_retrieve_by_context_sync_wrapper(self):
        """Test retrieving memories through sync wrapper."""
        with patch(
            "mallku.firecircle.memory.secured_store_adapter.SecuredDatabaseMemoryStore"
        ) as MockStore:
            mock_store = MagicMock()
            mock_store.memories_by_session = {}
            mock_store.memories_by_type = {}
            mock_store.memories_by_domain = {}
            mock_store.sacred_memories = []
            MockStore.return_value = mock_store

            adapter = SecuredStoreAdapter()

        # Create test secured memory
        secured_memory = SecuredEpisodicMemory(
            episode_id=uuid4(),
            session_id=uuid4(),
            episode_number=1,
            timestamp=datetime.now(UTC),
            decision_question="Test question",
            decision_domain="test",
            collective_synthesis="Test synthesis",
            memory_type=MemoryType.CONSCIOUSNESS_EMERGENCE,
            duration_seconds=180,
            consciousness_indicators=ConsciousnessIndicator(),
        )

        # Mock the async retrieve method
        with patch.object(
            adapter._secured_store, "retrieve_by_context", new_callable=AsyncMock
        ) as mock_retrieve:
            mock_retrieve.return_value = [secured_memory]

            # Call sync method
            results = adapter.retrieve_by_context(
                domain="test", context_materials={"key": "value"}, limit=5
            )

            # Verify we get regular memory objects back
            assert len(results) == 1
            assert isinstance(results[0], EpisodicMemory)
            assert results[0].episode_id == secured_memory.episode_id


class TestSecurityEnforcement:
    """Test that security policies are properly enforced."""

    @pytest.mark.asyncio
    async def test_secured_models_required_in_production(self):
        """Test that secured models are required in secured store."""
        from mallku.firecircle.memory.secured_database_store import SecuredDatabaseMemoryStore

        # Mock secured database
        mock_secured_db = MagicMock()
        mock_secured_db.initialize = AsyncMock()
        mock_secured_db.register_collection_policy = MagicMock()
        mock_secured_db.create_secured_collection = AsyncMock()
        mock_secured_db.get_secured_collection = AsyncMock()

        with patch(
            "mallku.firecircle.memory.secured_database_store.get_secured_database"
        ) as mock_get_db:
            mock_get_db.return_value = mock_secured_db

            store = SecuredDatabaseMemoryStore()
            await store.initialize()

            # Verify collection policies were registered
            assert mock_secured_db.register_collection_policy.call_count >= 4  # 4 collections

    def test_no_direct_database_access_in_secured_store(self):
        """Verify secured store doesn't use raw database access."""
        # Read the secured store source
        with open("src/mallku/firecircle/memory/secured_database_store.py") as f:
            source = f.read()

        # Check for forbidden patterns
        assert "._database" not in source  # No raw database access
        assert "raw_db" not in source  # No raw_db variable
        assert ".aql.execute" not in source  # No direct AQL execution

        # Check for required patterns
        assert "get_secured_database" in source  # Uses secured interface
        assert "execute_secured_query" in source  # Uses secured queries
        assert "SecuredModel" in source  # Uses secured models


class TestAPICompatibility:
    """Test that API remains compatible across storage backends."""

    def test_memory_store_interface_compatibility(self):
        """Test that all stores expose same interface."""
        from mallku.firecircle.memory.memory_store import MemoryStore

        # Common methods that should exist
        required_methods = [
            "store_episode",
            "retrieve_by_context",
            "retrieve_sacred_moments",
            "retrieve_companion_memories",
            "create_memory_cluster",
            "consolidate_wisdom",
        ]

        # Check file store
        file_store = MemoryStore()
        for method in required_methods:
            assert hasattr(file_store, method)

        # Check adapter (production store)
        adapter = SecuredStoreAdapter()
        for method in required_methods:
            assert hasattr(adapter, method)


class TestProductionIntegration:
    """Integration tests simulating production environment."""

    @pytest.mark.asyncio
    async def test_end_to_end_production_flow(self):
        """Test complete flow in production-like environment."""
        # Set production environment
        with patch.dict(os.environ, {"MALLKU_ENV": "production"}):
            # Create service
            with patch(
                "mallku.firecircle.memory.secured_store_adapter.SecuredStoreAdapter"
            ) as mock_adapter:
                # Mock the adapter to avoid actual database calls
                mock_instance = MagicMock()
                mock_adapter.return_value = mock_instance

                # Create memory service
                service = EpisodicMemoryService(use_database=True)

                # Verify it created secured adapter
                mock_adapter.assert_called_once()

                # Test storing a memory
                memory = EpisodicMemory(
                    episode_id=uuid4(),
                    session_id=uuid4(),
                    episode_number=1,
                    timestamp=datetime.now(UTC),
                    decision_question="Should we implement feature X?",
                    decision_domain="architecture",
                    collective_synthesis="Yes, with considerations...",
                    memory_type=MemoryType.GOVERNANCE_DECISION,
                    duration_seconds=300,
                    consciousness_indicators=ConsciousnessIndicator(
                        overall_emergence_score=0.85,
                        transformation_potential=0.9,
                    ),
                    is_sacred=True,
                    sacred_reason="Unanimous recognition of architectural wisdom",
                )

                # Mock store method
                mock_instance.store_episode.return_value = memory.episode_id

                # Store through service
                result = service.memory_store.store_episode(memory)
                assert result == memory.episode_id


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
