from fastapi import FastAPI
from routes.UserRoute import router as UserRoute #"as" apenas altera o nome do que está sendo importado para o que vc desejar
from routes.AuthRoute import router as AuthRoute
from routes.PostRoute import router as PostRoute
from fastapi.middleware.cors import CORSMiddleware


origins = [
    "*"
]  

app = FastAPI()

app.include_router(UserRoute, tags=["User"], prefix="/api/user")
app.include_router(AuthRoute, tags=["Auth"], prefix="/api/auth")
app.include_router(PostRoute, tags=["Post"], prefix="/api/post")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", tags=["Health"])
async def health():
    return {
        "status": "OK!"
    }
    