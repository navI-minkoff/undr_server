from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src import schemas
from src.dependencies import get_db_session
from src.schemas.token import TokenResponse
from src.services.auth import AuthService

router = APIRouter()


@router.post("/token", response_model=schemas.token.TokenResponse)
async def login_for_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db_session)):
    auth_service = AuthService(db)
    token = auth_service.login(form_data.username, form_data.password)
    return {"token": token, "token_type": "bearer"}


@router.post("/validate", response_model=schemas.token.TokenValidationResponse)
async def validate_token(token: str, db: Session = Depends(get_db_session)):
    auth_service = AuthService(db)
    return auth_service.validate_token(token)
