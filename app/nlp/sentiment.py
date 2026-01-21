"""
NLP service module for analyzing customer feedback.
Provides sentiment analysis and keyword extraction.
"""
import re
import logging
from typing import List
from textblob import TextBlob
from collections import Counter

logger = logging.getLogger(__name__)


class SentimentResult:
    """Result of sentiment analysis."""
    def __init__(self, polarity: float, subjectivity: float):
        self.polarity = polarity
        self.subjectivity = subjectivity
        self.label = self._classify_sentiment(polarity)
        self.confidence = self._calculate_confidence(polarity, subjectivity)
    
    def _classify_sentiment(self, polarity: float) -> str:
        """
        Classify sentiment based on polarity score.
        
        Args:
            polarity: Sentiment polarity (-1 to 1)
            
        Returns:
            Sentiment label: 'positive', 'negative', or 'neutral'
        """
        if polarity > 0.1:
            return "positive"
        elif polarity < -0.1:
            return "negative"
        else:
            return "neutral"
    
    def _calculate_confidence(self, polarity: float, subjectivity: float) -> float:
        """
        Calculate confidence score based on polarity strength and subjectivity.
        
        Args:
            polarity: Sentiment polarity (-1 to 1)
            subjectivity: Subjectivity score (0 to 1)
            
        Returns:
            Confidence score (0 to 1)
        """
        # Higher absolute polarity = higher confidence
        # Lower subjectivity = higher confidence (more objective)
        polarity_strength = abs(polarity)
        objectivity = 1 - subjectivity
        
        # Weighted combination
        confidence = (polarity_strength * 0.7) + (objectivity * 0.3)
        
        # Normalize to 0-1 range
        return min(1.0, max(0.0, confidence))


def analyze_sentiment(text: str) -> SentimentResult:
    """
    Analyze sentiment of the given text.
    
    Args:
        text: Input text to analyze
        
    Returns:
        SentimentResult object with sentiment analysis
    """
    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        return SentimentResult(polarity, subjectivity)
    except Exception as e:
        logger.error(f"Sentiment analysis failed: {str(e)}")
        # Return neutral sentiment on error
        return SentimentResult(0.0, 0.5)


def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """
    Extract keywords from text using noun phrases and word frequency.
    
    Args:
        text: Input text to extract keywords from
        max_keywords: Maximum number of keywords to return
        
    Returns:
        List of keyword strings
    """
    try:
        blob = TextBlob(text.lower())
        
        # Get noun phrases (multi-word keywords)
        noun_phrases = [str(phrase) for phrase in blob.noun_phrases]
        
        # Get individual significant words (nouns, adjectives, verbs)
        # Filter out common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
            'what', 'which', 'who', 'when', 'where', 'why', 'how', 'all', 'each',
            'every', 'both', 'few', 'more', 'most', 'other', 'some', 'such',
            'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too',
            'very', 'just', 'now'
        }
        
        # Extract significant words (length > 2, not stop words)
        words = [
            word for word, tag in blob.tags
            if len(word) > 2
            and word not in stop_words
            and tag.startswith(('NN', 'JJ', 'VB'))  # Nouns, adjectives, verbs
        ]
        
        # Combine noun phrases and words, count frequency
        all_keywords = noun_phrases + words
        keyword_counts = Counter(all_keywords)
        
        # Get top keywords by frequency
        top_keywords = [
            keyword for keyword, count in keyword_counts.most_common(max_keywords)
        ]
        
        return top_keywords[:max_keywords]
    
    except Exception as e:
        logger.error(f"Keyword extraction failed: {str(e)}")
        return []


def preprocess_text(text: str) -> str:
    """
    Preprocess text for better analysis.
    
    Args:
        text: Raw input text
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?;:\-()]', '', text)
    
    return text.strip()

