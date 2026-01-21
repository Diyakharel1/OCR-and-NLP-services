"""
In-memory data store for feedback analytics.
In production, this would be replaced with a proper database.
"""
from typing import List, Dict
from datetime import datetime
from collections import Counter
import logging

logger = logging.getLogger(__name__)


class FeedbackRecord:
    """Represents a single feedback record."""
    def __init__(self, feedback: str, sentiment: str, polarity: float, 
                 subjectivity: float, keywords: List[str], confidence: float):
        self.feedback = feedback
        self.sentiment = sentiment
        self.polarity = polarity
        self.subjectivity = subjectivity
        self.keywords = keywords
        self.confidence = confidence
        self.timestamp = datetime.now()


class FeedbackStore:
    """In-memory store for feedback records."""
    
    def __init__(self):
        self._records: List[FeedbackRecord] = []
        self._lock = False  # Simple lock for thread safety (basic implementation)
    
    def add_feedback(self, feedback: str, sentiment: str, polarity: float,
                     subjectivity: float, keywords: List[str], confidence: float) -> None:
        """
        Add a feedback record to the store.
        
        Args:
            feedback: Original feedback text
            sentiment: Sentiment label (positive/negative/neutral)
            polarity: Sentiment polarity score
            subjectivity: Subjectivity score
            keywords: List of extracted keywords
            confidence: Confidence score
        """
        record = FeedbackRecord(
            feedback=feedback,
            sentiment=sentiment,
            polarity=polarity,
            subjectivity=subjectivity,
            keywords=keywords,
            confidence=confidence
        )
        self._records.append(record)
        logger.info(f"Added feedback record. Total records: {len(self._records)}")
    
    def get_all_records(self) -> List[FeedbackRecord]:
        """Get all feedback records."""
        return self._records.copy()
    
    def get_sentiment_distribution(self) -> Dict[str, float]:
        """
        Calculate sentiment distribution as percentages.
        
        Returns:
            Dictionary with sentiment labels as keys and percentages as values
        """
        if not self._records:
            return {"positive": 0.0, "negative": 0.0, "neutral": 0.0}
        
        sentiment_counts = Counter(record.sentiment for record in self._records)
        total = len(self._records)
        
        distribution = {
            "positive": round((sentiment_counts.get("positive", 0) / total) * 100, 2),
            "negative": round((sentiment_counts.get("negative", 0) / total) * 100, 2),
            "neutral": round((sentiment_counts.get("neutral", 0) / total) * 100, 2)
        }
        
        return distribution
    
    def get_top_keywords(self, limit: int = 20) -> List[Dict[str, any]]:
        """
        Get top keywords across all feedback records.
        
        Args:
            limit: Maximum number of keywords to return
            
        Returns:
            List of dictionaries with keyword and count
        """
        if not self._records:
            return []
        
        # Aggregate all keywords
        all_keywords = []
        for record in self._records:
            all_keywords.extend(record.keywords)
        
        # Count keyword frequency
        keyword_counts = Counter(all_keywords)
        
        # Get top keywords
        top_keywords = [
            {"keyword": keyword, "count": count, "percentage": round((count / len(self._records)) * 100, 2)}
            for keyword, count in keyword_counts.most_common(limit)
        ]
        
        return top_keywords
    
    def get_total_count(self) -> int:
        """Get total number of feedback records."""
        return len(self._records)
    
    def get_average_confidence(self) -> float:
        """Get average confidence score across all records."""
        if not self._records:
            return 0.0
        return round(sum(record.confidence for record in self._records) / len(self._records), 3)
    
    def get_average_polarity(self) -> float:
        """Get average polarity score across all records."""
        if not self._records:
            return 0.0
        return round(sum(record.polarity for record in self._records) / len(self._records), 3)
    
    def clear(self) -> None:
        """Clear all records (useful for testing)."""
        self._records.clear()
        logger.info("Feedback store cleared")


# Global instance
feedback_store = FeedbackStore()

