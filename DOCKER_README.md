# TikTok Scraper - Docker Deployment Guide

## 🐳 Overview

This guide explains how to deploy the TikTok Scraper using Docker and Docker Compose. The Docker setup includes:

- **Main Application**: TikTok Scraper with all dependencies
- **Chrome/Chromium**: Automatically handled by SeleniumBase
- **Optional Services**: Redis, Nginx, Prometheus, Grafana
- **Health Checks**: Built-in monitoring and restart policies
- **Volume Management**: Persistent data and logs

## 📋 Prerequisites

### **Required Software**
- **Docker**: Version 20.10+ 
- **Docker Compose**: Version 2.0+
- **Git**: To clone the repository

### **System Requirements**
- **RAM**: Minimum 4GB, Recommended 8GB+
- **Storage**: Minimum 10GB free space
- **OS**: Linux, macOS, or Windows with Docker support

## 🚀 Quick Start

### **1. Clone Repository**
```bash
git clone <your-repo-url>
cd TikTok-Scraper
```

### **2. Make Script Executable**
```bash
chmod +x docker-deploy.sh
```

### **3. Deploy (Choose One)**

#### **Option A: Simple Deployment (Recommended for Start)**
```bash
./docker-deploy.sh simple
```

#### **Option B: Full Deployment (with Monitoring)**
```bash
./docker-deploy.sh full
```

## 📁 Docker Files Structure

```
TikTok-Scraper/
├── Dockerfile                    # Main application container
├── docker-compose.yml           # Full deployment (all services)
├── docker-compose.simple.yml    # Simple deployment (API only)
├── .dockerignore                # Exclude files from build
├── docker-deploy.sh             # Deployment automation script
├── DOCKER_README.md             # This file
└── ... (other project files)
```

## 🔧 Manual Deployment

### **1. Create Environment File**
```bash
# Copy and edit the environment template
cp .env.example .env
nano .env
```

**Required Environment Variables:**
```env
# Airtable Configuration
AIRTABLE_PAT=your_airtable_token
AIRTABLE_BASE_ID=your_base_id

# Google Gemini API
GOOGLE_API_KEY=your_gemini_key

# Optional: Proxy settings
PROXY=http://username:password@proxyserver:port
```

### **2. Create Directories**
```bash
mkdir -p logs downloads config
```

### **3. Deploy with Docker Compose**

#### **Simple Deployment (API Only)**
```bash
docker-compose -f docker-compose.simple.yml up -d --build
```

#### **Full Deployment (with Monitoring)**
```bash
docker-compose up -d --build
```

## 🎯 Deployment Options

### **Simple Deployment (`docker-compose.simple.yml`)**
- ✅ **TikTok Scraper API** (port 5000)
- ✅ **Chrome/Chromium** with SeleniumBase
- ✅ **Volume mounts** for logs and downloads
- ✅ **Health checks** and restart policies
- ✅ **Resource limits** (4GB RAM, 2 CPU cores)

**Use Case**: Development, testing, basic production

### **Full Deployment (`docker-compose.yml`)**
- ✅ **All Simple features** +
- ✅ **Redis** for task queue (port 6379)
- ✅ **Nginx** reverse proxy (ports 80, 443)
- ✅ **Prometheus** monitoring (port 9090)
- ✅ **Grafana** dashboards (port 3000)

**Use Case**: Production, monitoring, scaling

## 🌐 Service Ports

| Service | Port | Description |
|---------|------|-------------|
| **TikTok Scraper** | 5000 | Main API endpoints |
| **Redis** | 6379 | Task queue (optional) |
| **Nginx** | 80, 443 | Reverse proxy (optional) |
| **Prometheus** | 9090 | Metrics collection (optional) |
| **Grafana** | 3000 | Monitoring dashboards (optional) |

## 📊 Monitoring & Health Checks

### **Built-in Health Checks**
- **Application**: `/health` endpoint every 30s
- **Container**: Automatic restart on failure
- **Resource Monitoring**: CPU and memory limits

### **Optional Monitoring Stack**
- **Prometheus**: Collects metrics from the scraper
- **Grafana**: Visualizes performance data
- **Custom Dashboards**: Pre-configured for TikTok Scraper

## 🔍 Troubleshooting

### **Common Issues**

#### **1. Chrome Driver Problems**
```bash
# Check container logs
docker-compose logs tiktok-scraper

# Verify Chrome installation
docker exec -it tiktok-scraper chromium-browser --version
docker exec -it tiktok-scraper chromedriver --version
```

#### **2. Memory Issues**
```bash
# Check container resource usage
docker stats tiktok-scraper

# Increase memory limits in docker-compose.yml
deploy:
  resources:
    limits:
      memory: 8G  # Increase from 4G
```

#### **3. Port Conflicts**
```bash
# Check what's using port 5000
sudo lsof -i :5000

# Change port in docker-compose.yml
ports:
  - "5001:5000"  # Use port 5001 instead
```

### **Useful Commands**

#### **View Logs**
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f tiktok-scraper

