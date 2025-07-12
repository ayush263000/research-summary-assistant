# API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
Currently, no authentication is required for local usage.

## Endpoints

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### Upload Document
```http
POST /upload
Content-Type: multipart/form-data
```

**Parameters:**
- `file`: PDF or TXT file (max 50MB)

**Response:**
```json
{
  "document_id": "uuid-string",
  "filename": "document.pdf",
  "summary": "Auto-generated summary ≤150 words",
  "status": "processed"
}
```

### Ask Question
```http
POST /ask
Content-Type: application/json
```

**Request Body:**
```json
{
  "document_id": "uuid-string",
  "question": "What are the main conclusions?"
}
```

**Response:**
```json
{
  "answer": "Based on the document...",
  "references": [
    "Page 1, Paragraph 2: Introduction section",
    "Page 3, Section 2.1: Main findings"
  ],
  "confidence": 0.85
}
```

### Generate Challenge Questions
```http
POST /challenge
Content-Type: application/json
```

**Request Body:**
```json
{
  "document_id": "uuid-string",
  "difficulty": "medium",
  "num_questions": 3
}
```

**Response:**
```json
{
  "questions": [
    {
      "id": "q1",
      "question": "What is the main hypothesis?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_answer": "Option A",
      "explanation": "Explanation text",
      "difficulty": "medium",
      "type": "multiple_choice"
    }
  ]
}
```

### Evaluate Answer
```http
POST /evaluate
Content-Type: application/json
```

**Request Body:**
```json
{
  "document_id": "uuid-string",
  "question": "Question text",
  "user_answer": "User's answer",
  "correct_answer": "Correct answer"
}
```

**Response:**
```json
{
  "score": 85,
  "feedback": "Good answer! Here's why...",
  "references": ["Document references"],
  "correct_answer": "The correct answer",
  "is_correct": true
}
```

### List Documents
```http
GET /documents
```

**Response:**
```json
{
  "documents": [
    {
      "id": "uuid-string",
      "filename": "document.pdf",
      "created_at": "2025-07-12T10:30:00Z",
      "chunk_count": 15
    }
  ]
}
```

## Error Responses

All endpoints may return error responses in this format:

```json
{
  "error": "Error type",
  "detail": "Detailed error message",
  "timestamp": "2025-07-12T10:30:00Z"
}
```

Common HTTP status codes:
- `400`: Bad Request (invalid input)
- `404`: Not Found (document not found)
- `500`: Internal Server Error

## Rate Limits

Currently no rate limits are implemented for local usage.

## Examples

### Complete Workflow

1. **Upload a document:**
   ```bash
   curl -X POST "http://localhost:8000/upload" \
        -F "file=@document.pdf"
   ```

2. **Ask a question:**
   ```bash
   curl -X POST "http://localhost:8000/ask" \
        -H "Content-Type: application/json" \
        -d '{"document_id": "uuid", "question": "What are the key findings?"}'
   ```

3. **Generate challenge questions:**
   ```bash
   curl -X POST "http://localhost:8000/challenge" \
        -H "Content-Type: application/json" \
        -d '{"document_id": "uuid", "difficulty": "medium", "num_questions": 3}'
   ```
