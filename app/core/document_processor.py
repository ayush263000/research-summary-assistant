"""
Document processing module for handling PDF and TXT files
"""

import os
import uuid
from pathlib import Path
from typing import Optional, List, Dict, Any
import logging
from datetime import datetime

# PDF processing
import PyPDF2
from pdfminer.high_level import extract_text as extract_pdf_text
from pdfminer.layout import LAParams

# Text processing and embeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Database
from ..models.database import DocumentModel, SessionLocal
from ..utils.config import get_settings

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """
    Handles document upload, processing, and storage
    """
    
    def __init__(self):
        self.settings = get_settings()
        self.upload_dir = Path(self.settings.UPLOAD_DIR)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        # Initialize embeddings
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=self.settings.GOOGLE_API_KEY
        )
        
    async def process_document(self, file) -> str:
        """
        Process uploaded document and return document ID
        
        Args:
            file: Uploaded file object
            
        Returns:
            str: Unique document ID
        """
        try:
            # Generate unique document ID
            doc_id = str(uuid.uuid4())
            
            # Save file
            file_path = self.upload_dir / f"{doc_id}_{file.filename}"
            
            # Read and save file content
            content = await file.read()
            with open(file_path, "wb") as f:
                f.write(content)
            
            # Extract text based on file type
            if file.filename.lower().endswith('.pdf'):
                text_content = self._extract_pdf_text(file_path)
            else:  # .txt
                text_content = self._extract_txt_text(file_path)
            
            # Split text into chunks
            chunks = self._split_text(text_content)
            
            # Create vector store
            vector_store = await self._create_vector_store(doc_id, chunks)
            
            # Save document metadata to database
            await self._save_document_metadata(
                doc_id=doc_id,
                filename=file.filename,
                file_path=str(file_path),
                content=text_content[:5000],  # Store first 5000 chars
                chunk_count=len(chunks)
            )
            
            logger.info(f"Document processed successfully: {doc_id}")
            return doc_id
            
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            raise
    
    def _extract_pdf_text(self, file_path: Path) -> str:
        """Extract text from PDF file"""
        try:
            # Try pdfminer first (better for complex layouts)
            text = extract_pdf_text(str(file_path), laparams=LAParams())
            
            if not text.strip():
                # Fallback to PyPDF2
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"Error extracting PDF text: {str(e)}")
            raise
    
    def _extract_txt_text(self, file_path: Path) -> str:
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            # Try with different encoding
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read()
    
    def _split_text(self, text: str) -> List[Document]:
        """Split text into chunks for vector storage"""
        chunks = self.text_splitter.split_text(text)
        documents = []
        
        for i, chunk in enumerate(chunks):
            doc = Document(
                page_content=chunk,
                metadata={"chunk_id": i, "source": "document"}
            )
            documents.append(doc)
        
        return documents
    
    async def _create_vector_store(self, doc_id: str, chunks: List[Document]) -> Chroma:
        """Create vector store for document chunks"""
        try:
            vector_store_path = self.upload_dir / f"vector_store_{doc_id}"
            
            vector_store = Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                persist_directory=str(vector_store_path)
            )
            
            vector_store.persist()
            return vector_store
            
        except Exception as e:
            logger.error(f"Error creating vector store: {str(e)}")
            raise
    
    async def _save_document_metadata(self, doc_id: str, filename: str, 
                                    file_path: str, content: str, chunk_count: int):
        """Save document metadata to database"""
        try:
            db = SessionLocal()
            
            document = DocumentModel(
                id=doc_id,
                filename=filename,
                file_path=file_path,
                content_preview=content,
                chunk_count=chunk_count,
                created_at=datetime.utcnow()
            )
            
            db.add(document)
            db.commit()
            db.close()
            
        except Exception as e:
            logger.error(f"Error saving document metadata: {str(e)}")
            raise
    
    async def generate_summary(self, doc_id: str) -> str:
        """
        Generate auto-summary for the document
        
        Args:
            doc_id: Document ID
            
        Returns:
            str: Document summary (≤150 words)
        """
        try:
            from ..core.ai_client import AIClient
            
            # Get document content
            db = SessionLocal()
            document = db.query(DocumentModel).filter(DocumentModel.id == doc_id).first()
            db.close()
            
            if not document:
                raise ValueError(f"Document not found: {doc_id}")
            
            # Read full content
            with open(document.file_path, 'r', encoding='utf-8') as f:
                if document.filename.lower().endswith('.pdf'):
                    content = self._extract_pdf_text(Path(document.file_path))
                else:
                    content = f.read()
            
            # Generate summary using AI
            ai_client = AIClient()
            summary = await ai_client.generate_summary(content)
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            raise
    
    def get_vector_store(self, doc_id: str) -> Optional[Chroma]:
        """Get vector store for a document"""
        try:
            vector_store_path = self.upload_dir / f"vector_store_{doc_id}"
            
            if not vector_store_path.exists():
                return None
            
            vector_store = Chroma(
                persist_directory=str(vector_store_path),
                embedding_function=self.embeddings
            )
            
            return vector_store
            
        except Exception as e:
            logger.error(f"Error loading vector store: {str(e)}")
            return None
    
    async def list_documents(self) -> List[Dict[str, Any]]:
        """List all processed documents"""
        try:
            db = SessionLocal()
            documents = db.query(DocumentModel).all()
            db.close()
            
            return [
                {
                    "id": doc.id,
                    "filename": doc.filename,
                    "created_at": doc.created_at.isoformat(),
                    "chunk_count": doc.chunk_count
                }
                for doc in documents
            ]
            
        except Exception as e:
            logger.error(f"Error listing documents: {str(e)}")
            raise
