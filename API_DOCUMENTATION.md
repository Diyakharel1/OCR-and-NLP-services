# API Documentation

## Overview
FastAPI application providing OCR bill processing and NLP customer feedback analysis services.

## Base URL
- Local: `http://localhost:8000`
- Production: (configure as needed)

## API Endpoints

### Health Check
- **GET** `/health`
- **Description**: Health check endpoint
- **Response**:
  ```json
  {
    "status": "healthy"
  }
  ```

### OCR Bill Processing
- **POST** `/api/ocr/bill`
- **Description**: Process bill image and extract structured data (services, prices, dates)
- **Content-Type**: `multipart/form-data`
- **Request**: 
  - `file`: Image file (JPEG, PNG, etc.)
- **Response**:
  ```json
  {
    "raw_text": "Extracted text from image",
    "services": [
      {
        "name": "Service Name",
        "price": 99.99
      }
    ],
    "total_price": 199.98,
    "date": "01/15/2024",
    "success": true,
    "message": "OCR processing completed successfully"
  }
  ```
- **Example cURL**:
  ```bash
  curl -X POST "http://localhost:8000/api/ocr/bill" \
       -H "accept: application/json" \
       -H "Content-Type: multipart/form-data" \
       -F "file=@bill_image.jpg"
  ```

### NLP Feedback Analysis
- **POST** `/api/nlp/feedback`
- **Description**: Analyze customer feedback for sentiment and extract keywords
- **Content-Type**: `application/json`
- **Request Body**:
  ```json
  {
    "feedback": "I absolutely love this product! The quality is excellent."
  }
  ```
- **Response**:
  ```json
  {
    "sentiment": "positive",
    "confidence": 0.85,
    "polarity": 0.75,
    "subjectivity": 0.65,
    "keywords": ["product", "quality", "excellent"],
    "success": true,
    "message": "Feedback analysis completed successfully"
  }
  ```
- **Sentiment Values**: `positive`, `negative`, `neutral`
- **Example cURL**:
  ```bash
  curl -X POST "http://localhost:8000/api/nlp/feedback" \
       -H "Content-Type: application/json" \
       -d '{"feedback": "I love this product!"}'
  ```

### Feedback Analytics
- **GET** `/api/nlp/insights`
- **Description**: Get aggregated feedback analytics for admin dashboard
- **Response**:
  ```json
  {
    "total_feedback": 150,
    "sentiment_distribution": {
      "positive": 65.33,
      "negative": 20.67,
      "neutral": 14.0
    },
    "top_keywords": [
      {
        "keyword": "product",
        "count": 89,
        "percentage": 59.33
      }
    ],
    "average_confidence": 0.742,
    "average_polarity": 0.285,
    "success": true,
    "message": "Insights generated successfully"
  }
  ```
- **Example cURL**:
  ```bash
  curl -X GET "http://localhost:8000/api/nlp/insights"
  ```

## Interactive API Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Error message describing what went wrong"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Failed to process request: error details"
}
```

## Technology Stack
- **Framework**: FastAPI
- **OCR**: Pytesseract (Tesseract-OCR)
- **NLP**: TextBlob
- **Python**: 3.10
- **Server**: Uvicorn

## Data Storage
- Feedback data is stored in-memory (in-memory store)
- For production, replace with a proper database

