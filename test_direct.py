#!/usr/bin/env python
"""Direct API test"""
import sys
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Test the endpoint
response = client.post(
    "/api/v1/message",
    json={
        "sessionId": "test-001",
        "message": {
            "sender": "scammer",
            "text": "Hello verify account!",
            "timestamp": "2026-02-05T10:00:00Z"
        },
        "conversationHistory": []
    },
    headers={"X-API-Key": "test-api-key-12345"}
)

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
