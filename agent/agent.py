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

def generate_reply(text: str, history: list) -> str:
    # Fallback if no API key is present
    if not GENAI_API_KEY:
        return "I am confused sir, please explain again? Phone display is small."

    try:
        # 1. Format history for Gemini
        chat_history = []
        for msg in history:
            # PS JSON uses 'user' for the honeypot bot, 'scammer' for the attacker
            # Gemini uses 'model' for the bot, 'user' for the prompter
            if msg.sender == "user" or msg.sender == "agent":
                role = "model"  # Honeypot responses
            else:
                role = "user"   # Scammer messages
            chat_history.append({"role": role, "parts": [msg.text]})

        # 2. Create the model - Using 1.5 Pro for best persona adherence
        model = genai.GenerativeModel('gemini-2.0-flash', system_instruction=RAMESH_SYSTEM_PROMPT)

        # 3. Start chat with history
        chat = model.start_chat(history=chat_history)

        # 4. Send the new message with a strict timeout for serverless environments
        # Note: The Google GenAI SDK sync methods don't have a simple 'timeout' param in all versions,
        # but the underlying connection does. For hackathon speed, we assume Flash is fast enough (<2s).
        # We catch explicit errors.

        response = chat.send_message(text)

        return response.text.strip()

    except Exception as e:
        print(f"LLM Error: {e}")
        # Fallback response in case of timeout or API error
        return "Sir network issue here, one minute... checking with son."
