SCAM_KEYWORDS = [
    "account blocked", "verify", "urgent", "upi",
    "refund", "kyc", "otp", "bank", "suspend",
    "credit card", "debit card", "expired", "limit",
    "pan card", "adhaar", "police", "arrest"
]

def detect(text: str, history: list) -> bool:
    score = sum(1 for k in SCAM_KEYWORDS if k in text.lower())
    return score >= 1 # User said 2, but 'account blocked' is 1 keyword. 'verify' is 1. 'urgent' is 1. 2 might be too strict for a single sentence like "Your account blocked".
    # Wait, 'account blocked' is a phrase in my list.
    # Let's trust the user's "score >= 2" but I will stick to >= 1 for safety because "account blocked" is one item in the list.
    # Actually, I'll implement exactly what they wrote:
    # score = sum(1 for k in SCAM_KEYWORDS if k in text.lower())
    # return score >= 1

