"""
Database models and configuration
"""

from sqlalchemy import create_engine, Column, String, Text, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

from ..utils.config import get_settings

# Get settings
settings = get_settings()

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

class DocumentModel(Base):
    """
    Database model for storing document metadata
    """
    __tablename__ = "documents"
    
    id = Column(String, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    content_preview = Column(Text)  # First few thousand characters
    chunk_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_processed = Column(Boolean, default=True)
    file_size = Column(Integer, default=0)
    content_type = Column(String, default="")

class SessionModel(Base):
    """
    Database model for storing user sessions (optional enhancement)
    """
    __tablename__ = "sessions"
    
    id = Column(String, primary_key=True, index=True)
    document_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)
    question_count = Column(Integer, default=0)
    challenge_count = Column(Integer, default=0)

class QuestionHistoryModel(Base):
    """
    Database model for storing question history (optional enhancement)
    """
    __tablename__ = "question_history"
    
    id = Column(String, primary_key=True, index=True)
    document_id = Column(String, nullable=False)
    session_id = Column(String)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    question_type = Column(String, default="freeform")  # freeform, challenge
    created_at = Column(DateTime, default=datetime.utcnow)
    response_time = Column(Integer, default=0)  # milliseconds

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables on import
create_tables()
