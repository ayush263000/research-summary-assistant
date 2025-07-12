# 📚 Document-Aware GenAI Assistant

A powerful document analysis and question-answering application powered by Google Gemini AI. Upload PDF or TXT documents and interact with them through natural language queries, automatic summarization, and intelligent challenge questions.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

## ✨ Features

### 📄 Document Upload & Processing
- **Multi-format Support**: Upload PDF and TXT files up to 50MB
- **Intelligent Text Extraction**: Advanced PDF text extraction with fallback handling
- **Auto-summarization**: Generate concise 150-word summaries automatically
- **Content Preview**: View extracted content before processing

### ❓ Ask Anything Mode
- **Free-form Q&A**: Ask any question about your uploaded document
- **Contextual Answers**: AI provides answers grounded in document content
- **Reference Tracking**: Clear citations and references for every response
- **Conversation History**: Review all previous questions and answers
- **Smart UI**: Latest conversations appear at the top, auto-expanded

### 🎯 Challenge Me Mode
- **Interactive Learning**: AI generates comprehension questions based on document content
- **Multiple Difficulty Levels**: Easy, Medium, and Hard questions
- **Customizable Quantity**: Choose 1, 3, 5, or 10 questions
- **Multiple Choice Format**: Structured questions with 4 options each
- **Instant Feedback**: Immediate evaluation and explanations

### 🔒 Privacy & Security
- **Local Processing**: Documents processed locally, not stored permanently
- **API Key Security**: Secure Google API key management
- **Session Management**: Temporary storage in browser sessions only

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google API Key (for Gemini AI)
- Git (for cloning the repository)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd document-genai-assistant
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your Google API key
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

6. **Access the application**
   Open your browser and navigate to `http://localhost:8501`

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Required
GOOGLE_API_KEY=your_google_api_key_here

# Optional (with defaults)
GEMINI_MODEL=gemini-1.5-flash
MAX_TOKENS=8192
TEMPERATURE=0.1
DATABASE_URL=sqlite:///./data/app.db
UPLOAD_DIR=./data/uploads
MAX_FILE_SIZE=50MB
ALLOWED_EXTENSIONS=pdf,txt
DEBUG=True
LOG_LEVEL=INFO
```

### Getting a Google API Key

1. Visit the [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key and add it to your `.env` file

## 📁 Project Structure

```
document-genai-assistant/
├── app/                          # Main application code
│   ├── __init__.py
│   ├── api/                      # FastAPI backend (optional)
│   │   ├── __init__.py
│   │   └── main.py
│   ├── core/                     # Core functionality
│   │   ├── __init__.py
│   │   ├── ai_client.py          # Google Gemini integration
│   │   ├── challenge_engine.py   # Question generation
│   │   ├── document_processor.py # Document handling
│   │   └── qa_engine.py          # Q&A processing
│   ├── frontend/                 # Streamlit UI
│   │   ├── __init__.py
│   │   └── main.py               # Main UI application
│   ├── models/                   # Data models
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── schemas.py
│   └── utils/                    # Utilities
│       ├── __init__.py
│       ├── config.py
│       └── logging_config.py
├── config/                       # Configuration files
│   ├── logging.yaml
│   └── README.md
├── data/                         # Data directory
│   ├── uploads/                  # Uploaded documents
│   └── README.md
├── docs/                         # Documentation
│   ├── API.md
│   ├── DEVELOPMENT.md
│   └── GEMINI_MIGRATION.md
├── logs/                         # Application logs
├── scripts/                      # Utility scripts
│   ├── dev.sh
│   └── setup.py
├── tests/                        # Test files
│   ├── conftest.py
│   ├── test_api.py
│   └── test_document_processor.py
├── .env                          # Environment variables
├── .gitignore                    # Git ignore file
├── pyproject.toml                # Project configuration
├── requirements.txt              # Python dependencies
├── run.py                        # Application entry point
└── README.md                     # This file
```

## 🔧 Usage

### 1. Upload Document
1. Navigate to the "📄 Upload Document" section
2. Choose a PDF or TXT file (up to 50MB)
3. Click "🚀 Process Document"
4. View the auto-generated summary

### 2. Ask Questions
1. Go to "❓ Ask Anything" section
2. Type your question in the text area
3. Click "🔍 Ask Question"
4. View the AI-generated answer with references
5. Browse conversation history (latest at top)

### 3. Challenge Mode
1. Access "🎯 Challenge Me" section
2. Select difficulty level and number of questions
3. Click "🎲 Generate Challenge Questions"
4. Answer multiple-choice questions
5. Get immediate feedback and explanations

## 🛠️ Development

### Running in Development Mode

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run with auto-reload
streamlit run app/frontend/main.py --server.runOnSave true
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html
```

### Code Formatting

```bash
# Format code
black app/

# Check style
flake8 app/

# Type checking
mypy app/
```

## 📊 Technical Details

### AI Model
- **Model**: Google Gemini 1.5 Flash (Free Tier)
- **Rate Limiting**: 4 seconds between requests
- **Token Limit**: 8,192 tokens per request
- **Context Window**: Supports large document processing

### Document Processing
- **PDF**: PyPDF2 with pdfminer.six fallback
- **Text Extraction**: Handles multi-page documents
- **Content Limits**: First 4,000 characters for AI processing
- **Error Handling**: Graceful degradation for image-based PDFs

### UI Framework
- **Frontend**: Streamlit with custom CSS styling
- **Responsive Design**: Works on desktop and mobile
- **Session Management**: Browser-based state management
- **Real-time Updates**: Automatic UI refresh after operations

## 🔒 Security Considerations

- **API Keys**: Never commit API keys to version control
- **File Uploads**: Limited to safe file types (PDF, TXT)
- **Size Limits**: 50MB maximum file size
- **Local Processing**: Documents processed locally
- **No Permanent Storage**: Files not saved to disk

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Use meaningful commit messages

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Common Issues

**Q: The document summary is empty**
- Ensure your Google API key is set correctly
- Check that the document contains extractable text
- Verify the document is not image-based (for PDFs)

**Q: Upload fails with large files**
- Maximum file size is 50MB
- Try compressing your PDF or splitting large documents

**Q: API rate limit errors**
- The app includes automatic rate limiting (4 seconds between requests)
- Wait a moment between operations if you see rate limit warnings

### Getting Help

- 📧 Email: team@example.com
- 🐛 Report bugs: [GitHub Issues](https://github.com/example/document-genai-assistant/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/example/document-genai-assistant/discussions)

## 🙏 Acknowledgments

- Google Gemini AI for powerful language processing
- Streamlit for the excellent UI framework
- PyPDF2 and pdfminer.six for document processing
- The open-source community for inspiration and tools

---

**Built with ❤️ using Google Gemini AI and Streamlit**
