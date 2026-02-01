// Configuration
const API_BASE_URL = window.location.origin;
const API_KEY = 'test-api-key-12345';

// State
let currentConversationId = null;
let stats = {
    totalMessages: 0,
    scamsDetected: 0,
    intelligenceFound: 0,
    totalEngagement: 0,
    engagementCount: 0
};

let intelligence = {
    bank_accounts: [],
    upi_ids: [],
    phishing_urls: []
};

// Example messages
const examples = [
    "Your bank account has been suspended due to suspicious activity. Click here to verify: http://fake-bank-verify.com/secure",
    "Congratulations! You have won 1,00,000 rupees in our lottery! Send your bank account number to claim your prize immediately!",
    "Urgent: Your UPI needs verification. Share your UPI ID and account details to reactivate your account. Account number: 123456789012",
    "Your account will be blocked in 24 hours. Verify now at https://suspicious-link.com/verify?token=abc123"
];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    updateStats();
    updateIntelligenceSummary();
    loadPerformanceMetrics();
    // Refresh performance metrics every 10 seconds
    setInterval(loadPerformanceMetrics, 10000);
});

// Set example message
function setExample(index) {
    document.getElementById('messageInput').value = examples[index];
}

// Send message
async function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();
    
    if (!message) {
        alert('Please enter a message');
        return;
    }
    
    // Show loading state
    const sendBtn = document.querySelector('.send-btn');
    const originalText = sendBtn.innerHTML;
    sendBtn.innerHTML = '<span class="loading"></span> Processing...';
    sendBtn.disabled = true;
    
    try {
        const payload = {
            message: message
        };
        
        if (currentConversationId) {
            payload.conversation_id = currentConversationId;
        }
        
        const response = await fetch(`${API_BASE_URL}/api/v1/message`, {
            method: 'POST',
            headers: {
                'X-API-Key': API_KEY,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Update conversation ID
        currentConversationId = data.conversation_id;
        
        // Add messages to conversation
        addMessageToConversation(message, 'scammer');
        if (data.response_message) {
            addMessageToConversation(data.response_message, 'agent');
        }
        
        // Update stats
        stats.totalMessages++;
        if (data.scam_detected) {
            stats.scamsDetected++;
        }
        
        const intelCount = data.extracted_intelligence.bank_accounts.length +
                         data.extracted_intelligence.upi_ids.length +
                         data.extracted_intelligence.phishing_urls.length;
        stats.intelligenceFound += intelCount;
        
        if (data.engagement_metrics.conversation_duration_seconds) {
            stats.totalEngagement += data.engagement_metrics.conversation_duration_seconds;
            stats.engagementCount++;
        }
        
        updateStats();
        
        // Update intelligence
        updateIntelligence(data.extracted_intelligence);
        
        // Show response card
        showResponse(data);
        
        // Clear input
        messageInput.value = '';
        
    } catch (error) {
        console.error('Error:', error);
        alert('Error processing message: ' + error.message);
    } finally {
        sendBtn.innerHTML = originalText;
        sendBtn.disabled = false;
    }
}

// Add message to conversation
function addMessageToConversation(message, role) {
    const container = document.getElementById('conversationContainer');
    
    // Remove empty state if present
    const emptyState = container.querySelector('.empty-state');
    if (emptyState) {
        emptyState.remove();
    }
    
    const messageBubble = document.createElement('div');
    messageBubble.className = `message-bubble ${role}`;
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.textContent = message;
    
    const messageMeta = document.createElement('div');
    messageMeta.className = 'message-meta';
    messageMeta.textContent = `${role === 'scammer' ? 'Scammer' : 'AI Agent'} • ${new Date().toLocaleTimeString()}`;
    
    messageContent.appendChild(messageMeta);
    messageBubble.appendChild(messageContent);
    
    container.appendChild(messageBubble);
    
    // Scroll to bottom
    container.scrollTop = container.scrollHeight;
}

// Show response card
function showResponse(data) {
    const responseCard = document.getElementById('responseCard');
    const responseMessage = document.getElementById('responseMessage');
    const scamDetectedStatus = document.getElementById('scamDetectedStatus');
    const agentActivatedStatus = document.getElementById('agentActivatedStatus');
    const turnCount = document.getElementById('turnCount');
    
    responseMessage.textContent = data.response_message || 'No response generated';
    scamDetectedStatus.textContent = data.scam_detected ? 'Yes' : 'No';
    scamDetectedStatus.style.color = data.scam_detected ? '#10b981' : '#ef4444';
    agentActivatedStatus.textContent = data.agent_activated ? 'Yes' : 'No';
    agentActivatedStatus.style.color = data.agent_activated ? '#10b981' : '#ef4444';
    turnCount.textContent = data.engagement_metrics.turn_count;
    
    responseCard.style.display = 'block';
}

// Update intelligence
function updateIntelligence(newIntelligence) {
    // Merge new intelligence
    intelligence.bank_accounts = [...new Set([...intelligence.bank_accounts, ...newIntelligence.bank_accounts])];
    intelligence.upi_ids = [...new Set([...intelligence.upi_ids, ...newIntelligence.upi_ids])];
    intelligence.phishing_urls = [...new Set([...intelligence.phishing_urls, ...newIntelligence.phishing_urls])];
    
    updateIntelligenceSummary();
    updateIntelligenceDetails();
}

// Update intelligence summary
function updateIntelligenceSummary() {
    document.getElementById('bankCount').textContent = intelligence.bank_accounts.length;
    document.getElementById('upiCount').textContent = intelligence.upi_ids.length;
    document.getElementById('urlCount').textContent = intelligence.phishing_urls.length;
}

// Update intelligence details
function updateIntelligenceDetails() {
    const detailsCard = document.getElementById('intelligenceDetails');
    const bankList = document.getElementById('bankAccountsList');
    const upiList = document.getElementById('upiIdsList');
    const urlList = document.getElementById('phishingUrlsList');
    
    // Bank accounts
    bankList.innerHTML = '';
    if (intelligence.bank_accounts.length > 0) {
        intelligence.bank_accounts.forEach(account => {
            const item = document.createElement('div');
            item.className = 'intel-item-detail';
            item.textContent = account;
            bankList.appendChild(item);
        });
    } else {
        const item = document.createElement('div');
        item.className = 'intel-item-detail empty';
        item.textContent = 'No bank accounts found yet';
        bankList.appendChild(item);
    }
    
    // UPI IDs
    upiList.innerHTML = '';
    if (intelligence.upi_ids.length > 0) {
        intelligence.upi_ids.forEach(upi => {
            const item = document.createElement('div');
            item.className = 'intel-item-detail';
            item.textContent = upi;
            upiList.appendChild(item);
        });
    } else {
        const item = document.createElement('div');
        item.className = 'intel-item-detail empty';
        item.textContent = 'No UPI IDs found yet';
        upiList.appendChild(item);
    }
    
    // Phishing URLs
    urlList.innerHTML = '';
    if (intelligence.phishing_urls.length > 0) {
        intelligence.phishing_urls.forEach(url => {
            const item = document.createElement('div');
            item.className = 'intel-item-detail';
            item.textContent = url;
            urlList.appendChild(item);
        });
    } else {
        const item = document.createElement('div');
        item.className = 'intel-item-detail empty';
        item.textContent = 'No phishing URLs found yet';
        urlList.appendChild(item);
    }
    
    // Show details card if there's any intelligence
    if (intelligence.bank_accounts.length > 0 || 
        intelligence.upi_ids.length > 0 || 
        intelligence.phishing_urls.length > 0) {
        detailsCard.style.display = 'block';
    }
}

// Update statistics
function updateStats() {
    document.getElementById('totalMessages').textContent = stats.totalMessages;
    document.getElementById('scamsDetected').textContent = stats.scamsDetected;
    document.getElementById('intelligenceFound').textContent = stats.intelligenceFound;
    
    const avgEngagement = stats.engagementCount > 0 
        ? (stats.totalEngagement / stats.engagementCount).toFixed(1)
        : 0;
    document.getElementById('avgEngagement').textContent = avgEngagement + 's';
}

// Clear conversation
function clearConversation() {
    if (confirm('Are you sure you want to clear the conversation?')) {
        const container = document.getElementById('conversationContainer');
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-inbox"></i>
                <p>No messages yet. Send a test message to start!</p>
            </div>
        `;
        
        currentConversationId = null;
        intelligence = {
            bank_accounts: [],
            upi_ids: [],
            phishing_urls: []
        };
        
        updateIntelligenceSummary();
        document.getElementById('intelligenceDetails').style.display = 'none';
        document.getElementById('responseCard').style.display = 'none';
    }
}

// Allow Enter key to send (Shift+Enter for new line)
document.getElementById('messageInput').addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Load performance metrics
async function loadPerformanceMetrics() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/metrics`, {
            headers: {
                'X-API-Key': API_KEY
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            const perf = data.performance;
            
            document.getElementById('avgResponseTime').textContent = 
                (perf.avg_response_time * 1000).toFixed(0) + 'ms';
            document.getElementById('agentResponseTime').textContent = 
                (perf.avg_agent_time * 1000).toFixed(0) + 'ms';
            
            const accuracy = stats.totalMessages > 0 
                ? ((stats.scamsDetected / stats.totalMessages) * 100).toFixed(1) + '%'
                : '-';
            document.getElementById('detectionAccuracy').textContent = accuracy;
            
            // Format uptime
            const hours = Math.floor(perf.uptime_seconds / 3600);
            const minutes = Math.floor((perf.uptime_seconds % 3600) / 60);
            document.getElementById('systemUptime').textContent = 
                `${hours}h ${minutes}m`;
        }
    } catch (error) {
        console.error('Error loading performance metrics:', error);
    }
}

