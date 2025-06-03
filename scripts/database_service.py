#!/usr/bin/env python3
"""
Mallku Database Service - Secured Interface API

This service provides the ONLY authorized way to access the Mallku database.
It runs alongside ArangoDB in the container but prevents direct database access.

Philosophy: Cathedral stones must be perfectly placed - this service embodies
security through architecture, making bypassing the security model impossible.
"""

import asyncio
import logging
import os
import signal
import sys
from contextlib import asynccontextmanager
from typing import Any

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Add the Mallku path
sys.path.insert(0, '/opt/mallku')

from core.database.factory import get_secured_database
from core.database.secured_interface import SecurityViolationError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Pydantic models for API
class QueryRequest(BaseModel):
    query: str = Field(..., description="AQL query to execute")
    bind_vars: dict[str, Any] = Field(default_factory=dict, description="Query bind variables")
    collection_name: str | None = Field(None, description="Target collection name for security context")


class QueryResponse(BaseModel):
    success: bool
    data: list[dict] = Field(default_factory=list)
    error: str | None = None
    execution_time_ms: float | None = None


class SecurityMetricsResponse(BaseModel):
    operations_count: int
    security_violations: int
    registered_collections: int
    uuid_mappings: int
    recent_violations: list[str]


class HealthResponse(BaseModel):
    status: str
    database_connected: bool
    security_interface_initialized: bool
    uptime_seconds: float


# Global state
secured_db = None
startup_time = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown logic for the Mallku database service."""
    global secured_db, startup_time
    startup_time = asyncio.get_event_loop().time()

    try:
        logger.info("Initializing Mallku Database Service...")

        # Get secured database interface
        secured_db = await get_secured_database()
        await secured_db.initialize()

        logger.info("Mallku Database Service initialized successfully")
        logger.info("Security through architecture: Direct database access blocked")

        yield

    except Exception as e:
        logger.error(f"Failed to initialize database service: {e}")
        sys.exit(1)

    finally:
        logger.info("Shutting down Mallku Database Service")


# Create FastAPI app with lifespan
app = FastAPI(
    title="Mallku Secured Database Interface",
    description="The ONLY authorized way to access Mallku database - Security through Architecture",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for container monitoring."""
    global startup_time
    current_time = asyncio.get_event_loop().time()
    uptime = current_time - startup_time if startup_time else 0

    database_connected = secured_db is not None
    security_initialized = secured_db._initialized if secured_db else False

    status = "healthy" if database_connected and security_initialized else "degraded"

    return HealthResponse(
        status=status,
        database_connected=database_connected,
        security_interface_initialized=security_initialized,
        uptime_seconds=uptime
    )


@app.post("/query", response_model=QueryResponse)
async def execute_query(query_request: QueryRequest):
    """
    Execute AQL query through the secured interface.

    This is the primary way to interact with Mallku data while maintaining
    all security guarantees including field obfuscation and access control.
    """
    if not secured_db:
        raise HTTPException(status_code=503, detail="Database service not initialized")

    start_time = asyncio.get_event_loop().time()

    try:
        # Execute query through secured interface
        results = await secured_db.execute_secured_query(
            aql_query=query_request.query,
            bind_vars=query_request.bind_vars,
            collection_name=query_request.collection_name
        )

        end_time = asyncio.get_event_loop().time()
        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds

        logger.info(f"Query executed successfully, returned {len(results)} results in {execution_time:.2f}ms")

        return QueryResponse(
            success=True,
            data=results,
            execution_time_ms=execution_time
        )

    except SecurityViolationError as e:
        logger.warning(f"Security violation in query: {e}")
        raise HTTPException(status_code=403, detail=f"Security violation: {str(e)}")

    except Exception as e:
        logger.error(f"Query execution failed: {e}")
        raise HTTPException(status_code=400, detail=f"Query execution failed: {str(e)}")


@app.get("/security/metrics", response_model=SecurityMetricsResponse)
async def get_security_metrics():
    """Get security enforcement metrics for monitoring."""
    if not secured_db:
        raise HTTPException(status_code=503, detail="Database service not initialized")

    metrics = secured_db.get_security_metrics()

    return SecurityMetricsResponse(
        operations_count=metrics["operations_count"],
        security_violations=metrics["security_violations"],
        registered_collections=metrics["registered_collections"],
        uuid_mappings=metrics["uuid_mappings"],
        recent_violations=metrics["recent_violations"]
    )


@app.get("/security/collections")
async def list_secured_collections():
    """List all collections with their security policies."""
    if not secured_db:
        raise HTTPException(status_code=503, detail="Database service not initialized")

    policies = {}
    for name, policy in secured_db._collection_policies.items():
        policies[name] = {
            "requires_security": policy.requires_security,
            "allowed_model_types": [t.__name__ for t in policy.allowed_model_types],
            "has_schema_validation": bool(policy.schema_validation)
        }

    return {"collections": policies}


@app.exception_handler(SecurityViolationError)
async def security_violation_handler(request: Request, exc: SecurityViolationError):
    """Handle security violations with appropriate logging and response."""
    logger.error(f"Security violation from {request.client.host}: {exc}")
    return JSONResponse(
        status_code=403,
        content={
            "error": "Security Violation",
            "message": "This operation violates Mallku security policies",
            "detail": str(exc)
        }
    )


def setup_signal_handlers():
    """Setup graceful shutdown signal handlers."""
    def signal_handler(signum, frame):
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


if __name__ == "__main__":
    setup_signal_handlers()

    # Get configuration from environment
    host = os.getenv("MALLKU_API_HOST", "0.0.0.0")
    port = int(os.getenv("MALLKU_API_PORT", "8080"))

    logger.info(f"Starting Mallku Database Service on {host}:{port}")
    logger.info("Remember: This is cathedral work - built for those who come after us")

    # Run the service
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
        access_log=True
    )
