from fastapi import FastAPI, Depends
from app.auth import verify_api_key
from app.scam_detector import is_scam
from app.agent import generate_reply
from app.session_manager import update_session, get_session, add_intelligence
from app.intelligence import extract_intelligence
from app.session_manager import should_finalize
from app.callback import send_final_callback
import asyncio
import httpx

app = FastAPI(title="ScamTrap AI Honeypot")

@app.post("/", dependencies=[Depends(verify_api_key)])
def detect(payload: dict):
    session_id = payload.get("sessionId")
    message = payload.get("message", {})
    text = message.get("text", "")

    update_session(session_id, message)

    scam = is_scam(text)

    if scam:
        intel = extract_intelligence(text)
        add_intelligence(session_id, intel)

        reply = generate_reply()
        update_session(session_id, {
            "sender": "agent",
            "text": reply
        })

        if should_finalize(session_id):
            send_final_callback(session_id)

        session_data = get_session(session_id)

        return {
            "status": "success",
            "reply": reply,
            "intelligence": session_data["intelligence"],
            "totalMessages": session_data["total_messages"]
        }

    return {"status": "clean"}



@app.get("/health")
def health():
    return {"status": "ok"}

# Uptime on Render
async def heartbeat():
    await asyncio.sleep(30)
    while True:
        try:
            async with httpx.AsyncClient() as client:
                await client.get("https://scamtrap-ai.onrender.com/health")
        except Exception:
            pass
        await asyncio.sleep(600)  # 10 minutes

@app.on_event("startup")
async def start_heartbeat():
    asyncio.create_task(heartbeat())
