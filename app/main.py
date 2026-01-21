"""
FastAPI application with OCR and NLP endpoints.
"""
import logging
from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse

from app.schemas import (
    OCRResponse,
    FeedbackRequest,
    FeedbackResponse,
    InsightsResponse,
    SentimentDistribution,
    KeywordStat,
    ServiceItem
)
from app.ocr.bill_ocr import (
    extract_text_from_image,
    parse_services,
    parse_date,
    calculate_total_price
)
from app.nlp.sentiment import (
    analyze_sentiment,
    extract_keywords,
    preprocess_text
)
from app.nlp.feedback_store import feedback_store

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Services API",
    description="API for OCR bill processing and NLP customer feedback analysis",
    version="1.0.0"
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "AI Services API",
        "version": "1.0.0",
        "endpoints": ["/api/ocr/bill", "/api/nlp/feedback", "/api/nlp/insights"]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/api/ocr/bill", response_model=OCRResponse)
async def process_bill_ocr(file: UploadFile = File(...)):
    """
    Process bill image and extract structured data.
    
    Args:
        file: Image file upload
        
    Returns:
        OCRResponse with extracted text and parsed data
        
    Raises:
        HTTPException: If file processing fails
    """
    # Validate file type
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    try:
        # Read image file
        image_bytes = await file.read()
        
        if not image_bytes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Empty file uploaded"
            )
        
        logger.info(f"Processing image: {file.filename}, size: {len(image_bytes)} bytes")
        
        # Extract text using OCR
        raw_text = extract_text_from_image(image_bytes)
        
        if not raw_text or not raw_text.strip():
            return OCRResponse(
                raw_text="",
                services=[],
                total_price=None,
                date=None,
                success=False,
                message="No text could be extracted from the image"
            )
        
        # Parse structured data
        services = parse_services(raw_text)
        date = parse_date(raw_text)
        total_price = calculate_total_price(services)
        
        logger.info(f"Extracted {len(services)} services, date: {date}, total: {total_price}")
        
        return OCRResponse(
            raw_text=raw_text.strip(),
            services=services,
            total_price=total_price,
            date=date,
            success=True,
            message="OCR processing completed successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing bill OCR: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process image: {str(e)}"
        )


@app.post("/api/nlp/feedback", response_model=FeedbackResponse)
async def analyze_feedback(request: FeedbackRequest):
    """
    Analyze customer feedback for sentiment and extract keywords.
    
    Args:
        request: FeedbackRequest with feedback text
        
    Returns:
        FeedbackResponse with sentiment analysis and keywords
        
    Raises:
        HTTPException: If processing fails
    """
    try:
        if not request.feedback or not request.feedback.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Feedback text cannot be empty"
            )
        
        # Preprocess text
        processed_text = preprocess_text(request.feedback)
        
        if not processed_text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Feedback text contains no valid content after preprocessing"
            )
        
        logger.info(f"Analyzing feedback: {len(processed_text)} characters")
        
        # Analyze sentiment
        sentiment_result = analyze_sentiment(processed_text)
        
        # Extract keywords
        keywords = extract_keywords(processed_text, max_keywords=10)
        
        logger.info(f"Sentiment: {sentiment_result.label}, Confidence: {sentiment_result.confidence:.2f}, Keywords: {len(keywords)}")
        
        # Store feedback for analytics
        feedback_store.add_feedback(
            feedback=request.feedback,
            sentiment=sentiment_result.label,
            polarity=sentiment_result.polarity,
            subjectivity=sentiment_result.subjectivity,
            keywords=keywords,
            confidence=sentiment_result.confidence
        )
        
        return FeedbackResponse(
            sentiment=sentiment_result.label,
            confidence=round(sentiment_result.confidence, 3),
            polarity=round(sentiment_result.polarity, 3),
            subjectivity=round(sentiment_result.subjectivity, 3),
            keywords=keywords,
            success=True,
            message="Feedback analysis completed successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing feedback: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze feedback: {str(e)}"
        )


@app.get("/api/nlp/insights", response_model=InsightsResponse)
async def get_feedback_insights():
    """
    Get aggregated feedback analytics for admin dashboard.
    
    Returns:
        InsightsResponse with sentiment distribution, top keywords, and statistics
        
    Raises:
        HTTPException: If processing fails
    """
    try:
        logger.info("Generating feedback insights")
        
        # Get analytics data
        total_feedback = feedback_store.get_total_count()
        sentiment_dist = feedback_store.get_sentiment_distribution()
        top_keywords = feedback_store.get_top_keywords(limit=20)
        avg_confidence = feedback_store.get_average_confidence()
        avg_polarity = feedback_store.get_average_polarity()
        
        # Convert keyword dicts to KeywordStat models
        keyword_stats = [
            KeywordStat(keyword=kw["keyword"], count=kw["count"], percentage=kw["percentage"])
            for kw in top_keywords
        ]
        
        return InsightsResponse(
            total_feedback=total_feedback,
            sentiment_distribution=SentimentDistribution(
                positive=sentiment_dist["positive"],
                negative=sentiment_dist["negative"],
                neutral=sentiment_dist["neutral"]
            ),
            top_keywords=keyword_stats,
            average_confidence=avg_confidence,
            average_polarity=avg_polarity,
            success=True,
            message="Insights generated successfully"
        )
        
    except Exception as e:
        logger.error(f"Error generating insights: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate insights: {str(e)}"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

