from sqlalchemy import Column, Integer, String, Enum, BigInteger, DateTime
from sqlalchemy.sql import func
from src.models.base import Base

from src.entities.user import RoleEnum


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True)
    role = Column(Enum(RoleEnum), default=RoleEnum.USER)
    created_at = Column(DateTime(timezone=True), server_default=func.now())