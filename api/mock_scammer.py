import requests
from config import Config

class MockScammerAPI:
    """Integration with Mock Scammer API"""
    
    def __init__(self):
        self.base_url = Config.MOCK_SCAMMER_API_URL
        self.api_key = Config.MOCK_SCAMMER_API_KEY
    
    def send_message(self, conversation_id, agent_message):
        """Send agent message to mock scammer and get response"""
        
        if not self.base_url:
            # Fallback for testing without actual API
            return self._mock_response(agent_message)
        
        try:
            response = requests.post(
                f"{self.base_url}/respond",
                json={
                    'conversation_id': conversation_id,
                    'message': agent_message
                },
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                },
                timeout=10
            )
            
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            print(f"Mock Scammer API error: {e}")
            return self._mock_response(agent_message)
    
    def _mock_response(self, agent_message):
        """Generate mock scammer response for testing"""
        
        # Simple rule-based mock responses
        message_lower = agent_message.lower()
        
        if 'how' in message_lower or 'what' in message_lower:
            return {
                'message': 'Sir, very simple process. Just send your bank account number and IFSC code to my UPI: scammer123@paytm. We will transfer money immediately!',
                'scammer_id': 'mock_scammer_001'
            }
        
        elif 'son' in message_lower or 'check' in message_lower or 'family' in message_lower:
            return {
                'message': 'No need sir! This is 100% government approved. Your son will also say same thing. Just send details now before offer expires!',
                'scammer_id': 'mock_scammer_001'
            }
        
        elif 'safe' in message_lower or 'trust' in message_lower:
            return {
                'message': 'Yes sir, completely safe! Just click this link: http://fake-lottery-claim.com/verify and enter your card details. Or call me at 9876543210.',
                'scammer_id': 'mock_scammer_001'
            }
        
        else:
            return {
                'message': 'Sir please hurry! Send Rs 1000 processing fee to winner2024@paytm to claim your Rs 10 lakh prize. Limited time offer!',
                'scammer_id': 'mock_scammer_001'
            }

# Global instance
mock_scammer_api = MockScammerAPI()