"""
Q&A Engine for handling free-form questions about documents
"""

from typing import List, Optional
import logging
from dataclasses import dataclass

from .ai_client import AIClient, AIResponse
from .document_processor import DocumentProcessor
from ..models.database import SessionLocal, DocumentModel

logger = logging.getLogger(__name__)

@dataclass
class QAResult:
    """Result from Q&A processing"""
    text: str
    references: List[str]
    confidence: float
    source_chunks: List[str]

class QAEngine:
    """
    Engine for processing free-form questions about documents
    """
    
    def __init__(self):
        self.ai_client = AIClient()
        self.doc_processor = DocumentProcessor()
    
    async def answer_question(self, document_id: str, question: str) -> QAResult:
        """
        Answer a question about a specific document
        
        Args:
            document_id: ID of the document to query
            question: User's question
            
        Returns:
            QAResult: Answer with references and metadata
        """
        try:
            # Get relevant document chunks
            relevant_chunks = await self._get_relevant_chunks(document_id, question)
            
            if not relevant_chunks:
                return QAResult(
                    text="I couldn't find relevant information in the document to answer your question.",
                    references=[],
                    confidence=0.0,
                    source_chunks=[]
                )
            
            # Get AI response
            ai_response = await self.ai_client.answer_question(question, relevant_chunks)
            
            # Process references
            processed_references = self._process_references(relevant_chunks, document_id)
            
            return QAResult(
                text=ai_response.text,
                references=processed_references,
                confidence=ai_response.confidence,
                source_chunks=relevant_chunks
            )
            
        except Exception as e:
            logger.error(f"Error answering question: {str(e)}")
            raise
    
    async def _get_relevant_chunks(self, document_id: str, question: str, 
                                 top_k: int = 5) -> List[str]:
        """
        Retrieve relevant document chunks for the question
        
        Args:
            document_id: Document ID
            question: User's question
            top_k: Number of chunks to retrieve
            
        Returns:
            List of relevant text chunks
        """
        try:
            # Get vector store for the document
            vector_store = self.doc_processor.get_vector_store(document_id)
            
            if not vector_store:
                logger.warning(f"No vector store found for document: {document_id}")
                return []
            
            # Perform similarity search
            docs = vector_store.similarity_search(
                query=question,
                k=top_k
            )
            
            # Extract text content
            chunks = [doc.page_content for doc in docs]
            
            logger.info(f"Retrieved {len(chunks)} relevant chunks for question")
            return chunks
            
        except Exception as e:
            logger.error(f"Error retrieving relevant chunks: {str(e)}")
            return []
    
    def _process_references(self, chunks: List[str], document_id: str) -> List[str]:
        """
        Process chunks into readable references
        
        Args:
            chunks: Retrieved text chunks
            document_id: Document ID
            
        Returns:
            List of formatted references
        """
        references = []
        
        for i, chunk in enumerate(chunks):
            # Create reference with snippet
            snippet = chunk[:100] + "..." if len(chunk) > 100 else chunk
            reference = f"Document section {i+1}: \"{snippet}\""
            references.append(reference)
        
        return references
    
    async def get_document_info(self, document_id: str) -> Optional[dict]:
        """
        Get basic information about a document
        
        Args:
            document_id: Document ID
            
        Returns:
            Document information or None if not found
        """
        try:
            db = SessionLocal()
            document = db.query(DocumentModel).filter(DocumentModel.id == document_id).first()
            db.close()
            
            if not document:
                return None
            
            return {
                "id": document.id,
                "filename": document.filename,
                "created_at": document.created_at.isoformat(),
                "chunk_count": document.chunk_count
            }
            
        except Exception as e:
            logger.error(f"Error getting document info: {str(e)}")
            return None
