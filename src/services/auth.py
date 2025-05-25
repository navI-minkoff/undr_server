from src.models.token import Token
from src.repositories.token import TokenRepository
from fastapi import HTTPException, status
from sqlalchemy.orm import Session


class AuthService:
    def __init__(self, db: Session):
        self.token_repo = TokenRepository(db)

    def validate_token(self, token: str) -> dict:
        return self.token_repo.validate(token)

    def delete_token(self, token: str) -> bool:
        db_token = self.token_repo.db.query(Token).filter(Token.token == token).first()
        if not db_token:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Token not found")
        self.token_repo.db.delete(db_token)
        self.token_repo.db.commit()
        return True
