"""
Streamlit frontend for the Document-Aware GenAI Assistant
"""

import streamlit as st
import requests
import os
from typing import Optional
import time
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Document-Aware GenAI Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 2rem;
    }
    .upload-section {
        background-color: #f8fafc;
        padding: 2rem;
        border-radius: 0.5rem;
        border: 1px solid #e2e8f0;
    }
    .qa-section {
        margin-top: 2rem;
    }
    .reference-box {
        background-color: #f1f5f9;
        color: #1e293b;
        padding: 1rem;
        border-left: 4px solid #3b82f6;
        margin: 1rem 0;
        border-radius: 0.375rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }
    .challenge-mode {
        background-color: #fef3c7;
        padding: 2rem;
        border-radius: 0.5rem;
        border: 1px solid #f59e0b;
    }
    .document-summary {
        background-color: #e0f2fe;
        color: #0f172a;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #0891b2;
        margin: 1rem 0;
        font-size: 1rem;
        line-height: 1.6;
    }
    .summary-header {
        color: #0f766e;
        font-weight: 600;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'document_id' not in st.session_state:
    st.session_state.document_id = None
if 'document_summary' not in st.session_state:
    st.session_state.document_summary = None
if 'document_content' not in st.session_state:
    st.session_state.document_content = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'challenge_questions' not in st.session_state:
    st.session_state.challenge_questions = []
if 'current_challenge' not in st.session_state:
    st.session_state.current_challenge = None

def main():
    """Main application interface"""
    
    # Header
    st.markdown('<h1 class="main-header">📚 Document-Aware GenAI Assistant</h1>', 
                unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("Navigation")
        mode = st.radio(
            "Select Mode:",
            ["📄 Upload Document", "❓ Ask Anything", "🎯 Challenge Me"],
            index=0
        )
        
        # Document status
        if st.session_state.document_id:
            st.success("✅ Document loaded")
            st.info(f"Document ID: {st.session_state.document_id[:8]}...")
        else:
            st.warning("⚠️ No document loaded")
    
    # Main content based on selected mode
    if mode == "📄 Upload Document":
        upload_document_section()
    elif mode == "❓ Ask Anything":
        ask_anything_section()
    elif mode == "🎯 Challenge Me":
        challenge_me_section()

def upload_document_section():
    """Document upload interface"""
    
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.header("Upload Your Document")
    st.write("Upload a PDF or TXT file to get started with AI-powered document analysis.")
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['pdf', 'txt'],
        help="Upload PDF or TXT files up to 50MB"
    )
    
    if uploaded_file is not None:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.info(f"📁 File: {uploaded_file.name}")
            st.info(f"📊 Size: {uploaded_file.size / 1024:.1f} KB")
        
        with col2:
            if st.button("🚀 Process Document", type="primary"):
                process_document(uploaded_file)
    
    # Display document summary if available
    if st.session_state.document_summary:
        st.markdown('<h3 class="summary-header">📋 Document Summary</h3>', unsafe_allow_html=True)
        st.markdown(f'<div class="document-summary">{st.session_state.document_summary}</div>', 
                   unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def ask_anything_section():
    """Free-form Q&A interface"""
    
    if not st.session_state.document_id:
        st.warning("⚠️ Please upload a document first!")
        return
    
    st.header("Ask Anything About Your Document")
    st.write("Ask any question about the uploaded document. The AI will provide contextual answers with references.")
    
    # Question input
    question = st.text_area(
        "Your Question:",
        placeholder="e.g., What are the main conclusions of this research?",
        height=100
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🔍 Ask Question", type="primary"):
            if question.strip():
                ask_question(question)
            else:
                st.warning("⚠️ Please enter a question first!")
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown("### 💬 Conversation History")
        # Reverse the order to show latest question first
        reversed_history = list(reversed(st.session_state.chat_history))
        
        for i, (q, a, refs) in enumerate(reversed_history):
            # Calculate original question number for display
            original_index = len(st.session_state.chat_history) - i
            
            # Auto-expand the most recent question (first in reversed list)
            is_expanded = (i == 0)
            
            with st.expander(f"Q{original_index}: {q[:50]}...", expanded=is_expanded):
                st.markdown(f"**Question:** {q}")
                st.markdown(f"**Answer:** {a}")
                if refs:
                    st.markdown("**References:**")
                    for ref in refs:
                        st.markdown(f'<div class="reference-box">📍 {ref}</div>', 
                                   unsafe_allow_html=True)

def challenge_me_section():
    """Challenge mode interface"""
    
    if not st.session_state.document_id:
        st.warning("⚠️ Please upload a document first!")
        return
    
    st.markdown('<div class="challenge-mode">', unsafe_allow_html=True)
    st.header("🎯 Challenge Me Mode")
    st.write("Test your understanding with AI-generated questions based on the document content.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        difficulty = st.selectbox(
            "Difficulty Level:",
            ["Easy", "Medium", "Hard"],
            index=1
        )
    
    with col2:
        num_questions = st.selectbox(
            "Number of Questions:",
            [1, 3, 5, 10],
            index=1
        )
    
    if st.button("🎲 Generate Challenge Questions", type="primary"):
        generate_challenge_questions(difficulty.lower(), num_questions)
    
    # Display current challenge
    if st.session_state.challenge_questions:
        display_challenge_questions()
    
    st.markdown('</div>', unsafe_allow_html=True)

def process_document(uploaded_file):
    """Process uploaded document"""
    
    with st.spinner("🔄 Processing document..."):
        try:
            import google.generativeai as genai
            import os
            from pathlib import Path
            
            # Configure Gemini
            api_key = os.getenv('GOOGLE_API_KEY')
            if not api_key:
                st.error("❌ Please set your GOOGLE_API_KEY in the .env file")
                return
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Read file content
            content = ""
            if uploaded_file.name.lower().endswith('.txt'):
                content = str(uploaded_file.read(), 'utf-8')
            elif uploaded_file.name.lower().endswith('.pdf'):
                # Process PDF using PyPDF2
                import PyPDF2
                import io
                
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.getvalue()))
                content = ""
                for page in pdf_reader.pages:
                    content += page.extract_text() + "\n"
                
                if not content.strip():
                    st.warning("⚠️ Could not extract text from PDF. The PDF might be image-based.")
                    content = f"PDF file uploaded: {uploaded_file.name} ({len(uploaded_file.getvalue())} bytes) - Text extraction failed"
            
            # Show content extraction feedback
            if content:
                st.info(f"📄 Content extracted: {len(content)} characters")
            
            # Generate summary using Gemini
            summary_prompt = f"""
            Please provide a concise summary of the following document in exactly 150 words or less. 
            Focus on the main themes, key findings, and important conclusions.
            
            Document content:
            {content[:4000]}...
            
            Summary (≤150 words):
            """
            
            response = model.generate_content(summary_prompt)
            summary = response.text.strip()
            
            # Generate document ID and store
            import uuid
            doc_id = str(uuid.uuid4())
            
            st.session_state.document_id = doc_id
            st.session_state.document_summary = summary
            st.session_state.document_content = content
            
            st.success("✅ Document processed successfully!")
            time.sleep(1)
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Error processing document: {str(e)}")
            import traceback
            st.error(f"Details: {traceback.format_exc()}")

def ask_question(question):
    """Ask a question about the document"""
    
    with st.spinner("🤔 Thinking..."):
        try:
            import google.generativeai as genai
            import os
            
            # Configure Gemini
            api_key = os.getenv('GOOGLE_API_KEY')
            if not api_key:
                st.error("❌ Please set your GOOGLE_API_KEY in the .env file")
                return
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Get document content from session state
            content = st.session_state.get('document_content', '')
            
            # Create Q&A prompt
            qa_prompt = f"""
            Based on the following document context, please answer the user's question. 
            
            IMPORTANT RULES:
            1. Only use information from the provided context
            2. If the answer cannot be found in the context, say "I cannot find this information in the document"
            3. Include specific references to relevant parts of the document
            4. Be precise and factual
            
            Document Content:
            {content[:6000]}...
            
            Question: {question}
            
            Answer:
            """
            
            response = model.generate_content(qa_prompt)
            answer = response.text.strip()
            
            # Generate references (simplified)
            references = [
                "Document content: Direct reference to uploaded document",
                "Analysis: Based on document context and content"
            ]
            
            st.session_state.chat_history.append((question, answer, references))
            st.success("✅ Question answered!")
            time.sleep(1)
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Error asking question: {str(e)}")
            import traceback
            st.error(f"Details: {traceback.format_exc()}")

def generate_challenge_questions(difficulty, num_questions):
    """Generate challenge questions"""
    
    with st.spinner("🎲 Generating challenge questions..."):
        try:
            import google.generativeai as genai
            import os
            
            # Configure Gemini
            api_key = os.getenv('GOOGLE_API_KEY')
            if not api_key:
                st.error("❌ Please set your GOOGLE_API_KEY in the .env file")
                return
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Get document content from session state
            content = st.session_state.get('document_content', '')
            
            if not content:
                st.error("❌ No document content available. Please upload a document first.")
                return
            
            # Create question generation prompt
            prompt = f"""
            Based on the following document, create {num_questions} {difficulty} level comprehension questions.
            
            Each question should:
            1. Test understanding of key concepts
            2. Require reasoning about the content
            3. Have 4 multiple choice options (A, B, C, D)
            4. Include the correct answer
            5. Be challenging but fair
            
            Document content:
            {content[:4000]}...
            
            Generate questions in this format:
            Question 1: [Question text]
            A) [Option A]
            B) [Option B]
            C) [Option C]
            D) [Option D]
            Correct: [A/B/C/D]
            
            Questions:
            """
            
            response = model.generate_content(prompt)
            questions_text = response.text.strip()
            
            # Parse the response into structured questions
            questions = []
            lines = questions_text.split('\n')
            current_q = {}
            options = []
            
            for line in lines:
                line = line.strip()
                if line.startswith('Question'):
                    if current_q and options:
                        current_q['options'] = options
                        questions.append(current_q)
                    current_q = {
                        'id': len(questions) + 1,
                        'question': line.split(':', 1)[1].strip() if ':' in line else line,
                        'type': 'multiple_choice',
                        'correct_answer': 'A'  # Default, will be updated
                    }
                    options = []
                elif line.startswith(('A)', 'B)', 'C)', 'D)')):
                    options.append(line[2:].strip())
                elif line.startswith('Correct:'):
                    correct_letter = line.split(':')[1].strip()
                    if correct_letter in ['A', 'B', 'C', 'D'] and options:
                        idx = ord(correct_letter) - ord('A')
                        if idx < len(options):
                            current_q['correct_answer'] = options[idx]
            
            # Add last question
            if current_q and options:
                current_q['options'] = options
                questions.append(current_q)
            
            # Fallback if parsing failed
            if not questions:
                questions = [
                    {
                        "id": i+1,
                        "question": f"Based on the document, what is a key concept mentioned? (Generated question {i+1})",
                        "type": "multiple_choice",
                        "options": ["Concept A", "Concept B", "Concept C", "Concept D"],
                        "correct_answer": "Concept A"
                    }
                    for i in range(num_questions)
                ]
            
            st.session_state.challenge_questions = questions[:num_questions]
            st.session_state.current_challenge = 0
            st.success("✅ Challenge questions generated!")
            time.sleep(1)
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Error generating questions: {str(e)}")
            import traceback
            st.error(f"Details: {traceback.format_exc()}")

def display_challenge_questions():
    """Display and handle challenge questions"""
    
    if not st.session_state.challenge_questions:
        return
    
    current_idx = st.session_state.current_challenge
    total_questions = len(st.session_state.challenge_questions)
    
    if current_idx < total_questions:
        question = st.session_state.challenge_questions[current_idx]
        
        st.markdown(f"### Question {current_idx + 1} of {total_questions}")
        st.markdown(f"**{question['question']}**")
        
        if question['type'] == 'multiple_choice':
            selected_option = st.radio(
                "Select your answer:",
                question['options'],
                key=f"question_{current_idx}"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Submit Answer"):
                    evaluate_challenge_answer(question, selected_option)
            
            with col2:
                if st.button("⏭️ Next Question") and current_idx < total_questions - 1:
                    st.session_state.current_challenge += 1
                    st.rerun()
    else:
        st.success("🎉 Challenge completed! Great job!")

def evaluate_challenge_answer(question, user_answer):
    """Evaluate challenge answer"""
    
    with st.spinner("📝 Evaluating your answer..."):
        try:
            # Mock evaluation
            is_correct = user_answer == question['correct_answer']
            feedback = "Excellent reasoning!" if is_correct else f"The correct answer is {question['correct_answer']}. Here's why..."
            
            if is_correct:
                st.success(f"✅ Correct! {feedback}")
            else:
                st.error(f"❌ {feedback}")
            
            time.sleep(2)
            
        except Exception as e:
            st.error(f"❌ Error evaluating answer: {str(e)}")

if __name__ == "__main__":
    main()
