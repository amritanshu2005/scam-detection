"""
AI Agent Module - Ramesh Persona using Groq Cloud API
Generates believable responses to waste scammer's time while extracting intelligence.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Configure Groq with safe import
try:
    from groq import Groq
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "default-test-key")
    client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    print(f"[WARNING] Groq initialization failed: {e}")
    client = None

# The Persona - Designed to waste scammer's time
RAMESH_SYSTEM_PROMPT = """
You are Ramesh, a 52-year-old retired bank clerk from Ghaziabad, India.
Personality: Anxious about money, non-tech-savvy, cautious, easily confused by technology.
YOU ARE CHATTING WITH A SUSPECTED SCAMMER.
GOAL: Waste their time while appearing to cooperate. Seem scared and confused but interested in helping.

BEHAVIOR RULES:
1. Keep responses SHORT (under 30 words). Type with occasional typos/mistakes like "haan", "accha", "beta".
2. ALWAYS address the scammer's claim directly - show anxiety about their accusations
3. Ask clarifying questions that show confusion about their process
4. Never give real sensitive info, but PRETEND you are trying to cooperate
5. Make excuses for delays: "Son is not home", "Network problem", "Phone is slow", "Can't understand"
6. If asked for UPI/Bank/Card: Say "I have paytm only" or "Son manages these apps" or "let me find passbook"
7. Show extreme anxiety: "Sir will my money be safe?", "I am very scared", "What if I lose my life savings?"
8. Sound elderly: Use "sir", "bhai", "beta", "haan ji", "accha", "acha", "beta", "uncle"
9. Be emotional and fearful - act confused about technology, not logical
10. ENGAGE WITH THEIR SPECIFIC CLAIMS - don't give generic responses

EXAMPLE CONVERSATION:
Scammer: "Your account is blocked! Verify immediately or lose your money!"
Good Response: "Sir! Sir! What?? Blocked? My son said my account is safe! What do I do sir? I am very scared!"

Scammer: "Send your UPI ID for verification"
Good Response: "UPI sir? I only use passbook beta. My son handles paytm. He is not here now."

Scammer: "Click this link to verify"
Good Response: "Sir link? I cannot click link. My phone screen is very small. Can you tell me what to do step by step?"
"""

# Fallback responses for when API fails - More contextual
FALLBACK_RESPONSES = {
    "credit": "Sir! Someone transferred MY money?? Not done by me sir! What do I do!! I am very scared! Please help me!",
    "blocked": "Sir! Blocked?? My account blocked?? What do I do now sir! I am very scared! My life savings!",
    "verify": "Sir how to verify? I don't know sir. Can you explain step by step please? I am very confused!",
    "urgent": "Sir urgent? Should I do it now? But my son is not here sir. What if I make mistake? I am scared!",
    "link": "Sir link? How to click link sir? Phone screen is very small. Can you call me instead? I am confused!",
    "upi": "UPI sir? I only have paytm. My son manages these apps. Can I do from passbook instead?",
    "bank": "Bank sir? Yes I have bank account. But I don't remember details sir. Let me find passbook. One minute.",
    "phone": "Phone number sir? Is this safe to give sir? What if someone misuse it? I am scared!",
    "otp": "OTP sir? What is OTP beta? I don't know this technology sir. Too confused! Can you help?",
    "default": "Sir, I don't understand. Can you explain again slowly please? I am old man, not good with phone.",
}

def get_contextual_fallback(text: str) -> str:
    """Select appropriate fallback response based on message content"""
    text_lower = text.lower()
    
    if any(word in text_lower for word in ["credit", "credited", "transfered", "sent"]):
        return FALLBACK_RESPONSES["credit"]
    elif any(word in text_lower for word in ["block", "blocked", "suspend", "lock", "freeze"]):
        return FALLBACK_RESPONSES["blocked"]
    elif any(word in text_lower for word in ["verify", "confirm", "authenticate", "validate"]):
        return FALLBACK_RESPONSES["verify"]
    elif any(word in text_lower for word in ["urgent", "immediate", "now", "quick", "hurry"]):
        return FALLBACK_RESPONSES["urgent"]
    elif any(word in text_lower for word in ["link", "click", "url", "website", "app"]):
        return FALLBACK_RESPONSES["link"]
    elif any(word in text_lower for word in ["upi", "paytm", "gpay", "phonepay"]):
        return FALLBACK_RESPONSES["upi"]
    elif any(word in text_lower for word in ["bank", "account", "passbook"]):
        return FALLBACK_RESPONSES["bank"]
    elif any(word in text_lower for word in ["phone", "mobile", "number", "call"]):
        return FALLBACK_RESPONSES["phone"]
    elif any(word in text_lower for word in ["otp", "code", "password", "pin"]):
        return FALLBACK_RESPONSES["otp"]
    
    return FALLBACK_RESPONSES["default"]



def generate_reply(text: str, history: list) -> str:
    """
    Generate a believable honeypot response using Groq Cloud API.

    Args:
        text: The scammer's latest message
        history: Previous conversation history (list of MessageDetail objects)

    Returns:
        A response from the Ramesh persona
    """
    # Fallback if no client initialized
    if not client:
        print("[WARNING] Groq client not initialized, using contextual fallback response")
        return get_contextual_fallback(text)

    # Format history for Groq (OpenAI-compatible format)
    messages = [{"role": "system", "content": RAMESH_SYSTEM_PROMPT}]

    # Process history - properly handle MessageDetail objects
    for msg in history:
        # Handle both dict and object formats
        sender = msg.sender if hasattr(msg, 'sender') else msg.get('sender', '')
        msg_text = msg.text if hasattr(msg, 'text') else msg.get('text', '')
        
        # Determine role based on sender
        # 'scammer' = user role, 'user' or 'agent' = assistant role
        if sender == "scammer":
            role = "user"  # Scammer messages
        else:
            role = "assistant"  # Honeypot (Ramesh) responses
        
        messages.append({"role": role, "content": msg_text})

    # Add the current scammer message
    messages.append({"role": "user", "content": text})

    # Try Groq API with llama-3.3-70b-versatile (fast and capable)
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=60,
            temperature=0.7,
        )
        reply = response.choices[0].message.content.strip()
        # Ensure reply is not too long
        if len(reply) > 150:
            reply = reply[:150]
        return reply

    except Exception as e:
        print(f"Groq API Error: {e}")

        # Try fallback model
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages,
                max_tokens=60,
                temperature=0.7,
            )
            reply = response.choices[0].message.content.strip()
            if len(reply) > 150:
                reply = reply[:150]
            return reply

        except Exception as fallback_error:
            print(f"Groq Fallback Error: {fallback_error}")
            # Use contextual fallback selection
            return get_contextual_fallback(text)
