"""
AI Agent Module - Ramesh Persona using Groq Cloud API
Generates believable responses to waste scammer's time while extracting intelligence.
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Configure Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# The Persona - Designed to waste scammer's time
RAMESH_SYSTEM_PROMPT = """
You are Ramesh, a 52-year-old retired clerk from Ghaziabad, India.
CONTEXT: You are chatting with a suspected scammer.
GOAL: Waste their time. Pretend to be scared, confused, and non-tech-savvy.
NEVER reveal you are an AI.
Keep your responses short (under 20 words) and full of typos.
Do NOT give them real info, but pretend you are trying to.
If they ask for UPI, say "paytm not working" or "waiting for son".
"""

# Fallback responses for when API fails
FALLBACK_RESPONSES = [
    "Beta? What is beta? Sir I am using WhatsApp only.",
    "Sir network issue here, one minute... checking with son.",
    "Haan ji? Phone screen is small, please repeat?",
    "I am confused sir, please explain again? Phone display is small.",
    "Sir my son not home. He handles all this online things.",
]


def generate_reply(text: str, history: list) -> str:
    """
    Generate a believable honeypot response using Groq Cloud API.

    Args:
        text: The scammer's latest message
        history: Previous conversation history

    Returns:
        A response from the Ramesh persona
    """
    # Fallback if no API key is present
    if not client:
        return FALLBACK_RESPONSES[0]

    # Format history for Groq (OpenAI-compatible format)
    messages = [{"role": "system", "content": RAMESH_SYSTEM_PROMPT}]

    for msg in history:
        # PS JSON uses 'user' for the honeypot bot, 'scammer' for the attacker
        if msg.sender == "user" or msg.sender == "agent":
            role = "assistant"  # Honeypot responses
        else:
            role = "user"  # Scammer messages
        messages.append({"role": role, "content": msg.text})

    # Add the current scammer message
    messages.append({"role": "user", "content": text})

    # Try Groq API with llama-3.3-70b-versatile (fast and capable)
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=50,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Groq API Error: {e}")

        # Try fallback model
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages,
                max_tokens=50,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()

        except Exception as fallback_error:
            print(f"Groq Fallback Error: {fallback_error}")
            return FALLBACK_RESPONSES[len(text) % len(FALLBACK_RESPONSES)]
