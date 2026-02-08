# 🕵️‍♂️ ScamTrap-AI

**ScamTrap-AI** is an async AI-powered honeypot that detects scam messages, engages scammers in realistic conversations, and extracts actionable intelligence like UPI IDs, bank accounts, phone numbers, phishing links, and suspicious keywords.  

🚀 Built for **GUVI Hackathon**  
🌐 API Docs: [https://scamtrap-ai.onrender.com/docs](https://scamtrap-ai.onrender.com/docs)

---

## 🔍 Features

- Detect scam intent in incoming messages (MiniLM + keywords)  
- Multi-turn human-like agent replies  
- Extracts actionable intelligence from scams  
- Tracks session memory per conversation  
- Sends final structured intelligence to GUVI callback  
- `/health` endpoint for uptime monitoring  

---

## 🧰 Tech Stack

- **FastAPI** (async web framework)  
- **Sentence Transformers** (MiniLM-L6-v2)  
- **Python 3.14+**  
- **httpx** (async HTTP client)  

---

## ▶️ Run Locally

```bash
git clone https://github.com/rahulkumar-fullstack/ScamTrap-AI.git
cd ScamTrap-AI
python -m venv venv
# Activate venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 🧪 Example API Call

**POST / with header:**
```
x-api-key: YOUR_SECRET_API_KEY
Content-Type: application/json
```

**Body:**
```
{
  "sessionId": "mega-test",
  "message": {
    "sender": "scammer",
    "text": "URGENT! Your bank account 1234-5678-9012 will be suspended. Verify now by sending payment to scammer@upi or call +919876543210. Click https://secure-bank-verify.in immediately.",
    "timestamp": "2026-01-21T10:10:00Z"
  }
}
```

**Response:**
```
{
  "status": "success",
  "scamDetected": true,
  "reply": "I'll check with IT myself.",
  "intelligence": {
    "bankAccounts": ["1234-5678-9012", "919876543210"],
    "upiIds": ["scammer@upi"],
    "phishingLinks": ["https://secure-bank-verify.in"],
    "phoneNumbers": ["+919876543210"],
    "suspiciousKeywords": ["suspended", "urgent", "verify", "payment"]
  }
}
```

## 🛡️ Health Check

```
GET /health (protected with x-api-key):

{
  "status": "ok",
  "service": "ScamTrap AI",
  "version": "2.0"
}
```

## 📦 GUVI Callback
```
Once scam detection and agent engagement complete, ScamTrap-AI sends structured intelligence to:

POST https://hackathon.guvi.in/api/updateHoneyPotFinalResult
```

## Example payload:

```
{
  "sessionId": "mega-test",
  "scamDetected": true,
  "totalMessagesExchanged": 3,
  "extractedIntelligence": {
    "bankAccounts": ["1234-5678-9012", "919876543210"],
    "upiIds": ["scammer@upi"],
    "phishingLinks": ["https://secure-bank-verify.in"],
    "phoneNumbers": ["+919876543210"],
    "suspiciousKeywords": ["suspended", "urgent", "verify", "payment"]
  },
  "agentNotes": "Scammer used urgency, payment request, and phishing link"
}

```

## 📜 License

- **MIT License**