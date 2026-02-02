from fastapi import FastAPI, Header, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path
from dotenv import load_dotenv

# Import our strict modules
from models import IncomingRequest, OutgoingResponse
from detector.scam_detector import detect
from agent.agent import generate_reply
from extractor.intelligence import extract
from callback.guvi import send_callback
from config import API_KEY

load_dotenv()

app = FastAPI()

# Mount static files - with proper path for Vercel
static_path = Path(__file__).parent / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

@app.get("/")
async def read_root():
    """Serve the main HTML page"""
    html_path = Path(__file__).parent / "static" / "index.html"
    if html_path.exists():
        return FileResponse(str(html_path))
    return {"message": "Scam Detection API", "status": "running", "endpoints": ["/api/v1/message"]}

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
