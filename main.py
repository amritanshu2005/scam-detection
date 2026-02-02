"""
Agentic Honey-Pot API Server
Main entry point for scam detection and intelligence extraction system
"""

from fastapi import FastAPI, HTTPException, Header, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import os
import time
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

from scam_detector import ScamDetector
from ai_agent import AutonomousAgent
from intelligence_extractor import IntelligenceExtractor
from logger import log_error
from performance import performance_monitor

app = FastAPI(title="Agentic Honey-Pot API", version="1.0.0")

# Mount static files (with error handling)
try:
    if os.path.exists("static"):
        app.mount("/static", StaticFiles(directory="static"), name="static")
except Exception:
    pass

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
API_KEY = os.getenv("API_KEY", "your-secret-api-key-here")
CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

# Components
scam_detector = ScamDetector()
ai_agent = AutonomousAgent()
# Use a global instance or per-request? Global is fine for stateless extractor
intelligence_extractor = IntelligenceExtractor()

# --- Pydantic Models for Hackathon API ---

class MessageDetail(BaseModel):
    sender: str  # "scammer" or "user"
    text: str
    timestamp: str

class IncomingRequest(BaseModel):
    sessionId: str
    message: MessageDetail
    conversationHistory: List[MessageDetail] = Field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None

class SuccessResponse(BaseModel):
    status: str
    reply: str

# --- Helper Functions ---

def verify_api_key(x_api_key: str = Header(None)):
    """Verify API key from header"""
    # If API_KEY env var is set, enforce it. Otherwise, allow open access (for testing flexibility)
    # But for Hackathon, usually specific.
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

def send_callback(session_id: str, is_scam: bool, total_messages: int, intelligence: Dict[str, Any], agent_notes: str):
    """Send callback to Guvi API"""
    try:
        payload = {
            "sessionId": session_id,
            "scamDetected": is_scam,
            "totalMessagesExchanged": total_messages,
            "extractedIntelligence": {
                "bankAccounts": intelligence.get('bank_accounts', []),
                "upiIds": intelligence.get('upi_ids', []),
                "phishingLinks": intelligence.get('phishing_urls', []),
                "phoneNumbers": intelligence.get('phone_numbers', []),
                "suspiciousKeywords": intelligence.get('suspicious_keywords', [])
            },
            "agentNotes": agent_notes
        }

        # Fire and forget callback (timeout short)
        requests.post(CALLBACK_URL, json=payload, timeout=3)
    except Exception as e:
        # Just log error, don't crash main thread
        print(f"Callback failed for {session_id}: {e}")

# --- Endpoints ---

@app.get("/")
async def root():
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {"message": "Agentic Honey-Pot API Active"}

@app.get("/api/health")
async def health():
    return {"status": "active", "service": "Agentic Honey-Pot API"}

@app.post("/api/v1/message", response_model=SuccessResponse)
async def process_message(
    request: IncomingRequest,
    background_tasks: BackgroundTasks,
    x_api_key: str = Depends(verify_api_key)
):
    """
    Main webhook for Hackathon.
    """
    start_time = time.time()

    try:
        session_id = request.sessionId
        current_msg_text = request.message.text

        # Convert Pydantic models to dicts for internal tools
        # Our tools expect: [{"role": "scammer/agent", "content": "..."}]
        internal_history = []
        for msg in request.conversationHistory:
            role = "scammer" if msg.sender == "scammer" else "agent"
            internal_history.append({
                "role": role,
                "content": msg.text,
                # timestamp optional or formatted
            })

        # Add current message to history for context
        internal_history.append({
            "role": "scammer",
            "content": current_msg_text
        })

        # 2. Detect Scam
        is_scam = scam_detector.detect(current_msg_text, internal_history)

        # 3. Extract Intelligence (Full history scan)
        intelligence = intelligence_extractor.extract(internal_history)

        # 4. Agent Response
        agent_reply = ai_agent.generate_response(current_msg_text, internal_history, intelligence)

        # 5. Check for Callback Trigger
        # Trigger if critical info found OR conversation > 10 turns
        critical_info_found = (
            len(intelligence.get('bank_accounts', [])) > 0 or
            len(intelligence.get('upi_ids', [])) > 0 or
            len(intelligence.get('phone_numbers', [])) > 0
        )

        turn_count = len(internal_history)

        if critical_info_found or turn_count > 10:
            agent_notes = "Scam detected."
            if critical_info_found:
                agent_notes += " Intelligence extracted."
            if turn_count > 10:
                agent_notes += " Max turns exceeded."

            # Run callback in background to keep response fast
            background_tasks.add_task(
                send_callback,
                session_id,
                is_scam,
                turn_count,
                intelligence,
                agent_notes
            )

        # 6. Return Response
        return SuccessResponse(status="success", reply=agent_reply)

    except Exception as e:
        log_error(request.sessionId, e, "process_message")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
