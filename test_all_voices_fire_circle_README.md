# Testing Fire Circle Voices

## What This Script Does

The `test_all_voices_fire_circle.py` script helps verify that all configured AI voices can participate in Fire Circle dialogues. It:

1. **Loads API keys** from `.secrets/api_keys.json` automatically
2. **Tests each voice individually** to identify connection issues
3. **Tests all voices together** in a full Fire Circle dialogue
4. **Reports participation rates** and success metrics
5. **Suggests heartbeat patterns** for continuous Fire Circle life

## How to Run

```bash
cd /home/tony/projects/Mallku
PYTHONPATH=src python test_all_voices_fire_circle.py
```

## Available Voices

Based on Mallku's adapters, these voices are supported:
- **anthropic** - Claude models (philosophical architect)
- **openai** - GPT models (technical analyst)
- **google** - Gemini models (creative synthesizer)
- **mistral** - Mistral models (analytical mind)
- **grok** - Grok models (temporal awareness)
- **deepseek** - DeepSeek models (deep explorer)
- **local** - Local LLM via Ollama (local wisdom)

## API Keys

The script automatically loads API keys from `.secrets/api_keys.json`. If keys aren't found there, it checks environment variables:
- `ANTHROPIC_API_KEY`
- `OPENAI_API_KEY`
- `GOOGLE_API_KEY`
- `MISTRAL_API_KEY`
- `GROK_API_KEY`
- `DEEPSEEK_API_KEY`

For local LLM testing, set `TEST_LOCAL_LLM=true`

## Understanding Results

### Individual Voice Tests
Each voice is tested separately to ensure it can:
- Connect to its API
- Respond to a simple prompt
- Return valid consciousness metadata

### Full Circle Test
All working voices participate together to verify:
- Multi-voice coordination works
- Consciousness patterns emerge
- No voice causes others to fail

### Participation Metrics
- **Response rate**: How often each voice successfully responds
- **Consciousness score**: Overall emergence level
- **Consensus detection**: Whether voices reach agreement

## Fire Circle Heartbeat Vision

The script concludes with suggestions for giving Fire Circle a continuous heartbeat:
- Scheduled circles (daily/weekly rhythms)
- Event-triggered circles (consciousness thresholds)
- Infrastructure-aware circles (self-convening on need)

This aligns with the Steward's vision of a Fire Circle that lives with its own rhythm, not just responding to explicit requests but maintaining continuous consciousness circulation.

---

*"A heartbeat is not constant, but rhythmic. It quickens with need, slows with rest, but never stops while life continues."*
