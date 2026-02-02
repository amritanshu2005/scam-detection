"""
Vercel Serverless Function Entry Point
Properly configured for Vercel's Python runtime with Mangum ASGI adapter
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

try:
    # Import and configure the app
    from main import app
    
    # Use Mangum to wrap FastAPI for serverless environment
    from mangum import Mangum
    
    # Create the handler that Vercel will call
    handler = Mangum(app, lifespan="off")
    
except ImportError as e:
    # If Mangum is not available, create a fallback
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    
    fallback_app = FastAPI()
    
    @fallback_app.get("/")
    async def fallback():
        return JSONResponse(
            status_code=503,
            content={
                "error": "Missing dependency",
                "details": f"Could not import: {str(e)}",
                "message": "Ensure mangum is in requirements.txt"
            }
        )
    
    from mangum import Mangum
    handler = Mangum(fallback_app, lifespan="off")
    
except Exception as e:
    # General error handler
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    
    error_app = FastAPI()
    
    @error_app.get("/")
    async def error_handler():
        return JSONResponse(
            status_code=500,
            content={
                "error": "Application initialization failed",
                "details": str(e),
                "type": type(e).__name__
            }
        )
    
    from mangum import Mangum
    handler = Mangum(error_app, lifespan="off")
