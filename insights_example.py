"""
Example usage of the NLP feedback insights endpoint.

This file demonstrates the GET /api/nlp/insights endpoint response structure.
"""

# Example Response from GET /api/nlp/insights
example_insights_response = {
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
        },
        {
            "keyword": "customer service",
            "count": 67,
            "percentage": 44.67
        },
        {
            "keyword": "quality",
            "count": 54,
            "percentage": 36.0
        },
        {
            "keyword": "delivery",
            "count": 43,
            "percentage": 28.67
        },
        {
            "keyword": "price",
            "count": 38,
            "percentage": 25.33
        },
        {
            "keyword": "experience",
            "count": 32,
            "percentage": 21.33
        },
        {
            "keyword": "support",
            "count": 28,
            "percentage": 18.67
        },
        {
            "keyword": "design",
            "count": 25,
            "percentage": 16.67
        },
        {
            "keyword": "recommend",
            "count": 22,
            "percentage": 14.67
        },
        {
            "keyword": "value",
            "count": 19,
            "percentage": 12.67
        }
    ],
    "average_confidence": 0.742,
    "average_polarity": 0.285,
    "success": True,
    "message": "Insights generated successfully"
}

# Example cURL command:
"""
curl -X GET "http://localhost:8000/api/nlp/insights" \\
     -H "Content-Type: application/json"
"""

# Example Python requests:
"""
import requests

url = "http://localhost:8000/api/nlp/insights"
response = requests.get(url)
print(response.json())
"""

# Example usage flow:
"""
1. Submit feedback via POST /api/nlp/feedback
   - Each feedback is automatically stored for analytics

2. Retrieve insights via GET /api/nlp/insights
   - Returns aggregated analytics across all stored feedback
   - Perfect for admin dashboard visualization

3. Dashboard can use the data to:
   - Display sentiment pie chart (sentiment_distribution)
   - Show keyword cloud (top_keywords)
   - Display overall metrics (average_confidence, average_polarity)
   - Show total feedback count
"""

