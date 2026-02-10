import asyncio
from sentence_transformers import SentenceTransformer

_model = None
_lock = asyncio.Lock()

async def get_model():
    global _model
    if _model is None:
        async with _lock:
            if _model is None:  # double-checked locking
                # Load model off the main thread
                loop = asyncio.get_event_loop()
                _model = await loop.run_in_executor(
                    None,
                    lambda: SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
                )
    return _model
