FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy Mallku source (will be mounted in production)
# This is just for the base image
COPY src /app/src

# Install Python dependencies
COPY pyproject.toml /app/
RUN pip install --no-cache-dir uv && \
    uv pip install --system -e .

# Create apprentice user (non-root)
RUN useradd -m -s /bin/bash apprentice && \
    chown -R apprentice:apprentice /app

USER apprentice

# Set Python path
ENV PYTHONPATH=/app:/workspace

# Default command (will be overridden by Loom)
CMD ["python", "-m", "mallku.orchestration.weaver.apprentice_template"]
