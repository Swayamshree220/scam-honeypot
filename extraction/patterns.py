import re

# Regex patterns for extraction
PATTERNS = {
    'upi_id': r'\b[\w\.-]+@[\w\.-]+\b',
    'bank_account': r'\b\d{9,18}\b',
    'phone_indian': r'\b(?:\+91|0)?[6-9]\d{9}\b',
    'phone_international': r'\+\d{1,3}\d{6,14}\b',
    'url': r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
    'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    'ifsc': r'\b[A-Z]{4}0[A-Z0-9]{6}\b',
}

def extract_by_pattern(text, pattern_name):
    """Extract data using regex pattern"""
    pattern = PATTERNS.get(pattern_name)
    if not pattern:
        return []
    
    matches = re.findall(pattern, text, re.IGNORECASE)
    return list(set(matches))  # Remove duplicates