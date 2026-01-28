import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    # Groq (FREE & FAST)
    # Try both ways to get the API key
    GROQ_API_KEY = os.getenv('GROQ_API_KEY') or os.environ.get('GROQ_API_KEY')
    
    # Add a check to make sure we have the key
    if not GROQ_API_KEY:
        print("❌ ERROR: GROQ_API_KEY is not set!")
    else:
        print(f"✅ GROQ_API_KEY loaded: {GROQ_API_KEY[:10]}...")
    
    GROQ_MODEL = 'llama-3.1-70b-versatile'  # Fast and smart
    
    # API Security
    API_KEY = os.getenv('API_KEY', 'scam-honeypot-secret-key-12345')
    
    # Mock Scammer API
    MOCK_SCAMMER_API_URL = os.getenv('MOCK_SCAMMER_API_URL')
    MOCK_SCAMMER_API_KEY = os.getenv('MOCK_SCAMMER_API_KEY')
    
    # Application
    MAX_CONVERSATION_TURNS = 10
    RESPONSE_TIMEOUT = 30
    MAX_TOKENS = 200
    TEMPERATURE = 0.7
