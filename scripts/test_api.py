import requests
import json

BASE_URL = 'http://localhost:5000/api'
API_KEY = 'scam-honeypot-secret-key-12345'

headers = {
    'X-API-Key': API_KEY,
    'Content-Type': 'application/json'
}

print("Testing Scam Honeypot API...\n")

# Test 1: Health check
print("1. Health Check:")
response = requests.get(f'{BASE_URL}/health')
print(json.dumps(response.json(), indent=2))
print()

# Test 2: Process message
print("2. Process Message:")
response = requests.post(
    f'{BASE_URL}/process-message',
    headers=headers,
    json={
        'message': 'Congratulations! You won Rs 10 lakhs. Send bank details to claim prize at winner@paytm or call 9876543210!',
        'auto_engage': False
    }
)
print(json.dumps(response.json(), indent=2))
print()

# Test 3: Autonomous engagement
print("3. Autonomous Engagement:")
response = requests.post(
    f'{BASE_URL}/autonomous-engage',
    headers=headers,
    json={
        'initial_message': 'Your bank account will be blocked! Update KYC at fake-bank.com immediately!',
        'max_turns': 3
    }
)
result = response.json()
print(f"Status: {result['status']}")
print(f"Turns: {result['total_turns']}")
print(f"Intel Extracted: {sum(len(v) for v in result['extracted_intel'].values())}")
print()

# Test 4: Get stats
print("4. Statistics:")
response = requests.get(f'{BASE_URL}/stats', headers=headers)
print(json.dumps(response.json(), indent=2))