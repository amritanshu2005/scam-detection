"""
Production Sanity Check - Run against deployed Vercel URL
Usage: python test_prod.py
"""

import requests
import sys

# ============== CONFIGURE THESE ==============
PROD_URL = "https://scam-detection.vercel.app"  # Replace with your actual Vercel URL
API_KEY = "test-api-key-12345"  # Replace with your actual API key
# =============================================


def test_live():
    print(f"\nTesting {PROD_URL}...")
    print("=" * 50)

    success = True

    # 1. Check HTML Load
    print("\n[1] Testing UI Load...")
    try:
        r = requests.get(PROD_URL, timeout=10)
        if r.status_code == 200 and "<title>Agentic Honey-Pot" in r.text:
            print("   ✅ UI Loads Successfully")
        else:
            print(f"   ❌ UI Failed (Status: {r.status_code})")
            success = False
    except Exception as e:
        print(f"   ❌ UI Failed: {e}")
        success = False

    # 2. Check API Endpoint
    print("\n[2] Testing API Endpoint...")
    payload = {
        "sessionId": "prod-test-001",
        "message": {
            "sender": "scammer",
            "text": "Urgent! Your bank account has been blocked. Share your UPI ID to verify.",
            "timestamp": "2026-02-03T12:00:00Z"
        },
        "conversationHistory": []
    }

    try:
        r = requests.post(
            f"{PROD_URL}/api/v1/message",
            json=payload,
            headers={"x-api-key": API_KEY, "Content-Type": "application/json"},
            timeout=30
        )

        if r.status_code == 200:
            data = r.json()
            print("   ✅ API Success")
            print(f"   Status: {data.get('status')}")
            print(f"   Reply: {data.get('reply')[:80]}...")
        else:
            print(f"   ❌ API Failed: HTTP {r.status_code}")
            print(f"   Response: {r.text[:200]}")
            success = False
    except Exception as e:
        print(f"   ❌ API Failed: {e}")
        success = False

    # Summary
    print("\n" + "=" * 50)
    if success:
        print("🎉 ALL TESTS PASSED - Ready for submission!")
    else:
        print("⚠️  Some tests failed - Check configuration")
    print("=" * 50)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(test_live())
