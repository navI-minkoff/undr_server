from src.repositories.base import BaseRepository
from src.models.user import User
from src.entities.user import UserEntity, RoleEnum


class UserRepository(BaseRepository):
    def get_by_username(self, username: str) -> User:
        return self.db.query(User).filter(User.username == username).first()

    def get_by_telegram_id(self, telegram_id: int) -> User:
        return self.db.query(User).filter(User.telegram_id == telegram_id).first()

    def create(self, username: str, telegram_id: int) -> User:
        user = User(username=username, telegram_id=telegram_id)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def to_entity(self, user: User) -> UserEntity:
        return UserEntity(
            id=user.id,
            username=user.username,
            telegram_id=user.telegram_id,
            role=user.role,
            created_at=user.created_at
        )
