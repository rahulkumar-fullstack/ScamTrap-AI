from collections import defaultdict

sessions = defaultdict(lambda: {
    "messages": [],
    "total_messages": 0,
    "intelligence": {
        "upiIds": [],
        "phoneNumbers": [],
        "phishingLinks": [],
        "suspiciousKeywords": []
    }
})


def update_session(session_id: str, message: dict):
    sessions[session_id]["messages"].append(message)
    sessions[session_id]["total_messages"] += 1


def add_intelligence(session_id: str, intel: dict):
    for key in intel:
        sessions[session_id]["intelligence"][key].extend(intel[key])
        sessions[session_id]["intelligence"][key] = list(
            set(sessions[session_id]["intelligence"][key])
        )


def get_session(session_id: str):
    return sessions[session_id]
