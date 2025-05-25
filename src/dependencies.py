from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.entities.user import RoleEnum
from dotenv import load_dotenv
import os

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN", "fixed-api-token-123")


def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


security = HTTPBearer()


def get_api_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token != API_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return token


def get_current_moder_or_admin(token: str = Depends(get_api_token)):
    return RoleEnum.ADMIN


def get_current_admin(token: str = Depends(get_api_token)):
    return RoleEnum.ADMIN
