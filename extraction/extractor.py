from groq import Groq
import json
from config import Config
from .patterns import extract_by_pattern, PATTERNS

class IntelligenceExtractor:
    """Extract sensitive information from conversations"""
    
    def __init__(self):
        self.client = Groq(api_key=Config.GROQ_API_KEY)
    
    def extract(self, conversation):
        """Extract intelligence from conversation history"""
        
        if not conversation or not conversation.get('history'):
            return self._empty_intel()
        
        # Combine all messages
        all_text = self._combine_messages(conversation['history'])
        
        # Regex-based extraction
        regex_intel = self._regex_extraction(all_text)
        
        # AI-powered extraction
        ai_intel = self._ai_extraction(all_text)
        
        # Merge results
        merged = self._merge_intel(regex_intel, ai_intel)
        
        return merged
    
    def _combine_messages(self, history):
        """Combine all conversation messages"""
        messages = []
        for turn in history:
            messages.append(turn.get('scammer', ''))
            messages.append(turn.get('agent', ''))
        return ' '.join(messages)
    
    def _regex_extraction(self, text):
        """Extract using regex patterns"""
        return {
            'upi_ids': extract_by_pattern(text, 'upi_id'),
            'bank_accounts': extract_by_pattern(text, 'bank_account'),
            'phone_numbers': (
                extract_by_pattern(text, 'phone_indian') + 
                extract_by_pattern(text, 'phone_international')
            ),
            'urls': extract_by_pattern(text, 'url'),
            'emails': extract_by_pattern(text, 'email'),
            'ifsc_codes': extract_by_pattern(text, 'ifsc'),
        }
    
    def _ai_extraction(self, text):
        """Extract using AI"""
        try:
            prompt = f"""Extract sensitive information from this conversation between a scammer and victim:

{text}

Find and return ONLY a valid JSON object (no markdown, no extra text):
{{
    "upi_ids": ["list of UPI IDs like user@paytm"],
    "bank_accounts": ["list of account numbers"],
    "phone_numbers": ["list of phone numbers"],
    "urls": ["list of URLs/links"],
    "emails": ["list of email addresses"],
    "ifsc_codes": ["list of IFSC codes"],
    "payment_methods": ["any other payment info mentioned"]
}}"""

            response = self.client.chat.completions.create(
                model=Config.GROQ_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=500
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Clean JSON
            result_text = result_text.replace('```json', '').replace('```', '').strip()
            
            return json.loads(result_text)
            
        except Exception as e:
            print(f"AI extraction error: {e}")
            return {}
    
    def _merge_intel(self, regex_intel, ai_intel):
        """Merge regex and AI results"""
        merged = {}
        
        all_keys = set(regex_intel.keys()) | set(ai_intel.keys())
        
        for key in all_keys:
            regex_items = regex_intel.get(key, [])
            ai_items = ai_intel.get(key, [])
            
            # Combine and deduplicate
            combined = list(set(regex_items + ai_items))
            
            # Filter out empty/invalid
            combined = [item for item in combined if item and len(item) > 2]
            
            merged[key] = combined
        
        return merged
    
    def _empty_intel(self):
        """Return empty intelligence structure"""
        return {
            'upi_ids': [],
            'bank_accounts': [],
            'phone_numbers': [],
            'urls': [],
            'emails': [],
            'ifsc_codes': [],
            'payment_methods': []
        }