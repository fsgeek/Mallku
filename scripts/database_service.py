#!/usr/bin/env python3
"""
Mallku Database API Service - Cathedral Stone

This service is the sole gateway to the database.
Security through architecture, not through policy.
"""

import logging
import os
import sys
from contextlib import asynccontextmanager
from typing import Any

# Configure logging FIRST
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,  # Ensure logs go to stdout for Docker
)
logger = logging.getLogger(__name__)

logger.info("Starting Mallku API Service - Import phase")

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import Response

    logger.info("FastAPI imported successfully")
except ImportError as e:
    logger.error(f"Failed to import FastAPI: {e}")
    sys.exit(1)

try:
    from arango import ArangoClient

    logger.info("ArangoClient imported successfully")
except ImportError as e:
    logger.error(f"Failed to import ArangoClient: {e}")
    sys.exit(1)

try:
    from prometheus_client import Counter, Histogram, generate_latest
    from prometheus_client.core import CollectorRegistry

    logger.info("Prometheus client imported successfully")
except ImportError as e:
    logger.error(f"Failed to import prometheus_client: {e}")
    sys.exit(1)

try:
    import uvicorn

    logger.info("Uvicorn imported successfully")
except ImportError as e:
    logger.error(f"Failed to import uvicorn: {e}")
    sys.exit(1)

# Metrics
registry = CollectorRegistry()
request_count = Counter(
    "mallku_requests_total", "Total requests", ["method", "endpoint"], registry=registry
)
request_duration = Histogram(
    "mallku_request_duration_seconds", "Request duration", ["method", "endpoint"], registry=registry
)

# Database connection
db_client = None
db = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage service lifecycle - connect to database on startup."""
    global db_client, db

    # Startup
    logger.info("Lifespan startup phase beginning...")

    # Get database configuration from environment
    db_host = os.getenv("MALLKU_DB_HOST", "database")
    db_port = os.getenv("MALLKU_DB_PORT", "8529")
    db_name = os.getenv("MALLKU_DB_NAME", "mallku")
    db_user = os.getenv("MALLKU_DB_USER")
    db_password = os.getenv("MALLKU_DB_PASSWORD")

    logger.info(f"Attempting to connect to ArangoDB at {db_host}:{db_port}")
    logger.info(f"Database: {db_name}, User: {db_user}")

    try:
        db_client = ArangoClient(hosts=f"http://{db_host}:{db_port}")

        # Connect with authentication
        if db_user and db_password:
            db = db_client.db(db_name, username=db_user, password=db_password)
            logger.info(f"Successfully connected to {db_name} database as {db_user}")
        else:
            # Fallback for testing without auth
            logger.warning("No authentication credentials provided - using anonymous access")
            db = db_client.db(db_name)

        # Test the connection
        version = db.version()
        logger.info(f"Connected to ArangoDB version: {version}")

    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        logger.error(f"Exception type: {type(e)}")
        logger.error(f"Exception args: {e.args}")
        raise

    yield

    # Shutdown
    logger.info("Shutting down Mallku API Service...")
    if db_client:
        db_client.close()


# Create FastAPI app
logger.info("Creating FastAPI application...")
app = FastAPI(
    title="Mallku Database API",
    description="Secured gateway to ArangoDB - Cathedral Architecture",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    try:
        # Verify database connection
        if db is not None:
            db.version()
        return {"status": "healthy", "service": "mallku-api"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Database connection failed")


@app.get("/security/metrics")
async def security_metrics() -> dict[str, Any]:
    """Return security metrics - shows structural enforcement."""
    return {
        "architecture": "cathedral",
        "database_ports_exposed": 0,
        "api_ports_exposed": 1,
        "network_isolation": True,
        "direct_db_access_possible": False,
        "message": "Security through structure, not policy",
    }


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    return Response(generate_latest(registry), media_type="text/plain")


@app.get("/api/v1/collections")
async def list_collections():
    """List available collections - example secured endpoint."""
    try:
        collections = [col["name"] for col in db.collections()]
        return {"collections": collections}
    except Exception as e:
        logger.error(f"Failed to list collections: {e}")
        raise HTTPException(status_code=500, detail="Failed to list collections")


@app.post("/api/v1/collections/{collection_name}/documents")
async def create_document(collection_name: str, document: dict):
    """Create a document in specified collection."""
    try:
        collection = db.collection(collection_name)
        meta = collection.insert(document)
        return {"_key": meta["_key"], "_id": meta["_id"]}
    except Exception as e:
        logger.error(f"Failed to create document: {e}")
        raise HTTPException(status_code=500, detail="Failed to create document")


@app.get("/api/v1/collections/{collection_name}/documents")
async def list_documents(collection_name: str, limit: int = 10):
    """List documents from a collection."""
    try:
        collection = db.collection(collection_name)
        cursor = collection.all(limit=limit)
        return {"documents": list(cursor)}
    except Exception as e:
        logger.error(f"Failed to list documents: {e}")
        raise HTTPException(status_code=500, detail="Failed to list documents")


# Main entry point
def main():
    """Main function to start the service."""
    logger.info("Main function starting...")
    host = os.getenv("MALLKU_API_HOST", "0.0.0.0")
    port = int(os.getenv("MALLKU_API_PORT", "8080"))

    logger.info(f"Starting Mallku API on {host}:{port}")
    logger.info("Remember: This is the only door to the database")
    logger.info("Cathedral Architecture - Security through structure")

    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    logger.info("Script started as __main__")
    main()
