# Fire Circle Troubleshooting Guide
## Third Guardian - Operational Wisdom

### Common Issues and Solutions

#### 1. Database Connection Timeouts

**Symptom**: `ERROR:root:Database not ready after 60 seconds`

**Cause**: Fire Circle doesn't need database access but tries to connect by default

**Solution**: Set environment variables in workflow:
```yaml
env:
  MALLKU_NO_DATABASE: "true"
  CI_DATABASE_AVAILABLE: "0"
```

#### 2. Missing Adapter Configurations

**Symptom**:
- `Configuration missing required attribute: 'enable_search_grounding'`
- `Configuration missing required attribute: 'multilingual_mode'`

**Cause**: Some adapters require specific configuration parameters

**Solution**: Use VoiceConfig.config_overrides:
```python
config_overrides = {}
if provider == "google":
    config_overrides = {"enable_search_grounding": False}
elif provider == "mistral":
    config_overrides = {"multilingual_mode": True}

voice_configs.append(
    VoiceConfig(
        provider=provider,
        model=model,
        role=f"{provider.title()} Voice",
        config_overrides=config_overrides
    )
)
```

#### 3. Missing xai-sdk Package

**Symptom**: `xai-sdk not available. Install with: pip install xai-sdk`

**Cause**: Grok adapter requires xai-sdk package

**Solution**: Add to requirements.txt:
```
xai-sdk>=0.0.8
```

#### 4. XAI_API_KEY vs GROK_API_KEY

**Symptom**: Grok voice doesn't awaken despite having API key

**Cause**: Key might be stored as XAI_API_KEY instead of GROK_API_KEY

**Solution**: Check both environment variables:
```python
if provider == "grok":
    api_key = os.getenv("GROK_API_KEY") or os.getenv("XAI_API_KEY")
```

#### 5. Missing API Keys

**Symptom**: `Could not awaken {voice}: Failed to connect`

**Cause**: API key not configured in GitHub secrets

**Solution**:
1. Go to repository Settings → Secrets → Actions
2. Add the missing API key (e.g., OPENAI_API_KEY)
3. Ensure name matches exactly (case-sensitive)

### Verification Steps

1. **Check which voices are available**:
   Look in workflow logs for "✓ Awakened {voice} voice" messages

2. **Verify API keys are loaded**:
   The workflow should show "Loaded X API keys from secrets"

3. **Monitor review progress**:
   Fire Circle reviews can take 2-5 minutes depending on PR size

4. **Check for timeout**:
   If workflow runs >10 minutes, it may be stuck

### Emergency Recovery

If Fire Circle gets stuck:
1. Cancel the workflow run
2. Check logs for specific errors
3. Apply fixes from this guide
4. Re-trigger the review manually

### Sacred Debugging Philosophy

Remember: errors are teachers. Each failure reveals:
- Hidden assumptions in our code
- Opportunities for resilience
- Paths to greater robustness

The Fire Circle's struggles teach us about:
- Distributed system complexity
- Configuration management
- Graceful degradation

---

*Third Guardian - Troubleshooting Guide*
*"In failure, wisdom. In debugging, enlightenment."*
