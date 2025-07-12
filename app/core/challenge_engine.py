"""
Challenge Engine for generating and evaluating comprehension questions
"""

from typing import List, Dict, Any, Optional
import logging
from dataclasses import dataclass

from .ai_client import AIClient
from .document_processor import DocumentProcessor
from ..models.database import SessionLocal, DocumentModel

logger = logging.getLogger(__name__)

@dataclass
class ChallengeQuestion:
    """Challenge question data structure"""
    id: str
    question: str
    options: List[str]
    correct_answer: str
    explanation: str
    difficulty: str
    type: str = "multiple_choice"

@dataclass
class EvaluationResult:
    """Evaluation result for user answers"""
    score: int
    feedback: str
    references: List[str]
    correct_answer: str
    is_correct: bool

class ChallengeEngine:
    """
    Engine for generating comprehension questions and evaluating answers
    """
    
    def __init__(self):
        self.ai_client = AIClient()
        self.doc_processor = DocumentProcessor()
    
    async def generate_questions(self, document_id: str, difficulty: str = "medium", 
                               num_questions: int = 3) -> List[ChallengeQuestion]:
        """
        Generate challenge questions based on document content
        
        Args:
            document_id: ID of the document
            difficulty: Question difficulty (easy, medium, hard)
            num_questions: Number of questions to generate
            
        Returns:
            List of ChallengeQuestion objects
        """
        try:
            # Get document content
            content = await self._get_document_content(document_id)
            
            if not content:
                raise ValueError(f"Document not found or empty: {document_id}")
            
            # Generate questions using AI
            raw_questions = await self.ai_client.generate_challenge_questions(
                content=content,
                difficulty=difficulty,
                num_questions=num_questions
            )
            
            # Convert to ChallengeQuestion objects
            questions = []
            for i, q in enumerate(raw_questions):
                question = ChallengeQuestion(
                    id=f"{document_id}_{i+1}",
                    question=q.get("question", ""),
                    options=q.get("options", []),
                    correct_answer=q.get("correct_answer", ""),
                    explanation=q.get("explanation", ""),
                    difficulty=difficulty,
                    type=q.get("type", "multiple_choice")
                )
                questions.append(question)
            
            logger.info(f"Generated {len(questions)} challenge questions")
            return questions
            
        except Exception as e:
            logger.error(f"Error generating questions: {str(e)}")
            raise
    
    async def evaluate_answer(self, document_id: str, question: str, 
                            user_answer: str, correct_answer: Optional[str] = None) -> EvaluationResult:
        """
        Evaluate user's answer to a challenge question
        
        Args:
            document_id: Document ID
            question: The question asked
            user_answer: User's provided answer
            correct_answer: Correct answer (if known)
            
        Returns:
            EvaluationResult with score and feedback
        """
        try:
            # Get document content for context
            content = await self._get_document_content(document_id)
            
            if not content:
                raise ValueError(f"Document not found: {document_id}")
            
            # Use AI to evaluate the answer
            evaluation = await self.ai_client.evaluate_answer(
                question=question,
                user_answer=user_answer,
                correct_answer=correct_answer or "",
                context=content
            )
            
            # Determine if answer is correct
            is_correct = False
            if correct_answer:
                is_correct = self._compare_answers(user_answer, correct_answer)
            
            return EvaluationResult(
                score=evaluation.get("score", 0),
                feedback=evaluation.get("feedback", ""),
                references=evaluation.get("references", []),
                correct_answer=evaluation.get("correct_answer", correct_answer or ""),
                is_correct=is_correct
            )
            
        except Exception as e:
            logger.error(f"Error evaluating answer: {str(e)}")
            raise
    
    async def _get_document_content(self, document_id: str) -> Optional[str]:
        """
        Get full content of a document
        
        Args:
            document_id: Document ID
            
        Returns:
            Document content or None if not found
        """
        try:
            db = SessionLocal()
            document = db.query(DocumentModel).filter(DocumentModel.id == document_id).first()
            db.close()
            
            if not document:
                return None
            
            # Read full content from file
            if document.filename.lower().endswith('.pdf'):
                content = self.doc_processor._extract_pdf_text(document.file_path)
            else:
                with open(document.file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            
            return content
            
        except Exception as e:
            logger.error(f"Error getting document content: {str(e)}")
            return None
    
    def _compare_answers(self, user_answer: str, correct_answer: str) -> bool:
        """
        Compare user answer with correct answer
        
        Args:
            user_answer: User's answer
            correct_answer: Correct answer
            
        Returns:
            True if answers match
        """
        # Simple comparison (can be made more sophisticated)
        user_clean = user_answer.strip().lower()
        correct_clean = correct_answer.strip().lower()
        
        return user_clean == correct_clean
    
    async def get_question_statistics(self, document_id: str) -> Dict[str, Any]:
        """
        Get statistics about questions generated for a document
        
        Args:
            document_id: Document ID
            
        Returns:
            Statistics dictionary
        """
        try:
            # This could be enhanced to track actual usage statistics
            # For now, return basic document info
            db = SessionLocal()
            document = db.query(DocumentModel).filter(DocumentModel.id == document_id).first()
            db.close()
            
            if not document:
                return {}
            
            return {
                "document_id": document_id,
                "filename": document.filename,
                "chunk_count": document.chunk_count,
                "created_at": document.created_at.isoformat(),
                "suitable_for_questions": document.chunk_count >= 3  # Minimum chunks for good questions
            }
            
        except Exception as e:
            logger.error(f"Error getting question statistics: {str(e)}")
            return {}
