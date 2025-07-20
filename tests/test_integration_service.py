import asyncio
import logging
import tempfile
from pathlib import Path

import pytest
import pytest_asyncio

from mallku.integration import EndToEndIntegrationService, PipelineConfiguration, PipelineEvent
from mallku.integration.pipeline_models import PipelineStage

# Configure logging for tests
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def event_loop():
    """Create an instance of the default event loop for each test module."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="module")
async def test_directory():
    """Create a temporary directory for test file operations."""
    with tempfile.TemporaryDirectory(prefix="mallku_integration_test_") as tmpdir:
        test_dir = Path(tmpdir)
        (test_dir / "documents").mkdir()
        (test_dir / "code").mkdir()
        (test_dir / "projects").mkdir()
        logger.info(f"Created test directory: {test_dir}")
        yield test_dir


@pytest_asyncio.fixture(scope="module")
async def integration_service(test_directory):
    """Initialize the EndToEndIntegrationService for testing."""
    config = PipelineConfiguration(
        watch_directories=[str(test_directory)],
        correlation_confidence_threshold=0.5,
        anchor_creation_threshold=0.6,
        max_concurrent_events=10,
        file_filter_config={"test_mode": True},
    )

    service = EndToEndIntegrationService(config)

    # Use a list to capture events from the handler
    captured_events = []

    def _capture_pipeline_event(event: PipelineEvent) -> None:
        captured_events.append(event)

    service.add_event_handler(_capture_pipeline_event)

    await service.initialize()

    # Attach the captured_events list to the service instance for access in tests
    service.captured_events = captured_events

    yield service

    logger.info("Shutting down integration service...")
    await service.shutdown()
    logger.info("Integration service shutdown complete.")


@pytest.mark.asyncio
async def test_service_initialization_and_components(
    integration_service: EndToEndIntegrationService,
):
    """Test that the service and its components initialize correctly."""
    assert integration_service.is_running
    assert integration_service.memory_service is not None
    assert integration_service.correlation_engine is not None
    assert integration_service.file_connector is not None
    assert integration_service.correlation_adapter is not None

    status = await integration_service.get_pipeline_status()
    assert status.is_running
    assert status.file_connector_status == "running"
    assert status.correlation_engine_status == "active"
    assert status.memory_service_status == "active"
    logger.info("Service and components initialized successfully.")


@pytest.mark.asyncio
async def test_single_file_operation_creates_event(
    integration_service: EndToEndIntegrationService, test_directory: Path
):
    """Test that a single file operation is processed and creates a pipeline event."""
    initial_event_count = len(integration_service.captured_events)

    test_file = test_directory / "documents" / "single_op_test.txt"
    test_file.write_text("A single file operation.")

    # Wait for the event to be processed
    await asyncio.sleep(3.0)

    assert len(integration_service.captured_events) > initial_event_count

    # Check the newly captured event
    new_event = integration_service.captured_events[-1]
    assert "single_op_test.txt" in str(new_event.activity_event)
    assert new_event.current_stage in [PipelineStage.COMPLETED, PipelineStage.PERSISTENCE]
    logger.info(
        f"Single file operation processed, event captured and reached stage: {new_event.current_stage.value}"
    )


@pytest.mark.asyncio
async def test_correlation_and_anchor_creation(
    integration_service: EndToEndIntegrationService, test_directory: Path
):
    """Test that a pattern of file operations leads to correlation and memory anchor creation."""
    initial_event_count = len(integration_service.captured_events)

    project_dir = test_directory / "projects" / "correlated_project"
    project_dir.mkdir()

    # Create a series of related files to trigger a correlation
    files_to_create = ["README.md", "main.py", "utils.py", "requirements.txt"]
    for filename in files_to_create:
        (project_dir / filename).write_text(f"Content for {filename}")
        await asyncio.sleep(0.3)  # Short delay to ensure order

    # Wait for the pipeline to process everything
    await asyncio.sleep(8.0)

    new_events = integration_service.captured_events[initial_event_count:]
    assert len(new_events) >= len(files_to_create)

    # Check for events that resulted in correlations and anchors
    events_with_correlations = [e for e in new_events if e.detected_correlations]
    events_with_anchors = [e for e in new_events if e.created_anchors]

    assert len(events_with_correlations) > 0, "No correlations were detected."
    assert len(events_with_anchors) > 0, "No memory anchors were created."

    logger.info(
        f"Detected {len(events_with_correlations)} correlations and created {len(events_with_anchors)} anchors."
    )


@pytest.mark.asyncio
async def test_pipeline_statistics_and_monitoring(integration_service: EndToEndIntegrationService):
    """Test the collection of pipeline statistics and monitoring data."""
    # Ensure some events have been processed first
    assert len(integration_service.captured_events) > 0

    stats = await integration_service.get_pipeline_statistics()
    status = await integration_service.get_pipeline_status()

    assert stats.total_events_processed > 0
    assert stats.successful_events > 0
    assert "file_connector" in stats.component_stats
    assert "correlation_engine" in stats.component_stats

    assert status.events_processed > 0
    assert status.avg_processing_time_ms > 0

    logger.info(f"Statistics collected: {stats.total_events_processed} events processed.")
    logger.info(f"Monitoring status: avg processing time {status.avg_processing_time_ms:.2f}ms.")
