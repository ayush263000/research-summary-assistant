# Document-Aware GenAI Assistant

A sophisticated document analysis tool that provides deep insights, Q&A capabilities, and comprehension testing for uploaded PDF/TXT documents.

## Features

- **Document Upload**: Support for PDF and TXT files
- **Ask Anything**: Free-form Q&A with contextual understanding
- **Challenge Me**: Logic-based question generation and evaluation
- **Auto-Summary**: Immediate ≤150 word summaries upon upload
- **Reference Grounding**: All responses backed by exact document references
- **Zero Hallucination**: Strict grounding to source material

## Tech Stack

- **Frontend**: Streamlit (can be switched to Gradio/React)
- **Backend**: FastAPI
- **AI/ML**: Google Gemini 1.5 Flash (Free Tier) + document parsers
- **Document Processing**: PyPDF2, pdfminer.six
- **Storage**: SQLite for session management

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your Google API key
   ```

3. Run the application:
   ```bash
   python run.py
   ```

4. Access the web interface at `http://localhost:8501`

## Project Structure

```
├── app/                    # Main application code
│   ├── api/               # FastAPI backend
│   ├── frontend/          # Streamlit frontend
│   ├── core/              # Core business logic
│   ├── models/            # Data models
│   └── utils/             # Utility functions
├── data/                  # Data storage
├── tests/                 # Test suite
├── docs/                  # Documentation
├── scripts/               # Utility scripts
└── config/                # Configuration files
```

## Demo

A 2-3 minute demo video is available in the `docs/` directory.

## Development

See `docs/DEVELOPMENT.md` for development guidelines and setup instructions.
