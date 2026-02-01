"""
Comprehensive Test Suite for Agentic Honey-Pot System
"""

import pytest
import requests
import time
from typing import Dict, Any

API_BASE_URL = "http://localhost:8000"
API_KEY = "test-api-key-12345"

class TestScamDetection:
    """Test scam detection functionality"""
    
    def test_bank_suspension_scam(self):
        """Test detection of bank suspension scam"""
        response = requests.post(
            f"{API_BASE_URL}/api/v1/message",
            headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
            json={"message": "Your bank account has been suspended. Click here to verify: http://fake-bank.com"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["scam_detected"] == True
        assert data["agent_activated"] == True
        assert len(data["response_message"]) > 0
    
    def test_prize_winner_scam(self):
        """Test detection of prize winner scam"""
        response = requests.post(
            f"{API_BASE_URL}/api/v1/message",
            headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
            json={"message": "Congratulations! You won 1 lakh rupees! Send your bank account number."}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["scam_detected"] == True
    
    def test_upi_verification_scam(self):
        """Test detection of UPI verification scam"""
        response = requests.post(
            f"{API_BASE_URL}/api/v1/message",
            headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
            json={"message": "Urgent: Your UPI needs verification. Share your UPI ID: 9876543210@paytm"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["scam_detected"] == True

class TestIntelligenceExtraction:
    """Test intelligence extraction"""
    
    def test_bank_account_extraction(self):
        """Test bank account number extraction"""
        response = requests.post(
            f"{API_BASE_URL}/api/v1/message",
            headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
            json={"message": "Send money to account number 123456789012"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["extracted_intelligence"]["bank_accounts"]) > 0
    
    def test_upi_extraction(self):
        """Test UPI ID extraction"""
        response = requests.post(
            f"{API_BASE_URL}/api/v1/message",
            headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
            json={"message": "Send payment to UPI ID: user@paytm"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["extracted_intelligence"]["upi_ids"]) > 0
    
    def test_url_extraction(self):
        """Test phishing URL extraction"""
        response = requests.post(
            f"{API_BASE_URL}/api/v1/message",
            headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
            json={"message": "Click here: http://fake-bank-verify.com/secure"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["extracted_intelligence"]["phishing_urls"]) > 0

class TestMultiTurnConversation:
    """Test multi-turn conversation support"""
    
    def test_conversation_continuity(self):
        """Test conversation maintains context across turns"""
        # First message
        response1 = requests.post(
            f"{API_BASE_URL}/api/v1/message",
            headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
            json={"message": "Your account is suspended!"}
        )
        assert response1.status_code == 200
        data1 = response1.json()
        conversation_id = data1["conversation_id"]
        
        # Second message in same conversation
        response2 = requests.post(
            f"{API_BASE_URL}/api/v1/message",
            headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
            json={
                "message": "Verify at http://fake.com",
                "conversation_id": conversation_id
            }
        )
        assert response2.status_code == 200
        data2 = response2.json()
        assert data2["conversation_id"] == conversation_id
        assert data2["engagement_metrics"]["turn_count"] == 2

class TestAgentBehavior:
    """Test AI agent behavior"""
    
    def test_agent_activation(self):
        """Test agent activates when scam detected"""
        response = requests.post(
            f"{API_BASE_URL}/api/v1/message",
            headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
            json={"message": "You won a prize! Claim now!"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["scam_detected"] == True
        assert data["agent_activated"] == True
        assert len(data["response_message"]) > 0
    
    def test_agent_response_quality(self):
        """Test agent generates appropriate responses"""
        response = requests.post(
            f"{API_BASE_URL}/api/v1/message",
            headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
            json={"message": "Send your bank account number"}
        )
        assert response.status_code == 200
        data = response.json()
        # Response should be reasonable length
        assert 10 <= len(data["response_message"]) <= 300

class TestAPI:
    """Test API endpoints"""
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = requests.get(f"{API_BASE_URL}/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "active"
    
    def test_api_key_authentication(self):
        """Test API key authentication"""
        response = requests.post(
            f"{API_BASE_URL}/api/v1/message",
            headers={"X-API-Key": "wrong-key", "Content-Type": "application/json"},
            json={"message": "Test"}
        )
        assert response.status_code == 401
    
    def test_metrics_endpoint(self):
        """Test metrics endpoint"""
        response = requests.get(
            f"{API_BASE_URL}/api/v1/metrics",
            headers={"X-API-Key": API_KEY}
        )
        assert response.status_code == 200
        data = response.json()
        assert "performance" in data
        assert "conversations" in data

class TestPerformance:
    """Test system performance"""
    
    def test_response_time(self):
        """Test API response time is reasonable"""
        start = time.time()
        response = requests.post(
            f"{API_BASE_URL}/api/v1/message",
            headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
            json={"message": "Test message"}
        )
        elapsed = time.time() - start
        assert response.status_code == 200
        # Should respond within 2 seconds
        assert elapsed < 2.0
    
    def test_concurrent_requests(self):
        """Test system handles concurrent requests"""
        import concurrent.futures
        
        def make_request():
            return requests.post(
                f"{API_BASE_URL}/api/v1/message",
                headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
                json={"message": f"Test message {time.time()}"}
            )
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request) for _ in range(5)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        # All requests should succeed
        assert all(r.status_code == 200 for r in results)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

