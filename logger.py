"""
Logging Module
Comprehensive logging for monitoring and debugging
"""

import logging
import sys
from datetime import datetime
from typing import Optional
import os

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/honey-trap-{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("honey-trap")

def log_message_processing(conversation_id: str, message: str, scam_detected: bool):
    """Log message processing"""
    logger.info(f"Message processed | Conversation: {conversation_id} | Scam: {scam_detected} | Length: {len(message)}")

def log_agent_activation(conversation_id: str, stage: str):
    """Log agent activation"""
    logger.info(f"Agent activated | Conversation: {conversation_id} | Stage: {stage}")

def log_intelligence_extraction(conversation_id: str, intelligence: dict):
    """Log intelligence extraction"""
    counts = {
        "bank_accounts": len(intelligence.get("bank_accounts", [])),
        "upi_ids": len(intelligence.get("upi_ids", [])),
        "phishing_urls": len(intelligence.get("phishing_urls", []))
    }
    logger.info(f"Intelligence extracted | Conversation: {conversation_id} | {counts}")

def log_error(conversation_id: Optional[str], error: Exception, context: str = ""):
    """Log errors"""
    logger.error(f"Error | Conversation: {conversation_id} | Context: {context} | Error: {str(error)}", exc_info=True)

def log_api_request(endpoint: str, method: str, status_code: int, response_time: float):
    """Log API requests"""
    logger.info(f"API Request | {method} {endpoint} | Status: {status_code} | Time: {response_time:.3f}s")

