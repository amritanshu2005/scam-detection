"""
Agent Notes Generator - Analyzes scammer tactics and generates intelligent notes.
"""

def generate_agent_notes(text: str, intel: dict) -> str:
    """
    Generate dynamic agent notes based on conversation analysis.

    Args:
        text: Full conversation text
        intel: Extracted intelligence dictionary

    Returns:
        Human-readable summary of scammer tactics
    """
    tactics = []

    # Detect urgency tactics
    urgency_words = ["urgent", "immediately", "now", "today", "blocked", "suspend", "expire"]
    if any(word in text.lower() for word in urgency_words):
        tactics.append("urgency tactics")

    # Detect payment redirection
    if intel.get("upiIds") or intel.get("bankAccounts"):
        tactics.append("payment redirection")

    # Detect phishing attempts
    if intel.get("phishingLinks"):
        tactics.append("phishing link distribution")

    # Detect impersonation (bank, govt, etc.)
    impersonation_words = ["bank", "rbi", "police", "government", "sbi", "hdfc", "icici", "kyc"]
    if any(word in text.lower() for word in impersonation_words):
        tactics.append("authority impersonation")

    # Detect prize/lottery scam
    prize_words = ["winner", "prize", "lottery", "lakh", "crore", "congratulations"]
    if any(word in text.lower() for word in prize_words):
        tactics.append("prize/lottery fraud")

    # Detect OTP/credential harvesting
    credential_words = ["otp", "password", "pin", "cvv", "card number"]
    if any(word in text.lower() for word in credential_words):
        tactics.append("credential harvesting")

    # Build the notes string
    if not tactics:
        return "Scammer engaged but specific tactics unclear. Monitoring continued."

    return f"Scammer used {', '.join(tactics)}. Intelligence extracted successfully."
