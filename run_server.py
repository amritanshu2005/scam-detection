#!/usr/bin/env python
"""Direct server launcher"""
import os
from dotenv import load_dotenv
import uvicorn

load_dotenv()

# Set environment variables
os.environ.setdefault("GROQ_API_KEY", "default-test-key")
os.environ.setdefault("API_KEY", "test-api-key-12345")

if __name__ == "__main__":
    from main import app
    
    print("Starting server on 0.0.0.0:8000...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        access_log=True
    )
