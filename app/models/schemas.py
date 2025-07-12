"""
Pydantic schemas for API request/response models
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime

class DocumentUpload(BaseModel):
    """Schema for document upload"""
    filename: str
    content_type: str

class DocumentResponse(BaseModel):
    """Schema for document processing response"""
    document_id: str
    filename: str
    summary: str
    status: str
    created_at: Optional[datetime] = None

class QuestionRequest(BaseModel):
    """Schema for Q&A request"""
    document_id: str
    question: str = Field(..., min_length=5, max_length=1000)

class AnswerResponse(BaseModel):
    """Schema for Q&A response"""
    answer: str
    references: List[str] = []
    confidence: float = Field(ge=0.0, le=1.0)
    source_chunks: Optional[List[str]] = None

class ChallengeRequest(BaseModel):
    """Schema for challenge question generation request"""
    document_id: str
    difficulty: str = Field(default="medium", regex="^(easy|medium|hard)$")
    num_questions: int = Field(default=3, ge=1, le=10)

class ChallengeQuestion(BaseModel):
    """Schema for a single challenge question"""
    id: str
    question: str
    options: List[str]
    correct_answer: str
    explanation: Optional[str] = None
    difficulty: str
    type: str = "multiple_choice"

class ChallengeResponse(BaseModel):
    """Schema for challenge questions response"""
    questions: List[ChallengeQuestion]

class EvaluationRequest(BaseModel):
    """Schema for answer evaluation request"""
    document_id: str
    question: str
    user_answer: str
    correct_answer: Optional[str] = None

class EvaluationResponse(BaseModel):
    """Schema for answer evaluation response"""
    score: int = Field(ge=0, le=100)
    feedback: str
    references: List[str] = []
    correct_answer: str
    is_correct: bool

class DocumentListResponse(BaseModel):
    """Schema for document list response"""
    documents: List[dict]

class HealthResponse(BaseModel):
    """Schema for health check response"""
    status: str
    version: str
    timestamp: datetime

class ErrorResponse(BaseModel):
    """Schema for error responses"""
    error: str
    detail: Optional[str] = None
    timestamp: datetime
