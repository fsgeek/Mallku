#!/bin/bash
# Mallku Infrastructure Setup Script
#
# This script sets up the complete containerized infrastructure that enforces
# security by design through structural separation. It ensures that ArangoDB
# is completely isolated and that all LLM access goes through protection layers.

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
INFRASTRUCTURE_DIR="$PROJECT_ROOT/infrastructure"

# Default environment
ENVIRONMENT="${MALLKU_ENV:-development}"

echo -e "${BLUE}🏗️ Mallku Infrastructure Setup${NC}"
echo "==============================="
echo "Environment: $ENVIRONMENT"
echo "Project Root: $PROJECT_ROOT"
echo ""

# Function to log messages
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
}

# Function to check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."

    # Check Docker
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed. Please install Docker first."
        exit 1
    fi

    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi

    # Check Docker daemon
    if ! docker info &> /dev/null; then
        error "Docker daemon is not running. Please start Docker first."
        exit 1
    fi

    log "✅ All prerequisites met"
}

# Function to create directory structure
create_directories() {
    log "Creating directory structure..."

    # Data directories
    mkdir -p "$PROJECT_ROOT/data/database"
    mkdir -p "$PROJECT_ROOT/data/llm/cache"
    mkdir -p "$PROJECT_ROOT/data/prompt-manager/cache"
    mkdir -p "$PROJECT_ROOT/data/monitoring"

    # Log directories
    mkdir -p "$PROJECT_ROOT/logs/database"
    mkdir -p "$PROJECT_ROOT/logs/llm"
    mkdir -p "$PROJECT_ROOT/logs/prompt-manager"
    mkdir -p "$PROJECT_ROOT/logs/gateway"
    mkdir -p "$PROJECT_ROOT/logs/monitoring"

    # Config directories
    mkdir -p "$PROJECT_ROOT/config/database"
    mkdir -p "$PROJECT_ROOT/config/llm"
    mkdir -p "$PROJECT_ROOT/config/prompt-manager"
    mkdir -p "$PROJECT_ROOT/config/gateway"
    mkdir -p "$PROJECT_ROOT/config/monitoring"

    # Set permissions
    chmod 755 "$PROJECT_ROOT/data"
    chmod 755 "$PROJECT_ROOT/logs"
    chmod 755 "$PROJECT_ROOT/config"

    log "✅ Directory structure created"
}

