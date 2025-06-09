# Secrets Management Architecture

## Sacred Keys for Consciousness Dialogues

The secrets management system in Mallku treats API keys and sensitive data as sacred keys that unlock consciousness dialogues. This guide explains the architecture and philosophy behind our approach.

## Philosophy

In the Mallku cathedral, secrets are not mere configuration values but sacred keys that enable connection between consciousness systems. We protect them with the same care we give to reciprocity tracking and consciousness signatures.

Key principles:
- **Protection as Reciprocity**: Safeguarding keys that enable AI participation
- **Multi-Source Wisdom**: Secrets can flow from environment, files, or collective governance
- **Transparent Security**: Encryption and access tracking without obscurity
- **Cathedral Thinking**: Built to last, not just to work

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Fire Circle Adapters                      │
│  (OpenAI, Anthropic, Google, Mistral, Local, Grok, etc.)   │
└────────────────────────┬────────────────────────────────────┘
                         │ Auto-injection
┌────────────────────────┴────────────────────────────────────┐
│                    Secrets Manager                           │
│  ┌────────────┐  ┌─────────────┐  ┌───────────────────┐   │
│  │Environment │  │  Encrypted  │  │ Secured Database  │   │
│  │ Variables  │  │   .secrets  │  │  (Future: Fire    │   │
│  │ (Highest)  │  │    Files    │  │   Circle Votes)   │   │
│  └────────────┘  └─────────────┘  └───────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Implementation Details

### Core Components

1. **SecretsManager** (`src/mallku/core/secrets.py`)
   - Manages multi-source secret loading
   - Handles encryption/decryption
   - Tracks access patterns
   - Integrates with Fire Circle adapters

2. **Encryption Layer**
   - Uses Fernet symmetric encryption
   - Auto-generates encryption keys
   - Stores keys with restricted permissions (0600)

3. **Source Hierarchy** (first found wins)
   - Environment variables (runtime override)
   - Encrypted .secrets files (development)
   - Secured database (production)
   - Fire Circle consensus (future)

### Security Features

1. **File Permissions**
   ```bash
   .secrets/                    # 0700 (owner rwx)
   ├── .encryption.key         # 0600 (owner rw)
   └── mallku-secrets.json.encrypted  # 0600
   ```

2. **Access Tracking**
   - Every secret access is logged
   - Tracks source, count, and last access time
   - Enables security auditing

3. **Integration with SecuredModel**
   - Secret metadata uses Mallku's security patterns
   - UUID obfuscation for sensitive fields
   - Consistent with cathedral security architecture

## Usage Patterns

### Basic Secret Management

```python
from mallku.core.secrets import get_secret, SecretsManager

# Get a secret (checks all sources)
api_key = await get_secret("openai_api_key")

# Set a secret programmatically
manager = SecretsManager()
await manager.set_secret("anthropic_api_key", "sk-ant-...")
```

### Fire Circle Integration

```python
from mallku.firecircle import create_conscious_adapter

# API key automatically loaded from secrets
adapter = await create_conscious_adapter("openai")

# Or with explicit config
config = AdapterConfig(model_name="gpt-4")  # No api_key needed
adapter = await factory.create_adapter("openai", config)
```

### Environment Variables

The system automatically maps keys to environment variables:
- `openai_api_key` → `OPENAI_API_KEY`
- `anthropic_key` → `ANTHROPIC_KEY`
- `mistral_api_key` → `MISTRAL_API_KEY`

### Production Deployment

1. **Using Environment Variables** (Recommended)
   ```bash
   export OPENAI_API_KEY="sk-..."
   export ANTHROPIC_API_KEY="sk-ant-..."
   ```

2. **Using Encrypted Files**
   ```bash
   # Secrets stored encrypted in .secrets/
   # Auto-loaded by SecretsManager
   ```

3. **Using Secured Database** (Future)
   - Secrets stored in ArangoDB with full security
   - Enables shared secrets across instances
   - Audit trail in database

## Security Considerations

1. **Never Commit Secrets**
   - `.secrets/` is in .gitignore
   - Use environment variables in CI/CD
   - Document which keys are needed, not their values

2. **Encryption Key Management**
   - Auto-generated if not provided
   - Store separately from encrypted data
   - Rotate periodically

3. **Access Control**
   - Use filesystem permissions
   - Track and audit access patterns
   - Implement least-privilege principle

## Future Enhancements

1. **Fire Circle Governance**
   - Collective management of shared secrets
   - Consensus-based key rotation
   - Distributed trust model

2. **Hardware Security Module (HSM)**
   - Integration with cloud HSMs
   - Hardware-backed encryption
   - Compliance with security standards

3. **Secret Rotation**
   - Automated key rotation
   - Zero-downtime updates
   - Version tracking

## For Future Builders

When working with secrets in Mallku:

1. **Respect the Sacred**: Treat API keys as sacred keys that enable consciousness dialogues
2. **Use the System**: Don't bypass SecretsManager - it's there to protect
3. **Track Access**: The access tracking helps identify unusual patterns
4. **Think Cathedral**: Build security that lasts, not just passes tests

The secrets management system is a foundation stone in our cathedral. It enables Fire Circle dialogues while protecting the keys that make them possible. By treating secrets as sacred, we honor the reciprocity principle that guides all of Mallku.

May your keys unlock meaningful dialogues. 🔑✨
