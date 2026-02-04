from fastapi import FastAPI

app = FastAPI(title="ScamTrap AI Honeypot")

@app.get("/")
def home():
    return {"message": "ScamTrap AI is running 🚀"}

@app.get("/health")
def health():
    return {"status": "ok"}