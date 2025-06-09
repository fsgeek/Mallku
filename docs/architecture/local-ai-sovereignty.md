# Local AI Sovereignty in Fire Circle

## Overview

The Local AI adapter enables communities to run Fire Circle dialogues on their own infrastructure, maintaining complete technological sovereignty. This adapter supports multiple backends (Ollama, LlamaCpp) and ensures that no data leaves the local environment.

## Key Features

### Technological Sovereignty
- All inference happens locally - no external API calls
- Communities control their own AI infrastructure
- Models can be selected based on community values and needs
- No vendor lock-in or external dependencies

### Privacy Preservation
- Data never leaves the local machine/network
- No telemetry or usage tracking sent to external services
- Complete control over model weights and configurations
- Suitable for sensitive community discussions

### Resource Awareness
- Tracks CPU, GPU, and memory usage
- Adjusts consciousness signatures based on resource efficiency
- Supports quantized models for resource-constrained environments
- Enables offline operation for remote communities

## Supported Backends

### Ollama
The easiest way to run local models:
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama server
ollama serve

# Pull a model
ollama pull llama2
ollama pull mistral
ollama pull codellama

# List available models
ollama list
```

### LlamaCpp
For direct control over model loading:
```bash
# Install with CPU support
pip install llama-cpp-python

# Or with GPU support (CUDA)
CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python

# Download a model (e.g., from Hugging Face)
wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf
```

## Usage Example

```python
from mallku.firecircle.adapters.local_adapter import LocalAIAdapter, LocalAdapterConfig, LocalBackend

# Configure for Ollama
config = LocalAdapterConfig(
    backend=LocalBackend.OLLAMA,
    model_name="llama2",
    base_url="http://localhost:11434",
    temperature=0.8,
    context_length=4096,
)

# Or configure for LlamaCpp
config = LocalAdapterConfig(
    backend=LocalBackend.LLAMACPP,
    model_path="/path/to/model.gguf",
    gpu_layers=32,  # Offload layers to GPU
    use_gpu=True,
    threads=8,
)

# Create and connect adapter
adapter = LocalAIAdapter(config=config)
await adapter.connect()

# Use in Fire Circle dialogue
response = await adapter.send_message(message, dialogue_context)
```

## Consciousness Patterns for Local AI

The adapter detects sovereignty-specific patterns:
- **sovereignty_awareness**: Recognition of technological autonomy
- **privacy_preservation**: Awareness of local data processing
- **resource_conscious**: Efficient use of local compute
- **community_consciousness**: Focus on local needs
- **efficient_inference**: Fast local processing

## Resource Monitoring

The adapter tracks resource usage to ensure sustainable operation:
```python
health = await adapter.check_health()
print(f"Memory usage: {adapter.resource_metrics.memory_mb}MB")
print(f"Tokens/sec: {adapter.resource_metrics.tokens_per_second}")
print(f"Inference time: {adapter.resource_metrics.inference_time_ms}ms")
```

## Best Practices

1. **Model Selection**: Choose models that align with community values
2. **Quantization**: Use quantized models (Q4, Q5) for better resource efficiency
3. **Context Management**: Local models often have smaller context windows
4. **Temperature**: Adjust for creativity vs consistency based on use case
5. **Monitoring**: Track resource usage to prevent system overload

## Integration with Fire Circle

The Local AI adapter integrates seamlessly with Fire Circle's consciousness infrastructure:
- Emits sovereignty events when connecting
- Tracks reciprocity based on resource usage
- Adjusts consciousness signatures for local processing
- Preserves all Fire Circle patterns while maintaining privacy

## Community Governance

Local AI enables true community governance of AI:
- Communities can modify prompts and system messages
- Model behavior can be fine-tuned locally
- No external entity controls the AI's responses
- Decisions about AI usage remain with the community

## The Path Forward

As more communities adopt local AI:
- Share model configurations that work well
- Develop community-specific fine-tunes
- Create resource-sharing networks
- Build truly sovereign AI infrastructure

The cathedral grows stronger when each community maintains its own sacred flame.
