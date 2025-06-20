"""
Multi-LLM Layer for Mallku - Inspired by Indaleko

This module provides a unified interface to multiple LLM providers while
enforcing protection layers and prompt management. All LLM access must
go through this layer to ensure security and consistency.

Key principles:
- Provider abstraction allows switching between models
- Protection layer validates and preprocesses all prompts
- Caching reduces resource usage and improves performance
- Quality metrics track model performance
- Failover support for reliability
"""

import hashlib
import logging
import time
from abc import ABC, abstractmethod
from datetime import UTC, datetime, timedelta
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class LLMProvider(str, Enum):
    """Supported LLM providers."""

    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    AZURE_OPENAI = "azure_openai"
    GOOGLE = "google"
    COHERE = "cohere"
    LOCAL = "local"


class PromptCategory(str, Enum):
    """Categories of prompts for protection and caching."""

    DATABASE_VALIDATION = "database_validation"
    SCHEMA_ANALYSIS = "schema_analysis"
    DATA_CLASSIFICATION = "data_classification"
    SECURITY_EVALUATION = "security_evaluation"
    CONTENT_GENERATION = "content_generation"
    SYSTEM_ANALYSIS = "system_analysis"


class LLMRequest(BaseModel):
    """Request to the LLM layer."""

    prompt: str = Field(description="The prompt to send to the LLM")
    category: PromptCategory = Field(description="Category for protection and caching")
    context: dict[str, Any] = Field(default_factory=dict, description="Additional context")
    max_tokens: int = Field(default=1000, description="Maximum tokens to generate")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Sampling temperature")
    preferred_provider: LLMProvider | None = Field(
        default=None, description="Preferred LLM provider"
    )
    require_cached: bool = Field(default=False, description="Only use cached responses")
    priority: int = Field(default=5, ge=1, le=10, description="Request priority (1=highest)")


class LLMResponse(BaseModel):
    """Response from the LLM layer."""

    response_text: str = Field(description="Generated response")
    provider_used: LLMProvider = Field(description="Which provider generated this response")
    model_name: str = Field(description="Specific model used")
    tokens_used: int = Field(description="Total tokens consumed")
    processing_time: float = Field(description="Time taken in seconds")
    cached: bool = Field(description="Whether response came from cache")
    quality_score: float = Field(description="Quality assessment (0-1)")
    request_id: UUID = Field(default_factory=uuid4, description="Unique request identifier")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


class PromptCacheEntry(BaseModel):
    """Cached prompt and response."""

    prompt_hash: str = Field(description="Hash of the prompt and context")
    category: PromptCategory = Field(description="Prompt category")
    original_request: LLMRequest = Field(description="Original request")
    response: LLMResponse = Field(description="Cached response")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    last_accessed: datetime = Field(default_factory=lambda: datetime.now(UTC))
    access_count: int = Field(default=0, description="Number of times accessed")
    quality_rating: float = Field(default=0.0, description="User-provided quality rating")


class LLMMetrics(BaseModel):
    """Metrics for LLM usage and performance."""

    total_requests: int = Field(default=0)
    cached_responses: int = Field(default=0)
    total_tokens_used: int = Field(default=0)
    average_response_time: float = Field(default=0.0)
    provider_usage: dict[str, int] = Field(default_factory=dict)
    category_usage: dict[str, int] = Field(default_factory=dict)
    cache_hit_rate: float = Field(default=0.0)
    quality_scores: dict[str, float] = Field(default_factory=dict)


# === LLM Provider Interfaces ===


class BaseLLMProvider(ABC):
    """Base class for LLM providers."""

    def __init__(self, provider_config: dict[str, Any]):
        self.config = provider_config
        self.provider_name = self.get_provider_name()

    @abstractmethod
    def get_provider_name(self) -> LLMProvider:
        """Get the provider identifier."""
        pass

    @abstractmethod
    async def generate_response(self, request: LLMRequest) -> LLMResponse:
        """Generate response using this provider."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is currently available."""
        pass

    @abstractmethod
    def get_supported_models(self) -> list[str]:
        """Get list of supported models."""
        pass


