from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import users, auth
from src.database import engine
from src.models.base import Base
from src.models.user import User
from src.models.token import Token

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Token Auth API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])


@app.get("/")
async def root():
    return {"message": "Token Auth API is running"}
