# Use Python 3.9 slim as base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # Chrome/Chromium dependencies
    chromium \
    chromium-driver \
    chromium-sandbox \
    # System utilities
    curl \
    wget \
    gnupg \
    unzip \
    # Python build dependencies
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    # Cleanup
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user for security
RUN useradd -m -s /bin/bash scraper && \
    usermod -aG sudo scraper

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set proper ownership
RUN chown -R scraper:scraper /app

# Create necessary directories and set permissions
RUN mkdir -p /app/logs /app/downloads && \
    chown -R scraper:scraper /app/logs /app/downloads

# Switch to non-root user
USER scraper

# Expose the API port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Set Chrome environment variables for SeleniumBase
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver
ENV CHROME_HEADLESS=true
ENV CHROME_NO_SANDBOX=true
ENV CHROME_DISABLE_DEV_SHM_USAGE=true

# Default command
CMD ["python", "triggers.py"]
