import requests
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
    # Generate dynamic agent notes
    agent_notes = generate_agent_notes(full_text, intel)

    payload = {
        "sessionId": session_id,
        "scamDetected": True,
        "totalMessagesExchanged": total_msgs,
        "extractedIntelligence": intel,
        "agentNotes": agent_notes
    }

    try:
        requests.post(
            CALLBACK_URL,
            json=payload,
            timeout=TIMEOUT
        )
        print(f"Callback sent for session {session_id}")
    except Exception as e:
        print(f"Callback failed: {e}")

