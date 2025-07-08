#!/usr/bin/env python3
"""Test pytest import mechanism."""

import sys

print(f"Initial sys.path: {sys.path[:3]}")

# Try importing mallku directly
try:
    import mallku

    print(f"✅ Direct import of mallku succeeded: {mallku.__file__}")
except ImportError as e:
    print(f"❌ Direct import of mallku failed: {e}")

# Now try with pytest
import pytest

# Run a simple test
code = """
def test_mallku_import():
    import mallku
    assert mallku.__version__ == "0.1.0"
"""

# Write test file
with open("/tmp/test_mallku_import.py", "w") as f:
    f.write(code)

# Run pytest
print("\nRunning pytest...")
result = pytest.main(["-v", "/tmp/test_mallku_import.py"])
print(f"Pytest result: {result}")
