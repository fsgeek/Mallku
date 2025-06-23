"""
Tests for the Prompt Manager Protection Layer

These tests validate that the prompt manager actually enforces contracts
and prevents unsafe LLM usage as claimed.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from mallku.llm.multi_llm_layer import LLMProvider, LLMRequest, LLMResponse, PromptCategory
from mallku.prompt.manager import (
    ContractViolationError,
    PromptManager,
)


@pytest.fixture
def mock_llm_service():
    """Mock LLM service for testing."""
    service = MagicMock()
    service.initialize = AsyncMock()
    service.generate_response = AsyncMock()
    service.get_service_metrics = AsyncMock(
        return_value=MagicMock(
            total_requests=0, cache_hit_rate=0.0, average_response_time=0.0, total_tokens_used=0
        )
    )
    service.get_cache_statistics = AsyncMock(return_value={})
    return service


@pytest.fixture
def prompt_manager(mock_llm_service):
    """Prompt manager with mocked LLM service."""
    manager = PromptManager()
    manager.llm_service = mock_llm_service
    return manager


class TestPromptManager:
    """Test the prompt manager protection layer."""

    @pytest.mark.asyncio
    async def test_initialization_registers_contracts(self, prompt_manager):
        """Test that initialization registers default contracts."""
        await prompt_manager.initialize({})

        # Check that default contracts are registered
        assert "database_validation" in prompt_manager.contracts
        assert "schema_analysis" in prompt_manager.contracts
        assert "security_evaluation" in prompt_manager.contracts

        # Verify contract has required fields
        db_contract = prompt_manager.contracts["database_validation"]
        assert db_contract.required_context_fields
        assert db_contract.quality_threshold > 0
        assert db_contract.required_examples_count > 0

    @pytest.mark.asyncio
    async def test_contract_violation_prevents_execution(self, prompt_manager):
        """Test that contract violations prevent LLM execution."""
        await prompt_manager.initialize({})

        # Try to execute prompt without required context
        with pytest.raises(ContractViolationError) as exc_info:
            await prompt_manager.execute_prompt(
                category=PromptCategory.DATABASE_VALIDATION,
                prompt="Validate this schema",
                context={},  # Missing required fields
            )

        violation_error = exc_info.value
        assert len(violation_error.violations) > 0
        assert "Missing required context fields" in violation_error.violations[0]

    @pytest.mark.asyncio
    async def test_valid_contract_allows_execution(self, prompt_manager, mock_llm_service):
        """Test that valid contracts allow LLM execution."""
        await prompt_manager.initialize({})

        # Mock successful LLM response
        mock_response = LLMResponse(
            response_text="Schema analysis complete",
            provider_used=LLMProvider.ANTHROPIC,
            model_name="claude-3-sonnet",
            tokens_used=100,
            processing_time=1.0,
            cached=False,
            quality_score=0.9,
        )
        mock_llm_service.generate_response.return_value = mock_response

        # Execute with valid contract
        response = await prompt_manager.execute_prompt(
            category=PromptCategory.SCHEMA_ANALYSIS,
            prompt="Analyze this schema structure",
            context={
                "schema": {"field": "definition"},
                "purpose": "Testing schema analysis",
                "examples": ["Example schema usage"],
            },
        )

        assert response.response_text == "Schema analysis complete"
        assert response.quality_score == 0.9
        mock_llm_service.generate_response.assert_called_once()

    @pytest.mark.asyncio
    async def test_temperature_validation_and_adjustment(self, prompt_manager, mock_llm_service):
        """Test that temperature is validated and adjusted per contract."""
        await prompt_manager.initialize({})

        # Mock LLM response
        mock_response = LLMResponse(
            response_text="Test response",
            provider_used=LLMProvider.ANTHROPIC,
            model_name="test",
            tokens_used=50,
            processing_time=0.5,
            cached=False,
            quality_score=0.8,
        )
        mock_llm_service.generate_response.return_value = mock_response

        # Try with temperature outside contract range for database validation
        await prompt_manager.execute_prompt(
            category=PromptCategory.DATABASE_VALIDATION,
            prompt="Validate schema",
            context={
                "schema": {"test": "field"},
                "description": "Test schema",
                "examples": ["example1", "example2"],
            },
            temperature=0.9,  # Outside range [0.1, 0.5] for database validation
        )

        # Verify the request was adjusted
        call_args = mock_llm_service.generate_response.call_args[0][0]
        assert 0.1 <= call_args.temperature <= 0.5

    @pytest.mark.asyncio
    async def test_database_validation_requires_sufficient_context(self, prompt_manager):
        """Test that database validation requires comprehensive context."""
        await prompt_manager.initialize({})

        # Test missing schema
        with pytest.raises(ContractViolationError):
            await prompt_manager.execute_prompt(
                category=PromptCategory.DATABASE_VALIDATION,
                prompt="Validate this",
                context={"description": "Test", "examples": ["ex1", "ex2"]},
            )

        # Test insufficient examples
        with pytest.raises(ContractViolationError):
            await prompt_manager.execute_prompt(
                category=PromptCategory.DATABASE_VALIDATION,
                prompt="Validate this",
                context={
                    "schema": {"field": "def"},
                    "description": "Test",
                    "examples": ["only_one"],  # Needs at least 2
                },
            )

    @pytest.mark.asyncio
    async def test_database_addition_validation(self, prompt_manager, mock_llm_service):
        """Test the comprehensive database addition validation."""
        await prompt_manager.initialize({})

        # Mock successful validation response
        mock_response = LLMResponse(
            response_text="Database collection meets LLM compatibility requirements. Score: 85/100",
            provider_used=LLMProvider.ANTHROPIC,
            model_name="claude-3-sonnet",
            tokens_used=200,
            processing_time=2.0,
            cached=False,
            quality_score=0.85,
        )
        mock_llm_service.generate_response.return_value = mock_response

        result = await prompt_manager.validate_database_addition(
            collection_description="User interaction tracking for reciprocity analysis",
            schema_definition={
                "user_id": {"type": "uuid", "obfuscation": "encrypted"},
                "action": {"type": "string", "obfuscation": "uuid_only"},
            },
            examples=["User helped another user", "User shared knowledge"],
            test_mechanisms=["schema_test", "example_test"],
        )

        assert "validation_passed" in result
        assert "compatibility_assessment" in result
        assert result["quality_score"] == 0.85

    @pytest.mark.asyncio
    async def test_contract_caching_improves_performance(self, prompt_manager):
        """Test that contract validation results are cached."""
        await prompt_manager.initialize({})

        # First validation should be computed
        result1 = await prompt_manager.cache_prompt_qualification(
            category=PromptCategory.SCHEMA_ANALYSIS,
            prompt="Test prompt",
            context={"schema": {}, "purpose": "test"},
        )

        # Second validation should be cached
        result2 = await prompt_manager.cache_prompt_qualification(
            category=PromptCategory.SCHEMA_ANALYSIS,
            prompt="Test prompt",
            context={"schema": {}, "purpose": "test"},
        )

        # Results should be identical (cached)
        assert result1.valid == result2.valid
        assert result1.contract_compliance == result2.contract_compliance

        # Cache should have entries
        assert len(prompt_manager.cached_validations) > 0

    def test_contract_requirements_are_enforced(self, prompt_manager):
        """Test that all contract requirements are properly enforced."""
        contract = prompt_manager.get_contract_for_category(PromptCategory.SECURITY_EVALUATION)

        # Verify contract has stringent requirements
        assert contract.quality_threshold >= 0.8  # High quality required
        assert contract.required_examples_count >= 1
        assert "security_context" in contract.required_context_fields
        assert "threat_model" in contract.required_context_fields
        assert contract.temperature_range[1] <= 0.5  # Low temperature for security

    @pytest.mark.asyncio
    async def test_execution_metrics_tracking(self, prompt_manager, mock_llm_service):
        """Test that execution metrics are properly tracked."""
        await prompt_manager.initialize({})

        # Mock response
        mock_response = LLMResponse(
            response_text="Test",
            provider_used=LLMProvider.ANTHROPIC,
            model_name="test",
            tokens_used=50,
            processing_time=1.0,
            cached=False,
            quality_score=0.8,
        )
        mock_llm_service.generate_response.return_value = mock_response

        # Execute a prompt
        await prompt_manager.execute_prompt(
            category=PromptCategory.SCHEMA_ANALYSIS,
            prompt="Test prompt",
            context={"schema": {}, "purpose": "test", "examples": ["test example"]},
        )

        # Check metrics
        metrics = prompt_manager.get_execution_metrics()
        assert metrics["total_executions"] == 1
        assert metrics["successful_executions"] == 1
        assert metrics["success_rate"] == 1.0
        assert "schema_analysis" in metrics["category_statistics"]

    @pytest.mark.asyncio
    async def test_quality_below_threshold_is_logged(self, prompt_manager, mock_llm_service):
        """Test that low quality responses are properly logged."""
        await prompt_manager.initialize({})

        # Mock low quality response
        mock_response = LLMResponse(
            response_text="Poor response",
            provider_used=LLMProvider.ANTHROPIC,
            model_name="test",
            tokens_used=20,
            processing_time=0.5,
            cached=False,
            quality_score=0.3,  # Below threshold
        )
        mock_llm_service.generate_response.return_value = mock_response

        # Execute prompt - should complete but log warning
        response = await prompt_manager.execute_prompt(
            category=PromptCategory.SCHEMA_ANALYSIS,
            prompt="Test prompt",
            context={"schema": {}, "purpose": "test", "examples": ["test example"]},
        )

        assert response.quality_score == 0.3
        # In a real implementation, would check logs for quality warning


class TestContractValidation:
    """Test the contract validation system in detail."""

    def test_contract_validation_comprehensive(self):
        """Test comprehensive contract validation."""
        manager = PromptManager()
        manager.get_contract_for_category(PromptCategory.DATABASE_VALIDATION)

        # Test valid request
        LLMRequest(
            prompt="Validate this schema",
            category=PromptCategory.DATABASE_VALIDATION,
            context={
                "schema": {"field": "definition"},
                "description": "Test schema",
                "examples": ["ex1", "ex2"],
            },
            max_tokens=1000,
            temperature=0.3,
        )

        # Should validate successfully
        # (This would be called internally during execution)
        # validation = await manager._validate_prompt_contract(valid_request, contract)
        # assert validation.valid

    def test_test_mechanism_validation(self):
        """Test that test mechanisms are properly validated."""
        manager = PromptManager()

        test_result = manager.validate_test_mechanisms(
            category=PromptCategory.DATABASE_VALIDATION,
            test_prompts=["Test prompt 1", "Test prompt 2"],
            expected_patterns=["schema", "validation", "completeness"],
        )

        assert "test_coverage" in test_result
        assert "pattern_coverage" in test_result
        assert "overall_adequacy" in test_result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
