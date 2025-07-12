"""
AI Client for interacting with Google Gemini models
"""

import google.generativeai as genai
from typing import List, Dict, Any, Optional
import logging
from dataclasses import dataclass

from ..utils.config import get_settings

logger = logging.getLogger(__name__)

@dataclass
class AIResponse:
    """Response from AI model"""
    text: str
    confidence: float = 0.0
    references: List[str] = None
    
    def __post_init__(self):
        if self.references is None:
            self.references = []

class AIClient:
    """
    Client for interacting with Google Gemini API
    """
    
    def __init__(self):
        self.settings = get_settings()
        genai.configure(api_key=self.settings.GOOGLE_API_KEY)
        self.model_name = self.settings.GEMINI_MODEL
        self.max_tokens = self.settings.MAX_TOKENS
        self.temperature = self.settings.TEMPERATURE
        
        # Initialize the model
        self.model = genai.GenerativeModel(self.model_name)
        
        # Rate limiting for free tier
        self.last_request_time = 0
        self.min_request_interval = 4  # 4 seconds between requests (15 requests/minute limit)
    
    def _wait_for_rate_limit(self):
        """Ensure we don't exceed rate limits"""
        import time
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)
        self.last_request_time = time.time()
    
    async def generate_summary(self, content: str) -> str:
        """
        Generate a summary of the document content (≤150 words)
        
        Args:
            content: Full document content
            
        Returns:
            str: Summary text
        """
        try:
            # Rate limiting
            self._wait_for_rate_limit()
            
            # Truncate content if too long
            max_content_length = 8000  # Leave room for prompt
            if len(content) > max_content_length:
                content = content[:max_content_length] + "..."
            
            prompt = f"""
            Please provide a concise summary of the following document in exactly 150 words or less. 
            Focus on the main themes, key findings, and important conclusions.
            
            Document content:
            {content}
            
            Summary (≤150 words):
            """
            
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=200,  # Limit for summary
                    temperature=0.3,
                    top_p=0.8,
                    top_k=40
                )
            )
            
            summary = response.text.strip()
            return summary
            
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            raise
    
    async def answer_question(self, question: str, context_chunks: List[str]) -> AIResponse:
        """
        Answer a question based on document context
        
        Args:
            question: User's question
            context_chunks: Relevant document chunks
            
        Returns:
            AIResponse: Answer with references
        """
        try:
            # Rate limiting
            self._wait_for_rate_limit()
            
            # Combine context chunks
            context = "\n\n".join([f"[Chunk {i+1}]: {chunk}" for i, chunk in enumerate(context_chunks)])
            
            prompt = f"""
            Based on the following document context, please answer the user's question. 
            
            IMPORTANT RULES:
            1. Only use information from the provided context
            2. If the answer cannot be found in the context, say "I cannot find this information in the document"
            3. Include specific references to which chunks contain the relevant information
            4. Be precise and factual
            
            Context:
            {context}
            
            Question: {question}
            
            Answer:
            """
            
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=self.max_tokens,
                    temperature=self.temperature,
                    top_p=0.9,
                    top_k=40
                )
            )
            
            answer_text = response.text.strip()
            
            # Extract references (simplified)
            references = self._extract_references(answer_text, len(context_chunks))
            
            return AIResponse(
                text=answer_text,
                confidence=0.8,  # Could be calculated based on response
                references=references
            )
            
        except Exception as e:
            logger.error(f"Error answering question: {str(e)}")
            raise
    
    async def generate_challenge_questions(self, content: str, difficulty: str = "medium", 
                                         num_questions: int = 3) -> List[Dict[str, Any]]:
        """
        Generate challenge questions based on document content
        
        Args:
            content: Document content
            difficulty: Question difficulty (easy, medium, hard)
            num_questions: Number of questions to generate
            
        Returns:
            List of question dictionaries
        """
        try:
            # Truncate content if too long
            max_content_length = 6000
            if len(content) > max_content_length:
                content = content[:max_content_length] + "..."
            
            prompt = f"""
            Based on the following document, create {num_questions} {difficulty} level comprehension questions.
            
            Each question should:
            1. Test understanding of key concepts
            2. Require reasoning about the content
            3. Have 4 multiple choice options (A, B, C, D)
            4. Include the correct answer
            5. Be challenging but fair
            
            Document content:
            {content}
            
            Generate questions in this format:
            Question 1: [Question text]
            A) [Option A]
            B) [Option B]
            C) [Option C]
            D) [Option D]
            Correct: [A/B/C/D]
            Explanation: [Brief explanation]
            
            Questions:
            """
            
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=self.max_tokens,
                    temperature=0.7,
                    top_p=0.9,
                    top_k=40
                )
            )
            
            questions_text = response.text.strip()
            questions = self._parse_challenge_questions(questions_text)
            
            return questions[:num_questions]  # Ensure we don't exceed requested number
            
        except Exception as e:
            logger.error(f"Error generating challenge questions: {str(e)}")
            raise
    
    async def evaluate_answer(self, question: str, user_answer: str, 
                            correct_answer: str, context: str) -> Dict[str, Any]:
        """
        Evaluate user's answer to a challenge question
        
        Args:
            question: The question asked
            user_answer: User's answer
            correct_answer: Correct answer
            context: Document context
            
        Returns:
            Evaluation results
        """
        try:
            prompt = f"""
            Evaluate the user's answer to this question based on the document context.
            
            Question: {question}
            User's Answer: {user_answer}
            Correct Answer: {correct_answer}
            
            Document Context:
            {context[:2000]}...
            
            Please provide:
            1. Score (0-100)
            2. Detailed feedback explaining why the answer is correct/incorrect
            3. Key references from the document that support the correct answer
            
            Evaluation:
            """
            
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=500,
                    temperature=0.2,
                    top_p=0.8,
                    top_k=40
                )
            )
            
            evaluation_text = response.text.strip()
            
            # Parse evaluation (simplified)
            score = 100 if user_answer.lower() == correct_answer.lower() else 0
            
            return {
                "score": score,
                "feedback": evaluation_text,
                "references": [],  # Could extract references from evaluation
                "correct_answer": correct_answer
            }
            
        except Exception as e:
            logger.error(f"Error evaluating answer: {str(e)}")
            raise
    
    def _extract_references(self, text: str, num_chunks: int) -> List[str]:
        """Extract chunk references from AI response"""
        references = []
        for i in range(1, num_chunks + 1):
            if f"Chunk {i}" in text or f"chunk {i}" in text:
                references.append(f"Reference: Document chunk {i}")
        return references
    
    def _parse_challenge_questions(self, questions_text: str) -> List[Dict[str, Any]]:
        """Parse generated questions into structured format"""
        questions = []
        lines = questions_text.split('\n')
        
        current_question = {}
        options = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('Question'):
                if current_question:
                    current_question['options'] = options
                    questions.append(current_question)
                
                current_question = {
                    'question': line.split(':', 1)[1].strip() if ':' in line else line,
                    'type': 'multiple_choice',
                    'options': [],
                    'correct_answer': '',
                    'explanation': ''
                }
                options = []
            
            elif line.startswith(('A)', 'B)', 'C)', 'D)')):
                options.append(line[2:].strip())
            
            elif line.startswith('Correct:'):
                current_question['correct_answer'] = options[ord(line.split(':')[1].strip()) - ord('A')] if options else line.split(':')[1].strip()
            
            elif line.startswith('Explanation:'):
                current_question['explanation'] = line.split(':', 1)[1].strip()
        
        # Add last question
        if current_question:
            current_question['options'] = options
            questions.append(current_question)
        
        return questions
