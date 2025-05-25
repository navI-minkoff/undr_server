from sqlalchemy import insert

from src.repositories.base import BaseRepository, Repository
from src.models.token import Token
from src.entities.token import TokenEntity
import secrets
from datetime import datetime, timedelta


class TokenRepository(Repository[Token]):
    TOKEN_LENGTH = 32
    TOKEN_EXPIRE_DAYS = 365
    table = Token

    def create(self, user_id: int) -> Token:
        token = secrets.token_urlsafe(self.TOKEN_LENGTH)
        expires = datetime.utcnow() + timedelta(days=self.TOKEN_EXPIRE_DAYS)
        db_token = Token(user_id=user_id, token=token, expires_at=expires)
        self.session.add(db_token)
        self.session.commit()
        self.session.refresh(db_token)

        return db_token

    def validate(self, token: str) -> dict:
        db_token = self.db.query(Token).filter(Token.token == token).first()
        if not db_token:
            return {"is_valid": False, "user_id": None, "message": "Token not found"}
        if not db_token.is_active:
            return {"is_valid": False, "user_id": None, "message": "Token is deactivated"}
        if db_token.expires_at < datetime.utcnow():
            return {"is_valid": False, "user_id": None, "message": "Token expired"}
        return {"is_valid": True, "user_id": db_token.user_id, "message": "Token is valid"}

    def to_entity(self, token: Token) -> TokenEntity:
        return TokenEntity(
            id=token.id,
            user_id=token.user_id,
            token=token.token,
            is_active=token.is_active,
            created_at=token.created_at,
            expires_at=token.expires_at
        )