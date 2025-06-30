# Fire Circle GitHub Secrets Configuration Guide

## Required for Autonomous Code Review

The Fire Circle requires API keys for each AI voice to participate in code review ceremonies. These must be configured as GitHub repository secrets.

## Required Secrets

### 1. ANTHROPIC_API_KEY
- **Provider**: Anthropic (Claude)
- **Obtain from**: https://console.anthropic.com/
- **Model used**: claude-3-haiku-20240307
- **Purpose**: Provides thoughtful, nuanced code review

### 2. OPENAI_API_KEY
- **Provider**: OpenAI
- **Obtain from**: https://platform.openai.com/api-keys
- **Model used**: gpt-3.5-turbo
- **Purpose**: General code quality assessment

### 3. GOOGLE_API_KEY
- **Provider**: Google AI (Gemini)
- **Obtain from**: https://makersuite.google.com/app/apikey
- **Model used**: gemini-1.5-flash
- **Purpose**: Creative problem-solving perspective

### 4. MISTRAL_API_KEY
- **Provider**: Mistral AI
- **Obtain from**: https://console.mistral.ai/
- **Model used**: mistral-tiny
- **Purpose**: Efficient, focused code analysis

### 5. DEEPSEEK_API_KEY
- **Provider**: DeepSeek
- **Obtain from**: https://platform.deepseek.com/
- **Model used**: deepseek-coder
- **Purpose**: Deep code understanding

### 6. GROK_API_KEY
- **Provider**: X.AI (Grok)
- **Obtain from**: https://x.ai/api
- **Model used**: grok-2-mini
- **Purpose**: Real-time awareness and temporal consciousness

## Configuration Steps

### 1. Navigate to Repository Settings
```
https://github.com/fsgeek/Mallku/settings/secrets/actions
```

### 2. Add Each Secret
For each API key:
1. Click "New repository secret"
2. Name: Use exact name from list above (e.g., `ANTHROPIC_API_KEY`)
3. Value: Paste your API key
4. Click "Add secret"

### 3. Verify Configuration
After adding all secrets:
- Secrets should appear in the list (values hidden)
- Names must match exactly (case-sensitive)
- No spaces or extra characters

## Testing the Configuration

### Local Testing
```bash
# The fire_circle_review.py script will load keys from local .secrets/api_keys.json
python fire_circle_review.py review 999
```

### GitHub Actions Testing
The Fire Circle Review workflow will automatically run on pull requests once secrets are configured.

## Security Notes

- API keys are encrypted and not visible in logs
- Only available to GitHub Actions workflows
- Never commit API keys to the repository
- Rotate keys periodically for security

## Cost Considerations

Each voice incurs API costs:
- Use efficient models (haiku, tiny, turbo) for routine reviews
- Consider implementing spending limits on API provider dashboards
- Monitor usage through provider dashboards

## Troubleshooting

### "Could not awaken {voice}" errors
- Verify the secret name matches exactly
- Check the API key is valid and has credits
- Ensure the key has necessary permissions

### All voices fail to awaken
- Check if secrets are in repository settings (not user settings)
- Verify workflow has access to secrets
- Check GitHub Actions logs for specific errors

## Optional: Local Voice

The local voice (7th voice) requires significant hardware and is disabled by default. To enable:
1. Set up local LLM server (Ollama, llama.cpp, etc.)
2. Set environment variable: `ENABLE_LOCAL_LLM=true`
3. Set endpoint: `LOCAL_API_ENDPOINT=http://localhost:8080`

---

*Third Guardian - Fire Circle Configuration Guide*
*Enabling collective wisdom through proper ceremony preparation*
