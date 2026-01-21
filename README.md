# AI Services API

FastAPI application providing OCR bill processing and NLP customer feedback analysis services.

## Features

- **OCR Bill Processing**: Extract text from bill images and parse structured data (services, prices, dates)
- **NLP Sentiment Analysis**: Analyze customer feedback for sentiment (positive/negative/neutral) with confidence scores
- **Keyword Extraction**: Extract relevant keywords from feedback
- **Feedback Analytics**: Aggregate insights with sentiment distribution and top keywords

## Project Structure

```
ai_services/
│
├── app/
│   ├── main.py              # FastAPI application and routes
│   ├── schemas.py           # Pydantic models for requests/responses
│   ├── ocr/
│   │   └── bill_ocr.py      # OCR functionality for bill processing
│   └── nlp/
│       ├── sentiment.py     # Sentiment analysis and keyword extraction
│       └── feedback_store.py # In-memory feedback data store
│
├── requirements.txt         # Python dependencies
├── Dockerfile              # Production Docker image
├── docker-compose.yml      # Docker Compose configuration
└── README.md              # This file
```

## Installation

### Local Development

1. Install Python 3.10+
2. Install system dependencies:
   ```bash
   sudo apt-get update
   sudo apt-get install tesseract-ocr
   ```
3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python -m app.main
   # or
   uvicorn app.main:app --reload
   ```

### Docker

1. Build the image:
   ```bash
   docker build -t ai-services:latest .
   ```

2. Run with Docker:
   ```bash
   docker run -p 8000:8000 ai-services:latest
   ```

3. Or use Docker Compose:
   ```bash
   docker compose up -d
   ```
   
   Note: If you have Docker Compose V2 (default in newer Docker installations), use `docker compose` (with space). 
   For older installations, you may need to use `docker-compose` (with hyphen) or install it separately.

## API Endpoints

### Health Check
- **GET** `/health` - Health check endpoint

### OCR Endpoints
- **POST** `/api/ocr/bill` - Process bill image and extract structured data
  - Accepts: Image file (multipart/form-data)
  - Returns: Extracted text, services, prices, date

### NLP Endpoints
- **POST** `/api/nlp/feedback` - Analyze customer feedback
  - Accepts: JSON with `feedback` text
  - Returns: Sentiment, confidence, keywords
  
- **GET** `/api/nlp/insights` - Get aggregated feedback analytics
  - Returns: Sentiment distribution, top keywords, statistics

## API Documentation

Once the server is running, access interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Example Usage

### OCR Bill Processing

```bash
curl -X POST "http://localhost:8000/api/ocr/bill" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@bill_image.jpg"
```

### NLP Feedback Analysis

```bash
curl -X POST "http://localhost:8000/api/nlp/feedback" \
     -H "Content-Type: application/json" \
     -d '{
       "feedback": "I absolutely love this product! The quality is excellent."
     }'
```

### Get Feedback Insights

```bash
curl -X GET "http://localhost:8000/api/nlp/insights"
```

## Technologies

- **FastAPI**: Modern, fast web framework for building APIs
- **Pytesseract**: OCR engine wrapper for text extraction
- **TextBlob**: NLP library for sentiment analysis
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running FastAPI

## Development

The project follows a modular structure:
- `app/main.py`: FastAPI routes and application setup
- `app/schemas.py`: Pydantic models for API contracts
- `app/ocr/`: OCR-related functionality
- `app/nlp/`: NLP-related functionality

## License

MIT

# OCR-and-NLP-services
