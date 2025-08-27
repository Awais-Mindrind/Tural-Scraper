# TikTok Scraper - AWS Deployment Guide

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [AWS Architecture](#aws-architecture)
3. [Prerequisites](#prerequisites)
4. [Deployment Options](#deployment-options)
5. [EC2 Deployment](#ec2-deployment)
6. [ECS Deployment](#ecs-deployment)
7. [Lambda Deployment](#lambda-deployment)
8. [Monitoring & Scaling](#monitoring--scaling)
9. [Security Configuration](#security-configuration)
10. [Cost Optimization](#cost-optimization)
11. [Troubleshooting](#troubleshooting)

---

## 💻 System Requirements

### **Minimum Requirements**
- **CPU**: 2 vCPUs (Intel/AMD x86_64)
- **RAM**: 4 GB
- **Storage**: 20 GB SSD
- **Network**: 100 Mbps
- **OS**: Ubuntu 20.04+ or Amazon Linux 2

### **Recommended Requirements**
- **CPU**: 4-8 vCPUs
- **RAM**: 8-16 GB
- **Storage**: 50 GB SSD
- **Network**: 1 Gbps
- **OS**: Ubuntu 22.04 LTS

### **Production Requirements**
- **CPU**: 8+ vCPUs
- **RAM**: 16+ GB
- **Storage**: 100+ GB SSD
- **Network**: 1+ Gbps
- **OS**: Ubuntu 22.04 LTS or Amazon Linux 2023

### **Resource Usage Estimates**

| Component | CPU | RAM | Storage | Network |
|-----------|-----|------|---------|---------|
| **API Server** | 0.5-1 vCPU | 1-2 GB | 1-2 GB | Low |
| **Task Manager** | 0.5-1 vCPU | 1-2 GB | 1-2 GB | Low |
| **Scraping Engine** | 2-4 vCPU | 4-8 GB | 5-10 GB | High |
| **Chrome Driver** | 1-2 vCPU | 2-4 GB | 2-5 GB | Medium |
| **LLM Integration** | 0.5-1 vCPU | 1-2 GB | 1-2 GB | Medium |
| **Total (Recommended)** | **4-8 vCPU** | **8-16 GB** | **10-20 GB** | **1 Gbps** |

---

## ☁️ AWS Architecture

### **Recommended Architecture**

```
┌─────────────────────────────────────────────────────────────────┐
│                        AWS Cloud                                │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │   Route 53  │  │ Application │  │      CloudWatch        │ │
│  │   (DNS)     │  │   Gateway   │  │     (Monitoring)       │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
│           │               │                    │               │
│           ▼               ▼                    ▼               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │   CloudFront│  │     ALB     │  │      S3 (Logs)          │ │
│  │  (CDN)      │  │ (Load Bal.) │  │                         │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
│           │               │                    │               │
│           ▼               ▼                    ▼               │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    VPC                                      │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │ │
│  │  │   Public    │  │   Private   │  │      Database       │ │ │
│  │  │   Subnet    │  │   Subnet    │  │      Layer          │ │ │
│  │  │             │  │             │  │                     │ │ │
│  │  │ ┌─────────┐ │  │ ┌─────────┐ │  │  ┌─────────────┐   │ │ │
│  │  │ │   NAT   │ │  │ │ TikTok  │ │  │  │   RDS/      │   │ │ │
│  │  │ │ Gateway │ │  │ │ Scraper │ │  │  │  Airtable   │   │ │ │
│  │  │ │         │ │  │ │  EC2    │ │  │  │  Integration│   │ │ │
│  │  │ └─────────┘ │  │ └─────────┘ │  │  └─────────────┘   │ │ │
│  │  └─────────────┘  └─────────────┘  └─────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### **Alternative Architectures**

#### **Simple Single-Instance**
```
Internet → Route 53 → ALB → EC2 Instance
```

#### **Scalable Multi-Instance**
```
Internet → Route 53 → ALB → Auto Scaling Group → Multiple EC2 Instances
```

#### **Containerized (ECS)**
```
Internet → Route 53 → ALB → ECS Cluster → Fargate Tasks
```

---

## ✅ Prerequisites

### **AWS Account Setup**
1. **AWS Account**: Active AWS account with billing enabled
2. **IAM User**: User with appropriate permissions
3. **Access Keys**: AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
4. **Default Region**: Set your preferred AWS region

### **Required AWS Services**
- **EC2**: Virtual servers
- **VPC**: Virtual private cloud
- **IAM**: Identity and access management
- **CloudWatch**: Monitoring and logging
- **S3**: Object storage (for logs)
- **Route 53**: DNS management (optional)
- **Application Load Balancer**: Load balancing (optional)

### **Local Prerequisites**
- **AWS CLI**: Configured with credentials
- **Terraform** (optional): For infrastructure as code
- **Docker** (optional): For containerized deployment

---

## 🚀 Deployment Options

### **Option 1: Docker on EC2 (Recommended for Start)**
- **Pros**: Containerized, consistent environment, easy scaling
- **Cons**: Requires Docker knowledge
- **Best For**: Development, testing, small production
- **Docker Files**: Uses `docker-compose.simple.yml`

### **Option 2: EC2 Single Instance (Traditional)**
- **Pros**: Simple, cost-effective, full control
- **Cons**: Single point of failure, manual scaling
- **Best For**: Development, testing, small production

### **Option 3: ECS with Fargate (Containerized)**
- **Pros**: Serverless, auto-scaling, managed containers
- **Cons**: Higher cost, less control
- **Best For**: Production, enterprise
- **Docker Files**: Uses `Dockerfile` with ECS task definitions

### **Option 4: EC2 Auto Scaling Group**
- **Pros**: High availability, automatic scaling
- **Cons**: More complex, higher cost
- **Best For**: Production, high traffic

### **Option 5: Lambda + API Gateway**
- **Pros**: Serverless, pay-per-use
- **Cons**: Limited execution time, cold starts
- **Best For**: Light usage, event-driven

---

## 🐳 Docker on EC2 Deployment (Recommended)

### **Overview**
This deployment option uses Docker containers on EC2, providing a consistent environment and easy scaling. It leverages the Docker setup we've created with `docker-compose.simple.yml`.

### **Advantages**
- ✅ **Consistent Environment**: Same container runs everywhere
- ✅ **Easy Scaling**: Scale horizontally with Docker Compose
- ✅ **No Dependency Issues**: Chrome driver handled automatically
- ✅ **Easy Updates**: Rebuild and redeploy containers
- ✅ **Resource Isolation**: Better resource management

### **Step 1: Launch EC2 Instance with Docker**

#### **VPC Configuration**
```bash
# Create VPC
aws ec2 create-vpc --cidr-block 10.0.0.0/16 --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=TikTok-Scraper-VPC}]'

# Create subnets
aws ec2 create-subnet --vpc-id vpc-xxxxx --cidr-block 10.0.1.0/24 --availability-zone us-east-1a
aws ec2 create-subnet --vpc-id vpc-xxxxx --cidr-block 10.0.2.0/24 --availability-zone us-east-1b

# Create Internet Gateway
aws ec2 create-internet-gateway
aws ec2 attach-internet-gateway --vpc-id vpc-xxxxx --internet-gateway-id igw-xxxxx

# Create route table
aws ec2 create-route-table --vpc-id vpc-xxxxx
aws ec2 create-route --route-table-id rtb-xxxxx --destination-cidr-block 0.0.0.0/0 --gateway-id igw-xxxxx
```

#### **Security Group Configuration**
```bash
# Create security group
aws ec2 create-security-group --group-name TikTok-Scraper-SG --description "Security group for TikTok Scraper" --vpc-id vpc-xxxxx

# Allow SSH (port 22)
aws ec2 authorize-security-group-ingress --group-id sg-xxxxx --protocol tcp --port 22 --cidr 0.0.0.0/0

# Allow HTTP (port 80)
aws ec2 authorize-security-group-ingress --group-id sg-xxxxx --protocol tcp --port 80 --cidr 0.0.0.0/0

# Allow HTTPS (port 443)
aws ec2 authorize-security-group-ingress --group-id sg-xxxxx --protocol tcp --port 443 --cidr 0.0.0.0/0

# Allow API port (5000)
aws ec2 authorize-security-group-ingress --group-id sg-xxxxx --protocol tcp --port 5000 --cidr 0.0.0.0/0

# Allow outbound traffic
aws ec2 authorize-security-group-egress --group-id sg-xxxxx --protocol -1 --port -1 --cidr 0.0.0.0/0
```

### **Step 2: Launch EC2 Instance**

#### **Instance Configuration**
```bash
# Launch EC2 instance
aws ec2 run-instances \
  --image-id ami-0c02fb55956c7d316 \
  --count 1 \
  --instance-type t3.large \
  --key-name your-key-pair \
  --security-group-ids sg-xxxxx \
  --subnet-id subnet-xxxxx \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=TikTok-Scraper}]' \
  --user-data file://user-data.sh
```

#### **User Data Script for Docker (user-data.sh)**
```bash
#!/bin/bash
# Update system
apt-get update -y
apt-get upgrade -y

# Install Docker
apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update -y
apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Create application user
useradd -m -s /bin/bash scraper
usermod -aG docker scraper

# Create application directory
mkdir -p /home/scraper/tiktok-scraper
chown -R scraper:scraper /home/scraper/tiktok-scraper

# Create systemd service for Docker Compose
tee /etc/systemd/system/tiktok-scraper-docker.service > /dev/null << 'SERVICE'
[Unit]
Description=TikTok Scraper Docker Service
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
User=scraper
WorkingDirectory=/home/scraper/tiktok-scraper
ExecStart=/usr/local/bin/docker-compose -f docker-compose.simple.yml up -d
ExecStop=/usr/local/bin/docker-compose -f docker-compose.simple.yml down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
SERVICE

# Enable and start service
systemctl daemon-reload
systemctl enable tiktok-scraper-docker
systemctl start tiktok-scraper-docker

# Configure nginx for Docker
apt-get install -y nginx
cat > /etc/nginx/sites-available/tiktok-scraper << 'NGINX'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

NGINX

# Enable nginx site
ln -s /etc/nginx/sites-available/tiktok-scraper /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default
systemctl restart nginx
```

### **Step 3: Deploy Docker Application**

#### **Upload Application Files**
```bash
# Copy application files to EC2 (including Docker files)
scp -i your-key.pem -r ./* ubuntu@your-ec2-ip:/home/scraper/tiktok-scraper/

# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Set proper permissions
sudo chown -R scraper:scraper /home/scraper/tiktok-scraper/
sudo chmod +x /home/scraper/tiktok-scraper/docker-deploy.sh
```

#### **Environment Configuration**
```bash
# Create .env file
sudo -u scraper tee /home/scraper/tiktok-scraper/.env > /dev/null << 'ENV'
# Airtable Configuration
AIRTABLE_PAT=your_airtable_token
AIRTABLE_BASE_ID=your_airtable_base_id

# Google Gemini API
GOOGLE_API_KEY=your_gemini_api_key

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
ENV

# Create necessary directories
sudo -u scraper mkdir -p /home/scraper/tiktok-scraper/logs
sudo -u scraper mkdir -p /home/scraper/tiktok-scraper/downloads

# Deploy with Docker
cd /home/scraper/tiktok-scraper
sudo -u scraper ./docker-deploy.sh simple

# Check status
sudo -u scraper ./docker-deploy.sh status
```

---

## 🖥️ Traditional EC2 Deployment

### **Overview**
This deployment option installs Python and dependencies directly on EC2, suitable for users who prefer traditional server management.

### **Step 1: Create VPC and Security Groups**
#### **VPC Configuration**
```bash
# Create VPC
aws ec2 create-vpc --cidr-block 10.0.0.0/16 --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=TikTok-Scraper-VPC}]'

# Create subnets
aws ec2 create-subnet --vpc-id vpc-xxxxx --cidr-block 10.0.1.0/24 --availability-zone us-east-1a
aws ec2 create-subnet --vpc-id vpc-xxxxx --cidr-block 10.0.2.0/24 --availability-zone us-east-1b

# Create Internet Gateway
aws ec2 create-internet-gateway
aws ec2 attach-internet-gateway --vpc-id vpc-xxxxx --internet-gateway-id igw-xxxxx

# Create route table
aws ec2 create-route-table --vpc-id vpc-xxxxx
aws ec2 create-route --route-table-id rtb-xxxxx --destination-cidr-block 0.0.0.0/0 --gateway-id igw-xxxxx
```

#### **Security Group Configuration**
```bash
# Create security group
aws ec2 create-security-group --group-name TikTok-Scraper-SG --description "Security group for TikTok Scraper" --vpc-id vpc-xxxxx

# Allow SSH (port 22)
aws ec2 authorize-security-group-ingress --group-id sg-xxxxx --protocol tcp --port 22 --cidr 0.0.0.0/0

# Allow HTTP (port 80)
aws ec2 authorize-security-group-ingress --group-id sg-xxxxx --protocol tcp --port 80 --cidr 0.0.0.0/0

# Allow HTTPS (port 443)
aws ec2 authorize-security-group-ingress --group-id sg-xxxxx --protocol tcp --port 443 --cidr 0.0.0.0/0

# Allow API port (5000)
aws ec2 authorize-security-group-ingress --group-id sg-xxxxx --protocol tcp --port 5000 --cidr 0.0.0.0/0

# Allow outbound traffic
aws ec2 authorize-security-group-egress --group-id sg-xxxxx --protocol -1 --port -1 --cidr 0.0.0.0/0
```

### **Step 2: Launch EC2 Instance**
#### **Instance Configuration**
```bash
# Launch EC2 instance
aws ec2 run-instances \
  --image-id ami-0c02fb55956c7d316 \
  --count 1 \
  --instance-type t3.large \
  --key-name your-key-pair \
  --security-group-ids sg-xxxxx \
  --subnet-id subnet-xxxxx \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=TikTok-Scraper}]' \
  --user-data file://user-data-traditional.sh
```

#### **User Data Script for Traditional Deployment (user-data-traditional.sh)**
```bash
#!/bin/bash
# Update system
apt-get update -y
apt-get upgrade -y

# Install Python and dependencies
apt-get install -y python3 python3-pip python3-venv
apt-get install -y chromium-browser chromium-chromedriver
apt-get install -y nginx

# Install system dependencies
apt-get install -y build-essential libssl-dev libffi-dev python3-dev

# Create application user
useradd -m -s /bin/bash scraper
usermod -aG sudo scraper

# Switch to application user
su - scraper << 'EOF'
# Create application directory
mkdir -p /home/scraper/tiktok-scraper
cd /home/scraper/tiktok-scraper

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install fastapi uvicorn seleniumbase pyairtable python-dotenv apscheduler

# Create systemd service
sudo tee /etc/systemd/system/tiktok-scraper.service > /dev/null << 'SERVICE'
[Unit]
Description=TikTok Scraper Service
After=network.target

[Service]
Type=simple
User=scraper
WorkingDirectory=/home/scraper/tiktok-scraper
Environment=PATH=/home/scraper/tiktok-scraper/venv/bin
ExecStart=/home/scraper/tiktok-scraper/venv/bin/python triggers.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable tiktok-scraper
sudo systemctl start tiktok-scraper
EOF

# Configure nginx
cat > /etc/nginx/sites-available/tiktok-scraper << 'NGINX'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

NGINX

# Enable nginx site
ln -s /etc/nginx/sites-available/tiktok-scraper /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default
systemctl restart nginx
```

### **Step 3: Deploy Traditional Application**
#### **Upload Application Files**
```bash
# Copy application files to EC2
scp -i your-key.pem -r ./* ubuntu@your-ec2-ip:/home/scraper/tiktok-scraper/

# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Set proper permissions
sudo chown -R scraper:scraper /home/scraper/tiktok-scraper/
sudo chmod +x /home/scraper/tiktok-scraper/triggers.py
```

#### **Environment Configuration**
```bash
# Create .env file
sudo -u scraper tee /home/scraper/tiktok-scraper/.env > /dev/null << 'ENV'
AIRTABLE_PAT=your_airtable_token
GOOGLE_API_KEY=your_gemini_api_key
PROXY=your_proxy_settings
LOG_LEVEL=INFO
MAX_CONCURRENT_THREADS=3
ENV

# Restart service
sudo systemctl restart tiktok-scraper
```

---

## 🐳 ECS Deployment

### **Overview**
ECS deployment uses the Docker container we've created, providing managed container orchestration with automatic scaling and high availability.

### **Step 1: Create ECR Repository**
```bash
# Create ECR repository
aws ecr create-repository --repository-name tiktok-scraper

# Get login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-account-id.dkr.ecr.us-east-1.amazonaws.com
```

### **Step 2: Build and Push Docker Image**

#### **Dockerfile**
```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -s /bin/bash scraper && \
    chown -R scraper:scraper /app

# Switch to non-root user
USER scraper

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Start application
CMD ["python", "triggers.py"]
```

#### **Build and Push**
```bash
# Build image
docker build -t tiktok-scraper .

# Tag image
docker tag tiktok-scraper:latest your-account-id.dkr.ecr.us-east-1.amazonaws.com/tiktok-scraper:latest

# Push to ECR
docker push your-account-id.dkr.ecr.us-east-1.amazonaws.com/tiktok-scraper:latest
```

### **Step 3: Create ECS Cluster and Service**

#### **ECS Task Definition**
```json
{
  "family": "tiktok-scraper",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::your-account:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::your-account:role/ecsTaskRole",
  "containerDefinitions": [
    {
      "name": "tiktok-scraper",
      "image": "your-account-id.dkr.ecr.us-east-1.amazonaws.com/tiktok-scraper:latest",
      "portMappings": [
        {
          "containerPort": 5000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "AIRTABLE_PAT",
          "value": "your_airtable_token"
        },
        {
          "name": "GOOGLE_API_KEY",
          "value": "your_gemini_api_key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/tiktok-scraper",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

#### **Create ECS Service**
```bash
# Create cluster
aws ecs create-cluster --cluster-name tiktok-scraper-cluster

# Create service
aws ecs create-service \
  --cluster tiktok-scraper-cluster \
  --service-name tiktok-scraper-service \
  --task-definition tiktok-scraper:1 \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxxxx],securityGroups=[sg-xxxxx],assignPublicIp=ENABLED}"
```

---

## 🐳 Docker vs Traditional Deployment Comparison

### **Docker on EC2 Advantages**
- ✅ **Consistent Environment**: Same container runs everywhere
- ✅ **Easy Scaling**: Scale horizontally with Docker Compose
- ✅ **No Dependency Issues**: Chrome driver handled automatically
- ✅ **Easy Updates**: Rebuild and redeploy containers
- ✅ **Resource Isolation**: Better resource management
- ✅ **Portability**: Easy to move between environments

### **Traditional EC2 Advantages**
- ✅ **Familiar**: Standard server management
- ✅ **Direct Access**: Full control over system
- ✅ **Debugging**: Easier to troubleshoot system issues
- ✅ **Customization**: Full system customization
- ✅ **Performance**: Slightly better performance (no container overhead)

### **Recommendation**
- **Use Docker on EC2** for: Development, testing, production, scaling
- **Use Traditional EC2** for: Legacy systems, custom requirements, debugging

---

## 📊 Monitoring & Scaling

### **CloudWatch Monitoring**

#### **Key Metrics**
- **CPU Utilization**: Target < 70%
- **Memory Utilization**: Target < 80%
- **Network I/O**: Monitor bandwidth usage
- **Disk I/O**: Monitor storage performance
- **Application Metrics**: Response time, error rate

#### **CloudWatch Dashboard**
```bash
# Create dashboard
aws cloudwatch put-dashboard \
  --dashboard-name "TikTok-Scraper-Monitoring" \
  --dashboard-body file://dashboard.json
```

#### **Dashboard Configuration (dashboard.json)**
```json
{
  "widgets": [
    {
      "type": "metric",
      "properties": {
        "metrics": [
          ["AWS/EC2", "CPUUtilization", "InstanceId", "i-xxxxx"],
          ["AWS/EC2", "NetworkIn", "InstanceId", "i-xxxxx"],
          ["AWS/EC2", "NetworkOut", "InstanceId", "i-xxxxx"]
        ],
        "period": 300,
        "stat": "Average",
        "region": "us-east-1",
        "title": "EC2 Metrics"
      }
    }
  ]
}
```

### **Auto Scaling Configuration**

#### **EC2 Auto Scaling Group**
```bash
# Create launch template
aws ec2 create-launch-template \
  --launch-template-name tiktok-scraper-template \
  --version-description "v1" \
  --launch-template-data file://launch-template.json

# Create auto scaling group
aws autoscaling create-auto-scaling-group \
  --auto-scaling-group-name tiktok-scraper-asg \
  --launch-template LaunchTemplateName=tiktok-scraper-template,Version='$Latest' \
  --min-size 1 \
  --max-size 5 \
  --desired-capacity 1 \
  --vpc-zone-identifier "subnet-xxxxx,subnet-yyyyy"
```

#### **Scaling Policies**
```bash
# CPU-based scaling policy
aws autoscaling put-scaling-policy \
  --auto-scaling-group-name tiktok-scraper-asg \
  --policy-name cpu-scaling-policy \
  --policy-type TargetTrackingScaling \
  --target-tracking-configuration '{"PredefinedMetricSpecification":{"PredefinedMetricType":"ASGAverageCPUUtilization"},"TargetValue":70.0}'
```

---

## 🔒 Security Configuration

### **IAM Roles and Policies**

#### **EC2 Instance Role**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cloudwatch:PutMetricData",
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "*"
    }
  ]
}
```

#### **Security Group Rules**
```bash
# Restrict SSH access to your IP
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxx \
  --protocol tcp \
  --port 22 \
  --cidr your-ip-address/32

# Allow only necessary ports
aws ec2 revoke-security-group-ingress \
  --group-id sg-xxxxx \
  --protocol tcp \
  --port 22 \
  --cidr 0.0.0.0/0
```

### **SSL/TLS Configuration**

#### **Certificate Manager**
```bash
# Request SSL certificate
aws acm request-certificate \
  --domain-name your-domain.com \
  --validation-method DNS \
  --subject-alternative-names "*.your-domain.com"
```

#### **HTTPS Configuration**
```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /etc/ssl/certs/your-domain.com.crt;
    ssl_certificate_key /etc/ssl/private/your-domain.com.key;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 💰 Cost Optimization

### **Instance Type Selection**

| Use Case | Instance Type | Cost/Hour | Monthly Cost |
|----------|---------------|-----------|--------------|
| **Development** | t3.micro | $0.0104 | ~$7.50 |
| **Testing** | t3.small | $0.0208 | ~$15.00 |
| **Small Production** | t3.medium | $0.0416 | ~$30.00 |
| **Production** | t3.large | $0.0832 | ~$60.00 |
| **High Performance** | c5.large | $0.085 | ~$61.20 |

### **Reserved Instances**
```bash
# Purchase reserved instance for 1 year
aws ec2 purchase-reserved-instances-offering \
  --reserved-instances-offering-id ri-xxxxx \
  --instance-count 1
```

### **Spot Instances (Development Only)**
```bash
# Launch spot instance
aws ec2 run-instances \
  --image-id ami-xxxxx \
  --instance-type t3.large \
  --instance-market-options 'MarketType=spot,SpotOptions={MaxPrice=0.05}'
```

### **Cost Monitoring**
```bash
# Set up billing alerts
aws cloudwatch put-metric-alarm \
  --alarm-name "Monthly-Billing-Alert" \
  --alarm-description "Alert when monthly billing exceeds threshold" \
  --metric-name EstimatedCharges \
  --namespace AWS/Billing \
  --statistic Maximum \
  --period 86400 \
  --threshold 100 \
  --comparison-operator GreaterThanThreshold
```

---

## 🔧 Troubleshooting

### **Common Issues**

#### **1. Chrome Driver Issues**
```bash
# Check Chrome installation
chromium-browser --version

# Check ChromeDriver
chromedriver --version

# Install specific version
wget https://chromedriver.storage.googleapis.com/version/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
```

#### **2. Memory Issues**
```bash
# Check memory usage
free -h

# Check swap
swapon --show

# Create swap file
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

#### **3. Network Issues**
```bash
# Check network connectivity
ping 8.8.8.8

# Check DNS resolution
nslookup google.com

# Check firewall rules
sudo ufw status
```

### **Log Analysis**

#### **Application Logs**
```bash
# View application logs
sudo journalctl -u tiktok-scraper -f

# Check nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

#### **System Logs**
```bash
# Check system logs
sudo dmesg | tail

# Check cloud-init logs
sudo cat /var/log/cloud-init-output.log
```

### **Performance Tuning**

#### **Chrome Optimization**
```bash
# Add Chrome flags to reduce memory usage
chromium-browser --no-sandbox --disable-dev-shm-usage --disable-gpu --headless
```

#### **System Optimization**
```bash
# Optimize system settings
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
echo 'vm.vfs_cache_pressure=50' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

---

## 📋 Deployment Checklist

### **Pre-Deployment**
- [ ] AWS account configured with billing
- [ ] IAM user with appropriate permissions
- [ ] SSH key pair created
- [ ] Environment variables prepared
- [ ] Application code tested locally

### **Infrastructure Setup**
- [ ] VPC and subnets created
- [ ] Security groups configured
- [ ] Internet gateway attached
- [ ] Route tables configured

### **Application Deployment**
- [ ] EC2 instance launched
- [ ] Application files uploaded
- [ ] Dependencies installed
- [ ] Environment configured
- [ ] Service started

### **Post-Deployment**
- [ ] Health checks passing
- [ ] API endpoints responding
- [ ] Monitoring configured
- [ ] Alerts set up
- [ ] Backup strategy implemented

---

## 🚀 Quick Start Commands

### **Complete Docker Deployment in One Script**
```bash
#!/bin/bash
# Set variables
INSTANCE_TYPE="t3.large"
KEY_NAME="your-key-pair"
SECURITY_GROUP="sg-xxxxx"
SUBNET_ID="subnet-xxxxx"

# Launch instance with Docker user data
INSTANCE_ID=$(aws ec2 run-instances \
  --image-id ami-0c02fb55956c7d316 \
  --count 1 \
  --instance-type $INSTANCE_TYPE \
  --key-name $KEY_NAME \
  --security-group-ids $SECURITY_GROUP \
  --subnet-id $SUBNET_ID \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=TikTok-Scraper-Docker}]' \
  --user-data file://user-data.sh \
  --query 'Instances[0].InstanceId' \
  --output text)

echo "Instance launched: $INSTANCE_ID"

# Wait for instance to be running
aws ec2 wait instance-running --instance-ids $INSTANCE_ID

# Get public IP
PUBLIC_IP=$(aws ec2 describe-instances \
  --instance-ids $INSTANCE_ID \
  --query 'Reservations[0].Instances[0].PublicIpAddress' \
  --output text)

echo "Instance IP: $PUBLIC_IP"
echo "Waiting for Docker setup to complete..."

# Wait for Docker to be ready (give it time to install Docker)
sleep 120

# Copy application files
echo "Copying application files..."
scp -i $KEY_NAME.pem -r ./* ubuntu@$PUBLIC_IP:/home/scraper/tiktok-scraper/

# SSH and deploy
echo "Deploying application..."
ssh -i $KEY_NAME.pem ubuntu@$PUBLIC_IP << 'EOF'
cd /home/scraper/tiktok-scraper
sudo chown -R scraper:scraper /home/scraper/tiktok-scraper/
sudo chmod +x /home/scraper/tiktok-scraper/docker-deploy.sh

# Create .env file (you'll need to edit this with your actual values)
sudo -u scraper tee .env > /dev/null << 'ENV'
AIRTABLE_PAT=your_airtable_token_here
AIRTABLE_BASE_ID=your_base_id_here
GOOGLE_API_KEY=your_gemini_key_here
LOG_LEVEL=INFO
MAX_CONCURRENT_THREADS=3
ENV

# Deploy with Docker
sudo -u scraper ./docker-deploy.sh simple
EOF

echo "Deployment complete! Access your API at: http://$PUBLIC_IP"
echo "Check status with: ssh -i $KEY_NAME.pem ubuntu@$PUBLIC_IP 'cd /home/scraper/tiktok-scraper && sudo -u scraper ./docker-deploy.sh status'"
```

### **Complete Traditional Deployment in One Script**
```bash
#!/bin/bash
# Set variables
INSTANCE_TYPE="t3.large"
KEY_NAME="your-key-pair"
SECURITY_GROUP="sg-xxxxx"
SUBNET_ID="subnet-xxxxx"

# Launch instance with traditional user data
INSTANCE_ID=$(aws ec2 run-instances \
  --image-id ami-0c02fb55956c7d316 \
  --count 1 \
  --instance-type $INSTANCE_TYPE \
  --key-name $KEY_NAME \
  --security-group-ids $SECURITY_GROUP \
  --subnet-id $SUBNET_ID \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=TikTok-Scraper-Traditional}]' \
  --user-data file://user-data-traditional.sh \
  --query 'Instances[0].InstanceId' \
  --output text)

echo "Instance launched: $INSTANCE_ID"

# Wait for instance to be running
aws ec2 wait instance-running --instance-ids $INSTANCE_ID

# Get public IP
PUBLIC_IP=$(aws ec2 describe-instances \
  --instance-ids $INSTANCE_ID \
  --query 'Reservations[0].Instances[0].PublicIpAddress' \
  --output text)

echo "Instance IP: $PUBLIC_IP"
echo "Deployment complete! Access your API at: http://$PUBLIC_IP"
```

---

## 📞 Support & Resources

### **AWS Documentation**
- [EC2 User Guide](https://docs.aws.amazon.com/ec2/)
- [ECS User Guide](https://docs.aws.amazon.com/ecs/)
- [VPC User Guide](https://docs.aws.amazon.com/vpc/)
- [CloudWatch User Guide](https://docs.aws.amazon.com/cloudwatch/)

### **TikTok Scraper Resources**
- [Project Documentation](./PROJECT_DOCUMENTATION.md)
- [API Reference](./api.py)
- [Test Suite](./test_triggers.py)

### **Getting Help**
1. Check the troubleshooting section above
2. Review AWS CloudWatch logs
3. Check application logs
4. Verify security group configurations
5. Test network connectivity

---

*This deployment guide covers the most common AWS deployment scenarios. For production deployments, consider additional factors like high availability, disaster recovery, and compliance requirements.*
