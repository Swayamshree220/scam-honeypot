import os
from dotenv import load_dotenv

# Load variables from .env if running locally
load_dotenv()

class Config:
    """Application configuration for Scam Honeypot"""
    
    # Flask Settings
    # Use a secure key in production; defaults to 'dev-secret-key'
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Groq API Configuration (Updated for 2026)
    # The llama-3.1-70b-versatile model was deprecated in 2025.
    # llama-3.3-70b-versatile is the current stable workhorse.
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')
    
    # Startup check for Groq Key
    if not GROQ_API_KEY:
        print("❌ ERROR: GROQ_API_KEY is not set in environment variables!")
    else:
        # Prints first 10 characters to verify key loading without exposing it
        print(f"✅ GROQ_API_KEY loaded successfully: {GROQ_API_KEY[:10]}...")

    # API Security (For X-API-Key header)
    API_KEY = os.getenv('API_KEY', 'scam-honeypot-secret-key-12345')
    
    # Mock Scammer API (Optional integrations)
    MOCK_SCAMMER_API_URL = os.getenv('MOCK_SCAMMER_API_URL')
    MOCK_SCAMMER_API_KEY = os.getenv('MOCK_SCAMMER_API_KEY')
    
    # Application Logic & AI Parameters
    MAX_CONVERSATION_TURNS = 10
    RESPONSE_TIMEOUT = 30  # Seconds before giving up on an AI response
    MAX_TOKENS = 500       # Increased from 200 for more natural dialogue
    TEMPERATURE = 0.7      # Balanced between creative and predictable
