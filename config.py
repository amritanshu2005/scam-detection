import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY", "default-secret-key")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"
TIMEOUT = 5
