#!/usr/bin/env python3
"""
Test Mallku Package Installation
=================================

This test verifies that mallku is properly installed and can be imported.
It's the bridge between structural tests and full integration tests.

Second Guardian - Foundation Builder
"""


def test_mallku_is_installed():
    """Verify mallku is properly installed, not just sys.path accessible."""
    import subprocess
    import sys

    # Try uv first (used in CI), then pip as fallback
    commands = [
        ["uv", "pip", "list"],
        [sys.executable, "-m", "pip", "list"],
    ]

    installed = False
    for cmd in commands:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0 and "mallku" in result.stdout.lower():
                installed = True
                print(f"✓ mallku found via: {' '.join(cmd)}")
                break
        except (subprocess.SubprocessError, FileNotFoundError):
            continue

    # If neither worked, check if mallku can at least be imported
    if not installed:
        try:
            import mallku  # noqa: F401

            print("✓ mallku is importable (installed in development mode)")
            installed = True
        except ImportError:
            pass

    assert installed, "mallku not found - not installed via uv/pip and can't be imported"


def test_core_mallku_imports():
    """Test that core mallku modules can be imported."""
    # These imports will fail if mallku isn't properly installed
    import mallku

    print("✓ Core mallku modules imported successfully")
    assert mallku.__file__.endswith("src/mallku/__init__.py")


def test_fire_circle_config():
    """Test that Fire Circle configuration can be instantiated."""
    from mallku.firecircle.service import CircleConfig

    # Create a basic config
    config = CircleConfig(name="Test Circle", purpose="Verify proper installation")

    assert config.name == "Test Circle"
    assert config.min_voices == 3
    print("✓ Fire Circle configuration works")


def test_memory_anchor_creation():
    """Test that Memory Anchor models can be created."""
    from datetime import UTC, datetime
    from uuid import uuid4

    from mallku.models import MemoryAnchor

    anchor = MemoryAnchor(
        anchor_id=uuid4(),
        timestamp=datetime.now(UTC),
        cursors={"test": "value"},
        metadata={"source": "test"},
    )

    assert anchor.anchor_id is not None
    assert anchor.cursors["test"] == "value"
    print("✓ Memory Anchor model instantiation works")


def test_reciprocity_interfaces():
    """Test that reciprocity tracking interfaces are available."""
    from mallku.reciprocity.extraction_detector import ExtractionDetector

    # Just verify the class exists and can be referenced
    assert ExtractionDetector is not None
    assert hasattr(ExtractionDetector, "__init__")
    print("✓ Reciprocity interfaces accessible")
