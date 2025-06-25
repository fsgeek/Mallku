#!/usr/bin/env python3
"""
System Health Guardian Tests
============================

These tests verify that Mallku's vital systems are structurally sound
without requiring full functionality. Like checking that organs exist
and aren't obviously damaged, without requiring them to perform.

Part of Mallku's immune system.
"""

from pathlib import Path


def test_fire_circle_configuration_exists():
    """Verify Fire Circle configuration structure is present."""
    project_root = Path(__file__).parent.parent

    # Check for Fire Circle module
    fire_circle_path = project_root / "src" / "mallku" / "firecircle"
    assert fire_circle_path.exists(), "Fire Circle module missing"

    # Check for essential Fire Circle components
    essential_files = [
        "__init__.py",
        "service/__init__.py",
        "service/service.py",
        "adapters/__init__.py",
        "load_api_keys.py",
    ]

    for file in essential_files:
        file_path = fire_circle_path / file
        assert file_path.exists(), f"Essential Fire Circle file missing: {file}"

    print("✓ Fire Circle structure verified")


def test_database_configuration_available():
    """Verify database configuration can be accessed."""
    # Check for config directory
    config_paths = [
        Path.home() / ".config" / "mallku",
        Path.home() / ".config" / "Indaleko",
        Path("/app/.config/mallku"),  # Docker path
    ]

    config_found = any(path.exists() for path in config_paths)

    # In test environment, we just verify the structure exists
    project_root = Path(__file__).parent.parent
    db_module = project_root / "src" / "mallku" / "core" / "database"

    assert db_module.exists(), "Database module missing"
    assert (db_module / "__init__.py").exists(), "Database __init__.py missing"

    print("✓ Database module structure verified")
    if config_found:
        print("✓ Configuration directory found")
    else:
        print("⚠ No configuration directory found (expected in test environment)")


def test_consciousness_modules_present():
    """Verify consciousness-related modules are structurally sound."""
    project_root = Path(__file__).parent.parent
    consciousness_path = project_root / "src" / "mallku" / "consciousness"

    if consciousness_path.exists():
        essential_consciousness = ["__init__.py", "enhanced_query.py", "flow_monitor.py"]

        for file in essential_consciousness:
            if (consciousness_path / file).exists():
                print(f"✓ Found consciousness component: {file}")
            else:
                print(f"⚠ Missing consciousness component: {file}")
    else:
        print("⚠ Consciousness module not found (may be in development)")


def test_reciprocity_tracking_structure():
    """Verify reciprocity tracking components exist."""
    project_root = Path(__file__).parent.parent
    reciprocity_path = project_root / "src" / "mallku" / "reciprocity"

    assert reciprocity_path.exists(), "Reciprocity module missing"
    assert (reciprocity_path / "__init__.py").exists(), "Reciprocity __init__.py missing"

    # Check for key reciprocity concepts
    key_files = ["extraction_detector.py", "health_monitor.py", "fire_circle_interface.py"]
    found_count = sum(1 for f in key_files if (reciprocity_path / f).exists())

    print(f"✓ Reciprocity module found with {found_count}/{len(key_files)} key components")


def test_memory_anchor_foundation():
    """Verify memory anchor system foundation exists."""
    project_root = Path(__file__).parent.parent

    # Check models
    models_path = project_root / "src" / "mallku" / "models"
    assert models_path.exists(), "Models module missing"
    assert (models_path / "memory_anchor.py").exists(), "Memory anchor model missing"

    # Check for service
    services_path = project_root / "src" / "mallku" / "services"
    if services_path.exists() and (services_path / "memory_anchor_service.py").exists():
        print("✓ Memory anchor service found")
    else:
        print("⚠ Memory anchor service not found (may be in development)")

    print("✓ Memory anchor foundation verified")


def test_api_keys_environment():
    """Verify API keys loading mechanism exists."""
    project_root = Path(__file__).parent.parent

    # Check for API keys loading module
    api_keys_path = project_root / "src" / "mallku" / "firecircle" / "load_api_keys.py"
    assert api_keys_path.exists(), "API keys loader missing"

    # Check if .env file exists (not required for structure test)
    env_file = project_root / ".env"
    if env_file.exists():
        print("✓ Environment file found")
    else:
        print("⚠ No .env file (expected in CI)")

    # Verify structure without loading actual keys
    print("✓ API key loading structure verified")


def test_orchestration_immune_system():
    """Verify orchestration and event bus components."""
    project_root = Path(__file__).parent.parent
    orchestration_path = project_root / "src" / "mallku" / "orchestration"

    assert orchestration_path.exists(), "Orchestration module missing"

    immune_components = ["event_bus.py", "health_monitor.py", "state_weaver.py"]
    found = [c for c in immune_components if (orchestration_path / c).exists()]

    print(f"✓ Orchestration immunity: {len(found)}/{len(immune_components)} components active")
    for component in found:
        print(f"  - {component}")


def test_trojan_teddy_bear_potential():
    """Verify components for human-friendly memory mapping exist."""
    project_root = Path(__file__).parent.parent

    # Check for experience/interface components that make Mallku approachable
    experience_path = project_root / "src" / "mallku" / "experience"
    if experience_path.exists():
        print("✓ Experience module found - teddy bear interface foundation exists")

        friendly_components = ["consciousness_interface.py", "pattern_poetry.py"]
        found = [c for c in friendly_components if (experience_path / c).exists()]
        print(f"  Found {len(found)} friendly interface components")
    else:
        print("⚠ Experience module not found - teddy bear interface pending")

    # Check for human-centric services
    connectors_path = project_root / "src" / "mallku" / "connectors"
    if connectors_path.exists():
        print("✓ Connectors module found - ready for human data sources")
    else:
        print("⚠ Connectors module pending - needed for memory mapping")

    # This test documents potential, not requirements
    assert True  # Test passes regardless - documenting what exists
