# 🕵️‍♂️ ScamTrap-AI

ScamTrap-AI is an 🤖 AI-powered honeypot system that detects scam messages and actively engages scammers to extract actionable intelligence such as UPI IDs, bank details, and phishing links.

🚀 This project was built for the GUVI Hackathon.

🌐 Public API (Hosted on **Render**):
👉 https://scamtrap-ai.onrender.com/docs


---

🔍 Overview

ScamTrap-AI works as an autonomous scam-interaction engine:

🚨 Detects scam intent in incoming messages

🧠 Switches to an AI agent when a scam is detected

💬 Engages scammers in realistic conversation

🕵️ Extracts valuable scam intelligence

📦 Returns structured JSON output



---

🧰 Tech Stack

- ⚡ FastAPI

- 🧠 Sentence Transformers

- 📊 Model: all-MiniLM-L6-v2

- 🐍 Python



---

🏗️ Architecture

Message → Scam Detection → AI Agent → Data Extraction → JSON Response


---

▶️ Run Locally

Clone the repository
```
git clone https://github.com/rahulkumar-fullstack/ScamTrap-AI.git
cd ScamTrap-AI
```
Install dependencies
```
pip install -r requirements.txt
```
Start the server
```
uvicorn app.main:app --reload
```
Open API docs
```
http://127.0.0.1:8000/docs

```
---

🧪 Example Output
```
{
  "scam_detected": true,
  "extracted_data": {
    "upi_ids": ["fraud@upi"],
    "urls": ["http://fake-site.com"]
  }
}

```
---

📜 License

MIT License


---
