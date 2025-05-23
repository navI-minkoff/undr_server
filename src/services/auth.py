from src.repositories.user import UserRepository
from src.repositories.token import TokenRepository
from passlib.context import CryptContext
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
        self.token_repo = TokenRepository(db)

    def login(self, username: str, password: str) -> str:
        user = self.user_repo.get_by_username(username)
        if not user or not pwd_context.verify(password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
        token = self.token_repo.create(user.id)
        return token.token

    def validate_token(self, token: str) -> dict:
        return self.token_repo.validate(token)
