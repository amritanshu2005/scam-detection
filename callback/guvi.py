import requests
from config import CALLBACK_URL, CALLBACK_TIMEOUT

def send_callback(session_id, total_msgs, intel):
    payload = {
        "sessionId": session_id,
        "scamDetected": True,
        "totalMessagesExchanged": total_msgs,
        "extractedIntelligence": intel,
        "agentNotes": "Scammer used urgency and payment redirection tactics"
    }

    try:
        requests.post(
            CALLBACK_URL,
            json=payload,
            timeout=CALLBACK_TIMEOUT
        )
        print(f"Callback sent for session {session_id}")
    except Exception as e:
        print(f"Callback failed: {e}")
