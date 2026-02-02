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

# Import FastAPI app
from main import app

# Export for Vercel
handler = app
