import asyncio
from collections import defaultdict

# sessionId → list of messages
_sessions = defaultdict(list)

# async lock for thread safety
_lock = asyncio.Lock()


async def add_message(session_id: str, message: dict):
    async with _lock:
        _sessions[session_id].append(message)


async def get_history(session_id: str):
    async with _lock:
        return list(_sessions[session_id])


async def clear_session(session_id: str):
    async with _lock:
        _sessions.pop(session_id, None)
