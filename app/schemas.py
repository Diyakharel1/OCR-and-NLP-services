"""
Pydantic schemas for API request and response models.
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class ServiceItem(BaseModel):
    """Model for a service item with name and price."""
    name: str
    price: float


class OCRResponse(BaseModel):
    """Response model for OCR endpoint."""
    raw_text: str
    services: List[ServiceItem]
    total_price: Optional[float] = None
    date: Optional[str] = None
    success: bool
    message: str


class FeedbackRequest(BaseModel):
    """Request model for NLP feedback endpoint."""
    feedback: str = Field(..., description="Customer feedback text to analyze", min_length=1)


class FeedbackResponse(BaseModel):
    """Response model for NLP feedback endpoint."""
    sentiment: str = Field(..., description="Sentiment label: positive, negative, or neutral")
    confidence: float = Field(..., description="Confidence score (0.0 to 1.0)", ge=0.0, le=1.0)
    polarity: float = Field(..., description="Sentiment polarity score (-1.0 to 1.0)", ge=-1.0, le=1.0)
    subjectivity: float = Field(..., description="Subjectivity score (0.0 to 1.0)", ge=0.0, le=1.0)
    keywords: List[str] = Field(..., description="Extracted keywords from the feedback")
    success: bool
    message: str


class SentimentDistribution(BaseModel):
    """Sentiment distribution model."""
    positive: float = Field(..., description="Percentage of positive feedback", ge=0.0, le=100.0)
    negative: float = Field(..., description="Percentage of negative feedback", ge=0.0, le=100.0)
    neutral: float = Field(..., description="Percentage of neutral feedback", ge=0.0, le=100.0)


class KeywordStat(BaseModel):
    """Keyword statistics model."""
    keyword: str = Field(..., description="Keyword text")
    count: int = Field(..., description="Number of times keyword appears", ge=0)
    percentage: float = Field(..., description="Percentage of feedback containing this keyword", ge=0.0, le=100.0)


class InsightsResponse(BaseModel):
    """Response model for insights endpoint."""
    total_feedback: int = Field(..., description="Total number of feedback records", ge=0)
    sentiment_distribution: SentimentDistribution = Field(..., description="Sentiment distribution percentages")
    top_keywords: List[KeywordStat] = Field(..., description="Top keywords with counts and percentages")
    average_confidence: float = Field(..., description="Average confidence score across all feedback", ge=0.0, le=1.0)
    average_polarity: float = Field(..., description="Average polarity score across all feedback", ge=-1.0, le=1.0)
    success: bool
    message: str

