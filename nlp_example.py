"""
Example usage of the NLP feedback analysis endpoint.

This file demonstrates how to use the POST /api/nlp/feedback endpoint.
"""

# Example 1: Positive feedback
positive_feedback_request = {
    "feedback": "I absolutely love this product! The quality is excellent and the customer service was outstanding. Highly recommend to everyone!"
}

positive_feedback_response = {
    "sentiment": "positive",
    "confidence": 0.85,
    "polarity": 0.75,
    "subjectivity": 0.65,
    "keywords": [
        "product",
        "quality",
        "customer service",
        "love",
        "excellent",
        "outstanding"
    ],
    "success": True,
    "message": "Feedback analysis completed successfully"
}

# Example 2: Negative feedback
negative_feedback_request = {
    "feedback": "Terrible experience! The product broke after one day and the support team was unhelpful. Very disappointed and will not purchase again."
}

negative_feedback_response = {
    "sentiment": "negative",
    "confidence": 0.82,
    "polarity": -0.65,
    "subjectivity": 0.70,
    "keywords": [
        "product",
        "support team",
        "experience",
        "terrible",
        "unhelpful",
        "disappointed"
    ],
    "success": True,
    "message": "Feedback analysis completed successfully"
}

# Example 3: Neutral feedback
neutral_feedback_request = {
    "feedback": "The product arrived on time. It works as described. Nothing special but it does the job."
}

neutral_feedback_response = {
    "sentiment": "neutral",
    "confidence": 0.45,
    "polarity": 0.05,
    "subjectivity": 0.40,
    "keywords": [
        "product",
        "job",
        "time"
    ],
    "success": True,
    "message": "Feedback analysis completed successfully"
}

# Example 4: Mixed feedback
mixed_feedback_request = {
    "feedback": "The design is beautiful and modern, but the price is too high for what you get. The delivery was fast though."
}

mixed_feedback_response = {
    "sentiment": "positive",
    "confidence": 0.58,
    "polarity": 0.15,
    "subjectivity": 0.55,
    "keywords": [
        "design",
        "price",
        "delivery",
        "beautiful",
        "modern"
    ],
    "success": True,
    "message": "Feedback analysis completed successfully"
}


# Example cURL command:
"""
curl -X POST "http://localhost:8000/api/nlp/feedback" \\
     -H "Content-Type: application/json" \\
     -d '{
       "feedback": "I absolutely love this product! The quality is excellent and the customer service was outstanding. Highly recommend to everyone!"
     }'
"""

# Example Python requests:
"""
import requests

url = "http://localhost:8000/api/nlp/feedback"
payload = {
    "feedback": "I absolutely love this product! The quality is excellent and the customer service was outstanding. Highly recommend to everyone!"
}

response = requests.post(url, json=payload)
print(response.json())
"""

