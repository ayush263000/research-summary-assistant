"""
Test configuration and fixtures
"""

import pytest
import asyncio
import tempfile
import shutil
from pathlib import Path
import os

# Set test environment
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["UPLOAD_DIR"] = "./test_uploads"
os.environ["GOOGLE_API_KEY"] = "test-key"

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests"""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path)

@pytest.fixture
def sample_txt_file(temp_dir):
    """Create a sample TXT file for testing"""
    content = """
    This is a sample document for testing purposes.
    It contains multiple paragraphs with different topics.
    
    The first topic discusses artificial intelligence and machine learning.
    These technologies are transforming various industries.
    
    The second topic covers document processing and analysis.
    Natural language processing enables computers to understand text.
    
    The conclusion summarizes the main points and provides insights.
    """
    
    file_path = temp_dir / "sample.txt"
    with open(file_path, 'w') as f:
        f.write(content)
    
    return file_path

@pytest.fixture
def mock_gemini_response():
    """Mock Google Gemini API response"""
    return {
        "text": "This is a mock response from Google Gemini API."
    }
