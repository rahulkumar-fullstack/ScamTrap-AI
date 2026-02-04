from fastapi import FastAPI

app = FastAPI()

# Demo API - fastapi dev test.py
@app.get("/")
async def read_root():
    return {"Hello": "World","Message":"This is a test API for FastAPI"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

''' Async version of the above API
@app.get("/")
async def read_root():
     return {"Hello": "World","Message":"This is a test API for FastAPI"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
'''

