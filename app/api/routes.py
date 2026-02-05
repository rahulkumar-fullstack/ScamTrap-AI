from fastapi import APIRouter, Depends, Header, HTTPException
from app.core.config import settings

# verify API key for authentication
async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Unauthorized - Invalid API Key")
    
# Create API router
router = APIRouter(dependencies=[Depends(verify_api_key)]) # Apply API key dependency to all routes in this router

@router.get("/")
async def root():
    return {"message": "ScamTrap AI Async API is running!"}
