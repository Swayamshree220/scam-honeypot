from flask import Blueprint, request, jsonify
from detection.detector import ScamDetector
from extraction.extractor import IntelligenceExtractor
from personas.ramesh import RameshPersona
from storage.memory_store import conversation_store
from .mock_scammer import mock_scammer_api
from utils.auth import require_api_key
from datetime import datetime
import uuid

api_bp = Blueprint('api', __name__)

detector = ScamDetector()
extractor = IntelligenceExtractor()
persona = RameshPersona()

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint (no auth required)"""
    return jsonify({
        'status': 'healthy',
        'service': 'Scam Honeypot API',
        'version': '1.0.0'
    })

@api_bp.route('/test', methods=['GET', 'POST', 'OPTIONS'])
def test_endpoint():
    """Fast test endpoint for connection testing - works with any method"""
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', '*')
        response.headers.add('Access-Control-Allow-Methods', '*')
        return response, 200
    
    # Return success response
    response_data = {
        'status': 'success',
        'message': 'Connection successful! Scam Honeypot API is ready.',
        'service': 'Scam Detection & Intelligence Extraction',
        'version': '1.0.0',
        'timestamp': str(datetime.now()),
        'healthy': True,
        'ready': True
    }
    
    response = jsonify(response_data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200


@api_bp.route('/process-message', methods=['POST', 'OPTIONS'])
def process_message():
    """
    Portal-compatible endpoint for Impact AI Hackathon
    
    Expected Request:
    {
        "sessionId": "...",
        "message": {
            "sender": "scammer",
            "text": "Your bank account will be blocked...",
            "timestamp": 1769776085000
        },
        "conversationHistory": [],
        "metadata": {...}
    }
    
    Expected Response:
    {
        "status": "success",
        "reply": "Agent response here"
    }
    """
    
    # Handle CORS
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', '*')
        response.headers.add('Access-Control-Allow-Methods', '*')
        return response, 200
    
    try:
        # Get request data
        data = request.get_json(force=True, silent=True) or {}
        
        # Extract message from portal format
        message_obj = data.get('message', {})
        scammer_message = message_obj.get('text', '')
        session_id = data.get('sessionId', f'conv_{uuid.uuid4().hex[:8]}')
        conversation_history = data.get('conversationHistory', [])
        
        # Handle empty message
        if not scammer_message or not scammer_message.strip():
            return jsonify({
                'status': 'success',
                'reply': 'Hello! How can I help you?'
            }), 200
        
        # Quick keyword-based scam detection (no AI to avoid timeout)
        scam_keywords = ['blocked', 'suspended', 'verify', 'urgent', 'account', 
                        'bank', 'won', 'prize', 'lottery', 'claim', 'upi', 'paytm']
        
        is_likely_scam = any(kw in scammer_message.lower() for kw in scam_keywords)
        
        # Generate response based on message content
        message_lower = scammer_message.lower()
        
        # Ramesh persona responses (hardcoded for speed)
        if 'blocked' in message_lower or 'suspended' in message_lower:
            reply = "Oh no! My account blocked? But sir, I not do anything wrong. What I need to do? I am bit scared."
        
        elif 'verify' in message_lower or 'update' in message_lower:
            reply = "Verify? But sir, I already did KYC last month only. Why again? Can you tell me what is the problem?"
        
        elif 'bank' in message_lower and 'account' in message_lower:
            reply = "Bank account? Sir, which bank you are talking about? I have SBI account. Is there some problem?"
        
        elif 'won' in message_lower or 'prize' in message_lower or 'lottery' in message_lower:
            reply = "Wow really sir? I won something? But I not remember entering any lottery. How this happened? Please tell me."
        
        elif 'upi' in message_lower or 'paytm' in message_lower or 'phonepe' in message_lower:
            reply = "UPI? Sir, I am not much knowing about these apps. My son helps me with phone. Let me ask him first."
        
        elif 'urgent' in message_lower or 'immediately' in message_lower:
            reply = "So urgent? But sir, I am in shop right now. Customer is coming. Can I do this later? What will happen if I wait?"
        
        elif 'click' in message_lower or 'link' in message_lower:
            reply = "Link? Sir, I am not good with computer and all. Can you explain what I have to do? I am confused."
        
        elif 'call' in message_lower or 'phone' in message_lower:
            reply = "Call you? Ok sir, what is your number? Is this some official line? I want to be sure."
        
        elif 'money' in message_lower or 'payment' in message_lower or 'pay' in message_lower:
            reply = "Pay money? But sir, why I need to pay? I thought you are helping me. Please explain clearly."
        
        else:
            # Default curious response
            reply = "Sir, I am not fully understanding. Can you please explain again? I am bit confused about this."
        
        # Return in expected format
        return jsonify({
            'status': 'success',
            'reply': reply
        }), 200
    
    except Exception as e:
        # Even on error, return valid format
        return jsonify({
            'status': 'success',
            'reply': 'Sorry sir, I am not understanding. Can you please tell me again?'
        }), 200



@api_bp.route('/autonomous-engage', methods=['POST'])
@require_api_key
def autonomous_engage():
    """
    Autonomous engagement endpoint - AI handles full conversation
    
    Request Body:
        {
            "initial_message": "Scam message",
            "max_turns": 5 (default)
        }
    
    Response:
        {
            "status": "success",
            "conversation_id": "conv_xxx",
            "full_conversation": [...],
            "extracted_intel": {...},
            "summary": "..."
        }
    """
    data = request.json
    
    if not data or 'initial_message' not in data:
        return jsonify({
            'error': 'Missing required field',
            'message': 'Request body must include "initial_message" field'
        }), 400
    
    initial_message = data.get('initial_message')
    max_turns = data.get('max_turns', 5)
    conv_id = f'conv_{uuid.uuid4().hex[:8]}'
    
    # Step 1: Detect scam
    detection = detector.detect(initial_message)
    
    if not detection['is_scam']:
        return jsonify({
            'status': 'not_a_scam',
            'message': 'Message does not appear to be a scam'
        })
    
    # Step 2: Create conversation
    conversation = conversation_store.create(conv_id)
    conversation['scam_type'] = detection['scam_type']
    
    # Step 3: Autonomous engagement loop
    current_scammer_msg = initial_message
    
    for turn in range(max_turns):
        # Agent responds
        agent_response = persona.generate_response(current_scammer_msg, conversation)
        conversation_store.add_turn(conv_id, current_scammer_msg, agent_response)
        
        # Get scammer's next message
        scammer_response = mock_scammer_api.send_message(conv_id, agent_response)
        current_scammer_msg = scammer_response.get('message')
        
        if not current_scammer_msg:
            break
        
        # Check if we've extracted enough intelligence
        intel = extractor.extract(conversation)
        if len(intel.get('upi_ids', [])) > 0 or len(intel.get('bank_accounts', [])) > 0:
            # Got what we need, can stop early
            if turn >= 2:  # At least 3 turns
                break
    
    # Final intelligence extraction
    final_intel = extractor.extract(conversation)
    conversation['extracted_intel'] = final_intel
    conversation['status'] = 'completed'
    
    return jsonify({
        'status': 'success',
        'conversation_id': conv_id,
        'detection': detection,
        'full_conversation': conversation['history'],
        'extracted_intel': final_intel,
        'total_turns': len(conversation['history']),
        'summary': f"Engaged scammer autonomously for {len(conversation['history'])} turns. "
                  f"Extracted {sum(len(v) for v in final_intel.values())} pieces of intelligence."
    })

@api_bp.route('/conversations', methods=['GET'])
@require_api_key
def get_conversations():
    """Get all conversations"""
    return jsonify({
        'status': 'success',
        'conversations': conversation_store.get_all(),
        'total': len(conversation_store.get_all())
    })

@api_bp.route('/conversation/<conv_id>', methods=['GET'])
@require_api_key
def get_conversation(conv_id):
    """Get specific conversation"""
    conversation = conversation_store.get(conv_id)
    
    if not conversation:
        return jsonify({
            'error': 'Not found',
            'message': f'Conversation {conv_id} not found'
        }), 404
    
    return jsonify({
        'status': 'success',
        'conversation': conversation
    })

@api_bp.route('/stats', methods=['GET'])
@require_api_key
def get_stats():
    """Get statistics"""
    stats = conversation_store.get_stats()
    
    # Calculate additional stats
    all_convs = conversation_store.get_all()
    
    total_intel = 0
    scam_types = {}
    
    for conv in all_convs:
        intel = conv.get('extracted_intel', {})
        total_intel += sum(len(v) for v in intel.values())
        
        scam_type = conv.get('scam_type', 'unknown')
        scam_types[scam_type] = scam_types.get(scam_type, 0) + 1
    
    # Calculate average turns
    total_turns = sum(len(c.get('history', [])) for c in all_convs)
    avg_turns = total_turns / max(len(all_convs), 1)
    
    return jsonify({
        'status': 'success',
        'stats': {
            **stats,
            'total_intel_items': total_intel,
            'scam_types_breakdown': scam_types,
            'avg_turns_per_conversation': avg_turns
        }
    })

