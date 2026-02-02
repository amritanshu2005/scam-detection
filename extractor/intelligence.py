import re

def extract(text: str):
    # Regex patterns (Standard Indian formats)
    patterns = {
        "upi": r"[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}",
        "phone": r"(\+91[\-\s]?)?[6-9]\d{9}",
        "link": r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w\.-]*",
        "account": r"\b\d{9,18}\b"
    }

    # 1. Basic Extraction
    intel = {
        "upiIds": re.findall(patterns["upi"], text),
        "phoneNumbers": re.findall(patterns["phone"], text),
        "phishingLinks": re.findall(patterns["link"], text),
        "bankAccounts": re.findall(patterns["account"], text),
        "suspiciousKeywords": []
    }

    # 2. Context Filtering (Heuristic check)
    # Filter out common false positives (like '123456' being an OTP, not an account)
    intel["bankAccounts"] = [acc for acc in intel["bankAccounts"] if len(acc) > 8]

    # 3. Add keywords that trigger "Scam Detected" status
    triggers = ["urgent", "verify", "blocked", "suspend", "kyc", "expire", "pan card"]
    intel["suspiciousKeywords"] = [k for k in triggers if k in text.lower()]

    # Deduplicate lists
    for key in intel:
        if isinstance(intel[key], list):
            intel[key] = list(set(intel[key]))

    return intel
