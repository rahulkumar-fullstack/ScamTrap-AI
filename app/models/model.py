import asyncio
from sentence_transformers import SentenceTransformer
from app.core.config import settings

_model = None
_lock = asyncio.Lock()

async def load_model():
    global _model
    async with _lock:  # prevent race condition
        if _model is None:
            loop = asyncio.get_event_loop()

            _model = await loop.run_in_executor(
                None,
                lambda: SentenceTransformer(settings.minilm_model)
            )
    return _model

def get_model():
    if _model is None:
        raise RuntimeError("Model not loaded. Call load_model() at startup.")
    return _model
