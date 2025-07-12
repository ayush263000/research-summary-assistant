#!/usr/bin/env python3
"""
Main entry point for the Document-Aware GenAI Assistant
"""

import os
import sys
import subprocess
from pathlib import Path

# Add the app directory to Python path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))

def run_streamlit():
    """Run the Streamlit frontend"""
    frontend_path = app_dir / "frontend" / "main.py"
    cmd = [
        sys.executable, "-m", "streamlit", "run", 
        str(frontend_path),
        "--server.port=8501",
        "--server.address=localhost"
    ]
    subprocess.run(cmd)

def run_fastapi():
    """Run the FastAPI backend (if needed separately)"""
    import uvicorn
    from app.api.main import app
    
    uvicorn.run(
        "app.api.main:app",
        host="localhost",
        port=8000,
        reload=True
    )

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--api-only":
        print("Starting FastAPI backend only..")
        run_fastapi()
    else:
        print("Starting Document-Aware GenAI Assistant...")
        print("Access the application at: http://localhost:8501")
        run_streamlit()
