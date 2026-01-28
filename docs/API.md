# Scam Honeypot API Documentation

## Authentication

All endpoints (except `/health`) require an API key in the request headers:
```
X-API-Key: your-api-key-here
```

## Endpoints

### 1. Health Check
**GET** `/api/health`

No authentication required.

**Response:**
```json
{
  "status": "healthy",
  "service": "Scam Honeypot API",
  "version": "1.0.0"
}
```

---

### 2. Process Message (Manual)
**POST** `/api/process-message`

Process a single scam message and get agent response.

**Request:**
```json
{
  "message": "You won Rs 10 lakhs! Send bank details.",
  "conversation_id": "conv_abc123",  // optional
  "auto_engage": false
}
```

**Response:**
```json
{
  "status": "success",
  "conversation_id": "conv_abc123",
  "detection": {
    "is_scam": true,
    "confidence": 0.95,
    "scam_type": "lottery",
    "reasoning": "Message contains prize/lottery keywords"
  },
  "agent_response": "Wow really sir? How I won? I not remember entering lottery...",
  "extracted_intel": {
    "upi_ids": [],
    "bank_accounts": [],
    "phone_numbers": [],
    "urls": []
  },
  "conversation_length": 1
}
```

---

### 3. Autonomous Engagement
**POST** `/api/autonomous-engage`

Let the AI handle the full conversation autonomously.

**Request:**
```json
{
  "initial_message": "You won Rs 10 lakhs! Call 9876543210",
  "max_turns": 5
}
```

**Response:**
```json
{
  "status": "success",
  "conversation_id": "conv_xyz789",
  "detection": { ... },
  "full_conversation": [
    {
      "scammer": "You won Rs 10 lakhs!",
      "agent": "Really? How sir?",
      "timestamp": "2026-01-28T10:30:00"
    },
    ...
  ],
  "extracted_intel": {
    "upi_ids": ["scammer@paytm"],
    "phone_numbers": ["9876543210"],
    "urls": ["fake-lottery.com"]
  },
  "total_turns": 4,
  "summary": "Engaged scammer for 4 turns. Extracted 3 pieces of intelligence."
}
```

---

### 4. Get All Conversations
**GET** `/api/conversations`

Retrieve all stored conversations.

**Response:**
```json
{
  "status": "success",
  "conversations": [ ... ],
  "total": 15
}
```

---

### 5. Get Specific Conversation
**GET** `/api/conversation/<conv_id>`

**Response:**
```json
{
  "status": "success",
  "conversation": { ... }
}
```

---

### 6. Get Statistics
**GET** `/api/stats`

**Response:**
```json
{
  "status": "success",
  "stats": {
    "total_conversations": 25,
    "active_conversations": 5,
    "total_intel_items": 67,
    "scam_types_breakdown": {
      "lottery": 10,
      "banking": 8,
      "tech_support": 7
    },
    "avg_turns_per_conversation": 3.2
  }
}
```
