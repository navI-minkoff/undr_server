from datetime import datetime
from enum import Enum


class RoleEnum(str, Enum):
    USER = "USER"
    MODER = "MODER"
    ADMIN = "ADMIN"


class UserEntity:
    def __init__(self
                 , id: int
                 , username: str
                 , telegram_id: int
                 , role: RoleEnum
                 , created_at: datetime):
        self.id = id
        self.username = username
        self.telegram_id = telegram_id
        self.role = role
        self.created_at = created_at
