import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY", "default-secret-key")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"
TIMEOUT = 5
