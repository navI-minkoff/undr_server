from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.schemas.token import TokenValidationResponse
from src.services.auth import AuthService
from src.dependencies import get_db_session, get_current_moder_or_admin, get_api_token

router = APIRouter()


def get_auth_service(db: Session = Depends(get_db_session)):
    return AuthService(db)


@router.post("/validate", response_model=TokenValidationResponse)
async def validate_token(token: str, db: Session = Depends(get_db_session), _: str = Depends(get_api_token)):
    auth_service = get_auth_service(db)
    return auth_service.validate_token(token)


@router.post("/create-token", response_model=str)
async def create_token(
        user_id: int,
        db: Session = Depends(get_db_session),
        _: str = Depends(get_api_token)
):
    auth_service = get_auth_service(db)
    token = auth_service.token_repo.create(user_id)
    return token.token


@router.delete("/delete-token")
async def delete_token(
        token: str,
        db: Session = Depends(get_db_session),
        _: str = Depends(get_api_token)
):
    auth_service = get_auth_service(db)
    return auth_service.delete_token(token)
