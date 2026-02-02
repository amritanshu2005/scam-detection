from fastapi import FastAPI, Header, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Scam Detection API")

# Lazy imports with error handling
try:
    from models import IncomingRequest, OutgoingResponse
    from detector.scam_detector import detect
    from agent.agent import generate_reply
    from extractor.intelligence import extract
    from callback.guvi import send_callback
    from config import API_KEY
except ImportError as e:
    # If imports fail, create minimal versions for debugging
    from pydantic import BaseModel
    from typing import List, Optional, Dict, Any
    
    class MessageDetail(BaseModel):
        sender: str
        text: str
        timestamp: str
    
    class IncomingRequest(BaseModel):
        sessionId: str
        message: MessageDetail
        conversationHistory: List[MessageDetail]
        metadata: Optional[Dict[str, Any]] = None
    
    class OutgoingResponse(BaseModel):
        status: str
        reply: str
    
    API_KEY = os.getenv("API_KEY", "default-key")
    
    def detect(text: str, history: list) -> bool:
        return False
    
    def generate_reply(text: str, history: list) -> str:
        return "Service temporarily unavailable"
    
    def extract(text: str):
        return {"upiIds": [], "phoneNumbers": [], "bankAccounts": [], "phishingLinks": [], "suspiciousKeywords": []}
    
    def send_callback(*args, **kwargs):
        pass

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve a simple landing page"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Scam Detection API</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            h1 { color: #333; }
            .status { color: #28a745; font-weight: bold; }
            .endpoint { background: #f4f4f4; padding: 10px; border-radius: 5px; margin: 10px 0; }
            code { background: #e8e8e8; padding: 2px 6px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <h1>🛡️ Scam Detection API</h1>
        <p class="status">✅ Status: Running</p>
        <h2>API Endpoint:</h2>
        <div class="endpoint">
            <strong>POST</strong> <code>/api/v1/message</code>
        </div>
        <h2>Documentation:</h2>
        <p>Visit <a href="/docs">/docs</a> for interactive API documentation</p>
    </body>
    </html>
    """

def verify_api_key(x_api_key: str):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

@app.post("/api/v1/message", response_model=OutgoingResponse)
async def webhook(
    req: IncomingRequest,
    background_tasks: BackgroundTasks,
    x_api_key: str = Header(...)
):
    verify_api_key(x_api_key)

    text = req.message.text
    history = req.conversationHistory
    session_id = req.sessionId

    # 1. Detect
    is_scam = detect(text, history)

    # 2. Reply
    reply = generate_reply(text, history)

    # 3. Extract (Full history check)
    full_text = " ".join([m.text for m in history] + [text])
    intel = extract(full_text)

    # 4. Callback Trigger Strategy
    # We want to send the callback if:
    # A) We found critical info (Bank/UPI) AND we haven't sent it yet.
    # B) The conversation is getting long (e.g., > 8 messages) and we want to wrap up.

    # Count extracted items
    critical_count = len(intel["upiIds"]) + len(intel["bankAccounts"]) + len(intel["phoneNumbers"])

    # Trigger condition: Scam IS detected AND (High turn count OR We found actionable intel)
    should_trigger_callback = is_scam and (len(history) > 8 or critical_count > 0)

    if should_trigger_callback:
        background_tasks.add_task(
            send_callback,
            session_id,
            len(history) + 1,
            intel
        )

    return OutgoingResponse(
        status="success",
        reply=reply
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
