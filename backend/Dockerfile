# Multi-stage Dockerfile for VeriGraph Backend

# Stage 1: Base image with dependencies
FROM python:3.10-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Stage 2: Runtime image
FROM base as runtime

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 verigraph && \
    chown -R verigraph:verigraph /app

USER verigraph

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "wsgi:application"]

# Stage 3: Development image
FROM base as development

# Install development dependencies
RUN pip install \
    jupyter \
    ipython \
    black \
    flake8 \
    pytest \
    pytest-cov

COPY . .

RUN useradd -m -u 1000 verigraph && \
    chown -R verigraph:verigraph /app

USER verigraph

WORKDIR /app

EXPOSE 5000 8888

CMD ["python", "app.py"]
