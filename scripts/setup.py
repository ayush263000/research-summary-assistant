#!/usr/bin/env python3
"""
Setup script for the Document-A        print("✅ Setup completed successfully!")
        print("\nNext steps:")
        print("1. Edit .env file with your Google API key")
        print("2. Run: python run.py")
        print("3. Access the app at: http://localhost:8501")GenAI Assistant
"""

import os
import sys
import subprocess
from pathlib import Path

def install_dependencies():
    """Install Python dependencies"""
    print("Installing Python dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def setup_environment():
    """Setup environment configuration"""
    print("Setting up environment...")
    
    # Create .env file if it doesn't exist
    if not Path(".env").exists():
        print("Creating .env file from template...")
        subprocess.check_call(["cp", ".env.example", ".env"])
        print("Please edit .env file with your Google API key")
    
    # Create data directories
    data_dirs = [
        "data",
        "data/uploads",
        "logs"
    ]
    
    for dir_path in data_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {dir_path}")

def run_tests():
    """Run the test suite"""
    print("Running tests...")
    try:
        subprocess.check_call([sys.executable, "-m", "pytest", "tests/", "-v"])
        print("All tests passed!")
    except subprocess.CalledProcessError:
        print("Some tests failed. Please check the output above.")

def main():
    """Main setup function"""
    print("Setting up Document-Aware GenAI Assistant...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        sys.exit(1)
    
    try:
        install_dependencies()
        setup_environment()
        
        print("\n✅ Setup completed successfully!")
        print("\nNext steps:")
        print("1. Edit .env file with your OpenAI API key")
        print("2. Run: python run.py")
        print("3. Access the app at: http://localhost:8501")
        
        # Optionally run tests
        response = input("\nRun tests? (y/n): ").lower().strip()
        if response == 'y':
            run_tests()
            
    except Exception as e:
        print(f"Setup failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
