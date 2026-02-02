import requests
import json
import time
from unittest.mock import MagicMock

# Configuration
API_URL = "http://localhost:8000/api/v1/message"
API_KEY = "your-secret-api-key-here"

def test_hackathon_flow():
    print("Testing Hackathon API Flow...")

    # payload matching hackathon schema
    payload = {
        "sessionId": "test-session-123",
        "message": {
            "sender": "scammer",
            "text": "Hello, your bank account is blocked. Update immediately.",
            "timestamp": "2023-10-27T10:00:00Z"
        },
        "conversationHistory": [
            {
                "sender": "scammer",
                "text": "Hello",
                "timestamp": "2023-10-27T09:59:00Z"
            }
        ],
        "metadata": {}
    }

    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)

        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")

        assert response.status_code == 200
        assert "status" in response.json()
        assert "reply" in response.json()
        assert response.json()["status"] == "success"

        print("✅ API Response format correct.")

    except Exception as e:
        print(f"❌ API Request failed: {e}")

if __name__ == "__main__":
    # Wait for server to start (manual start required or use subprocess)
    print("Ensure server is running on port 8000")
    test_hackathon_flow()
