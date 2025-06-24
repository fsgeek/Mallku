"""Simple test to verify pytest works in CI."""


def test_simple():
    """Test that doesn't require any imports."""
    assert 1 + 1 == 2


def test_python_version():
    """Test Python version."""
    import sys
    assert sys.version_info >= (3, 12)
