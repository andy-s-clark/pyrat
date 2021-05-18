from typing import Optional
from fastapi import FastAPI

app = FastAPI()


@app.get("/healthz")
async def read_health():
    return {"status": "OK"}


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
