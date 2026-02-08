import httpx

GUVI_ENDPOINT = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

async def send_final_result(
    session_id: str,
    scam_detected: bool,
    total_messages: int,
    intelligence: dict,
    agent_notes: str
):
    payload = {
        "sessionId": session_id,
        "scamDetected": scam_detected,
        "totalMessagesExchanged": total_messages,
        "extractedIntelligence": intelligence,
        "agentNotes": agent_notes
    }

    async with httpx.AsyncClient(timeout=5) as client:
        await client.post(GUVI_ENDPOINT, json=payload)
