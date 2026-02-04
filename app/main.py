from fastapi import FastAPI, Depends
from app.auth import verify_api_key
from app.scam_detector import is_scam

app = FastAPI(title="ScamTrap AI Honeypot")

@app.post("/detect", dependencies=[Depends(verify_api_key)])
def detect(message: dict):
    text = message.get("text", "")
    result = is_scam(text)

    return {
        "scamDetected": result
    }

'''
@app.get("/", dependencies=[Depends(verify_api_key)])
def home():
    return {"message": "ScamTrap AI is running 🚀"}

@app.get("/health")
def health():
    return {"status": "ok"}
'''