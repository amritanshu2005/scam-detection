# Quick Start Guide

## Setup (5 minutes)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   Create a `.env` file:
   ```env
   API_KEY=your-secret-api-key-here
   OPENAI_API_KEY=your-openai-key-optional
   ```

3. **Start the server:**
   ```bash
   python main.py
   ```
   Or:
   ```bash
   uvicorn main:app --reload
   ```

4. **Test the API:**
   ```bash
   python test_api.py
   ```

## API Usage Example

```python
import requests

url = "http://localhost:8000/api/v1/message"
headers = {
    "X-API-Key": "your-secret-api-key-here",
    "Content-Type": "application/json"
}

payload = {
    "message": "Your account is suspended! Verify at http://fake-bank.com"
}

response = requests.post(url, headers=headers, json=payload)
print(response.json())
```

## Key Features

✅ **Scam Detection** - Automatically detects scam intent  
✅ **AI Agent** - Engages scammers autonomously  
✅ **Intelligence Extraction** - Extracts bank accounts, UPI IDs, URLs  
✅ **Multi-turn Conversations** - Maintains conversation context  
✅ **Structured Output** - Returns standardized JSON responses  

## Deployment

### Local Testing
```bash
python main.py
```

### Production (Docker)
```bash
docker build -t honey-trap .
docker run -p 8000:8000 -e API_KEY=your-key honey-trap
```

### Cloud Platforms
- **Heroku**: `git push heroku main`
- **Railway**: Connect GitHub repo
- **Render**: Deploy from GitHub

## Next Steps

1. Customize the API key in `.env`
2. Optionally add OpenAI API key for better AI responses
3. Deploy to your preferred platform
4. Test with the Mock Scammer API

For detailed documentation, see [README.md](README.md)

