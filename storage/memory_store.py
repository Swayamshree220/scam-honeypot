from datetime import datetime
from typing import Dict, List, Optional

class ConversationStore:
    """In-memory conversation storage"""
    
    def __init__(self):
        self.conversations: Dict[str, dict] = {}
    
    def create(self, conv_id: str) -> dict:
        """Create new conversation"""
        self.conversations[conv_id] = {
            'id': conv_id,
            'history': [],
            'extracted_intel': {},
            'scam_type': None,
            'created_at': datetime.now().isoformat(),
            'status': 'active'
        }
        return self.conversations[conv_id]
    
    def get(self, conv_id: str) -> Optional[dict]:
        """Get conversation by ID"""
        return self.conversations.get(conv_id)
    
    def add_turn(self, conv_id: str, scammer_msg: str, agent_msg: str):
        """Add conversation turn"""
        if conv_id not in self.conversations:
            self.create(conv_id)
        
        self.conversations[conv_id]['history'].append({
            'scammer': scammer_msg,
            'agent': agent_msg,
            'timestamp': datetime.now().isoformat()
        })
    
    def get_all(self) -> List[dict]:
        """Get all conversations"""
        return list(self.conversations.values())
    
    def get_stats(self) -> dict:
        """Get statistics"""
        return {
            'total_conversations': len(self.conversations),
            'active_conversations': sum(
                1 for c in self.conversations.values() 
                if c['status'] == 'active'
            ),
            'total_intel_extracted': sum(
                len(c.get('extracted_intel', {})) 
                for c in self.conversations.values()
            )
        }

# Global instance
conversation_store = ConversationStore()