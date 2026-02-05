from fastapi import FastAPI, Depends
from app.auth import verify_api_key
from app.scam_detector import is_scam
from app.agent import generate_reply
from app.session_manager import update_session, get_session, add_intelligence
from app.intelligence import extract_intelligence

app = FastAPI(title="ScamTrap AI Honeypot")

@app.post("/detect", dependencies=[Depends(verify_api_key)])
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

        session_data = get_session(session_id)

        return {
            "status": "success",
            "reply": reply,
            "intelligence": session_data["intelligence"],
            "totalMessages": session_data["total_messages"]
        }

    return {"status": "clean"}
