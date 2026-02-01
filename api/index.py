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

# Set working directory to parent
try:
    os.chdir(parent_dir)
except Exception:
    pass  # Continue if chdir fails

# Import FastAPI app
try:
    from main import app
    
    # Use Mangum adapter for AWS Lambda/Vercel compatibility
    try:
        from mangum import Mangum
        handler = Mangum(app, lifespan="off")
    except ImportError:
        # Fallback: use ASGI directly
        handler = app
except Exception as e:
    # Create minimal error handler if import fails
    from fastapi import FastAPI
    error_app = FastAPI()
    
    @error_app.get("/")
    async def error_root():
        return {"error": f"Import error: {str(e)}", "status": "error"}
    
    handler = error_app
