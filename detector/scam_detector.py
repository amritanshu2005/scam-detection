"""
Scam Detection Module - Enhanced for Indian Context
Detects scam messages using keyword analysis with Hinglish support.
"""

SCAM_KEYWORDS = [
    # English - Core scam patterns
    "account blocked", "verify", "urgent", "upi", "refund", "kyc", "otp",
    "bank", "suspend", "credit card", "debit card", "expired", "limit",
    "pan card", "adhaar", "police", "arrest", "winner", "prize", "lakh",
    "lottery", "click here", "link", "apk", "download",
    # Hinglish / Indian Context
    "bhai", "sir", "mam", "madam", "offer", "free", "money", "paytm",
    "phonepe", "gpay", "amount", "credited", "debited", "password",
    "pin", "cvv", "expiry", "date", "karo", "kijiye",
    # Additional urgency patterns
    "immediately", "within 24 hours", "last chance", "act now",
    "confirm", "update", "secure", "protect", "hack", "compromised"
]


def detect(text: str, history: list) -> bool:
    """
    Detect if the given text is a scam message.

    Args:
        text: The message text to analyze
        history: Previous conversation history (for context)

    Returns:
        True if scam is detected, False otherwise
    """
    text_lower = text.lower()
    score = sum(1 for keyword in SCAM_KEYWORDS if keyword in text_lower)
    return score >= 1
