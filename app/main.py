from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.routes import router
from app.models.model import load_model


@asynccontextmanager
async def lifespan(app: FastAPI):
    #print("Loading MiniLM model...")
    await load_model()
    #print("Model loaded successfully.")
    yield
   #print("Shutting down application...")


# Create FastAPI instance
app = FastAPI(
    title="ScamTrap AI Honeypot",
    description="""
Async AI-powered honeypot for scam detection.

**Developer:** [Rahul Kumar](https://github.com/rahulkumar-fullstack)

**License:** [MIT](https://opensource.org/licenses/MIT)
""",
    version="2.0",
    lifespan=lifespan
)

# Include routes
app.include_router(router)