class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude provider."""

    def get_provider_name(self) -> LLMProvider:
        return LLMProvider.ANTHROPIC

    async def generate_response(self, request: LLMRequest) -> LLMResponse:
        """Generate response using Anthropic Claude."""
        start_time = time.time()

        try:
            # Import anthropic client (would be actual implementation)
            # import anthropic

            # Simulate response for demo
            response_text = f"Anthropic response to: {request.prompt[:50]}..."
            tokens_used = len(response_text.split()) * 2  # Rough estimate

            processing_time = time.time() - start_time

            return LLMResponse(
                response_text=response_text,
                provider_used=self.provider_name,
                model_name="claude-3-sonnet",
                tokens_used=tokens_used,
                processing_time=processing_time,
                cached=False,
                quality_score=0.9,  # Would be calculated based on actual response
            )

        except Exception as e:
            logger.error(f"Anthropic provider error: {e}")
            raise

    def is_available(self) -> bool:
        """Check if Anthropic API is available."""
        # Would check API connectivity
        return True

    def get_supported_models(self) -> list[str]:
        """Get Anthropic models."""
        return ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"]


class OpenAIProvider(BaseLLMProvider):
    """OpenAI GPT provider."""

    def get_provider_name(self) -> LLMProvider:
        return LLMProvider.OPENAI

    async def generate_response(self, request: LLMRequest) -> LLMResponse:
        """Generate response using OpenAI GPT."""
        start_time = time.time()

        try:
            # Simulate response for demo
            response_text = f"OpenAI response to: {request.prompt[:50]}..."
            tokens_used = len(response_text.split()) * 2

            processing_time = time.time() - start_time

            return LLMResponse(
                response_text=response_text,
                provider_used=self.provider_name,
                model_name="gpt-4",
                tokens_used=tokens_used,
                processing_time=processing_time,
                cached=False,
                quality_score=0.85,
            )

        except Exception as e:
            logger.error(f"OpenAI provider error: {e}")
            raise

    def is_available(self) -> bool:
        """Check if OpenAI API is available."""
        return True

    def get_supported_models(self) -> list[str]:
        """Get OpenAI models."""
        return ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"]


# === Prompt Cache Manager ===


class PromptCacheManager:
    """
    Manages caching of prompts and responses.

    Implements intelligent caching strategies similar to database query plan caching.
    """

    def __init__(self, max_cache_size: int = 10000, ttl_hours: int = 24):
        self.cache: dict[str, PromptCacheEntry] = {}
        self.max_cache_size = max_cache_size
        self.ttl = timedelta(hours=ttl_hours)

    def _generate_cache_key(self, request: LLMRequest) -> str:
        """Generate cache key for request."""
        # Include prompt, category, and relevant context
        cache_data = {
            "prompt": request.prompt,
            "category": request.category.value,
            "context": request.context,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
        }

        cache_str = str(sorted(cache_data.items()))
        return hashlib.sha256(cache_str.encode()).hexdigest()

    async def get_cached_response(self, request: LLMRequest) -> LLMResponse | None:
        """Get cached response if available and valid."""
        cache_key = self._generate_cache_key(request)

        if cache_key not in self.cache:
            return None

        entry = self.cache[cache_key]

        # Check if cache entry is still valid
        if datetime.now(UTC) - entry.created_at > self.ttl:
            del self.cache[cache_key]
            return None

        # Update access tracking
        entry.last_accessed = datetime.now(UTC)
        entry.access_count += 1

        # Mark response as cached
        cached_response = entry.response.copy()
        cached_response.cached = True
        cached_response.request_id = uuid4()  # New request ID
        cached_response.timestamp = datetime.now(UTC)

        logger.info(f"Cache hit for category {request.category}")
        return cached_response

    async def cache_response(self, request: LLMRequest, response: LLMResponse) -> None:
        """Cache a response for future use."""
        cache_key = self._generate_cache_key(request)

        # Check cache size limit
        if len(self.cache) >= self.max_cache_size:
            await self._evict_old_entries()

        # Create cache entry
        entry = PromptCacheEntry(
            prompt_hash=cache_key,
            category=request.category,
            original_request=request,
            response=response,
        )

        self.cache[cache_key] = entry
        logger.info(f"Cached response for category {request.category}")

    async def _evict_old_entries(self) -> None:
        """Evict old cache entries using LRU strategy."""
        # Sort by last accessed time
        sorted_entries = sorted(self.cache.items(), key=lambda x: x[1].last_accessed)

        # Remove oldest 20% of entries
        evict_count = max(1, len(sorted_entries) // 5)
        for i in range(evict_count):
            cache_key = sorted_entries[i][0]
            del self.cache[cache_key]

        logger.info(f"Evicted {evict_count} cache entries")

    def get_cache_stats(self) -> dict[str, Any]:
        """Get cache statistics."""
        total_entries = len(self.cache)
        category_counts = {}

        for entry in self.cache.values():
            category = entry.category.value
            category_counts[category] = category_counts.get(category, 0) + 1

        return {
            "total_entries": total_entries,
            "max_size": self.max_cache_size,
            "category_distribution": category_counts,
            "oldest_entry": min((e.created_at for e in self.cache.values()), default=None),
            "newest_entry": max((e.created_at for e in self.cache.values()), default=None),
        }


# === Protection Layer ===


class PromptProtectionLayer:
    """
    Protection layer that validates and preprocesses prompts.

    This is a critical security component that ensures all prompts
    meet safety and quality standards before reaching LLMs.
    """

    def __init__(self):
        self.validation_rules: dict[PromptCategory, list[callable]] = {}
        self._register_default_rules()

    def _register_default_rules(self) -> None:
        """Register default validation rules for each category."""

        # Database validation rules
        self.validation_rules[PromptCategory.DATABASE_VALIDATION] = [
            self._validate_contains_schema_context,
            self._validate_no_injection_patterns,
            self._validate_required_examples,
        ]

        # Schema analysis rules
        self.validation_rules[PromptCategory.SCHEMA_ANALYSIS] = [
            self._validate_contains_field_descriptions,
            self._validate_security_context,
        ]

        # Security evaluation rules
        self.validation_rules[PromptCategory.SECURITY_EVALUATION] = [
            self._validate_security_scope,
            self._validate_no_sensitive_exposure,
        ]

    async def validate_and_preprocess(self, request: LLMRequest) -> LLMRequest:
        """
        Validate and preprocess a prompt request.

        This method ensures the prompt meets all safety and quality standards.
        """
        # Run category-specific validation rules
        if request.category in self.validation_rules:
            for rule in self.validation_rules[request.category]:
                rule(request)

        # Preprocess prompt
        processed_request = await self._preprocess_prompt(request)

        # Add safety context
        processed_request = await self._add_safety_context(processed_request)

        logger.info(f"Validated and preprocessed {request.category} prompt")
        return processed_request

    def _validate_contains_schema_context(self, request: LLMRequest) -> None:
        """Validate that database validation prompts contain schema context."""
        if "schema" not in request.prompt.lower() and "schema" not in request.context:
            raise ValueError("Database validation prompts must include schema context")

    def _validate_no_injection_patterns(self, request: LLMRequest) -> None:
        """Check for potential injection patterns."""
        dangerous_patterns = ["DROP", "DELETE", "TRUNCATE", "UPDATE"]
        prompt_upper = request.prompt.upper()

        for pattern in dangerous_patterns:
            if pattern in prompt_upper:
                logger.warning(f"Potential injection pattern detected: {pattern}")
                # Would implement more sophisticated detection in production

    def _validate_required_examples(self, request: LLMRequest) -> None:
        """Validate that prompts include sufficient examples."""
        if len(request.context.get("examples", [])) < 1:
            raise ValueError("At least one example required for database validation")

    def _validate_contains_field_descriptions(self, request: LLMRequest) -> None:
        """Validate schema analysis has field descriptions."""
        if "field" not in request.prompt.lower():
            logger.warning("Schema analysis prompt should reference fields")

    def _validate_security_context(self, request: LLMRequest) -> None:
        """Validate security context is provided."""
        if "security" not in request.context and "security" not in request.prompt.lower():
            logger.warning("Security context recommended for schema analysis")

    def _validate_security_scope(self, request: LLMRequest) -> None:
        """Validate security evaluation has appropriate scope."""
        if "evaluate" not in request.prompt.lower():
            raise ValueError("Security evaluation prompts must be clearly evaluative")

    def _validate_no_sensitive_exposure(self, request: LLMRequest) -> None:
        """Check that prompts don't expose sensitive information."""
        sensitive_patterns = ["password", "key", "secret", "token"]
        prompt_lower = request.prompt.lower()

        for pattern in sensitive_patterns:
            if pattern in prompt_lower:
                logger.warning(f"Potential sensitive data in prompt: {pattern}")

    async def _preprocess_prompt(self, request: LLMRequest) -> LLMRequest:
        """Preprocess prompt to improve quality and safety."""
        processed_prompt = request.prompt

        # Add category-specific prefixes
        if request.category == PromptCategory.DATABASE_VALIDATION:
            processed_prompt = f"Database Validation Task:\n{processed_prompt}"
        elif request.category == PromptCategory.SCHEMA_ANALYSIS:
            processed_prompt = f"Schema Analysis Task:\n{processed_prompt}"
        elif request.category == PromptCategory.SECURITY_EVALUATION:
            processed_prompt = f"Security Evaluation Task:\n{processed_prompt}"

        # Create processed request
        processed_request = request.copy()
        processed_request.prompt = processed_prompt

        return processed_request

    async def _add_safety_context(self, request: LLMRequest) -> LLMRequest:
        """Add safety context to the prompt."""
        safety_suffix = (
            "\n\nIMPORTANT: Provide analysis only. Do not execute any operations or modifications."
        )

        processed_request = request.copy()
        processed_request.prompt += safety_suffix

        return processed_request


