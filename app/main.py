from fastapi import FastAPI, Depends
from app.auth import verify_api_key

app = FastAPI(title="ScamTrap AI Honeypot")

@app.get("/", dependencies=[Depends(verify_api_key)])
def home():
    return {"message": "ScamTrap AI is running 🚀"}

@app.get("/health")
def health():
    return {"status": "ok"}