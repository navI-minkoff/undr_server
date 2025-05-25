from fastapi import Depends, HTTPException, status, Header
from src.entities.user import RoleEnum


def get_current_user_role(x_role: str = Header(...)):
    try:
        role = RoleEnum(x_role)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role")
    return role


def get_current_moder_or_admin(role: RoleEnum = Depends(get_current_user_role)):
    if role not in [RoleEnum.MODER, RoleEnum.ADMIN]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return role


def get_current_admin(role: RoleEnum = Depends(get_current_user_role)):
    if role != RoleEnum.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return role
