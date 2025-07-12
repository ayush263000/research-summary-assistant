# Migration from OpenAI to Google Gemini

This document outlines the changes made to migrate from OpenAI GPT-4 to Google Gemini Pro API.

## Changes Made

### 1. Dependencies Updated

**Before (OpenAI):**
```
openai==1.3.5
langchain-openai==0.0.2
```

**After (Google Gemini):**
```
google-generativeai==0.3.2
langchain-google-genai==0.0.5
```

### 2. Environment Variables

**Before:**
```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4
```

**After:**
```env
GOOGLE_API_KEY=your_google_api_key_here
GEMINI_MODEL=gemini-pro
```

### 3. Core Changes

#### AI Client (`app/core/ai_client.py`)
- Replaced `openai` with `google.generativeai`
- Updated API calls to use Gemini's `generate_content()` method
- Modified generation config parameters
- Maintained the same interface for seamless integration

#### Document Processor (`app/core/document_processor.py`)
- Replaced `OpenAIEmbeddings` with `GoogleGenerativeAIEmbeddings`
- Updated embedding model to `models/embedding-001`

#### Configuration (`app/utils/config.py`)
- Updated environment variable names
- Changed default model from `gpt-4` to `gemini-pro`

### 4. Key API Differences

| Feature | OpenAI GPT-4 | Google Gemini Pro |
|---------|--------------|-------------------|
| Chat Completion | `ChatCompletion.acreate()` | `generate_content()` |
| Model Name | `gpt-4` | `gemini-pro` |
| Response Format | `response.choices[0].message.content` | `response.text` |
| System Messages | Supported | Not directly supported* |
| Embeddings | `text-embedding-ada-002` | `models/embedding-001` |

*Note: System instructions are handled differently in Gemini - they're included in the prompt context.

### 5. Benefits of Migration

1. **Cost Efficiency**: Google Gemini Pro offers competitive pricing
2. **Performance**: Similar quality responses with good performance
3. **Free Tier**: Google provides generous free usage limits
4. **Integration**: Good LangChain support for embeddings and text generation

### 6. Getting Started

1. **Get Google API Key:**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy the key to your `.env` file

2. **Update Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your Google API key
   ```

4. **Run the Application:**
   ```bash
   python run.py
   ```

### 7. API Limits and Considerations

- **Rate Limits**: 60 requests per minute (free tier)
- **Token Limits**: 32,760 tokens per request
- **Content Filtering**: Gemini has built-in safety filters
- **Languages**: Supports multiple languages with good performance

### 8. Troubleshooting

**Common Issues:**

1. **API Key Not Found:**
   - Ensure `GOOGLE_API_KEY` is set in `.env`
   - Verify the API key is valid

2. **Rate Limit Exceeded:**
   - Implement retry logic with exponential backoff
   - Consider upgrading to paid tier

3. **Content Blocked:**
   - Gemini may block certain content due to safety filters
   - Rephrase prompts if necessary

### 9. Future Enhancements

- Add support for Gemini Vision for image analysis
- Implement function calling when available
- Add multi-modal document processing capabilities
- Optimize prompt engineering for Gemini-specific features
