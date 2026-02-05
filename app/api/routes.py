from fastapi import APIRouter, Header, HTTPException
from app.core.config import settings

router = APIRouter()

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Unauthorized")

@router.get("/")
async def root(x_api_key: str = Header(...)):
    verify_api_key(x_api_key)
    return {"message": "ScamTrap AI Async API is running!"}
