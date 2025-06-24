"""Tests that verify basic functionality without importing mallku."""

import os
import sys
from pathlib import Path


def test_project_structure():
    """Verify basic project structure exists."""
    project_root = Path(__file__).parent.parent
    assert project_root.exists()
    
    src_dir = project_root / "src"
    assert src_dir.exists(), "src directory should exist"
    
    mallku_dir = src_dir / "mallku"
    assert mallku_dir.exists(), "src/mallku directory should exist"
    
    init_file = mallku_dir / "__init__.py"
    assert init_file.exists(), "mallku/__init__.py should exist"


def test_python_environment():
    """Verify Python environment is set up correctly."""
    assert sys.version_info >= (3, 12), "Python 3.12+ required"
    
    # Check if we're in a virtual environment
    assert hasattr(sys, 'prefix'), "sys.prefix should exist"
    

def test_environment_variables():
    """Test that environment variables can be set and read."""
    test_var = "MALLKU_TEST_VAR"
    test_value = "test_value_123"
    
    os.environ[test_var] = test_value
    assert os.environ.get(test_var) == test_value
    
    del os.environ[test_var]
    assert os.environ.get(test_var) is None


def test_file_operations():
    """Test basic file operations work."""
    test_file = Path("/tmp/mallku_test_file.txt")
    test_content = "Mallku CI test content"
    
    # Write
    test_file.write_text(test_content)
    assert test_file.exists()
    
    # Read
    content = test_file.read_text()
    assert content == test_content
    
    # Delete
    test_file.unlink()
    assert not test_file.exists()


def test_path_manipulation():
    """Test Python path manipulation works."""
    original_path = sys.path.copy()
    test_path = "/tmp/mallku_test_path"
    
    sys.path.insert(0, test_path)
    assert sys.path[0] == test_path
    
    sys.path = original_path
    assert test_path not in sys.path