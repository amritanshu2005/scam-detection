# Agentic Honey-Pot for Scam Detection & Intelligence Extraction

An AI-powered system that detects scam messages and autonomously engages scammers to extract actionable intelligence such as bank account details, UPI IDs, and phishing links through multi-turn conversations.

## Features

- **Beautiful Web Dashboard**: Modern, responsive UI with dark theme for real-time monitoring
- **Scam Detection**: Pattern-based detection of scam intent in incoming messages
- **Autonomous AI Agent**: Maintains believable human persona and engages scammers strategically
- **Intelligence Extraction**: Extracts bank accounts, UPI IDs, phishing URLs, and other intelligence
- **Multi-turn Conversations**: Supports conversation history and context management
- **RESTful API**: Public API endpoint with API key authentication
- **Structured Output**: Returns standardized JSON responses with engagement metrics
- **Real-time Visualization**: Live conversation view, statistics, and intelligence display

## Architecture

```
┌─────────────────┐
│  Mock Scammer   │
│      API        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FastAPI Server │
│  (main.py)      │
└────────┬────────┘
         │
    ┌────┴────┬──────────────┬──────────────┐
    ▼         ▼              ▼              ▼
┌────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ Scam   │ │   AI     │ │Intelligence│ │Conversation│
│Detector│ │  Agent   │ │ Extractor │ │  Manager  │
└────────┘ └──────────┘ └──────────┘ └──────────┘
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd honey-trap
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your API_KEY and optional OPENAI_API_KEY
```

## Configuration

Create a `.env` file with the following variables:

```env
API_KEY=your-secret-api-key-here
OPENAI_API_KEY=your-openai-api-key-optional
```

- `API_KEY`: Required. Used to secure your API endpoint
- `OPENAI_API_KEY`: Optional. If provided, the AI agent will use GPT-3.5-turbo. Otherwise, it uses a rule-based approach.

## Running the Server

### Development Mode

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Access the Web Dashboard

Once the server is running, open your browser and visit:
- **Dashboard**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

The dashboard provides:
- Interactive message testing interface
- Real-time conversation visualization
- Statistics and engagement metrics
- Intelligence extraction display
- Beautiful, modern UI with dark theme

### Production Mode

For production deployment, use a production ASGI server:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Or use gunicorn with uvicorn workers:

```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## API Endpoints

### 1. Health Check

```http
GET /
```

**Response:**
```json
{
  "status": "active",
  "service": "Agentic Honey-Pot API",
  "version": "1.0.0"
}
```

### 2. Process Message (Main Endpoint)

```http
POST /api/v1/message
Headers:
  X-API-Key: your-secret-api-key-here
Content-Type: application/json
```

**Request Body:**
```json
{
  "message": "Your account has been suspended. Click here to verify: http://fake-bank.com/verify",
  "conversation_id": "optional-existing-conversation-id",
  "sender_id": "optional-sender-identifier",
  "metadata": {}
}
```

**Response:**
```json
{
  "conversation_id": "uuid-here",
  "scam_detected": true,
  "agent_activated": true,
  "response_message": "I want to make sure this is legitimate. Can you explain what this is about?",
  "engagement_metrics": {
    "turn_count": 1,
    "conversation_duration_seconds": 2.5,
    "messages_exchanged": 2,
    "intelligence_items_found": 1
  },
  "extracted_intelligence": {
    "bank_accounts": [],
    "upi_ids": [],
    "phishing_urls": ["http://fake-bank.com/verify"],
    "other_intelligence": {}
  },
  "timestamp": "2024-01-15T10:30:00.000000"
}
```

### 3. Get Conversation

```http
GET /api/v1/conversation/{conversation_id}
Headers:
  X-API-Key: your-secret-api-key-here
```

## How It Works

1. **Message Reception**: The API receives messages from the Mock Scammer API
2. **Scam Detection**: The `ScamDetector` analyzes the message for scam indicators
3. **Agent Activation**: If scam is detected, the autonomous AI agent is activated
4. **Response Generation**: The agent generates a believable human response
5. **Intelligence Extraction**: The `IntelligenceExtractor` scans the conversation for actionable intelligence
6. **Response Return**: Structured JSON response is returned with all metrics and extracted data

## Intelligence Extraction

The system extracts:

- **Bank Account Numbers**: 9-18 digit account numbers
- **UPI IDs**: UPI payment IDs and links
- **Phishing URLs**: Suspicious URLs and links
- **Other Intelligence**: IFSC codes, phone numbers, email addresses

## Agent Behavior

The autonomous agent:

- Maintains a consistent human persona
- Gradually increases engagement (skeptical → interested → engaged → extracting)
- Asks for specific intelligence without revealing detection
- Adapts responses based on conversation stage
- Uses either OpenAI GPT-3.5-turbo or rule-based responses

## Deployment

### Using Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Using Cloud Platforms

- **Heroku**: Use the included `Procfile`
- **AWS Lambda**: Use Mangum adapter
- **Google Cloud Run**: Deploy container
- **Railway/Render**: Direct deployment

## Testing

Test the API using curl:

```bash
curl -X POST http://localhost:8000/api/v1/message \
  -H "X-API-Key: your-secret-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "You have won a prize! Click here: http://scam.com/claim"
  }'
```

## Performance Considerations

- **In-memory storage**: Current implementation uses in-memory conversation storage. For production, use Redis or a database.
- **Rate limiting**: Consider adding rate limiting middleware
- **Logging**: Add comprehensive logging for monitoring
- **Error handling**: Enhance error handling for edge cases

## Security

- API key authentication required for all endpoints
- Input validation and sanitization
- CORS configured for public API access
- Consider adding rate limiting and DDoS protection in production

## License

MIT License

## Contributing

Contributions welcome! Please open an issue or submit a pull request.