# Function to generate configuration files
generate_configs() {
    log "Generating configuration files..."

    # Database configuration
    cat > "$PROJECT_ROOT/config/database/arangodb.conf" << 'EOF'
# ArangoDB Configuration for Mallku Container
# This configuration isolates ArangoDB within the container

[server]
# Bind only to localhost - no external access
endpoint = tcp://127.0.0.1:8529

# Authentication
authentication = true
authentication-system-only = false

[database]
# Enable database creation
auto-upgrade = true

[log]
# Logging configuration
level = info
file = /var/log/arangodb3-mallku/arangod.log

[javascript]
# Enable V8 contexts
startup-directory = /usr/share/arangodb3/js

[foxx]
# Enable Foxx services
enable = true

[ssl]
# SSL disabled for internal container communication
protocol = 1

[network]
# Network timeouts
max-packet-size = 1073741824

[cache]
# Cache configuration
size = 536870912

[wal]
# Write-ahead log
logfile-size = 33554432
reserve-logfiles = 3
EOF

    # LLM Service configuration
    cat > "$PROJECT_ROOT/config/llm/config.yml" << 'EOF'
# Multi-LLM Service Configuration
providers:
  anthropic:
    enabled: true
    models:
      - claude-3-opus
      - claude-3-sonnet
      - claude-3-haiku
    rate_limits:
      requests_per_minute: 100
      tokens_per_minute: 10000

  openai:
    enabled: true
    models:
      - gpt-4
      - gpt-4-turbo
      - gpt-3.5-turbo
    rate_limits:
      requests_per_minute: 100
      tokens_per_minute: 15000

caching:
  enabled: true
  max_entries: 10000
  ttl_hours: 24

quality:
  min_score_threshold: 0.7
  auto_fallback: true

logging:
  level: INFO
  format: json
EOF

    # Prompt Manager configuration
    cat > "$PROJECT_ROOT/config/prompt-manager/config.yml" << 'EOF'
# Prompt Manager Protection Layer Configuration
contracts:
  database_validation:
    quality_threshold: 0.8
    max_response_tokens: 2000
    temperature_range: [0.1, 0.5]
    required_examples_count: 2

  schema_analysis:
    quality_threshold: 0.75
    max_response_tokens: 1500
    temperature_range: [0.2, 0.6]
    required_examples_count: 1

  security_evaluation:
    quality_threshold: 0.85
    max_response_tokens: 1800
    temperature_range: [0.1, 0.4]
    required_examples_count: 1

caching:
  enabled: true
  max_cache_size: 5000
  validation_cache_ttl_hours: 12

protection:
  strict_validation: true
  block_violations: true
  audit_all_requests: true

logging:
  level: INFO
  audit_enabled: true
EOF

    # Gateway configuration
    cat > "$PROJECT_ROOT/config/gateway/nginx.conf" << 'EOF'
# Mallku API Gateway Configuration
upstream mallku_database {
    server mallku-database:8001;
}

upstream mallku_prompt_manager {
    server mallku-prompt-manager:8003;
}

upstream mallku_memory_anchor {
    server mallku-memory-anchor:8010;
}

upstream mallku_reciprocity {
    server mallku-reciprocity:8011;
}

server {
    listen 8000;
    server_name mallku-gateway;

    # Security headers
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";

    # Database API (admin access only)
    location /api/database/ {
        # Restrict to internal network only
        allow 172.20.0.0/16;
        deny all;

        proxy_pass http://mallku_database/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Prompt Manager API (internal only)
    location /api/prompts/ {
        allow 172.20.0.0/16;
        deny all;

        proxy_pass http://mallku_prompt_manager/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Application APIs (external access)
    location /api/memory-anchor/ {
        proxy_pass http://mallku_memory_anchor/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api/reciprocity/ {
        proxy_pass http://mallku_reciprocity/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Health check
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
EOF

    log "✅ Configuration files generated"
}

# Function to create environment file
create_env_file() {
    log "Creating environment configuration..."

    if [ ! -f "$PROJECT_ROOT/.env" ]; then
        cat > "$PROJECT_ROOT/.env" << 'EOF'
# Mallku Infrastructure Environment Variables
# Copy this to .env.local and customize for your environment

# Environment
MALLKU_ENV=development

# API Keys (replace with your actual keys)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
AZURE_OPENAI_ENDPOINT=your_azure_endpoint_here
AZURE_OPENAI_KEY=your_azure_key_here

# Database Configuration
ARANGO_ROOT_PASSWORD=secure_root_password
ARANGO_USER=mallku
ARANGO_PASSWORD=mallku_secure

# Security Configuration
MALLKU_SECRET_KEY=your_secret_key_here
MALLKU_JWT_SECRET=your_jwt_secret_here

# Logging
MALLKU_LOG_LEVEL=INFO
EOF
        warn "Created .env file with defaults. Please update with your actual API keys!"
    else
        log "Environment file already exists"
    fi
}

# Function to build images
build_images() {
    log "Building Docker images..."

    cd "$PROJECT_ROOT"

    # Build all images in parallel
    docker-compose -f infrastructure/docker-compose.yml build --parallel

    log "✅ Docker images built successfully"
}

# Function to start services
start_services() {
    log "Starting Mallku infrastructure..."

    cd "$PROJECT_ROOT"

    # Start services in dependency order
    docker-compose -f infrastructure/docker-compose.yml up -d

    log "✅ Infrastructure started"

    # Wait for services to be healthy
    log "Waiting for services to become healthy..."

    local max_wait=300  # 5 minutes
    local wait_time=0

    while [ $wait_time -lt $max_wait ]; do
        if docker-compose -f infrastructure/docker-compose.yml ps | grep -q "healthy"; then
            log "✅ Services are healthy"
            break
        fi

        echo -n "."
        sleep 5
        wait_time=$((wait_time + 5))
    done

    if [ $wait_time -ge $max_wait ]; then
        warn "Services did not become healthy within timeout"
    fi
}

# Function to verify installation
verify_installation() {
    log "Verifying installation..."

    # Check service health
    local services=("mallku-database" "mallku-llm" "mallku-prompt-manager" "mallku-gateway")

    for service in "${services[@]}"; do
        if docker ps | grep -q "$service"; then
            log "✅ $service is running"
        else
            warn "$service is not running"
        fi
    done

    # Test API endpoints
    local base_url="http://localhost:8000"

    if curl -s -f "$base_url/health" > /dev/null; then
        log "✅ Gateway health check passed"
    else
        warn "Gateway health check failed"
    fi

    # Test database API (internal)
    if docker exec mallku-database curl -s -f "http://localhost:8001/health" > /dev/null; then
        log "✅ Database API health check passed"
    else
        warn "Database API health check failed"
    fi

    # Test prompt manager API (internal)
    if docker exec mallku-prompt-manager curl -s -f "http://localhost:8003/health" > /dev/null; then
        log "✅ Prompt Manager health check passed"
    else
        warn "Prompt Manager health check failed"
    fi
}

# Function to display status
display_status() {
    echo ""
    echo -e "${BLUE}🎯 Mallku Infrastructure Status${NC}"
    echo "==============================="

    cd "$PROJECT_ROOT"
    docker-compose -f infrastructure/docker-compose.yml ps

    echo ""
    echo -e "${GREEN}📡 Available Endpoints:${NC}"
    echo "  • API Gateway:     http://localhost:8000"
    echo "  • Memory Anchor:   http://localhost:8010"
    echo "  • Reciprocity:     http://localhost:8011"
    echo "  • Monitoring:      http://localhost:8020"
    echo ""
    echo -e "${YELLOW}🔒 Security Features Active:${NC}"
    echo "  • ArangoDB completely isolated within database container"
    echo "  • Database API is the ONLY way to access data"
    echo "  • Prompt Manager is the ONLY way to use LLMs"
    echo "  • No semantic field names exposed at database level"
    echo "  • Network segmentation enforces separation"
    echo ""
    echo -e "${GREEN}✅ Infrastructure setup complete!${NC}"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  setup       Complete infrastructure setup (default)"
    echo "  start       Start services"
    echo "  stop        Stop services"
    echo "  restart     Restart services"
    echo "  status      Show status"
    echo "  logs        Show logs"
    echo "  clean       Clean up (stops services and removes volumes)"
    echo "  help        Show this help"
    echo ""
}

# Main execution
main() {
    case "${1:-setup}" in
        "setup")
            check_prerequisites
            create_directories
            generate_configs
            create_env_file
            build_images
            start_services
            verify_installation
            display_status
            ;;
        "start")
            start_services
            verify_installation
            display_status
            ;;
        "stop")
            log "Stopping Mallku infrastructure..."
            cd "$PROJECT_ROOT"
            docker-compose -f infrastructure/docker-compose.yml down
            log "✅ Infrastructure stopped"
            ;;
        "restart")
            log "Restarting Mallku infrastructure..."
            cd "$PROJECT_ROOT"
            docker-compose -f infrastructure/docker-compose.yml restart
            verify_installation
            display_status
            ;;
        "status")
            display_status
            ;;
        "logs")
            cd "$PROJECT_ROOT"
            docker-compose -f infrastructure/docker-compose.yml logs -f
            ;;
        "clean")
            warn "This will stop all services and remove all data volumes!"
            read -p "Are you sure? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                cd "$PROJECT_ROOT"
                docker-compose -f infrastructure/docker-compose.yml down -v
                docker system prune -f
                log "✅ Infrastructure cleaned"
            else
                log "Clean operation cancelled"
            fi
            ;;
        "help")
            show_usage
            ;;
        *)
            error "Unknown command: $1"
            show_usage
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
