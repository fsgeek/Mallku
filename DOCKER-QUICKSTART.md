# Docker Quick Start Guide

This guide helps you start Mallku's cathedral architecture quickly.

## Prerequisites

- Docker and Docker Compose installed
- Git for cloning the repository
- Basic command line familiarity

## Quick Start

```bash
# Clone and enter Mallku
git clone https://github.com/fsgeek/Mallku.git
cd Mallku

# Make scripts executable
chmod +x start-mallku.sh
chmod +x scripts/mallku-docker.sh

# Start the cathedral
./start-mallku.sh
```

If successful, you'll see:
```
✅ Mallku is running!
🔗 API Gateway: http://localhost:8080/health
🔒 Security: http://localhost:8080/security/metrics
```

## Architecture Overview

```
Your Machine (Host)
│
├── Port 8080 ──→ API Gateway Container
│                 (Only exposed port)
│
└── Docker Networks:
    ├── mallku-external (API can reach host)
    └── mallku-internal (isolated network)
        └── Database Container
            (No exposed ports)
```

**Key Security**: The database has NO exposed ports. It can only be reached through the API gateway.

## Common Operations

### Start Services
```bash
./scripts/mallku-docker.sh start
# Or with rebuild:
./scripts/mallku-docker.sh start --build
```

### Stop Services
```bash
./scripts/mallku-docker.sh stop
```

### View Logs
```bash
# All logs
./scripts/mallku-docker.sh logs

# Just API logs
./scripts/mallku-docker.sh logs api

# Just database logs
./scripts/mallku-docker.sh logs database
```

### Check Status
```bash
./scripts/mallku-docker.sh status
```

### Reset Database (Careful!)
```bash
# This destroys all data and starts fresh
./scripts/mallku-docker.sh reset
```

## Testing the Architecture

Verify cathedral security:

```bash
# ✅ This works (API gateway)
curl http://localhost:8080/health

# ❌ This fails (database not exposed)
curl http://localhost:8529

# See security metrics
curl http://localhost:8080/security/metrics
```

## Troubleshooting

### Services won't start
```bash
# Check if ports are in use
lsof -i :8080

# View detailed logs
cd docker/
docker-compose logs
```

### Reset everything
```bash
# Stop services and remove all data
./scripts/mallku-docker.sh stop
docker volume rm docker_mallku_data docker_mallku_apps_data
./scripts/mallku-docker.sh start
```

### Access container directly (debugging only)
```bash
# API container
./scripts/mallku-docker.sh shell api

# Database (breaks cathedral security - debugging only)
./scripts/mallku-docker.sh shell database
```

## Next Steps

- Read about [Cathedral Architecture](docs/architecture/docker-cathedral-architecture.md)
- Explore the [API endpoints](#)
- Understand the [Ayni philosophy](README.md)

---

*Remember: We build cathedrals, not tents. Each action should strengthen the structure.*
