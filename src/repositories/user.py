from collections.abc import Sequence

from sqlalchemy import select, delete

from src.core.logging import get_logger
from src.repositories.base import Repository
from src.models.user import User
from src.entities.user import UserEntity, RoleEnum

logger = get_logger(__name__)


class UserRepository(Repository[User]):
    table = User

    def list(self) -> Sequence[User]:
        query = select(self.table)

        result = self.session.execute(query)
        logger.info(event="Got users", result=result)

        return result.scalars().all()

    def get_by_id(self, user_id: int) -> User | None:
        query = select(self.table).where(self.table.id == user_id)
        result = self.session.execute(query)

        logger.info(event="Got user by id", user_id=user_id, result=result)

        return result.scalars().first()

    def get_by_username(self, username: str) -> User:
        query = select(self.table).where(self.table.username == username)
        result = self.session.execute(query)

        logger.info(event="Got user by username", username=username, result=result)

        return result.scalars().first()

    def get_by_telegram_id(self, telegram_id: int) -> User:
        query = select(self.table).where(self.table.telegram_id == telegram_id)
        result = self.session.execute(query)

        logger.info(event="Got user by telegram_id", telegram_id=telegram_id, result=result)

        return result.scalars().first()

    def create(self, username: str, telegram_id: int, role: str) -> User:
        user = self.table(
            username=username,
            telegram_id=telegram_id,
            role=role
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        logger.info(event="Created user", username=username, telegram_id=telegram_id, role=role, user_id=user.id)

        return user

    def delete_by_id(self, user_id: int):
        query = delete(self.table).where(self.table.id == user_id)
        result = self.session.execute(query)
        self.session.commit()

        logger.info(event="Deleted user by telegram_id", user_id=user_id, result=result)

    def delete_by_telegram_id(self, telegram_id: int):
        query = delete(self.table).where(self.table.telegram_id == telegram_id)
        result = self.session.execute(query)
        self.session.commit()

        logger.info(event="Deleted user by telegram_id", telegram_id=telegram_id, result=result)

    @staticmethod
    def to_entity(user: User) -> UserEntity:
        return UserEntity(id=user.id, username=user.username, telegram_id=user.telegram_id, role=user.role,
                          created_at=user.created_at)
