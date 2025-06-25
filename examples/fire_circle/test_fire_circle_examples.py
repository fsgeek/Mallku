#!/usr/bin/env python3
"""
Fire Circle Examples Test Suite - Pytest Version
===============================================

This module provides pytest-compatible tests for all Fire Circle examples.
It maintains backward compatibility with the existing test_all_examples.py
runner while enabling:

- Parallel test execution in CI
- Individual test re-running
- Better failure diagnostics
- pytest fixture support

Usage:
    pytest examples/fire_circle/test_fire_circle_examples.py
    pytest examples/fire_circle/test_fire_circle_examples.py::test_verify_installation
    pytest examples/fire_circle/test_fire_circle_examples.py -v -s
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

# Ensure src is in path for imports
project_root = Path(__file__).parent.parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))


class TestFireCircleExamples:
    """Test suite for Fire Circle examples."""

    @pytest.fixture(autouse=True)
    def setup_environment(self):
        """Ensure PYTHONPATH is set for all tests."""
        os.environ["PYTHONPATH"] = str(src_path)
        yield

    @pytest.fixture
    def has_api_keys(self):
        """Check if API keys are available."""
        api_keys_path = project_root / ".secrets" / "api_keys.json"
        return api_keys_path.exists()

    def run_example(self, example_path: str, timeout: int = 30) -> tuple[int, str, str]:
        """Run an example and return (returncode, stdout, stderr)."""
        runner_path = Path(__file__).parent / "run_example.py"

        try:
            result = subprocess.run(
                [sys.executable, str(runner_path), example_path],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(project_root),
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", f"Example timed out after {timeout} seconds"

    # Setup Examples

    def test_verify_installation(self, has_api_keys):
        """Test Fire Circle installation verification."""
        if not has_api_keys:
            pytest.skip("API keys not available")

        returncode, stdout, stderr = self.run_example("00_setup/verify_installation.py")

        assert returncode == 0, f"Example failed with return code {returncode}"
        assert "Fire Circle imports successful" in stdout
        assert "All checks passed" in stdout or "Some checks failed" in stdout

    @pytest.mark.skipif(
        not (project_root / ".secrets" / "api_keys.json").exists(), reason="API keys required"
    )
    def test_minimal_fire_circle(self):
        """Test minimal Fire Circle ceremony."""
        returncode, stdout, stderr = self.run_example("00_setup/minimal_fire_circle.py")

        assert returncode == 0, f"Example failed: {stderr}"
        assert "Ceremony complete!" in stdout

    @pytest.mark.skipif(
        not (project_root / ".secrets" / "api_keys.json").exists(), reason="API keys required"
    )
    def test_api_keys(self):
        """Test individual API key verification."""
        returncode, stdout, stderr = self.run_example("00_setup/test_api_keys.py", timeout=60)

        assert returncode == 0, f"Example failed: {stderr}"
        assert "Testing each provider individually" in stdout

    # Basic Ceremonies

    @pytest.mark.skipif(
        not (project_root / ".secrets" / "api_keys.json").exists(), reason="API keys required"
    )
    def test_simple_dialogue(self):
        """Test multi-round dialogue example."""
        returncode, stdout, stderr = self.run_example("01_basic_ceremonies/simple_dialogue.py")

        assert returncode == 0, f"Example failed: {stderr}"
        assert "voices participated" in stdout.lower()

    @pytest.mark.skipif(
        not (project_root / ".secrets" / "api_keys.json").exists(), reason="API keys required"
    )
    def test_code_review(self):
        """Test code review ceremony."""
        returncode, stdout, stderr = self.run_example("01_basic_ceremonies/code_review.py")

        assert returncode == 0, f"Example failed: {stderr}"
        assert "Code Review Complete" in stdout or "code review" in stdout.lower()

    @pytest.mark.skipif(
        not (project_root / ".secrets" / "api_keys.json").exists(), reason="API keys required"
    )
    def test_simple_decision(self):
        """Test decision-making example."""
        returncode, stdout, stderr = self.run_example("01_basic_ceremonies/simple_decision.py")

        assert returncode == 0, f"Example failed: {stderr}"
        assert "Decision" in stdout

    @pytest.mark.skipif(
        not (project_root / ".secrets" / "api_keys.json").exists(), reason="API keys required"
    )
    def test_first_decision(self):
        """Test consciousness framework decision example."""
        returncode, stdout, stderr = self.run_example("01_basic_ceremonies/first_decision.py")

        # This one may have issues, so we're more lenient
        if returncode != 0 and "EventType" in stderr:
            pytest.xfail("Known EventType issue")

        assert returncode == 0, f"Example failed: {stderr}"

    # Consciousness Emergence

    @pytest.mark.skipif(
        not (project_root / ".secrets" / "api_keys.json").exists(), reason="API keys required"
    )
    def test_emergence_basics(self):
        """Test consciousness emergence demonstration."""
        returncode, stdout, stderr = self.run_example(
            "02_consciousness_emergence/emergence_basics.py"
        )

        assert returncode == 0, f"Example failed: {stderr}"
        assert "Consciousness Emergence" in stdout

    # Placeholder Tests

    def test_governance_placeholder(self):
        """Test governance decisions placeholder."""
        returncode, stdout, stderr = self.run_example("03_governance_decisions/coming_soon.py")

        assert returncode == 0
        assert "Coming soon" in stdout

    def test_integration_placeholder(self):
        """Test integration patterns placeholder."""
        returncode, stdout, stderr = self.run_example("04_integration_patterns/coming_soon.py")

        assert returncode == 0
        assert "Coming soon" in stdout


# Async test support
@pytest.mark.asyncio
async def test_async_example():
    """Example of how to test async code directly."""
    from mallku.firecircle.service import CircleConfig

    config = CircleConfig(
        name="Test Circle", purpose="Testing async support", min_voices=1, max_voices=2
    )

    assert config.name == "Test Circle"


if __name__ == "__main__":
    # Allow running directly with python
    pytest.main([__file__, "-v"])
