import requests
import json
from config import CALLBACK_URL, TIMEOUT
from extractor.notes_generator import generate_agent_notes

def send_callback(session_id: str, total_msgs: int, intel: dict, full_text: str = ""):
    """
    Send extracted intelligence to GUVI evaluation endpoint.

    Args:
        session_id: Unique session identifier
        total_msgs: Total messages exchanged
        intel: Extracted intelligence dictionary
        full_text: Full conversation text for notes generation
    """
    try:
        # Ensure intel has all required fields
        intel = {
            "bankAccounts": intel.get("bankAccounts", []),
            "upiIds": intel.get("upiIds", []),
            "phishingLinks": intel.get("phishingLinks", []),
            "phoneNumbers": intel.get("phoneNumbers", []),
            "suspiciousKeywords": intel.get("suspiciousKeywords", [])
        }
        
        # Generate dynamic agent notes
        try:
            agent_notes = generate_agent_notes(full_text, intel)
        except Exception as e:
            print(f"[CALLBACK] Note generation failed: {e}, using default notes")
            agent_notes = f"Scam detection alert for session {session_id}"

        payload = {
            "sessionId": session_id,
            "scamDetected": True,
            "totalMessagesExchanged": total_msgs,
            "extractedIntelligence": intel,
            "agentNotes": agent_notes
        }

        print(f"\n[CALLBACK] Sending callback to GUVI endpoint...")
        print(f"[CALLBACK] Session: {session_id}")
        print(f"[CALLBACK] Messages: {total_msgs}")
        print(f"[CALLBACK] Intelligence: {json.dumps(intel, indent=2)}")
        
        response = requests.post(
            CALLBACK_URL,
            json=payload,
            timeout=TIMEOUT
        )
        
        print(f"[CALLBACK SUCCESS] Status: {response.status_code}")
        if response.status_code == 200:
            print(f"[CALLBACK] Response: {response.json()}")
        else:
            print(f"[CALLBACK WARNING] Non-200 response: {response.text}")
            
    except requests.exceptions.Timeout:
        print(f"[CALLBACK ERROR] Timeout while sending callback for session {session_id}")
    except requests.exceptions.ConnectionError as e:
        print(f"[CALLBACK ERROR] Connection error: {e}")
    except Exception as e:
        print(f"[CALLBACK ERROR] Failed to send callback for session {session_id}: {str(e)}")


