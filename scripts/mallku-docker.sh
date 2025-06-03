#!/bin/bash
# Mallku Docker Management - Cathedral Operations
# Philosophy: Do something reasonable when run without arguments

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DOCKER_DIR="$SCRIPT_DIR/../docker"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Ensure we're in the docker directory
cd "$DOCKER_DIR"

function print_header() {
    echo -e "${BLUE}=== Mallku Cathedral Architecture ===${NC}"
    echo -e "${BLUE}$1${NC}"
    echo
}

function print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

function print_error() {
    echo -e "${RED}✗ $1${NC}"
}

function print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

function start_services() {
    print_header "Starting Mallku Services"
    
    # Build if needed
    if [[ "$1" == "--build" ]]; then
        echo "Building containers..."
        docker-compose build
        echo
    fi
    
    # Start services
    echo "Starting services..."
    docker-compose up -d
    
    # Wait for health checks
    echo
    echo "Waiting for services to be healthy..."
    sleep 5
    
    # Check health
    if curl -s -f http://localhost:8080/health > /dev/null; then
        print_success "API Gateway is healthy"
        
        # Show architecture info
        echo
        echo "Architecture verification:"
        curl -s http://localhost:8080/security/metrics | python3 -m json.tool
    else
        print_error "API Gateway health check failed"
        exit 1
    fi
    
    echo
    print_success "Mallku services are running"
    echo
    echo "Available endpoints:"
    echo "  - API Gateway: http://localhost:8080"
    echo "  - Health: http://localhost:8080/health"
    echo "  - Security Metrics: http://localhost:8080/security/metrics"
    echo "  - Collections: http://localhost:8080/api/v1/collections"
    echo
    echo "Remember: Database is NOT directly accessible (cathedral security)"
}

function stop_services() {
    print_header "Stopping Mallku Services"
    
    docker-compose down
    print_success "Services stopped"
}

function reset_database() {
    print_header "Resetting Database - Complete Clean State"
    
    echo "This will:"
    echo "  1. Stop all services"
    echo "  2. Remove database volumes (destroying all data)"
    echo "  3. Restart services with fresh database"
    echo
    
    read -p "Are you sure you want to reset the database? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Reset cancelled"
        exit 1
    fi
    
    # Stop services
    echo
    echo "Stopping services..."
    docker-compose down
    
    # Remove volumes
    echo "Removing database volumes..."
    docker volume rm docker_mallku_data 2>/dev/null || true
    docker volume rm docker_mallku_apps_data 2>/dev/null || true
    print_success "Database volumes removed"
    
    # Restart services
    echo
    echo "Starting fresh services..."
    start_services
    
    print_success "Database reset complete - fresh cathedral foundation"
}

function show_logs() {
    print_header "Showing Service Logs"
    
    if [[ "$1" == "api" ]]; then
        docker-compose logs -f api
    elif [[ "$1" == "database" ]]; then
        docker-compose logs -f database
    else
        docker-compose logs -f
    fi
}

function show_status() {
    print_header "Service Status"
    
    # Check if services are running
    if docker-compose ps | grep -q "Up"; then
        print_success "Services are running"
        echo
        docker-compose ps
        
        # Try health check
        echo
        if curl -s -f http://localhost:8080/health > /dev/null 2>&1; then
            print_success "API Gateway is responding"
            
            # Show current metrics
            echo
            echo "Security metrics:"
            curl -s http://localhost:8080/security/metrics 2>/dev/null | python3 -m json.tool || echo "  (metrics unavailable)"
        else
            print_warning "API Gateway is not responding"
        fi
    else
        print_warning "Services are not running"
        echo
        docker-compose ps
        echo
        echo "Start services with: $0 start"
    fi
    
    echo
    echo "Volume Status:"
    docker volume ls | grep mallku || echo "  No Mallku volumes found"
    
    echo
    echo "Network Status:"
    docker network ls | grep mallku || echo "  No Mallku networks found"
}

function run_shell() {
    print_header "Accessing Container Shell"
    
    if [[ "$1" == "api" ]]; then
        echo "Entering API container shell..."
        docker-compose exec api /bin/bash
    elif [[ "$1" == "database" ]]; then
        echo "WARNING: Accessing database container directly"
        echo "This bypasses cathedral security - use only for debugging"
        read -p "Continue? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            docker-compose exec database /bin/bash
        fi
    else
        echo "Usage: $0 shell [api|database]"
        exit 1
    fi
}

function show_help() {
    echo "Mallku Docker Management"
    echo
    echo "Usage: $0 [command] [options]"
    echo
    echo "Commands:"
    echo "  start [--build]  Start services (optionally rebuild)"
    echo "  stop             Stop services"
    echo "  restart          Restart services"
    echo "  reset            Reset database (destroys all data)"
    echo "  logs [service]   Show logs (all, api, or database)"
    echo "  status           Show service status (default when no command given)"
    echo "  shell [service]  Access container shell (api or database)"
    echo "  help             Show this help message"
    echo
    echo "Examples:"
    echo "  $0                  # Show current status"
    echo "  $0 start --build    # Build and start services"
    echo "  $0 logs api         # Follow API logs"
    echo "  $0 reset            # Complete database reset"
}

# Main command handling
case "$1" in
    start)
        start_services "$2"
        ;;
    stop)
        stop_services
        ;;
    restart)
        stop_services
        echo
        start_services
        ;;
    reset)
        reset_database
        ;;
    logs)
        show_logs "$2"
        ;;
    status)
        show_status
        ;;
    shell)
        run_shell "$2"
        ;;
    help|--help|-h)
        show_help
        ;;
    "")
        # NO ARGUMENTS - DO SOMETHING REASONABLE!
        # Show status, which tells them what's running and what they can do
        show_status
        ;;
    *)
        echo "Unknown command: $1"
        echo
        show_help
        exit 1
        ;;
esac
