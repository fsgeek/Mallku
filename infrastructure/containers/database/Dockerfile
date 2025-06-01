# Mallku Database Container - PROOF OF CONCEPT
#
# This is a simplified proof-of-concept Dockerfile that demonstrates
# the isolation principle. A production version would install ArangoDB.

FROM python:3.12-slim

# Install basic dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create mallku user and directories
RUN useradd -m -s /bin/bash mallku \
    && mkdir -p /opt/mallku \
    && chown -R mallku:mallku /opt/mallku

# Copy project files
COPY . /opt/mallku/

# Install Python dependencies
WORKDIR /opt/mallku
RUN pip install -e .[docker]

# Switch to mallku user
USER mallku

# Expose only the Mallku Database API port
EXPOSE 8001

# Health check for the Mallku API
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# For proof of concept, just run a simple API server
CMD ["python", "-m", "uvicorn", "infrastructure.containers.database.api.mallku_database_api:app", "--host", "0.0.0.0", "--port", "8001"]
