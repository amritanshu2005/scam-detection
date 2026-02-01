"""
Agentic Honey-Pot API Server
Main entry point for scam detection and intelligence extraction system
"""

from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import os
import uuid
from datetime import datetime
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from scam_detector import ScamDetector
from ai_agent import AutonomousAgent
from intelligence_extractor import IntelligenceExtractor
from logger import log_message_processing, log_agent_activation, log_intelligence_extraction, log_error, log_api_request
from performance import performance_monitor
import time

app = FastAPI(title="Agentic Honey-Pot API", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS middleware for public API access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory conversation storage (use Redis/DB in production)
conversations: Dict[str, Dict[str, Any]] = {}

# API Key validation
API_KEY = os.getenv("API_KEY", "your-secret-api-key-here")

def verify_api_key(x_api_key: str = Header(...)):
    """Verify API key from header"""
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key


class MessageRequest(BaseModel):
    """Incoming message from Mock Scammer API"""
    message: str = Field(..., description="The scam message content")
    conversation_id: Optional[str] = Field(None, description="Existing conversation ID for multi-turn")
    sender_id: Optional[str] = Field(None, description="Sender/scammer identifier")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class IntelligenceData(BaseModel):
    """Extracted intelligence structure"""
    bank_accounts: List[str] = Field(default_factory=list, description="Extracted bank account numbers")
    upi_ids: List[str] = Field(default_factory=list, description="Extracted UPI IDs")
    phishing_urls: List[str] = Field(default_factory=list, description="Extracted phishing URLs")
    other_intelligence: Dict[str, Any] = Field(default_factory=dict, description="Other extracted information")


class ResponseOutput(BaseModel):
    """Structured API response"""
    conversation_id: str = Field(..., description="Unique conversation identifier")
    scam_detected: bool = Field(..., description="Whether scam intent was detected")
    agent_activated: bool = Field(..., description="Whether autonomous agent is active")
    response_message: str = Field(..., description="Agent's response to the scammer")
    engagement_metrics: Dict[str, Any] = Field(..., description="Engagement statistics")
    extracted_intelligence: IntelligenceData = Field(..., description="Extracted intelligence")
    timestamp: str = Field(..., description="Response timestamp")


# Initialize components
scam_detector = ScamDetector()
ai_agent = AutonomousAgent()
intelligence_extractor = IntelligenceExtractor()


@app.get("/")
async def root():
    """Serve the dashboard UI"""
    return FileResponse("static/index.html")

@app.get("/api/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "active",
        "service": "Agentic Honey-Pot API",
        "version": "1.0.0"
    }


@app.post("/api/v1/message", response_model=ResponseOutput)
async def process_message(
    request: MessageRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Main endpoint to process incoming scam messages
    
    Accepts messages from Mock Scammer API, detects scam intent,
    activates autonomous agent if needed, and extracts intelligence.
    """
    start_time = time.time()
    conversation_id = None
    
    try:
        # Get or create conversation
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        # Log message processing start
        log_message_processing(conversation_id, request.message, False)
        
        if conversation_id not in conversations:
            conversations[conversation_id] = {
                "messages": [],
                "scam_detected": False,
                "agent_activated": False,
                "turn_count": 0,
                "start_time": datetime.utcnow().isoformat(),
                "intelligence": {
                    "bank_accounts": [],
                    "upi_ids": [],
                    "phishing_urls": [],
                    "other": {}
                }
            }
        
        conv = conversations[conversation_id]
        
        # Add incoming message to history
        conv["messages"].append({
            "role": "scammer",
            "content": request.message,
            "timestamp": datetime.utcnow().isoformat()
        })
        conv["turn_count"] += 1
        
        # Detect scam intent (if not already detected)
        if not conv["scam_detected"]:
            detection_start = time.time()
            conv["scam_detected"] = scam_detector.detect(request.message, conv["messages"])
            performance_monitor.record_detection_time(time.time() - detection_start)
            log_message_processing(conversation_id, request.message, conv["scam_detected"])
        
        # Activate agent if scam detected
        agent_activated = False
        response_message = ""
        
        if conv["scam_detected"]:
            if not conv["agent_activated"]:
                conv["agent_activated"] = True
                # Determine stage for logging
                turn_count = len([m for m in conv["messages"] if m.get("role") == "agent"])
                stage = "initial" if turn_count == 0 else "engaged"
                log_agent_activation(conversation_id, stage)
            
            agent_activated = True
            
            # Generate agent response
            agent_start = time.time()
            response_message = ai_agent.generate_response(
                request.message,
                conv["messages"],
                conv["intelligence"]
            )
            performance_monitor.record_agent_time(time.time() - agent_start)
            
            # Add agent response to history
            conv["messages"].append({
                "role": "agent",
                "content": response_message,
                "timestamp": datetime.utcnow().isoformat()
            })
        
        # Extract intelligence from conversation
        extraction_start = time.time()
        intelligence = intelligence_extractor.extract(conv["messages"])
        performance_monitor.record_extraction_time(time.time() - extraction_start)
        
        # Update conversation intelligence (merge new findings)
        for key in ["bank_accounts", "upi_ids", "phishing_urls"]:
            conv["intelligence"][key] = list(set(conv["intelligence"][key] + intelligence[key]))
        
        conv["intelligence"]["other"].update(intelligence.get("other", {}))
        
        # Log intelligence extraction if new items found
        if any(len(intelligence[key]) > 0 for key in ["bank_accounts", "upi_ids", "phishing_urls"]):
            log_intelligence_extraction(conversation_id, intelligence)
        
        # Calculate engagement metrics
        engagement_metrics = {
            "turn_count": conv["turn_count"],
            "conversation_duration_seconds": (
                datetime.utcnow() - datetime.fromisoformat(conv["start_time"])
            ).total_seconds(),
            "messages_exchanged": len(conv["messages"]),
            "intelligence_items_found": (
                len(conv["intelligence"]["bank_accounts"]) +
                len(conv["intelligence"]["upi_ids"]) +
                len(conv["intelligence"]["phishing_urls"])
            )
        }
        
        # Prepare response
        response = ResponseOutput(
            conversation_id=conversation_id,
            scam_detected=conv["scam_detected"],
            agent_activated=agent_activated,
            response_message=response_message,
            engagement_metrics=engagement_metrics,
            extracted_intelligence=IntelligenceData(
                bank_accounts=conv["intelligence"]["bank_accounts"],
                upi_ids=conv["intelligence"]["upi_ids"],
                phishing_urls=conv["intelligence"]["phishing_urls"],
                other_intelligence=conv["intelligence"]["other"]
            ),
            timestamp=datetime.utcnow().isoformat()
        )
        
        # Log successful request and record performance
        response_time = time.time() - start_time
        performance_monitor.record_response_time(response_time)
        log_api_request("/api/v1/message", "POST", 200, response_time)
        
        return response
        
    except Exception as e:
        response_time = time.time() - start_time
        performance_monitor.record_error()
        log_error(conversation_id, e, "process_message")
        log_api_request("/api/v1/message", "POST", 500, response_time)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/api/v1/conversation/{conversation_id}")
async def get_conversation(
    conversation_id: str,
    api_key: str = Depends(verify_api_key)
):
    """Retrieve conversation history and status"""
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return conversations[conversation_id]


@app.get("/api/v1/metrics")
async def get_metrics(api_key: str = Depends(verify_api_key)):
    """Get system performance metrics"""
    return {
        "performance": performance_monitor.get_stats(),
        "conversations": {
            "total": len(conversations),
            "active": len([c for c in conversations.values() if c.get("agent_activated", False)])
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

