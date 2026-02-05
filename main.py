from fastapi import FastAPI, Header, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

load_dotenv()

# Get API_KEY early
API_KEY = os.getenv("API_KEY", "test-api-key-12345")

app = FastAPI(title="Scam Detection API")

# Session storage for conversation tracking (in-memory)
sessions = {}

# Define models directly here to avoid import issues
class MessageDetail(BaseModel):
    sender: str
    text: str
    timestamp: str

class IncomingRequest(BaseModel):
    sessionId: str
    message: MessageDetail
    conversationHistory: List[MessageDetail] = []
    metadata: Optional[Dict[str, Any]] = None

class OutgoingResponse(BaseModel):
    status: str
    reply: str
    is_scam: bool = False
    intel: Optional[Dict[str, Any]] = None

# Import the business logic
from detector.scam_detector import detect
from agent.agent import generate_reply
from extractor.intelligence import extract
from callback.guvi import send_callback

# ==========================================
# INLINED FRONTEND (CSS & JS)
# This ensures it works on Vercel Serverless
# ==========================================
HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agentic Honey-Pot Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        /* INLINED STYLES.CSS */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        :root {
            --bg-main: #e0f2fe; --bg-card: #ffffff; --text-main: #0f172a; --text-muted: #475569;
            --primary: #a855f7; --secondary: #3b82f6; --accent: #f43f5e; --success: #10b981;
            --warning: #f59e0b; --border-color: #000000; --border-width: 3px; --shadow-offset: 5px;
        }
        body {
            font-family: "Inter", sans-serif; background-color: var(--bg-main);
            background-image: radial-gradient(#000000 1px, transparent 1px); background-size: 24px 24px;
            color: var(--text-main); min-height: 100vh; padding-bottom: 40px;
        }
        h1, h2, h3, h4, .logo, .stat-value { font-family: "Space Grotesk", sans-serif; }
        .container { max-width: 1400px; margin: 0 auto; padding: 24px; }
        .header {
            background: #ffd43b; border: var(--border-width) solid var(--border-color);
            box-shadow: var(--shadow-offset) var(--shadow-offset) 0px 0px var(--border-color);
            border-radius: 12px; padding: 20px 32px; margin-bottom: 32px;
            display: flex; justify-content: space-between; align-items: center;
        }
        .logo { display: flex; align-items: center; gap: 16px; }
        .logo i { font-size: 36px; }
        .logo h1 { font-size: 32px; font-weight: 700; text-transform: uppercase; letter-spacing: -1px; }
        .status-indicator {
            background: var(--bg-card); border: 2px solid var(--border-color);
            padding: 8px 16px; border-radius: 50px; font-weight: 700;
            display: flex; align-items: center; gap: 8px; box-shadow: 3px 3px 0 0 #000;
        }
        .status-dot {
            width: 12px; height: 12px; background: var(--success);
            border: 2px solid var(--border-color); border-radius: 50%;
            animation: blink 1s infinite alternate;
        }
        @keyframes blink { from { opacity: 1; } to { opacity: 0.4; } }
        .dashboard { display: grid; grid-template-columns: 1fr 1.4fr; gap: 32px; }
        .card {
            background: var(--bg-card); border: var(--border-width) solid var(--border-color);
            box-shadow: var(--shadow-offset) var(--shadow-offset) 0px 0px var(--border-color);
            border-radius: 12px; padding: 24px; margin-bottom: 32px;
        }
        .card h2 {
            font-size: 24px; font-weight: 700; margin-bottom: 24px;
            display: flex; align-items: center; gap: 12px;
            border-bottom: 3px solid var(--border-color); padding-bottom: 12px;
        }
        textarea {
            width: 100%; padding: 16px; background: #f8fafc;
            border: 3px solid var(--border-color); border-radius: 8px;
            font-size: 16px; font-family: "Inter", sans-serif; resize: vertical;
        }
        textarea:focus { outline: none; background: #fff; box-shadow: 4px 4px 0 0 #000; }
        .quick-examples { margin: 20px 0; display: flex; flex-wrap: wrap; gap: 12px; }
        .label { font-weight: 700; margin-right: 8px; text-transform: uppercase; font-size: 14px; }
        .example-btn {
            padding: 8px 16px; background: #bae6fd; border: 2px solid var(--border-color);
            border-radius: 6px; font-weight: 600; cursor: pointer;
            font-family: "Space Grotesk", sans-serif; box-shadow: 2px 2px 0 0 #000;
        }
        .example-btn:hover { transform: translate(-2px, -2px); box-shadow: 4px 4px 0 0 #000; }
        .send-btn {
            width: 100%; padding: 16px; background: var(--accent); color: white;
            font-family: "Space Grotesk", sans-serif; font-size: 20px; font-weight: 700;
            border: 3px solid var(--border-color); border-radius: 8px; cursor: pointer;
            box-shadow: 6px 6px 0 0 #000; text-transform: uppercase;
            display: flex; justify-content: center; align-items: center; gap: 12px;
        }
        .send-btn:hover { transform: translate(-3px, -3px); box-shadow: 9px 9px 0 0 #000; }
        .send-btn:active { transform: translate(2px, 2px); box-shadow: 2px 2px 0 0 #000; }
        .stats-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .stat-item {
            background: #f0fdf4; border: 3px solid var(--border-color);
            padding: 16px; text-align: center; border-radius: 8px; box-shadow: 4px 4px 0 0 #000;
        }
        .stat-value { font-size: 36px; font-weight: 700; display: block; margin-bottom: 8px; }
        .stat-label { font-size: 12px; font-weight: 700; text-transform: uppercase; color: var(--text-muted); }
        .conversation-container {
            height: 500px; overflow-y: auto; background: #f8fafc;
            border: 3px solid var(--border-color); box-shadow: inset 4px 4px 0 0 rgba(0,0,0,0.05);
            padding: 20px; display: flex; flex-direction: column; gap: 20px; border-radius: 8px;
        }
        .message-bubble { max-width: 80%; display: flex; flex-direction: column; }
        .message-bubble.scammer { align-self: flex-start; }
        .message-bubble.agent { align-self: flex-end; }
        .message-content {
            padding: 16px 20px; border: 3px solid var(--border-color);
            border-radius: 12px; font-size: 15px; line-height: 1.5; font-weight: 500;
        }
        .message-bubble.scammer .message-content { background: #fee2e2; border-bottom-left-radius: 0; box-shadow: 4px 4px 0 0 #000; }
        .message-bubble.agent .message-content { background: #dcfce7; border-bottom-right-radius: 0; box-shadow: -4px 4px 0 0 #000; text-align: right; }
        .message-meta { font-size: 11px; font-weight: 700; margin-top: 6px; text-transform: uppercase; opacity: 0.6; }
        .message-bubble.agent .message-meta { text-align: right; }
        .response-message {
            font-family: "Space Grotesk", sans-serif; font-size: 18px; padding: 24px;
            background: #c7d2fe; border: 3px solid var(--border-color);
            box-shadow: 4px 4px 0 0 #000; border-radius: 8px; margin-bottom: 24px;
        }
        .intel-item { margin-bottom: 12px; font-weight: 600; display: flex; align-items: center; gap: 10px; }
        .intel-item i { width: 20px; text-align: center; }
        @media (max-width: 768px) { .dashboard { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <div class="logo">
                <i class="fas fa-shield-alt"></i>
                <h1>Agentic Honey-Pot</h1>
            </div>
            <div class="status-indicator">
                <span class="status-dot"></span>
                <span>System Active</span>
            </div>
        </header>

        <div class="dashboard">
            <div class="left-panel">
                <div class="card message-input-card">
                    <h2><i class="fas fa-comment-dots"></i> Simulate Scam Message</h2>
                    <div class="input-group">
                        <textarea id="messageInput" placeholder="Enter a scam message..." rows="4"></textarea>
                    </div>
                    <div class="quick-examples">
                        <span class="label">Quick Examples:</span>
                        <button class="example-btn" onclick="setExample(0)">Bank</button>
                        <button class="example-btn" onclick="setExample(1)">Prize</button>
                        <button class="example-btn" onclick="setExample(2)">UPI</button>
                    </div>
                    <button class="send-btn" onclick="sendMessage()">
                        <i class="fas fa-paper-plane"></i> Process Message
                    </button>
                </div>

                <div class="card stats-card">
                    <h2><i class="fas fa-chart-line"></i> Session Stats</h2>
                    <div class="stats-grid">
                        <div class="stat-item">
                            <div class="stat-value" id="totalMessages">0</div>
                            <div class="stat-label">Messages</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value" id="scamsDetected">0</div>
                            <div class="stat-label">Scams</div>
                        </div>
                    </div>
                </div>

                <div class="card intelligence-card">
                    <h2><i class="fas fa-search"></i> Extracted Intel</h2>
                    <div class="intelligence-summary">
                        <div class="intel-item"><i class="fas fa-university"></i> Bank Accounts: <strong id="bankCount">0</strong></div>
                        <div class="intel-item"><i class="fas fa-mobile-alt"></i> UPI IDs: <strong id="upiCount">0</strong></div>
                        <div class="intel-item"><i class="fas fa-link"></i> Links: <strong id="urlCount">0</strong></div>
                    </div>
                </div>
            </div>

            <div class="right-panel">
                <div class="card conversation-card">
                    <div class="card-header" style="display:flex; justify-content:space-between;">
                        <h2><i class="fas fa-comments"></i> Conversation</h2>
                        <button onclick="location.reload()" style="background:none; border:none; cursor:pointer; font-weight:bold;">Clear</button>
                    </div>
                    <div class="conversation-container" id="conversationContainer">
                        <div class="empty-state" style="text-align:center; padding-top:100px; opacity:0.5;">
                            <i class="fas fa-inbox" style="font-size:48px;"></i>
                            <p>No messages yet.</p>
                        </div>
                    </div>
                </div>

                <div class="card response-card" id="responseCard" style="display: none;">
                    <h2><i class="fas fa-robot"></i> Agent Reply</h2>
                    <div class="response-message" id="responseMessage"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // INLINED SCRIPT.JS
        const API_BASE_URL = window.location.origin;
        // Try to get key from URL ?key=XYZ or prompt user if missing in code
        const API_KEY = "test-api-key-12345";

        let stats = { totalMessages: 0, scamsDetected: 0 };
        let intelligence = { bank_accounts: [], upi_ids: [], phishing_urls: [] };

        const examples = [
            "Your bank account has been suspended due to suspicious activity. Click here to verify: http://fake-bank-verify.com/secure",
            "Congratulations! You have won 1,00,000 rupees in our lottery! Send your bank account number.",
            "Urgent: Your UPI needs verification. Share your UPI ID and account details to reactivate your account."
        ];

        function setExample(index) {
            document.getElementById('messageInput').value = examples[index];
        }

        async function sendMessage() {
            const messageInput = document.getElementById('messageInput');
            const message = messageInput.value.trim();
            if (!message) return alert('Please enter a message');

            const sendBtn = document.querySelector('.send-btn');
            const originalText = sendBtn.innerHTML;
            sendBtn.innerHTML = '⏳ Processing...';
            sendBtn.disabled = true;

            try {
                const payload = {
                    sessionId: "session-" + Date.now(),
                    message: {
                        sender: "scammer",
                        text: message,
                        timestamp: new Date().toISOString()
                    },
                    conversationHistory: [] // Simplification for UI demo
                };

                // Add current history from UI if we were building a full chat client
                // For hackathon demo, sending single turns is often safer to show detection

                const response = await fetch(`${API_BASE_URL}/api/v1/message`, {
                    method: 'POST',
                    headers: {
                        'X-API-Key': API_KEY,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                });

                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                const data = await response.json();

                addMessageToConversation(message, 'scammer');
                // Pass agent reply as an object so we can attach intel to the bubble
                addMessageToConversation({ text: data.reply, intel: data.intel }, 'agent');

                stats.totalMessages++;
                // If reply isn't the fallback, assume detection worked
                if (data.is_scam) stats.scamsDetected++;
                updateStats();

                // --- REAL-TIME INTEL EXTRACTION (CLIENT SIDE VISUALS) ---
                // 1. Bank Accounts (9-18 digits)
                const bankMatch = message.match(/\b\d{9,18}\b/);
                if(bankMatch) {
                    intelligence.bank_accounts.push(bankMatch[0]);
                    document.getElementById('bankCount').innerText = intelligence.bank_accounts.length;
                }

                // 2. UPI IDs (something@something)
                const upiMatch = message.match(/[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}/);
                if(upiMatch) {
                    intelligence.upi_ids.push(upiMatch[0]);
                    document.getElementById('upiCount').innerText = intelligence.upi_ids.length;
                }

                // 3. Links (http/https)
                const linkMatch = message.match(/https?:\/\/[^\s]+/);
                if(linkMatch) {
                    intelligence.phishing_urls.push(linkMatch[0]);
                    document.getElementById('urlCount').innerText = intelligence.phishing_urls.length;
                }
                // ---------------------------------------------------------

                showResponse(data);
                messageInput.value = '';

            } catch (error) {
                console.error(error);
                alert('Error: ' + error.message);
            } finally {
                sendBtn.innerHTML = originalText;
                sendBtn.disabled = false;
            }
        }

        function addMessageToConversation(message, role) {
            const container = document.getElementById('conversationContainer');
            const emptyState = container.querySelector('.empty-state');
            if (emptyState) emptyState.remove();

            const bubble = document.createElement('div');
            bubble.className = `message-bubble ${role}`;

            // Support both string messages and message objects with intel
            let contentText = '';
            let intel = null;
            if (typeof message === 'object' && message !== null) {
                contentText = message.text || '';
                intel = message.intel || null;
            } else {
                contentText = String(message);
            }

            const contentEl = document.createElement('div');
            contentEl.className = 'message-content';
            contentEl.textContent = contentText;
            bubble.appendChild(contentEl);

            // If agent bubble contains intel, render a small intel list below
            if (role === 'agent' && intel) {
                const intelBox = document.createElement('div');
                intelBox.style.marginTop = '8px';
                intelBox.style.padding = '8px';
                intelBox.style.borderTop = '1px dashed rgba(0,0,0,0.1)';
                intelBox.style.fontSize = '13px';
                intelBox.style.fontWeight = '700';
                intelBox.innerHTML = '<div style="margin-bottom:6px;">Extracted Intel:</div>';
                const u = document.createElement('ul');
                u.style.margin = '0'; u.style.paddingLeft = '18px'; u.style.fontWeight = '600';

                if (intel.upiIds && intel.upiIds.length) {
                    const li = document.createElement('li'); li.textContent = 'UPI: ' + intel.upiIds.join(', '); u.appendChild(li);
                }
                if (intel.bankAccounts && intel.bankAccounts.length) {
                    const li = document.createElement('li'); li.textContent = 'Accounts: ' + intel.bankAccounts.join(', '); u.appendChild(li);
                }
                if (intel.phoneNumbers && intel.phoneNumbers.length) {
                    const li = document.createElement('li'); li.textContent = 'Phones: ' + intel.phoneNumbers.join(', '); u.appendChild(li);
                }
                if (intel.phishingLinks && intel.phishingLinks.length) {
                    const li = document.createElement('li'); li.textContent = 'Links: ' + intel.phishingLinks.join(', '); u.appendChild(li);
                }
                if (intel.suspiciousKeywords && intel.suspiciousKeywords.length) {
                    const li = document.createElement('li'); li.textContent = 'Keywords: ' + intel.suspiciousKeywords.join(', '); u.appendChild(li);
                }

                if (u.childElementCount > 0) intelBox.appendChild(u);
                bubble.appendChild(intelBox);
            }

            const meta = document.createElement('div');
            meta.className = 'message-meta';
            meta.textContent = `${role === 'scammer' ? 'Scammer' : 'AI Agent'} • Just now`;
            bubble.appendChild(meta);

            container.appendChild(bubble);
            container.scrollTop = container.scrollHeight;
        }

        function showResponse(data) {
            const card = document.getElementById('responseCard');
            const msgEl = document.getElementById('responseMessage');
            // Clear previous
            msgEl.innerHTML = '';

            // If backend classified as scam, show badge and intel
            if (data.is_scam) {
                const badge = document.createElement('div');
                badge.style.background = '#fee2e2';
                badge.style.border = '2px solid #f43f5e';
                badge.style.padding = '8px 12px';
                badge.style.borderRadius = '8px';
                badge.style.fontWeight = '800';
                badge.style.marginBottom = '12px';
                badge.textContent = '⚠️ Scam Alert — classified as FRAUDULENT';
                msgEl.appendChild(badge);

                if (data.intel) {
                    const intelContainer = document.createElement('div');
                    intelContainer.style.marginBottom = '12px';
                    intelContainer.innerHTML = '<strong>Extracted Intel:</strong>';
                    const list = document.createElement('ul');
                    list.style.marginTop = '8px';
                    if (data.intel.upiIds && data.intel.upiIds.length) {
                        const li = document.createElement('li'); li.textContent = 'UPI: ' + data.intel.upiIds.join(', '); list.appendChild(li);
                    }
                    if (data.intel.bankAccounts && data.intel.bankAccounts.length) {
                        const li = document.createElement('li'); li.textContent = 'Accounts: ' + data.intel.bankAccounts.join(', '); list.appendChild(li);
                    }
                    if (data.intel.phoneNumbers && data.intel.phoneNumbers.length) {
                        const li = document.createElement('li'); li.textContent = 'Phones: ' + data.intel.phoneNumbers.join(', '); list.appendChild(li);
                    }
                    if (data.intel.phishingLinks && data.intel.phishingLinks.length) {
                        const li = document.createElement('li'); li.textContent = 'Links: ' + data.intel.phishingLinks.join(', '); list.appendChild(li);
                    }
                    if (list.childElementCount > 0) intelContainer.appendChild(list);
                    msgEl.appendChild(intelContainer);
                }
            }

            // Persona reply (may include alert prefix as well)
            const p = document.createElement('div');
            p.textContent = data.reply;
            msgEl.appendChild(p);

            card.style.display = 'block';
        }

        function updateStats() {
            document.getElementById('totalMessages').textContent = stats.totalMessages;
            document.getElementById('scamsDetected').textContent = stats.scamsDetected;
        }
    </script>
</body>
</html>
"""

# Now that API_KEY is defined, we can use it in verify_api_key
def verify_api_key(x_api_key: str):
    global API_KEY
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return HTML_TEMPLATE

@app.post("/api/v1/message", response_model=OutgoingResponse)
async def webhook(
    req: IncomingRequest,
    x_api_key: str = Header(...),
    background_tasks: BackgroundTasks = None,
):
    try:
        verify_api_key(x_api_key)

        text = req.message.text
        history = req.conversationHistory if req.conversationHistory else []
        session_id = req.sessionId

        # Initialize session if not exists
        if session_id not in sessions:
            sessions[session_id] = {
                "messages": [],
                "scam_detected": False,
                "total_messages": 0,
                "intelligence": {}
            }

        session = sessions[session_id]

        # 1. Detect scam
        is_scam = detect(text, history)
        if is_scam:
            session["scam_detected"] = True

        # 2. Generate reply from agent
        # Pass MessageDetail objects to generate_reply
        reply = generate_reply(text, history)

        # 3. Add current exchange to session history (scammer then agent)
        session["messages"].append({
            "sender": "scammer",
            "text": text,
            "timestamp": req.message.timestamp
        })
        session["messages"].append({
            "sender": "agent",
            "text": reply,
            "timestamp": req.message.timestamp
        })
        session["total_messages"] = len(session["messages"])

        # 4. Extract intelligence from full conversation
        full_conversation = [msg["text"] for msg in session["messages"]]
        full_text = " ".join(full_conversation)
        intel = extract(full_text)
        session["intelligence"] = intel

        # If scam detected, prepend a clear classification/alert so the reply answers
        # whether the message is fraudulent before continuing the persona reply.
        if is_scam:
            # Summarize any critical intel we found
            intel_summary_parts = []
            if intel.get("upiIds"):
                intel_summary_parts.append(f"UPI: {', '.join(intel.get('upiIds'))}")
            if intel.get("phoneNumbers"):
                intel_summary_parts.append(f"Phones: {', '.join(intel.get('phoneNumbers'))}")
            if intel.get("phishingLinks"):
                intel_summary_parts.append(f"Links: {', '.join(intel.get('phishingLinks'))}")
            if intel.get("bankAccounts"):
                intel_summary_parts.append(f"Accounts: {', '.join(intel.get('bankAccounts'))}")

            intel_summary = "; ".join(intel_summary_parts) if intel_summary_parts else ""

            alert_prefix = "⚠️ Scam Alert: This message appears fraudulent. DO NOT call or share any details."
            if intel_summary:
                alert_prefix += f" Detected intel: {intel_summary}."

            # Use a concise safety-first reply instead of emotional persona text.
            safety_text = (
                "This is fraudulent. Do not click any links or share personal/financial "
                "information. Contact your nearest police station and report the incident to your bank immediately."
            )
            reply = f"{alert_prefix}\n\n{safety_text}"

        # 5. Log detection results
        print(f"[SESSION {session_id}] Scam: {is_scam}, Messages: {session['total_messages']}, Intel: {len([i for i in intel.values() if isinstance(i, list) and len(i) > 0])}")

        # 6. Optionally trigger callback asynchronously (non-blocking)
        should_trigger_callback = (
            is_scam and (
                len(intel.get("upiIds", [])) > 0 or
                len(intel.get("bankAccounts", [])) > 0 or
                len(intel.get("phishingLinks", [])) > 0 or
                session["total_messages"] > 6
            )
        )
        if should_trigger_callback and background_tasks is not None:
            try:
                background_tasks.add_task(send_callback, session_id, session["total_messages"], intel, full_text)
                session["callback_sent"] = True
            except Exception as e:
                print(f"[ERROR] Failed to schedule callback: {e}")

        return OutgoingResponse(
            status="success",
            reply=reply,
            is_scam=is_scam,
            intel=intel
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Webhook processing failed: {str(e)}", exc_info=True)
        return OutgoingResponse(
            status="error",
            reply="Error processing message"
        )

# Note: Use run_server.py to start the server instead
