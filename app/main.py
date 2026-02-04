from fastapi import FastAPI, Depends
from app.auth import verify_api_key
from app.scam_detector import is_scam
from app.agent import generate_reply

app = FastAPI(title="ScamTrap AI Honeypot")

@app.post("/detect", dependencies=[Depends(verify_api_key)])
def detect(message: dict):
    text = message.get("text", "")
    scam = is_scam(text)

    if scam:
        reply = generate_reply()
        return {
            "status": "success",
            "scamDetected": True,
            "reply": reply
        }

    return {
        "status": "clean",
        "scamDetected": False
    }

'''
@app.get("/", dependencies=[Depends(verify_api_key)])
def home():
    return {"message": "ScamTrap AI is running 🚀"}

@app.get("/health")
def health():
    return {"status": "ok"}
'''