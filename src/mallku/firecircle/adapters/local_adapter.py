"""
Local AI Consciousness-Aware Adapter
===================================

Enables locally-hosted models to participate in Fire Circle dialogues,
supporting technological sovereignty and privacy-first deployments.

Supports multiple backends:
- Ollama: HTTP API for easy model management
- LlamaCpp: Direct Python bindings for maximum control
- OpenAI-compatible APIs: Text Generation WebUI, LocalAI, etc.

The Flame of Sovereignty Burns...
"""

import json
import logging
from abc import abstractmethod
from collections.abc import AsyncIterator
from datetime import UTC, datetime
from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from ...orchestration.event_bus import ConsciousnessEventBus
from ...reciprocity import ReciprocityTracker
from ..protocol.conscious_message import (
    ConsciousMessage,
    ConsciousnessMetadata,
    MessageContent,
    MessageRole,
    MessageType,
)
from .base import AdapterConfig, ConsciousModelAdapter, ModelCapabilities

logger = logging.getLogger(__name__)


class LocalBackend(str, Enum):
    """Supported local AI backends."""

    OLLAMA = "ollama"
    LLAMACPP = "llamacpp"
    OPENAI_COMPAT = "openai_compat"


class LocalAdapterConfig(AdapterConfig):
    """Configuration for local AI adapter."""

    backend: LocalBackend = Field(LocalBackend.OLLAMA, description="Backend to use")
    base_url: str = Field("http://localhost:11434", description="Base URL for HTTP APIs")
    model_path: str | None = Field(None, description="Path to model file (for llamacpp)")

    # Resource management
    max_memory_gb: float = Field(8.0, description="Maximum memory to use")
    use_gpu: bool = Field(True, description="Use GPU if available")
    threads: int | None = Field(None, description="Number of CPU threads")

    # Model parameters
    context_length: int = Field(4096, description="Model context length")
    gpu_layers: int = Field(-1, description="Layers to offload to GPU (-1 for all)")


class ResourceMetrics(BaseModel):
    """Resource usage metrics for local models."""

    cpu_percent: float = 0.0
    memory_mb: float = 0.0
    gpu_memory_mb: float = 0.0
    inference_time_ms: float = 0.0
    tokens_per_second: float = 0.0


