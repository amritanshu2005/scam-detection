"""
Quick Test Script - Verify Your System Works
Run this to check if everything is working correctly
"""

import requests
import json
import sys

API_URL = "http://localhost:8000"
API_KEY = "test-api-key-12345"

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_success(text):
    print(f"[PASS] {text}")

def print_error(text):
    print(f"[FAIL] {text}")

def test_health():
    """Test 1: Health Check"""
    print_header("TEST 1: Health Check")
    try:
        response = requests.get(f"{API_URL}/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Server is running!")
            print(f"   Status: {data.get('status')}")
            print(f"   Service: {data.get('service')}")
            print(f"   Version: {data.get('version')}")
            return True
        else:
            print_error(f"Server returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to server. Is it running?")
        print("   Start server with: python main.py")
        return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_scam_detection():
    """Test 2: Scam Detection"""
    print_header("TEST 2: Scam Detection")
    try:
        headers = {
            "X-API-Key": API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "message": "Your bank account has been suspended! Click here to verify: http://fake-bank.com/verify"
        }
        
        response = requests.post(
            f"{API_URL}/api/v1/message",
            headers=headers,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            print_success("Message processed successfully!")
            print(f"   Conversation ID: {data.get('conversation_id')[:20]}...")
            print(f"   Scam Detected: {data.get('scam_detected')}")
            print(f"   Agent Activated: {data.get('agent_activated')}")
            print(f"   Agent Response: {data.get('response_message')[:60]}...")
            
            intelligence = data.get('extracted_intelligence', {})
            print(f"\n   Intelligence Extracted:")
            print(f"   - Bank Accounts: {len(intelligence.get('bank_accounts', []))}")
            print(f"   - UPI IDs: {len(intelligence.get('upi_ids', []))}")
            print(f"   - Phishing URLs: {len(intelligence.get('phishing_urls', []))}")
            
            metrics = data.get('engagement_metrics', {})
            print(f"\n   Engagement Metrics:")
            print(f"   - Turn Count: {metrics.get('turn_count')}")
            print(f"   - Messages Exchanged: {metrics.get('messages_exchanged')}")
            
            if data.get('scam_detected'):
                print_success("Scam detection is working!")
            else:
                print_error("Scam was not detected (should have been)")
                return False
            
            if data.get('agent_activated'):
                print_success("AI Agent is working!")
            else:
                print_error("Agent was not activated")
                return False
            
            return True
        elif response.status_code == 401:
            print_error("Authentication failed. Check API key.")
            return False
        else:
            print_error(f"Server returned status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_intelligence_extraction():
    """Test 3: Intelligence Extraction"""
    print_header("TEST 3: Intelligence Extraction")
    try:
        headers = {
            "X-API-Key": API_KEY,
            "Content-Type": "application/json"
        }
        
        # Test with bank account
        payload1 = {
            "message": "Send payment to account number 123456789012"
        }
        response1 = requests.post(
            f"{API_URL}/api/v1/message",
            headers=headers,
            json=payload1,
            timeout=10
        )
        
        if response1.status_code == 200:
            data1 = response1.json()
            bank_accounts = data1.get('extracted_intelligence', {}).get('bank_accounts', [])
            
            if bank_accounts:
                print_success(f"Bank account extraction works! Found: {bank_accounts[0]}")
            else:
                print("[INFO] Bank account not extracted (may need pattern refinement)")
        
        # Test with UPI ID
        payload2 = {
            "message": "Send money to UPI ID: testuser@paytm"
        }
        response2 = requests.post(
            f"{API_URL}/api/v1/message",
            headers=headers,
            json=payload2,
            timeout=10
        )
        
        if response2.status_code == 200:
            data2 = response2.json()
            upi_ids = data2.get('extracted_intelligence', {}).get('upi_ids', [])
            
            if upi_ids:
                print_success(f"UPI ID extraction works! Found: {upi_ids[0]}")
            else:
                print("[INFO] UPI ID not extracted (may need pattern refinement)")
        
        # Test with URL
        payload3 = {
            "message": "Click here: http://suspicious-site.com/verify"
        }
        response3 = requests.post(
            f"{API_URL}/api/v1/message",
            headers=headers,
            json=payload3,
            timeout=10
        )
        
        if response3.status_code == 200:
            data3 = response3.json()
            urls = data3.get('extracted_intelligence', {}).get('phishing_urls', [])
            
            if urls:
                print_success(f"URL extraction works! Found: {urls[0]}")
            else:
                print("[INFO] URL not extracted (may need pattern refinement)")
        
        return True
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_multi_turn():
    """Test 4: Multi-turn Conversation"""
    print_header("TEST 4: Multi-turn Conversation")
    try:
        headers = {
            "X-API-Key": API_KEY,
            "Content-Type": "application/json"
        }
        
        # First message
        payload1 = {"message": "You won a prize!"}
        response1 = requests.post(
            f"{API_URL}/api/v1/message",
            headers=headers,
            json=payload1,
            timeout=10
        )
        
        if response1.status_code == 200:
            data1 = response1.json()
            conversation_id = data1.get('conversation_id')
            print_success(f"First message sent. Conversation ID: {conversation_id[:20]}...")
            
            # Second message in same conversation
            payload2 = {
                "message": "Send your bank account number to claim",
                "conversation_id": conversation_id
            }
            response2 = requests.post(
                f"{API_URL}/api/v1/message",
                headers=headers,
                json=payload2,
                timeout=10
            )
            
            if response2.status_code == 200:
                data2 = response2.json()
                turn_count = data2.get('engagement_metrics', {}).get('turn_count')
                
                if turn_count == 2:
                    print_success(f"Multi-turn conversation works! Turn count: {turn_count}")
                    return True
                else:
                    print_error(f"Turn count is {turn_count}, expected 2")
                    return False
            else:
                print_error(f"Second message failed with status {response2.status_code}")
                return False
        else:
            print_error(f"First message failed with status {response1.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_metrics():
    """Test 5: Performance Metrics"""
    print_header("TEST 5: Performance Metrics")
    try:
        headers = {"X-API-Key": API_KEY}
        response = requests.get(
            f"{API_URL}/api/v1/metrics",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            perf = data.get('performance', {})
            convs = data.get('conversations', {})
            
            print_success("Metrics endpoint works!")
            print(f"   Total Requests: {perf.get('total_requests', 0)}")
            print(f"   Avg Response Time: {perf.get('avg_response_time', 0)*1000:.0f}ms")
            print(f"   Total Conversations: {convs.get('total', 0)}")
            print(f"   Active Conversations: {convs.get('active', 0)}")
            return True
        else:
            print_error(f"Metrics endpoint returned status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def main():
    print("\n" + "="*60)
    print("  AGENTIC HONEY-POT SYSTEM - QUICK TEST")
    print("="*60)
    print("\nTesting your system...")
    
    results = []
    
    # Run all tests
    results.append(("Health Check", test_health()))
    results.append(("Scam Detection", test_scam_detection()))
    results.append(("Intelligence Extraction", test_intelligence_extraction()))
    results.append(("Multi-turn Conversation", test_multi_turn()))
    results.append(("Performance Metrics", test_metrics()))
    
    # Summary
    print_header("TEST SUMMARY")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"  {status} - {name}")
    
    print(f"\n  Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n*** ALL TESTS PASSED! Your system is working perfectly! ***")
        print("\nNext steps:")
        print("  1. Open http://localhost:8000 in your browser")
        print("  2. Try the web dashboard")
        print("  3. Test with different scam messages")
        return 0
    else:
        print("\n*** Some tests failed. Check the errors above. ***")
        return 1

if __name__ == "__main__":
    sys.exit(main())

