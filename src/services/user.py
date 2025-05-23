from sqlalchemy.orm import Session

from src.repositories.user import UserRepository
from passlib.context import CryptContext
from fastapi import HTTPException, status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def create(self, username: str, telegram_id: int, password: str):
        if self.user_repo.get_by_username(username) or self.user_repo.get_by_telegram_id(telegram_id):
            raise HTTPException(status_code=400, detail="User already exists")
        hashed_password = pwd_context.hash(password)
        user = self.user_repo.create(username, telegram_id, hashed_password)
        return self.user_repo.to_entity(user)

    def get_all(self):
        return [self.user_repo.to_entity(user) for user in self.user_repo.db.query(self.user_repo.model).all()]

    def get_by_id(self, user_id: int):
        user = self.user_repo.db.query(self.user_repo.model).filter(self.user_repo.model.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return self.user_repo.to_entity(user)
