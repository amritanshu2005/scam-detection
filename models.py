from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class MessageDetail(BaseModel):
    sender: str        # "scammer" | "user"
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
