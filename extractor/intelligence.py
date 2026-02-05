import re

def extract(text: str):
    """
    Extract intelligence from scam conversation.
    Returns structured data with bank accounts, UPI IDs, links, and keywords.
    """
    # Regex patterns (Standard Indian formats)
    patterns = {
        "upi": r"[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}",
        "phone": r"(\+91[\-\s]?)?[6-9]\d{9}",
        "link": r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w\.-]*",
        "account": r"\b\d{9,18}\b"
    }

    # 1. Basic Extraction with safety checks
    intel = {
        "upiIds": list(set(re.findall(patterns["upi"], text))),  # Deduplicate
        "phoneNumbers": list(set(re.findall(patterns["phone"], text))),
        "phishingLinks": list(set(re.findall(patterns["link"], text))),
        "bankAccounts": list(set(re.findall(patterns["account"], text))),
        "suspiciousKeywords": []
    }

    # 2. Context Filtering (Heuristic check)
    # Filter out common false positives
    intel["bankAccounts"] = [
        acc for acc in intel["bankAccounts"] 
        if len(acc) >= 9  # At least 9 digits for valid account
    ]
    
    # Filter phone numbers - must be valid Indian format
    intel["phoneNumbers"] = [
        phone for phone in intel["phoneNumbers"]
        if re.match(r"^(\+91)?[6-9]\d{9}$", phone.replace("-", "").replace(" ", ""))
    ]

    # 3. Add suspicious keywords found in text
    suspicious_triggers = [
        "urgent", "verify", "blocked", "suspend", "kyc", "expire", 
        "pan card", "adhaar", "otp", "password", "click here", "confirm",
        "update", "account", "bank", "upi", "paytm", "immediate"
    ]
    intel["suspiciousKeywords"] = [k for k in suspicious_triggers if k.lower() in text.lower()]
    
    # Remove duplicates and maintain order
    for key in ["upiIds", "phoneNumbers", "phishingLinks", "bankAccounts", "suspiciousKeywords"]:
        if isinstance(intel[key], list):
            intel[key] = list(dict.fromkeys(intel[key]))  # Preserve order while deduplicating

    return intel
