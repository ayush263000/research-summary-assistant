"""
FastAPI backend for the Document-Aware GenAI Assistant
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from typing import List, Optional
import logging

from ..core.document_processor import DocumentProcessor
from ..core.qa_engine import QAEngine
from ..core.challenge_engine import ChallengeEngine
from ..models.schemas import (
    DocumentResponse, 
    QuestionRequest, 
    AnswerResponse,
    ChallengeRequest,
    EvaluationResponse
)
from ..utils.config import get_settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Document-Aware GenAI Assistant API",
    description="API for document analysis and Q&A",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize core components
settings = get_settings()
doc_processor = DocumentProcessor()
qa_engine = QAEngine()
challenge_engine = ChallengeEngine()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "1.0.0"}

@app.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and process a document (PDF/TXT)
    Returns auto-summary and document metadata
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith(('.pdf', '.txt')):
            raise HTTPException(
                status_code=400, 
                detail="Only PDF and TXT files are supported"
            )
        
        # Process document
        doc_id = await doc_processor.process_document(file)
        summary = await doc_processor.generate_summary(doc_id)
        
        return DocumentResponse(
            document_id=doc_id,
            filename=file.filename,
            summary=summary,
            status="processed"
        )
        
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """
    Ask a free-form question about the document
    """
    try:
        answer = await qa_engine.answer_question(
            document_id=request.document_id,
            question=request.question
        )
        
        return AnswerResponse(
            answer=answer.text,
            references=answer.references,
            confidence=answer.confidence
        )
        
    except Exception as e:
        logger.error(f"Error answering question: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/challenge", response_model=dict)
async def generate_challenge(request: ChallengeRequest):
    """
    Generate challenge questions for the document
    """
    try:
        questions = await challenge_engine.generate_questions(
            document_id=request.document_id,
            difficulty=request.difficulty,
            num_questions=request.num_questions
        )
        
        return {"questions": questions}
        
    except Exception as e:
        logger.error(f"Error generating challenge: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/evaluate", response_model=EvaluationResponse)
async def evaluate_answer(request: dict):
    """
    Evaluate user's answer to a challenge question
    """
    try:
        evaluation = await challenge_engine.evaluate_answer(
            document_id=request["document_id"],
            question=request["question"],
            user_answer=request["user_answer"],
            correct_answer=request.get("correct_answer")
        )
        
        return EvaluationResponse(
            score=evaluation.score,
            feedback=evaluation.feedback,
            references=evaluation.references,
            correct_answer=evaluation.correct_answer
        )
        
    except Exception as e:
        logger.error(f"Error evaluating answer: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents")
async def list_documents():
    """
    List all processed documents
    """
    try:
        documents = await doc_processor.list_documents()
        return {"documents": documents}
        
    except Exception as e:
        logger.error(f"Error listing documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
