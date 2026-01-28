from functools import wraps
from flask import request, jsonify
import os

API_KEY = os.getenv('API_KEY', 'scam-honeypot-secret-key-12345')

# DEBUG: Print the API key on startup
print(f"🔑 Backend expecting API_KEY: {API_KEY}")

def require_api_key(f):
    """Decorator to require API key for endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check for API key in headers
        api_key = request.headers.get('X-API-Key')
        
        # DEBUG
        print(f"🔍 Received API key: {api_key}")
        print(f"🔍 Expected API key: {API_KEY}")
        print(f"🔍 Match: {api_key == API_KEY}")
        
        if not api_key:
            return jsonify({
                'error': 'Missing API key',
                'message': 'Please provide X-API-Key header'
            }), 401
        
        if api_key != API_KEY:
            return jsonify({
                'error': 'Invalid API key',
                'message': 'The provided API key is not valid'
            }), 403
        
        return f(*args, **kwargs)
    
    return decorated_function
