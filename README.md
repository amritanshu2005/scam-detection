# Scam Detection API

This project implements a scam detection API designed for the Guvi Hackathon. It features a rule-based agent named "Ramesh" to simulate a vulnerable user and extract intelligence from potential scammers.

## Project Structure

- **main.py**: The entry point for the FastAPI application.
- **config.py**: Configuration settings and API key management.
- **models.py**: Pydantic models for request and response validation.
- **detector/scam_detector.py**: Logic for detecting scam attempts based on keyword analysis.
- **agent/agent.py**: Rule-based agent logic simulating the persona.
- **extractor/intelligence.py**: Logic for extracting phone numbers, UPI IDs, and other critical information.
- **callback/guvi.py**: Implementation of the feedback callback to the hackathon platform.
- **requirements.txt**: List of Python dependencies.

## Installation

1.  Clone the repository and navigate to the project directory.

2.  Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  Start the FastAPI server:

    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```

2.  The API will be available at `http://localhost:8000`.

## API Endpoint

**POST /api/v1/message**

This endpoint handles incoming messages, detects scams, generates a response from the agent, and triggers a callback if necessary.

**Request Header:**

- `x-api-key`: Your secure API key.

**Request Body:**

```json
{
  "sessionId": "string",
  "message": {
    "sender": "string",
    "text": "string",
    "timestamp": "string"
  },
  "conversationHistory": [
    {
      "sender": "string",
      "text": "string",
      "timestamp": "string"
    }
  ],
  "metadata": {}
}
```

**Response Body:**

```json
{
  "status": "success",
  "reply": "string"
}
```

## Features

- **Generative AI Persona ("Ramesh")**: Utilizes Google Gemini 1.5 Flash to simulate a hyper-realistic, non-tech-savvy persona that dynamically adapts to scammer tactics, effectively wasting their time while extracting intelligence.
- **Scam Detection**: Uses keyword analysis to identify potential scams.
- **Rule-Based Fallback**: Ensures reliability even if the AI service encounters issues.
- **Intelligence Extraction**: Extracts phone numbers, UPI IDs, and bank account details from the conversation.
- **Callback Mechanism**: Automatically sends conversation data to the hackathon platform when specific criteria are met.

## License

This project is open source and available under the MIT License.
