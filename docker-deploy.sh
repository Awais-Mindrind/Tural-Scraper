#!/bin/bash

# TikTok Scraper Docker Deployment Script
# This script helps you deploy the TikTok Scraper using Docker

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    if ! command_exists docker; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command_exists docker-compose; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_success "Prerequisites check passed!"
}

# Function to create environment file
create_env_file() {
    if [ ! -f .env ]; then
        print_status "Creating .env file from template..."
        
        cat > .env << 'EOF'
# Airtable Configuration
AIRTABLE_PAT=your_airtable_personal_access_token_here
AIRTABLE_BASE_ID=your_airtable_base_id_here

# Google Gemini API
GOOGLE_API_KEY=your_google_gemini_api_key_here

# Proxy Configuration (optional)
# PROXY=http://username:password@proxyserver:port

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=scraper_logs.log

# System Configuration
MAX_CONCURRENT_THREADS=3
DEFAULT_PROFILES_PER_HASHTAG=500

# Chrome/Selenium Configuration
CHROME_HEADLESS=true
CHROME_NO_SANDBOX=true
CHROME_DISABLE_DEV_SHM_USAGE=true

# Grafana Password (for monitoring)
GRAFANA_PASSWORD=admin
EOF
        
        print_warning "Please edit .env file with your actual credentials before continuing!"
        print_status "Press Enter when you've updated the .env file..."
        read -r
    else
        print_success ".env file already exists!"
    fi
}

# Function to create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    
    mkdir -p logs downloads config
    
    print_success "Directories created!"
}

# Function to deploy with simple compose
deploy_simple() {
    print_status "Deploying with simple Docker Compose..."
    
    docker-compose -f docker-compose.simple.yml up -d --build
    
    print_success "Simple deployment completed!"
    print_status "Your API is available at: http://localhost:5000"
}

# Function to deploy with full compose
deploy_full() {
    print_status "Deploying with full Docker Compose (includes monitoring)..."
    
    # Create monitoring directories
    mkdir -p monitoring/prometheus monitoring/grafana/dashboards monitoring/grafana/datasources
    
    # Create basic Prometheus config
    cat > monitoring/prometheus.yml << 'EOF'
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'tiktok-scraper'
    static_configs:
      - targets: ['tiktok-scraper:5000']
EOF
    
    # Create basic Grafana datasource
    cat > monitoring/grafana/datasources/prometheus.yml << 'EOF'
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
EOF
    
    docker-compose up -d --build
    
    print_success "Full deployment completed!"
    print_status "Your API is available at: http://localhost:5000"
    print_status "Prometheus monitoring at: http://localhost:9090"
    print_status "Grafana dashboard at: http://localhost:3000 (admin/admin)"
}

# Function to show deployment status
show_status() {
    print_status "Checking deployment status..."
    
    docker-compose ps
    
    print_status "Container logs (last 50 lines):"
    docker-compose logs --tail=50
}

# Function to stop services
stop_services() {
    print_status "Stopping all services..."
    
    if [ -f docker-compose.yml ]; then
        docker-compose down
    fi
    
    if [ -f docker-compose.simple.yml ]; then
        docker-compose -f docker-compose.simple.yml down
    fi
    
    print_success "Services stopped!"
}

# Function to show help
show_help() {
    echo "TikTok Scraper Docker Deployment Script"
    echo ""
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  simple     Deploy with simple configuration (API only)"
    echo "  full       Deploy with full configuration (API + monitoring)"
    echo "  status     Show deployment status"
    echo "  stop       Stop all services"
    echo "  logs       Show container logs"
    echo "  help       Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 simple    # Deploy basic API"
    echo "  $0 full      # Deploy with monitoring"
    echo "  $0 status    # Check status"
    echo "  $0 stop      # Stop services"
}

# Function to show logs
show_logs() {
    print_status "Showing container logs..."
    
    if [ -f docker-compose.yml ]; then
        docker-compose logs -f
    elif [ -f docker-compose.simple.yml ]; then
        docker-compose -f docker-compose.simple.yml logs -f
    else
        print_error "No Docker Compose files found!"
        exit 1
    fi
}

# Main script logic
main() {
    case "${1:-help}" in
        "simple")
            check_prerequisites
            create_env_file
            create_directories
            deploy_simple
            ;;
        "full")
            check_prerequisites
            create_env_file
            create_directories
            deploy_full
            ;;
        "status")
            show_status
            ;;
        "stop")
            stop_services
            ;;
        "logs")
            show_logs
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# Run main function with all arguments
main "$@"
