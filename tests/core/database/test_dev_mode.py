"""
Tests for Development Mode Database Interface
============================================

60th Artisan - Ayni Awaq - Testing Development Mode Safety
"""

import os
import warnings
from unittest.mock import patch

import pytest

from mallku.core.database.dev_interface import DevDatabaseInterface
from mallku.core.database.factory import get_secured_database


class TestDevelopmentMode:
    """Test development mode functionality and safety checks."""

    def test_dev_mode_warning_on_init(self):
        """Test that development mode emits appropriate warnings."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            dev_db = DevDatabaseInterface()

            # Should have warning about development mode
            assert len(w) == 1
            assert "DEVELOPMENT ONLY" in str(w[0].message)

    @patch.dict(os.environ, {"MALLKU_DEV_MODE": "true", "MALLKU_PRODUCTION": "false"})
    def test_dev_mode_enabled(self):
        """Test that development mode can be enabled in non-production."""
        db = get_secured_database()
        assert isinstance(db, DevDatabaseInterface)

    @patch.dict(os.environ, {"MALLKU_DEV_MODE": "true", "MALLKU_PRODUCTION": "true"})
    def test_dev_mode_blocked_in_production(self):
        """Test that development mode is blocked in production."""
        with pytest.raises(RuntimeError) as exc_info:
            get_secured_database()

        assert "SECURITY VIOLATION" in str(exc_info.value)
        assert "Development mode cannot be enabled in production" in str(exc_info.value)

    def test_mock_collection_operations(self):
        """Test that mock collections provide basic functionality."""
        dev_db = DevDatabaseInterface()

        # Test collection creation
        assert dev_db.has_collection("test_collection")
        dev_db.create_collection("test_collection")

        # Test collection access
        collection = dev_db.collection("test_collection")
        assert collection is not None

        # Test document operations
        doc = collection.insert({"test": "data"})
        assert "_id" in doc
        assert doc["_id"].startswith("dev_")

        # Test batch insert
        docs = collection.insert_many([{"test": 1}, {"test": 2}])
        assert len(docs) == 2

        # Test query operations (return empty)
        assert collection.all() == []
        assert collection.find({"test": 1}) == []

        # Test index creation
        index = collection.add_persistent_index(["test"], unique=True)
        assert "idx_test_collection_test" in index["id"]

    def test_mock_aql_operations(self):
        """Test that mock AQL provides basic functionality."""
        dev_db = DevDatabaseInterface()
        aql = dev_db.aql

        # Test AQL execution (returns empty)
        result = aql.execute("FOR doc IN test RETURN doc")
        assert result == []

        # Test with bind variables
        result = aql.execute(
            "FOR doc IN @@collection RETURN doc", bind_vars={"@collection": "test"}
        )
        assert result == []

    async def test_async_query_operations(self):
        """Test async query operations in dev mode."""
        dev_db = DevDatabaseInterface()

        # Test async query
        result = await dev_db.query("test_collection", {"filter": "test"})
        assert result == []

        # Test async batch insert
        await dev_db.batch_insert("test_collection", [{"test": 1}, {"test": 2}])
        # Should complete without error

    def test_security_metrics(self):
        """Test that security metrics are tracked."""
        dev_db = DevDatabaseInterface()

        # Perform some operations
        dev_db.collection("test1")
        dev_db.collection("test2")
        dev_db.has_collection("test3")

        # Check metrics
        metrics = dev_db.get_security_metrics()
        assert metrics["mode"] == "development"
        assert metrics["operations_count"] >= 2  # At least 2 different operations
        assert "test1" in metrics["collections_accessed"]
        assert "test2" in metrics["collections_accessed"]
        assert metrics["security_violations"] == 0

    def test_operation_warnings_once(self):
        """Test that each operation type warns only once."""
        dev_db = DevDatabaseInterface()

        # Reset warned operations
        dev_db._warned_operations.clear()

        # First collection access should warn
        with patch("logging.Logger.warning") as mock_warning:
            dev_db.collection("test1")
            assert mock_warning.call_count == 1
            assert "Accessing collection" in mock_warning.call_args[0][0]

        # Second collection access should not warn
        with patch("logging.Logger.warning") as mock_warning:
            dev_db.collection("test2")
            assert mock_warning.call_count == 0
