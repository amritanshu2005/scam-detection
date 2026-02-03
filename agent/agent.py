"""
AI Agent Module - Ramesh Persona with Model Fallback
Generates believable responses to waste scammer's time while extracting intelligence.
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
GENAI_API_KEY = os.getenv("GEMINI_API_KEY")

if GENAI_API_KEY:
    genai.configure(api_key=GENAI_API_KEY)

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

# Fallback responses for when both models fail
FALLBACK_RESPONSES = [
    "Beta? What is beta? Sir I am using WhatsApp only.",
    "Sir network issue here, one minute... checking with son.",
    "Haan ji? Phone screen is small, please repeat?",
    "I am confused sir, please explain again? Phone display is small.",
    "Sir my son not home. He handles all this online things.",
]


def generate_reply(text: str, history: list) -> str:
    """
    Generate a believable honeypot response using Gemini AI.

    Args:
        text: The scammer's latest message
        history: Previous conversation history

    Returns:
        A response from the Ramesh persona
    """
    # Fallback if no API key is present
    if not GENAI_API_KEY:
        return FALLBACK_RESPONSES[0]

    # Format history for Gemini
    chat_history = []
    for msg in history:
        # PS JSON uses 'user' for the honeypot bot, 'scammer' for the attacker
        # Gemini uses 'model' for the bot, 'user' for the prompter
        if msg.sender == "user" or msg.sender == "agent":
            role = "model"  # Honeypot responses
        else:
            role = "user"   # Scammer messages
        chat_history.append({"role": role, "parts": [msg.text]})

    # Try primary model (Gemini 2.0 Flash - fastest)
    try:
        model = genai.GenerativeModel(
            'gemini-2.0-flash',
            system_instruction=RAMESH_SYSTEM_PROMPT
        )
        chat = model.start_chat(history=chat_history)
        response = chat.send_message(text)
        return response.text.strip()

    except Exception as e:
        print(f"Gemini 2.0 Error: {e}")

        # Try fallback model (Gemini 1.5 Flash - more stable)
        try:
            model_fallback = genai.GenerativeModel(
                'gemini-1.5-flash-latest',
                system_instruction=RAMESH_SYSTEM_PROMPT
            )
            chat = model_fallback.start_chat(history=chat_history)
            response = chat.send_message(text)
            return response.text.strip()

        except Exception as fallback_error:
            print(f"Gemini 1.5 Fallback Error: {fallback_error}")
            # Return a random-ish fallback based on message length
            return FALLBACK_RESPONSES[len(text) % len(FALLBACK_RESPONSES)]
