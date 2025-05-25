from pydantic import BaseModel
from datetime import datetime
from src.entities.user import RoleEnum


class UserBase(BaseModel):
    username: str
    telegram_id: int


class UserCreate(UserBase):
    role: RoleEnum


class UserResponse(UserBase):
    id: int
    role: RoleEnum
    created_at: datetime

    class Config:
        orm_mode = True
