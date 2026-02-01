"""
Simple test script for the Agentic Honey-Pot API
Run this after starting the server to test the endpoints
"""

import requests
import json
import time

# Configuration
API_BASE_URL = "http://localhost:8000"
API_KEY = "your-secret-api-key-here"  # Change this to match your .env file

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}


def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check endpoint...")
    response = requests.get(f"{API_BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_scam_message():
    """Test with a scam message"""
    print("Testing scam message detection...")
    
    test_messages = [
        "Your bank account has been suspended. Click here to verify: http://fake-bank.com/verify",
        "You have won 1 lakh rupees! Send your bank account number to claim.",
        "Urgent: Your UPI needs verification. Share your UPI ID immediately.",
    ]
    
    conversation_id = None
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n--- Message {i} ---")
        print(f"Input: {message}")
        
        payload = {
            "message": message
        }
        
        if conversation_id:
            payload["conversation_id"] = conversation_id
        
        response = requests.post(
            f"{API_BASE_URL}/api/v1/message",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            data = response.json()
            conversation_id = data["conversation_id"]
            
            print(f"Scam Detected: {data['scam_detected']}")
            print(f"Agent Activated: {data['agent_activated']}")
            print(f"Agent Response: {data['response_message']}")
            print(f"Turn Count: {data['engagement_metrics']['turn_count']}")
            print(f"Intelligence Found:")
            print(f"  - Bank Accounts: {data['extracted_intelligence']['bank_accounts']}")
            print(f"  - UPI IDs: {data['extracted_intelligence']['upi_ids']}")
            print(f"  - Phishing URLs: {data['extracted_intelligence']['phishing_urls']}")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
        
        time.sleep(1)  # Small delay between messages


def test_conversation_retrieval(conversation_id):
    """Test retrieving conversation history"""
    if not conversation_id:
        print("No conversation ID to retrieve")
        return
    
    print(f"\nRetrieving conversation {conversation_id}...")
    response = requests.get(
        f"{API_BASE_URL}/api/v1/conversation/{conversation_id}",
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"Conversation Status:")
        print(f"  - Scam Detected: {data['scam_detected']}")
        print(f"  - Agent Activated: {data['agent_activated']}")
        print(f"  - Turn Count: {data['turn_count']}")
        print(f"  - Messages: {len(data['messages'])}")
        print(f"  - Intelligence: {json.dumps(data['intelligence'], indent=4)}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


if __name__ == "__main__":
    print("=" * 60)
    print("Agentic Honey-Pot API Test Script")
    print("=" * 60)
    print()
    
    # Test health check
    test_health_check()
    
    # Test scam detection
    test_scam_message()
    
    print("\n" + "=" * 60)
    print("Tests completed!")
    print("=" * 60)

