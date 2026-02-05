from fastapi import FastAPI
from app.api.routes import router

# Create FastAPI instance
app = FastAPI(
    title="ScamTrap AI Honeypot",
   description="""
Async AI-powered honeypot for scam detection.

**Developer:** [Rahul Kumar](https://github.com/rahulkumar-fullstack)

**License:** [MIT](https://opensource.org/licenses/MIT)
""",
    version="2.0"
)

# Include routes from router
app.include_router(router)