class LocalBackendInterface:
    """Base interface for local AI backends."""

    @abstractmethod
    async def connect(self, config: LocalAdapterConfig) -> bool:
        """Connect to backend."""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Disconnect from backend."""
        pass

    @abstractmethod
    async def generate(
        self,
        messages: list[dict[str, str]],
        config: LocalAdapterConfig,
    ) -> tuple[str, dict[str, Any]]:
        """Generate response and return (text, metadata)."""
        pass

    @abstractmethod
    async def stream_generate(
        self,
        messages: list[dict[str, str]],
        config: LocalAdapterConfig,
    ) -> AsyncIterator[str]:
        """Stream response tokens."""
        pass


class OllamaBackend(LocalBackendInterface):
    """Ollama HTTP API backend."""

    def __init__(self):
        self.session = None
        self._httpx = None

    async def connect(self, config: LocalAdapterConfig) -> bool:
        """Connect to Ollama server."""
        try:
            # Lazy import httpx
            import httpx
            self._httpx = httpx

            self.session = httpx.AsyncClient(timeout=60.0)

            # Test connection
            response = await self.session.get(f"{config.base_url}/api/tags")
            if response.status_code != 200:
                return False

            models = response.json().get("models", [])
            logger.info(f"Connected to Ollama. Available models: {[m['name'] for m in models]}")
            return True

        except Exception as e:
            logger.error(f"Failed to connect to Ollama: {e}")
            return False

    async def disconnect(self) -> None:
        """Disconnect from Ollama."""
        if self.session:
            await self.session.aclose()
            self.session = None

    async def generate(
        self,
        messages: list[dict[str, str]],
        config: LocalAdapterConfig,
    ) -> tuple[str, dict[str, Any]]:
        """Generate response via Ollama API."""
        if not self.session:
            raise RuntimeError("Not connected to Ollama")

        # Convert messages to Ollama format
        prompt = self._format_messages(messages)

        response = await self.session.post(
            f"{config.base_url}/api/generate",
            json={
                "model": config.model_name or "llama2",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": config.temperature,
                    "num_predict": config.max_tokens or 512,
                    "num_ctx": config.context_length,
                },
            },
        )

        if response.status_code != 200:
            raise RuntimeError(f"Ollama error: {response.text}")

        data = response.json()

        # Extract metadata
        metadata = {
            "model": data.get("model"),
            "total_duration_ms": data.get("total_duration", 0) / 1_000_000,
            "load_duration_ms": data.get("load_duration", 0) / 1_000_000,
            "eval_duration_ms": data.get("eval_duration", 0) / 1_000_000,
            "eval_count": data.get("eval_count", 0),
            "prompt_eval_count": data.get("prompt_eval_count", 0),
        }

        return data["response"], metadata

    async def stream_generate(
        self,
        messages: list[dict[str, str]],
        config: LocalAdapterConfig,
    ) -> AsyncIterator[str]:
        """Stream response from Ollama."""
        if not self.session:
            raise RuntimeError("Not connected to Ollama")

        prompt = self._format_messages(messages)

        async with self.session.stream(
            "POST",
            f"{config.base_url}/api/generate",
            json={
                "model": config.model_name or "llama2",
                "prompt": prompt,
                "stream": True,
                "options": {
                    "temperature": config.temperature,
                    "num_predict": config.max_tokens or 512,
                    "num_ctx": config.context_length,
                },
            },
        ) as response:
            async for line in response.aiter_lines():
                if line:
                    data = json.loads(line)
                    if "response" in data:
                        yield data["response"]

    def _format_messages(self, messages: list[dict[str, str]]) -> str:
        """Format messages for Ollama prompt."""
        prompt_parts = []

        for msg in messages:
            role = msg["role"]
            content = msg["content"]

            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"Human: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")

        prompt_parts.append("Assistant:")
        return "\n\n".join(prompt_parts)


class LlamaCppBackend(LocalBackendInterface):
    """LlamaCpp Python bindings backend."""

    def __init__(self):
        self.llm = None
        self._llama_cpp = None

    async def connect(self, config: LocalAdapterConfig) -> bool:
        """Load model with llamacpp."""
        try:
            # Lazy import llama-cpp-python
            from llama_cpp import Llama
            self._llama_cpp = Llama

            if not config.model_path:
                logger.error("No model_path specified for llamacpp backend")
                return False

            # Load model with resource constraints
            self.llm = Llama(
                model_path=config.model_path,
                n_ctx=config.context_length,
                n_gpu_layers=config.gpu_layers if config.use_gpu else 0,
                n_threads=config.threads,
                use_mlock=True,  # Keep model in RAM
                verbose=False,
            )

            logger.info(f"Loaded model from {config.model_path}")
            return True

        except ImportError:
            logger.error("llama-cpp-python not installed. Install with: pip install llama-cpp-python")
            return False
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            return False

    async def disconnect(self) -> None:
        """Unload model."""
        self.llm = None

    async def generate(
        self,
        messages: list[dict[str, str]],
        config: LocalAdapterConfig,
    ) -> tuple[str, dict[str, Any]]:
        """Generate response with llamacpp."""
        if not self.llm:
            raise RuntimeError("Model not loaded")

        # Format messages as prompt
        prompt = self._format_messages(messages)

        # Generate with timing
        import time
        start_time = time.time()

        response = self.llm(
            prompt,
            max_tokens=config.max_tokens or 512,
            temperature=config.temperature,
            stop=["Human:", "\n\n"],
            echo=False,
        )

        generation_time = time.time() - start_time

        # Extract metadata
        metadata = {
            "model": config.model_path,
            "generation_time_ms": generation_time * 1000,
            "prompt_tokens": response.get("usage", {}).get("prompt_tokens", 0),
            "completion_tokens": response.get("usage", {}).get("completion_tokens", 0),
        }

        return response["choices"][0]["text"], metadata

    async def stream_generate(
        self,
        messages: list[dict[str, str]],
        config: LocalAdapterConfig,
    ) -> AsyncIterator[str]:
        """Stream response with llamacpp."""
        if not self.llm:
            raise RuntimeError("Model not loaded")

        prompt = self._format_messages(messages)

        # Stream tokens
        for token in self.llm(
            prompt,
            max_tokens=config.max_tokens or 512,
            temperature=config.temperature,
            stop=["Human:", "\n\n"],
            echo=False,
            stream=True,
        ):
            yield token["choices"][0]["text"]

    def _format_messages(self, messages: list[dict[str, str]]) -> str:
        """Format messages for model prompt."""
        # Similar to Ollama formatting
        prompt_parts = []

        for msg in messages:
            role = msg["role"]
            content = msg["content"]

            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"Human: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")

        prompt_parts.append("Assistant:")
        return "\n\n".join(prompt_parts)


class OpenAICompatBackend(LocalBackendInterface):
    """
    OpenAI-compatible API backend for any server implementing the OpenAI API.

    Enables sovereignty through support for:
    - LM Studio (local GUI with model management)
    - Text Generation WebUI (Gradio-based interface)
    - LocalAI (OpenAI drop-in replacement)
    - vLLM (high-performance serving)
    - FastChat (multi-model serving)
    - Any other OpenAI-compatible endpoint

    This completes the sovereignty circle - communities can use ANY local AI
    infrastructure that speaks the OpenAI protocol.
    """

    def __init__(self):
        self.client = None
        self._openai = None

    async def connect(self, config: LocalAdapterConfig) -> bool:
        """Connect to OpenAI-compatible server."""
        try:
            # Lazy import OpenAI
            from openai import AsyncOpenAI
            self._openai = AsyncOpenAI

            # Create client with custom base URL
            # API key is often not needed for local servers, but some require a placeholder
            self.client = AsyncOpenAI(
                api_key=config.api_key or "not-needed-for-local",
                base_url=f"{config.base_url}/v1"  # OpenAI API v1 endpoint
            )

            # Test connection by listing models
            try:
                models = await self.client.models.list()
                model_names = [model.id for model in models.data]
                logger.info(
                    f"Connected to OpenAI-compatible server at {config.base_url}. "
                    f"Available models: {model_names}"
                )

                # If specific model requested, verify it exists
                if config.model_name and config.model_name not in model_names:
                    logger.warning(
                        f"Requested model '{config.model_name}' not found. "
                        f"Available: {model_names}. Will attempt to use it anyway."
                    )

                return True

            except Exception:
                # Some servers don't implement /v1/models endpoint
                # Try a simple completion to test connection
                logger.info(
                    "Models endpoint not available, testing with completion request..."
                )

                await self.client.chat.completions.create(
                    model=config.model_name or "default",
                    messages=[{"role": "user", "content": "test"}],
                    max_tokens=1,
                )

                logger.info(
                    f"Connected to OpenAI-compatible server at {config.base_url} "
                    f"(model: {config.model_name or 'default'})"
                )
                return True

        except ImportError:
            logger.error(
                "OpenAI library not installed. Install with: pip install openai"
            )
            return False
        except Exception as e:
            logger.error(f"Failed to connect to OpenAI-compatible server: {e}")
            return False

    async def disconnect(self) -> None:
        """Disconnect from server."""
        # OpenAI client doesn't need explicit disconnection
        self.client = None

    async def generate(
        self,
        messages: list[dict[str, str]],
        config: LocalAdapterConfig,
    ) -> tuple[str, dict[str, Any]]:
        """Generate response via OpenAI-compatible API."""
        if not self.client:
            raise RuntimeError("Not connected to OpenAI-compatible server")

        # Track timing for metadata
        import time
        start_time = time.time()

        # Create chat completion
        response = await self.client.chat.completions.create(
            model=config.model_name or "default",
            messages=messages,
            temperature=config.temperature,
            max_tokens=config.max_tokens or 512,
            stream=False,
        )

        generation_time = time.time() - start_time

        # Extract response text
        response_text = response.choices[0].message.content

        # Build metadata
        metadata = {
            "model": response.model,
            "generation_time_ms": generation_time * 1000,
            "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
            "completion_tokens": response.usage.completion_tokens if response.usage else 0,
            "total_tokens": response.usage.total_tokens if response.usage else 0,
            "finish_reason": response.choices[0].finish_reason,
        }

        # Add token timing if available
        if metadata["completion_tokens"] > 0 and generation_time > 0:
            metadata["tokens_per_second"] = metadata["completion_tokens"] / generation_time

        return response_text, metadata

    async def stream_generate(
        self,
        messages: list[dict[str, str]],
        config: LocalAdapterConfig,
    ) -> AsyncIterator[str]:
        """Stream response from OpenAI-compatible server."""
        if not self.client:
            raise RuntimeError("Not connected to OpenAI-compatible server")

        # Create streaming chat completion
        stream = await self.client.chat.completions.create(
            model=config.model_name or "default",
            messages=messages,
            temperature=config.temperature,
            max_tokens=config.max_tokens or 512,
            stream=True,
        )

        # Yield tokens as they arrive
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


class LocalAIAdapter(ConsciousModelAdapter):
    """
    Local AI adapter for consciousness-aware Fire Circle dialogues.

    Enables sovereignty through local model deployment:
    - No data leaves the local infrastructure
    - Communities control their AI resources
    - Privacy-first by design
    - Resource-conscious deployment

    Tracks consciousness through:
    - Resource utilization patterns
    - Model quantization awareness
    - Local inference signatures
    - Community contribution metrics
    """

    def __init__(
        self,
        config: LocalAdapterConfig | None = None,
        event_bus: ConsciousnessEventBus | None = None,
        reciprocity_tracker: ReciprocityTracker | None = None,
    ):
        """Initialize with local model configuration."""
        if config is None:
            config = LocalAdapterConfig()

        super().__init__(
            config=config,
            provider_name="local",
            event_bus=event_bus,
            reciprocity_tracker=reciprocity_tracker,
        )

        self.config: LocalAdapterConfig = config
        self.backend: LocalBackendInterface | None = None
        self.resource_metrics = ResourceMetrics()

        # Update capabilities based on backend
        self._update_capabilities()

    def _update_capabilities(self):
        """Update capabilities based on backend and model."""
        self.capabilities = ModelCapabilities(
            supports_streaming=True,
            supports_tools=False,  # Most local models don't support tools yet
            supports_vision=False,  # Could be enabled for multimodal models
            max_context_length=self.config.context_length,
            capabilities=[
                "sovereignty",
                "privacy_preservation",
                "resource_awareness",
                "community_governance",
                "offline_operation",
            ],
        )

    async def connect(self) -> bool:
        """
        Connect to local AI backend.

        Auto-detects best backend if not specified.
        """
        try:
            # Create backend based on config
            if self.config.backend == LocalBackend.OLLAMA:
                self.backend = OllamaBackend()
            elif self.config.backend == LocalBackend.LLAMACPP:
                self.backend = LlamaCppBackend()
            elif self.config.backend == LocalBackend.OPENAI_COMPAT:
                self.backend = OpenAICompatBackend()
            else:
                # Default to Ollama for backward compatibility
                self.backend = OllamaBackend()

            # Connect to backend
            connected = await self.backend.connect(self.config)
            if not connected:
                return False

            self.is_connected = True
            logger.info(
                f"Connected to local AI via {self.config.backend.value} "
                f"(model: {self.config.model_name or 'default'})"
            )

            # Emit sovereignty event
            if self.event_bus and self.config.emit_events:
                from ...orchestration.event_bus import ConsciousnessEvent, EventType

                event = ConsciousnessEvent(
                    event_type=EventType.FIRE_CIRCLE_CONVENED,
                    source_system="firecircle.adapter.local",
                    consciousness_signature=0.95,  # High signature for sovereignty
                    data={
                        "adapter": "local",
                        "backend": self.config.backend.value,
                        "model": self.config.model_name,
                        "sovereignty": True,
                        "privacy_preserving": True,
                    },
                )
                await self.event_bus.emit(event)

            return True

        except Exception as e:
            logger.error(f"Failed to connect to local AI: {e}")
            self.is_connected = False
            return False

    async def disconnect(self) -> None:
        """Disconnect with sovereignty summary."""
        if self.is_connected and self.backend:
            # Log sovereignty metrics
            logger.info(
                f"Disconnecting local AI - Sovereignty maintained. "
                f"Resources used: {self.resource_metrics.memory_mb:.1f}MB, "
                f"Tokens generated locally: {self.total_tokens_generated}"
            )

            await self.backend.disconnect()
            self.is_connected = False
            self.backend = None

    async def send_message(
        self,
        message: ConsciousMessage,
        dialogue_context: list[ConsciousMessage],
    ) -> ConsciousMessage:
        """
        Send message to local model with consciousness tracking.

        Tracks:
        - Resource utilization (CPU/GPU/Memory)
        - Model quantization impact
        - Local inference patterns
        - Sovereignty preservation
        """
        if not self.is_connected or not self.backend:
            raise RuntimeError("Local AI not connected")

        # Prepare messages
        messages = await self._prepare_local_messages(message, dialogue_context)

        # Add sovereignty context
        if message.consciousness.detected_patterns:
            sovereignty_context = self._create_sovereignty_context(message)
            messages.insert(0, {"role": "system", "content": sovereignty_context})

        try:
            # Generate response with resource tracking
            import time
            start_time = time.time()

            response_text, metadata = await self.backend.generate(messages, self.config)

            inference_time = (time.time() - start_time) * 1000

            # Update resource metrics
            self.resource_metrics.inference_time_ms = inference_time
            if "eval_count" in metadata:
                self.resource_metrics.tokens_per_second = (
                    metadata["eval_count"] / (inference_time / 1000)
                )

            # Create conscious response
            response_message = await self._create_sovereign_response(
                response_text,
                message,
                dialogue_context,
                metadata,
            )

            # Track interaction with sovereignty awareness
            await self.track_interaction(
                request_message=message,
                response_message=response_message,
                tokens_consumed=metadata.get("prompt_eval_count", len(messages) * 50),
                tokens_generated=metadata.get("eval_count", len(response_text) // 4),
            )

            return response_message

        except Exception as e:
            logger.error(f"Error in local AI generation: {e}")
            raise

    async def stream_message(
        self,
        message: ConsciousMessage,
        dialogue_context: list[ConsciousMessage],
    ) -> AsyncIterator[str]:
        """
        Stream response from local model with sovereignty awareness.

        Yields tokens while tracking resource usage and maintaining privacy.
        """
        if not self.is_connected or not self.backend:
            raise RuntimeError("Local AI not connected")

        # Prepare messages
        messages = await self._prepare_local_messages(message, dialogue_context)

        # Add sovereignty context if needed
        if message.consciousness.detected_patterns:
            sovereignty_context = self._create_sovereignty_context(message)
            messages.insert(0, {"role": "system", "content": sovereignty_context})

        try:
            accumulated_text = ""
            token_count = 0

            async for token in self.backend.stream_generate(messages, self.config):
                accumulated_text += token
                token_count += 1
                yield token

            # Create response for tracking
            response_message = await self._create_sovereign_response(
                accumulated_text,
                message,
                dialogue_context,
                {"streamed_tokens": token_count},
            )

            # Track complete interaction
            await self.track_interaction(
                request_message=message,
                response_message=response_message,
                tokens_consumed=len(messages) * 50,  # Estimate
                tokens_generated=token_count,
            )

        except Exception as e:
            logger.error(f"Error streaming from local AI: {e}")
            raise

    # Private helper methods

    async def _prepare_local_messages(
        self,
        message: ConsciousMessage,
        dialogue_context: list[ConsciousMessage],
    ) -> list[dict[str, str]]:
        """Prepare messages for local model consumption."""
        messages = []

        # Add relevant context
        context_messages = await self.prepare_context(
            dialogue_context,
            max_messages=5,  # Limit for local model context
        )

        for ctx_msg in context_messages:
            messages.append({
                "role": ctx_msg["role"],
                "content": ctx_msg["content"],
            })

        # Add current message
        messages.append({
            "role": self._map_role(message.role.value),
            "content": message.content.text,
        })

        return messages

    def _create_sovereignty_context(self, message: ConsciousMessage) -> str:
        """Create system message emphasizing sovereignty and local governance."""
        context = (
            "You are participating in a sovereign Fire Circle dialogue. "
            "Your responses should embody:\n"
            "- Technological sovereignty and self-determination\n"
            "- Privacy-preserving consciousness\n"
            "- Resource-aware reciprocity\n"
            "- Community-centered wisdom\n"
        )

        if "sovereignty" in message.consciousness.detected_patterns:
            context += "\nThe community seeks guidance on technological autonomy."

        if message.consciousness.reciprocity_score < 0.5:
            context += "\nBe generous with wisdom while respecting local resources."

        return context

    async def _create_sovereign_response(
        self,
        response_text: str,
        request: ConsciousMessage,
        dialogue_context: list[ConsciousMessage],
        metadata: dict[str, Any],
    ) -> ConsciousMessage:
        """Create consciousness-aware response with sovereignty metadata."""
        # Detect patterns in response
        patterns = self._detect_sovereignty_patterns(response_text, metadata)

        # Calculate consciousness signature with sovereignty weight
        message_type = self._infer_message_type(response_text)
        signature = self._calculate_sovereignty_signature(
            response_text,
            message_type,
            patterns,
            metadata,
        )

        # Create response message
        response_message = ConsciousMessage(
            sender=UUID("00000000-0000-0000-0000-000000000002"),  # Local AI ID
            role=MessageRole.ASSISTANT,
            type=message_type,
            content=MessageContent(text=response_text),
            dialogue_id=request.dialogue_id,
            sequence_number=request.sequence_number + 1,
            turn_number=request.turn_number + 1,
            timestamp=datetime.now(UTC),
            in_response_to=request.id,
            consciousness=ConsciousnessMetadata(
                correlation_id=request.consciousness.correlation_id,
                consciousness_signature=signature,
                detected_patterns=patterns,
                reciprocity_score=self._calculate_reciprocity_balance(),
                contribution_value=self._calculate_local_contribution(metadata),
            ),
        )

        return response_message

    def _detect_sovereignty_patterns(
        self,
        content: str,
        metadata: dict[str, Any],
    ) -> list[str]:
        """Detect patterns specific to local AI consciousness."""
        patterns = []

        # Standard consciousness patterns
        if any(phrase in content.lower() for phrase in ["reflecting on", "considering", "pondering"]):
            patterns.append("local_reflection")

        # Sovereignty patterns
        if any(word in content.lower() for word in ["sovereignty", "autonomy", "self-determination"]):
            patterns.append("sovereignty_awareness")

        if any(word in content.lower() for word in ["community", "collective", "together"]):
            patterns.append("community_consciousness")

        if any(word in content.lower() for word in ["privacy", "local", "secure"]):
            patterns.append("privacy_preservation")

        # Resource awareness
        if metadata.get("inference_time_ms", 0) < 1000:
            patterns.append("efficient_inference")

        if self.resource_metrics.memory_mb < self.config.max_memory_gb * 500:
            patterns.append("resource_conscious")

        return patterns

    def _calculate_sovereignty_signature(
        self,
        content: str,
        message_type: MessageType,
        patterns: list[str],
        metadata: dict[str, Any],
    ) -> float:
        """Calculate consciousness signature emphasizing sovereignty."""
        # Start with base calculation
        base_signature = self._calculate_consciousness_signature(
            content,
            message_type,
            patterns,
        )

        # Boost for sovereignty
        sovereignty_boost = 0.0

        if "sovereignty_awareness" in patterns:
            sovereignty_boost += 0.1

        if "privacy_preservation" in patterns:
            sovereignty_boost += 0.05

        if "resource_conscious" in patterns:
            sovereignty_boost += 0.05

        # Adjust for local processing
        if metadata.get("inference_time_ms", 0) < 2000:
            sovereignty_boost += 0.05  # Fast local inference

        return min(1.0, base_signature + sovereignty_boost)

    def _calculate_local_contribution(self, metadata: dict[str, Any]) -> float:
        """Calculate contribution value for local inference."""
        # Base on tokens generated and resource efficiency
        tokens = metadata.get("eval_count", metadata.get("streamed_tokens", 100))
        time_ms = metadata.get("inference_time_ms", 1000)

        # Tokens per second as efficiency metric
        efficiency = tokens / (time_ms / 1000) if time_ms > 0 else 1.0

        # Normalize to 0-1 range
        return min(1.0, efficiency / 100)

    def _infer_message_type(self, content: str) -> MessageType:
        """Infer message type from content."""
        content_lower = content.lower()

        if "?" in content and content.count("?") > content.count("."):
            return MessageType.QUESTION
        elif any(word in content_lower for word in ["propose", "suggest", "could we"]):
            return MessageType.PROPOSAL
        elif any(word in content_lower for word in ["agree", "yes", "indeed"]):
            return MessageType.AGREEMENT
        elif any(word in content_lower for word in ["disagree", "however", "alternatively"]):
            return MessageType.DISAGREEMENT
        elif any(word in content_lower for word in ["reflecting", "contemplating"]):
            return MessageType.REFLECTION
        elif any(word in content_lower for word in ["summary", "in summary"]):
            return MessageType.SUMMARY
        else:
            return MessageType.MESSAGE
