from src.repositories.user import UserRepository
from src.repositories.token import TokenRepository
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.entities.user import RoleEnum, UserEntity
from typing import List


class UserService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
        self.token_repo = TokenRepository(db)
        self.db = db

    def create(self, username: str, telegram_id: int, role: str):
        if self.user_repo.get_by_username(username) or self.user_repo.get_by_telegram_id(telegram_id):
            raise HTTPException(status_code=400, detail="User already exists")
        user = self.user_repo.create(username, telegram_id, role)
        if role in [RoleEnum.USER, RoleEnum.MODER]:
            self.token_repo.create(user.id)
        return self.user_repo.to_entity(user)

    def get_all(self) -> List[UserEntity]:
        users = self.user_repo.list()
        return [self.user_repo.to_entity(user) for user in users]

    def get_by_id(self, user_id: int) -> UserEntity:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return self.user_repo.to_entity(user)

    def get_by_telegram_id(self, telegram_id: int) -> UserEntity:
        user = self.user_repo.get_by_telegram_id(telegram_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return self.user_repo.to_entity(user)

    def delete(self, user_id: int):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        try:
            self.db.delete(user)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to delete user: {str(e)}")