# === Main Multi-LLM Service ===


class MultiLLMService:
    """
    Main service that coordinates all LLM operations.

    This is the ONLY interface that should be used for LLM operations in Mallku.
    """

    def __init__(self):
        self.providers: dict[LLMProvider, BaseLLMProvider] = {}
        self.cache_manager = PromptCacheManager()
        self.protection_layer = PromptProtectionLayer()
        self.metrics = LLMMetrics()
        self.default_provider = LLMProvider.ANTHROPIC

    async def initialize(self, provider_configs: dict[str, dict]) -> None:
        """Initialize the multi-LLM service with provider configurations."""
        try:
            # Initialize providers based on configuration
            if "anthropic" in provider_configs:
                self.providers[LLMProvider.ANTHROPIC] = AnthropicProvider(
                    provider_configs["anthropic"]
                )

            if "openai" in provider_configs:
                self.providers[LLMProvider.OPENAI] = OpenAIProvider(provider_configs["openai"])

            # Add more providers as needed

            logger.info(f"Initialized multi-LLM service with {len(self.providers)} providers")

        except Exception as e:
            logger.error(f"Failed to initialize multi-LLM service: {e}")
            raise

    async def generate_response(self, request: LLMRequest) -> LLMResponse:
        """
        Generate response using the multi-LLM system.

        This is the main entry point for all LLM operations.
        """
        try:
            # Update metrics
            self.metrics.total_requests += 1
            category_key = request.category.value
            self.metrics.category_usage[category_key] = (
                self.metrics.category_usage.get(category_key, 0) + 1
            )

            # Check cache first
            if not request.require_cached:
                cached_response = await self.cache_manager.get_cached_response(request)
                if cached_response:
                    self.metrics.cached_responses += 1
                    self._update_cache_hit_rate()
                    return cached_response

            # If cache required but not found, return error
            if request.require_cached:
                raise ValueError("Cached response required but not found")

            # Validate and preprocess through protection layer
            protected_request = await self.protection_layer.validate_and_preprocess(request)

            # Select provider
            provider = self._select_provider(protected_request)

            # Generate response
            response = await provider.generate_response(protected_request)

            # Update metrics
            self.metrics.total_tokens_used += response.tokens_used
            provider_key = response.provider_used.value
            self.metrics.provider_usage[provider_key] = (
                self.metrics.provider_usage.get(provider_key, 0) + 1
            )

            # Cache response
            await self.cache_manager.cache_response(protected_request, response)

            # Update average response time
            self._update_average_response_time(response.processing_time)

            # Update quality scores
            self.metrics.quality_scores[provider_key] = response.quality_score

            logger.info(f"Generated response using {response.provider_used}")
            return response

        except Exception as e:
            logger.error(f"Failed to generate response: {e}")
            raise

    def _select_provider(self, request: LLMRequest) -> BaseLLMProvider:
        """Select the best provider for the request."""
        # Use preferred provider if specified and available
        if request.preferred_provider and request.preferred_provider in self.providers:
            provider = self.providers[request.preferred_provider]
            if provider.is_available():
                return provider

        # Use default provider if available
        if self.default_provider in self.providers:
            provider = self.providers[self.default_provider]
            if provider.is_available():
                return provider

        # Use any available provider
        for provider in self.providers.values():
            if provider.is_available():
                return provider

        raise RuntimeError("No LLM providers available")

    def _update_cache_hit_rate(self) -> None:
        """Update cache hit rate metric."""
        if self.metrics.total_requests > 0:
            self.metrics.cache_hit_rate = (
                self.metrics.cached_responses / self.metrics.total_requests
            )

    def _update_average_response_time(self, response_time: float) -> None:
        """Update average response time metric."""
        current_avg = self.metrics.average_response_time
        total_requests = self.metrics.total_requests

        if total_requests == 1:
            self.metrics.average_response_time = response_time
        else:
            # Incremental average calculation
            self.metrics.average_response_time = (
                current_avg * (total_requests - 1) + response_time
            ) / total_requests

    async def get_service_metrics(self) -> LLMMetrics:
        """Get comprehensive service metrics."""
        return self.metrics

    async def get_cache_statistics(self) -> dict[str, Any]:
        """Get cache statistics."""
        return self.cache_manager.get_cache_stats()

    async def validate_database_schema(
        self, schema_definition: dict, collection_description: str, examples: list[str]
    ) -> dict[str, Any]:
        """
        Validate database schema using LLM analysis.

        This is a convenience method for database validation tasks.
        """
        request = LLMRequest(
            prompt=f"""
            Analyze this database schema for completeness and quality:

            Collection: {collection_description}
            Schema: {schema_definition}

            Evaluate:
            1. Are field types appropriate for the data?
            2. Are security strategies suitable?
            3. Are index strategies optimal?
            4. Are there missing required fields?
            5. Is the schema well-designed for the described purpose?

            Provide specific recommendations for improvements.
            """,
            category=PromptCategory.DATABASE_VALIDATION,
            context={
                "schema": schema_definition,
                "description": collection_description,
                "examples": examples,
            },
            max_tokens=1500,
            temperature=0.3,  # Lower temperature for analytical tasks
        )

        response = await self.generate_response(request)

        return {
            "validation_result": response.response_text,
            "quality_score": response.quality_score,
            "provider_used": response.provider_used.value,
            "tokens_used": response.tokens_used,
        }
