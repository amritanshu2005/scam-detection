"""
Quick debugging script to verify backend functionality.
Run this before running the full test suite.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

print("="*70)
print("BACKEND VERIFICATION SCRIPT")
print("="*70)

# 1. Check imports
print("\n[1] Checking imports...")
try:
    from models import IncomingRequest, OutgoingResponse, MessageDetail
    print("  ✓ Models imported successfully")
except Exception as e:
    print(f"  ✗ Error importing models: {e}")
    sys.exit(1)

try:
    from detector.scam_detector import detect
    print("  ✓ Scam detector imported successfully")
except Exception as e:
    print(f"  ✗ Error importing scam detector: {e}")

try:
    from agent.agent import generate_reply
    print("  ✓ Agent module imported successfully")
except Exception as e:
    print(f"  ✗ Error importing agent: {e}")

try:
    from extractor.intelligence import extract
    print("  ✓ Intelligence extractor imported successfully")
except Exception as e:
    print(f"  ✗ Error importing extractor: {e}")

try:
    from callback.guvi import send_callback
    print("  ✓ Callback module imported successfully")
except Exception as e:
    print(f"  ✗ Error importing callback: {e}")

# 2. Test scam detection
print("\n[2] Testing scam detection...")
test_scam_message = "Your account has been suspended. Verify immediately."
test_safe_message = "How are you today?"

is_scam = detect(test_scam_message, [])
is_safe = detect(test_safe_message, [])

print(f"  Message: '{test_scam_message}'")
print(f"  Detection: {'✓ SCAM DETECTED' if is_scam else '✗ NOT DETECTED'}")
print(f"  Message: '{test_safe_message}'")
print(f"  Detection: {'✓ SAFE (no scam)' if not is_safe else '✗ FALSE POSITIVE'}")

# 3. Test intelligence extraction
print("\n[3] Testing intelligence extraction...")
test_message = "Send money to scammer@bank.com or call +919876543210"
intel = extract(test_message)

print(f"  Message: '{test_message}'")
print(f"  Extracted UPI IDs: {intel.get('upiIds', [])}")
print(f"  Extracted Phone: {intel.get('phoneNumbers', [])}")
print(f"  Extracted Keywords: {intel.get('suspiciousKeywords', [])}")

# 4. Test agent response generation
print("\n[4] Testing agent response generation...")
print("  Note: If GROQ_API_KEY is not set, fallback responses will be used")

try:
    # Create a MessageDetail object for history
    from models import MessageDetail
    
    history = [
        MessageDetail(sender="scammer", text="Your account is blocked", timestamp="123456"),
        MessageDetail(sender="agent", text="Oh no, what should I do sir?", timestamp="123457")
    ]
    
    reply = generate_reply("Please verify your details", history)
    print(f"  Agent reply: '{reply}'")
    print(f"  Reply length: {len(reply)} characters")
    
    if len(reply) > 0:
        print("  ✓ Agent generating responses")
    else:
        print("  ✗ Agent returned empty response")
        
except Exception as e:
    print(f"  ✗ Error generating reply: {e}")

# 5. Check environment variables
print("\n[5] Checking environment variables...")
from dotenv import load_dotenv
load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")
api_key = os.getenv("API_KEY", "default-secret-key")

if groq_key:
    print(f"  ✓ GROQ_API_KEY is set (length: {len(groq_key)})")
else:
    print("  ⚠ GROQ_API_KEY is not set - using fallback responses")

if api_key != "default-secret-key":
    print(f"  ✓ API_KEY is configured")
else:
    print("  ⚠ API_KEY using default value - should change in production")

# 6. Test conversation history handling
print("\n[6] Testing conversation history format...")
try:
    history = [
        MessageDetail(sender="scammer", text="Message 1", timestamp="1"),
        MessageDetail(sender="agent", text="Reply 1", timestamp="2"),
    ]
    
    # Test that generate_reply handles history properly
    reply = generate_reply("Test message", history)
    print("  ✓ Conversation history properly handled")
    
except Exception as e:
    print(f"  ✗ Error with conversation history: {e}")

print("\n" + "="*70)
print("VERIFICATION COMPLETE")
print("="*70)
print("\nNext steps:")
print("1. Ensure GROQ_API_KEY is set in .env for production")
print("2. Start the server: uvicorn main:app --reload")
print("3. Open browser: http://localhost:8000")
print("4. Run test suite: python test_backend_fix.py")
print("="*70 + "\n")
