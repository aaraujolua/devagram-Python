from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    name: str
    user: Optional[str] = None
    password: str

app = FastAPI()

@app.get("/api/health", tags=["Health"])
async def health():
    return {
        "status": "OK!"
    }