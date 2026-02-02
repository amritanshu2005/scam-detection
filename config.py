import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY", "your-secret-api-key-here")
CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"
CALLBACK_TIMEOUT = 5
