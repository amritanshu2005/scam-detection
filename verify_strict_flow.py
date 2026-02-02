import requests
import json
import time

# Configuration
API_URL = "http://localhost:8000/api/v1/message"
# Assuming API_KEY is set in environment or default
API_KEY = "your-secret-api-key-here"

def test_hackathon_flow():
    print("Testing Hackathon API Flow (Strict Mode)...")

    # payload matching hackathon schema
    payload = {
        "sessionId": "strict-session-456",
        "message": {
            "sender": "scammer",
            "text": "Your account is blocked. Verify immediately.",
            "timestamp": "2023-10-27T10:00:00Z"
        },
        "conversationHistory": [],
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
        data = response.json()
        assert "status" in data
        assert "reply" in data
        assert data["status"] == "success"
        assert "Why will my account be blocked?" in data["reply"]

        print("✅ API Response format & Logic correct.")

    except Exception as e:
        print(f"❌ API Request failed: {e}")

if __name__ == "__main__":
    test_hackathon_flow()
