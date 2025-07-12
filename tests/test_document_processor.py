"""
Tests for document processor
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
from pathlib import Path

from app.core.document_processor import DocumentProcessor

class TestDocumentProcessor:
    """Test cases for DocumentProcessor"""
    
    @pytest.fixture
    def processor(self):
        """Create a DocumentProcessor instance"""
        return DocumentProcessor()
    
    def test_extract_txt_text(self, processor, sample_txt_file):
        """Test text extraction from TXT file"""
        content = processor._extract_txt_text(sample_txt_file)
        
        assert content is not None
        assert len(content) > 0
        assert "artificial intelligence" in content.lower()
        assert "document processing" in content.lower()
    
    def test_split_text(self, processor):
        """Test text splitting functionality"""
        sample_text = "This is a long document. " * 100
        chunks = processor._split_text(sample_text)
        
        assert len(chunks) > 0
        assert all(len(chunk.page_content) <= 1200 for chunk in chunks)  # chunk_size + overlap
    
    @pytest.mark.asyncio
    async def test_generate_summary(self, processor):
        """Test summary generation"""
        with patch('app.core.ai_client.AIClient.generate_summary') as mock_summary:
            mock_summary.return_value = "This is a test summary."
            
            # This test would need a real document ID in the database
            # For now, it's a placeholder for the structure
            pass
    
    def test_get_vector_store_nonexistent(self, processor):
        """Test getting vector store for non-existent document"""
        vector_store = processor.get_vector_store("nonexistent-id")
        assert vector_store is None
