"""
Vercel Serverless Function Entry Point
This file adapts FastAPI for Vercel's serverless environment
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

try:
    # Import FastAPI app
    from main import app
    # Export for Vercel
    handler = app
except Exception as e:
    # If import fails, create a minimal error handler
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    
    error_app = FastAPI()
    
    @error_app.get("/")
    async def error_handler():
        return JSONResponse(
            status_code=500,
            content={
                "error": "Failed to initialize application",
                "details": str(e),
                "message": "Check environment variables and dependencies"
            }
        )
    
    handler = error_app
