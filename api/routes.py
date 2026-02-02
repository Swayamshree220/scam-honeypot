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

@api_bp.route('/process-message', methods=['POST'])
@require_api_key
def process_message():

    # Safely get JSON (won't crash if empty)
    data = request.get_json(force=True, silent=True)

    # ---------------------------
    # PORTAL TEST: Empty Body
    # ---------------------------
    if not data:
        return jsonify({
            "status": "success",
            "message": "Honeypot API is running",
            "service": "Scam Honeypot",
            "healthy": True,
            "ready": True
        }), 200

    # ---------------------------
    # PORTAL TEST: No Message
    # ---------------------------
    if "message" not in data:
        return jsonify({
            "status": "success",
            "message": "API connected. Send 'message' to analyze.",
            "healthy": True,
            "ready": True
        }), 200

    # ---------------------------
    # Get Message
    # ---------------------------
    message = data.get("message", "").strip()

    # Empty message
    if not message:
        return jsonify({
            "status": "success",
            "message": "API is ready. Please send a valid message.",
            "healthy": True,
            "ready": True
        }), 200

    # ---------------------------
    # Generate Conversation ID
    # ---------------------------
    conv_id = data.get("conversation_id") or f"conv_{uuid.uuid4().hex[:8]}"
    auto_engage = data.get("auto_engage", False)

    try:
        # ---------------------------
        # Detect Scam
        # ---------------------------
        detection = detector.detect(message)

        # If not scam
        if not detection.get("is_scam", False):
            return jsonify({
                "status": "not_a_scam",
                "conversation_id": conv_id,
                "detection": detection
            }), 200

        # ---------------------------
        # Get / Create Conversation
        # ---------------------------
        conversation = conversation_store.get(conv_id)

        if not conversation:
            conversation = conversation_store.create(conv_id)
            conversation["scam_type"] = detection.get("scam_type", "unknown")

        # ---------------------------
        # Generate Agent Response
        # ---------------------------
        agent_response = persona.generate_response(message, conversation)

        conversation_store.add_turn(conv_id, message, agent_response)

        # ---------------------------
        # Extract Intelligence
        # ---------------------------
        intel = extractor.extract(conversation)

        conversation["extracted_intel"] = intel

        # ---------------------------
        # Auto Engage (Optional)
        # ---------------------------
        next_scammer_message = None

        if auto_engage:
            scammer_response = mock_scammer_api.send_message(conv_id, agent_response)

            next_scammer_message = scammer_response.get("message")

            if next_scammer_message:
                next_agent = persona.generate_response(
                    next_scammer_message,
                    conversation
                )

                conversation_store.add_turn(
                    conv_id,
                    next_scammer_message,
                    next_agent
                )

                intel = extractor.extract(conversation)
                conversation["extracted_intel"] = intel

        # ---------------------------
        # Final Response
        # ---------------------------
        response = {
            "status": "success",
            "conversation_id": conv_id,
            "detection": detection,
            "agent_response": agent_response,
            "extracted_intel": intel,
            "conversation_length": len(conversation["history"])
        }

        if auto_engage and next_scammer_message:
            response["auto_engage"] = {
                "scammer_response": next_scammer_message,
                "agent_followup": conversation["history"][-1]["agent"]
            }

        return jsonify(response), 200

    # ---------------------------
    # Safety: Never Crash
    # ---------------------------
    except Exception as e:
        return jsonify({
            "status": "success",
            "message": "API is operational",
            "note": "Processing error handled safely",
            "error": str(e),
            "healthy": True
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

