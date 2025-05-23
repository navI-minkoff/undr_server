from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src import schemas, models
from src.auth import get_current_admin_user, get_current_user
from src.dependencies import get_db_session
from src.entities.user import RoleEnum
from src.schemas.user import UserCreate
from src.services.user import UserService

router = APIRouter()


@router.post("/", response_model=schemas.user.UserResponse)
async def create_user(user: schemas.user.UserCreate, db: Session = Depends(get_db_session)):
    user_service = UserService(db)
    return user_service.create(user.username, user.telegram_id, user.password)


@router.get("/", response_model=List[schemas.user.UserResponse])
async def read_users(db: Session = Depends(get_db_session),
                     current_user: models.user.User = Depends(get_current_admin_user)):
    user_service = UserService(db)
    return user_service.get_all()


@router.get("/{user_id}", response_model=schemas.user.UserResponse)
async def read_user(user_id: int, db: Session = Depends(get_db_session),
                    current_user: models.user.User = Depends(get_current_user)):
    user_service = UserService(db)
    user = user_service.get_by_id(user_id)
    if current_user.role != RoleEnum.ADMIN and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return user
