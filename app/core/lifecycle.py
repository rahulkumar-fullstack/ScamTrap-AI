import asyncio
import httpx
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from typing import Dict


RENDER_URL = "https://scamtrap-ai.onrender.com/health"


async def heartbeat():
    await asyncio.sleep(30)

    while True:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                await client.get(
                    RENDER_URL,
                    headers={"x-api-key": settings.api_key}
                )
                #print("Heartbeat ping successful")
        except Exception as e:
            print("Heartbeat failed:", e)

        await asyncio.sleep(600)

def should_finalize(total_messages: int,intelligence: Dict) -> bool:
    high_value_signal = (
        intelligence["upiIds"]
        or intelligence["phishingLinks"]
        or intelligence["bankAccounts"]
    )

    enough_conversation = total_messages >= 3

    return high_value_signal or enough_conversation

def generate_agent_notes(intelligence: Dict) -> str:
    notes = []

    if intelligence["upiIds"]:
        notes.append("Scammer requested UPI transfer")

    if intelligence["phishingLinks"]:
        notes.append("Phishing link shared")

    if intelligence["bankAccounts"]:
        notes.append("Bank account provided")

    if intelligence["suspiciousKeywords"]:
        notes.append("Used urgency language")

    if not notes:
        notes.append("General scam attempt detected")

    return "; ".join(notes)


@asynccontextmanager
async def lifespan(app: FastAPI):

    task = asyncio.create_task(heartbeat())

    yield

    task.cancel()
    #print("Shutdown complete")
