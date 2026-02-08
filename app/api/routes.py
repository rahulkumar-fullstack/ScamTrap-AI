from fastapi import APIRouter, Depends, Header, HTTPException
from app.core.config import settings
from app.services.detector import is_scam
from app.services.agent import generate_reply
from app.services.session_store import add_message, get_history
from app.services.intelligence import extract_intelligence
from app.services.callback import send_final_result
from app.core.lifecycle import should_finalize, generate_agent_notes



# verify API key for authentication
async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Unauthorized - Invalid API Key")
    
# Apply API key dependency to all routes in this router
router = APIRouter(dependencies=[Depends(verify_api_key)]) 

@router.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "ScamTrap AI",
        "version": "2.0"
    }


@router.post("/")
async def handle_message(payload: dict):
    session_id = payload["sessionId"]
    message = payload["message"]

    # 1. Store incoming scammer message
    await add_message(session_id, message)

    # 2. Detect scam intent
    scam_detected = await is_scam(message["text"])

    reply = None

    # 3. Agent engages
    if scam_detected:
        reply = await generate_reply(message["text"])

        agent_msg = {
            "sender": "user",
            "text": reply
        }

        await add_message(session_id, agent_msg)

    # 4. Build conversation history
    history = await get_history(session_id)

    # 5. Extract intelligence
    intelligence = await extract_intelligence(history)

    # 6. Lifecycle decision
    total_messages = len(history)

    if scam_detected and should_finalize(total_messages, intelligence):

        notes = generate_agent_notes(intelligence)

        await send_final_result(
            session_id=session_id,
            scam_detected=True,
            total_messages=total_messages,
            intelligence=intelligence,
            agent_notes=notes
        )

    # 7. Response to platform
    return {
        "status": "success",
        "scamDetected": scam_detected,
        "reply": reply,
        "intelligence": intelligence
    }
