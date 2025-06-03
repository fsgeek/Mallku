#!/usr/bin/env python3
"""
Minimal database service for Docker container.
Just enough to get the container running.
"""

import uvicorn
from fastapi import FastAPI

app = FastAPI(title="Mallku Database API")

@app.get("/health")
def health_check():
    """Basic health check endpoint"""
    return {"status": "healthy", "service": "mallku-database"}

@app.get("/")
def root():
    """Root endpoint"""
    return {"message": "Mallku Database API", "version": "0.1.0-minimal"}

if __name__ == "__main__":
    # Run the API server
    uvicorn.run(app, host="0.0.0.0", port=8080)
