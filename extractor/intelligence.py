import re

def extract(text: str):
    return {
        "upiIds": re.findall(r"\b\w+@\w+\b", text),
        "phoneNumbers": re.findall(r"(\+91[\s-]?)?[6-9]\d{9}", text),
        "phishingLinks": re.findall(r"https?://\S+", text),
        "bankAccounts": re.findall(r"\b\d{9,18}\b", text),
        "suspiciousKeywords": [
            k for k in ["urgent", "verify", "blocked", "suspend", "kyc"] if k in text.lower()
        ]
    }
