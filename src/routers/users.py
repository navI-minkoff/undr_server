from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from starlette import status

from src.schemas.user import UserCreate, UserResponse
from src.services.user import UserService
from src.dependencies import get_db_session, get_current_moder_or_admin, get_current_admin
from src.entities.user import RoleEnum

router = APIRouter()


def get_user_service(db: Session = Depends(get_db_session)):
    return UserService(db)


@router.post("/", response_model=UserResponse)
async def create_user(
        user: UserCreate,
        db: Session = Depends(get_db_session),
        role: RoleEnum = Depends(get_current_moder_or_admin)
):
    user_service = get_user_service(db)
    if user.role == RoleEnum.MODER and role != RoleEnum.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only ADMIN can create MODER")
    return user_service.create(user.username, user.telegram_id, user.role.value)


@router.get("/", response_model=List[UserResponse])
async def read_users(db: Session = Depends(get_db_session)):
    user_service = get_user_service(db)
    return user_service.get_all()


@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: Session = Depends(get_db_session)):
    user_service = get_user_service(db)
    return user_service.get_by_id(user_id)


@router.delete("/{user_id}")
async def delete_user(
        user_id: int,
        db: Session = Depends(get_db_session),
        role: RoleEnum = Depends(get_current_moder_or_admin)
):
    user_service = get_user_service(db)
    user_to_delete = user_service.get_by_id(user_id)
    if user_to_delete.role == RoleEnum.MODER and role != RoleEnum.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only ADMIN can delete MODER")
    return user_service.delete(user_id)
