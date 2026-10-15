# ─────────────────────────────────────────────────────────────
# VeriGraph AI — Backend Dockerfile  (Python 3.11 / FastAPI)
# Multi-stage build for lean production image
# ─────────────────────────────────────────────────────────────

# ── Stage 1: dependency builder ───────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /build

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_ROOT_USER_ACTION=ignore

# System build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install into a prefix so we can copy cleanly into the runtime stage
RUN pip install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt

# ── Stage 2: runtime ──────────────────────────────────────────
FROM python:3.11-slim AS runtime

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # Put installed packages on the path
    PYTHONPATH=/usr/local/lib/python3.11/site-packages

# Only runtime system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application source
COPY . .

# Create the data directory so the JSON database can write
RUN mkdir -p /app/data

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
