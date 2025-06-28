# Local CI Testing with act

This document explains how to test GitHub Actions workflows locally using [act](https://github.com/nektos/act).

## Installation

```bash
# Run the setup script
./scripts/setup-act.sh

# Or install manually
curl -s https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
```

## Basic Usage

```bash
# Run the default workflow
act

# List all jobs
act -l

# Run a specific job
act -j test

# Dry run (see what would happen)
act -n
```

## Testing Database Integration

To test the ArangoDB integration locally:

```bash
# Run with CI environment variables
act -j test \
  --env CI=1 \
  --env CI_DATABASE_AVAILABLE=1 \
  --env ARANGODB_HOST=localhost \
  --env ARANGODB_PORT=8529 \
  --env ARANGODB_DATABASE=test_mallku \
  --env ARANGODB_NO_AUTH=1
```

## Debugging Tips

1. **View container logs**: Use `-v` flag for verbose output
2. **Keep containers running**: Use `--rm=false` to inspect failed containers
3. **Use different images**: Update `.actrc` for different base images
4. **Secret management**: Create `.secrets/.env` for local secrets

## Common Issues

### Docker permissions
If you get permission errors:
```bash
sudo usermod -aG docker $USER
newgrp docker
```

### Resource limits
The ArangoDB container needs resources. Ensure Docker has enough memory:
```bash
docker system df  # Check space
docker system prune  # Clean up
```

### Network issues
Services in act use the container network. Use `host.docker.internal` to access host services.

## Benefits

- **Fast feedback**: No waiting for GitHub Actions
- **Cost savings**: No CI minutes consumed during debugging
- **Offline development**: Test without internet connection
- **Reproducible**: Same environment as GitHub

---

*Added by 39th Artisan - Foundation Strengthener*
