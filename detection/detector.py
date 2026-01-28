from groq import Groq
import json
from config import Config
from .keywords import SCAM_KEYWORDS, SCAM_TYPES

class ScamDetector:
    """Main scam detection class"""
    
    def __init__(self):
        self.client = Groq(api_key=Config.GROQ_API_KEY)
    
    def detect(self, message):
        """Detect if message is a scam"""
        
        # Quick keyword check
        keyword_score, matched_type = self._keyword_check(message)
        
        # If keyword score is high enough, it's definitely a scam
        if keyword_score >= 0.4:  # Lowered threshold
            return {
                'is_scam': True,
                'confidence': min(keyword_score + 0.3, 0.95),
                'scam_type': matched_type or 'fraud',
                'reasoning': f'Message contains multiple scam indicators: prize/money requests, urgency, payment details',
                'keyword_matches': keyword_score
            }
        
        # AI-powered detection for borderline cases
        ai_result = self._ai_detect(message)
        
        # Combine results - be more aggressive
        is_scam = ai_result.get('is_scam', False) or keyword_score > 0.3
        
        return {
            'is_scam': is_scam,
            'confidence': max(ai_result.get('confidence', 0), keyword_score + 0.2),
            'scam_type': ai_result.get('scam_type', matched_type or 'fraud'),
            'reasoning': ai_result.get('reasoning', f'Detected {int(keyword_score*10)} scam patterns'),
            'keyword_matches': keyword_score
        }
    
    def _keyword_check(self, message):
        """Quick keyword-based detection"""
        message_lower = message.lower()
        
        # High-confidence scam indicators
        high_confidence_keywords = [
            'won', 'prize', 'lottery', 'claim', 'winner',
            'bank account', 'send money', 'transfer', 'payment',
            'upi', '@paytm', '@phonepe', '@gpay',
            'urgent', 'immediately', 'blocked', 'suspended',
            'kyc', 'verify', 'update details'
        ]
        
        # Count high-confidence matches
        high_matches = sum(1 for kw in high_confidence_keywords if kw in message_lower)
        
        # Count all keyword matches
        all_matches = sum(1 for kw in SCAM_KEYWORDS if kw in message_lower)
        
        # Calculate score (more aggressive)
        score = min((high_matches * 0.3) + (all_matches * 0.15), 0.9)
        
        # Detect scam type
        scam_type = None
        for stype, keywords in SCAM_TYPES.items():
            if any(kw in message_lower for kw in keywords):
                scam_type = stype
                break
        
        # Special patterns that are almost always scams
        if any(pattern in message_lower for pattern in ['@paytm', '@phonepe', '@gpay']):
            score = max(score, 0.8)
            scam_type = scam_type or 'payment_fraud'
        
        if any(pattern in message_lower for pattern in ['won rs', 'won rupees', 'claim prize']):
            score = max(score, 0.8)
            scam_type = 'lottery'
        
        return score, scam_type
    
    def _ai_detect(self, message):
        """AI-powered detection using Groq"""
        try:
            prompt = f"""You are a scam detection AI. Analyze this message and determine if it's a scam.

Message: "{message}"

Common scam patterns:
- Lottery/prize winning messages
- Requests for bank details, UPI IDs, or payments
- Urgent account blocking/suspension warnings
- Too-good-to-be-true offers
- Requests to click links or call numbers
- Government/bank impersonation

Return ONLY valid JSON (no markdown):
{{
    "is_scam": true or false,
    "confidence": 0.0 to 1.0,
    "scam_type": "lottery" or "banking" or "payment_fraud" or "phishing" or "tech_support" or "job" or "none",
    "reasoning": "brief explanation"
}}

Be sensitive - if there's any suspicion of fraud, mark as scam."""

            response = self.client.chat.completions.create(
                model=Config.GROQ_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,  # Lower temperature for more consistent detection
                max_tokens=300
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Clean JSON
            result_text = result_text.replace('```json', '').replace('```', '').strip()
            
            # Try to parse JSON
            parsed = json.loads(result_text)
            
            # Boost confidence if AI says it's a scam
            if parsed.get('is_scam'):
                parsed['confidence'] = max(parsed.get('confidence', 0.5), 0.7)
            
            return parsed
            
        except Exception as e:
            print(f"AI detection error: {e}")
            # On error, be cautious and return uncertain
            return {
                'is_scam': True,  # Default to True for safety
                'confidence': 0.5,
                'scam_type': 'unknown',
                'reasoning': 'Could not analyze fully, treating as suspicious'
            }