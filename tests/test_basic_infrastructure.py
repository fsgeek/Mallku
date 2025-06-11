"""
Basic infrastructure test to verify test setup is working correctly.
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest


def test_mallku_import():
    """Test that mallku package can be imported"""
    import mallku
    assert mallku is not None


def test_rich_import():
    """Test that rich module can be imported"""
    import rich
    assert rich is not None


def test_core_modules():
    """Test that core modules can be imported"""
    from mallku.core import config, database, log
    assert config is not None
    assert database is not None
    assert log is not None


def test_reciprocity_tracker():
    """Test that ReciprocityTracker can be imported without circular imports"""
    from mallku.reciprocity.tracker import ReciprocityTracker
    assert ReciprocityTracker is not None


def test_correlation_engine():
    """Test that CorrelationEngine can be imported"""
    from mallku.correlation.engine import CorrelationEngine
    assert CorrelationEngine is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
