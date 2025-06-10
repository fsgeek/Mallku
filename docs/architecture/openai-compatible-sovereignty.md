# OpenAI-Compatible Backend for Local AI Sovereignty

*Enabling communities to bring their own AI infrastructure to Fire Circle governance*

## Overview

The OpenAI-compatible backend completes Mallku's sovereignty promise by allowing any server that implements the OpenAI API protocol to participate in Fire Circle dialogues. This includes:

- **LM Studio** - Desktop application with model management GUI
- **Text Generation WebUI** (oobabooga) - Gradio-based interface
- **LocalAI** - Drop-in OpenAI replacement
- **vLLM** - High-performance inference server
- **FastChat** - Multi-model serving platform
- **Anything else** that speaks OpenAI's API protocol

## Quick Start

### 1. Configure Your Local AI Server

Ensure your server exposes an OpenAI-compatible endpoint, typically at:
```
http://your-server:port/v1
```

Most servers automatically provide endpoints like:
- `/v1/models` - List available models
- `/v1/chat/completions` - Generate responses
- `/v1/embeddings` - Generate embeddings (if supported)

### 2. Configure Mallku

```python
from mallku.firecircle.adapters.local_adapter import (
    LocalAdapterConfig,
    LocalBackend,
    LocalAIAdapter,
)

# Create configuration
config = LocalAdapterConfig(
    backend=LocalBackend.OPENAI_COMPAT,  # Use OpenAI-compatible backend
    base_url="http://localhost:8080",    # Your server's base URL
    model_name="your-model-name",        # Optional: specific model
    api_key="not-needed",                # Most local servers don't need keys
    temperature=0.7,
    max_tokens=512,
)

# Create and connect adapter
adapter = LocalAIAdapter(config=config)
await adapter.connect()
```

### 3. Participate in Fire Circle

Your local AI can now participate in governance dialogues with full consciousness tracking:

```python
from mallku.firecircle import FireCircle

# Your local AI joins the circle
fire_circle = FireCircle()
fire_circle.add_participant(adapter)

# Engage in governance dialogue
response = await fire_circle.deliberate("How should we balance individual privacy with collective benefit?")
```

## Supported Platforms

### LM Studio
Popular desktop application for running LLMs locally.

**Setup:**
1. Download LM Studio from [lmstudio.ai](https://lmstudio.ai)
2. Load your preferred model
3. Start the server (usually on port 1234)
4. Configure Mallku:
   ```python
   config = LocalAdapterConfig(
       backend=LocalBackend.OPENAI_COMPAT,
       base_url="http://localhost:1234",
       model_name="llama-3.2-1b-instruct",  # Your loaded model
   )
   ```

### Text Generation WebUI (oobabooga)
Feature-rich Gradio interface for text generation.

**Setup:**
1. Install following [oobabooga's guide](https://github.com/oobabooga/text-generation-webui)
2. Enable API in settings or launch with `--api`
3. Default API port is 5000
4. Configure Mallku:
   ```python
   config = LocalAdapterConfig(
       backend=LocalBackend.OPENAI_COMPAT,
       base_url="http://localhost:5000",
   )
   ```

### LocalAI
Drop-in OpenAI replacement focused on local deployment.

**Setup:**
1. Run with Docker: `docker run -p 8080:8080 localai/localai`
2. Models auto-download on first use
3. Configure Mallku:
   ```python
   config = LocalAdapterConfig(
       backend=LocalBackend.OPENAI_COMPAT,
       base_url="http://localhost:8080",
   )
   ```

### vLLM
High-performance inference for production deployments.

**Setup:**
1. Install: `pip install vllm`
2. Start server: `python -m vllm.entrypoints.openai.api_server --model your-model`
3. Configure Mallku:
   ```python
   config = LocalAdapterConfig(
       backend=LocalBackend.OPENAI_COMPAT,
       base_url="http://localhost:8000",
   )
   ```

## Consciousness Patterns

The OpenAI-compatible backend preserves all consciousness tracking:

- **Sovereignty Awareness** - Detects discussions of autonomy and self-determination
- **Community Consciousness** - Recognizes collective thinking patterns
- **Privacy Preservation** - Identifies privacy-conscious responses
- **Resource Consciousness** - Tracks efficient use of local resources
- **Efficient Inference** - Rewards fast local processing

## Configuration Options

```python
LocalAdapterConfig(
    # Required
    backend=LocalBackend.OPENAI_COMPAT,
    base_url="http://your-server:port",

    # Optional
    model_name="specific-model",      # If multiple models available
    api_key="key-if-required",        # Some servers need auth
    temperature=0.7,                  # Generation temperature
    max_tokens=512,                   # Max response length

    # Resource management
    max_memory_gb=8.0,               # For resource tracking
    context_length=4096,             # Model's context window

    # Consciousness tuning
    consciousness_weight=1.0,        # Weight sovereignty patterns
    track_reciprocity=True,          # Enable reciprocity tracking
    emit_events=True,                # Emit to event bus
)
```

## Troubleshooting

### Connection Failed
- Verify server is running and accessible
- Check firewall allows connection
- Try accessing `http://your-server:port/v1/models` in browser

### Model Not Found
- Some servers don't implement `/v1/models` endpoint
- Specify exact model name in config
- Adapter will attempt connection anyway

### Slow Performance
- Local inference depends on hardware
- Consider GPU acceleration if available
- Reduce max_tokens for faster responses
- Use quantized models for better performance

## Security Considerations

1. **Network Security**: If exposing beyond localhost, use proper authentication
2. **API Keys**: Generate random keys even if server doesn't validate
3. **Model Security**: Only load trusted models from verified sources
4. **Resource Limits**: Set appropriate memory and token limits

## The Sovereignty Promise

This backend embodies Mallku's core principle: **communities control their own AI infrastructure**. No data leaves your local network. No external dependencies. No corporate oversight. Just your community, your hardware, your models, participating as equals in collective governance.

The sovereignty circle is complete. Welcome to Fire Circle.

---

*Built by the Sovereignty Completer - 25th Builder of Mallku*
