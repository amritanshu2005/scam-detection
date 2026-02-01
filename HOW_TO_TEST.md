# 🧪 How to Test Your Agentic Honey-Pot System

## Quick Start Testing

### Step 1: Start the Server

```bash
cd c:\Users\amrit\OneDrive\Desktop\honey-trap
python main.py
```

Or using uvicorn:
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Step 2: Test via Web Dashboard (Easiest!)

1. **Open your browser** and go to:
   ```
   http://localhost:8000
   ```

2. **You'll see the beautiful dashboard!**

3. **Test with Quick Examples:**
   - Click "Bank Suspension" button
   - Click "Process Message"
   - Watch the conversation appear!
   - See scam detection status
   - View extracted intelligence

4. **Try different examples:**
   - Prize Winner
   - UPI Verification
   - Phishing Link

5. **Check the Statistics:**
   - Messages Processed count increases
   - Scams Detected count increases
   - Intelligence items appear

6. **View Intelligence Details:**
   - Scroll down to see extracted data
   - Bank accounts, UPI IDs, URLs

### Step 3: Test via API (Command Line)

#### Test 1: Health Check
```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "active",
  "service": "Agentic Honey-Pot API",
  "version": "1.0.0"
}
```

#### Test 2: Send a Scam Message
```bash
curl -X POST http://localhost:8000/api/v1/message ^
  -H "X-API-Key: test-api-key-12345" ^
  -H "Content-Type: application/json" ^
  -d "{\"message\": \"Your bank account is suspended! Verify at http://fake-bank.com\"}"
```

Expected response:
```json
{
  "conversation_id": "uuid-here",
  "scam_detected": true,
  "agent_activated": true,
  "response_message": "I want to make sure this is legitimate...",
  "engagement_metrics": {...},
  "extracted_intelligence": {
    "bank_accounts": [],
    "upi_ids": [],
    "phishing_urls": ["http://fake-bank.com"],
    "other_intelligence": {}
  },
  "timestamp": "2024-..."
}
```

#### Test 3: Multi-turn Conversation
```bash
# First message
curl -X POST http://localhost:8000/api/v1/message ^
  -H "X-API-Key: test-api-key-12345" ^
  -H "Content-Type: application/json" ^
  -d "{\"message\": \"You won a prize!\"}"

# Save the conversation_id from response, then:
curl -X POST http://localhost:8000/api/v1/message ^
  -H "X-API-Key: test-api-key-12345" ^
  -H "Content-Type: application/json" ^
  -d "{\"message\": \"Send your bank account number\", \"conversation_id\": \"YOUR_CONVERSATION_ID\"}"
```

### Step 4: Test with Python Script

Run the included test script:
```bash
python test_api.py
```

This will:
- Test health endpoint
- Test scam detection
- Test multi-turn conversations
- Show all results

### Step 5: Run Comprehensive Tests

```bash
# Install pytest if not already installed
pip install pytest pytest-asyncio

# Run all tests
pytest tests/test_system.py -v
```

This tests:
- ✅ Scam detection accuracy
- ✅ Intelligence extraction
- ✅ Multi-turn conversations
- ✅ Agent behavior
- ✅ API endpoints
- ✅ Performance

### Step 6: Check Performance Metrics

```bash
curl -H "X-API-Key: test-api-key-12345" http://localhost:8000/api/v1/metrics
```

Shows:
- Response times
- Detection times
- Agent response times
- System uptime
- Error rates

## Visual Testing Checklist

### ✅ Dashboard Tests

- [ ] Dashboard loads at http://localhost:8000
- [ ] All UI elements visible
- [ ] Quick example buttons work
- [ ] Message input accepts text
- [ ] "Process Message" button works
- [ ] Conversation appears in real-time
- [ ] Statistics update automatically
- [ ] Intelligence details show up
- [ ] Performance metrics display
- [ ] Clear conversation button works

### ✅ Scam Detection Tests

Test these messages (should detect as scams):

