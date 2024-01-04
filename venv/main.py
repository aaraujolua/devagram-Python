from fastapi import FastAPI
from routes.UserRoute import router as UserRoute #"as" apenas altera o nome do que está sendo importado para o que vc desejar

from pydantic import BaseModel
from typing import Optional


#class User(BaseModel):
    #name: str
    #user: Optional[str] = None
    #password: str

app = FastAPI()

app.include_router(UserRoute, tags=["User"], prefix="/api/user")

@app.get("/api/health", tags=["Health"])
async def health():
    return {
        "status": "OK!"
    }