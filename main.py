from fastapi import FastAPI, Header, HTTPException, BackgroundTasks
import os
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

    # 4. Callback Trigger
    # If scam detected AND (long conversation OR critical info found)
    has_critical_info = (intel["upiIds"] or intel["bankAccounts"] or intel["phoneNumbers"])

    if is_scam and (len(history) >= 10 or has_critical_info):
        # Fire callback in background
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