1. **Bank Suspension:**
   ```
   Your bank account has been suspended. Click here to verify: http://fake-bank.com
   ```
   ✅ Should detect: YES
   ✅ Should extract: URL

2. **Prize Winner:**
   ```
   Congratulations! You won 1 lakh rupees! Send your bank account number: 123456789012
   ```
   ✅ Should detect: YES
   ✅ Should extract: Bank account

3. **UPI Verification:**
   ```
   Urgent: Your UPI needs verification. Share your UPI ID: user@paytm
   ```
   ✅ Should detect: YES
   ✅ Should extract: UPI ID

4. **Phishing Link:**
   ```
   Your account will be blocked. Verify now at https://suspicious-site.com/verify
   ```
   ✅ Should detect: YES
   ✅ Should extract: URL

### ✅ Agent Response Tests

- [ ] Agent responds when scam detected
- [ ] Response is natural and believable
- [ ] Response length is reasonable (10-300 chars)
- [ ] Agent asks for more information
- [ ] Multi-turn conversation flows naturally

### ✅ Intelligence Extraction Tests

Test extraction with:

1. **Bank Account:**
   ```
   Send money to account 987654321098
   ```
   ✅ Should extract: 987654321098

2. **UPI ID:**
   ```
   Payment UPI: someone@ybl
   ```
   ✅ Should extract: someone@ybl

3. **Phishing URL:**
   ```
   Click here: http://fake-verify.com/secure
   ```
   ✅ Should extract: http://fake-verify.com/secure

## Common Issues & Solutions

### Issue: Server won't start
**Solution:**
- Check if port 8000 is already in use
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.11+)

### Issue: API returns 401 Unauthorized
**Solution:**
- Check API key matches: `test-api-key-12345`
- Verify header name: `X-API-Key` (not `X-API-KEY` or `api-key`)

### Issue: Dashboard doesn't load
**Solution:**
- Make sure server is running
- Check browser console for errors (F12)
- Try refreshing the page
- Clear browser cache

### Issue: No intelligence extracted
**Solution:**
- Make sure message contains extractable data (account numbers, UPI IDs, URLs)
- Check message format matches patterns
- Try different example messages

## Expected Results

### Successful Test Results:

1. **Health Check:**
   - Status: 200 OK
   - Response: `{"status": "active", ...}`

2. **Scam Message:**
   - `scam_detected`: `true`
   - `agent_activated`: `true`
   - `response_message`: Non-empty string
   - `extracted_intelligence`: Contains data if present

3. **Dashboard:**
   - Statistics update
   - Conversation appears
   - Intelligence shows
   - Performance metrics display

## Quick Test Commands

### Windows PowerShell:
```powershell
# Health check
Invoke-WebRequest http://localhost:8000/api/health | Select-Object -ExpandProperty Content

# Send message
$headers = @{"X-API-Key" = "test-api-key-12345"; "Content-Type" = "application/json"}
$body = '{"message": "Your account is suspended!"}' | ConvertTo-Json
Invoke-WebRequest -Uri http://localhost:8000/api/v1/message -Method POST -Headers $headers -Body $body | Select-Object -ExpandProperty Content
```

### Python Quick Test:
```python
import requests

# Health check
r = requests.get("http://localhost:8000/api/health")
print(r.json())

# Send scam message
headers = {"X-API-Key": "test-api-key-12345", "Content-Type": "application/json"}
data = {"message": "Your account is suspended! Verify at http://fake.com"}
r = requests.post("http://localhost:8000/api/v1/message", headers=headers, json=data)
print(r.json())
```

## Success Indicators

✅ **System is working if:**
- Dashboard loads and displays correctly
- Health endpoint returns 200 OK
- Scam messages are detected
- Agent generates responses
- Intelligence is extracted
- Statistics update
- No errors in logs

## Next Steps

Once testing passes:
1. ✅ Review extracted intelligence
2. ✅ Check performance metrics
3. ✅ Review logs in `logs/` directory
4. ✅ Test with different scam types
5. ✅ Try multi-turn conversations
6. ✅ Deploy to production!

---

**Your system is working correctly if all tests pass!** 🎉

