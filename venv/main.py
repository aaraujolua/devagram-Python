from fastapi import FastAPI
from routes.UserRoute import router as UserRoute #"as" apenas altera o nome do que está sendo importado para o que vc desejar

app = FastAPI()

app.include_router(UserRoute, tags=["User"], prefix="/api/user")

@app.get("/api/health", tags=["Health"])
async def health():
    return {
        "status": "OK!"
    }