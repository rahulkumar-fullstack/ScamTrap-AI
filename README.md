# ScamTrap-AI

ScamTrap-AI is an AI-powered honey-pot system that detects scam messages and engages scammers to extract intelligence like UPI IDs, bank details, and phishing links.

This project was built for the **GUVI Hackathon**.

🔗 Live API: https://scamtrap-ai.onrender.com/docs

---

## Overview

The system:

- Detects scam intent in messages
- Switches to an autonomous AI agent
- Engages scammers in conversation
- Extracts useful scam intelligence
- Returns structured JSON output

---
## Tech Stack

- FastAPI
- Sentence Transformers
- Model: `all-MiniLM-L6-v2`
- Python

---
## Architecture

Message → Scam Detection → Agent → Extraction → JSON Response

---
## Run Locally

Clone the repo:

```bash
git clone https://github.com/rahulkumar-fullstack/ScamTrap-AI.git
cd ScamTrap-AI
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run server:
```bash
uvicorn app.main:app --reload
```

Open docs:
```
http://127.0.0.1:8000/docs
```

---

## Example Output

```json
{
  "scam_detected": true,
  "extracted_data": {
    "upi_ids": ["fraud@upi"],
    "urls": ["http://fake-site.com"]
  }
}
```

---

## License

MIT License
