import requests
from app.session_manager import get_session

CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"


def send_final_callback(session_id: str):
    session = get_session(session_id)

    payload = {
        "sessionId": session_id,
        "scamDetected": True,
        "totalMessagesExchanged": session["total_messages"],
        "extractedIntelligence": session["intelligence"],
        "agentNotes": "Scammer used urgency tactics and attempted data extraction"
    }

    try:
        response = requests.post(CALLBACK_URL, json=payload, timeout=5)
        print("Callback status:", response.status_code)
    except Exception as e:
        print("Callback failed:", e)