# Last 100 lines
docker-compose logs --tail=100 tiktok-scraper
```

#### **Container Management**
```bash
# Check status
docker-compose ps

# Restart service
docker-compose restart tiktok-scraper

# Stop all services
docker-compose down

# Remove volumes (careful!)
docker-compose down -v
```

#### **Shell Access**
```bash
# Access container shell
docker exec -it tiktok-scraper bash

# Check environment variables
docker exec -it tiktok-scraper env

# Test API from inside container
docker exec -it tiktok-scraper curl http://localhost:5000/health
```

## 🔒 Security Considerations

### **Container Security**
- ✅ **Non-root user**: Application runs as `scraper` user
- ✅ **Read-only filesystem**: Critical directories mounted as volumes
- ✅ **Resource limits**: Prevents resource exhaustion attacks
- ✅ **Health checks**: Automatic failure detection and restart

### **Network Security**
- ✅ **Isolated network**: Services communicate over internal Docker network
- ✅ **Port exposure**: Only necessary ports exposed to host
- ✅ **Reverse proxy**: Nginx handles external traffic (optional)

### **Data Security**
- ✅ **Volume mounts**: Sensitive data stored on host
- ✅ **Environment variables**: Secrets managed via .env file
- ✅ **No secrets in images**: Credentials mounted at runtime

## 📈 Scaling & Performance

### **Resource Optimization**

#### **Memory Tuning**
```yaml
deploy:
  resources:
    limits:
      memory: 8G      # Increase for heavy scraping
    reservations:
      memory: 4G      # Guaranteed memory
```

#### **CPU Tuning**
```yaml
deploy:
  resources:
    limits:
      cpus: '4.0'     # Use 4 CPU cores
    reservations:
      cpus: '2.0'     # Guaranteed 2 cores
```

### **Horizontal Scaling**
```bash
# Scale to multiple instances
docker-compose up -d --scale tiktok-scraper=3

# Load balancer configuration needed for multiple instances
```

### **Performance Monitoring**
```bash
# Real-time resource usage
docker stats

# Container performance metrics
docker exec -it tiktok-scraper python -c "
import psutil
print(f'CPU: {psutil.cpu_percent()}%')
print(f'Memory: {psutil.virtual_memory().percent}%')
"
```

## 🚀 Production Deployment

### **Environment-Specific Configs**

#### **Development**
```bash
# Use simple compose
docker-compose -f docker-compose.simple.yml up -d
```

#### **Staging**
```bash
# Use full compose with reduced resources
docker-compose -f docker-compose.staging.yml up -d
```

#### **Production**
```bash
# Use full compose with production settings
docker-compose -f docker-compose.prod.yml up -d
```

### **Production Checklist**
- [ ] **Environment variables** properly configured
- [ ] **Resource limits** appropriate for workload
- [ ] **Monitoring** enabled and configured
- [ ] **Logging** configured and rotated
- [ ] **Backup strategy** for persistent data
- [ ] **SSL certificates** configured (if using Nginx)
- [ ] **Firewall rules** configured
- [ ] **Health checks** passing

## 🔄 Updates & Maintenance

### **Updating the Application**
```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

### **Updating Dependencies**
```bash
# Rebuild with new requirements
docker-compose build --no-cache tiktok-scraper
docker-compose up -d
```

### **Database Migrations**
```bash
# If using local database
docker-compose exec tiktok-scraper python manage.py migrate
```

## 📚 Additional Resources

### **Docker Documentation**
- [Docker Getting Started](https://docs.docker.com/get-started/)
- [Docker Compose Overview](https://docs.docker.com/compose/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

### **SeleniumBase Documentation**
- [SeleniumBase Installation](https://seleniumbase.io/help_docs/installation/)
- [Chrome Driver Setup](https://seleniumbase.io/help_docs/chrome_driver_setup/)

### **Project Documentation**
- [Main Project Documentation](./PROJECT_DOCUMENTATION.md)
- [API Reference](./api.py)
- [AWS Deployment Guide](./AWS_DEPLOYMENT_GUIDE.md)

## 🆘 Getting Help

### **Common Solutions**
1. **Check logs**: `docker-compose logs tiktok-scraper`
2. **Verify environment**: Check `.env` file configuration
3. **Resource issues**: Monitor with `docker stats`
4. **Network issues**: Check port conflicts and firewall

### **Support Channels**
- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: Check this guide and project docs
- **Community**: Join developer discussions

---

## 🎉 Quick Commands Reference

```bash
# Deploy
./docker-deploy.sh simple      # Simple deployment
./docker-deploy.sh full        # Full deployment with monitoring

# Management
./docker-deploy.sh status      # Check status
./docker-deploy.sh stop        # Stop services
./docker-deploy.sh logs        # View logs

# Manual Docker commands
docker-compose up -d           # Start services
docker-compose down            # Stop services
docker-compose logs -f         # Follow logs
docker-compose ps              # Check status
docker-compose restart         # Restart services
```

---

*This Docker deployment guide provides everything you need to run the TikTok Scraper in containers. For production deployments, consider additional factors like high availability, backup strategies, and security hardening.*
