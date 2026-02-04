from collections import defaultdict

# In-memory session storage
sessions = defaultdict(lambda: {
    "messages": [],
    "total_messages": 0
})


def update_session(session_id: str, message: dict):
    sessions[session_id]["messages"].append(message)
    sessions[session_id]["total_messages"] += 1


def get_session(session_id: str):
    return sessions[session_id]
