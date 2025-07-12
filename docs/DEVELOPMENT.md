# Development Guide

## Setup

1. **Clone and Install**
   ```bash
   git clone <repository-url>
   cd document-genai-assistant
   pip install -r requirements.txt
   ```

2. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your Google API key
   ```

3. **Run the Application**
   ```bash
   python run.py
   ```

## Project Architecture

### Core Components

1. **Document Processor** (`app/core/document_processor.py`)
   - Handles PDF/TXT file processing
   - Creates vector embeddings
   - Manages document storage

2. **AI Client** (`app/core/ai_client.py`)
   - Google Gemini API integration
   - Summary generation
   - Question answering
   - Challenge question creation

3. **Q&A Engine** (`app/core/qa_engine.py`)
   - Free-form question processing
   - Context retrieval
   - Answer generation with references

4. **Challenge Engine** (`app/core/challenge_engine.py`)
   - Generates comprehension questions
   - Evaluates user answers
   - Provides feedback

### API Layer

- **FastAPI Backend** (`app/api/main.py`)
  - RESTful endpoints
  - File upload handling
  - Response formatting

### Frontend

- **Streamlit Interface** (`app/frontend/main.py`)
  - Document upload interface
  - Q&A chat interface
  - Challenge mode interface

### Data Models

- **Database Models** (`app/models/database.py`)
  - SQLite for document metadata
  - Session tracking
  - Question history

- **API Schemas** (`app/models/schemas.py`)
  - Pydantic models for requests/responses
  - Data validation

## Development Workflow

1. **Adding New Features**
   - Create feature branch
   - Implement in appropriate module
   - Add tests
   - Update documentation

2. **Testing**
   ```bash
   pytest tests/
   ```

3. **Code Quality**
   ```bash
   black app/
   flake8 app/
   mypy app/
   ```

## Configuration

Environment variables (see `.env.example`):
- `GOOGLE_API_KEY`: Your Google API key
- `GEMINI_MODEL`: Model to use (default: gemini-pro)
- `DATABASE_URL`: Database connection string
- `UPLOAD_DIR`: Directory for uploaded files

## Extending the System

### Adding New Document Types

1. Extend `DocumentProcessor._extract_text()` method
2. Add new file type validation
3. Update allowed extensions in config

### Adding New Question Types

1. Extend `ChallengeEngine.generate_questions()`
2. Add new question schemas
3. Update frontend interface

### Adding New AI Providers

1. Create new client in `core/` directory
2. Implement common interface
3. Update configuration
