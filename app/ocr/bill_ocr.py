"""
OCR module for bill processing.
Extracts text from images and parses structured data.
"""
import re
import logging
from typing import List, Optional
import pytesseract
from PIL import Image
import io

from app.schemas import ServiceItem

logger = logging.getLogger(__name__)


def extract_text_from_image(image_bytes: bytes) -> str:
    """
    Extract raw text from image using pytesseract.
    
    Args:
        image_bytes: Image file as bytes
        
    Returns:
        Extracted text string
        
    Raises:
        Exception: If OCR processing fails
    """
    try:
        image = Image.open(io.BytesIO(image_bytes))
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        logger.error(f"OCR extraction failed: {str(e)}")
        raise Exception(f"Failed to extract text from image: {str(e)}")


def parse_services(text: str) -> List[ServiceItem]:
    """
    Parse service names and prices from text using regex.
    
    Looks for patterns like:
    - Service Name $XX.XX
    - Service Name XX.XX
    - Service Name: $XX.XX
    
    Args:
        text: Raw OCR text
        
    Returns:
        List of ServiceItem objects
    """
    services = []
    
    # Pattern to match service names followed by prices
    # Matches: service name (with spaces, dashes, etc.) followed by currency symbol and price
    price_patterns = [
        # Pattern 1: Service Name $XX.XX or Service Name $XX
        r'([A-Za-z0-9\s\-&,\.]+?)\s+\$?(\d+\.?\d{0,2})',
        # Pattern 2: Service Name: $XX.XX
        r'([A-Za-z0-9\s\-&,\.]+?):\s+\$?(\d+\.?\d{0,2})',
        # Pattern 3: Service Name - $XX.XX
        r'([A-Za-z0-9\s\-&,\.]+?)\s+-\s+\$?(\d+\.?\d{0,2})',
    ]
    
    seen_services = set()
    
    for pattern in price_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
        for match in matches:
            service_name = match.group(1).strip()
            price_str = match.group(2).strip()
            
            # Filter out common false positives
            if len(service_name) < 3:
                continue
            
            # Skip if it looks like a date or other non-service text
            if re.match(r'^\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4}$', service_name):
                continue
            
            try:
                price = float(price_str)
                # Only add if price is reasonable (between 0.01 and 999999)
                if 0.01 <= price <= 999999:
                    # Create a unique key to avoid duplicates
                    service_key = f"{service_name.lower()}_{price}"
                    if service_key not in seen_services:
                        seen_services.add(service_key)
                        services.append(ServiceItem(name=service_name, price=price))
            except ValueError:
                continue
    
    return services


def parse_date(text: str) -> Optional[str]:
    """
    Extract date from text using regex patterns.
    
    Looks for common date formats:
    - MM/DD/YYYY
    - DD/MM/YYYY
    - YYYY-MM-DD
    - Month DD, YYYY
    
    Args:
        text: Raw OCR text
        
    Returns:
        Date string if found, None otherwise
    """
    date_patterns = [
        # MM/DD/YYYY or MM-DD-YYYY
        r'\b(\d{1,2})[/\-](\d{1,2})[/\-](\d{2,4})\b',
        # YYYY-MM-DD
        r'\b(\d{4})[/\-](\d{1,2})[/\-](\d{1,2})\b',
        # Month DD, YYYY
        r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),?\s+(\d{4})\b',
    ]
    
    for pattern in date_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            date_str = match.group(0)
            # Validate that it's a reasonable date
            if len(date_str) >= 6:  # Minimum reasonable date length
                return date_str
    
    return None


def calculate_total_price(services: List[ServiceItem]) -> Optional[float]:
    """
    Calculate total price from list of services.
    
    Args:
        services: List of ServiceItem objects
        
    Returns:
        Total price or None if no services
    """
    if not services:
        return None
    return sum(service.price for service in services)

