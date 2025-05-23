from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.entities.user import RoleEnum
from src.services.auth import AuthService
from src.dependencies import get_db_session
from src.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_session)):
    auth_service = AuthService(db)
    validation = auth_service.validate_token(token)
    if not validation["is_valid"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=validation["message"])
    user = db.query(User).filter(User.id == validation["user_id"]).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return current_user
